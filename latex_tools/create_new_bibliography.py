# %%
import os
import json
import argparse

from .texhelpers import strip_comments_in_tex, get_citations_in_tex, read_bib_file

def load_file(filename):
    textfile = open(filename, 'r', encoding="utf8")
    lines = []
    for line in textfile:
        lines.append(line)
    textfile.close()
    return lines

def write_output(bib_str, output_file = 'out.bib'):
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(bib_str)

def create_new_bib_str(cite_keys, bib_dict):
    """ writes a new bib file from a list of cite_keys

    Args:
        cite_keys (list): list of citations keys
        bib_dict (dict): dictionary of bib entries
        output_file (string, optional): path to the output file to which should be written. Defaults to 'out.bib'.
    
    Returns:
        bib file as a str
    """

    bib_str = ''
    for ck in cite_keys:
        try:
            bib_str += bib_dict[ck]
        except:
            if ck in bib_dict:
                print('could not print key "%s"' % ck)
            else:
                print('could not find key "%s"' % ck)
    return bib_str

def create_new_bibliography(bib_filename, tex_filename, output_file, overwrite_json = False):
    bib_dict = read_bib_file(bib_filename, overwrite_json=overwrite_json)

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
    parser.add_argument('--bib_filename', type=str, default = 'references.bib', help='path to the bibtex library (bib file)')
    parser.add_argument('--tex_filename', type=str, default = 'main.tex', help='path to the latex file')
    parser.add_argument('--out_filename', type=str, default = 'out.bib', help='path to the new output filename to which the new bibtex library should be written')
    parser.add_argument('--overwrite_json', type=bool, default = False, help='whether to overwrite an existing json of the bib database')
    
    args = parser.parse_args()

    bib_filename = args.bib_filename
    tex_filename = args.tex_filename
    output_file = args.out_filename
    overwrite_json = args.overwrite_json

    print(('creating new bibfile').upper())
    print('input tex document: %s' % tex_filename)
    print('input bibtex database: %s' % bib_filename)
    create_new_bibliography(bib_filename, tex_filename, output_file, overwrite_json)


