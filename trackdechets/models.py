# -*- coding: utf-8 -*-

import grequests
import requests
from peewee import *
import camelot
import pandas as pd

from .config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_HOST, POSTGRES_USER, \
    POSTGRES_PWD, POSTGRES_PORT, SIV_CENTRES_VHU_FILE_PATH
from .utils import parse_icpe_fiche_detail


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
    def bulk_create(cls, data):
        """ Insert VHU data in bulk """
        with db.atomic():
            cls.insert_many(data).execute()

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
        cls.bulk_create(vhus)


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
    def bulk_create(cls, data):
        """ Insert Rubrique data in bulk """
        with db.atomic():
            cls.insert_many(data).execute()

    @classmethod
    def create_from_icpe_table_async(cls):
        """ extract rubrique information from the ICPE's fiche url """
        query = ICPE.select()
        urls = [icpe.url_fiche for icpe in query]
        icpe_ids = [icpe.id for icpe in query]
        requests = (grequests.get(u) for u in urls)
        responses = grequests.map(requests)
        htmls = [
            (icpe_id, response.text) for
            (icpe_id, response) in
            list(zip(icpe_ids, responses))]

        data = [
            (icpe_id, parse_icpe_fiche_detail(html)) for
            (icpe_id, html)
            in htmls]

        flatlist = []

        for (icpe_id, rubriques) in data:
            for rubrique in rubriques:
                flatlist.append((icpe_id, rubrique))

        rubriques = [{
            cls.icpe_id.column: icpe_id,
            cls.rubrique.column: rubrique['Rubri. IC'],
            cls.alinea.column: rubrique['Ali.'],
            cls.date_autorisation.column: rubrique['Date auto.'],
            cls.etat_activite.column: rubrique['Etat d\'activité'],
            cls.regime_autorise.column: rubrique['Régime autorisé(3)'],
            cls.activite.column: rubrique['Activité'],
            cls.volume.column: rubrique['Volume'],
            cls.unite.column: rubrique['Unité']
        } for (icpe_id, rubrique) in flatlist]

        cls.bulk_create(rubriques)

    @classmethod
    def create_from_icpe_table(cls):
        query = ICPE.select()
        rubriques = []
        for icpe in query:
            response = requests.get(icpe.url_fiche)
            html = response.text
            parsed = parse_icpe_fiche_detail(html)
            for r in parsed:
                rubrique = {
                    cls.icpe_id.column_name: icpe.id,
                    cls.rubrique.column_name: r['Rubri. IC'],
                    cls.alinea.column_name: r['Ali.'],
                    cls.date_autorisation.column_name: r['Date auto.'],
                    cls.etat_activite.column_name: r['Etat d\'activité'],
                    cls.regime_autorise.column_name: r['Régime autorisé(3)'],
                    cls.activite.column_name: r['Activité'],
                    cls.volume.column_name: r['Volume'],
                    cls.unite.column_name: r['Unité']
                }
                cls.create(**rubrique)
