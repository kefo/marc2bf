`bfdr` Compared to LC Conversion Specifications 
==========================

`bfdr` departs from the LC Conversion Specifications in the following 
specific ways.  For a description of more general, philosophical differences,
 see XXXXXX.

MARC Bib 001 & 003
-------------
LC Spec: Work/adminMetadata/AdminMetdata/identifiedBy/Local/rdf:value
bfdr: Instance/identifiedBy/Local/rdf:value
Reasoning: Each MARC Bib record represents at least one Instance.  
The Local Identifier is therefore associated with the Instance, not the Work's 
administrative metadata.

LC Spec for the 003 indicates to use Org URI for LC and Agent/code for all
other libraries.  `bfdr` appends the code found in 003 to the MARC Org URI pattern, 
rightly or wrongly.

