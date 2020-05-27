from rdflib import BNode

class Filters:

    def agentmap(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        if data.endswith('00'):
            return "bf:Person"
        elif data.endswith('10'):
            return "bf:Organization"
        elif data.endswith('11'):
            return "bf:Meeting"
        return ""
    
    def appenduri(
        self,
        data: list = [],
        uribase: str = ""
    ) -> str:
        if not isinstance(data, list):
            data = [data]
        newdata = [ d.lower() for d in data ]
        return self.prepend(newdata, uribase)
        
    def bnode(
        self,
        data: str = ""
    ) -> str:
        bnode = BNode()
        return bnode.n3()
        
    def carrierMap(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        datamap = {
            "a": "http://id.loc.gov/vocabulary/mediaTypes/h",
            "b": "http://id.loc.gov/vocabulary/carriers/he",
            "c": "http://id.loc.gov/vocabulary/carriers/hg",
            "o": "http://id.loc.gov/vocabulary/carriers/cr",
            "q": "http://id.loc.gov/vocabulary/carriers/cz",
            "r": "http://id.loc.gov/vocabulary/carriers/nc",
            "s": "http://id.loc.gov/vocabulary/carriers/cz",
        }
        if data in datamap:
            return datamap[data]
        
    def f005date(
        self,
        data: list = []
    ) -> str:
        data = data[0]
        year = data[:4]
        month = data[4:6]
        day = data[6:8]
        hour = data[8:10]
        minutes = data[10:12]
        seconds = data[12:14]
        date = year + "-" + month + "-" + day + "T" + hour + ":" + minutes + ":" + seconds 
        return date
        
    
    def f008date(
        self,
        data: list = []
    ) -> str:
        data = data[0]
        year = data[:2]
        if int(year) > 65 and int(year) <= 99:
            year = "19" + year
        else:
            year = "20" + year
        month = data[2:4]
        day = data[4:6]
        date = year + "-" + month + "-" + day
        return date
        
    def fontSizeMap(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        datamap = {
            "d": "http://id.loc.gov/vocabulary/mfont/lp",  # 008, Text
        }
        if data in datamap:
            return datamap[data]

    def illustrativeContentMap(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        datamap = {
            "a": "ill",
            "b": "map",
            "c": "por",
            "d": "chr",
            "e": "pln",
            "f": "plt",
            "g": "mus",
            "h": "fac",
            "i": "coa",
            "j": "gnt",
            "k": "for",
            "l": "sam",
            "m": "pho",
            "o": "pht",
            "p": "ilm",
        }
        if data in datamap:
            return datamap[data]
            
    def intendedAudienceMap(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        datamap = {
            "a": "pre",
            "b": "pri",
            "c": "pad",
            "d": "ado",
            "e": "adu",
            "f": "spe",
            "g": "gen",
            "j": "juv",
        }
        if data in datamap:
            return datamap[data]

    def iscoded(
        self,
        data: list = []
    ) -> str:
        newdata = []
        for d in data:
            d = d.lower().strip()
            if d != "|" and d != "x" and d != "||" and d != "xx" and d != "|||" and d != "xxx" and d!= "":
                newdata.append(d)
        return newdata

    def join(
        self,
        data: list = [],
        separator: str = " "
    ) -> str:
        return separator.join(data)


    def last(
        self,
        data: list = []
    ) -> str:
        if len(data) == 1:
            return data
        else:
            return data[:-1]
            
    def prepend(
        self,
        data: list = [],
        prependstr: str = ""
    ) -> str:
        if not isinstance(data, list):
            data = [data]
        newdata = [ prependstr + d for d in data ]
        return newdata


    def roles(
        self,
        data: list = []
    ) -> str:
        returndata = []
        if len(data) == 0:
            returndata.append("http://id.loc.gov/vocabulary/relators/ctb")
        else:
            for d in data:
                if strlen(d) == '3':
                    returndata.append("http://id.loc.gov/vocabulary/relators/" + d.lower())
                else:
                    returndata.append(self.bnode())
        return returndata
        
    def tactileMap(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        datamap = {
            "f": "http://id.loc.gov/vocabulary/mtactile/brail",  # 008, Text
        }
        if data in datamap:
            return datamap[data]


    def uri_or_bnode(
        self,
        data: list = []
    ) -> str:
        if len(data) == 0:
            return self.bnode()
        else:
            return data[0]


    