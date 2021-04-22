import os
import re
import json

def strip_comments_in_tex(tex_lines):
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

def get_citations_in_tex(tex_lines, cite_commands = ['autocite', 'cite']): 
    """returns list of cite keys being used in the tex_lines

    Args:
        tex_string (list): list of strings with tex code
        cite_commands (list, optional): keywords commands in the tex document. Defaults to ['autocite', 'cite'].

    Returns:
        list: list of citation keys (strings)
    """
    cite_keys = []
    for line in tex_lines:
        for cc in cite_commands:
            # https://stackoverflow.com/questions/57064771/extract-cited-bibtex-keys-from-tex-file-using-regex-in-python
            rx = re.compile(r'''(?<!\\)%.+|(\\(?:no)?''' + cc +  r'''?\{((?!\*)[^{}]+)\})''')
            ck_str = [m.group(2) for m in rx.finditer(line) if m.group(2)]
            if len(ck_str)>0:
                for c in ck_str:
                    c = c.split(',')
                    cite_keys.extend(c)    
    
    for i,k in enumerate(cite_keys):
        cite_keys[i] = cite_keys[i].strip()
    cite_keys = list(set(cite_keys))

    return cite_keys


def read_bib_file(bib_filename, overwrite_json = False):
    """ reads a bibtext bib file and returns the content as a dict
        stores a copy of the dict as json and loads it if it exists

    Args:
        bib_filename (string): path to bib file
        overwrite_json (bool, optional): whether to overwrite an existing json of the dict. Defaults to False.

    Returns:
        dict: bibiliography. cite_keys as keys 
    """

    def find_idx(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]


    if os.path.exists(bib_filename+'.json') and not overwrite_json:
        with open(bib_filename+'.json') as json_file:
            bibdb = json.load(json_file)
    else:
        print('reading the bib file')
        # load bib file
        textfile = open(bib_filename, 'r', encoding="utf8")
        filetext = textfile.read()
        textfile.close()     

        # find locations of '@'
        indices = find_idx(filetext, '@')
        indices.append(-1)

        bibdb = {}
        for i,p in enumerate(indices[:-1]):
            actkey_start = filetext[p:].find('{') + 1
            actkey_end = filetext[p+actkey_start:].find(',')
            actkey = filetext[p+actkey_start:actkey_end+actkey_start+p]
            
            next_entry_start = indices[i+1]
            entry = filetext[p:next_entry_start]

            #entry = entry.replace('\\', '')
            #entry = entry.encode('utf-8').decode('ascii', 'ignore')

            bibdb[actkey] = entry

            if len(bibdb) % 500 == 0:
                print('%d of %d' % (len(bibdb), len(indices)))   
        
        print('finished reading bib file')

        with open(filename+'.json', 'w') as fp:
            json.dump(bibdb, fp)    
    return bibdb


#def strip_tex_commands_with_content(tex_lines, strip_commands = ['section', 'subsection', 'subsubsection', 'paragraph', 'cite', 'autocite']):
