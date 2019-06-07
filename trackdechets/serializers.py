
from .models import IREP, GEREP


class BaseSerializer():

    def __init__(self, data):
        self.data = data
        self.instance = None

    def to_internal_value(self):
        raise NotImplementedError()


class RubriqueSerializer(BaseSerializer):

    def to_internal_value(self):
        pass


class IREPSerializer(BaseSerializer):

    def to_internal_value(self):
        irep = {
            IREP.identifiant.column.name: self.data['Identifiant'],
            IREP.nom_etablissement.column.name: self.data['Nom_Etablissement'],
            IREP.numero_siret.column.name: self.data['Numero_SIRET'],
            IREP.adresse.column.name: self.data['Adresse'],
            IREP.code_postal.column.name: self.data['Code_Postal'],
            IREP.commune.column.name: self.data['Commune'],
            IREP.departement.column.name: self.data['Departement'],
            IREP.region.column.name: self.data['Region'],
            IREP.coordonnees_X.column.name: self.data['Coordonnees_X'],
            IREP.coordonnees_Y.column.name: self.data['Coordonnees_Y'],
            IREP.code_ape.column.name: self.data['Code_APE'],
            IREP.libelle_ape.column.name: self.data['Libelle_APE'],
            IREP.code_eprtr.column.name: self.data['code_eprtr'],
            IREP.libelle_eprtr.column.name: self.data['libelle_eprtr']
        }
        self.instance = IREP(**irep)


class GEREPSerializer(BaseSerializer):

    def __init__(self, data, etablissement_type):
        self.data = data
        self.etablissement_type = etablissement_type
        self.instance = None

    def to_internal_value(self):

        gerep = {
            GEREP.type_etablissement.column_name: self.etablissement_type,
            GEREP.annee.column_name: self.data['Annee'],
            GEREP.code_etablissement.column_name:
                self.data['Code établissement'],
            GEREP.nom_etablissement.column_name:
                self.data['Nom Etablissement'],
            GEREP.adresse_site_exploitation.column_name:
                self.data['Adresse Site Exploitation'],
            GEREP.code_insee.column_name: self.data['Code Insee'],
            GEREP.code_ape.column_name: self.data['Code APE'],
            GEREP.numero_siret.column_name: self.data['Numero Siret'],
            GEREP.nom_contact.column_name: self.data['Nom Contact'],
            GEREP.fonction_contact.column_name: self.data['Fonction Contact'],
            GEREP.tel_contact.column_name: self.data['Tel Contact'],
            GEREP.mail_contact.column_name: self.data['Mail Contact']
        }

        if self.etablissement_type == 'producteur':
            gerep[GEREP.code_dechet.column_name] = \
                self.data['Code déchet produit']
            gerep[GEREP.dechet.column_name] = \
                self.data['Déchet produit']

        elif self.etablissement_type == 'traiteur':
            gerep[GEREP.code_dechet.column_name] = \
                self.data['Code déchet traité']
            gerep[GEREP.dechet.column_name] = self.data['Déchet traité']

        self.instance = GEREP(**gerep)
