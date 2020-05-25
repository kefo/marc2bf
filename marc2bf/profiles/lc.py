from marc2bf.patterns import Patterns
from marc2bf.filters import Filters

patterns = Patterns()
filters = Filters()
profile = [
    {
        "resourcetype": "bf:AdminMetadata",
        "seturi": [(filters.bnode, )],
        'uriref': "%AM1%",
        "condition": "always",
        "properties": [
            {
                "field": "005",
                "property": "bf:changeDate",
                "pattern": (patterns.literal, { "datatype": "xsd:dateTime", "data": (filters.f005date, ['[:14]']) })
            },
            {
                "field": "008",
                "property": "bf:creationDate",
                "pattern": (patterns.literal, { "datatype": "xsd:date", "data": (filters.f008date, ['[:6]']) })
            },
            {
                "field": "040",
                "property": "bf:source",
                "pattern": (patterns.object_simple, { "objtypes": ["bf:Source", "bf:Agent"], "valuesprop": "rdfs:label", "data": (None, ['a']) })
            },
            {
                "field": "leader",
                "property": "bfdr:resourceStatus",
                "pattern": (patterns.uri, { "data": [(None, ['value=n']), (filters.appenduri, 'http://id.loc.gov/vocabulary/resourceStatus/')] })
            },
            # Having two sources does not make it clear which was responsible for its creation and which for modification.
            {
                "field": "040",
                "property": "bf:source",
                "pattern": (patterns.object_simple, { "objtypes": ["bf:Source", "bf:Agent"], "valuesprop": "rdfs:label", "data": (filters.last, ['d']) })
            },
        ]
    },
    {
        "resourcetype": "bf:Instance",
        "condition": "always",
        "properties": [
            {
                "field": "010",
                "property": "bf:identifiedBy",
                "pattern": (patterns.object_simple, { "objtypes": ["bf:Lccn"], "valuesprop": "rdf:value", "data": (None, ['a']) })
            },
            {
                "field": "260",
                "property": "bf:provisionActivityStatement",
                "pattern": (patterns.literal, { "data": (filters.join, ['a', 'b', 'c']) })
            },
            {
                "field": "260",
                "property": "bf:provisionActivity",
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:ProvisionActivity"],
                        "props": {
                            "bf:place": (patterns.object_simple, { "objtypes": ["bf:Place"], "valuesprop": "rdfs:label", "data": (None, ['a']) }),
                            "bf:agent": (patterns.object_simple, { "objtypes": ["bf:Agent"], "valuesprop": "rdfs:label", "data": (None, ['b']) }),
                            "bf:date": (patterns.literal, { "data": (None, ['c']) })
                        }
                    }
                )
            },
            {
                "field": "300",
                "property": "bf:dimensions",
                "pattern": (patterns.literal, { "data": (None, ['a']) })
            },
            {
                "field": "490",
                "property": "bf:seriesStatement",
                "pattern": (patterns.literal, { "data": (None, ['a']) })
            },
        ]
    },
    {
        "resourcetype": "bf:Work",
        "condition": "always",
        "properties": [
            {
                "field": "010",
                "subfields": ["a"],
                "property": "bf:identifiedBy",
                "pattern": (patterns.object_simple, { "objtypes": ["bf:Lccn"], "valuesprop": "rdf:value", "data": (None, ['a']) })
            },
            {
                "field": "001", # Using 001 here is a bit of a hack.  We need to pick a field in the MARC record.  All will have this one.  Could have chosen leader.
                "property": "bf:adminMetadata",
                "pattern": (patterns.uri, { "data": [(None, ['%AM1%'])] })
            },
        ]
    }
]