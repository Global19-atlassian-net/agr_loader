# Used for loading a test subset of data for AGR.
# Note: When testing is enabled, GO annotations and GO terms are only loaded for the following testIdSet.
# The testIdSet is used to "filter" these entries in the appropriate extractor files.
import logging


logger = logging.getLogger(__name__)


class TestObject(object):

    def __init__(self, useTestObject):
        # TODO Separate gene ids from other forms of id?

        self.useTestObject = useTestObject

        self.mgiIdSet = {
            'MGI:5437116', 'MGI:1915135', 'MGI:109337', 'MGI:108202', 'MGI:2676586', 'MGI:88180', 'MGI:88467',
            'MGI:109583', 'MGI:96765', 'MGI:1099804',
            'MGI:1916172', 'MGI:96680', 'MGI:2175810', 'MGI:5437110', 'MGI:5437073', 'MGI:88525',
            'MGI:1923696', 'MGI:1929597', 'MGI:87853', 'MGI:2179405',
            'MGI:1337006', 'MGI:1929470', 'MGI:1929288', 'MGI:1929209', 'MGI:1915127', 'MGI:1915121',
            'MGI:1915122', 'MGI:1915123', 'MGI:3643831',
            'MGI:1929183', 'MGI:2443198', 'MGI:1861441', 'MGI:1928478', 'MGI:1928761',
            'MGI:1914047', 'MGI:88053', 'MGI:88054', 'MGI:1855948',
            'MGI:88056', 'MGI:88456', 'MGI:88447', 'MGI:88587', 'MGI:1338803', 'MGI:94864', 'MGI:1915101',
            'MGI:1915112', 'MGI:1355324', 'MGI:3029164', 'MGI:1856330',
                                                         'MGI:1915181', 'MGI:1915162', 'MGI:1915164', 'MGI:1929699',
            'MGI:94909', 'MGI:1856331', 'MGI:97490', 'MGI:108092', 'MGI:2156738',
            'MGI:2148260', 'MGI:1856328', 'MGI:2678393', 'MGI:2429942', 'MGI:1856332', 'MGI:5569634',
            'MGI:3531484', 'MGI:3531484',
            'MGI:2148259', 'MGI:3531483', 'MGI:1856329', 'MGI:3531484', 'MGI:5781149', 'MGI:2148259', 'MGI:104735',
            'MGI:98834',
            # phenotype objects
            'MGI:2670749', 'MGI:2656842', 'MGI:3575645', 'MGI:104796', 'MGI:1860955', 'MGI:1860970', 'MGI:2384499',
            'MGI:2388016',
            # disease objects
            'MGI:88123', 'MGI:2148259', 'MGI:98297', 'MGI:5011818', 'MGI:98371', 'MGI:1919338', 'MGI:96575',
            'MGI:95832', 'MGI:2387629', 'MGI:2446564', 'MGI:2446568', 'MGI:1860955', 'MGI:1860970', 'MGI:2384499',
            'MGI:2388016'
            # expression
            'MGI:97570', 'MGI:2181676', 'MGI:1918911', 'MGI:1919311', 'MGI:1920484', 'MGI:109583',
            # gene descriptions
            'MGI:96067', 'MGI:88388', 'MGI:107202', 'MGI:106658', 'MGI:105043', 'MGI:104807',
            # variant
            'MGI:109151', 'MGI:106679', 'MGI:103223', 'MGI:104554', 'MGI:104993', 'MGI:5316784', 'MGI:5566856',
            'MGI:3776030', 'MGI:1857423', 'MGI:5806340',
        }

        self.wormbaseIdSet = {
            'WB:WBGene00044305', 'WB:WBGene00169423', 'WB:WBGene00000987', 'WB:WBGene00021789',
            'WB:WBGene00006750', 'WB:WBGene00000540', 'WB:WBGene00017866', 'WB:WBGene00001131',
            'WB:WBGene00015146', 'WB:WBGene00015599', 'WB:WBGene00001133', 'WB:WBGene00001115',
            'WB:WBGene00018468', 'WB:WBGene00019001', 'WB:WBGene00007438', 'WB:WBGene00001136', 'WB:WBGene00006742',
            'WB:WBGene00003883',
            # expression,
            'WB:WBGene00012650', 'WB:Gene00006649', 'WB:WBGene00008117', 'WB:WBGene00004876',
            'WB:WBGene00003883', 'WB:WBGene00006508',
            # phenotype and disease objects
            'WBVar:WBVar00000012', 'WBVar:WBVar00000013', 'WB:WBVar00000001', 'WB:WBVar00242490', 'WB:WBGene00004264',
            'WB:WBGene00004488', 'WB:WBGene00000898',
            # gene descriptions
            'WB:WBGene00003412', 'WB:WBGene00000227', 'WB:WBGene00006844', 'WB:WBGene00022425', 'WB:WBGene00022223',
            'WB:WBVar00239315',
            # variant
            'WB:WBGene00006752', 'WB:WBGene00021840', 'WB:WBGene00001117', 'WB:WBVar00241694', 'WB:WBVar02147569',
            'WB:WBVar00089131',
            # disease
            'WB:WBGene00011936',
        }

        self.sgdIdSet = {
            'SGD:S000003256', 'SGD:S000003513', 'SGD:S000000119', 'SGD:S000001015',
            # phenotypic genes
            'SGD:S000001101', 'SGD:S000006136', 'SGD:S000000383',
            # disease
            'SGD:S000005481', 'SGD:S000005246', 'SGD:S000003865', 'SGD:S000002862', 'SGD:S000001596',
            # expression
            'SGD:S000005737', 'SGD:S000004802', 'SGD:S000000002', 'SGD:S000001596',
            # gene descriptions
            'SGD:S000004695', 'SGD:S000004916', 'SGD:S000004646', 'SGD:S000000253', 'SGD:S000000364', 'SGD:S000002284',
            'SGD:S000004603', 'SGD:S000004802', 'SGD:S000005707', 'SGD:S000001596', 'SGD:S000004777', 'SGD:S000006074',
            'SGD:S000002678', 'SGD:S000003487', 'SGD:S000000458', 'SGD:S000006068', 'SGD:S000005269', 'SGD:S000007324',
            'SGD:S000004241', 'SGD:S000002536',
            # expression
            'SGD:S000002200',

        }

        self.zfinIdSet = {
            'ZFIN:ZDB-GENE-990415-72', 'ZFIN:ZDB-GENE-030131-3445', 'ZFIN:ZDB-GENE-980526-388',
            'ZFIN:ZDB-GENE-010525-1', 'ZFIN:ZDB-GENE-010525-1', 'ZFIN:ZDB-GENE-060117-5',
            'ZFIN:ZDB-GENE-050302-80', 'ZFIN:ZDB-GENE-060503-876',
            'ZFIN:ZDB-GENE-050302-82', 'ZFIN:ZDB-GENE-030131-4430', 'ZFIN:ZDB-GENE-060503-872',
            'ZFIN:ZDB-GENE-060503-873', 'ZFIN:ZDB-GENE-010525-1', 'ZFIN:ZDB-GENE-990415-72',
            'ZFIN:ZDB-GENE-060503-867', 'ZFIN:ZDB-GENE-010323-11', 'ZFIN:ZDB-GENE-010525-1',
            'ZFIN:ZDB-GENE-010320-1', 'ZFIN:ZDB-GENE-010525-1', 'ZFIN:ZDB-GENE-051127-5',
            'ZFIN:ZDB-GENE-990415-270', 'ZFIN:ZDB-LINCRNAG-160518-1', 'ZFIN:ZDB-GENE-030131-3776',
            'ZFIN:ZDB-GENE-030616-47',
            'ZFIN:ZDB-GENE-040426-1716', 'ZFIN:ZDB-ALT-980203-985', 'ZFIN:ZDB-ALT-060608-195',
            'ZFIN:ZDB-ALT-050428-6', 'ZFIN:ZDB-ALT-151012-9', 'ZFIN:ZDB-GENE-070117-2142', 'ZFIN:ZDB-ALT-161003-10628',
            # allele for synonym
            'ZFIN:ZDB-ALT-980413-591',
            # disease specific test objects
            'ZFIN:ZDB-GENE-030131-5607', 'ZFIN:ZDB-GENE-050517-20', 'ZFIN:ZDB-GENE-990415-122',
            'ZFIN:ZDB-GENE-980526-41',
            'ZFIN:ZDB-GENE-050517-20', 'ZFIN:ZDB-ALT-980203-1091', 'ZFIN:ZDB-ALT-121210-2',
            'ZFIN:ZDB-GENE-000816-1', 'ZFIN:ZDB-ALT-160129-6', 'ZFIN:ZDB-ALT-160129-6', 'ZFIN:ZDB-GENE-980526-41',
            'ZFIN:ZDB-GENE-980526-166', 'ZFIN:ZDB-GENE-040426-1716', 'ZFIN:ZDB-GENE-020905-1',
            'ZFIN:ZDB-GENE-060312-41', 'ZFIN:ZDB-ALT-160129-6', 'ZFIN:ZDB-FISH-170912-2', 'ZFIN:ZDB-FISH-161201-9',
            'ZFIN:ZDB-FISH-180928-1', 'ZFIN:ZDB-FISH-180912-16', 'ZFIN:ZDB-GENE-060503-338',
            'ZFIN:ZDB-FISH-150901-3961', 'ZFIN:ZDB-ALT-040716-14', 'ZFIN:ZDB-GENE-980526-178',
            'ZFIN:ZDB-GENE-060503-338', 'ZFIN:ZDB-FISH-190411-12', 'ZFIN:ZDB-ALT-181016-1', 'ZFIN:ZDB-GENE-060503-219',

            # expression
            'ZFIN:ZDB-GENE-070410-17', 'ZFIN:ZDB-GENE-990714-29', 'ZFIN:ZDB-GENE-001103-1', 'ZFIN:ZDB-GENE-050913-20',
            'ZFIN:ZDB-GENE-980526-474', 'ZFIN:ZDB-GENE-000627-1', 'ZFIN:ZDB-GENE-050913-20', 'ZFIN:ZDB-GENE-030912-6',
            'ZFIN:ZDB-GENE-131121-260', 'ZFIN:ZDB-GENE-980526-368', 'ZFIN:ZDB-GENE-051101-2', 'ZFIN:ZDB-GENE-090311-1',
            'ZFIN:ZDB-GENE-040426-2889', 'ZFIN:ZDB-GENE-140619-1', 'ZFIN:ZDB-GENE-990714-29',
            'ZFIN:ZDB-GENE-030131-7696', 'ZFIN:ZDB-GENE-060312-41', 'ZFIN:ZDB-FISH-180912-16',
            # gene descriptions
            'ZFIN:ZDB-GENE-990415-131', 'ZFIN:ZDB-GENE-050517-20', 'ZFIN:ZDB-GENE-040426-1294',
            'ZFIN:ZDB-GENE-040426-1294', 'ZFIN:ZDB-GENE-040718-10',
            # genomic locations
            'ZFIN:ZDB-GENE-990415-8',
            # variant
            'ZFIN:ZDB-GENE-040702-4', 'ZFIN:ZDB-GENE-030131-9825', 'ZFIN:ZDB-GENE-030131-6129',
            'ZFIN:ZDB-GENE-000208-20', 'ZFIN:ZDB-GENE-090421-1', 'ZFIN:ZDB-GENE-000427-6', 'ZFIN:ZDB-GENE-980526-221',
            'ZFIN:ZDB-ALT-070807-6', 'ZFIN:ZDB-ALT-070315-5', 'ZFIN:ZDB-ALT-000621-2',
            'ZFIN:ZDB-ALT-980203-1091', 'ZFIN:ZDB-ALT-050713-2',
            'ZFIN:ZDB-ALT-040716-14', 'ZFIN:ZDB-ALT-160601-8105', 'ZFIN:ZDB-ALT-170321-11', 'ZFIN:ZDB-ALT-180207-16',
            # affected genomic model
            'ZFIN:ZDB-ALT-040721-14',
            'ZFIN:ZDB-GENE-990415-101', 'ZFIN:ZDB-ALT-180201-1', 'ZFIN:ZDB-ALT-050714-2', 'ZFIN:ZDB-ALT-140917-5',
            'ZFIN:ZDB-FISH-150901-27842', 'ZFIN:ZDB-FISH-180220-12', 'ZFIN:ZDB-FISH-150901-28582',
            'ZFIN:ZDB-FISH-171114-2', 'ZFIN:ZDB-FISH-150901-3478', 'ZFIN:ZDB-FISH-150901-29713',
            'ZFIN:ZDB-FISH-150901-25842', 'ZFIN:ZDB-FISH-150901-9361', 'ZFIN:ZDB-FISH-150901-3961',
            'ZFIN:ZDB-FISH-150901-13024', 'ZFIN:ZDB-FISH-150901-18822', 'ZFIN:ZDB-FISH-150901-10526',
            'ZFIN:ZDB-FISH-180220-12', 'ZFIN:ZDB-FISH-150901-19267', 'ZFIN:ZDB-FISH-150901-11465',
            # sqtr
            'ZFIN:ZDB-GENE-031027-1', 'ZFIN:ZDB-GENE-091204-147',
            'ZFIN:ZDB-MRPHLNO-081021-3', 'ZFIN:ZDB-MRPHLNO-050818-6', 'ZFIN:ZDB-MRPHLNO-060620-3',
            'ZFIN:ZDB-MRPHLNO-060620-5', 'ZFIN:ZDB-MRPHLNO-070911-3', 'ZFIN:ZDB-CRISPR-181015-8',
            'ZFIN:ZDB-CRISPR-161214-618', 'ZFIN:ZDB-CRISPR-161214-737',
            # background
            'ZFIN:ZDB-FISH-150901-29235', 'ZFIN:ZDB-FISH-150901-14423', 'ZFIN:ZDB-FISH-150901-26753',
            'ZFIN:ZDB-FISH-150901-5094',
            # GO annotations
            'ZFIN:ZDB-GENE-080424-7',
            # Phenotype
            'ZFIN:ZDB-FISH-150901-24820', 'ZFIN:ZDB-ALT-980203-469', 'ZFIN:ZDB-GENE-990415-198',

        }
        self.flybaseIdSet = {
            'FB:FBgn0083973', 'FB:FBgn0037960', 'FB:FBgn0027296', 'FB:FBgn0032006', 'FB:FBgn0001319',
            'FB:FBgn0002369', 'FB:FBgn0026379',
            'FB:FBgn0033885', 'FB:FBgn0024320', 'FB:FBgn0283499',
            'FB:FBgn0032465', 'FB:FBgn0285944', 'FB:FBgn0032728', 'FB:FBgn0000014',
            'FB:FBgn0032729', 'FB:FBgn0065610', 'FB:FBgn0032730', 'FB:FBgn0032732', 'FB:FBgn0260987',
            'FB:FBgn0032781', 'FB:FBgn0032782', 'FB:FBgn0032740',
            'FB:FBgn0032741', 'FB:FBgn0032744', 'FB:FBgn0036309', 'FB:FBgn0003470', 'FB:FBal0161187', 'FB:FBal0000003',
            'FB:FBal0000004', 'FB:FBgn0039156',
            # expression
            'FB:FBgn0027660', 'FB:FBgn0284221', 'FB:FBgn0013765', 'FB:FBgn0004620',
            # disease
            'FB:FBgn0004644', 'FB:FBgn0039129', 'FB:FBgn0010412', 'FB:FBgn0263006', 'FB:FBgn0283499', 'FB:FBgn0025790',
            # gene descriptions
            'FB:FBgn0027655', 'FB:FBgn0045035', 'FB:FBgn0024238',
            # variants
            'FB:FBgn0011224', 'FB:FBal0226899', 'FB:FBal0179527',
        }
        self.rgdTestSet = {
            'RGD:70891', 'RGD:1306349', 'RGD:708528', 'RGD:620796', 'RGD:61995', 'RGD:1309165',
            'RGD:1581495', 'RGD:2322065', 'RGD:1309063', 'RGD:2845', 'RGD:628748', 'RGD:1581476',
            'RGD:1309312', 'RGD:7627512', 'RGD:1309105', 'RGD:1309109', 'RGD:7627503', 'RGD:1578801',
            # disease pheno specific test objects
            'RGD:68936', 'RGD:3886', 'RGD:3673', 'RGD:6498788', 'RGD:1303329', 'RGD:2917', 'RGD:2869',
            # expression
            'RGD:3884', 'RGD:3889', 'RGD:2129',
            # allele gene and alleles
            'RGD:2219', 'RGD:728326', 'RGD:2454', 'RGD:728295', 'RGD:2129', 'RGD:621293',
            # gene descriptions
            'RGD:68337', 'RGD:2332', 'RGD:1593265', 'RGD:1559787', 'RGD:621409',
            # variant consequences
            'RGD:1310046', 'RGD:69305', 'RGD:1589755', 'RGD:1307511', 'RGD:3889', 'RGD:13437613', 'RGD:1600311',
            'RGD:5143979',
        }

        self.humanTestSet = {
            'HGNC:17889', 'HGNC:25818', 'HGNC:3686', 'HGNC:7881', 'HGNC:6709', 'HGNC:6526', 'HGNC:6553', 'HGNC:7218',
            'HGNC:6560', 'HGNC:6551', 'HGNC:6700', 'HGNC:9588', 'HGNC:11973',
            # disease pheno specific test objects
            'HGNC:897', 'HGNC:869', 'HGNC:10848', 'HGNC:10402', 'HGNC:11204', 'HGNC:12597', 'HGNC:811', 'HGNC:6091',
            # gene descriptions
            'HGNC:4851', 'HGNC:1884', 'HGNC:795', 'HGNC:11291', 'HGNC:9091',
            # disease
            'HGNC:4693', 'HGNC:11179', 'HGNC:7325', 'HGNC:3650', 'HGNC:4601', 'HGNC:9508', 'HGNC:6893', 'HGNC:7',
        }

        self.modMap = {"RGD": self.rgdTestSet,
                  "MGI": self.mgiIdSet,
                  "ZFIN": self.zfinIdSet,
                  "WB": self.wormbaseIdSet,
                  "SGD": self.sgdIdSet,
                  "FlyBase": self.flybaseIdSet,
                  "Human": self.humanTestSet}

        self.testIdSet = self.zfinIdSet.union(self.mgiIdSet.union(self.wormbaseIdSet).union(self.flybaseIdSet).union(self.sgdIdSet).union(self.rgdTestSet).union(self.humanTestSet))

    def using_test_data(self):
        return self.useTestObject

    def check_for_test_id_entry(self, primaryId):
        if primaryId in self.testIdSet:
            return True
        else:
            return False
