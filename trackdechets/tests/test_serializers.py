
from unittest import TestCase

from ..serializers import IREPSerializer


class IREPSerializerTestCase(TestCase):

    def test_to_internal_value(self):
        """ it should convert dict to model instance """

        data = dict(
            [('Identifiant', '068.06166'),
             ('Nom_Etablissement', 'SARL ETS VIU'),
             ('Numero_SIRET', '37852819400012'),
             ('Adresse', '13 Avenue de Gounon'),
             ('Code_Postal', '32800'),
             ('Commune', 'EAUZE'),
             ('Departement', 'GERS'),
             ('Region', 'OCCITANIE'),
             ('Coordonnees_X', '420134'),
             ('Coordonnees_Y', '1875638'),
             ('Code_APE', '3831Z'),
             ('Libelle_APE', "Démantèlement d'épaves"),
             ('code_eprtr', ''),
             ('libelle_eprtr', '')])

        serializer = IREPSerializer(data)
        serializer.to_internal_value()
        self.assertIsNotNone(serializer.instance)
