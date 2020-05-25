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
                "field": "008",
                "property": "bf:creationDate",
                "pattern": (patterns.literal, { "datatype": "xsd:date", "data": (filters.f008date, ['[:6]']) })
            },
            {
                "field": "040",
                "subfields": ["a"],
                "property": "bf:source",
                "pattern": (patterns.object_simple, { "objtypes": ["bf:Source", "bf:Agent"], "valuesprop": "rdfs:label", "data": (None, ['a']) })
            },
            {
                "field": "leader",
                "property": "bfdr:resourceStatus",
                "pattern": (patterns.uri, { "data": [(None, ['value=n']), (filters.appenduri, 'http://id.loc.gov/vocabulary/resourceStatus/')] })
            },
        ]
    },
    {
        "resourcetype": "bf:AdminMetadata",
        "seturi": [(filters.bnode, )],
        'uriref': "%AM2%",
        "condition": "always",
        "properties": [
            {
                "field": "005",
                "property": "bf:changeDate",
                "pattern": (patterns.literal, { "datatype": "xsd:dateTime", "data": (filters.f005date, ['[:14]']) })
            },
            {
                "field": "040",
                "property": "bf:source",
                "pattern": (patterns.uri, { "data": [(filters.last, ['d']), (filters.appenduri, 'http://id.loc.gov/vocabulary/organizations/')] })
            },
        ]
    },
    {
        "resourcetype": "bf:Instance",
        "condition": "always",
        "properties": [
            {
                "field": "010",
                "subfields": ["a"],
                "property": "bf:identifiedBy",
                "pattern": (patterns.object_simple, { "objtypes": ["bf:Lccn"], "valuesprop": "rdf:value", "data": (None, ['a']) })
            },
            {
                "field": "260",
                "subfields": ["c"],
                "property": "bf:provisionActivityStatement",
                "pattern": (patterns.literal, { "data": (filters.join, ['a', 'b', 'c']) })
            },
            {
                "field": "300",
                "subfields": ["c"],
                "property": "bf:dimensions",
                "pattern": (patterns.literal, { "data": (None, ['a']) })
            },
            {
                "field": "001", # Using 001 here is a bit of a hack.  We need to pick a field in the MARC record.  All will have this one.  Could have chosen leader.
                "property": "bf:adminMetadata",
                "pattern": (patterns.uri, { "data": [(None, ['%AM1%', '%AM2%'])] })
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
                "field": "001",
                "property": "bf:adminMetadata",
                "pattern": (patterns.uri, { "data": [(None, ['%AM1%', '%AM2%'])] })
            },
        ]
    }
]