import pandas as pd

datasets = {
    'cow_counters': {
        'type': 'simple',
        'steps': [
            #'''df = pd.read_csv('https://opendata.arcgis.com/datasets/a5e1adba2e5545a9b4f0a1d198cd0498_0.csv')''',
            '''df = pd.read_csv('EcoCounters.csv')''',
            '''df = df[['LOCATION', 'LONG', 'LAT', 'ID']]'''
        ],
        'df': None
    },
    'cok_counters': {
        'type': 'simple',
        'steps': [
            #'''df = pd.read_csv('https://app2.kitchener.ca/appdocs/opendata/staticdatasets/Trails_Counters_Pedestrians_Cyclists.csv')''',
            '''df = pd.read_csv('Trails_Counters_Pedestrians_Cyclists.csv')''',
            '''df = df.groupby(by=['STATION_LOCATION_DESCRIPTION', 'X_COORD_LL_DD', 'Y_COORD_LL_DD']).first().reset_index()[['STATION_LOCATION_DESCRIPTION', 'X_COORD_LL_DD', 'Y_COORD_LL_DD']]''',
            '''df = df.rename(columns={'STATION_LOCATION_DESCRIPTION': 'LOCATION', 'X_COORD_LL_DD': 'LONG', 'Y_COORD_LL_DD': 'LAT'})''',
            '''df['ID'] = df['LOCATION']''',
            '''df['LOCATION'] = df['LOCATION'].replace('CHERRY ST', 'Iron Horse/Trans Canada Trail at Cherry St. S.')''',
            '''df['LOCATION'] = df['LOCATION'].replace('BORDEN AVE S', 'Iron Horse/Trans Canada Trail at Borden St. S.')''',
            '''df['LOCATION'] = df['LOCATION'].replace('QUEEN ST S', 'Iron Horse/Trans Canada Trail at Queen St. S.')'''
        ]
    },
    'counters': {
        'type': 'composite',
        'steps': ['cow_counters', 'cok_counters']
    },
    'cow_counter_readings': {
        'type': 'simple',
        'steps': [
            #'''df = pd.read_csv('https://opendata.arcgis.com/datasets/5d41afff252e45b5b5fe7fc3fd5df3ab_0.csv')''',
            '''df = pd.read_csv('City_of_Waterloo_Trail_Counter_Data.csv')''',
            '''df['DATE'] = pd.to_datetime(df['DATE'], infer_datetime_format=True).dt.date''',
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
            '''df['DATE'] = pd.to_datetime(df['DATE'], infer_datetime_format=True).dt.date''',
            '''df = df[['LOC_ID', 'DATE', 'TOTAL_COUNT', 'PEDESTRIAN_TOTAL', 'CYCLIST_TOTAL']]''',
            '''df = df.groupby(by=['LOC_ID', 'DATE']).sum().reset_index()'''
        ]
    },
    'counter_readings': {
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
    return pd.concat(df_list).reset_index(drop=True)

def get_data(dataset_key):
    if datasets[dataset_key]['type'] == 'composite':
        return composite_process(dataset_key)
    elif datasets[dataset_key]['type'] == 'simple':
        return simple_process(dataset_key)

def get_cycling_infrstructure():
    cow_df = pd.read_csv()


       
