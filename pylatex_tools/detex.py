# %%    
import argparse
import regex as re

def get_tex_string_from_file(filename: str):
    # just opens the file and returns the content as a string
    textfile = open(filename, 'r', encoding="utf8")
    filetext = textfile.read()
    textfile.close()
    return filetext

# detex functions largely based of http://www.gilles-bertrand.com/2012/11/a-simple-detex-function-in-python.html

def apply_regexps(text: str, list_reg_exp: list, text_mode: bool = False):
    """ Applies successively many regexps to a text"""
    if text_mode:
        print('\n'.join(list_reg_exp))
    # apply all the rules in the ruleset
    for element in list_reg_exp:
        left = element['left']
        right = element['right']
        r = re.compile(left)
        text = r.sub(right,text)
    return text

def detex_remove_header(text: str):
    # remove all the contents of the header, ie everything before the first occurence of "\begin{document}"
    text = re.sub(r"(?s).*?(\\begin\{document\})", "", text, 1)
    return text

def detex_remove_comments(text: str):
    # remove comments
    regexps=[]
    regexps.append({r'left':r'([^\\])%.*', 'right':r'\1'})
    text= apply_regexps(text, regexps)    
    return text

def detex_reduce(text: str, to_reduce: list = [r'\\emph', r'\\textbf', r'\\textit', r'\\text', r'\\IEEEauthorblockA', r'\\IEEEauthorblockN', r'\\author', r'\\caption',r'\\author',r'\\thanks']):
    # replace some LaTeX commands by the contents inside the curly brackets
    regexps=[]
    for tag in to_reduce:
        regexps.append({'left':tag+r'\{([^\}\{]*)\}', 'right':r'\1'})
    text = apply_regexps(text, regexps)
    return text

def detex_highlight(text: str):
    # replace some LaTeX commands by the contents inside curly brackets and highlight these contents
    regexps = []
    to_highlight = [r'\\part[\*]*', r'\\chapter[\*]*', r'\\section[\*]*', r'\\subsection[\*]*', r'\\subsubsection[\*]*', r'\\paragraph[\*]*'];
    # highlightment pattern: #--content--#
    for tag in to_highlight:
      regexps.append({'left':tag+r'\{([^\}\{]*)\}','right':r'\n#--\1--#\n'})
    # highlightment pattern: [content]
    to_highlight = [r'\\title',r'\\author',r'\\thanks',r'\\cite', r'\\ref'];
    for tag in to_highlight:
      regexps.append({'left':tag+r'\{([^\}\{]*)\}','right':r'[\1]'})
    text = apply_regexps(text, regexps)
    return text

def detex_remove(text: str):
    # remove LaTeX tags
    # - remove completely some LaTeX commands that take arguments
    to_remove = [r'\\maketitle',r'\\footnote', r'\\centering', r'\\IEEEpeerreviewmaketitle', r'\\includegraphics', 
                 r'\\IEEEauthorrefmark', r'\\label', r'\\begin', r'\\end', r'\\big', r'\\right', r'\\left', 
                 r'\\documentclass', r'\\usepackage', r'\\bibliographystyle', r'\\bibliography',  r'\\cline', r'\\multicolumn', 
                 r'\\autocite', r'\\cite', r'\\caption', r'\\ref', r'\\input']
    
    # replace tag with options and argument by a single space
    regexps = []
    for tag in to_remove:
      regexps.append({'left':tag+r'(\[[^\]]*\])*(\{[^\}\{]*\})*', 'right':r' '})
      #regexps.append({'left':tag+r'\{[^\}\{]*\}\[[^\]\[]*\]', 'right':r' '})
    text = apply_regexps(text, regexps)
    return text

