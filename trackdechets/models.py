# -*- coding: utf-8 -*-

from peewee import *

from .config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_HOST, POSTGRES_USER, \
    POSTGRES_PWD, POSTGRES_PORT


db = PostgresqlDatabase(
    POSTGRES_DB,
    host=POSTGRES_HOST,
    user=POSTGRES_USER,
    password=POSTGRES_PWD,
    port=POSTGRES_PORT)


class BaseModel(Model):

    class Meta:
        database = db


class VHU(BaseModel):

    departement = CharField()
    raison_sociale = CharField()
    numero_agrement = CharField()
    siren = CharField()
    date_debut_validite = DateTimeField()
    date_fin_validite = DateTimeField()

db.connect()

db.create_tables([
    VHU
])

