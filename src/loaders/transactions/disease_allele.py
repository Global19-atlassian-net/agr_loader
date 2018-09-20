from .transaction import Transaction


class DiseaseAlleleTransaction(Transaction):
    def __init__(self, graph):
        Transaction.__init__(self, graph)

    def disease_allele_object_tx(self, data):
        # Loads the Disease data into Neo4j.

        executeFeature = """
            UNWIND $data as row
            // GET PRIMARY DATA OBJECTS

            MATCH (d:DOTerm:Ontology {primaryKey:row.doId})
            MATCH (feature:Feature {primaryKey:row.primaryId})
            MATCH (g:Gene)-[a:IS_ALLELE_OF]-(feature)

            // LOAD NODES
            MERGE (l:Load:Entity {primaryKey:row.loadKey})
                SET l.dateProduced = row.dateProduced,
                 l.loadName = "Disease",
                 l.dataProviders = row.dataProviders,
                 l.dataProvider = row.dataProvider


            MERGE (dfa:Association:DiseaseEntityJoin {primaryKey:row.uuid})
                SET dfa.dataProviders = row.dataProviders
                
            MERGE (dfa)-[dfal:LOADED_FROM]-(l)

            FOREACH (rel IN CASE when row.relationshipType = 'is_marker_for' THEN [1] ELSE [] END |
                MERGE (feature)<-[faf:IS_MARKER_FOR {uuid:row.uuid}]->(d)
                SET faf.dateProduced = row.dateProduced,
                 faf.dataProvider = row.dataProvider,
                 dfa.joinType = 'is_marker_of'
            )

            FOREACH (rel IN CASE when row.relationshipType = 'is_implicated_in' THEN [1] ELSE [] END |
                MERGE (feature)<-[faf:IS_IMPLICATED_IN {uuid:row.uuid}]->(d)
                SET faf.dateProduced = row.dateProduced,
                 faf.dataProvider = row.dataProvider,
                 dfa.joinType = 'is_implicated_in'
            )

            //FOREACH (dataProvider in row.dataProviders |
                //MERGE (dp:DataProvider {primaryKey:dataProvider})
                //MERGE (dfa)-[odp:DATA_PROVIDER]-(dp)
                //MERGE (l)-[ldp:DATA_PROVIDER]-(dp))


            MERGE (feature)-[fdaf:ASSOCIATION]->(dfa)
            MERGE (dfa)-[dadf:ASSOCIATION]->(d)
            MERGE (g)-[gadf:ASSOCIATION]->(dfa)

            // PUBLICATIONS FOR FEATURE
            MERGE (pubf:Publication {primaryKey:row.pubPrimaryKey})
                SET pubf.pubModId = row.pubModId,
                 pubf.pubMedId = row.pubMedId,
                 pubf.pubModUrl = row.pubModUrl,
                 pubf.pubMedUrl = row.pubMedUrl

            MERGE (l)-[loadAssociation:LOADED_FROM]-(pubf)
            MERGE (dfa)-[dapuf:EVIDENCE]->(pubf)

            // EVIDENCE CODES FOR FEATURE
            FOREACH (entity in row.ecodes|
                MERGE (ecode1f:EvidenceCode {primaryKey:entity})
                MERGE (dfa)-[daecode1f:EVIDENCE]->(ecode1f)
            )
            """

        deleteEmptyDONodes = """
            MATCH (dd:DOTerm) WHERE keys(dd)[0] = 'primaryKey' and size(keys(dd)) = 1
            DETACH DELETE (dd)
        """

        Transaction.execute_transaction(self, executeFeature, data)
        Transaction.execute_transaction(self, deleteEmptyDONodes, data)
