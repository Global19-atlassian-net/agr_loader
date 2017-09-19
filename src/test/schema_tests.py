from neo4j.v1 import GraphDatabase
import os
import pytest

# Query to return all distinct node labels:
# MATCH (n) RETURN DISTINCT labels(n)

nodeLabels = ['Ontology', 'SOTerm', 'DOTerm', 'Identifier', 'Gene', 'Synonym', 'CrossReference', \
              'Species', 'Entity', 'Chromosome', 'DiseaseGeneJoin', 'Association', 'Publication', \
              'EvidenceCode', 'GOTerm']

# Query to return all distinct properties from all nodes of a certain type:
# MATCH (n:Gene) WITH DISTINCT keys(n) AS keys UNWIND keys AS keyslisting WITH DISTINCT keyslisting AS allfields RETURN allfields;

geneRequiredProperties = ['modGlobalCrossRefId', 'dateProduced', 'geneLiteratureUrl', 'dataProvider',  \
                  'modCrossRefCompleteUrl', 'taxonId', 'geneticEntityExternalUrl', 'modLocalId', \
                  'symbol', 'name', 'primaryKey', 'modGlobalId']

sotermRequiredProperties = ['name', 'primaryKey']

dotermRequiredProperties = ['doPrefix', 'doId', 'doDisplayId', 'doUrl', 'defLinks', 'is_obsolete', 'subset', \
                           'name', 'nameKey', 'primaryKey', 'definition']

identifierRequiredProperties = ['primaryKey']

synonymRequiredProperties = ['primaryKey', 'name']

crossReferenceRequiredProperties = ['localId', 'name', 'crossRefCompleteUrl', 'primaryKey', 'prefix']

def execute_transaction(query):
    host = os.environ['NEO4J_NQC_HOST']
    port = os.environ['NEO4J_NQC_PORT']
    uri = "bolt://" + host + ":" + port
    graph = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

    result = None

    with graph.session() as session:
        result = session.run(query)

    return result    

@pytest.mark.parametrize("data", nodeLabels)
def test_node_labels(data):
    query = 'MATCH (n:%s) RETURN distinct count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] > 0

@pytest.mark.parametrize("data", geneRequiredProperties)
def test_gene_properties(data):
    query = 'MATCH (n:Gene) WHERE NOT EXISTS(n.%s) RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", geneRequiredProperties)
def test_gene_properties_not_null(data):
    query = 'MATCH (n:Gene) WHERE n.%s is NULL RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", sotermRequiredProperties)
def test_soterm_properties(data):
    query = 'MATCH (n:SOTerm) WHERE NOT EXISTS(n.%s) RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", sotermRequiredProperties)
def test_soterm_properties_not_null(data):
    query = 'MATCH (n:SOTerm) WHERE n.%s is NULL RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", dotermRequiredProperties)
def test_doterm_properties(data):
    query = 'MATCH (n:DOTerm) WHERE NOT EXISTS(n.%s) RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", dotermRequiredProperties)
def test_doterm_properties_not_null(data):
    query = 'MATCH (n:DOTerm) WHERE n.%s is NULL RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", identifierRequiredProperties)
def test_identifier_properties(data):
    query = 'MATCH (n:Identifier) WHERE NOT EXISTS(n.%s) RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", identifierRequiredProperties)
def test_identifier_properties_not_null(data):
    query = 'MATCH (n:Identifier) WHERE n.%s is NULL RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", synonymRequiredProperties)
def test_synonym_properties(data):
    query = 'MATCH (n:synonym) WHERE NOT EXISTS(n.%s) RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", synonymRequiredProperties)
def test_synonym_properties_not_null(data):
    query = 'MATCH (n:synonym) WHERE n.%s is NULL RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", crossReferenceRequiredProperties)
def test_cross_reference_properties(data):
    query = 'MATCH (n:CrossReference) WHERE NOT EXISTS(n.%s) RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0

@pytest.mark.parametrize("data", crossReferenceRequiredProperties)
def test_cross_reference_properties_not_null(data):
    query = 'MATCH (n:CrossReference) WHERE n.%s is NULL RETURN count(n) as count' % (data)

    result = execute_transaction(query)
    for record in result:
        assert record["count"] == 0