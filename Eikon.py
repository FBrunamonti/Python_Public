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
L = 1000

address = 'C:\\Users\\Francesco\\Dropbox\\RA\\GovernmentBonds\\Datastream_Search\\Yields_Missing.xlsx'
colName = 'MainSuperRIC'

# -----------------------------------------

# Codes
file = pd.read_excel(address)
codes = file[colName].tolist()
codes = [i for i in codes if str(i) != "nan"]

print("Data imported.")

# Set queries
num_codes = len(codes)
num_queries = num_codes // L # Returns floor
num_leftover = num_codes - num_queries*L

# Initialize list to append dataframes
dfList = []

# -----------------------------------------

# Loop queries
for i in trange(num_queries):
    start = i * L
    end = (i+1) * L
    current_codes = codes[start:end]
    
    try:
        df_current = ek.get_timeseries(
            current_codes,
            fields = ["CLOSE"],
            normalize = True,
            start_date = "1900-01-01",
            end_date = "2021-07-07",
            interval = "monthly"
        )
        dfList.append(df_current)
    except:
        pass

# Get residual data
if num_leftover > 0:
    current_codes = codes[-num_leftover:]
    df_current = ek.get_timeseries(
        current_codes,
        fields = ["CLOSE"],
        normalize = True,
        start_date = "1900-01-01",
        end_date = "2021-07-07",
        interval = "monthly"
    )
    dfList.append(df_current)

# Concatenate, print, copy
final = pd.concat(dfList)
print(final)
final.to_clipboard(index = False, header = True)
