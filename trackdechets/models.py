# -*- coding: utf-8 -*-

import requests
from peewee import *
import camelot

from .config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_HOST, POSTGRES_USER, \
    POSTGRES_PWD, POSTGRES_PORT, SIV_CENTRES_VHU_FILE_PATH
from .scrapers import RUBRIQUE, ALINEA, DATE_AUTORISATION, ETAT_ACTIVITE, \
    REGIME_AUTORISE, ACTIVITE, VOLUME, UNITE


db = PostgresqlDatabase(
    POSTGRES_DB,
    host=POSTGRES_HOST,
    user=POSTGRES_USER,
    password=POSTGRES_PWD,
    port=POSTGRES_PORT)


class BaseModel(Model):

    class Meta:
        database = db


class GeometryField(Field):

    field_type = 'geometry'


class VHU(BaseModel):

    departement = CharField()
    raison_sociale = CharField()
    numero_agrement = CharField()
    siren = CharField()
    date_debut_validite = DateTimeField()
    date_fin_validite = DateTimeField()

    @classmethod
    def create_from_siv_pdf(cls, pages='all'):
        """
        create VHU records from the pdf published by the SIV at
        https://immatriculation.ants.gouv.fr/Documents-Pro/Referentiels/Centres-VHU
        """
        tables = camelot.read_pdf(SIV_CENTRES_VHU_FILE_PATH, pages=pages)
        frames = [table.df for table in tables]
        df = pd.concat(frames)
        # skip first row and add headers
        df = df.drop([0])
        columns = [
            cls.departement.column_name,
            cls.raison_sociale.column_name,
            cls.numero_agrement.column_name,
            cls.siren.column_name,
            cls.date_debut_validite.column_name,
            cls.date_fin_validite.column_name
        ]
        df.columns = columns
        date_format = '%d/%m/%Y'
        df[cls.date_debut_validite.column_name] = pd.to_datetime(
            df[cls.date_debut_validite.column_name],
            format=date_format)
        df[cls.date_fin_validite.column_name] = pd.to_datetime(
            df[cls.date_fin_validite.column_name],
            format=date_format)
        vhus = df.to_dict(orient='records')
        cls.insert_many(vhus)


class ICPE(BaseModel):

    geom = GeometryField(null=True)
    code_s3ic = CharField(max_length=10, null=True)
    x = BitField(null=True)
    y = BitField(null=True)
    epsg = BitField(null=True)
    nom_ets = CharField(null=True)
    num_dep = CharField(max_length=80, null=True)
    cd_insee = CharField(max_length=5, null=True)
    cd_postal = CharField(max_length=5, null=True)
    nomcommune = CharField(max_length=40, null=True)
    code_naf = CharField(max_length=6, null=True)
    lib_naf = CharField(max_length=254, null=True)
    num_siret = CharField(max_length=14, null=True)
    regime = CharField(max_length=4, null=True)
    lib_regime = CharField(max_length=50, null=True)
    ippc = BitField(null=True)
    seveso = CharField(max_length=3, null=True)
    lib_seveso = CharField(max_length=20, null=True)
    famille_ic = CharField(max_length=80, null=True)
    url_fiche = CharField(max_length=127, null=True)
    rayon = BitField(null=True)
    precis_loc = BitField(null=True)
    lib_precis = CharField(max_length=80, null=True)


class Rubrique(BaseModel):

    icpe_id = ForeignKeyField(ICPE, backref='rubriques')
    rubrique = CharField()
    alinea = CharField()
    date_autorisation = CharField()
    etat_activite = CharField()
    regime_autorise = CharField()
    activite = TextField()
    volume = CharField()
    unite = CharField()

    @classmethod
    def from_rubrique_scraped(cls, icpe_id, rubrique):
        """
        return an instance of Rubrique from a dict
        parsed by the scraper
        """
        data = {
            cls.icpe_id.column.name: icpe_id,
            cls.rubrique.column.name: rubrique[RUBRIQUE],
            cls.alinea.column.name: rubrique[ALINEA],
            cls.date_autorisation.column.name: rubrique[DATE_AUTORISATION],
            cls.etat_activite.column.name: rubrique[ETAT_ACTIVITE],
            cls.regime_autorise.column.name: rubrique[REGIME_AUTORISE],
            cls.activite.column.name: rubrique[ACTIVITE],
            cls.volume.column.name: rubrique[VOLUME],
            cls.unite.column.name: rubrique[UNITE]
        }

        return cls(**data)



class ICPE_27_35(ICPE):
    """ ICPE table filtered for """
    pass


