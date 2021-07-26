# Import
import pandas as pd
from tqdm import tqdm, trange

import eikon as ek
ek.set_app_key('249fbcada92c44f7a1587816a282e4120b3fb4bb')

# -----------------------------------------
# Set parameters
'''
L is the length of each Eikon query.
Maximum is 7500, higher is faster.
However, too high can raise Error 408 - Timeout Exception.
Try 4000 or 5000 first.
'''
L = 2000

fields = [
    'TR.FIIssuerName',
    'TR.FIIssuerCountryName',
    'TR.FIIssueDate'
    'TR.RIC',
    'TR.RICCode',
    'TR.PreferredRIC'
    'TR.FIMaturityDate',
    'TR.FICurrency',
    'TR.FIDomicile',
    'TR.FIIndustrySubSectorDescription',
    'TR.GreenBondFlag',
    'TR.FIInflationProtected',
    'TR.FIIsHybrid',
    'TR.FISovereignClass'
]

address = 'C:\\Users\\Francesco\\Dropbox\\RA\\GovernmentBonds\\Datastream_Search\\Characteristics.xlsx'
colName = 'ISIN'

# -----------------------------------------

# codes
file = pd.read_excel(address)
codes = file[colName].tolist()

print("Data imported.")

# Set queries
num_codes = len(codes)
num_queries = num_codes // L # Returns floor
num_leftover = num_codes - num_queries*L

# Initialize list to append dataframes
dfList = []

# -----------------------------------------

# Loop queries

print("Starting first of {} queries.".format(num_queries))

for i in trange(num_queries):
    start = i * L
    end = (i+1) * L
    current_codes = codes[start:end]
    
    df_current, err = ek.get_data(current_codes, fields)
    dfList.append(df_current)

# Get residual data
if num_leftover > 0:
    current_codes = codes[-num_leftover:]
    df_current, err = ek.get_data(current_codes, fields)
    dfList.append(df_current)

# Concatenate, print, copy
final = pd.concat(dfList)
print(final)
final.to_clipboard(index = False, header = False)
