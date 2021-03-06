# %%
import os
import sys
import re
import argparse

from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from pylatex_tools.detex import detex
from pylatex_tools.texhelpers import strip_comments_in_tex, load_file_as_list, strip_tc_ignore

sectioning_commands = ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
sectioning_commands_dict = {x: i for i, x in enumerate(sectioning_commands)}

def has_struct_el(text: str) -> tuple[Optional[str], Optional[int]]:    
    """checks for the presence of a sectioning command in a string

    Args:
        text (str): string

    Returns:
        tuple: (sectioning_command, position in str) if present, otherwise (None,None)
    """
    for i, h in enumerate(sectioning_commands):
        p = text.find('\\' + h)
        if p >= 0:
            return h, p    
    return None, None
    
def count_words_in_list(lines: list[str]) -> tuple[list[str], list[str], list[int], list[int]]:
    """counts word in a tex doc - structure by the sectioning commands

    Args:
        lines (list): list of tex lines

    Returns:
        tuple (list, list, list, list): 
            heading_name (list): subsectioning heading names
            heading_level (list): which level the corresponding heading is at
            counts (list): word count in between two subsectioning commands
            counts_cum (list): cummulative count of all words in a subsection
    """
    current_level = 0
    
    heading_name = []
    heading_level = []
    level = [] 
    linenum = [] 
    for i, line in enumerate(lines):
        h, p = has_struct_el(line)
        if h:
            rx = re.compile(r'''(?<!\\)%.+|(\\(?:no)?''' + h +  r'''[\*]*?\{((?!\*)[^{}]+)\})''')
            ck_str = [m.group(2) for m in rx.finditer(line) if m.group(2)]
            heading_level.append(h)
            heading_name.append(ck_str[0])
            level.append(sectioning_commands_dict[h])
            linenum.append(i)
    linenum.append(len(lines))

    counts = [0 for x in heading_name]
    # loop over headings
    for i, h in enumerate(heading_name):
        
        # count number of words in that part (until the next heading)
        tex_str = ''
        #print('%s from line %d to %d' % (h, linenum[i], linenum[i+1]))
        for j in range(linenum[i], linenum[i+1]):
            tex_str += lines[j]
        txt = detex(tex_str)
        cnt = len(txt.split())        
        counts[i] = cnt
    
    # now add counts to higher level headings
    counts_cum = counts.copy()
    for i, l1 in enumerate(level):
        for j, l2 in enumerate(level[i+1:]):
            if l2 <= l1:
                break
            else:
                counts_cum[i] += counts[j+i+1]

    sep = '  '
    print('\n\n  **word count from heading to next heading (e.g., from section heading to next heading, which could be subsection)**\n')
    for i, h in enumerate(heading_level):
        print(sep * sectioning_commands_dict[h] + '%d' % counts[i] + sep * (6-sectioning_commands_dict[h]) + sep * (sectioning_commands_dict[h]) + heading_name[i])

    print('\n\n  **word count for each subpart (e.g., all words in a section)**\n')
    for i, h in enumerate(heading_level):
        print(sep * sectioning_commands_dict[h] + '%d' % counts_cum[i] + sep * (6-sectioning_commands_dict[h]) + sep * (sectioning_commands_dict[h]) + heading_name[i])

    print('\n')
    print('%d in total words when summed across the section count\n' % sum([x for i,x in enumerate(counts_cum) if heading_level[i]=='section']))

    return heading_name, heading_level, counts, counts_cum


def write_to_csv(filename: str, counts: list[int], heading_level: list[str], heading_name: list[str], sep: str = ',') -> None:
    with open(filename, 'w', encoding = "utf-8") as f:
        f.write(sep.join(sectioning_commands) + sep + sep.join(sectioning_commands))
        f.write('\n')
        for i, h in enumerate(heading_level):
            line = sep * sectioning_commands_dict[h] + heading_name[i].replace(sep, '') + sep * (6-sectioning_commands_dict[h]) + sep * (sectioning_commands_dict[h]) + '%d' % counts[i]
            f.write(line)
            f.write('\n')

def count_words(tex_filename: str, ignore_via_tc_ignore: bool = False, write_csv_output: bool = False) -> None:
    """creates a word count for each document level and subpart for a tex document
       removes tex commands, image captions, header, citations, etc. - only counts the text
    """
    lines = load_file_as_list(tex_filename)
    if ignore_via_tc_ignore:
        lines = strip_tc_ignore(lines)
    lines = strip_comments_in_tex(lines)

    print(('\n\nword count for file %s' % tex_filename).upper())

    heading_name, heading_level, counts, counts_cum = count_words_in_list(lines)

    if write_csv_output:
        output_file = tex_filename.split('.')[0]+'-wordcount.csv'
        write_to_csv(output_file, counts_cum, heading_level, heading_name)

        output_file = tex_filename.split('.')[0]+'-wordcount-till-next-header.csv'
        write_to_csv(output_file, counts, heading_level, heading_name)

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description = "creates a word count for each document level and subpart for a tex document\nremoves tex commands, image captions, header, citations, etc. - only counts the text",
                formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tex_filename', type = str, help = 'path to the latex file')   
    parser.add_argument('-i', '--ignore_via_tc_ignore', type = bool, default = False, help='wethere to ignore lines between "%TC:ignore" and "%TC:endignore".')    
    parser.add_argument('-w', '--write_csv_output', type = bool, default = False, help = 'whether to write the word count to csv file. Default True.')
    args = parser.parse_args()

    count_words(args.tex_filename, ignore_via_tc_ignore=args.ignore_via_tc_ignore, write_csv_output=args.write_csv_output)
