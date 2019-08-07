from dash.dependencies import Input, Output

from app import app
import pandas as pd
import data_processor
import plotly.graph_objs as go

debug = True

def debug_print(statement):
    if debug:
        print(statement)

debug_print('Loading trail counter readings...')
trail_counter_readings_df = data_processor.get_data('trail_counter_readings')
debug_print('Loading trail counter info...')
trail_counter_info_df = data_processor.get_data('trail_counter_info')

def list_for_dropdown(df):
    dropdown_options = []
    for index, row in df.iterrows():
        option = {'label': row['LOCATION'], 'value': row['ID']}
        dropdown_options.append(option)
    return dropdown_options

def name_lookup(df, id, key_field, name_field):
    return df.loc[df[key_field] == id][name_field].values[0]

@app.callback(
    [Output('traffic_graph', 'figure'),
    Output('traffic_summary', 'figure'),
    Output('traffic_by_year_summary', 'figure')],
    [Input('counter_combo', 'value'),
    Input('traffic_type_radio', 'value'),
    Input('legend_radio', 'value'),
    Input('aggregate_type_checklist', 'value'),
    Input('resolution', 'value')
    ])

def update_graph(combo_choices, traffic_type, legend_radio, agg_type, resolution):
    if legend_radio == 'Show':
        legend_radio_value = True
    elif legend_radio == 'Hide':
        legend_radio_value = False
    filtered_df = trail_counter_readings_df.loc[trail_counter_readings_df['LOC_ID'].isin(combo_choices)]
    local_df = filtered_df
    df_list = []
    for location in local_df['LOC_ID'].unique():
        print(location)
        temp_df = local_df.loc[local_df['LOC_ID'] == location].resample(resolution, on='DATE').sum()
        
        #temp_df = temp_df.interpolate(method='linear', limit_direction='forward', axis=0)
        temp_df['LOC_ID'] = location
        print(temp_df)
        df_list.append(temp_df)
    
    local_df = pd.concat(df_list)
    print(local_df)


    local_df = local_df.reset_index(drop=False)
    print(local_df)
    filtered_df = local_df
    test_df = local_df.copy(deep=True)
    test_df['YEAR'] = test_df['DATE'].dt.year
    test_df = test_df.groupby(by=['LOC_ID', 'YEAR']).sum().reset_index()
    graph_data_dict = []
    traffic_by_year_summary_dict = []
    for choice in combo_choices:
        temp_dict = {'x': filtered_df.loc[filtered_df['LOC_ID'] == choice]['DATE'], 'y': filtered_df.loc[filtered_df['LOC_ID'] == choice][traffic_type], 'type': 'line', 'name': name_lookup(trail_counter_info_df, choice, 'ID', 'LOCATION')}
        graph_data_dict.append(temp_dict)
        
    for agg in agg_type:
        if agg == 'mean':
            temp_dict = {'x': filtered_df.groupby(by='DATE').mean()[traffic_type].reset_index()['DATE'], 'y': filtered_df.groupby(by='DATE').mean()[traffic_type].reset_index()[traffic_type], 'type': 'line', 'name': 'Mean'}
            graph_data_dict.append(temp_dict)
        elif agg == 'min':
            temp_dict = {'x': filtered_df.groupby(by='DATE').min()[traffic_type].reset_index()['DATE'], 'y': filtered_df.groupby(by='DATE').min()[traffic_type].reset_index()[traffic_type], 'type': 'line', 'name': 'Min'}
            graph_data_dict.append(temp_dict)
        elif agg == 'max':
            temp_dict = {'x': filtered_df.groupby(by='DATE').max()[traffic_type].reset_index()['DATE'], 'y': filtered_df.groupby(by='DATE').max()[traffic_type].reset_index()[traffic_type], 'type': 'line', 'name': 'Max'}
            graph_data_dict.append(temp_dict)
        elif agg == 'sum':
            temp_dict = {'x': filtered_df.groupby(by='DATE').sum()[traffic_type].reset_index()['DATE'], 'y': filtered_df.groupby(by='DATE').sum()[traffic_type].reset_index()[traffic_type], 'type': 'line', 'name': 'Sum'}
            graph_data_dict.append(temp_dict)
    summary_df = filtered_df
    summary_df = summary_df.groupby(by=['LOC_ID']).sum().reset_index()
    graph_summary_dict_list = []
    for choice in combo_choices:
        temp_dict = {'x': [name_lookup(trail_counter_info_df, choice, 'ID', 'LOCATION')], 'y': summary_df.loc[summary_df['LOC_ID'] == choice][traffic_type], 'type': 'bar', 'name': name_lookup(trail_counter_info_df, choice, 'ID', 'LOCATION')}
        graph_summary_dict_list.append(temp_dict)
        traffic_by_year_summary_temp_dict = {'x': test_df.loc[test_df['LOC_ID'] == choice ]['YEAR'], 'y': test_df.loc[test_df['LOC_ID'] == choice ][traffic_type], 'type': 'bar', 'name': name_lookup(trail_counter_info_df, choice, 'ID', 'LOCATION')}
        traffic_by_year_summary_dict.append(traffic_by_year_summary_temp_dict)
    return ({
        'data': graph_data_dict,
            'layout': {
                'title': 'Traffic by Counter',
                'legend': {
                    #'orientation': 'v',
                    #'x': 0,
                    #'y': 1
                },
                'showlegend': legend_radio_value
            }
    },
    {
        'data': graph_summary_dict_list,
            'layout': {
                'title': 'Range Total by Counter',
                'legend': {
                    #'orientation': 'v',
                    #'x': 0,
                    #'y': 1
                },
                'showlegend': False,
                'bargroupgap': 0.5
            }
    },
    {
        'data': traffic_by_year_summary_dict,
            'layout': {
                'title': 'Total by Year by Counter',
                'legend': {
                    #'orientation': 'v',
                    #'x': 0,
                    #'y': 1
                },
                'showlegend': False,
                #'bargroupgap': 0.5,
                'barmode': 'group,'
            }
    })

