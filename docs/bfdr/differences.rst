`bfdr` Compared to LC Conversion Specifications 
==========================

`bfdr` departs from the LC Conversion Specifications in the following 
specific ways.  For a description of more general, philosophical differences,
 see XXXXXX.

MARC Bib 001 & 003
-------------
LC Spec: Work/adminMetadata/AdminMetdata/identifiedBy/Local/rdf:value
bfdr: Instance/adminMetadata/AdminMetadata/identifiedBy/Local/rdf:value
Reasoning: Each MARC Bib record represents at least one Instance.  
The Local SYSTEM Identifier is therefore associated with the Instance's, not the 
Work's administrative metadata.

LC Spec for the 003 indicates to use Org URI for LC and Agent/code for all
other libraries.  `bfdr` appends the code found in 003 to the MARC Org URI pattern, 
rightly or wrongly.  LC Spec says to use DLC if 003 is empty.  Current 003="" isn't
handled at present.

001s are system numbers.  Control numbers, such as 010 and 016, though they
can be used as system numbers, are associated with the Instance directly.


MARC Bib 005
-------------
If 005 date is all zeros, LC SPec says "do not convert."   Do not understand this 
condition.  `bfdr` will skip the date but continue to convert the record.  Don't
feed it crap.


MARC Bib 006
-------------
Initial thoughts:  Need a few examples of where/how 006 used.  On the surface 006 appears
to be used only in cases when there are additional resources.  This has important
modelling ramifications potentially.  For example, if an 006 represents something else
do you create another Work + Instance or just another Instance?

MARC Bib 007
-------------
For Text (007/00=t), LC Spec says 'nac,' which I suppose means "not attempt to convert?" 
This is probably fine, but perhaps it's just easy to do?  Need example.


MARC Bib 010, 016
-------------
These identifiers are placed on both the Instance.  These identifiers are important 
in a MARC environment but their purpose in a BF environment is unclear.


MARC Bib 015
-------------
This identifier is on both Work and Instance.
