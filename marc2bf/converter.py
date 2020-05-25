import sys
import json

from copy import deepcopy

from rdflib import Graph, Literal, URIRef
# from rdflib.plugin import Serializer

from pymarc import MARCReader, parse_xml_to_array

class M2BFConverter:
    
    _prefixblock = """
            PREFIX bf: <http://id.loc.gov/ontologies/bibframe/> 
            PREFIX bflc: <http://id.loc.gov/ontologies/bflc/>
            PREFIX madsrdf: <http://www.loc.gov/mads/rdf/v1#>
            PREFIX iddatatypes: <http://id.loc.gov/datatypes/edtf>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            """
    _context = {
            "bf": "http://id.loc.gov/ontologies/bibframe/",
            "madsrdf": "http://www.loc.gov/mads/rdf/v1#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "bflc": "http://id.loc.gov/ontologies/bflc/",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "bfdr": "http://github.com/kefo/bfdr/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        }
    _graph = []
    _urirefs = {}

    def __init__(
        self,
        config: object = {},
    ) -> None:
        self.config = config
        self._g = Graph()
        self.set_profile()
        self.records = []
        return None

    def load(
        self,
        mrcfile: str = '',
        filetype: str = 'mrc'
    ) -> None:
        if filetype == "mrc":
            with open(mrcfile, 'rb') as fh:
                reader = MARCReader(fh)
                for record in reader:
                    self.records.append(record)
        elif filetype == "xml":
            self.records = parse_xml_to_array(mrcfile)
        return None    

    def convert(
        self
    ) -> None:
        self._graph = []
        self._g = Graph()
        for robj in self.records:
            rdict = robj.as_dict()
            # print(rdict)
            r = {}
            r["leader"] = [rdict["leader"]]
            for f in rdict["fields"]:
                for k in f:
                    field = f[k]
                    if k in r:
                        r[k].append(field)
                    else:
                        r[k] = [field]
            # print(r)
            for profile in self._profile:
                uri = ""
                resource = {"@type": profile["resourcetype"]}
                if 'seturi' in profile:
                    if not isinstance(profile["seturi"], list):
                        profile["seturi"] = [profile["seturi"]]
                    for urifilter in profile["seturi"]:
                        filterfn = urifilter[0]
                        if len(urifilter) == 1:
                            uri = filterfn()
                        else:
                            filterparams = urifilter[1]
                            uri = filterfn(filterparams)
                        
                    resource["@id"] = uri
                if 'uriref' in profile and uri != "":
                    self._urirefs[profile["uriref"]] = uri
                    
                for i in profile["properties"]:
                    field = i["field"]
                    prop = i["property"]
                    fn = i["pattern"][0]
                    params = i["pattern"][1]
                    for f in r[field]:
                        if "data" in params:
                            if not isinstance(params["data"], list):
                                params["data"] = [params["data"]]
                            primarydata = params["data"][0]
                            datafn = primarydata[0]
                            datafields = []
                            for df in primarydata[1]:
                                if ':' in df:
                                    datafields.append(eval('f' + df))
                                elif df == "ind1" or df == "ind2":
                                   datafields.append(f[df])
                                elif "subfields" in f:
                                    for sf in f["subfields"]:
                                        key = list(sf.keys())[0]
                                        if df == key:
                                            datafields.append(sf[key])
                                elif '=' in df:
                                    datafields.append(df.split("=")[1])
                                elif df.startswith('%') and df.endswith("%"):
                                    if df in self._urirefs:
                                        datafields.append(self._urirefs[df])
                            if datafn != None:
                                fielddata = datafn(datafields)
                                if not isinstance(fielddata, list):
                                    fielddata = [fielddata]
                            else:
                                fielddata = datafields
                            if len(params["data"]) > 1:
                                for additionaldata in params["data"][1:]:
                                    additionaldatafn = additionaldata[0]
                                    additionaldataparams = additionaldata[1]
                                    fielddata = additionaldatafn(fielddata, additionaldataparams)
                                    if not isinstance(fielddata, list):
                                        fielddata = [fielddata]
                            params["data"] = fielddata
                        objectdata = fn(**params)
                        resource[prop] = objectdata
                self._graph.append(resource)
                print(resource)
                
        self.jsonld_obj = {
            "@context": self._context,
            "@graph": self._graph
        }
        return self.jsonld_obj
        
    def serialize(
        self,
        format: str = "pretty-xml"
    ) -> str:
        jsonld_str = json.dumps(self.jsonld_obj)
        self._g.parse(data=jsonld_str, format='json-ld')
        return self._g.serialize(format=format)
        
    def set_profile(
        self,
        use_profile: str = 'bfdr'
    ) -> None:
        if type(use_profile) is str:
            if use_profile == "bfdr":
                from marc2bf.profiles.bfdr import profile
                self._profile = profile
            elif use_profile == "lc":
                from marc2bf.profiles.lc import profile
                self._profile = profile
            else:
                raise
        else:
            # Assume profile object
            self._profile = use_profile
        return None