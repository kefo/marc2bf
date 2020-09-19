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
        c.load(mrcfile="test/marcxml/010s.xml", filetype="xml")
        c.convert()
        self.g = c.graph()
        print(c.serialize('n3').decode("utf-8"))


    '''
    def test_invalid_010s_on_work_1(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "6" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 6 is invalid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 6 not found as invalid identifier on Work.")
            

    def test_invalid_010s_on_work_2(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "7" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
            }
            """
        ask_answer = bool(self.
        g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 7 is invalid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 7 not found as invalid identifier on Work.")
            

    def test_valid_010s_on_work_1(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "5" .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 5 is valid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 5 not found as valid identifier on Work.")
            

    def test_valid_010s_on_work_2(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "   82060878 " .
                FILTER ( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: '   82060878 ' is valid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: '   82060878 ' not found as valid identifier on Work.")
    '''

    def test_leader_as_local_identifier_on_instance(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:adminMetadata ?am .
                ?am bf:identifiedBy ?id . 
                ?id a bf:Local .
                ?id rdf:value "5226" .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 5226 is valid local identifier on Instance Admin Metadata.")
        else:
            self.assertTrue(False, "FAIL: 5226 not found as valid local identifier on Instance Admin Metadata.")
            

    def test_invalid_010s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "6" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 6 is invalid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 6 not found as invalid identifier on Instance.")
            

    def test_invalid_010s_on_instance_2(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "7" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 7 is invalid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 7 not found as invalid identifier on Instance.")


    def test_valid_010s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "5" .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 5 is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 5 not found as valid identifier on Instance.")
            


    def test_valid_010s_on_instance_2(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Lccn .
                ?id rdf:value "   82060878 " .
                FILTER ( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: '   82060878 ' is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: '   82060878 ' not found as valid identifier on Instance.")

def suite():
    test_suite = unittest.makeSuite(IdentifiersTest, 'test')
    return test_suite

if __name__ == "__main__":
    unittest.main()

