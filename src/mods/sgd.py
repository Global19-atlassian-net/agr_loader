from .mod import MOD

class SGD(MOD):

    def __init__(self, batch_size):
        self.species = "Saccharomyces cerevisiae"
        super().__init__(batch_size, self.species)
        self.loadFile = "SGD_1.0.0.7_1.tar.gz"
        self.bgiName = "/SGD_1.0.0.7_basicGeneInformation.json"
        self.diseaseName = "/SGD_1.0.0.7_disease.daf.json"
        self.phenotypeName = "/SGD_1.0.0.7_phenotype.json"
        self.alleleName = ""
        self.wtExpressionName = "/SGD_1.0.0.7_expression.json"
        self.geneAssociationFile = "gene_association_1.7.sgd.gz"
        self.identifierPrefix = "SGD:"
        self.geoRetMax = "10000"
        self.dataProvider = "SGD"

    def load_wt_expression_objects(self):
        data = self.load_wt_expression_objects_mod(self.wtExpressionName, self.loadFile)
        return data