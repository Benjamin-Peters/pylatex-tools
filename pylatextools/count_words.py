# %%
import re
import argparse

from .detex import detex
from .texhelpers import strip_comments_in_tex

hierarchy = ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph']
hierarchy_dict = {x: i for i,x in enumerate(hierarchy)}

def load_file(filename):
    textfile = open(filename, 'r', encoding="utf8")
    lines = []
    for line in textfile:
        lines.append(line)
    textfile.close()
    return lines


def has_struct_el(text):    
    for i, h in enumerate(hierarchy):
        p = text.find('\\' + h)
        if p >= 0:
            return h, p    
    return None, None
    

def count_words(lines):
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
            level.append(hierarchy_dict[h])
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
    for i,l1 in enumerate(level):
        for j, l2 in enumerate(level[i+1:]):
            if l2 <= l1:
                break
            else:
                counts_cum[i] += counts[j+i+1]

    sep = '  '
    print('\n\n  **word count from heading to next heading (e.g., from section heading to next heading, which could be subsection)**\n')
    for i, h in enumerate(heading_level):
        print(sep * hierarchy_dict[h] + '%d' % counts[i] + sep * (6-hierarchy_dict[h]) + sep * (hierarchy_dict[h]) + heading_name[i])

    print('\n\n  **word count for each subpart (e.g., all words in a section)**\n')
    for i, h in enumerate(heading_level):
        print(sep * hierarchy_dict[h] + '%d' % counts_cum[i] + sep * (6-hierarchy_dict[h]) + sep * (hierarchy_dict[h]) + heading_name[i])

    print('\n')
    print('%d in total words when summed across the section count\n' % sum([x for i,x in enumerate(counts) if heading_level[i]=='section']))

    return heading_name, heading_level, counts, counts_cum


def write_to_csv(filename, counts, heading_level, heading_name, sep = ','):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(sep.join(hierarchy) + sep + sep.join(hierarchy))
        f.write('\n')
        for i, h in enumerate(heading_level):
            line = sep * hierarchy_dict[h] + heading_name[i].replace(sep, '') + sep * (6-hierarchy_dict[h]) + sep * (hierarchy_dict[h]) + '%d' % counts[i]
            f.write(line)
            f.write('\n')
            
if __name__ == '__main__':
    """creates a word count for each document level and subpart for a tex document
       removes tex commands, image captions, header, citations, etc. - only counts the text
    """

    parser = argparse.ArgumentParser(description= "creates a word count for each document level and subpart for a tex document\nremoves tex commands, image captions, header, citations, etc. - only counts the text",
                formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('tex_filename', type=str, help='path to the latex file')   
    parser.add_argument('-w', '--write_csv_output', type=bool, default=False, help='whether to write the word count to csv file')
    args = parser.parse_args()    

    filename = args.tex_filename

    lines = load_file(filename)
    lines = strip_comments_in_tex(lines)

    print(('\n\nword count for file %s' % args.tex_filename).upper())

    heading_name, heading_level, counts, counts_cum = count_words(lines)

    output_file = filename.split('.')[0]+'-wordcount.csv'
    write_to_csv(output_file, counts_cum, heading_level, heading_name)

    output_file = filename.split('.')[0]+'-wordcount-till-next-header.csv'
    write_to_csv(output_file, counts, heading_level, heading_name)
# %%
