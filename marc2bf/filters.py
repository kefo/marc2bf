from rdflib import BNode

class Filters:

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
        self
    ) -> str:
        bnode = BNode()
        return bnode.n3()
        
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
        

    def join(
        self,
        data: list = [],
        separator: str = " "
    ) -> str:
        return separator.join(data)
        
    def prepend(
        self,
        data: list = [],
        prependstr: str = ""
    ) -> str:
        if not isinstance(data, list):
            data = [data]
        newdata = [ prependstr + d for d in data ]
        return newdata

    def last(
        self,
        data: list = []
    ) -> str:
        if len(data) == 1:
            return data
        else:
            return data[:-1]