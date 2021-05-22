import argparse
from typing import Union, Optional
import pylatex_tools as pl

def str2bool(v: Union[str, bool]) -> bool:
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "extracts citation keys and displays how often you used that citation",
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('operation', type=str, choices=['count_citations', 'count_words', 'create_new_bibliography', 'detex'])
    parser.add_argument('tex_filename', type=str, help='path to the latex file')   
    parser.add_argument('-b', '--bibliography', type=str, default = None, help='for operations [count_citations, create_new_bibliography]: path to the bibliography (bibtex file)')
    parser.add_argument('-r', '--remove_fields', nargs='*', default=[''], help='for operations [create_new_bibliography]: bibliography fields that should not be included in the newly written bib file (default: file, abstract, note)')
    parser.add_argument('-c', '--citation_keys', nargs='*', default=[], help='for operations [count_citations]: if citation keys are provided - only these are searched for (also searches for partial matches of citation keys with the argument) (default: []])')
    parser.add_argument('-p', '--pattern_match_in_bibliography', nargs='*', default=[], help='for operations [count_citations]: performs pattern matching in author names and title of the references - requires argument --bibliography to be specified (default: None)')
    parser.add_argument('-i', '--ignore_via_tc_ignore', type=str2bool, default=False, nargs='?', const=True,  help='for operations [count_words]: wethere to ignore lines between "%TC:ignore" and "%TC:endignore".')    
    parser.add_argument('-w', '--write_csv_output', type=str2bool, default=False, nargs='?', const=True, help='for operations [count_words]: whether to write the word count to csv file. Default True.')
    parser.add_argument('-o', '--out_filename', type=str, default = None, help='for operations [detex, create_new_bibliography]: specify a path to an output file (default: None)')

    args = parser.parse_args()    
    tex_filename = args.tex_filename
    
    if args.operation == "count_citations":

        citation_keys = args.citation_keys
        pattern_match_in_bibliography = args.pattern_match_in_bibliography
        bibliography = args.bibliography
        if pattern_match_in_bibliography:
            assert bibliography, "you need to specify the bibliography file via --bibliography when using --pattern_match_in_bibliography"

        print((f"counting citations in {tex_filename}").upper())
        pl.count_citations(tex_filename, citation_keys, pattern_match_in_bibliography, bibliography)

    elif args.operation == "count_words":

        ignore_via_tc_ignore = args.ignore_via_tc_ignore
        write_csv_output = args.write_csv_output   

        print((f"counting words in {tex_filename}{' - writing counts to two csv files' if write_csv_output else ''}").upper())
        
        pl.count_words(tex_filename, ignore_via_tc_ignore=ignore_via_tc_ignore, write_csv_output=write_csv_output)

    elif args.operation == "create_new_bibliography":
        
        bibliography = args.bibliography
        assert bibliography, "--bibliography has to be specified for operation create_new_bibliography"
        output_bibliography = args.out_filename
        assert output_bibliography, "--out_filename has to be specified for operation create_new_bibliography"
        remove_fields = args.remove_fields
        
        if len(remove_fields) == 1 and remove_fields[0] == 'most':
                remove_fields = ['file', 'abstract', 'day', 'month', 'keywords', 'urldate', 'language', 'iss', 'note', 'isbn']

        print(('creating new bibfile').upper())
        if len(remove_fields)>0:
                print('the following fields will be removed from the new bibliography: %s' % ', '.join(remove_fields))
                
        print('input tex document: %s' % tex_filename)
        print('input bibtex database: %s' % bibliography)

        pl.create_new_bibliography(tex_filename, bibliography, output_bibliography, remove_fields)

    elif args.operation == "detex":

        out_filename = args.out_filename
        tex_string = pl.get_tex_string_from_file(tex_filename)
        detex_string = pl.detex(tex_string)
        detex_string = detex_string.replace('\\', '').replace('\\','')
        
    
        print((f"detex file {tex_filename}").upper())
        if args.out_filename is not None:
            with open(out_filename, 'w', encoding="utf8") as f:
                f.write(detex_string)
                print('\noutput written to file %s' % out_filename)
        else:
            print(detex_string)
    
    else:
        raise Exception(f"operation {args.operation} not known")
