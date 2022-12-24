from flask import Flask, render_template, request, redirect, url_for, send_file
from typing import NamedTuple
from datetime import datetime
import os
import logging

from ..invoicer.generate_invoice import InvoiceGenerator

INPUT_PATH = "input/"
OUTPUT_PATH = "output/"

TEMPLATE_PATH = "input/template.docx"

# For templates, HTML and response files
CSV_FILE_ID = "csv_file"
MD_FILE_ID = "md_file"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class FinalFile(NamedTuple):
    caption: str
    href: str
    path_from_server_root: str
    creation_datetime: str


app = Flask(__name__)
# logging.basicConfig(filename='demo.log', level=logging.DEBUG)


def get_final_files(path: str) -> list[FinalFile]: 
    files = scan_filenames(path)
    final_files: list[FinalFile] = []

    for filename in files:
        path_from_server_root = f"{path}{filename}"
        final_file = FinalFile(caption=filename, 
                               href=filename, 
                               path_from_server_root=path_from_server_root, 
                               creation_datetime=get_creation_date(path_from_server_root))
                            
        final_files.append(final_file)
    return final_files
    

def scan_filenames(path: str) -> list[str]:
    files = []
    filenames = os.listdir(path)
    filenames.sort()
    for filename in filenames:
        files.append(filename)
    return files


def get_creation_date(path: str) -> str:
    creation_timestamp = os.path.getctime(path)
    creation_datetime = datetime.fromtimestamp(creation_timestamp)
    return creation_datetime.strftime(DATETIME_FORMAT)
    


def generate_invoices(csv_path: str, md_path: str, template_path: str = TEMPLATE_PATH):
    invoicer = InvoiceGenerator(md_path, csv_path, template_path) 
    invoicer.generate()
    
# -------------------------------------------------------


@app.route("/", methods=["GET", "POST"])
def index_page():
    if request.method == "POST":
        return redirect(url_for("download_page"))
    else:
        return render_template("index.html", CSV_FILE_ID=CSV_FILE_ID, MD_FILE_ID=MD_FILE_ID)
    
@app.route("/upload", methods=["GET", "POST"])
def upload_input():
    if request.method == "GET":
        return redirect(url_for("download_page"))
    if request.method == "POST":
        csv_file = request.files[CSV_FILE_ID]
        md_file = request.files[MD_FILE_ID]

        csv_path = f"{INPUT_PATH}input.csv"
        md_path = f"{INPUT_PATH}input.md"

        request.files[CSV_FILE_ID].save(csv_path)
        request.files[MD_FILE_ID].save(md_path)
        
        generate_invoices(csv_path, md_path)
        return redirect(url_for("download_page"))
    else:
        raise Exception(f"wtf. method: {request.method}")


@app.route("/download")
def download_page():
    return render_template("download.html", files=get_final_files(OUTPUT_PATH))


@app.route("/download/<path:filename>")
def download_file(filename: str):
    return send_file(f"{OUTPUT_PATH}/{filename}")
    
    
if __name__ == "__main__":
    app.run()
