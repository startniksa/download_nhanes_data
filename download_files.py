# Using Python 3.7.9. for this one, 3.9.1 otherwise
# To add new columns, see where I've commented "newly added". Did it for Vitamin D.

# Download the files from CDC, merge them into one
from pathlib import Path
from functools import reduce
import pandas as pd
import requests
import xport

NHANES_BASE_URL = 'https://wwwn.cdc.gov/Nchs/Nhanes/'
NHANES_SUFFIX = '.XPT'

input_files = {
    '1999-2000': [
        'LAB25',
        'DEMO',
        'LAB13',
        'LAB18',
        'LAB06',
        'LAB13AM',
        'BMX',#newly added
    ],
    '2001-2002': [
        'L25_B',
        'L25_2_B',
        'DEMO_B',
        'L40_B',
        'L13AM_B',
        'L13_B',
        'L13_2_B',
        'L40_2_B',
        'L06_2_B',
        'L40FE_B',
        "VID_B",#newly added
        "BMX_B",#newly added
    ],
    '2003-2004': [
        'L25_C',
        'DEMO_C',
        'L40_C',
        'L13_C',
        'L06COT_C',
        'L06BMT_C',
        'L06TFR_C',
        'L13AM_C',
        'L40FE_C',
        "VID_C",#newly added
        "BMX_C",#newly added
    ],
    '2005-2006': [
        'CBC_D',
        'DEMO_D',
        'HDL_D',
        'BIOPRO_D',
        'FERTIN_D',
        'FETIB_D',
        'TCHOL_D',
        "VID_D",#newly added
        "BMX_D",#newly added
    ],
    '2007-2008': [
        'CBC_E',
        'DEMO_E',
        'BIOPRO_E',
        'HDL_E',
        'FERTIN_E',
        'TCHOL_E',
        "VID_E",#newly added
        "BMX_E",#newly added
    ],
    '2009-2010': [
        'CBC_F',
        'BIOPRO_F',
        'DEMO_F',
        'HDL_F',
        'FERTIN_F',
        'TCHOL_F',
        "VID_F",#newly added
        "BMX_F",#newly added
            ],
    '2011-2012': [
        'CBC_G',
        'DEMO_G',
        'HDL_G',
        'BIOPRO_G',
        'TCHOL_G',
        "VID_G",#newly added
        "BMX_G",#newly added
        ],
    '2013-2014': [
        'CBC_H',
        'DEMO_H',
        'HDL_H',
        'BIOPRO_H',
        'TCHOL_H',
        'TRIGLY_H',
        "VID_H",#newly added
        "BMX_H",#newly added
        ],
    '2015-2016': [
        'CBC_I',
        'DEMO_I',
        'HDL_I',
        'BIOPRO_I',
        'TCHOL_I',
        "VID_I",#newly added
        "BMX_I",#newly added
        ]
}

