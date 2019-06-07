
from .models import IREP


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




