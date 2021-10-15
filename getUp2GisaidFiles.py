import pandas as pd
from datetime import datetime

# load origin lab datagrame

prog_lab_df = pd.read_csv('./example/orig_labs.csv')
to_submit_df = pd.read_csv(
    '/HDD/Projects/tables_IAM/14-10-2021_to_submit.csv')

cte_vals_path = './example/constantValues.val'

# --- FUNCTIONS ---------------------------------------------------------------


def load_cte_values(val_path):
    dct = {}
    val_fl = open(val_path, 'r')
    for line in val_fl:
        if line.startswith('#'):
            continue
        else:
            ln_data = line.split('=')
            if len(ln_data) < 2:
                continue
            dct[ln_data[0].replace(' ', '')] = ln_data[1].replace('\n', '')
    return dct

# location


def get_location_col(row):
    cte_loc = 'South America/Brazil/'
    # location
    state = row['estado']
    city = row['municipio']
    return cte_loc+state+'/'+city

# virus name


def get_viral_name(row):
    '''
    get viral name string using a model string
    '''
    col_char = False
    viral_name = ''
    vn_model = 'hCoV-19/Brazil/<UF>-FIOCRUZ-<cod_iam>/<ano>'
    # vn model is defined on the previous cell
    for char in vn_model:
        if char == '<':
            col = ''
            col_char = True
            continue
        if char == '>':
            # get col
            viral_name += str(row[col])
            col_char = False
            continue
        if col_char is True:
            col += char
            continue
        viral_name += char
    return viral_name

# constant values


def add_cte_cols(df, value):
    '''
    get a columns with constant values
    '''
    def f(row):
        return value

    return df.apply(f, axis=1)


def get_gisaid_cols(row):
    # collection date
    # cov_gender
    # cov_patient_age
    # covv_coverage
    return row[['collection_date', 'Genero', 'idade', 'coverage']]

# get ori lab info
# covv_orig_lab


def get_ori_lab(row):
    '''
    get origin lab informations
    '''
    olab = prog_lab_df.loc[prog_lab_df['UF'] == row['UF']]
    # if PE, then can be NUPIT or LACEN
    if len(olab) == 2:
        if row['cod_iam'].startswith('AMU'):
            sel_lab = 'NUPIT/UFPE'
        else:
            sel_lab = 'LACEN/PE'

    # if another state, then assume is LACEN from that state
    if len(olab) == 1:
        sel_lab = 'LACEN/'+row['UF']
        if row['UF'] == 'SP':
            sel_lan = 'LACEN/PE'

    # if no orig lab found, raise error
    if len(olab) == 0:
        print(row)
        raise Exception('NO ORI LAB FOUND FOR ', row['UF'])

    return sel_lab


def get_ori_lab_add(row):
    sel_lab = row['covv_orig_lab']
    #print(row.index, ' ',sel_lab)
    orig_lab_addr = prog_lab_df.loc[prog_lab_df['orig_lab']
                                    == sel_lab]['orig_lab_addr'].values[0]
    return orig_lab_addr


def get_ori_lab_authors(row):
    sel_lab = row['covv_orig_lab']
    return prog_lab_df.loc[prog_lab_df['orig_lab'] == sel_lab]['cov_authors'].values[0]


# -----------------------------------------------------------------------------
cte_dct = load_cte_values(cte_vals_path)
# get values
submitter = cte_dct['submitter']
covv_type = cte_dct['covv_type']
covv_add_location = cte_dct['covv_add_location']
covv_passage = cte_dct['covv_passage']  # 'Original'
covv_host = cte_dct['covv_host']  # 'Human'
covv_add_host_info = cte_dct['covv_add_host_info']  # 'unknown'
covv_sampling_strategy = cte_dct['covv_sampling_strategy']  # 'unknown'
covv_patient_status = cte_dct['covv_patient_status']  # 'unknown'
covv_specimen = cte_dct['covv_specimen']  # 'unknown'
covv_outbreak = cte_dct['covv_outbreak']  # 'unknown'
covv_last_vaccinated = cte_dct['covv_last_vaccinated']  # 'unknown'
covv_treatment = cte_dct['covv_treatment']  # 'unknown'
covv_provider_sample_id = cte_dct['covv_provider_sample_id']  # 'unknown'
# 'WallauLab on behalf of Fiocruz COVID-19 Genomic Surveillance Network'
covv_subm_lab = cte_dct['covv_subm_lab']
# 'Campus da UFPE - Av. Prof. Moraes Rego, s/n - Cidade Universitária, Recife – PE'
covv_subm_lab_addr = cte_dct['covv_subm_lab_addr']
covv_sbm_sample_id = cte_dct['covv_sbm_sample_id']  # 'unknow'
covv_authors = cte_dct['covv_authors']
covv_comment = cte_dct['covv_comment']
comment_type = cte_dct['comment_type']

