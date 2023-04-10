from flask import Flask, render_template, request, redirect, url_for, send_file
from typing import NamedTuple
from datetime import datetime
import os
import logging

from ..invoicer.generate_invoice import InvoiceGenerator

# Paths

INPUT_PATH = "input/"
TSV_INPUT_PATH = f"{INPUT_PATH}input.tsv"
MD_INPUT_PATH = f"{INPUT_PATH}input.md"

OUTPUT_PATH = "output/"

TEMPLATE_PATH = "input/template.docx"

# For templates, HTML and response files
TSV_FILE_ID = "tsv_file"
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
    


def generate_invoices(tsv_path: str, md_path: str, template_path: str = TEMPLATE_PATH):
    invoicer = InvoiceGenerator(md_path, tsv_path, template_path) 
    invoicer.generate_all()


def there_is_request_file(file_id):
    if file_id in request.files:
        if request.files[file_id].filename:
            return True
    # If enything is not True    
    return False
    
# -------------------------------------------------------


@app.route("/", methods=["GET", "POST"])
def index_page():
    if request.method == "POST":
        return redirect(url_for("download_page"))
    else:
        return render_template("index.html", TSV_FILE_ID=TSV_FILE_ID, MD_FILE_ID=MD_FILE_ID)
    
@app.route("/upload", methods=["GET", "POST"])
def upload_input():
    if request.method == "GET":
        return redirect(url_for("download_page"))
    if request.method == "POST":
        
        if there_is_request_file(TSV_FILE_ID):
            request.files[TSV_FILE_ID].save(TSV_INPUT_PATH)
        if there_is_request_file(MD_FILE_ID):
            request.files[MD_FILE_ID].save(MD_INPUT_PATH)
        
            
        # Input files are optional. Recent files can be used
        # if :
        # if MD_FILE_ID in request.files:
        # except IndexError
        generate_invoices(TSV_INPUT_PATH, MD_INPUT_PATH)
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
