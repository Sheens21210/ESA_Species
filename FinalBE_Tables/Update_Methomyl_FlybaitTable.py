import pandas as pd
import datetime
import os

# new_list_df =new_list_df.loc[new_list_df['Fly bait Only'].isin(zones) == True]

plant_groups = ['Flowering Plants', 'Conifers and Cycads', 'Ferns and Allies', 'Lichens', 'Corals']

old_table_plants = 'L:\Workspace\ESA_Species\Step3\ToolDevelopment\TerrestrialGIS\Tabulated_NewComps\DraftBEs\Methomyl\Flybait\Terr_Plant_List of Species that Overlap with Developed CDL_fromPanger_20170131.csv'
old_table_animals = 'L:\Workspace\ESA_Species\Step3\ToolDevelopment\TerrestrialGIS\Tabulated_NewComps\DraftBEs\Methomyl\Flybait\Terr_Animal_List of Species that Overlap with Developed CDL_fromPanger_20170131.csv'

new_species_list = 'L:\Workspace\ESA_Species\Step3\ToolDevelopment\TerrestrialGIS\Tabulated_NewComps\DraftBEs\Methomyl\Overlap Tables\R_FinalBE_Methomyl_Overlap_20170202.csv'

outlocation = 'L:\Workspace\ESA_Species\Step3\ToolDevelopment\TerrestrialGIS\Tabulated_NewComps\DraftBEs\Methomyl\Flybait'
new_list_df = pd.read_csv(new_species_list)
old_plants_df = pd.read_csv(old_table_plants)
old_animals_df = pd.read_csv(old_table_animals)

final_col_order_anmials = old_animals_df.columns.values.tolist()
final_col_order_anmials.append('Fly bait Only')
final_col_order_plants = old_plants_df.columns.values.tolist()
final_col_order_plants.append('Fly bait Only')

old_plants_df['EntityID'] = old_plants_df['EntityID'].astype(str)
old_animals_df['EntityID'] = old_animals_df['EntityID'].astype(str)

new_list_df = new_list_df.loc[new_list_df['Fly bait Only'].isin(['Yes', 'Yes- Spray Drift Only'])]

new_plants = new_list_df.loc[new_list_df['Group'].isin(plant_groups) == True]
current_plant = new_plants['EntityID'].astype(str).values.tolist()
print current_plant
plants_nochange = old_plants_df.loc[old_plants_df['EntityID'].isin(current_plant) == True]

new_plants_change = new_plants.loc[new_plants['EntityID'].isin(current_plant) == True]
new_plants_info = new_plants_change[['EntityID', 'comname', 'sciname', 'Group','Fly bait Only']]
new_plants_info.columns = ['EntityID', 'Common Name', 'Scientific Name', 'Taxa','Fly bait Only']

new_animals = new_list_df.loc[new_list_df['Group'].isin(plant_groups) == False]
current_animals = new_animals['EntityID'].astype(str).values.tolist()
animals_nochange = old_animals_df.loc[old_animals_df['EntityID'].isin(current_animals) == True]

new_animals_change = new_animals.loc[new_animals['EntityID'].isin(current_animals) == True]
new_animals_info = new_animals_change[['EntityID', 'comname', 'sciname', 'Group','Fly bait Only']]
new_animals_info.columns = ['EntityID', 'Common Name', 'Scientific Name', 'Taxa','Fly bait Only']

out_plants = pd.concat([plants_nochange, new_plants_info], axis =0)
out_plants=out_plants.reindex(columns=final_col_order_plants,)
out_animals = pd.concat([animals_nochange, new_animals_info], axis =0)
out_animals=out_animals.reindex(columns=final_col_order_anmials)


out_animals.to_csv(outlocation + os.sep + 'TerrAnimal_Updated_20170202.csv')
out_plants.to_csv(outlocation + os.sep + 'TerrPlant_Updated_20170202.csv')
