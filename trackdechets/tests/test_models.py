
from unittest import TestCase
from datetime import datetime

from peewee import *

from ..config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_HOST, \
    POSTGRES_USER, POSTGRES_PWD, POSTGRES_PORT
from ..models import VHU, ICPE, Rubrique


test_db = PostgresqlDatabase(
    '%s_test' % POSTGRES_DB,
    host=POSTGRES_HOST,
    user=POSTGRES_USER,
    password=POSTGRES_PWD,
    port=POSTGRES_PORT)


MODELS = [VHU, ICPE, Rubrique]


class BaseTestCase(TestCase):

    def setUp(self):
        # Bind model classes to test db
        test_db.bind(MODELS)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS, cascade=True)
        test_db.close()


class VHUTestCase(BaseTestCase):

    def test_create_from_siv_pdf(self):
        """ it should load data from the SIV pdf """
        VHU.create_from_siv_pdf(pages='1')
        count = VHU.select().count()
        self.assertEqual(count, 73)
