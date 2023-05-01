from argparse import ArgumentParser
import csv
import datetime
import pandas

parser = ArgumentParser(description="My utils for RULSTM")
#parser.add_argument('mode', type=str, choices=['train', 'validate', 'test', 'test', 'validate_json'], default='train',
#                    help="Whether to perform training, validation or test.\
#                            If test is selected, --json_directory must be used to provide\
#                            a directory in which to save the generated jsons.")
parser.add_argument('--fun', type=str, help="function to run")
parser.add_argument('--inf', type=str, help="Path to input file")
parser.add_argument('--outf', type=str, help="Path to output file")
parser.add_argument('--mod', type=int, default=1, help="Write every mod lines")
parser.add_argument('--int', type=str, help="Path to training file")
parser.add_argument('--inv', type=str, help="Path to validation file")
parser.add_argument('--ina', type=str, help="Path to actions file")
parser.add_argument('--outp', type=str, help="Path to output file prefix")
parser.add_argument('--rpera', type=int, default=10, help='rows to actions ratio')
parser.add_argument('--caption', type=str, default='caption', help='caption to use if required by function')
parser.add_argument('--label', type=str, default='label', help='label to use if required by function')
#parser.add_argument('--alpha', type=float, default=0.25,
#                    help="Distance between time-steps in seconds")
args = parser.parse_args()


def one_in_many():
    lineno = 0
    with open(args.inf, 'r') as inf:
        with open(args.outf, 'w') as outf:
            while (lin := inf.readline()):
                lineno += 1
                if lineno % args.mod == 0:
                    outf.write(lin)


def subsample_one(out_suf, row_num, annotations, actions):
    outfieldnames = ['index', 'video','start','end','verb','noun','action']
    #print(outfieldnames)
    with open(args.outp + out_suf, newline='', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=outfieldnames)
        offset = 0
        wcount = 0
        done = False
        while offset < args.mod and wcount < row_num and not done:
            i = 0
            while offset + i < len(annotations) and wcount < row_num:
                if annotations.values[offset+i][5] in actions:
                    row = {
                        'index':  annotations.index[offset+i],
                        'video':  annotations.values[offset+i][0].strip(),
                        'start':  annotations.values[offset+i][1],
                        'end':    annotations.values[offset+i][2],
                        'verb':   annotations.values[offset+i][3],
                        'noun':   annotations.values[offset+i][4],
                        'action': actions[annotations.values[offset+i][5]]
                    }
                    #print(f'offset: {offset}, i: {i}, wcount: {wcount}, row: {row}')
                    writer.writerow(row)
                    wcount += 1
                    #if wcount == row_num:
                    #    done = True
                    #    break
                i += args.mod
            offset += 1


def relabel_actions(out_suf, a_in, a_out):
    outfieldnames = ['id', 'action', 'verb', 'noun']
    with open(args.outp + out_suf, newline='', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=outfieldnames)
        writer.writeheader()
        for a in a_out.items():
            in_index = a[0]
            row = {
                'id':     a[1],
                'action': a_in.values[in_index][1].strip(),
                'verb':   a_in.values[in_index][2],
                'noun':   a_in.values[in_index][3]
            }
            writer.writerow(row)