@app.callback(
    [Output('counter_combo', 'options'), Output('counter_combo', 'value'), Output('activity', 'figure'), Output('activity_hour_week', 'figure')],
    [Input('main_div', 'children')
    ])

def update_counter(children):
    # combo_options = []
    # for index, row in trail_counter_info_df.iterrows():
    #     temp_dict = {'label': row['LOCATION'], 'value': row['ID']}
    #     combo_options.append(temp_dict)
    
    activity_df = trail_counter_readings_df
    activity_df['hour'] = activity_df['DATE'].dt.hour
    activity_df['dayofweek'] = activity_df['DATE'].dt.dayofweek
    activity_df['week'] = activity_df['DATE'].dt.week
    activity_df['month'] = activity_df['DATE'].dt.month
    activity_df_week_month = activity_df.groupby(by=['month', 'dayofweek']).mean().reset_index()
    activity_df_hour_week = activity_df.groupby(by=['week', 'hour']).mean().reset_index()

    trace_week_month = go.Heatmap(
        x=activity_df_week_month['month'],
        y=activity_df_week_month['dayofweek'],
        z=activity_df_week_month['CYCLIST_TOTAL'],
        colorscale='Greens',
        colorbar={"title": "Mean Cyclist Traffic"},
        showscale=True)
    
    trace_hour_week = go.Heatmap(
        x=activity_df_hour_week['week'],
        y=activity_df_hour_week['hour'],
        z=activity_df_hour_week['CYCLIST_TOTAL'],
        colorscale='Greens',
        colorbar={"title": "Mean Cyclist Traffic"},
        showscale=True)

    figure = {"data": [trace_week_month],
            "layout": go.Layout(
                title="Mean Cyclist Traffic by Day of Week and Month of Year (All Counters all Years)",
                xaxis={"title": "Month"},
                yaxis={"title": "Day of Week", "tickmode": "array"},
            )}
    figure_hour_week = {"data": [trace_hour_week],
            "layout": go.Layout(
                title="Mean Cyclist Traffic by Hour of Day and Week of Year (All Counters all Years)",
                xaxis={"title": "Week of Year"},
                yaxis={"title": "Hour of Day", "tickmode": "array"},
            )}
    #Laurel: [9, 6, 5, 1, 4, 3]
    return [list_for_dropdown(trail_counter_info_df), [1], figure, figure_hour_week]