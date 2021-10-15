import pandas as pd
import argparse
from datetime import datetime

# --- FUNCTIONS ---------------------------------------------------------------


def get_year_col(row):
    '''
    get a column containing only the year
    '''
    # NOTE: it is necessary for gisaid viral name columns

    try:
        data = [int(x) for x in row['data-seq'].split('/')]
        assert(len(data) == 3)
    except(AssertionError):
        print('missing value at ', row.name, ' | ', row['data-seq'], ' |')

    except(ValueError):
        return False

    for i in data:
        # REMOVE THIS!!! GAMBIARRA
        if i == 201:
            i = 2021
        ###############
        if i >= 1900:
            return int(i)
    raise Exception('No year data for '+row['cod_iam']+'('+row['data-seq']+')')


# virus name
VN_MODEL = 'hCoV-19/Brazil/<UF>-FIOCRUZ-<cod_iam>/<ano>'


def get_viral_name(row):
    '''
    get viral name string using a model string
    '''
    col_char = False
    viral_name = ''
    # vn model is defined on the previous cell
    for char in VN_MODEL:
        if char == '<':
            col = ''
            col_char = True
            continue
        if char == '>':
            # get col
            viral_name += str(row[col])
            col_char = False
            continue
        if col_char == True:
            col += char
            continue
        viral_name += char
    return viral_name


# -----------------------------------------------------------------------------
# --- INPUT PROCESSING --------------------------------------------------------
dsc = '''
Get a sub dataframe containing only ready to submit sequences from THE TABELAO.
'''


parser = argparse.ArgumentParser(description=dsc)
parser.add_argument('tabelao', type=str, help='path of THE TABELAO file')
parser.add_argument('--outName', default=None, type=str,
                    help='path for output csv (default = <date>_to_submit.csv)')

args = parser.parse_args()

# -----------------------------------------------------------------------------
print(' Fiocruz Genomic Surveillance Engine :: Gisaid submition module')
print(' v.0.0.1 : Prototype')
print('                     APP: getSubmitDF')
print(' ---------------------------------------------------------------------')

# load original source
print('@ loading THE TABELAO [', args.tabelao, ']...')
# TODO: add sanity check
tabelao = pd.read_csv(args.tabelao)

print('@ filtering only ready for submitions...')
# get sequence ids to submit
to_submit_df = tabelao.loc[tabelao['submissao gisaid']
                           == 'pronto para submissao']

print("@ generating 'ano' and 'viral_name' columns")
to_submit_df.loc[:, ('ano')] = to_submit_df.apply(get_year_col, axis=1)
to_submit_df['viral_name'] = to_submit_df.apply(get_viral_name, axis=1)

print('@ writing output...')
if args.outName is None:
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y")
    outName = dt_string+'_to_submit.csv'
else:
    outName = args.outName

to_submit_df.to_csv(outName)
print(':: DONE ::')
