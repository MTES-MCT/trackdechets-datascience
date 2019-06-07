
from unittest import TestCase

from ..serializers import IREPSerializer, GEREPSerializer


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


class GEREPSerializerTestCase(TestCase):

    def test_to_internal_value_traiteur(self):
        """ it should convert dict to model instance """
        data = {
            'Annee': 2016.0,
            'Code établissement': '029.16724',
            'Nom Etablissement': 'ACME',
            'Adresse Site Exploitation': 'adresse',
            'Code Postal Etablissement': '29700',
            'Commune': 'Pluguffan',
            'Code Insee': '29216',
            'Numero Siret': 'siret',
            'Code APE': '38.11Z',
            'Nom Contact': 'Mr le Président',
            'Tel Contact': 'telephone',
            'Fonction Contact': 'contrôleur de gestion',
            'Mail Contact': 'president@acme.fr',
            'Code déchet traité': '17 02 03',
            'Déchet traité': 'matières plastiques'}

        serializer = GEREPSerializer(data, 'traiteur')
        serializer.to_internal_value()
        self.assertIsNotNone(serializer.instance)

    def test_to_internal_value_producteur(self):
        """ it should convert dict to model instance """

        data = {
            'Annee': 2016.0,
            'Code établissement': '029.16724',
            'Nom Etablissement': 'ACME',
            'Adresse Site Exploitation': 'adresse',
            'Code Postal Etablissement': '29700',
            'Commune': 'Pluguffan',
            'Code Insee': '29216',
            'Numero Siret': 'siret',
            'Code APE': '38.11Z',
            'Nom Contact': 'Mr le Président',
            'Tel Contact': 'telephone',
            'Fonction Contact': 'contrôleur de gestion',
            'Mail Contact': 'president@acme.fr',
            'Code déchet produit': '17 02 03',
            'Déchet produit': 'matières plastiques'}

        serializer = GEREPSerializer(data, 'producteur')
        serializer.to_internal_value()
        self.assertIsNotNone(serializer.instance)