# subsample both files by mod factor
# use number of actions rpera times smaller than number of output rows
def subsample():
    print(f'starting: {datetime.datetime.now()}')
    fieldnames = ['video','start','end','verb','noun','action']
    #print(fieldnames)
    trn_anns = pandas.read_csv(args.int, header=None, names=fieldnames)
    val_anns = pandas.read_csv(args.inv, header=None, names=fieldnames)
    actions_in = pandas.read_csv(args.ina)
    print(f'in trn: {len(trn_anns)}, in val: {len(val_anns)}, in actions: {len(actions_in)}')
    #print(actions_in)

    # calculate number of output rows and actions
    trn_row_num = int(len(trn_anns) / args.mod)
    val_row_num = int(len(val_anns) / args.mod)
    act_num = int(trn_row_num / args.rpera)
    print(f'out trn: {trn_row_num}, out val: {val_row_num}, out actions: {act_num}')

    # iterate over validation set, and fill dictionary with act_num actions
    actions_out = {}
    offset = 0
    done = False
    act_count = 0
    while offset < args.mod and act_count < act_num and not done:
        #for i in range(0, val_row_num, args.mod):
        i = 0
        while offset + i < len(val_anns) and act_count < act_num:
            #actions[val_anns.values[offset+i][5]] = val_anns.index[offset+i]
            # re-map action ids to be in the expected range
            if val_anns.values[offset+i][5] not in actions_out:
                actions_out[val_anns.values[offset+i][5]] = act_count
                act_count += 1
            i += args.mod
        offset += 1
    print(f'captured {len(actions_out)} actions')
    print(f'relabeling: {datetime.datetime.now()}')
    relabel_actions('actions.csv', actions_in, actions_out)

    # iterate over validation set, and write val_row_num actions from dictionary
    print(f'subsampling validation: {datetime.datetime.now()}')
    subsample_one('validation.csv', val_row_num, val_anns, actions_out)
    print(f'subsampling training: {datetime.datetime.now()}')
    subsample_one('training.csv', trn_row_num, trn_anns, actions_out)
    #val_anns_out = pandas.DataFrame().reindex_like(val_anns)
    #val_anns_out = pandas.DataFrame(val_rows)
    #val_anns_out.to_csv(args.outp + 'validation.csv')
    print(f'done: {datetime.datetime.now()}')


def make_latex_table_full(caption, label):
    # open file, read results and tokenise into dict
    rows = {}
    tta = ''
    with open(args.inf, 'r') as inf:
        header = inf.readline() # ignore
        lineno = 0
        while (lin := inf.readline()):
            print(f'lin: {lin}')
            if lineno == 10:
                tta = lin.strip()
            elif len(lin) > 1:
                row = {}
                row['cat'] = lin[0:7]
                row['met'] = lin[7:25]
                for c in range(0, 8):
                    row[c] = lin[25+6*c:25+6*c+5]
                rows[lineno] = row
            lineno += 1
    # print out a table
    header = '''\\begin{table}[H]
    \centering
    \\begin{tabular}{|l|l|r|r|r|r|r|r|r|r|}
    \hline
    \\rowcolor[HTML]{FFEEEE} \\textbf{Class} & \\textbf{Metric} & \multicolumn{8}{|c|}{\\textbf{Anticipation time}} \\\\
       & & \\textbf{2.00s} & \\textbf{1.75s} & \\textbf{1.50s} & \\textbf{1.25s} & \\textbf{1.00s} & \\textbf{0.75s} & \\textbf{0.50s} & \\textbf{0.25s} \\\\ \hline\n'''
    footer1 = '''    \hline
    \end{tabular}
    \caption{Validation results for '''
    footer2 = ''' \label{'''
    footerr = '''}}
\end{table}'''
    samplerow = '''     4 &         23.23  &         24.65  &          26.46 &          27.88 &          29.49 &          27.68 &         31.72  & \\textbf{33.33} \\\\'''
    with open(args.outf, 'w') as outf:
        outf.write(header)
        for idx, row in rows.items():
            print(idx, row)
            if idx > 0 and idx % 3 == 0:
                outf.write("    \hline\n")
            outf.write(f"    {row['cat']} & {row['met']}")
            for c in range(0, 8):
                outf.write(f" & {row[c]}")
            outf.write(" \\\\\n")
        outf.write(f"    \hline\n    \\rowcolor[HTML]{{FFEEFF}} \multicolumn{{10}}{{|l|}}{{{tta}}} \\\\\n")
        outf.write(footer1)
        outf.write(caption)
        outf.write(footer2)
        outf.write(label)
        outf.write(footerr)

if __name__ == '__main__':
    if args.fun == 'one_in_many':
        one_in_many()
    elif args.fun == 'subsample':
        subsample()
    elif args.fun == 'latex_table':
        make_latex_table_full(args.caption, args.label)
