
from unittest import TestCase

from ..loaders import load_irep_data, load_gerep_data


class LoadersTestCase(TestCase):

    def test_load_irep_data(self):
        load_irep_data()

    def test_load_gerep_data(self):
        load_gerep_data()
