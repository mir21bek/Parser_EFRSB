from openpyxl import Workbook
import pandas as pd


def create_file(list_info, file_name):
    workbook = Workbook()
    sheet = workbook["Sheet"]
    headers_wb = [
        "ФИО АУ",
        "Ссылка на АУ",
        "ИНН АУ",
        "СРО АУ",
        "Название должника",
        "Ссылка на должника",
        "ИНН должника",
    ]

    sheet.append(headers_wb)
    for row in list_info:
        sheet.append(row)

    workbook.save(file_name)


def read_file(file_name: str) -> list:
    data = pd.read_excel(file_name, usecols='A')
    column_a_list = data.iloc[:, 0].tolist()

    return column_a_list
