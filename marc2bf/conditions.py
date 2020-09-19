class Conditions:

    def always(
        self,
        field: object = {}
    ) -> int:
        return True
        
    def leader_06_equals(
        self,
        record: object = {},
        field: object = {},
        data: object = {}
    ) -> int:
        if record["leader"][0]["content"][6:7] in data:
            return True
        return False

    def leader_07_equals(
        self,
        record: object = {},
        field: object = {},
        data: object = {}
    ) -> int:
        if record["leader"][0]["content"][7:8] in data:
            return True
        return False

    def no_dollar_t(
        self,
        record: object = {},
        field: object = {},
        data: object = {}
    ) -> int:
        if "subfields" in field and "t" in field["subfields"]:
            # dollar t exists, so no_dollar_t is false
            return False
        return True

    def exists(
        self,
        record: object = {},
        field: object = {},
        data: object = {}
    ) -> int:
        if "subfields" in field:
            for sf in field["subfields"]:
                key = list(sf.keys())[0]
                if key in data:
                    return True
        return False
        
    def not_exists(
        self,
        record: object = {},
        field: object = {},
        data: object = {}
    ) -> int:
        exists = False
        if "subfields" in field:
            for sf in field["subfields"]:
                key = list(sf.keys())[0]
                if key in data:
                    exists = True
        return not exists
        
    def ind1_is(
        self,
        record: object = {},
        field: object = {},
        data: object = {}
    ) -> int:
        if "ind1" in field:
            if field["ind1"] in data:
                return True
        return False