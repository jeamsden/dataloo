import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import custom_core_components as ccc
import pandas as pd

fluid_setting = False # A global setting for fluid containers

home_layout = html.Div([
    ccc.navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('Welcome to Dataloo')
            ])
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.P('Hi there! Welcome to Dataloo. Dataloo is a transparent and accountable region. Best of all, Dataloo is always open. Feel free to take a look around. Things are really just getting started. Head on over to the cycling area to see what Dataloo knows about that.')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Cycling Overview", className='bg-primary text-white'),
                    dbc.CardBody([
                        html.P('Click here to check out an overview of Cycling data in Dataloo.'),
                        dcc.Link('Let\'s ride...', href='/cycling_overview', className='btn btn-primary'),
                    ])
                ])
            ], width=3)
        ])
                        
    ], fluid=fluid_setting)
])



cycling_overview_layout = html.Div([
    ccc.navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('Cycling Overview'),
            ])
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.P([
                    "Now with data from ",
                    html.Span('XX', id='counter_count'),
                    " counters across Kitchener and Waterloo!"
                ]),
                html.P([
                    "A note about the data: most counters provide data in 15 minute intervals while a few some provide data in one hour intervals. Data has been resampled to 15 minute intervals to preserve the higher level of detail. Because of this, resampled counters may show fractional pedestrians or cyclists in an interval. Linear resampling has been used to preserve the integrity of totals."
                ]),
            ])
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.Label('Pick Counter:'),
                dcc.Dropdown(
                    id='counter_combo',
                    options=[],
                    value=[1],
                    multi=True
                ),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Traffic Type:'),
                dcc.RadioItems(
                    id='traffic_type_radio',
                    options=[
                        {'label': 'All', 'value': 'TOTAL_COUNT'},
                        {'label': 'Cyclists', 'value': 'CYCLIST_TOTAL'},
                        {'label': 'Pedestrians', 'value': 'PEDESTRIAN_TOTAL'}
                    ],
                    value='CYCLIST_TOTAL',
                    #labelStyle={'display': 'inline-block'}
                )
            ]),
            dbc.Col([
                html.Label('Display Aggregate:'),
                dcc.Checklist(
                    id='aggregate_type_checklist',
                    options=[
                        {'label': 'Mean', 'value': 'mean'},
                        {'label': 'Max', 'value': 'max'},
                        {'label': 'Min', 'value': 'min'},
                        #{'label': 'Sum', 'value': 'sum'}
                    ],
                    value=[],
                    #labelStyle={'display': 'inline-block'}
                )
            ]),
            dbc.Col([
                html.Label('Display Legend:'),
                dcc.RadioItems(
                    id='legend_radio',
                    options=[
                        {'label': 'Show', 'value': 'Show'},
                        {'label': 'Hide', 'value': 'Hide'},
                    ],
                    value='Show',
                    #labelStyle={'display': 'inline-block'}
                )
            ]),
            dbc.Col([
                html.Label('Resolution:'),
                dcc.RadioItems(
                    id='resolution',
                    options=[
                        {'label': 'Year', 'value': 'Y'},
                        {'label': 'Quarter', 'value': '3M'},
                        {'label': 'Month', 'value': 'M'},
                        {'label': 'Week', 'value': 'W'},
                        {'label': 'Day', 'value': 'D'},
                        {'label': 'Hour', 'value': 'H'},
                        {'label': '15 Minutes', 'value': '15T'},
                    ],
                    value='W',
                    #labelStyle={'display': 'inline-block'}
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='traffic_graph'),
                dcc.Graph(id='traffic_summary'),
                dcc.Graph(id='traffic_by_year_summary'),
                dcc.Graph(id='activity'),
                dcc.Graph(id='activity_hour_week'),
            ])
        ])
    ], fluid=fluid_setting),
], id='main_div')

layout2 = html.Div([
    ccc.navbar,
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])