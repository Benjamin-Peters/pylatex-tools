# pylatex-tools

This library contains a few useful Python tools to work with latex.

I wrote these functions because I am more versatile with Python and I am using overleaf - which does not always have the flexibility one might need.

## functions

- **create_new_bibilography**: extracts all citation keys that have been used in a tex document. then, writes a new bibliography that only contains the cited entries.

example usage:
```
python .\latex_tools\create_new_bibliography.py .\example\main.tex .\example\references.bib
```

writes new file "out.bib" that only contains the cited references

- **detex**: creates a text-only version of a tex document (uses a lot of code from [here](http://www.gilles-bertrand.com/2012/11/a-simple-detex-function-in-python.html))

example usage:
```
python .\latex_tools\detex.py .\example\main.tex
```

Prints text stripped of all tex commands and writes to file (optionally).

- **count_words**: creates a word count overview for a (single) tex document for each section, subsection, etc.

example usage:
```
python .\latex_tools\count_words.py .\example\main.tex
```

Returns count to console and writes csv files (optionally).
```
WORD COUNT FOR FILE MAIN.TEX


  **word count from heading to next heading (e.g., from section heading to next heading, which could be subsection)**

    535            Introduction
      169            First subsection
        66            First subsubsection
    237            Finally


  **word count for each subpart (e.g., all words in a section)**

    770            Introduction
      235            First subsection
        66            First subsubsection
    237            Finally

1007 in total words when summed across the section count
```

Other helpful functions:

- **get_citations_in_tex**: returns all citation keys used in the tex document
- **strip_comments_in_tex**: removes all comments from the tex document
