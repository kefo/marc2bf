import re

class Patterns:

    def literal(
        self,
        data: list = [],
        datatype: str = ""
    ) -> object:
        '''
        "bflc:subjectOf": [ "str1", "str2" ]
        '''
        returndata = []
        if datatype != "":
            for d in data:
                returndata.append( {"@type": datatype, "@value": d} )
        else:
            returndata = data
        return returndata
        
    def object_simple(self,
        uri: str = "",
        objtypes: list = [],
        valuesprop: str = '',
        data: list = [],
        datatype: str = ""
    ) -> object:
        '''
        {
      "@id": "http://id.loc.gov/authorities/subjects/sh99001237",
      "@type": [
        "madsrdf:GenreForm",
        "madsrdf:Authority"
      ],
      "madsrdf:authoritativeLabel": {
        "@language": "en",
        "@value": "Biography"
      },
        '''
        obj = {}
        if uri != "":
            obj["@id"] = uri
        if len(objtypes) == 1:
            objtypes = objtypes[0]
        obj["@type"] = objtypes
        if len(data) == 1:
            data = data[0]
        obj[valuesprop] = data
        return obj
        
    def object_complex(self,
        uri: str = "",
        objtypes: list = [],
        props: object = {}
    ) -> object:
        '''
        {
      "@id": "http://id.loc.gov/authorities/subjects/sh99001237",
      "@type": [
        "madsrdf:GenreForm",
        "madsrdf:Authority"
      ],
      "madsrdf:authoritativeLabel": {
        "@language": "en",
        "@value": "Biography"
      },
        '''
        obj = {}
        if uri != "":
            obj["@id"] = uri
        if len(objtypes) == 1:
            objtypes = objtypes[0]
        obj["@type"] = objtypes
        for k in props:
            prop_k = k
            re_pattern = '_[0-9]$'
            instr = re.search(re_pattern, k)
            if(instr != None):
                # Ends with _number
                prop_k = re.sub(re_pattern, '', prop_k)
            if prop_k not in obj:
                obj[prop_k] = props[k]
            else:
                obj[prop_k] += props[k]
        print("obj is")
        print(obj)
        return obj

    def uri(
        self,
        data: list = []
    ) -> object:
        '''
        "bflc:subjectOf": [
            {
              "@id": "http://id.loc.gov/resources/works/5170453"
            },
        ]
        '''
        returndata = []
        for d in data:
            if d !=  "" and d != None:
                returndata.append( {"@id": d} )
        return returndata
        
        
    # NOTHING USED BELOW HERE?????
    def property_uri(
        self,
        prop: str = '',
        data: list = []
    ) -> object:
        '''
        "bflc:subjectOf": [
            {
              "@id": "http://id.loc.gov/resources/works/5170453"
            },
        ]
        '''
        ids = []
        for u in data:
            o = { "@id": u }
            ids.append(o)
            
        obj = {
            prop: ids
        }
        
        return obj
        
    def property_literals(
        self,
        prop: str = '',
        data: list = [],
        datatype: str = ""
    ) -> object:
        '''
        "bflc:subjectOf": [ "str1", "str2" ]
        '''
        if len(data) == 1:
            data = data[0]
        obj = {
            prop: data
        }
        
        return obj

    def property_object_value(
        self,
        prop: str = '',
        objtypes: list = [],
        valuesprop: str = '',
        data: list = [],
        datatype: str = ""
    ) -> object:
        '''
        "bf:prop": [{
      "@id": "http://id.loc.gov/authorities/subjects/sh99001237",
      "@type": [
        "madsrdf:GenreForm",
        "madsrdf:Authority"
      ],
      "madsrdf:authoritativeLabel": {
        "@language": "en",
        "@value": "Biography"
      },
        '''
        if len(literals) == 1:
            data = data[0]
        obj = {
            prop: data
        }
        
        return obj