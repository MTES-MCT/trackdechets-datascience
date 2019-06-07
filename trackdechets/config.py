# -*- coding: utf-8 -*-

import os


# POSTGRESQL CONFIGURATION

POSTGRES_DB = 'trackdechets'

POSTGRES_HOST = os.environ['POSTGRES_HOST']

POSTGRES_USER = os.environ['POSTGRES_USER']

POSTGRES_PWD = os.environ['POSTGRES_PWD']

POSTGRES_PORT = os.environ['POSTGRES_PORT']

# VHU CONFIGURATION

SIV_CENTRES_VHU_FILE_PATH = './data/VHU/Centres_VHU_20190517.pdf'


# IREP CONFIGURATION

IREP_DOWNLOAD_URL = 'http://www.georisques.gouv.fr/irep/data/2017'
IREP_ETABLISSEMENTS_FILENAME = 'etablissements.csv'


# GEREP CONFIGURATION

GEREP_FILE_PATH = './data/GEREP/GEREP-2016-2017.xlsx'
GEREP_PRODUCTEURS_SHEET = 'Etablissements producteurs'
GEREP_TRAITEURS_SHEET = 'Etablissements traiteurs'
