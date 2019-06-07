
import requests
import os
import io
import csv
import tempfile
import zipfile
import shutil

import xlrd

from .config import IREP_DOWNLOAD_URL, IREP_ETABLISSEMENTS_FILENAME
from .config import GEREP_FILE_PATH, GEREP_PRODUCTEURS_SHEET, \
    GEREP_TRAITEURS_SHEET
from .utils import spreadsheet2array


def get_irep_data():
    """ retrieves and parse IREP data from georisques """
    with tempfile.TemporaryDirectory() as tmp:
        response = requests.get(IREP_DOWNLOAD_URL, stream=True)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file.extract(IREP_ETABLISSEMENTS_FILENAME, tmp)
        csv_path = os.path.join(tmp, IREP_ETABLISSEMENTS_FILENAME)
        with open(csv_path) as csv_file:
            reader = csv.DictReader(
                csv_file,
                delimiter=',')
            return list(reader)


def get_gerep_data():
    """ Retrieves GEREP data from Excel file """
    with xlrd.open_workbook(GEREP_FILE_PATH) as wb:
        producteurs_sh = wb.sheet_by_name(GEREP_PRODUCTEURS_SHEET)
        traiteurs_sh = wb.sheet_by_name(GEREP_TRAITEURS_SHEET)
        offset = 3
        producteurs = spreadsheet2array(producteurs_sh, offset)
        traiteurs = spreadsheet2array(traiteurs_sh, offset)
        return (producteurs, traiteurs)
