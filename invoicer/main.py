from typing import NamedTuple
from loguru import logger
from generate_invoice import InvoiceGenerator
from parse_ids import parse_ids


logger.add("debug.log")
tsv_filename = 'Магазины За ХЛЕБ! - Main info.tsv'


class WeekIDs(NamedTuple):
    #monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


def read_id_lines(filename: str) -> list[str]:
    with open(filename, "r") as file:
        text = file.read()
        id_lines = text.splitlines()
                
        for index, line in enumerate(id_lines):
            if not line:
                del id_lines[index]
            else:
                id_lines[index] = line.strip()
        return id_lines
            


if __name__ == "__main__":
    raw_ids_filename = "target.md"
    ids_filename = "ids.md"
    
    parse_ids(raw_ids_filename, ids_filename)
    id_lines = read_id_lines(ids_filename)
    
    
    logger.debug(id_lines)
    
    generators: list[InvoiceGenerator] = [
        InvoiceGenerator(id_lines[0], "template.docx", input_shops_filename=tsv_filename, output_name="2. Вторник"),
        InvoiceGenerator(id_lines[1], "template.docx", input_shops_filename=tsv_filename, output_name="3. Среда"),
        InvoiceGenerator(id_lines[2], "template.docx", input_shops_filename=tsv_filename, output_name="4. Четверг"),
        InvoiceGenerator(id_lines[3], "template.docx", input_shops_filename=tsv_filename, output_name="5. Пятница"),
        InvoiceGenerator(id_lines[4], "template.docx", input_shops_filename=tsv_filename, output_name="6. Суббота"),
        InvoiceGenerator(id_lines[5], "template.docx", input_shops_filename=tsv_filename, output_name="7. Воскресенье"),
    ]
    
    for generator in generators:
        generator.generate_file()

