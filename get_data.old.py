import pandas as pd

#get COW data - make sure to parse the date
cow_df = pd.read_csv('https://opendata.arcgis.com/datasets/416741dbcb40451899b84ca7e10a80ee_0.csv', parse_dates=['INSTALLDATE'])
#rename the date column because we are going to use this later
cow_df = cow_df.rename(columns={'INSTALLDATE': 'install_date', 'ASSET_TYPE': 'type', 'OWNER': 'owner'})
cow_df['length_km'] = cow_df['LENGTH_M'] / 1000
#create a year column for grouping later
cow_df['install_year'] = cow_df['install_date'].dt.year
#create a month column for grouping later
cow_df['install_month'] = cow_df['install_date'].dt.month
#group by year
grouped_cow_df = cow_df.groupby(by=['install_year', 'owner', 'type']).sum()['length_km'].reset_index()
grouped_cow_df = grouped_cow_df.loc[grouped_cow_df['owner'] == 'City of Waterloo']

#get COK data - no need to parse the date
cok_df = pd.read_csv('https://opendata.arcgis.com/datasets/18817096d9ee49cca89f6a0d6092c2e7_0.csv')
#rename the year column because we are going to use this later
cok_df = cok_df.rename(columns={'INSTALLATION_YEAR': 'install_year', 'SUBCATEGORY': 'type', 'OWNERSHIP': 'owner'})
cok_df['length_km'] = cok_df['Shape__Length'] / 1000
#group by year
grouped_cok_df = cok_df.groupby(by=['install_year', 'owner', 'type']).sum()['length_km'].reset_index()
grouped_cok_df = grouped_cok_df.loc[grouped_cok_df['owner'] == 'KITCHENER']
grouped_cok_df['owner'] = 'City of Kitchener'

df = pd.concat([grouped_cok_df, grouped_cow_df]).reset_index(drop=True)

