from dash_extensions.enrich import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


# vars

options_traces = [
    {"label": "N/A", "value": 0},
    {"label": "Channel 1", "value": 1},
    {"label": "Channel 2", "value": 2},
    {"label": "Channel 3", "value": 3},
    {"label": "Channel 4", "value": 4},
]

option_gammes = [
    {"label": "10pT", "value": 0},
    {"label": "20pT", "value": 1},
    {"label": "...", "value": 2},
    {"label": "100nT", "value": 3}
    ]

input_groups_traces_1 = [
    dbc.Select(options=options_traces, id="trace-1-left", value=1),
    dbc.InputGroupText("-"),
    dbc.Select(options=options_traces, id="trace-1-right", value=0),
    dbc.InputGroupText("gamme:"),
    dbc.Select(options=option_gammes, value=0, style={"width": 50}),
    dbc.InputGroupText("Offset:"),
    dbc.Input(type="number", step=0.1, id="trace-1-offset", value=0, style={"width": 20})
]


input_groups_traces_2 = [
    dbc.Select(options=options_traces, id="trace-2-left", value=2),
    dbc.InputGroupText("-"),
    dbc.Select(options=options_traces, id="trace-2-right", value=0),
    dbc.InputGroupText("gamme:"),
    dbc.Select(options=option_gammes, value=0),
    dbc.InputGroupText("Offset:"),
    dbc.Input(type="number", step=0.1, id="trace-2-offset", value=0)
]

input_groups_traces_3 = [
    dbc.Select(options=options_traces, id="trace-3-left", value=3),
    dbc.InputGroupText("-"),
    dbc.Select(options=options_traces, id="trace-3-right", value=0),
    dbc.InputGroupText("gamme:"),
    dbc.Select(options=option_gammes, value=0),
    dbc.InputGroupText("Offset:"),
    dbc.Input(type="number", step=0.1, id="trace-3-offset", value=0)
]

input_groups_traces_4 = [
    dbc.Select(options=options_traces, id="trace-4-left", value=4),
    dbc.InputGroupText("-"),
    dbc.Select(options=options_traces, id="trace-4-right", value=0),
    dbc.InputGroupText("gamme:"),
    dbc.Select(options=option_gammes, value=0),
    dbc.InputGroupText("Offset:"),
    dbc.Input(type="number", step=0.1, id="trace-4-offset", value=0)
]

# Devices card

device_option_1 = "N/A"
device_option_2 = "RMN"
device_option_3 = "He4"

device_card = html.Div([
    dbc.Row([
        dbc.Col(dbc.Label("Channel 1:", html_for="name"), width={"size": 1}),
        dbc.Col(
            dbc.RadioItems(
                id="radios_channel1",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": device_option_1, "value": 1},
                    {"label": device_option_2, "value": 2},
                    {"label": device_option_3, "value": 3},
                ],
                value=1,
            ),width={"size": 1}
        )
    ], align='center'),
    dbc.Row([
        dbc.Col(dbc.Label("Channel 2:", html_for="name"), width={"size": 1}),
        dbc.Col(
            dbc.RadioItems(
                id="radios_channel2",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": device_option_1, "value": 1},
                    {"label": device_option_2, "value": 2},
                    {"label": device_option_3, "value": 3},
                ],
                value=1,
            ),width={"size": 1}
        )
    ], align='center'),
    dbc.Row([
        dbc.Col(dbc.Label("Channel 3:", html_for="name"), width={"size": 1}),
        dbc.Col(
            dbc.RadioItems(
                id="radios_channel3",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": device_option_1, "value": 1},
                    {"label": device_option_2, "value": 2},
                    {"label": device_option_3, "value": 3},
                ],
                value=1,
            ),width={"size": 1}
        )
    ], align='center'),
    dbc.Row([
        dbc.Col(dbc.Label("Channel 4:", html_for="name"), width={"size": 1}),
        dbc.Col(
            dbc.RadioItems(
                id="radios_channel4",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": device_option_1, "value": 1},
                    {"label": device_option_2, "value": 2},
                    {"label": device_option_3, "value": 3},
                ],
                value=1,
            ),width={"size": 1}
        )
    ], align='center'),
    html.Br(style={"line-height": "2"}),
    dbc.Button('Send', id='send-frequencemetre', n_clicks=0,className="me-md-2")
], className="radio-group")


traces_card = html.Div([
    dbc.Row(
        dbc.Col(
        [
            dbc.InputGroup(input_groups_traces_1, className="mb-3"),
            dbc.InputGroup(input_groups_traces_2, className="mb-3"),
            dbc.InputGroup(input_groups_traces_3, className="mb-3"),
            dbc.InputGroup(input_groups_traces_4, className="mb-3")
        ],width={"size": 6})
        )
    ]
)

