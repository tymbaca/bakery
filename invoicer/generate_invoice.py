from classes.shops import *
from loguru import logger
from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document

import shops_parser
import parse_ids


logger.add("debug.log")
TEMP_FOLDER = "tmp/"
RESULT_FOLDER = "Result/"


OUTPUT_FILENAMES = [
    "2. Вторник",
    "3. Среда",
    "4. Четверг",
    "5. Пятница",
    "6. Суббота",
    "7. Воскресенье",
]


class InvalidShopIDError(Exception):
    pass


class InvoiceGeneratorInitError(Exception):
    pass


class NotCreatedFunctionalityError(Exception):
    pass


class InvoiceGenerator:
    def __init__(self,
                 raw_ids_filename: str,
                 template_filename: str,
                 input_shops_filename: str = "target.tsv",
                 output_name: str = "Generated_Invoice",
                 ids_separator: str = " ",
                 start_count_from=1):

        # self.ids = ids_string.split(ids_separator)
        # self.ids_string = ids_string
        # self.ids_separator = ids_separator
        
        self.ids_by_days: list[list[str]] = parse_ids._parse_ids(raw_ids_filename)
        
        self.template_filename = template_filename
        self.output_name = output_name
        self.start_count_from = start_count_from
        self.shops = InvoiceGenerator.parse_shops(input_shops_filename)
        self._input_shops_filename = input_shops_filename

        # Existing files analysis can be here
        self.invoices_filenames: list[str] = []

    @staticmethod
    def parse_shops(input_shops_filename: str) -> list[Shop]:
        try:
            return shops_parser.parse_shops(input_shops_filename)
        except FileNotFoundError as err:
            message = f"No such file in directory: {input_shops_filename}"
            logger.error(message)
            raise err
        except OSError as err:
            message = f"""Check input file name type (must be string). Current filename: 
                - name: {input_shops_filename}
                - type: {type(input_shops_filename)}"""
            logger.error(message)
            raise err
        except Exception as err:
            logger.error(err)
            raise err

    def generate_empty_file(self) -> None:
        
    
    def generate_merged_file(self, do_all: bool = True) -> None:
        """
        Generates final merged file. Can do only merging or also call other functions needed to do all process.

            - do_all: [bool] Need to repair.
        """
        if do_all is True:
            self.generate_files()
        else:
            err_message = "do_all argument functionality is not created yet. Put it on True (default value)"
            logger.error(err_message)
            raise NotCreatedFunctionalityError(err_message)

        err_message = "There is no invoice files generated. You can turn do_all to True to do it automatically"
        try:
            assert len(self.invoices_filenames) > 0, err_message
        except AssertionError as err:
            logger.error(err_message)
            raise err

        if len(self.invoices_filenames) == 1:
            self._rename_alone_docx()
            logger.info(f"There was only one invoice file {self.invoices_filenames[0]}. It was renamed {self.output_name}.docx")
            return
        else:
            self._merge_files()

    def _merge_files(self):
        master = Document(f"{TEMP_FOLDER}{self.invoices_filenames[0]}")
        composer = Composer(master)
        for filename in self.invoices_filenames[1:]:
            doc = Document(f"{TEMP_FOLDER}{filename}")
            composer.append(doc)
        composer.save(f"{RESULT_FOLDER}{self.output_name}.docx")
        logger.info(f"Merged file generated: {self.output_name}.docx")

    def _rename_alone_docx(self):
        filename = self.invoices_filenames[0]
        doc = Document(filename)
        doc.save(self.output_name + ".docx")

    def generate_files(self) -> None:
        count = self.start_count_from
        for shop_id in self.ids:
            # Creating filename and
            invoice_filename = f"{self.output_name}_{count}.docx"

            # Appending it to filenames stack
            self.invoices_filenames.append(invoice_filename)

            self.generate_invoice(invoice_filename, shop_id)
            count += 1

    def generate_invoice(self, invoice_filename: str, shop_id: str) -> None:
        doc = DocxTemplate(self.template_filename)
        shop = self._find_shop(shop_id)
        context = self._generate_context(shop)
        doc.render(context)
        doc.save(f"{TEMP_FOLDER}{invoice_filename}")

        logger.info(f"Invoice file generated (Shop info: {shop})")

    def _find_shop(self, shop_id) -> Shop:
        for shop in self.shops:
            if shop.id == shop_id:
                return shop

        # If shop wasn't found
        message = f"Invalid ID: there are no shop with current ID ({shop_id}). Please check ID list or original TSV file"
        logger.error(message)
        raise InvalidShopIDError(message)

    @staticmethod
    def _generate_context(shop) -> dict[str, str]:
        context = {
            "organisation": shop.organisation,
            "address": shop.address
        }
        return context


if __name__ == "__main__":
    id_input = "6 35 30 22 37 56"
    # id_input = "6"
    generator = InvoiceGenerator(input_shops_filename="Shops.tsv", ids_string=id_input, template_filename="Template.docx", output_name="Someday")
    generator.generate_merged_file()
    pass
