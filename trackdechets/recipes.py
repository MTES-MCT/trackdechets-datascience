from datetime import datetime
import zipfile

import camelot
import pandas as pd

from .models import db, VHU
from .sirene import get_entreprise


def extract_vhu_from_pdf(pdf_file):
    """ extract tables from the VHU pdf available at the SIV website
    https://immatriculation.ants.gouv.fr/Documents-Pro/Referentiels/Centres-VHU
    """
    tables = camelot.read_pdf(pdf_file, pages='all')
    frames = [table.df for table in tables]
    df = pd.concat(frames)
    df = df.drop([0])
    # skip first row and add headers
    columns = [
        VHU.departement.column_name,
        VHU.raison_sociale.column_name,
        VHU.numero_agrement.column_name,
        'siren',
        'date_debut_validite',
        'date_fin_validite'
    ]
    df.columns = columns
    date_format = '%d/%m/%Y'
    df['date_debut_validite'] = pd.to_datetime(df['date_debut_validite'],
                                               format=date_format)
    df['date_fin_validite'] = pd.to_datetime(df['date_fin_validite'],
                                             format=date_format)
    data = df.to_dict(orient='records')
    return data


def bulk_insert_vhu(data):
    """ Insert VHU data in bulk """
    with db.atomic():
        VHU.insert_many(data).execute()
