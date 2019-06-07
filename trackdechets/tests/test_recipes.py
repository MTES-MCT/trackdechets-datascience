
from unittest import TestCase, mock

from ..recipes import create_rubriques


class RecipesTestCase(TestCase):

    @mock.patch('trackdechets.recipes.ICPE')
    @mock.patch('trackdechets.recipes.Rubrique')
    @mock.patch('trackdechets.recipes.IcpeScraper')
    def test_create_rubriques(self, mock_IcpeScraper,
                              mock_Rubrique, mock_ICPE):

        mock_icpe = mock.Mock()
        mock_icpe.code_s3ic = 's3ic'
        mock_icpe.url_fiche = 'url'

        mock_ICPE.select.return_value = [mock_icpe]

        mock_scraper = mock.Mock()
        mock_IcpeScraper.return_value = mock_scraper
        mock_scraper.rubriques = ['2765', '3567']

        create_rubriques()

    def test_create_rubriques_real(self):
        from ..models import db, Rubrique
        db.connect()
        db.create_tables([Rubrique])
        create_rubriques()
