
import os
from unittest import TestCase, mock

from ..connectors import get_irep_data, get_gerep_data


class ConnectorsTestCase(TestCase):

    @mock.patch('trackdechets.connectors.requests')
    def test_get_irep_data(self, mock_requests):
        """ it should retrieve and parse IREP data """
        mock_response = mock.Mock()
        dirname = os.path.dirname(os.path.realpath(__file__))
        mock_data_path = os.path.join(dirname, 'data', 'irep.zip')
        with open(mock_data_path, 'rb') as f:
            mock_response.content = f.read()
        mock_requests.get.return_value = mock_response
        data = get_irep_data()
        self.assertEqual(len(data), 9)

    def test_get_gerep_data(self):
        """ it should retrieves GEREP data from Excel file """
        (producteurs, traiteurs) = get_gerep_data()
        self.assertEqual(len(producteurs), 8)
        self.assertEqual(len(traiteurs), 10)
