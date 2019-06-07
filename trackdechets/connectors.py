
import requests
import os
import io
import csv
import tempfile
import zipfile
import shutil

from .config import IREP_DOWNLOAD_URL, IREP_ETABLISSEMENTS_FILENAME


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