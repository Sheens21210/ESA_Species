import pandas as pd

in_table = r'C:\Users\JConno02\Documents\Projects\ESA\Bins\updates\Update_Jan2016_FishesError\Recode_BinTable_asof_20170106.csv'
out_table = r'C:\Users\JConno02\Documents\Projects\ESA\Bins\updates\Update_Jan2016_FishesError\LongBins_20170110.csv'
in_df = pd.read_csv(in_table)
print in_df.columns.values.tolist()
# in_df.drop('Unnamed: 0',axis=1,inplace=True)
# in_df.drop('Terrestrial Bin',axis=1, inplace=True)

long_df = pd.melt(in_df, id_vars=['ENTITYID', 'HUC_2', 'Lead_Agency', 'Group', 'COMNAME', 'SCINAME', 'STATUS_TEXT',
                                  'Multi HUC', 'AttachID', 'Reassigned','sur_huc','Bins_reassigned'],
                  value_vars=['Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6', 'Bin 7', 'Bin 8', 'Bin 9',
                              'Bin 10'],
                  var_name='Bins', value_name='Value')
print long_df

out_col = ['Lead_Agency',
           'Group',
           'HUC_2',
           'COMNAME',
           'ENTITYID',
           'SCINAME',
           'STATUS_TEXT',
           'Multi HUC',
           'Reassigned',
           'sur_huc',
           'Bins_reassigned',
           'AttachID',
           'Bins',
           'Value',
           'WoE_group_1',
           'WoE_group_2'
           ]

long_df = long_df.reindex(columns=out_col)
long_df.to_csv(out_table)
