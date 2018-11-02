import uuid
from etl import ETL
from services import *
from extractors import *
from neo4j_transactor import Neo4jTransactor

import logging

logger = logging.getLogger(__name__)

class BGIETL(ETL):

    genomic_locations_template = """
        USING PERIODIC COMMIT 10000
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row
                
            MATCH (o:Gene {primaryKey:row.primaryId})
            MERGE (chrm:Chromosome {primaryKey:row.chromosome})

            CREATE (o)-[gchrm:LOCATED_ON]->(chrm)
            SET gchrm.start = row.start ,
                gchrm.end = row.end ,
                gchrm.assembly = row.assembly ,
                gchrm.strand = row.strand """
    
    gene_secondaryIds_template = """
        USING PERIODIC COMMIT 10000
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

            MATCH (g:Gene {primaryKey:row.primary_id})
            
            MERGE (second:SecondaryId:Identifier {primaryKey:row.secondary_id})
                SET second.name = row.secondary_id
            MERGE (g)-[aka1:ALSO_KNOWN_AS]->(second) """

    gene_synonyms_template = """
        USING PERIODIC COMMIT 10000
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

            MATCH (g:Gene {primaryKey:row.primary_id})
            MATCH (g:Gene {primaryKey:row.primary_id})
            
           MERGE(syn:Synonym:Identifier {primaryKey:row.synonym})
                SET syn.name = row.synonym
            MERGE (g)-[aka2:ALSO_KNOWN_AS]->(syn) """

    gene_query_template = """
        USING PERIODIC COMMIT 10000
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

            //Create the load node(s)
            MERGE (l:Load:Entity {primaryKey:row.loadKey})
                SET l.dateProduced = row.dateProduced,
                 l.loadName = "BGI",
                 l.release = row.release,
                 l.dataProviders = row.dataProviders,
                 l.dataProvider = row.dataProvider

            //Create the Gene node and set properties. primaryKey is required.
            MERGE (o:Gene {primaryKey:row.primaryId})
                SET o.symbol = row.symbol,
                 o.taxonId = row.taxonId,
                 o.name = row.name,
                 o.description = row.description,
                 o.geneSynopsisUrl = row.geneSynopsisUrl,
                 o.geneSynopsis = row.geneSynopsis,
                 o.geneLiteratureUrl = row.geneLiteratureUrl,
                 o.geneticEntityExternalUrl = row.geneticEntityExternalUrl,
                 o.dateProduced = row.dateProduced,
                 o.modGlobalCrossRefId = row.modGlobalCrossRefId,
                 o.modCrossRefCompleteUrl = row.modCrossRefCompleteUrl,
                 o.modLocalId = row.localId,
                 o.modGlobalId = row.modGlobalId,
                 o.uuid = row.uuid,
                 o.dataProvider = row.dataProvider,
                 o.dataProviders = row.dataProviders

            MERGE (l)-[loadAssociation:LOADED_FROM]-(o)
            //Create nodes for other identifiers.

            //FOREACH (dataProvider in row.dataProviders |
                //MERGE (dp:DataProvider:Entity {primaryKey:dataProvider})
                  //SET dp.dateProduced = row.dateProduced
                //MERGE (o)-[odp:DATA_PROVIDER]-(dp)
               // MERGE (l)-[ldp:DATA_PROVIDER]-(dp))

            MERGE (spec:Species {primaryKey: row.taxonId})
                SET spec.species = row.species
                SET spec.name = row.species
            MERGE (o)-[:FROM_SPECIES]->(spec)
            MERGE (l)-[laspec:LOADED_FROM]-(spec)

            //MERGE the SOTerm node and set the primary key.
            MERGE (s:SOTerm:Ontology {primaryKey:row.soTermId})
            MERGE (l)-[laso:LOADED_FROM]-(s)

            //Create the relationship from the gene node to the SOTerm node.
            MERGE (o)-[x:ANNOTATED_TO]->(s) """

    xrefs_template = """

        USING PERIODIC COMMIT 10000
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS event

            MATCH (o:Gene {primaryKey:event.dataId}) """ + CreateCrossReference.get_cypher_xref_text()

    def __init__(self, config):
        super().__init__()
        self.data_type_config = config

    def _load_and_process_data(self):
        
        for mod_config in self.data_type_config.get_mod_configs():
            data = mod_config.get_data()
            
            bgi_dataset = self.get_generators(data, mod_config.species, 1000)

            for bgi_batch in bgi_dataset:
                Neo4jTransactor.execute_transaction(bgi_batch[0], "gene_data_" + mod_config.species + ".csv", BGIETL.gene_query_template)
                Neo4jTransactor.execute_transaction(bgi_batch[1], "gene_synonyms_" + mod_config.species + ".csv", BGIETL.gene_synonyms_template)
                Neo4jTransactor.execute_transaction(bgi_batch[2], "gene_secondaryIds_" + mod_config.species + ".csv", BGIETL.gene_secondaryIds_template)
                Neo4jTransactor.execute_transaction(bgi_batch[3], "gene_genomicLocations_" + mod_config.species + ".csv", BGIETL.genomic_locations_template)
                Neo4jTransactor.execute_transaction(bgi_batch[4], "gene_crossReferences_" + mod_config.species + ".csv", BGIETL.xrefs_template)

    def get_generators(self, gene_data, species, batch_size):
        xrefUrlMap = ResourceDescriptor().get_data()
        dateProduced = gene_data['metaData']['dateProduced']
        dataProviders = []
        synonyms = []
        secondaryIds = []
        crossReferences = []
        genomicLocations = []
        gene_dataset = []
        release = None
        counter = 0

        dataProviderObject = gene_data['metaData']['dataProvider']

        dataProviderCrossRef = dataProviderObject.get('crossReference')
        dataProvider = dataProviderCrossRef.get('id')
        dataProviderPages = dataProviderCrossRef.get('pages')
        dataProviderCrossRefSet = []

        loadKey = dateProduced + dataProvider + "_BGI"

        if dataProviderPages is not None:
            for dataProviderPage in dataProviderPages:
                crossRefCompleteUrl = UrlService.get_page_complete_url(dataProvider, xrefUrlMap, dataProvider, dataProviderPage)
                dataProviderCrossRefSet.append(CreateCrossReference.get_xref(dataProvider, dataProvider, dataProviderPage, dataProviderPage, dataProvider, crossRefCompleteUrl, dataProvider + dataProviderPage))
                dataProviders.append(dataProvider)
                logger.info("data provider: " + dataProvider)

        dataProviderSingle = DataProvider().get_data_provider(species)

        if 'release' in gene_data['metaData']:
            release = gene_data['metaData']['release']

        for geneRecord in gene_data['data']:
            counter = counter + 1


            primary_id = geneRecord['primaryId']
            global_id = geneRecord['primaryId']

            local_id = global_id.split(":")[1]
            geneLiteratureUrl = ""
            geneticEntityExternalUrl = ""
            modCrossReferenceCompleteUrl = ""
            taxonId = geneRecord.get("taxonId")

            if geneRecord['taxonId'] == "NCBITaxon:9606" or geneRecord['taxonId'] == "NCBITaxon:10090":
                local_id = geneRecord['primaryId']

            if self.testObject.using_test_data() is True:
                is_it_test_entry = self.testObject.check_for_test_id_entry(primary_id)
                if is_it_test_entry is False:
                    counter = counter - 1
                    continue

            #TODO: can we split this off into another class?

            if 'crossReferences' in geneRecord:
                for crossRef in geneRecord['crossReferences']:
                    if ':' in crossRef.get('id'):
                        crossRefId = crossRef.get('id')
                        localCrossRefId = crossRefId.split(":")[1]
                        prefix = crossRef.get('id').split(":")[0]
                        pages = crossRef.get('pages')
                        globalXrefId = crossRef.get('id')
                        displayName = globalXrefId

                        # some pages collection have 0 elements
                        if pages is not None and len(pages) > 0:
                            for page in pages:
                                modCrossReferenceCompleteUrl = ""
                                geneLiteratureUrl = ""
                                displayName = ""

                                crossRefCompleteUrl = UrlService.get_page_complete_url(localCrossRefId, xrefUrlMap, prefix, page)

                                if page == 'gene':
                                    modCrossReferenceCompleteUrl = UrlService.get_page_complete_url(localCrossRefId, xrefUrlMap, prefix, prefix + page)

                                geneticEntityExternalUrl = UrlService.get_page_complete_url(localCrossRefId, xrefUrlMap, prefix, prefix + page)

                                if page == 'gene/references':
                                    geneLiteratureUrl = UrlService.get_page_complete_url(localCrossRefId, xrefUrlMap, prefix, prefix + page)

                                if page == 'gene/spell':
                                    displayName='Serial Patterns of Expression Levels Locator (SPELL)'

                                # TODO: fix generic_cross_reference in SGD, RGD

                                if page == 'generic_cross_reference':
                                    crossRefCompleteUrl = UrlService.get_no_page_complete_url(localCrossRefId, xrefUrlMap, prefix, primary_id)

                                # TODO: fix gene/disease xrefs for SGD once resourceDescriptor change in develop
                                # makes its way to the release branch.

                                if page == 'gene/disease' and species == 'Saccharomyces cerevisiae':
                                    crossRefCompleteUrl = "https://www.yeastgenome.org/locus/"+local_id+"/disease"

                                xrefMap = CreateCrossReference.get_xref(localCrossRefId, prefix, page, page, displayName, crossRefCompleteUrl, globalXrefId+page)
                                xrefMap['dataId'] = primary_id
                                crossReferences.append(xrefMap)

                        else:
                            if prefix == 'PANTHER':  # TODO handle in the resourceDescriptor.yaml
                                crossRefPrimaryId = crossRef.get('id') + '_' + primary_id
                                crossRefCompleteUrl = UrlService.get_no_page_complete_url(localCrossRefId, xrefUrlMap, prefix, primary_id)
                                xrefMap = CreateCrossReference.get_xref(localCrossRefId, prefix, "gene/panther", "gene/panther", displayName, crossRefCompleteUrl, crossRefPrimaryId + "gene/panther")
                                xrefMap['dataId'] = primary_id
                                crossReferences.append(xrefMap)

                            else:
                                crossRefPrimaryId = crossRef.get('id')
                                crossRefCompleteUrl = UrlService.get_no_page_complete_url(localCrossRefId, xrefUrlMap, prefix, primary_id)
                                xrefMap = CreateCrossReference.get_xref(localCrossRefId, prefix, "generic_cross_reference", "generic_cross_reference", displayName, crossRefCompleteUrl, crossRefPrimaryId + "generic_cross_reference")
                                xrefMap['dataId'] = primary_id
                                crossReferences.append(xrefMap)

            gene = {
                "symbol": geneRecord.get('symbol'),
                "name": geneRecord.get('name'),
                "geneticEntityExternalUrl": geneticEntityExternalUrl,
                "description": geneRecord.get('description'),
                "soTermId": geneRecord['soTermId'],
                "geneSynopsis": geneRecord.get('geneSynopsis'),
                "geneSynopsisUrl": geneRecord.get('geneSynopsisUrl'),
                "taxonId": geneRecord['taxonId'],
                "species": SpeciesService.get_species(taxonId),
                "geneLiteratureUrl": geneLiteratureUrl,
                "name_key": geneRecord.get('symbol'),
                "primaryId": primary_id,
                "category": "gene",
                "dateProduced": dateProduced,
                "dataProviders": dataProviders,
                "dataProvider": dataProviderSingle,
                "release": release,
                "href": None,
                "uuid": str(uuid.uuid4()),
                "modCrossRefCompleteUrl": modCrossReferenceCompleteUrl,
                "localId": local_id,
                "modGlobalCrossRefId": global_id,
                "modGlobalId": global_id,
                "loadKey": loadKey
            }
            gene_dataset.append(gene)

            if 'genomeLocations' in geneRecord:
                for genomeLocation in geneRecord['genomeLocations']:
                    chromosome = genomeLocation['chromosome']
                    assembly = genomeLocation['assembly']
                    if 'startPosition' in genomeLocation:
                        start = genomeLocation['startPosition']
                    else:
                        start = None
                    if 'endPosition' in genomeLocation:
                        end = genomeLocation['endPosition']
                    else:
                        end = None
                    if 'strand' in geneRecord['genomeLocations']:
                        strand = genomeLocation['strand']
                    else:
                        strand = None
                    genomicLocations.append(
                        {"primaryId": primary_id, "chromosome": chromosome, "start":
                            start, "end": end, "strand": strand, "assembly": assembly})

            if geneRecord.get('synonyms') is not None:
                for synonym in geneRecord.get('synonyms'):
                    geneSynonym = {
                        "primary_id": primary_id,
                        "synonym": synonym
                    }
                    synonyms.append(geneSynonym)

            if geneRecord.get('secondaryIds') is not None:
                for secondaryId in geneRecord.get('secondaryIds'):
                    geneSecondaryId = {
                        "primary_id": primary_id,
                        "secondary_id": secondaryId
                    }
                    secondaryIds.append(geneSecondaryId)
            
            # Establishes the number of genes to yield (return) at a time.
            if counter == batch_size:
                counter = 0
                yield (gene_dataset, synonyms, secondaryIds, genomicLocations, crossReferences)
                gene_dataset = []
                synonyms = []
                secondaryIds = []
                genomicLocations = []
                crossReferences = []

        if counter > 0:
            yield (gene_dataset, synonyms, secondaryIds, genomicLocations, crossReferences)
