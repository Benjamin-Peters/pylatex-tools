# pylatex-tools

This library contains a few useful Python tools to work with latex (overleaf).

## Table of contents

[create_new_bibliography](#create_new_bibliography)

[count_words](#count_words)

[count_citations](#count_citations)

[detex](#detex)

[get_citations_in_tex](#get_citations_in_tex)

[strip_comments_in_tex](#strip_comments_in_tex)


## functions

### <a name="create_new_bibliography"></a> create_new_bibliography

Creates a new bibliography specific to your tex document. Extracts all citation keys that have been used in a tex document. Then, writes a new bibliography that only contains the cited entries.

Example usage:
```
python .\pylatextools\create_new_bibliography.py .\example\main.tex .\example\references.bib
```

Writes new file "out.bib" that only contains the cited references.


To remove unncessary fields (that often mess up the bibliography):
```
python .\pylatextools\create_new_bibliography.py .\example\main.tex .\example\references.bib --remove_fields file abstract day month keywords urldate language iss note isbn
```

### <a name="count_words"></a> count_words

Creates a word count overview for a (single) tex document for each section, subsection, etc.

Example usage:
```
python .\pylatextools\count_words.py .\example\main.tex
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

### <a name="count_citations"></a> count_citations

Counts the number of references in a document, how often they are cited, and allows to filter for specific authors/keywords.

Example usage:
```
python .\pylatextools\count_citations.py .\example\main.tex
```

Returns:
```
--------------------------------------------------

citation_key: # occurences

laemmli_1970_cleavage: 2
einstein_1935_can: 1

A total of 3 citations found, 2 unique.

--------------------------------------------------

# occurences:# references
2:1
1:1

--------------------------------------------------
```

We can specify the bibliography to make it prettier and search for specific authors:
```
python .\pylatextools\count_citations.py .\example\main.tex -b .\example\references.bib -p albert
```
Returns:
```
--------------------------------------------------

citation_key: # occurences -- reference

einstein_1935_can: 1 -- Einstein, Albert Podolsky, Boris Rosen, Nathan (1935) Can quantum-mechanical description of physical reality be considered complete?

A total of 1 citations found, 1 unique.

--------------------------------------------------

# occurences:# references
1:1

--------------------------------------------------
```

### <a name="detex"></a> detex

Creates a text-only version of a tex document (uses a lot of code from [here](http://www.gilles-bertrand.com/2012/11/a-simple-detex-function-in-python.html))

Example usage:
```
python .\pylatextools\detex.py .\example\main.tex
```

Prints text stripped of all tex commands and writes to file (optionally).

### <a name="get_citations_in_tex"></a> get_citations_in_tex
Returns all citation keys used in the tex document

### <a name="strip_comments_in_tex"></a> strip_comments_in_tex
Removes all comments from the tex document
