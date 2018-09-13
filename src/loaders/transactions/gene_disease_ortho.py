# coding=utf-8

import csv
import uuid
from datetime import datetime, timezone
from .transaction import Transaction


class GeneDiseaseOrthoTransaction(Transaction):
    def __init__(self, graph):
        Transaction.__init__(self, graph)
        self.neo_import_dir = '/var/lib/neo4j/import/'
        self.filename = 'disease_by_orthology.csv'

        # Add publication and evidence code
        query = """
              MERGE (pubg:Publication {primaryKey:"MGI:6194238"})
                  SET pubg.pubModId = "MGI:6194238"
                  SET pubg.pubModUrl = "http://www.informatics.jax.org/reference/summary?id=mgi:6194238"
              MERGE (:EvidenceCode {primaryKey:"IEA"})"""
        tx = Transaction(graph)
        tx.run_single_query(query)

    def retreive_diseases_inferred_by_ortholog(self):
        query = """
        MATCH (disease:DOTerm)-[da]-(allele:Feature)-[ag:IS_ALLELE_OF]-(gene1:Gene)-[o:ORTHOLOGOUS]->(gene2:Gene)
        MATCH (ec)-[:EVIDENCE]-(dej:DiseaseEntityJoin)-[e]-(allele)-[ag]-(gene1)-[FROM_SPECIES]->(species:Species)
             WHERE o.strictFilter
                 AND da.uuid = dej.primaryKey
                 AND NOT ec.primaryKey IN ["IEA", "ISS", "ISO"]
        OPTIONAL MATCH (disease:DOTerm)-[da2]-(gene2:Gene)-[ag2:IS_ALLELE_OF]->(:Feature)-[da3]-(disease:DOTerm)
            WHERE da2 IS null  // filters relations that already exist
                 AND da3 IS null // filter where allele already has disease association
        RETURN DISTINCT gene2.primaryKey AS geneID,
               species.primaryKey AS speciesID,
               type(da) AS relationType,
               disease.primaryKey AS doId
        UNION
        MATCH (disease:DOTerm)-[da]-(gene1:Gene)-[o:ORTHOLOGOUS]->(gene2:Gene)
        MATCH (ec)-[:EVIDENCE]-(dej:DiseaseEntityJoin)-[e]-(gene1)-[FROM_SPECIES]->(species:Species)
             WHERE o.strictFilter
                 AND da.uuid = dej.primaryKey
                 AND NOT ec.primaryKey IN ["IEA", "ISS", "ISO"]
        OPTIONAL MATCH (disease:DOTerm)-[da2]-(gene2:Gene)-[ag:IS_ALLELE_OF]->(:Feature)-[da3]-(disease:DOTerm)
            WHERE da2 IS null  // filters relations that already exist
                 AND da3 IS null // filter where allele already has disease association
        RETURN DISTINCT gene2.primaryKey AS geneID,
               species.primaryKey AS speciesID,
               type(da) AS relationType,
               disease.primaryKey AS doId"""

        orthologous_disease_data = []
        tx = Transaction(self.graph)
        returnSet = tx.run_single_query(query)
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        filepath = self.neo_import_dir + self.filename
        print("creating: " + filepath)
        with open(filepath, 'w') as csvfile:
            fieldnames = ["primaryId", "speciesId", "relationshipType", "doId", "dateProduced", "uuid"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for record in returnSet:
                writer.writerow({"primaryId": record["geneID"],
                                 "speciesId": record["speciesID"],
                                 "relationshipType": record["relationType"].lower(),
                                 "doId": record["doId"],
                                 "dateProduced": now,
                                 "uuid": str(uuid.uuid4())})

    def add_disease_inferred_by_ortho_tx(self):
        # Loads the gene to disease via ortho data into Neo4j.

        executeG2D = """

            LOAD CSV WITH HEADERS FROM "file:///""" + self.filename + """" AS row

            MATCH (d:DOTerm:Ontology {primaryKey:row.doId}),
                  (gene:Gene {primaryKey:row.primaryId}),
                  (species:Species {primaryKey:row.speciesId}),
                  (pub:Publication {primaryKey:"MGI:6194238"}),
                  (ecode:EvidenceCode {primaryKey:"IEA"})

            MERGE (dga:Association {primaryKey:row.uuid})
                SET dga :DiseaseEntityJoin

            FOREACH (rel IN CASE when row.relationshipType = 'is_marker_for' THEN [1] ELSE [] END |
                MERGE (gene)<-[fafg:IS_MARKER_FOR {uuid:row.uuid}]->(d)
                    SET fafg.dataProvider = "Alliance"
                    SET fafg.dateProduced = row.dateProduced
                    SET dga.joinType = row.relationshipType)

            FOREACH (rel IN CASE when row.relationshipType = 'is_implicated_in' THEN [1] ELSE [] END |
                MERGE (gene)<-[fafg:IS_IMPLICATED_IN {uuid:row.uuid}]->(d)
                    SET fafg.dataProvider = "Alliance"
                    SET fafg.dateProduced = row.dateProduced
                    SET dga.joinType = row.relationshipType)

            MERGE (gene)-[fdag:ASSOCIATION]->(dga)
            MERGE (dga)-[dadg:ASSOCIATION]->(d)

            MERGE (dga)-[dapug:EVIDENCE]->(pub)
            MERGE (dga)-[:FROM_SPECIES]-(species)

            MERGE (dga)-[daecode1g:EVIDENCE]->(ecode)

            """

        Transaction.run_single_query(self, executeG2D)
