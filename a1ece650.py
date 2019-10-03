import sys
import shlex
import re
from drawgraph import Graph
gr = Graph()

def main():

    while True:
        try:
            user_input = raw_input("")
        except EOFError:
            break
        if user_input == '':
            break
        Line = user_input.replace('\n', '')
        pattern = r'(^[ \t]*a[ \t]+\"{1}([ \t]*[a-zA-Z \t]+[ \t]*)+\"{1}[ \t]+(\({1}([ \t]*[-+]?[0-9]+[ \t]*)\,{1}([ \t]*[-+]?[0-9]+[ \t]*)\){1} *)+[ \t]*$)|(^[ \t]*c[ \t]+\"{1}([ \t]*[a-zA-Z \t]+[ \t]*)+\"{1}[ \t]+(\({1}([ \t]*[-+]?[0-9]+[ \t]*)\,{1}([ \t]*[-+]?[0-9]+[ \t]*)\){1} *)+[ \t]*$)|(^[ \t]*r[ \t]+\"{1}([ \t]*[a-zA-Z \t]+[ \t]*)+\"{1}[ \t]*$)|(^[ \t]*g[ \t]*$)'
        r = re.compile(pattern)
        if not (r.match(Line)):
            sys.stderr.write("Error: Non valid input, please enter a right command\n")
            continue

        else:
            vld_input = Line
            if '(' in vld_input:
                coord_indx = vld_input.index('(')
                coord = vld_input[coord_indx:]
                cln_coord = re.sub(' +', '', coord)
                seprt_coord = re.sub('\)\(', ') (', cln_coord)
                final_str = vld_input[:coord_indx] + seprt_coord
                final_parts = shlex.split(final_str)


                if final_parts[0] == 'a':
                    gr.add_strt(final_parts[1].lower(), final_parts[2:])


                elif final_parts[0] == 'c':
                    gr.change_strt(final_parts[1].lower(), final_parts[2:])

                else:
                    sys.stderr.write("Error: Not valid format for the input\n")


            else:
                final_parts = shlex.split(vld_input)
                if final_parts[0] == 'r':
                    gr.remove_srtr(final_parts[1].lower())

                elif final_parts[0] == 'g':
                    gr.print_graph()

                else:
                    sys.stderr.write("Error: Non valid input\n")

    sys.exit(0)



if __name__ == '__main__':
    main()

