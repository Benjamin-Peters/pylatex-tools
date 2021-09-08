# %%
import os
import sys
import argparse

from typing import Optional

from pybtex.database import BibliographyData # type: ignore

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pylatex_tools.texhelpers import strip_comments_in_tex, get_citations_in_tex, read_bib_file, remove_fields_from_bibliography

def load_file(filename: str) -> list[str]:
    """ reads a text file and returns a list of the lines in the file

    Args:
        filename (str): file to be read

    Returns:
        list: list of lines
    """
    textfile = open(filename, 'r', encoding="utf8")
    lines = []
    for line in textfile:
        lines.append(line)
    textfile.close()
    return lines

def write_output(string: str, output_file: str = 'out.bib'):
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(string)

def create_new_bib_str(cite_keys: list[str], bib_dict: BibliographyData) -> str:
    """ creates a new bibtex bibliography from a list of cite_keys as a string

    Args:
        cite_keys (list): list of citations keys
        bib_dict (pybtex.database.BibliographyData): bibliography object
        output_file (string, optional): path to the output file to which should be written. Defaults to 'out.bib'.
    
    Returns:
        bib file as a string
    """

    bib_str = ''
    for ck in cite_keys:
        if ck in bib_dict.entries:
            bib_str += bib_dict.entries[ck].to_string('bibtex')
        else:
            print('could not find key "%s"' % ck)
    return bib_str

def create_new_bibliography(tex_filename: str, bib_filename: str, 
                            output_file: str, remove_fields: list[str] = ['file', 'abstract', 'note']) -> None:
    """ creates a new bibliography (bibtex) which contains only those bib entries that have been cited in the tex file

    Args:
        bib_filename (str): path to the original bibliography (bibtex file)
        tex_filename (str): path to the tex document in which citations occur
        output_file (str): path to the to-be created bibliography (bibtex file)
        remove_fields (list, optional): a list of fields that should not be included in the new bibliography. Defaults to ['file', 'abstract', 'note'].
    """
    bib_dict = read_bib_file(bib_filename)
    
    bib_dict = remove_fields_from_bibliography(bib_dict, remove_fields)

    tex_lines = load_file(tex_filename)
    stripped_lines = strip_comments_in_tex(tex_lines)
    cite_keys = get_citations_in_tex(stripped_lines)

    bib_str = create_new_bib_str(cite_keys, bib_dict)
    print('found %d citations in the file %s\nwriting new bibtex file to %s' % (len(cite_keys), tex_filename, output_file))
    write_output(bib_str, output_file='out.bib')

# %%
if __name__ == "__main__":
    """ this function writes a new bib file from the citation keys found in a tex file
            this function might come handy if you have a large bibtex file and you want to
            create a new bibtex file that only contains the citations in a specific document
    """
    parser = argparse.ArgumentParser(description= "this function writes a new bib file from the citation keys found in a tex file\nit function might come handy if you have a large bibtex file and you want to\ncreate a new bibtex file that only contains the citations in a specific document",
                formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tex_filename', type=str, default = 'main.tex', help='path to the latex file')
    parser.add_argument('bib_filename', type=str, default = 'references.bib', help='path to the bibtex library (bib file)')
    parser.add_argument('-o', '--out_filename', type=str, default = 'out.bib', help='path to the new output filename to which the new bibtex library should be written')
    parser.add_argument('-r', '--remove_fields', nargs='*', default=[], help='bibliography fields that should not be included in the newly written bib file (default: file)')

    args = parser.parse_args()

    bib_filename = args.bib_filename
    tex_filename = args.tex_filename
    output_file = args.out_filename
    remove_fields = args.remove_fields
    
    if len(remove_fields) >= 1 and 'most' in remove_fields:
        remove_fields = [f for f in remove_fields if f != 'most']
        remove_fields += ['file', 'abstract', 'day', 'month', 'keywords', 'urldate', 'language', 'issn', 'note', 'isbn']

    print(('creating new bibfile').upper())
    if len(remove_fields)>0:
        print('the following fields will be removed from the new bibliography: %s' % ', '.join(remove_fields))
        
    print('input tex document: %s' % tex_filename)
    print('input bibtex database: %s' % bib_filename)
    create_new_bibliography(tex_filename,bib_filename, output_file, remove_fields)



# %%
