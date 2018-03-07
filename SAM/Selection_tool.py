import sys
import os
import datetime

import pandas as pd

##TODO what columns are needed for PWC
## TODO if the there is missing data in any of the columns should the row be excluded
## TODO Set up NHD regions loop - do we want to do one at a time or all at the same time

qa_table = r'C:\Users\JConno02\OneDrive - Environmental Protection Agency (EPA)\Documents_C_drive\Projects\SAM\ScenarioInputs_par_20171004.csv'
matrix_table = r'C:\Users\JConno02\OneDrive - Environmental Protection Agency (EPA)\Documents_C_drive\Projects\SAM\scenarios_fromP\IA_scenarios_agg_101217.txt'
outlocation = r''
random_sample_size = 100

# TODO check the crop lookups to SAM table; possible replace this with that table
useLookup = {10: 'Corn',
             20: 'Cotton',
             22: 'Drum Wheat',
             23: 'Spring Wheat',
             24: 'Winter Wheat',
             30: 'Rice',
             40: 'Soybeans',
             60: 'Vegetables and Ground Fruit',
             70: 'Other Orchards',
             71: 'Grapes',
             72: 'Citrus',
             75: 'Other Trees',
             80: 'Other Grains',
             90: 'Other RowCrops',
             100: 'Other Crops',
             110: 'Pasture'
             }


def filter_table (table, value, col):
    key = [k for k, v in useLookup.iteritems() if v == value][0]
    filter_df = table.loc[(table[col] == key)].copy()
    sample = filter_df.sample(n=random_sample_size)
    return sample



input_df = pd.read_csv(qa_table)
data_df = pd.read_table(matrix_table , sep=',')
data_df['cdl'] = (data_df['cdl']).map (lambda x:x).astype(int)
list_cdl = list(set(data_df['cdl'].values.tolist()))
filtered_dict = {k:v for k,v in useLookup.items() if k in list_cdl}

possAnswer = filtered_dict.values()
askQ = True

while askQ:
    print 'Crops to select from {0}'.format(sorted(filtered_dict.values()))
    user_input = raw_input('What crop would you like to look at: ')
    if user_input not in possAnswer:
        print 'This is not a valid answer'
    else:
        break

ran_sample = filter_table(data_df,user_input,'cdl')
print ran_sample
ran_sample.to_csv(outlocation +os.sep+'random_sample.csv')
print 'Random sample can be found at {0}'.format(outlocation +os.sep+'random_sample.csv')