from marc2bf.patterns import Patterns
from marc2bf.filters import Filters
from marc2bf.conditions import Conditions
from marc2bf.mappings import mappings

patterns = Patterns()
filters = Filters()
conditions = Conditions()
profile = [
    {
        "resourcetype": "bf:AdminMetadata",
        "seturi": [(filters.bnode, )],
        'uriref': "%AM1%",
        "condition": conditions.always,
        "properties": [
            {
                "field": "008",
                "property": "bf:creationDate",
                "pattern": (patterns.literal, { "datatype": "xsd:date", "data": (filters.f008date, ['[:6]']) })
            },
            {
                "field": "040",
                "property": "bf:source",
                "pattern": (patterns.uri, { "data": [(None, ['a']), (filters.appenduri, 'http://id.loc.gov/vocabulary/organizations/')] })
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
        "condition": conditions.always,
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
            {
                "field": "leader",
                "property": "bfdr:resourceStatus",
                "pattern": (patterns.uri, { "data": [(None, ['[5:6]']), (filters.appenduri, 'http://id.loc.gov/vocabulary/resourceStatus/')] })
            },
        ]
    },
    {
        "resourcetype": "bf:AdminMetadata",
        "seturi": [(filters.bnode, )],
        'uriref': "%AM3%",
        "condition": conditions.always,
        "properties": [
            # This needs refinement.  If 003 is not present, then there is no organization associated with the local identifier.
            {
                "field": "001",
                "property": "bf:identifiedBy",
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Local"],
                        "props": {
                            "rdf:value": (patterns.literal, { "data": (None, ['[0:]']) }),
                            "bf:assigner": (patterns.uri, { "fieldref": "003", "data": [(filters.lower, ['[0:]']), (filters.appenduri, 'http://id.loc.gov/vocabulary/organizations/'), ] })
                        }
                    }
                )
            },
        ]
    },
    {
        "resourcetype": "bf:Instance",
        "condition": conditions.always,
        "properties": [
            {
                # This should be fine because 'a' is NR.  Of course there's bound to be a record where this is violated, but ....
                "field": ["010", "020", "025"],
                "property": "bf:identifiedBy",
                "conditions": (conditions.exists, ['a', 'z']),
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": [(filters.no_parenthetical, ['a', 'z']), (filters.no_ending_punctuation, )] }),
                            "bf:qualifier": (patterns.literal, { "data": [(None, ['q'])] }),
                            "bf:qualifier_0": (patterns.literal, { "data": [(filters.extract_parenthetical, ['a', 'z'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                            "bf:source": (patterns.uri, { "data": [(filters.lower, ['2']), (filters.appenduri, 'http://id.loc.gov/vocabulary/organizations/'), ] }),
                        }
                    }
                ),
            },
            # This 015 is when a national bib scheme is identified in the $2
            {
                "field": "015",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a', 'z']), (conditions.exists, ['2']),],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "bf:source": (patterns.uri, { "data": [(filters.lower, ['2']), (filters.appenduri, 'http://id.loc.gov/vocabulary/nationalbibschemes/'), ] }),
                            "bf:qualifier": (patterns.literal, { "data": [(None, ['q'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            # This 015 is when there is no national bib scheme in $2 - will set as org running conversion.
            {
                "field": "015",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a', 'z']), (conditions.not_exists, ['2']),],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "bf:source": (patterns.uri, { "data": [(None, ['value=%ORGRESPONSIBLE%'])] }),
                            "bf:qualifier": (patterns.literal, { "data": [(None, ['q'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            # This 016 is for when the org code is identified in $2
            {
                "field": "016",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a']), (conditions.ind1_is, ['7']), (conditions.exists, ['2']),],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "bf:source": (patterns.uri, { "data": [(filters.lower, ['2']), (filters.appenduri, 'http://id.loc.gov/vocabulary/organizations/'), ] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            # This 016 is for when ind1 is blank, which is for the LAC.
            {
                "field": "016",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a']), (conditions.ind1_is, [' '])],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "bf:source": (patterns.uri, { "data": [(None, ['value=https://www.bac-lac.gc.ca/'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            {
                "field": "017",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a'])],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "rdfs:comment": (patterns.literal, { "data": [(None, ['i'])] }),
                            "bf:date": (patterns.literal, { "data": [(None, ['d'])] }),
                            "bf:source": (
                                patterns.object_complex, 
                                { 
                                    "objtypes": ["bf:Agent"],
                                    "uri": (filters.uri_or_bnode, {"data": (None, ['1'])}),
                                    "props": {
                                        "rdfs:label": (patterns.literal, { "data": (filters.join, ['b']) }),
                                    }
                                }
                            ),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            {
                "field": ["024"],
                "property": "bf:identifiedBy",
                "conditions": (conditions.exists, ['a', 'z']),
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_024_map, ['ind1']) }),
                            "rdf:type_0": (patterns.uri, { "data": [(filters.lower, ['2']), (filters.appenduri, 'http://id.loc.gov/vocabulary/identifiers/'), ] }),
                            "rdf:value": (patterns.literal, { "data": [(None, ['a', 'z'])] }),
                            "bf:qualifier": (patterns.literal, { "data": [(None, ['q'])] }),
                            "rdfs:comment": (patterns.literal, { "data": [(None, ['d'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            {
                "field": "260",
                "property": "bf:provisionActivityStatement",
                "pattern": (patterns.literal, { "data": (filters.join, ['a', 'b', 'c']) })
            },
            {
                "field": "300",
                "property": "bf:dimensions",
                "pattern": (patterns.literal, { "data": (None, ['a']) })
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
                "field": "490",
                "property": "bf:seriesStatement",
                "pattern": (patterns.literal, { "data": (None, ['a']) })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:carrier",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[23:24]']), (filters.f008Map, mappings["f008mappingsText"]["carrierMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:fontSize",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[23:24]']), (filters.f008Map, mappings["f008mappingsText"]["fontSizeMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:notation",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[23:24]']), (filters.f008Map, mappings["f008mappingsText"]["tactileMap"]), ] })
            },
            {
                "field": "001", # Using 001 here is a bit of a hack.  We need to pick a field in the MARC record.  All will have this one.  Could have chosen leader.
                "property": "bf:adminMetadata",
                "pattern": (patterns.uri, { "data": [(None, ['%AM1%', '%AM2%', '%AM3%'])] })
            },
        ]
    },
    {
        "resourcetype": "bf:Work",
        "condition": conditions.always,
        "properties": [
            {
                "field": "015",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a']), (conditions.exists, ['2']),],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "bf:source": (patterns.uri, { "data": [(filters.lower, ['2']), (filters.appenduri, 'http://id.loc.gov/vocabulary/nationalbibschemes/'), ] }),
                            "bf:qualifier": (patterns.literal, { "data": [(None, ['q'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            {
                "field": "015",
                "property": "bf:identifiedBy",
                "conditions": [(conditions.exists, ['a']), (conditions.not_exists, ['2']),],
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "props": {
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": (None, ['a']) }),
                            "bf:source": (patterns.uri, { "data": [(None, ['value=%ORGRESPONSIBLE%'])] }),
                            "bf:qualifier": (patterns.literal, { "data": [(None, ['q'])] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                        }
                    }
                ),
            },
            {
                # ISSNs active and cancelled.  Note two ways to do a URI.
                "field": ["022"],
                "property": "bf:identifiedBy",
                "conditions": (conditions.exists, ['a', 'z']),
                "foreach": [('a', {'omit': ['z']}), ('z', {'omit': ['a']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "uri": (None, ['0']),
                        "props": {
                            # "@id": (filters.uri_or_bnode, {"data": (None, ['0'])}),
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": [(filters.no_parenthetical, ['a', 'z']), (filters.no_ending_punctuation, )] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['z']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                            "bf:source": (
                                patterns.object_complex, 
                                { 
                                    "conditions": (conditions.exists, ['2']), 
                                    "objtypes": ["bf:Agent"],
                                    "uri": (filters.uri_or_bnode, {"data": (None, )}),
                                    "props": {
                                        "rdfs:label": (patterns.literal, { "data": (filters.no_parenthetical, ['2']) }),
                                    }
                                }
                            ),
                        }
                    }
                ),
            },
            {
                # ISSNs incorrect.  Note two ways to do a URI.
                "field": ["022"],
                "property": "bf:identifiedBy",
                "conditions": (conditions.exists, ['y']),
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier"],
                        "uri": (None, ['0']),
                        "props": {
                            # "@id": (filters.uri_or_bnode, {"data": (None, ['0'])}),
                            "rdf:type": (patterns.uri, { "data": (filters.identifier_field_map, ['tag']) }),
                            "rdf:value": (patterns.literal, { "data": [(filters.no_parenthetical, ['y']), (filters.no_ending_punctuation, )] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['y']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/incorrect'])] }),
                            "bf:source": (
                                patterns.object_complex, 
                                { 
                                    "conditions": (conditions.exists, ['2']), 
                                    "objtypes": ["bf:Agent"],
                                    "uri": (filters.uri_or_bnode, {"data": (None, )}),
                                    "props": {
                                        "rdfs:label": (patterns.literal, { "data": (filters.no_parenthetical, ['2']) }),
                                    }
                                }
                            ),
                        }
                    }
                ),
            },
            {
                # ISSN-Ls active and cancelled.  Note two ways to do a URI.
                "field": ["022"],
                "property": "bf:identifiedBy",
                "conditions": (conditions.exists, ['l', 'm']),
                "foreach": [('l', {'omit': ['m']}), ('m', {'omit': ['l']}),],
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Identifier", "identifiers:issn-l"],
                        "uri": (None, ['0']),
                        "props": {
                            # "@id": (filters.uri_or_bnode, {"data": (None, ['0'])}),
                            "rdf:value": (patterns.literal, { "data": [(filters.no_parenthetical, ['l', 'm']), (filters.no_ending_punctuation, )] }),
                            "bf:status": (patterns.uri, { "conditions": (conditions.exists, ['m']), "data": [(None, ['value=http://id.loc.gov/vocabulary/mstatus/cancinv'])] }),
                            "bf:source": (
                                patterns.object_complex, 
                                { 
                                    "conditions": (conditions.exists, ['2']), 
                                    "objtypes": ["bf:Agent"],
                                    "uri": (filters.uri_or_bnode, {"data": (None, )}),
                                    "props": {
                                        "rdfs:label": (patterns.literal, { "data": (filters.no_parenthetical, ['2']) }),
                                    }
                                }
                            ),
                        }
                    }
                ),
            },
            {
                "field": ["100", "110", "111"],
                "conditions": (conditions.no_dollar_t, ''),
                "property": "bf:contribution",
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Contribution",],
                        "uri": (filters.bnode, {}),
                        "uriref": "%CTB01%",
                        "props": {
                            "bf:agent": (
                                patterns.object_complex, 
                                { 
                                    "objtypes": ["bf:Agent"],
                                    "uri": (filters.uri_or_bnode, {"data": (None, ['1'])}),
                                    "props": {
                                        "rdfs:label": (patterns.literal, { "data": (filters.join, ['a', 'q', 'b', 'c', 'd']) }),
                                        "rdf:type": (patterns.uri, { "data": (filters.agentmap, ['tag']) }),
                                        "bf:isIdentifiedByAuthority": (patterns.uri, { "data": [(None, ['0'])] }),
                                    }
                                }
                            ),
                            #"bf:role": (
                            #    patterns.object_complex, 
                            #    { 
                            #        "objtypes": ["bf:Role"],
                            #        "uri": (filters.roles, { "data": (None, ['e','4'])}),
                            #        "props": {
                            #            "rdfs:label": (patterns.literal, { "data": (None, ['e']) })
                            #        }
                            #    }
                            #),
                            "bf:role": (patterns.uri, { "data": (filters.roles, ['e','4'])}),
                        }
                    }
                )
            },
            {
                "field": ["700", "710", "711"],
                "conditions": (conditions.no_dollar_t, ''),
                "property": "bf:contribution",
                "pattern": (
                    patterns.object_complex, 
                    { 
                        "objtypes": ["bf:Contribution",],
                        "props": {
                            "bf:agent": (
                                patterns.object_complex, 
                                { 
                                    "objtypes": ["bf:Agent"],
                                    "uri": (filters.uri_or_bnode, {"data": (None, ['1'])}),
                                    "props": {
                                        "rdfs:label": (patterns.literal, { "data": (filters.join, ['a', 'q', 'b', 'c', 'd']) }),
                                        "rdf:type": (patterns.uri, { "data": (filters.agentmap, ['tag']) }),
                                        "bf:isIdentifiedByAuthority": (patterns.uri, { "data": [(None, ['0'])] }),
                                    }
                                }
                            ),
                            #"bf:role": (
                            #    patterns.object_complex, 
                            #    { 
                            #        "objtypes": ["bf:Role"],
                            #        "uri": (filters.roles, { "data": (None, ['e','4'])}),
                            #        "props": {
                            #            "rdfs:label": (patterns.literal, { "data": (None, ['e']) })
                            #        }
                            #    }
                            #),
                            "bf:role": (patterns.uri, { "data": (filters.roles, ['e','4'])}),
                        }
                    }
                )
            },
            {
                "field": "100",
                "property": "bfdr:primaryContribution",
                "pattern": (patterns.uri, { "data": [(None, ["%CTB01%"])] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:illustrativeContent",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[18:19]', '[19:20]', '[20:21]', '[21:22]']), (filters.f008Map, mappings["f008mappingsText"]["illustrativeContentMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:intendedAudience",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[22:23]']), (filters.f008Map, mappings["f008mappingsText"]["intendedAudienceMap"]), ] })
            },
            {
                "field": "008",
                "property": "bf:language",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[35:38]']), (filters.appenduri, 'http://id.loc.gov/vocabulary/languages/')] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:supplementaryContent",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[23:24]', '[24:25]', '[25:26]', '[26:27]']), (filters.f008Map, mappings["f008mappingsText"]["supplementaryContentMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:genreForm",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[27:28]']), (filters.f008Map, mappings["f008mappingsText"]["govPubMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:genreForm",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[29:30]']), (filters.f008Map, mappings["f008mappingsText"]["festschriftMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:supplementaryContent",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[30:31]']), (filters.f008Map, mappings["f008mappingsText"]["indexMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:genreForm",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[32:33]']), (filters.f008Map, mappings["f008mappingsText"]["literaryFormMap"]), ] })
            },
            {
                "field": "008",
                "conditions": [(conditions.leader_06_equals, ['a', 't']), (conditions.leader_07_equals, ['a', 'c', 'd', 'm'])],
                "property": "bf:genreForm",
                "pattern": (patterns.uri, { "data": [(filters.iscoded, ['[33:34]']), (filters.f008Map, mappings["f008mappingsText"]["biographyMap"]), ] })
            },
            {
                "field": "001",
                "property": "bf:adminMetadata",
                "pattern": (patterns.uri, { "data": [(None, ['%AM1%', '%AM2%'])] })
            },
        ]
    }
]