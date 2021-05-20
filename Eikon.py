# Import
import pandas as pd
import time

import eikon as ek
ek.set_app_key('249fbcada92c44f7a1587816a282e4120b3fb4bb')

# -----------------------------------------
# Set parameters
'''
L is the length of each Eikon query.
Maximum is 7500, higher is faster.
However, too high can raise Error 408 - Timeout Exception.
'''
L = 4000

fields = [
    'CF_NAME',
    'TR.CommonName',
    'TR.CUSIPExtended',
    'TR.SEDOL',
    'TR.CIKNUMBER',
    'TR.RIC',
    'TR.ISIN'
]

address = 'E:\\Geographic_Revenues\\security_isin_subset.xlsx'

# -----------------------------------------

# RICs
file = pd.read_excel(address)
rics = file['RIC'].tolist() # Required for 

print("Data imported.")

# Set queries
num_rics = len(rics)
num_queries = num_rics // L # Returns floor
num_leftover = num_rics - num_queries*L

# Initialize df
df = pd.DataFrame()
df_list = [df]

# -----------------------------------------

# Get data with loop
print("Starting first query.")

for i in range(num_queries):
    time_start = time.time()
    
    start = i * L
    end = (i+1) * L
    current_rics = rics[start:end]
    
    df_current, er = ek.get_data(current_rics, fields)
    df_list.append(df_current)
    
    time_end = time.time()
    time_total = time_end - time_start
    time_total = round(time_total, 1)
    print("Iterations completed: {} out of {}. Seconds: {}".format(i+1, num_queries, time_total))

# Get residual data
current_rics = rics[-num_leftover:]
df_current, er = ek.get_data(current_rics, fields)
df_list.append(df_current)

# Concatenate, print, copy
final = pd.concat(df_list)
print(final)
final.to_clipboard(index = False)
