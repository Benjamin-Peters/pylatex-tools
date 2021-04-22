# pylatex-tools

This library contains a few useful tools to work latex.

I wrote these functions because I am more versatile with Python and I am using overleaf - which does not have always have the flexibility one might need.

**functions**

- create_new_bibilography: extracts from a tex document all citation keys that have been used. then, writes a new bibliography that only contains the cited entries.
- get_citations_in_tex: returns all citation keys used in the tex document
- strip_comments_in_tex: removes all comments from the tex document
- detex: creates a text-only version of a tex document (uses a lot of code from [here](http://www.gilles-bertrand.com/2012/11/a-simple-detex-function-in-python.html))
- count_words: creates a word count overview for a (single) tex document for each section, subsection, etc.

count_words.py, create_new_bibliography.py, detex.py work as standalone
