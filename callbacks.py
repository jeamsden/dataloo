from dash.dependencies import Input, Output

from app import app
import pandas as pd
import data_processor
counter_data = data_processor.get_data('counter_readings')
counter_info = data_processor.get_data('counters')

counter_data['DATE'] = pd.to_datetime(counter_data['DATE'], infer_datetime_format=True)

combo_options = []
value_list = []
better_dict = {}
for index, row in counter_info.iterrows():
    temp_dict = {'label': row['LOCATION'], 'value': row['ID']}
    combo_options.append(temp_dict)
    value_list.append(row['ID'])
    better_dict[row['ID']] = row['LOCATION']

@app.callback(
    [Output('traffic_graph', 'figure'),
    Output('traffic_summary', 'figure'),
    Output('traffic_by_year_summary', 'figure')],
    [Input('counter_combo', 'value'),
    Input('traffic_type_radio', 'value'),
    Input('legend_radio', 'value'),
    Input('aggregate_type_checklist', 'value')
    ])

def update_graph(combo_choices, traffic_type, legend_radio, agg_type):
    print(combo_choices)
    if legend_radio == 'Show':
        legend_radio_value = True
    elif legend_radio == 'Hide':
        legend_radio_value = False
    filtered_df = counter_data.loc[counter_data['LOC_ID'].isin(combo_choices)]
    test_df = filtered_df.copy(deep=True)
    test_df['YEAR'] = test_df['DATE'].dt.year
    test_df = test_df.groupby(by=['LOC_ID', 'YEAR']).sum().reset_index()
    graph_data_dict = []
    traffic_by_year_summary_dict = []
    for choice in combo_choices:
        temp_dict = {'x': filtered_df.loc[filtered_df['LOC_ID'] == choice]['DATE'], 'y': filtered_df.loc[filtered_df['LOC_ID'] == choice][traffic_type], 'type': 'line', 'name': better_dict[choice]}
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
        temp_dict = {'x': [better_dict[choice]], 'y': summary_df.loc[summary_df['LOC_ID'] == choice][traffic_type], 'type': 'bar', 'name': better_dict[choice]}
        graph_summary_dict_list.append(temp_dict)
        traffic_by_year_summary_temp_dict = {'x': test_df.loc[test_df['LOC_ID'] == choice ]['YEAR'], 'y': test_df.loc[test_df['LOC_ID'] == choice ][traffic_type], 'type': 'bar', 'name': better_dict[choice]}
        traffic_by_year_summary_dict.append(traffic_by_year_summary_temp_dict)
    return ({
        'data': graph_data_dict,
            'layout': {
                'title': 'Traffic per Day by Counter',
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
    [Output('counter_combo', 'options'), Output('counter_combo', 'value')],
    [Input('test1', 'children')
    ])

def update_counter(children):
    combo_options = []
    for index, row in counter_info.iterrows():
        temp_dict = {'label': row['LOCATION'], 'value': row['ID']}
        combo_options.append(temp_dict)
    return [combo_options, [9, 6, 5, 1, 4, 3]]