def detex_replace(text: str):
    # - replace some LaTeX commands by the contents inside curly rackets
    # replace some symbols by their ascii equivalent
    # - common symbols
    regexps = []    
    regexps.append({'left':r'\\eg(\{\})* *','right':r'e.g., '})
    regexps.append({'left':r'\\ldots','right':r'...'})
    regexps.append({'left':r'\\Rightarrow','right':r'=>'})
    regexps.append({'left':r'\\rightarrow','right':r'->'})
    regexps.append({'left':r'\\le','right':r'<='})
    regexps.append({'left':r'\\ge','right':r'>'})
    regexps.append({'left':r'\\_','right':r'_'})
    regexps.append({'left':r'\\\\','right':r'\n'})
    regexps.append({'left':r'~','right':r' '})
    regexps.append({'left':r'\\&','right':r'&'})
    regexps.append({'left':r'\\%','right':r'%'})
    regexps.append({'left':r'([^\\])&','right':r'\1\t'})
    regexps.append({'left':r'\\item','right':r'\t- '})
    regexps.append({'left':r'\\\hline[ \t]*\\hline','right':r'============================================='})
    regexps.append({'left':r'[ \t]*\\hline','right':r'_____________________________________________'})
    # - special letters
    regexps.append({'left':r'\\\'{?\{e\}}?','right':r'é'})
    regexps.append({'left':r'\\`{?\{a\}}?','right':r'à'})
    regexps.append({'left':r'\\\'{?\{o\}}?','right':r'ó'})
    regexps.append({'left':r'\\\'{?\{a\}}?','right':r'á'})
    # keep untouched the contents of the equations
    regexps.append({'left':r'\$(.)\$', 'right':r'\1'})
    regexps.append({'left':r'\$([^\$]*)\$', 'right':r'\1'})
    # remove the equation symbols ($)
    regexps.append({'left':r'([^\\])\$', 'right':r'\1'})
    # correct spacing problems
    regexps.append({'left':r' +,','right':r','})
    regexps.append({'left':r' +','right':r' '})
    regexps.append({'left':r' +\)','right':r'\)'})
    regexps.append({'left':r'\( +','right':r'\('})
    regexps.append({'left':r' +\.','right':r'\.'})    
    # remove lonely curly brackets    
    regexps.append({'left':r'^([^\{]*)\}', 'right':r'\1'})
    regexps.append({'left':r'([^\\])\{([^\}]*)\}','right':r'\1\2'})
    regexps.append({'left':r'\\\{','right':r'\{'})
    regexps.append({'left':r'\\\}','right':r'\}'})
    # strip white space characters at end of line
    regexps.append({'left':r'[ \t]*\n','right':r'\n'})
    # remove consecutive blank lines
    regexps.append({'left':r'([ \t]*\n){3,}','right':r'\n'})
    # apply all those regexps
    text = apply_regexps(text, regexps)
    # return the modified text
    return text    

def detex(text: str):
    """removes all tex commands from a tex document and creates a text-only version of the document

    Args:
        text (string): input latex string

    Returns:
        string: text-only version of the input
    """
    text = detex_remove_header(text)
    text = detex_remove_comments(text)
    text = detex_reduce(text)
    text = detex_highlight(text)
    text = detex_remove(text)
    text = detex_replace(text)
    return text

if __name__ == "__main__":
    """removes all tex commands from a tex document and creates a text-only version of the document
    """

    parser = argparse.ArgumentParser(description="removes all tex commands from a tex document and creates a text-only version of the document")
    parser.add_argument('tex_filename', type=str, help='path to the latex file')   
    parser.add_argument('-o', '--out_filename', type=str, default = None, help='specify a path to an output file in case you want to write the output')
    args = parser.parse_args()    
    
    tex_string = get_tex_string_from_file(args.tex_filename)

    detex_string = detex(tex_string)
    detex_string = detex_string.replace('\\', '').replace('\\','')
    if args.out_filename is not None:
        with open(args.out_filename, 'w', encoding="utf8") as f:
            f.write(detex_string)
        print('\noutput written to file %s' % args.out_filename)
    else:
        print(detex_string)
# %%
