# Import
import pandas as pd
from tqdm import tqdm, trange

import eikon as ek
ek.set_app_key('0ab94a053c8a4fffb38f75b1de2bcd7ebd9654f3')

# -------------------------------------------------------------------------------
# Set parameters
'''
L is the length of each Eikon query.
Maximum is 7500, higher is faster.
However, too high can raise Error 408 - Timeout Exception.
Try 4000 or 5000 first.
'''
L = 7000

fields = [
    # Issuer information
    'TR.FIIssuerName',
    'TR.FIIssuerCountryName',
    'TR.FIDomicile',
    'TR.FIIndustrySubSectorDescription',
    'TR.FIIndustrySectorDescription',
    # Identifiers
    'TR.LegalEntityIdentifier',
    'TR.AssetIDCode',
    'TR.BondISIN',
    'TR.BondRIC',
    'TR.RIC',
    'TR.RICCode',
    'TR.PreferredRIC'
    # Characteristics
    'TR.AssetCategory',
    'TR.FICouponFrequency',
    'TR.FICouponType',
    'TR.FIDebtType',
    'TR.FIIssueDate'
    'TR.FIMaturityDate',
    'TR.FICurrency',
    'TR.GreenBondFlag',
    'TR.FIIsCallable',
    'TR.FIIsConvertible',
    'TR.FIIsPerpetualSecurity',
    'TR.FIInflationProtected',
    'TR.FIIsHybrid',
    'TR.FISovereignClass'
]

address = 'https://www.dropbox.com/s/navn63y8r4xy1bo/allcusips.csv?dl=1'
colName = 'CUSIP'

# -------------------------------------------------------------------------------

# codes
file = pd.read_csv(address, sep = ',')
codes = file[colName].tolist()

print("Data imported.")

# Set queries
num_codes = len(codes)
num_queries = num_codes // L # Returns floor
num_leftover = num_codes - num_queries*L

# Initialize list to append dataframes
dfList = []

# -------------------------------------------------------------------------------

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

# Concatenate
final = pd.concat(dfList)
print(final)
