
from unittest import TestCase

from ..utils import parse_icpe_fiche_detail


class UtilsTestCase(TestCase):

    def test_parse_icpe_fiche_detail(self):
        """ it should parse the content of the table in the html page"""

        html = """
        <h2>Situation administrative</h2>
        <br>
        <div class="listeEtabl">
            <table border="1" cellpadding="2px" class="listeEtabl" summary="liste des résultats">
                <tbody><tr class="listeEtablenTete">
                    <th title="Rubrique IC">Rubri. IC
                    </th><th title="Alinéa">Ali.
                    </th><th title="Date d'autorisation">Date auto.
                    </th><th>Etat d'activité
                    </th><th title="Régime">Régime autorisé<sup>(3)</sup>
                    </th><th>Activité
                    </th><th>Volume
                    </th><th>Unité
                </th></tr>
                <tr class="listeEtabl1">
                    <td><a href="http://www.ineris.fr/aida/textes/nomenclature/rubriques/rub_2760.htm" target="_blank">2760</a></td>
                    <td>3</td>
                    <td>10/06/2009</td>
                    <td title="En fonctionnement">En fonct.</td>
                    <td>E</td>
                    <td>Installations de stockage de déchets inertes</td>
                    <td align="right">1400000</td>
                    <td> </td>
                </tr>
            </tbody></table>
        </div>
        """
        data = parse_icpe_fiche_detail(html)
        expected = [
            {
                'Rubri. IC': '2760',
                'Ali.': '3',
                'Date auto.': '10/06/2009',
                "Etat d'activité": 'En fonct.',
                'Régime autorisé(3)': 'E',
                'Activité': 'Installations de stockage de déchets inertes',
                'Volume': '1400000', 'Unité': ' '
            }
        ]
        self.assertEqual(data, expected)