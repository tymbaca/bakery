import csv
import tomllib
from loguru import logger
from classes.shops import *


logger.add("debug.log")
COL_INDEXES = {}  # See _update_column_indexes function docstring
# with open("config.toml", "rb") as file:
#     CONFIG = tomllib.load(file)


class InvalidShopDataError(Exception):
    pass


def parse_shops(tsv_filename: str, table_header=True, separator="\t") -> list[Shop]:
    data = _parse_data(tsv_filename, table_header, separator)
    shops = _build_shops(data)
    return shops


def _parse_data(tsv_filename: str, table_header, separator) -> list[list[str]]:
    with open(tsv_filename, "r") as file:
        lines = file.read().splitlines()
        data = _split_lines(lines, separator)

        if table_header:
            _update_column_indexes(data[0])
            return data[1:]
        else:
            return data


def _split_lines(lines: list[str], separator) -> list[list[str]]:
    new_lines = []
    for line in lines:
        try:
            new_lines.append(line.split(separator))
        except TypeError as error:
            print("Incorrect separator. Must be str")
            raise error
    return new_lines


def _update_column_indexes(header: list[str]):
    """Matches Column Indexes and Column Names. Now you can safely change column priority in your Shops Table file.
    Important! Update functions when changing Column Names in Shop Table file"""
    for index, name in enumerate(header):
        COL_INDEXES[name] = index


def _build_shops(data: list[list[str]]) -> list[Shop]:
    shops = []
    for raw_shop in data:
        try:
            shop = _build_shop(raw_shop)
            shops.append(shop)
        except InvalidShopDataError:
            continue
    return shops


def _build_shop(raw_shop: list[str]) -> Shop:
    try:
        id = raw_shop[COL_INDEXES["ID"]]
        organisation = raw_shop[COL_INDEXES["Organisation Name"]]
        department = raw_shop[COL_INDEXES["Org. Department"]]
        address = raw_shop[COL_INDEXES["Full Address"]]
        if organisation == "":
            logger.debug(f"Shop (ID: {id}) have not organisation name.")
            raise InvalidShopDataError("Organisation name is empty")
        shop = Shop(id, organisation + department, address)
        logger.info(f"Built Shop instance: {shop}")
        return shop
    except KeyError:
        message = "Make sure your"
    

if __name__ == "__main__":
    ...
