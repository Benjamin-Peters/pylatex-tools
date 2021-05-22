# %%
import re

from pybtex.database import parse_file # type: ignore
from pybtex.database import BibliographyData # type: ignore

def load_file_as_list(filename: str) -> list[str]:
    textfile = open(filename, 'r', encoding="utf8")
    lines = []
    for line in textfile:
        lines.append(line)
    textfile.close()
    return lines

def strip_comments_in_tex(tex_lines: list[str]) -> list[str]:
    """strips comments (%) from list of tex lines

    Args:
        tex_lines (list): list of strings with tex code

    Returns:
        list: same list where everything after a % is removed
    """
    for i, line in enumerate(tex_lines):
        p = line.find('%')
        if p >= 0:
            tex_lines[i] = line[:p]
    return tex_lines

def strip_tc_ignore(lines: list[str]) -> list[str]:
    """removes lines that are between lines "%TC:ignore" and %TC:endignore"
    
        this is used in overleafs word count to ignore text 
        https://de.overleaf.com/learn/how-to/Is_there_a_way_to_run_a_word_count_that_doesn't_include_LaTeX_commands%3F

    Returns:
        list: list of lines with ignored lines removed
    """
    new_lines = []
    ignore_next_line = False
    for l in lines:
        p = l.find('%TC:ignore')
        if p >=0:
            ignore_next_line = True

        if not ignore_next_line:
            new_lines.append(l)

        p = l.find('%TC:endignore')
        if p >=0:
            ignore_next_line = False                  
    
    return new_lines
    
def get_citations_in_tex(tex_lines: list[str], cite_commands:list[str] = ['autocite', 'cite'], unique_set: bool = True) -> list[str]: 
    """returns list of cite keys being used in a list of tex strings 

    Args:
        tex_string (list): list of strings with tex code
        cite_commands (list, optional): keywords commands in the tex document. Defaults to ['autocite', 'cite'].

    Returns:
        list: list of citation keys (strings)
    """
    cite_keys: list[str] = []
    for line in tex_lines:
        for cc in cite_commands:
            # https://stackoverflow.com/questions/57064771/extract-cited-bibtex-keys-from-tex-file-using-regex-in-python
            rx = re.compile(r'''(?<!\\)%.+|(\\(?:no)?''' + cc +  r'''?[\[\w|\.\-*\]]*?\{((?!\*)[^{}]+)\})''')
            ck_str = [m.group(2) for m in rx.finditer(line) if m.group(2)]
            if len(ck_str)>0:
                for c in ck_str:
                    c = c.split(',')
                    cite_keys.extend(c)    
    
    for i,k in enumerate(cite_keys):
        cite_keys[i] = cite_keys[i].strip()
    # unique set:
    if unique_set:
        cite_keys = list(set(cite_keys))

    return cite_keys


def read_bib_file(bib_filename: str) -> BibliographyData:
    """ reads a bibtext bib file and returns the content as a BibliographyData object

    Args:
        bib_filename (string): path to bib file

    Returns:
        pybtex.database.BibliographyData: bibiliography object. (see https://docs.pybtex.org/api/parsing.html#pybtex.database.BibliographyData.to_file for docs)
    """

    print('reading the bib file')
    bib_data = parse_file(bib_filename)
    return bib_data


def remove_fields_from_bibliography(bib_dict: BibliographyData, remove_fields: list[str] = []) -> BibliographyData:
    """removes fields in a bibliography

    Args:
        bib_dict (pybtex.database.BibliographyData): bibliography object
        remove_fields (list, optional): names of fields that should be removed (e.g., ['file', 'abstract']). Defaults to [].

    Returns:
        [pybtex.database.BibliographyData]: reference to changed bib_dict
    """
    for key in bib_dict.entries:
        for rm in remove_fields:
            if rm in bib_dict.entries[key].fields:
                del bib_dict.entries[key].fields[rm]
    return bib_dict
