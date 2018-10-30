from .mod import MOD

class Human(MOD):

    def __init__(self):
        self.species = "Homo sapiens"

        self.wtExpressionName = "/RGD_1.0.0.7_expression.9606.json"
        self.loadFile = "RGD_1.0.0.7_4.tar.gz"

        self.bgiName = "/RGD_1.0.0.7_BGI.9606.json"
        self.diseaseName = "/RGD_1.0.0.7_disease.9606.json"
        self.phenotypeName = "/RGD_1.0.0.7_phenotype.9606.json"
        self.geneAssociationFile = "gene_association_1.7.1.human.gz"

        self.identifierPrefix = "" # None for Human.
        self.geoSpecies = "Homo+sapiens"
        self.geoRetMax = "40000"
        self.dataProvider = "RGD"

    def load_genes(self, batch_size, testObject, species):
        data = MOD.load_genes_mod(self, batch_size, testObject, self.bgiName, self.loadFile, species)
        return data

    @staticmethod
    def get_organism_names():
        return ["Homo sapiens", "H. sapiens", "HUMAN"]

    def extract_go_annots(self, testObject):
        go_annot_list = MOD.extract_go_annots_mod(self, self.geneAssociationFile, self.species, self.identifierPrefix, testObject)
        return go_annot_list

    def load_disease_allele_objects(self, batch_size, testObject, species):
        data = ""
        return data

    def load_disease_gene_objects(self, batch_size, testObject, species):
        data = MOD.load_disease_gene_objects_mod(self, batch_size, testObject, self.diseaseName, self.loadFile, species)
        return data

    def load_phenotype_objects(self, batch_size, testObject, species):
        data = MOD.load_phenotype_objects_mod(self, batch_size, testObject, self.phenotypeName, self.loadFile, species)
        return data


    def extract_geo_entrez_ids_from_geo(self):
        xrefs = MOD.extract_geo_entrez_ids_from_geo(self, self.geoSpecies, self.geoRetMax)
        return xrefs