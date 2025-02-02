import sys
import getopt
import re

HELP_STRING = """
Creates a Bibtex chapter bibliography file by scanning the chapter source for references to the 
sources listed in the master Bibtex bibliography.
"""


def main(argv):
    chapter_file = None

    try:
        opts, args = getopt.getopt(
            argv,
            "c:m:",
            ["chapter_source=", "master_bibliography="]
        )
    except getopt.GetoptError:
        print(HELP_STRING)
        sys.exit(2)

    # comment out this block to test
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print(HELP_STRING)
            sys.exit()
        elif opt in ["-c", "--chapter_source"]:
            chapter_file = arg
        elif opt in ["-m", "--master_bibliography"]:
            master_file = arg

    if chapter_file is not None and master_file is not None:
        chapter_bib = []

        print('\x1b[34m Scanning the chapter TeX file for references... \n \x1b[37m')
        chp_handle = open(chapter_file, 'r')
        chp = chp_handle.read()
        ref_pos = [match.start() for match in re.finditer(r'\\cite', chp)]
        print(f'Found {len(ref_pos)} in-line references \n')

        print('\x1b[34m Comparing the references to the master bibliography... \n \x1b[37m')
        mstr_handle = open(master_file, 'r')
        mstr = mstr_handle.read()
        lines = mstr.split("\n")
        pos = 0
        while pos < len(lines):
            line = lines[pos]
            if '@' in line:
                ref_info = f"\n{line}"
                ref_str = line.split('{')[1].split(',')[0]  # strip @inproceedings or @article, etc. and ,
                found = False
                for chp_pos in ref_pos:
                    pos_refs = chp[chp_pos + 6 : chp_pos + chp[chp_pos:].index('}')].split(',')
                    for pos_ref in pos_refs:
                        if pos_ref.strip() == ref_str:  # if the ref is in the chapter
                            found = True
                            print(f'Found ref {ref_str} \n')
                            while line and line[0] != '}':
                                pos += 1
                                line = lines[pos]
                                ref_info += f"\n{line}"
                            chapter_bib.append(ref_info)
                            break
                    if found:
                        break
                if not found:
                    print(f'No match for {ref_str} in {chapter_file} \n')
            pos += 1

        print('\x1b[34m Writing the matching references to the chapter bibliography... \n \x1b[37m')
        chp_bib_handle = open(f"{chapter_file.split('.')[0]}.bib", 'w')
        chp_bib_handle.write('\n'.join(chapter_bib))

        print('\x1b[34m Done! Cleaning up... \n \x1b[37m')
        chp_handle.close()
        mstr_handle.close()
        chp_bib_handle.close()

        print('\x1b[34m ~*Squeaky clean*~ \n \x1b[37m')

    else:
        print("The chapter file and master bibliography file are required parameters.")


if __name__ == '__main__':
    main(sys.argv[1:])
