import pandas as pd

datasets = {
    'cow_counters': {
        'type': 'simple',
        'steps': [
            '''df = pd.read_csv('https://opendata.arcgis.com/datasets/a5e1adba2e5545a9b4f0a1d198cd0498_0.csv')''',
            #'''df = pd.read_csv('EcoCounters.csv')''',
            '''df = df[['LOCATION', 'LONG', 'LAT', 'ID']]''',
            '''df['LOCATION'] = df['LOCATION'].replace('Laurel/Trans Canada Trail at Bearinger Rd', 'Laurel Trail at Bearinger Rd.')''',
            '''df['LOCATION'] = df['LOCATION'].replace('Laurel/Trans Canada Trail at Columbia St. W.', 'Laurel Trail at Columbia St. W.')''',
            '''df['LOCATION'] = df['LOCATION'].replace('Trans Canada/Laurel Trail at Silver Lake Bridge', 'Laurel Trail at Silver Lake Bridge')''',
            '''df['SOURCE'] = "City of Waterloo"'''
        ],
        'df': None
    },
    'cok_counters': {
        'type': 'simple',
        'steps': [
            '''df = pd.read_csv('https://app2.kitchener.ca/appdocs/opendata/staticdatasets/Trails_Counters_Pedestrians_Cyclists.csv')''',
            #'''df = pd.read_csv('Trails_Counters_Pedestrians_Cyclists.csv')''',
            '''df = df.groupby(by=['STATION_LOCATION_DESCRIPTION', 'X_COORD_LL_DD', 'Y_COORD_LL_DD']).first().reset_index()[['STATION_LOCATION_DESCRIPTION', 'X_COORD_LL_DD', 'Y_COORD_LL_DD']]''',
            '''df = df.rename(columns={'STATION_LOCATION_DESCRIPTION': 'LOCATION', 'X_COORD_LL_DD': 'LONG', 'Y_COORD_LL_DD': 'LAT'})''',
            '''df['ID'] = df['LOCATION']''',
            '''df['LOCATION'] = df['LOCATION'].replace('CHERRY ST', 'Iron Horse Trail at Cherry St. S.')''',
            '''df['LOCATION'] = df['LOCATION'].replace('BORDEN AVE S', 'Iron Horse Trail at Borden St. S.')''',
            '''df['LOCATION'] = df['LOCATION'].replace('QUEEN ST S', 'Iron Horse Trail at Queen St. S.')''',
            '''df['SOURCE'] = "City of Kitchener"'''
        ]
    },
    'trail_counter_info': {
        'type': 'composite',
        'steps': ['cow_counters', 'cok_counters']
    },
    'cow_counter_readings': {
        'type': 'simple',
        'steps': [
            #'''df = pd.read_csv('https://opendata.arcgis.com/datasets/5d41afff252e45b5b5fe7fc3fd5df3ab_0.csv')''',
            '''df = pd.read_csv('City_of_Waterloo_Trail_Counter_Data.csv')''',
            '''df['DATE'] = df['DATE'].str.replace('T',' ')''',
            '''df['DATE'] = df['DATE'].str.replace(':00.000Z','')''',
            #'''df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d %H:%M').dt.round('H')''',
            '''df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d %H:%M')''',
            '''df = df[['LOC_ID', 'DATE', 'TOTAL_COUNT', 'PEDESTRIAN_TOTAL', 'CYCLIST_TOTAL']]''',
            '''df = df.groupby(by=['LOC_ID', 'DATE']).sum().reset_index()'''

        ]
    },
    'cok_counter_readings': {
        'type': 'simple',
        'steps': [
            #'''df = pd.read_csv('https://app2.kitchener.ca/appdocs/opendata/staticdatasets/Trails_Counters_Pedestrians_Cyclists.csv')''',
            '''df = pd.read_csv('Trails_Counters_Pedestrians_Cyclists.csv')''',
            '''df = df.rename(columns={'DATE_TIME': 'DATE', 'STATION_LOCATION_DESCRIPTION': 'LOC_ID', 'PEDESTRIANS': 'PEDESTRIAN_TOTAL', 'CYCLISTS': 'CYCLIST_TOTAL', 'TOTAL': 'TOTAL_COUNT',})''',
            #'''df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y T%H:%M').dt.round('H')''',
            '''df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y T%H:%M')''',
            '''df = df[['LOC_ID', 'DATE', 'TOTAL_COUNT', 'PEDESTRIAN_TOTAL', 'CYCLIST_TOTAL']]''',
            '''df = df.groupby(by=['LOC_ID', 'DATE']).sum().reset_index()'''
        ]
    },
    'trail_counter_readings': {
        'type': 'composite',
        'steps': ['cok_counter_readings', 'cow_counter_readings']
    },
    'cycling_infrastructure': {
        'df': ''
    }
}

d = dict(locals())

def simple_process(dataset_key):        
    for step in datasets[dataset_key]['steps']:
        exec(step, d, d)
    return d['df']

def composite_process(dataset_key):
    df_list = []
    for sub_dataset in datasets[dataset_key]['steps']:
        df_list.append(simple_process(sub_dataset))
    df = pd.concat(df_list)
    if dataset_key == 'trail_counter_readings':
        df = df.reset_index(drop=True)
        df_list = []
        for location in df['LOC_ID'].unique():
            temp_df = df.loc[df['LOC_ID'] == location].resample('15T', on='DATE').mean()
            temp_df = temp_df.interpolate(method='linear', limit_direction='forward', axis=0)
            temp_df['LOC_ID'] = location
            df_list.append(temp_df)
        df = pd.concat(df_list)
        df = df.reset_index(drop=False)
    elif dataset_key == 'trail_counter_info':
        df = df.reset_index(drop=True)
        df = df.sort_values(by='LOCATION')
    print(df)
    return df

def get_data(dataset_key):
    if datasets[dataset_key]['type'] == 'composite':
        return composite_process(dataset_key)
    elif datasets[dataset_key]['type'] == 'simple':
        return simple_process(dataset_key)




       