input_col_map = {
  'LBXMCHSI': 'MCH',
  'LBDLYMNO': 'Lymphs (Absolute)',
  'RIDAGEYR': 'PATIENT_AGE_YEARS',
  'LBXPLTSI': 'Platelets',
  'LBDMONO': 'Monocytes(Absolute)',
  'LBXSGB': 'Globulin, Total',
  'LBXRDW': 'RDW',
  #'LBXTR': 'Triglycerides',
  'LBXSTR': 'Triglycerides',
  #'LB2STR': 'Triglycerides',
  #'LB2TR': 'Triglycerides',
  'LBXFER': 'Ferritin, Serum',
  'LB2FER': 'Ferritin, Serum',
  'LBDFER': 'Ferritin, Serum',
  'LBXTIB': 'Iron Bind.Cap.(TIBC)',
  'LBDTIB': 'Iron Bind.Cap.(TIBC)',
  'LBDEONO': 'Eos (Absolute)',
  'LBDBANO': 'Baso (Absolute)',
  'LBXSAL': 'Albumin, Serum',
  'LBXSCR': 'Creatinine, Serum',
  'LBDSCR': 'Creatinine, Serum',
  'LBXSPH': 'Phosphorus, Serum',
  'LBDSPH': 'Phosphorus, Serum',
  'LBDNENO': 'Neutrophils (Absolute)',
  'LBXSGL': 'Glucose, Serum',
  'LBXTC': 'Cholesterol, Total',
  'LBXSIR': 'Iron, Serum',
  'LBXSCA': 'Calcium, Serum',
  'LBXSCLSI': 'Chloride, Serum',
  'LBXSLDSI': 'LDH',
  'LB2SLDSI': 'LDH',
  'LBXSBU': 'BUN (mg/dL)',
  'LBXSASSI': 'AST (SGOT)',
  'LBXSATSI': 'ALT (SGPT)',
  'LBXSTB': 'Bilirubin, Total',
  'LB2STB': 'Bilirubin, Total',
  'LBXSNASI': 'Sodium, Serum',
  'LBXSUA': 'Uric Acid, Serum',
  'LBXSAPSI': 'Alkaline Phosphatase, S',
  'LBDSAPSI':  'Alkaline Phosphatase, S',
  'LBXSGTSI': 'GGT',
  'LBXSC3SI': 'Carbon Dioxide, Total',
  'LBDHDD': 'HDL-C',
  'LBDHDL': 'HDL-C',
  'LBXHDD': 'HDL-C',
  'LBXHCT': 'Hematocrit',
  'LBXSKSI': 'Potassium, Serum',
  'LBXMC': 'MCHC',
  'LBXMCVSI': 'MCV',
  'RIAGENDR': 'PATIENT_GNDR',
  'LBXRBCSI': 'RBC',
  'LBXHGB': 'Hemoglobin',
  'LBDLDL': 'LDL-C',
  'LBXMPSI': 'MPV',
  "LB2VID": "Vitamin D (ng/mL)",#newly added
  "LBDVIDMS": "Vitamin D (nmol/L)",#newly added
  "LBXVD3MS": "Vitamin D3 (nmol/L)",#newly added
  "LBXWBCSI": "WBC",# White blood cell count, newly added
  "LBDSBUSI": "BUN (mmol/L)",#Blood urea nitrogen, newly added
  "LBDSUASI": "Uric acid (umol/L)",#newly added
  "BMXWT": "Weight (kg)",#newly added
  "BMXWAIST": "Waist Circumference (cm)",#newly added
  "BMXHT": "Standing Height (cm)",#newly added
}
included_markers = input_col_map.values()

output_col_map = {
    'YEAR': 'YEAR',
}

all_cols = set(output_col_map.keys()) | set(input_col_map.keys())

def get_fname(fname):
    return f'{fname}{NHANES_SUFFIX}'

def download(datadir, input_files=input_files):
    for (year, files) in input_files.items():
        for fname in files:
            fname = get_fname(fname)
            ofname = datadir / fname
            if ofname.exists():
                print(f'Skipping {ofname} (file exists)')
            else:
                url = f'{NHANES_BASE_URL}{year}/{fname}'
                print(f'Downloading {url} to {ofname}')
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    with open(ofname, 'wb') as f:
                        f.write(r.content)
                else:
                    raise FileNotFoundError(f'{url}')
    print('Done')

def get_df(datadir, fname, key):
    fname = get_fname(fname)
    print(fname)
    df = xport.to_dataframe(open(datadir / fname, 'rb'))
    df.set_index(key, inplace=True)
    df.drop(df.columns.difference(all_cols), axis=1, inplace=True)
    df.rename(columns={**input_col_map, **output_col_map}, inplace=True)
    return df

def join_input(datadir, year, key='SEQN'):
    dfs = [get_df(datadir, fname, key) for fname in input_files[year]]
    df = pd.concat(dfs, ignore_index=True, sort=False)
    df = reduce(lambda x, y: x.merge(y,
                                     left_index=True,
                                     right_index=True,
                                     how='outer',
                                     suffixes=('', '_y')),
				dfs)

    year = int(year.split('-')[0])
    df['YEAR'] = [year] * len(df)
    return df

def join_all(datadir):
    dfs = []
    included_markers = input_col_map.values()
    for year in sorted(input_files.keys(), reverse=False):
        df = join_input(datadir, year)
        dfs.append(df)
        print(f'Checking for missing columns in {year}... ', end='')
        diff = df.columns.symmetric_difference(included_markers).drop('YEAR')
        if len(diff) == 0:
            print('OK')
            continue
        print('\nMissing columns: {}'.format(', '.join([f'"{d}"' for d in diff])))
    print('Done')
    return pd.concat(dfs, ignore_index=True, sort=False)

# Name the place where data files will be downloaded from the CDC website
datadir = Path('./data')
# Create the folder if ti doesn't exist
Path(datadir).mkdir(parents=True, exist_ok=True)
# Name the file where the preprocessed data will be saved as one Pandas DataFrame
fname = 'nhanes.csv'

download(datadir)
df = join_all(datadir)
# Drop duplicate rows and rows with more than 15 null columns
df = df.dropna(thresh=15).drop_duplicates()
# PATIENT_GNDR == 0 women, 1 == men
df.PATIENT_GNDR = df.PATIENT_GNDR.replace({2: 0})
df.to_csv(fname)
