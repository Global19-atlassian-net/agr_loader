import logging

logger = logging.getLogger(__name__)
import multiprocessing
from .helpers import ETLHelper
from etl import ETL
from transactors import Neo4jTransactor


class MolInteractionsXrefETL(ETL):

    query_xref = """
        PROFILE
        USING PERIODIC COMMIT %s
        LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row WITH row LIMIT 0

        // This needs to be a MERGE below.
        MATCH (o:InteractionGeneJoin {primaryKey:row.reference_uuid}) """ + ETLHelper.get_cypher_xref_tuned_text()

    xrefs_relationships_template = """
    
        USING PERIODIC COMMIT %s
            LOAD CSV WITH HEADERS FROM \'file:///%s\' AS row

            MATCH (o:InteractionGeneJoin {primaryKey:row.reference_uuid})
            MATCH (c:CrossReference {primaryKey:row.primaryKey})
            
            MERGE (o)-[oc:CROSS_REFERENCE]-(c)
            
    """

    def __init__(self, config):
        super().__init__()
        self.data_type_config = config

    def _load_and_process_data(self):

        commit_size = self.data_type_config.get_neo4j_commit_size()

        all_query_list = [
            [MolInteractionsXrefETL.query_xref, commit_size, "mol_int_xref.csv"],
            [MolInteractionsXrefETL.xrefs_relationships_template, commit_size, "mol_int_xref.csv"]
        ]

        query_list = self.process_query_params(all_query_list)
        Neo4jTransactor.execute_query_batch(query_list)