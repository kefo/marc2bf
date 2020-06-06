Issues with conversion; Items to look for
==========================

1) No clear way to provide a default value in the absence of an existing field.
For example, LC conversion says of no 003 value, default to DLC.  This is reasonable.
But if the record has no 003, then there is no way to do this presently.  Is this 
a common desire or a one-, two-off situation?

2) 010/z is repeatable and, as such, should produce multiple Identifier resources.
It is no clear how to output multiple resources based on a repeating subfield value.
Is this a common issue or a one-, two-off situation?