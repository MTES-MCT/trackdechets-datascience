
from unittest import TestCase, mock

from ..recipes import create_rubriques, filter_icpe_27xx_35xx, \
    prepare_irep, join_icpe_irep, prepare_gerep


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

    def test_filter_icpe_27xx_35xx(self):
        filter_icpe_27xx_35xx()

    def test_prepare_irep(self):
        from ..models import db, IREP_Prepared
        db.connect()
        db.create_tables([IREP_Prepared])
        prepare_irep()

    def test_join_icpe_irep(self):
        from ..models import db, ICPE_join_IREP
        db.connect()
        db.create_tables([ICPE_join_IREP])
        join_icpe_irep()

    def test_prepare_gerep(self):
        from ..models import db, GEREP_prepared
        db.connect()
        db.create_tables([GEREP_prepared])
        prepare_gerep()

