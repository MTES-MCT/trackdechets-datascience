
from unittest import TestCase

from ..loaders import load_irep_data


class LoadersTestCase(TestCase):

    def test_load_irep_data(self):
        load_irep_data()