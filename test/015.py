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
        c.load(mrcfile="test/marcxml/015s.xml", filetype="xml")
        c.convert()
        self.g = c.graph()   
        # print(c.serialize('n3').decode("utf-8"))


    def test_invalid_015s_on_work_1(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "67-A14-54" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/dnb> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 67-A14-54 is invalid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 67-A14-54 not found as invalid identifier on Work.")
            

    def test_invalid_015s_on_work_2(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "05,N51,1204" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/dnb> .
            }
            """
        ask_answer = bool(self.
        g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 05,N51,1204 is invalid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 05,N51,1204 not found as invalid identifier on Work.")
            

    def test_valid_015s_on_work_1(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "06,A29,1122" .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/dnb> .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 06,A29,1122 is valid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 06,A29,1122 not found as valid identifier on Work.")
            

    def test_valid_015s_on_work_2(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "B67-20988" .
                ?id bf:qualifier "pbk" .
                FILTER ( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 'B67-20988' is valid identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: 'B67-20988' not found as valid identifier on Work.")
            
    def test_valid_015s_on_work_3(self):
        ask_query = """
            ASK {
                ?w a bf:Work .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "67-A14-55" .
                ?id bf:qualifier "some extra info" .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/bnf> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: some extra info found on Nbn identifier on Work.")
        else:
            self.assertTrue(False, "FAIL: some extra info NOT found on Nbn identifier on Work.")


    
    def test_invalid_015s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "67-A14-54" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/dnb> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 67-A14-54 is invalid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 67-A14-54 not found as invalid identifier on Instance.")
            

    def test_invalid_015s_on_instance_2(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "05,N51,1204" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/dnb> .
            }
            """
        ask_answer = bool(self.
        g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 05,N51,1204 is invalid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 05,N51,1204 not found as invalid identifier on Instance.")
            

    def test_valid_015s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "06,A29,1122" .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/dnb> .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 06,A29,1122 is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 06,A29,1122 not found as valid identifier on Instance.")
            

    def test_valid_015s_on_instance_2(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "B67-20988" .
                ?id bf:qualifier "pbk" .
                FILTER ( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 'B67-20988' is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 'B67-20988' not found as valid identifier on Instance.")
            
    def test_valid_015s_on_instance_3(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Nbn .
                ?id rdf:value "67-A14-55" .
                ?id bf:qualifier "some extra info" .
                ?id bf:source <http://id.loc.gov/vocabulary/nationalbibschemes/bnf> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: some extra info found on Nbn identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: some extra info NOT found on Nbn identifier on Instance.")


def suite():
    test_suite = unittest.makeSuite(IdentifiersTest, 'test')
    return test_suite

if __name__ == "__main__":
    unittest.main()


