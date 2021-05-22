# pylatex-tools

This library contains a few useful Python tools to work with latex (overleaf). It requires that the text is in a single tex file (it cannot intepret tex commands like input).

## Table of contents

[Run from console](#run_from_console)
 - [count_words](#count_words)
 - [create_new_bibliography](#create_new_bibliography)
 - [count_citations](#count_citations)
 - [detex](#detex)

[Python](#python)

## <a name="run_from_console"></a> Run from console

### <a name="count_words"></a> `count_words`

Creates a word count overview for a (single) tex document for each section, subsection, etc.

Example usage:
```bash
python pylatex-tools.py count_words example\main.tex
```

Returns count to console.
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

When specifying the `--ignore_via_tc_ignore` flag, all text between the line `%TC:ignore` and a subsequent line `%TC:endignore` is ignored.

```bash
python pylatex-tools.py count_words example\main.tex --ignore_via_tc_ignore
```
Returns (The "First subsubsection" is enclosed by `%TC:ignore` and `%TC:endignore` in the example.tex).

```
COUNTING WORDS IN EXAMPLE\MAIN.TEX


WORD COUNT FOR FILE EXAMPLE\MAIN.TEX


  **word count from heading to next heading (e.g., from section heading to next heading, which could be subsection)**

    535            Introduction
      169            First subsection
    237            Finally


  **word count for each subpart (e.g., all words in a section)**

    704            Introduction
      169            First subsection
    237            Finally


941 in total words when summed across the section count
```

 Writes to two csv files.
 ```bash
python pylatex-tools.py count_words example\main.tex --write_csv_output
```

### <a name="create_new_bibliography"></a> `create_new_bibliography`

Creates a new bibliography specific to your tex document. Extracts all citation keys that have been used in a tex document. Then, writes a new bibliography that only contains the cited entries.

Example usage:

```bash
python pylatex-tools.py create_new_bibliography example\main.tex --bibliography example\references.bib --out_filename out.bib
```

Specify `remove_fields` flag to specify which fields should not be included in the new bibliography.
```bash
python pylatex-tools.py create_new_bibliography example\main.tex --bibliography example\references.bib --out_filename out.bib --remove_fields file abstract note
```

The flag `--remove_fields most` removes fields 'file', 'abstract', 'day', 'month', 'keywords', 'urldate', 'language', 'iss', 'note', 'isbn'
```bash
python pylatex-tools.py create_new_bibliography example\main.tex --bibliography example\references.bib --out_filename out.bib --remove_fields most
```

Writes new file "out.bib" that only contains the cited references.


### <a name="count_citations"></a> `count_citations`

Counts the number of references in a document, how often they are cited, and allows to filter for specific authors/keywords.

Example usage:
```bash
python pylatex-tools.py count_citations example\main.tex
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

We can search for a specific `--citation_key`

```bash
python pylatex-tools.py count_citations example\main.tex --citation_keys einstein_1935_can
```

We can specify the `--bibliography` to make it prettier and search for specific authors via `--pattern_match_in_bibliography`:
```bash
python pylatex-tools.py count_citations example\main.tex --pattern_match_in_bibliography proteins --bibliography example\references.bib
```

Returns:
```
COUNTING CITATIONS IN EXAMPLE\MAIN.TEX
reading the bib file

--------------------------------------------------

citation_key: # occurences -- reference

laemmli_1970_cleavage: 2 -- Laemmli, Ulrich K (1970) Cleavage of structural proteins during the assembly of the head of bacteriophage T4

A total of 2 citations found, 1 unique.

--------------------------------------------------

# occurences:# references
2:1

--------------------------------------------------
```

### <a name="detex"></a> `detex`

Creates a text-only version of a tex document (uses a lot of code from [here](http://www.gilles-bertrand.com/2012/11/a-simple-detex-function-in-python.html))

Example usage:
```bash
python pylatex-tools.py detex example\main.tex
```

Write to `--out_filename`
```bash
python pylatex-tools.py detex example\main.tex --out_filename detexed.txt
```


## <a name="python"></a> Python

```python
import pylatex_tools as pl

# count words
pl.count_words('example\main.tex')

# create new bibliography
pl.create_new_bibliography('example\main.tex', 'example\references.bib')

# count citations
pl.count_citations('example\main.tex')

# detex
tex_string = pl.get_tex_string_from_file('example\main.tex')
pl.detex(tex_string)
```

