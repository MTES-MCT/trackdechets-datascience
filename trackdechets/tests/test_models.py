
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

    def test_bulk_create(self):
        """ it should create records in bulk """
        vhus = [
            {
                'departement': '07',
                'raison_sociale': 'Casse Auto',
                'numero_agrement': '1',
                'siren': '98675435',
                'date_debut_validite': datetime(2019, 1, 1),
                'date_fin_validite': datetime(2019, 2, 1)
            },
            {
                'departement': '26',
                'raison_sociale': 'Broyage Auto',
                'numero_agrement': '2',
                'siren': '785643',
                'date_debut_validite': datetime(2019, 1, 1),
                'date_fin_validite': datetime(2019, 2, 1)
            }
        ]
        VHU.bulk_create(vhus)
        count = VHU.select().count()
        self.assertEqual(count, 2)

    def test_create_from_siv_pdf(self):
        """ it should load data from the SIV pdf """
        VHU.create_from_siv_pdf(pages='1')
        count = VHU.select().count()
        self.assertEqual(count, 73)


class RubriqueTestCase(BaseTestCase):

    def test_create_from_icpe_table(self):

        data = {
            'id': 1,
            'geom': '01040000206A0800000100000001010000000000000070E0244100000000A92E5A41',
            'code_s3ic': '0065.00509',
            'x': 684088,
            'y': 6863524,
            'epsg': 2154,
            'nom_ets': 'SCETA',
            'num_dep': '77',
            'cd_insee': '77111',
            'cd_postal': '77700',
            'nomcommune': 'CHESSY',
            'code_naf': None,
            'lib_naf': None,
            'num_siret': None,
            'regime': None,
            'lib_regime': None,
            'ippc': 0, 'seveso':
            'NS', 'lib_seveso':
            'Non Seveso',
            'famille_ic': 'Industries',
            'url_fiche': 'http://www.installationsclassees.developpement-durable.gouv.fr/ficheEtablissement.php?champEtablBase=65&champEtablNumero=509',
            'rayon': None,
            'precis_loc': 3,
            'lib_precis': 'Valeur Initiale'}
        ICPE.create(**data)
        Rubrique.create_from_icpe_table()
        count = Rubrique.select().count()
        self.assertEqual(count, 1)
