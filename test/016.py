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
        c.load(mrcfile="test/marcxml/016s.xml", filetype="xml")
        c.convert()
        self.g = c.graph()   
        print(c.serialize('n3').decode("utf-8"))

    
    def test_invalid_016s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Local .
                ?id rdf:value "89000298##" .
                ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> .
                ?id bf:source <https://www.bac-lac.gc.ca/> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: 89000298## is invalid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: 89000298## not found as invalid identifier on Instance.")
            

    def test_valid_016s_on_instance_1(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Local .
                ?id rdf:value "PTBN000004618" .
                ?id bf:source <http://id.loc.gov/vocabulary/organizations/polibn> .
                FILTER( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: PTBN000004618 is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: PTBN000004618 not found as valid identifier on Instance.")
            

    def test_valid_016s_on_instance_2(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Local .
                ?id rdf:value "94.763966.7" .
                FILTER ( NOT EXISTS { ?id bf:status <http://id.loc.gov/vocabulary/mstatus/cancinv> . } ) .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: '94.763966.7' is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: '94.763966.7' not found as valid identifier on Instance.")
            
    def test_valid_016s_on_instance_3(self):
        ask_query = """
            ASK {
                ?w a bf:Instance .
                ?w bf:identifiedBy ?id . 
                ?id a bf:Local .
                ?id rdf:value "#890000298##rev" .
                ?id bf:source <https://www.bac-lac.gc.ca/> .
            }
            """
        ask_answer = bool(self.g.query(pfx_decl + ask_query))
        if ask_answer:
            self.assertTrue(True, "PASS: '#890000298##rev' is valid identifier on Instance.")
        else:
            self.assertTrue(False, "FAIL: '#890000298##rev' not found as valid identifier on Instance.")


def suite():
    test_suite = unittest.makeSuite(IdentifiersTest, 'test')
    return test_suite

if __name__ == "__main__":
    unittest.main()


