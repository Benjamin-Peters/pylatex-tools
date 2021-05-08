# %%
import os
import sys
import argparse
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pylatextools.texhelpers import strip_comments_in_tex, get_citations_in_tex, load_file_as_list, strip_tc_ignore, read_bib_file


def count_citations(filename, citation_keys=None, 
            pattern_match_in_bibliography = None, bibliography = None):
    # load lines from tex file
    lines = load_file_as_list(filename)
    if args.ignore_via_tc_ignore:
        lines = strip_tc_ignore(lines)
    lines = strip_comments_in_tex(lines)

    # get citation keys from tex file
    cites = get_citations_in_tex(lines, unique_set=False)
    
    # if citation_keys was specified as argument, filter for these
    if args.citation_keys:
        cites = [c for c in cites if any([c.find(ck)>=0 for ck in args.citation_keys])]
    
    if bibliography:
        bib_dict = read_bib_file(args.bibliography)

    # if pattern_match_in_bibliography was specified, filter for matches
    if args.pattern_match_in_bibliography:
        #load bibliography
        cites_ = []
        for c in cites:
            
            title_match = False
            try:
                title = bib_dict.entries[c].fields['title'].replace('{', '').replace('}', '')
                title_match = any([title.find(p)>=0 for p in args.pattern_match_in_bibliography])
            except:
                pass

            authors_match = False
            try:
                authors = [x.__str__() for x in bib_dict.entries[c].persons['author']]
                for a in authors:
                    for p in args.pattern_match_in_bibliography:
                        authors_match = authors_match or re.search(p, a, re.IGNORECASE)
                    #authors_match = authors_match or any([a.find(p)>=0 for p in args.pattern_match_in_bibliography])
            except:
                pass

            if any([title_match, authors_match]):
                cites_.append(c)
        cites = cites_

    # count occurences per key
    unique_cites = list(set(cites))
    counts = [cites.count(c) for c in unique_cites]

    # print keys with the number of their occurences, ordered by their occurences
    order = sorted(range(len(counts)), reverse = True, key=lambda k: counts[k])
    if bibliography:
        print('\n' + '-' * 50)
        print('\ncitation_key: # occurences -- reference\n')        
        for o in order:
            authors = ''
            try:
                authors = [x.__str__() for x in bib_dict.entries[unique_cites[o]].persons['author']]
            except:
                pass
            year = bib_dict.entries[unique_cites[o]].fields['year']
            title = bib_dict.entries[unique_cites[o]].fields['title']
            print(f"{unique_cites[o]}: {counts[o]} -- {' '.join(authors)} ({year}) {title}")
    else:
        print('\n' + '-' * 50)
        print('\ncitation_key: # occurences\n')        
        for o in order:
            print(f"{unique_cites[o]}: {counts[o]}")
        
    print(f"\nA total of {len(cites)} citations found, {len(unique_cites)} unique.")
    print('\n' + '-' * 50)
    # tabulate the number of occurences
    tab = {}
    for c in counts:
        if c in tab.keys():
            tab[c] += 1
        else:
            tab[c] = 1
    print('\n# occurences:# references')
    for c in sorted(tab.keys(), reverse=True):
        print(f"{c}:{tab[c]}")
    print('\n' + '-' * 50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "extracts citation keys and displays how often you used that citation",
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tex_filename', type=str, help='path to the latex file')   
    parser.add_argument('-c', '--citation_keys', nargs='*', default=[], help='if citation keys are provided - only these are searched for (also searches for partial matches of citation keys with the argument')
    parser.add_argument('-p', '--pattern_match_in_bibliography', nargs='*', default=[], help='performs pattern matching in author names and title of the references - requires argument --bibliography to be specified')
    parser.add_argument('-b', '--bibliography', type=str, default = None, help='path to the bibliography (bibtex file)')
    parser.add_argument('-i', '--ignore_via_tc_ignore', type=bool, default=False, help='wethere to ignore lines between "%TC:ignore" and "%TC:endignore".')    
    #parser.add_argument('-w', '--write_csv_output', type=bool, default=False, help='whether to write the word count to csv file. Default True.')
    args = parser.parse_args()

    count_citations(args.tex_filename, args.citation_keys, args.pattern_match_in_bibliography, args.bibliography)
# %%