# cov_assembly method (viralflow)
covv_assembly_method = cte_dct['covv_assembly_method']  # 'ViralFlow v.0.0.5'
# cov_seq_technology
covv_seq_technology = cte_dct['covv_seq_technology']  # 'Illumina Miseq'
# fn (FASTA filename)
fn = cte_dct['fn']  # 'myFastaFile.fa'

# Mount csv sequences

gisaid_df = pd.DataFrame([])

# get constant values columns

gisaid_df['submitter'] = add_cte_cols(to_submit_df, submitter)

gisaid_df['covv_type'] = add_cte_cols(to_submit_df, covv_type)

gisaid_df['covv_add_location'] = add_cte_cols(to_submit_df, covv_add_location)

gisaid_df['covv_host'] = add_cte_cols(to_submit_df, covv_host)

gisaid_df['covv_add_host_info'] = add_cte_cols(
    to_submit_df, covv_add_host_info)

gisaid_df['covv_passage'] = add_cte_cols(to_submit_df, covv_passage)

gisaid_df['covv_sampling_strategy'] = add_cte_cols(
    to_submit_df, covv_sampling_strategy)

gisaid_df['covv_patient_status'] = add_cte_cols(
    to_submit_df, covv_patient_status)

gisaid_df['covv_specimen'] = add_cte_cols(to_submit_df, covv_specimen)

gisaid_df['covv_outbreak'] = add_cte_cols(to_submit_df, covv_outbreak)

gisaid_df['covv_last_vaccinated'] = add_cte_cols(
    to_submit_df, covv_last_vaccinated)

gisaid_df['covv_treatment'] = add_cte_cols(to_submit_df, covv_treatment)

gisaid_df['covv_provider_sample_id'] = add_cte_cols(
    to_submit_df, covv_provider_sample_id)

gisaid_df['covv_subm_lab'] = add_cte_cols(to_submit_df, covv_subm_lab)

gisaid_df['covv_subm_lab_addr'] = add_cte_cols(
    to_submit_df, covv_subm_lab_addr)

gisaid_df['covv_sbm_sample_id'] = add_cte_cols(
    to_submit_df, covv_sbm_sample_id)

gisaid_df['covv_authors'] = add_cte_cols(to_submit_df, covv_authors)

gisaid_df['covv_comment'] = add_cte_cols(to_submit_df, covv_comment)

gisaid_df['covv_type'] = add_cte_cols(to_submit_df, covv_type)

gisaid_df['covv_assembly_method'] = add_cte_cols(
    to_submit_df, covv_assembly_method)

# cov_seq_technology
gisaid_df['covv_seq_technology'] = add_cte_cols(
    to_submit_df, covv_seq_technology)

# fn (FASTA filename)
fn = 'myFastaFile.fa'
gisaid_df['fn'] = add_cte_cols(to_submit_df, fn)


# get sample specific columns
new_cols = ['collection_date', 'covv_gender',
            'covv_patient age', 'covv_coverage']
gisaid_df[new_cols] = to_submit_df.apply(get_gisaid_cols, axis=1)

# covv_orig_lab cols
# covv_orig_lab
# return covv_orig_lab, covv_orig_lab_addr and covv_authors
gisaid_df['covv_orig_lab'] = to_submit_df.apply(get_ori_lab, axis=1)
gisaid_df['covv_orig_lab_addr'] = gisaid_df.apply(get_ori_lab_add, axis=1)
gisaid_df['covv_authors'] = gisaid_df.apply(get_ori_lab_authors, axis=1)

gisaid_df['covv_virus_name'] = to_submit_df.apply(get_viral_name, axis=1)

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y")
outName = dt_string+'_IAMsequences.csv'
gisaid_df.to_csv(outName)
