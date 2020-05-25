class Conditions:

    def always(
        self,
        field: object = {}
    ) -> int:
        return True

    def no_dollar_t(
        self,
        field: object = {}
    ) -> int:
        if "subfields" in field and "t" in field["subfields"]:
            return False
        return True
    