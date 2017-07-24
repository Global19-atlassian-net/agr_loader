from .mod import MOD

class RGD(MOD):

    def __init__(self):
        self.species = "Rattus norvegicus"
        self.loadFile = "RGD_0.6.2.tar.gz"
        self.bgiName = "/RGD_0.6.2_basicGeneInformation.10116.json"
        self.diseaseName = "/RGD_0.6.2_disease.10116.daf.json"
        self.geneAssociationFile = "gene_association.rgd.gz"

    def load_genes(self, batch_size, test_set):
        data = MOD().load_genes(batch_size, test_set, self.bgiName, self.loadFile)
        return data

    @staticmethod
    def gene_href(gene_id):
        return "http://www.rgd.mcw.edu/rgdweb/report/gene/main.html?id=" + gene_id

    @staticmethod
    def get_organism_names():
        return ["Rattus norvegicus", "R. norvegicus", "RAT"]

    def load_go_prefix(self):
        go_annot_dict = MOD().load_go_prefix(self.geneAssociationFile, self.species)
        return go_annot_dict

    def load_do_annots(self):
        gene_disease_dict = MOD().load_do_annots(self.diseaseName)
        return gene_disease_dict