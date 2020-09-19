import unittest
import os

from marc2bf.converter import M2BFConverter

from rdflib import namespace
from rdflib.namespace import Namespace

ns_collection = {
    'dc' : namespace.DC,
    'dcterms' : namespace.DCTERMS,
    'foaf' : namespace.FOAF,
    'geo' : Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#'),
    'ldp' : Namespace('http://www.w3.org/ns/ldp#'),
    'owl' : namespace.OWL,
    'premis' : Namespace('http://www.loc.gov/premis/rdf/v1#'),
    'rdf' : namespace.RDF,
    'rdfs' : namespace.RDFS,
    'rel' : Namespace('http://id.loc.gov/vocabulary/relators/'),
    'skos' : namespace.SKOS,
    'xsd' : namespace.XSD,
    
    'bf' : Namespace('http://id.loc.gov/ontologies/bibframe/'),
    'bflc' : Namespace('http://id.loc.gov/ontologies/bflc/'),
}


# Collection of prefixes in a dict.
ns_pfx_sparql = {}
for ns,uri in ns_collection.items():
    ns_pfx_sparql[ns] = 'PREFIX {}: <{}>'.format(ns, uri)

# Prefix declarations formatted for SPARQL queries.
pfx_decl='\n'.join(ns_pfx_sparql.values())

class IdentifiersTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        c = M2BFConverter()
        c.load(mrcfile="test/marcxml/017s.xml", filetype="xml")
        c.convert()
        self.g = c.graph()   
        print(c.serialize('n3').decode("utf-8"))

    
    def test_invalid_017s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:CopyrightNumber .
                ?id rdf:value "EU781596" .
                ?id bf:source ?source .
                ?source rdf:type bf:Agent .
                ?source rdfs:label "U.S. Copyright Office" .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: EU781596 is valid CopyrightNumber on Instance.")
        else:
            self.assertTrue(False, "FAIL: EU781596 not found as valid identifier on Instance.")
            

    def test_valid_017s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:CopyrightNumber .
                ?id rdf:value "A1116341" .
                ?id bf:date "20020703" . 
                ?id bf:source ?source .
                ?source rdf:type bf:Agent .
                ?source rdfs:label "U.S. Copyright Office" .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: A1116341is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: A1116341 not found as valid identifier on Instance.")
            

    def test_valid_017s_on_instance_2(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:CopyrightNumber .
                ?id rdf:value "PA52-759 (English language dubbed version)" .
                ?id bf:source ?source .
                ?source rdf:type bf:Agent .
                ?source rdfs:label "U.S. Copyright Office" .
                FILTER ( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 'PA52-759 (English language dubbed version)' is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 'PA52-759 (English language dubbed version)' not found as valid identifier on Instance.")
            
    def test_valid_017s_on_instance_3(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:CopyrightNumber .
                ?id rdf:value "M444120-2006" .
                FILTER ( EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 'M444120-2006' is an invalid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 'M444120-2006' not found as an invalid identifier on Instance.")


def suite():
    test_suite = unittest.makeSuite(IdentifiersTest, 'test')
    return test_suite

if __name__ == "__main__":
    unittest.main()


