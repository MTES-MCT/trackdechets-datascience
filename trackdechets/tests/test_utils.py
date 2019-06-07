
import os
from unittest import TestCase

import xlrd

from ..utils import spreadsheet2array


class UtilsTestCase(TestCase):

    def test_spreadsheet2array(self):
        """ it should convert a spreadsheet table to an array """
        dirname = os.path.dirname(os.path.realpath(__file__))
        xlsx_path = os.path.join(dirname, 'data', 'test.xlsx')
        with xlrd.open_workbook(xlsx_path) as wb:
            sh = wb.sheet_by_name('test')
            data = spreadsheet2array(sh, 1)
            expected = [
                {'column1': 'cell11', 'column2': 'cell12', 'column3': 'cell13'},
                {'column1': 'cell21', 'column2': 'celle22', 'column3': 'cell23'}]
            self.assertEqual(data, expected)