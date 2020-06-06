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
            r = {}
            r["leader"] = [rdict["leader"]]
            
            r["leader"] = []
            leader = {
                "tag": "leader",
                "content": rdict["leader"]
            }
            r["leader"].append(leader)
            
            for f in rdict["fields"]:
                for k in f:
                    if int(k) < 10:
                        field = {}
                        field["content"] = f[k]
                    else:
                        field = f[k]
                    field["tag"] = k
                    if k in r:
                        r[k].append(field)
                    else:
                        r[k] = [field]
            # print(r)
            for profile in self._profile:
                if 'conditions' in profile:
                    # Conditions at the profile level must look at entire marc record
                    conditionfn = profile["conditions"]
                    to_continue = conditionfn(r)
                    if not to_continue:
                        continue
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
                    if not isinstance(i["field"], list):
                        i["field"] = [i["field"]]
                    for ifield in i["field"]:
                        field = ifield
                        if field in r:
                            prop = i["property"]
                            fn = i["pattern"][0]
                            # params = deepcopy(i["pattern"][1])
                            for f in r[field]:
                                params = deepcopy(i["pattern"][1])
                                if 'conditions' in i:
                                    if not isinstance(i["conditions"], list):
                                        i["conditions"] = [i["conditions"]]
                                    # Conditions at the profile level must look at entire marc record
                                    continue_on = True
                                    for condition in i["conditions"]:
                                        conditionfn = condition[0]
                                        if len(condition) == 2:
                                            conditiondata = condition[1]
                                            to_continue = conditionfn(r, f, conditiondata)
                                        else:
                                            to_continue = conditionfn(r, f)
                                        # to_continue = conditionfn(r, f, conditiondata)
                                        if not to_continue:
                                            continue_on = False
                                    if not continue_on:
                                        continue;
                                if "data" in params:
                                    params["data"] = self._handle_data(f, params["data"])
                                if "props" in params:
                                    params["props"] = self._handle_props(r, f, params["props"])
                                if "uri" in params:
                                    params["uri"] = self._handle_uri(f, params["uri"])
                                    if 'uriref' in params and params["uri"][0] != "":
                                        self._urirefs[params["uriref"]] = params["uri"]
                                        del params["uriref"]
                                objectdata = fn(**params)
                                if prop not in resource:
                                    resource[prop] = []
                                resource[prop].append(objectdata)
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
    
    
    def _handle_data(
        self,
        field,
        data
    ) -> list:
        if not isinstance(data, list):
            data = [data]
        primarydata = data[0]
        datafn = primarydata[0]
        datafields = []
        for df in primarydata[1]:
            if '=' in df:
                datafields.append(df.split("=")[1])
            elif ':' in df:
                datafields.append(eval('field["content"]' + df))
            elif df == "ind1" or df == "ind2" or df == "tag":
               datafields.append(field[df])
            elif df.startswith('%') and df.endswith("%"):
                if df in self._urirefs:
                    datafields.append(self._urirefs[df])
            elif "subfields" in field:
                for sf in field["subfields"]:
                    key = list(sf.keys())[0]
                    if df == key:
                        datafields.append(sf[key])
        if datafn != None:
            # print(datafn)
            fielddata = datafn(datafields)
            if not isinstance(fielddata, list):
                fielddata = [fielddata]
        else:
            fielddata = datafields
        if len(data) > 1:
            for additionaldata in data[1:]:
                additionaldatafn = additionaldata[0]
                if len(additionaldata) == 2:
                    additionaldataparams = additionaldata[1]
                    fielddata = additionaldatafn(fielddata, additionaldataparams)
                else:
                    fielddata = additionaldatafn(fielddata)
                if not isinstance(fielddata, list):
                    fielddata = [fielddata]
        return fielddata
        
    def _handle_props(
        self,
        record,
        field,
        props
    ) -> object:
        subresource = {}
        for k in props:
            # k is the subresource property
            # kfn sub resource property function, will create a literal or object
            kfn = props[k][0]
            # This is the variables/parameters, one of which will be data
            kparams = props[k][1]
            if "fieldref" in kparams:
                if kparams["fieldref"] in record:
                    for tempfield in record[kparams["fieldref"]]:
                        kparams["data"] = self._handle_data(tempfield, kparams["data"])
                else:
                    kparams["data"] = ""
                del kparams["fieldref"]
            elif "data" in kparams:
                kparams["data"] = self._handle_data(field, kparams["data"])
            
            if "props" in kparams:
                kparams["props"] = self._handle_props(record, field, kparams["props"])
            if "uri" in kparams:
                kparams["uri"] = self._handle_uri(field, kparams["uri"])

            subresourcedata = kfn(**kparams)
            subresource[k] = subresourcedata
        return subresource

    def _handle_uri(
        self,
        field,
        uridata
    ) -> list:
        if not isinstance(uridata, list):
            uridata = [uridata]
        
        urid = uridata[0]
        uridatafn = urid[0]
        uridatavals = urid[1]
        datafields = []
        for v in uridatavals:
            if ':' in v:
                datafields.append(eval('field' + v))
            elif v == "ind1" or v == "ind2":
               datafields.append(field[v])
            elif "subfields" in field:
                for sf in field["subfields"]:
                    key = list(sf.keys())[0]
                    if v == key:
                        datafields.append(sf[key])
            elif '=' in v:
                datafields.append(v.split("=")[1])
            elif v.startswith('%') and v.endswith("%"):
                if v in self._urirefs:
                    datafields.append(self._urirefs[v])
        if uridatafn != None:
            fielddata = uridatafn(datafields)
            if not isinstance(fielddata, list):
                fielddata = [fielddata]
        else:
            fielddata = datafields
        if len(uridata) > 1:
            for additionaldata in uridata[1:]:
                additionaldatafn = additionaldata[0]
                additionaldataparams = additionaldata[1]
                fielddata = additionaldatafn(fielddata, additionaldataparams)
                if not isinstance(fielddata, list):
                    fielddata = [fielddata]
        if len(fielddata) > 0:
            return fielddata[0]
        else:
            return ''
                            
        