import pandas as pd

def get_counter_data(source='local'):
    if source == 'local':
        #COW data
        cow_counter_info = pd.read_csv('EcoCounters.csv')
        cow_counter_readings = pd.read_csv('City_of_Waterloo_Trail_Counter_Data.csv')
        #COK data
        cok_counter_readings = pd.read_csv('Trails_Counters_Pedestrians_Cyclists.csv')

    elif source == 'remote':
        #COW data
        cow_counter_info = pd.read_csv('https://opendata.arcgis.com/datasets/a5e1adba2e5545a9b4f0a1d198cd0498_0.csv')
        cow_counter_readings = pd.read_csv('https://opendata.arcgis.com/datasets/5d41afff252e45b5b5fe7fc3fd5df3ab_0.csv')
        #COK data
        cok_counter_readings = pd.read_csv('https://app2.kitchener.ca/appdocs/opendata/staticdatasets/Trails_Counters_Pedestrians_Cyclists.csv')
    print('I made it here quickly. FNF')
    cok_counter_info = cok_counter_readings.groupby(by=['STATION_LOCATION_DESCRIPTION', 'X_COORD_LL_DD', 'Y_COORD_LL_DD']).first().reset_index()[['STATION_LOCATION_DESCRIPTION', 'X_COORD_LL_DD', 'Y_COORD_LL_DD']]
    cok_counter_info = cok_counter_info.rename(columns={'STATION_LOCATION_DESCRIPTION': 'LOCATION', 'X_COORD_LL_DD': 'LONG', 'Y_COORD_LL_DD': 'LAT'})
    print('I made it here quickly. HFV')
    cok_counter_info['ID'] = cok_counter_info['LOCATION']
    cok_counter_info['LOCATION'] = cok_counter_info['LOCATION'].replace('CHERRY ST', 'Iron Horse/Trans Canada Trail at Cherry St. S.')
    cok_counter_info['LOCATION'] = cok_counter_info['LOCATION'].replace('BORDEN AVE S', 'Iron Horse/Trans Canada Trail at Borden St. S.')
    cok_counter_info['LOCATION'] = cok_counter_info['LOCATION'].replace('QUEEN ST S', 'Iron Horse/Trans Canada Trail at Queen St. S.')
    print('I made it here quickly. BUJ')
    cow_counter_info = cow_counter_info[['LOCATION', 'LONG', 'LAT', 'ID']]
    print('I made it here quickly. EDT')
    counter_info = pd.concat([cow_counter_info, cok_counter_info]).reset_index(drop=True)
    print('I made it here quickly. JKY')
    cok_counter_readings = cok_counter_readings.rename(columns={'DATE_TIME': 'DATE', 'STATION_LOCATION_DESCRIPTION': 'LOC_ID', 'PEDESTRIANS': 'PEDESTRIAN_TOTAL', 'CYCLISTS': 'CYCLIST_TOTAL', 'TOTAL': 'TOTAL_COUNT',})
    print('I made it here quickly. SKV')
    cok_counter_readings['DATE'] = pd.to_datetime(cok_counter_readings['DATE'], infer_datetime_format=True).dt.date
    cow_counter_readings['DATE'] = pd.to_datetime(cow_counter_readings['DATE'], infer_datetime_format=True).dt.date
    print('I made it here quickly. GFB')
    cok_counter_readings = cok_counter_readings[['LOC_ID', 'DATE', 'TOTAL_COUNT', 'PEDESTRIAN_TOTAL', 'CYCLIST_TOTAL']]
    
    cow_counter_readings = cow_counter_readings[['LOC_ID', 'DATE', 'TOTAL_COUNT', 'PEDESTRIAN_TOTAL', 'CYCLIST_TOTAL']]

    counter_readings = pd.concat([cok_counter_readings, cow_counter_readings])
    #counter_readings['DATE'] = pd.to_datetime(counter_readings['DATE']).dt.date
    counter_readings = counter_readings.groupby(by=['LOC_ID', 'DATE']).sum().reset_index()
    
    return counter_readings, counter_info

if __name__ == '__main__':
    counter_readings, counter_info = get_counter_data()