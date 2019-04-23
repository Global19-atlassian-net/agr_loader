import logging
import multiprocessing
import uuid

from etl import ETL
from etl.helpers import ETLHelper
from files import JSONFile
from transactors import CSVTransactor, Neo4jTransactor

logger = logging.getLogger(__name__)


class VariationETL(ETL):

    variation_query_template = """

            USING PERIODIC COMMIT %s
            LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

                MATCH (a:Allele:Feature {primaryKey: row.alleleId})

                //Create the Allele node and set properties. primaryKey is required.
                MERGE (o:Variant {primaryKey:row.uuid})
                    ON CREATE SET 
                     o.genomicReferenceSequence = row.genomicReferenceSequence,
                     o.genomicVariantSequence = row.genomicVariantSequence,
                     o.dateProduced = row.dateProduced,
                     o.release = row.release,
                     o.localId = row.localId,
                     o.globalId = row.globalId,
                     o.uuid = row.uuid,
                     o.dataProviders = row.dataProviders,
                     o.dataProvider = row.dataProvider

                MERGE (o)<-[:VARIATION]->(a) """

    soterms_template = """
        USING PERIODIC COMMIT %s
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row
            MATCH (o:Allele:Feature {primaryKey:row.alleleId})
            MATCH (s:SOTerm:Ontology {primaryKey:row.soTermId})
            MERGE (o)-[:VARIATION_TYPE]->(s)"""


    genomic_locations_template = """
        USING PERIODIC COMMIT %s
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

            MATCH (o:Variant {primaryKey:row.variantId})
            MATCH (chrm:Chromosome {primaryKey:row.chromosome})

            MERGE (o)-[gchrm:LOCATED_ON]->(chrm)
            ON CREATE SET gchrm.start = apoc.number.parseInt(row.start),
                gchrm.end = apoc.number.parseInt(row.end),
                gchrm.assembly = row.assembly,
                gchrm.strand = row.strand """

    xrefs_template = """

        USING PERIODIC COMMIT %s
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

            MATCH (o:Variant {primaryKey:row.variantId}) """ + ETLHelper.get_cypher_xref_text()

    def __init__(self, config):
        super().__init__()
        self.data_type_config = config

    def _load_and_process_data(self):
        thread_pool = []

        for sub_type in self.data_type_config.get_sub_type_objects():
            p = multiprocessing.Process(target=self._process_sub_type, args=(sub_type,))
            p.start()
            thread_pool.append(p)

        ETL.wait_for_threads(thread_pool)

    def _process_sub_type(self, sub_type):

        logger.info("Loading Variation Data: %s" % sub_type.get_data_provider())
        filepath = sub_type.get_filepath()
        logger.info(filepath)
        data = JSONFile().get_data(filepath)
        logger.info("Finished Loading Variation Data: %s" % sub_type.get_data_provider())

        if data is None:
            logger.warn("No Data found for %s skipping" % sub_type.get_data_provider())
            return

        # This order is the same as the lists yielded from the get_generators function.
        # A list of tuples.

        commit_size = self.data_type_config.get_neo4j_commit_size()
        batch_size = self.data_type_config.get_generator_batch_size()

        # This needs to be in this format (template, param1, params2) others will be ignored
        query_list = [
            [VariationETL.variation_query_template, commit_size, "variation_data_" + sub_type.get_data_provider() + ".csv"],
            [VariationETL.genomic_locations_template, commit_size,
             "variant_genomiclocations_" + sub_type.get_data_provider() + ".csv"],
            [VariationETL.soterms_template, commit_size,
             "variant_soterms_" + sub_type.get_data_provider() + ".csv"],
            [VariationETL.xrefs_template, commit_size,
             "variant_xrefs_" + sub_type.get_data_provider() + ".csv"]
        ]

        # Obtain the generator
        generators = self.get_generators(data, sub_type.get_data_provider(), batch_size)

        query_and_file_list = self.process_query_params(query_list)
        CSVTransactor.save_file_static(generators, query_and_file_list)
        Neo4jTransactor.execute_query_batch(query_and_file_list)

    def get_generators(self, variant_data, data_provider, batch_size):

        dataProviders = []
        release = ""
        variants = []
        variant_genomic_locations = []
        variant_so_terms = []
        crossReferences = []

        counter = 0
        dateProduced = variant_data['metaData']['dateProduced']

        dataProviderObject = variant_data['metaData']['dataProvider']

        dataProviderCrossRef = dataProviderObject.get('crossReference')
        dataProvider = dataProviderCrossRef.get('id')
        dataProviderPages = dataProviderCrossRef.get('pages')
        dataProviderCrossRefSet = []

        loadKey = dateProduced + dataProvider + "_VARIATION"

        if dataProviderPages is not None:
            for dataProviderPage in dataProviderPages:
                crossRefCompleteUrl = ETLHelper.get_page_complete_url(dataProvider, self.xrefUrlMap, dataProvider,
                                                                      dataProviderPage)

                dataProviderCrossRefSet.append(ETLHelper.get_xref_dict(dataProvider, dataProvider, dataProviderPage,
                                                                       dataProviderPage, dataProvider,
                                                                       crossRefCompleteUrl,
                                                                       dataProvider + dataProviderPage))

                dataProviders.append(dataProvider)
                logger.info("data provider: " + dataProvider)

        if 'release' in variant_data['metaData']:
            release = variant_data['metaData']['release']

        for alleleRecord in variant_data['data']:
            counter = counter + 1
            globalId = alleleRecord.get('alleleId')
            localId = globalId.split(":")[1]
            modGlobalCrossRefId = ""
            crossReferences = []
            variantUUID = str(uuid.uuid4())

            if self.testObject.using_test_data() is True:
                is_it_test_entry = self.testObject.check_for_test_id_entry(globalId)
                if is_it_test_entry is False:
                    counter = counter - 1
                    continue

            crossRefPrimaryId = alleleRecord.get('sequenceOfReferenceAccessionNumber')
            localCrossRefId = crossRefPrimaryId.split(":")[1]
            prefix = crossRefPrimaryId.split(":")[0]

            crossRefCompleteUrl = ETLHelper.get_no_page_complete_url(localCrossRefId, ETL.xrefUrlMap, prefix,
                                                                     globalId)
            xrefMap = ETLHelper.get_xref_dict(localCrossRefId, prefix, "variant_sequence_of_reference",
                                              "sequence_of_reference_accession_number", globalId, crossRefCompleteUrl,
                                              crossRefPrimaryId + "variant_sequence_of_reference")
            xrefMap['dataId'] = globalId
            crossReferences.append(xrefMap)


            variant_dataset = {
                "genomicReferenceSequence": alleleRecord.get('genomicReferenceSequence'),
                "genomicVariantSequence": alleleRecord.get('genomicVariantSequence'),
                "alleleId": alleleRecord.get('alleleId'),
                "globalId": globalId,
                "localId": localId,
                "dataProviders": dataProviders,
                "dateProduced": dateProduced,
                "loadKey": loadKey,
                "release": release,
                "modGlobalCrossRefId": modGlobalCrossRefId,
                # TODO: eventaully uuid won't be the unique identifier, the HGVS nomenclature will be the unique identifier (hopefully)
                "uuid": variantUUID,
                "dataProvider": data_provider
            }
            logger.info(variant_dataset)

            variant_genomic_location_dataset = {
                "variantId": variantUUID,
                "assembly": alleleRecord.get('assembly'),
                "chromosome": alleleRecord.get('chromosome'),
                "start": alleleRecord.get('start'),
                "end": alleleRecord.get('end')

            }

            variant_so_term = {
                "alleleId": alleleRecord.get('alleleId'),
                "soTerm": alleleRecord.get('type')
            }

            cross_reference_data_set = {
                "variantId" : variantUUID,
                "sequenceOfReferenceXref": xrefMap
            }

            crossReferences.append(cross_reference_data_set)
            variant_so_terms.append(variant_so_term)
            variant_genomic_locations.append(variant_genomic_location_dataset)
            variants.append(variant_dataset)

            if counter == batch_size:
                yield [variants, variant_genomic_locations, variant_so_terms, crossReferences]
                variants = []
                variant_genomic_locations =[]
                variant_so_terms =[]
                crossReferences = []

        if counter > 0:
            yield [variants,variant_genomic_locations,variant_so_terms, crossReferences]
