import re 
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

    def extract_parenthetical(
        self,
        data: str = ''
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        if len(data) == 0:
            return ""
        elif '(' not in data:
            return ""
        else:
            return data[data.find('(')+1:data.find(')')].strip()

    def f005date(
        self,
        data: list = []
    ) -> str:
        data = data[0]
        if int(data) == 0:
            return ""
            
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
        
    def f008Map(
        self,
        data: str = "",
        datamap: object = {}
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        if data in datamap:
            return datamap[data]
            
    def identifier_field_map(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        if data == '010':
            return "identifiers:lccn"
        elif data == '015':
            return "bf:Nbn"
        elif data == '016':
            return "bf:Local"
        elif data == '017':
            return "bf:CopyrightNumber"
        elif data == '020':
            return "identifiers:isbn"
        elif data == '022':
            return "identifiers:issn"
        elif data == '025':
            return "bf:LcOverseasAcq"
        return ""

    def identifier_024_map(
        self,
        data: str = ""
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        if data == '0':
            return "identifiers:isrc"
        elif data == '1':
            return "identifiers:upc"
        elif data == '2':
            return "identifiers:ismn"
        elif data == '3':
            return "identifiers:ean"
        elif data == '4':
            return "identifiers:sici"
        return ""

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
            
    def lower(
        self,
        data: list = []
    ) -> str:
        newdata = []
        for d in data:
            d = d.lower().strip()
            newdata.append(d)
        return newdata

    def no_ending_punctuation(
        self,
        data: str = ''
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        data = data.strip()
        
        re_pattern = '[\.;:]$'
        instr = re.search(re_pattern, data)
        if instr != None:
            return re.sub(re_pattern, '', data)
        else:
            return data

    def no_parenthetical(
        self,
        data: str = ''
    ) -> str:
        if isinstance(data, list):
            if len(data) == 0:
                return ""
            else:
                data = data[0]
        data = data.strip()
        if '(' not in data:
            return data
        else:
            return data[0:data.find('(')].strip()
            
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


    def uri_or_bnode(
        self,
        data: list = []
    ) -> str:
        if len(data) == 0:
            return self.bnode()
        else:
            return data[0]


    