record_card = html.Div([
    dbc.Row([
        # Colonne Filtres
        dbc.Col([
            html.H4('Bessel Filter'),
            dbc.Row(
                dbc.InputGroup(
                    [dbc.InputGroupText("FC Basse"), dbc.Input(type="number"),dbc.InputGroupText("Hz")])
            ),
            html.Br(style={"line-height": "1"}),
            dbc.Row(
                dbc.InputGroup(
                    [dbc.InputGroupText("F décim"), dbc.Input(type="number"),dbc.InputGroupText("Hz")])
            ),
            
        ],  width={"size": 2}),
        # Colonne File
        dbc.Col([
            html.H4('File'),
            dbc.Row(
                    dbc.InputGroup([dbc.InputGroupText("Name"), dbc.Input(placeholder="Filename")]),
            ),
            html.Br(style={"line-height": "1"}),
            dbc.Row(dbc.InputGroup(
                    [
                        dbc.Button( "Select", id="input-group-button", n_clicks=0),
                        dbc.Input(id="input-group-button-input", placeholder="Folder")
                    ])),
            html.Br(style={"line-height": "1"}),     
            dbc.Row(
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Comment"),
                        dbc.Textarea(),
                    ],
                    className="mb-3",
                ) 
            )
            
        ],width={"size": 4})]),
    dbc.Row([
        dbc.Col(dbc.Button(
        "Record",
        id="button-record",
        className="me-1",
        n_clicks=0,
        )),
        dbc.Col(dbc.Button(
        "Download",
        id="button-record-download",
        className="me-1",
        n_clicks=0,
        )),
    ]),
])


graph_card = dbc.Card([
    dbc.CardHeader("Live Feed"),
    dbc.CardBody([
        dcc.Graph(id='live-update-graph',
                    figure=go.Figure(data = [go.Scattergl(
                       x = [], y = [], mode = 'lines', yaxis="y2"
                    )]*8 + 
                    [go.Scattergl(x = [], y = [], mode = 'lines', line_shape='hv')],
                    layout=go.Layout(
                        xaxis=dict(fixedrange=True, type='date'),
                        margin=dict(l=20, r=20, t=20, b=20),
                        yaxis=dict(side='right'),
                        hovermode="x",
                        yaxis2=dict(fixedrange=True, side='left',type='category',categoryorder='array', categoryarray=["STOPPED", "STARTING", "RUNNING"])
                ))),
        dcc.Interval(
            id='interval-component',
            interval=0.5*1000, # in milliseconds
            n_intervals=0
            ),
     
    ]
)])

fft_card = dbc.Card([
    dbc.CardHeader("FFT"),
    dbc.CardBody([
        dcc.Graph(id="fft-graph",
        figure=go.Figure(data=go.Scattergl(
                       x = [], y = [], mode = 'lines'
                    ),
        layout=go.Layout(
                    yaxis = dict(title = 'Amplitude'),
                    xaxis = dict(title = 'Frequency (Hz)'), 
                    margin=dict(l=20, r=20, t=20, b=20),
                    hovermode='closest'
                    ))),
        dcc.Interval(
            id='fft-interval',
            interval=1*1000, # in milliseconds
            n_intervals=0
            ),
    ])
])

time_at_frequency_card = dbc.Card([
    dbc.CardHeader("Value at selected Frequency"),
    dbc.CardBody([
        dcc.Graph(id="time-at-frequency-graph",
        figure=go.Figure(data=go.Scattergl(
                       x = [], y = [], mode = 'lines'
                    ),
        layout=go.Layout(
                    yaxis = dict(title = 'Amplitude'), 
                    xaxis = dict(title = 'Time'), 
                    margin=dict(l=20, r=20, t=20, b=20)
                    ))),
    ])
])


param_card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Device", tab_id="tab-device"),
                    dbc.Tab(label="Traces", tab_id="tab-traces"),
                    dbc.Tab(label="Recording", tab_id="tab-record"),
                ],
                id="param-tabs",
                active_tab="tab-device",
            )
        ),
        dbc.CardBody(html.P(id="param-content", className="card-text")),
    ]
)


alert_send = dbc.Alert(
            "Commande envoyée au fréquencemètre.",
            id="send-frequencemetre",
            dismissable=True,
            fade=False,
            is_open=False,
        )





layout = html.Div([
        dcc.Store(id='param-device', storage_type='session'),
        dcc.Store(id='param-traces', storage_type='session'),
        dcc.Store(id='param-record', storage_type='session'),
        param_card,
        html.Br(style={"line-height": "1"}),
        dbc.Row([
            dbc.Col(graph_card)
            ]),
        html.Br(style={"line-height": "1"}),
        dbc.Row([
                dbc.Col(fft_card),
                dbc.Col(time_at_frequency_card)
            ])
        ])
    



