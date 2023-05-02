import dash
import dash_bootstrap_components as dbc
#from dash import Input, Output, State, dcc, html
import math
import time
import datetime
import numpy as np
import orjson as json
from dash_extensions import EventSource
from dash_extensions.enrich import (
    #DashProxy,
    #Dash,
    Output,
    Input,
    State,
    dcc,
    html,
    #ServersideOutput,
    #ServersideOutputTransform,
    #OperatorTransform,
    #Operator,
    #OperatorOutput
)
import plotly.graph_objs as go
from scipy import fftpack

import redis

import pages.frequencemetre as frequencemetre
import pages.stress_test.stress_test_1 as stress_test_1
import pages.stress_test.stress_test_2 as stress_test_2



NOMBRE_DE_POINTS = 1000

r = redis.Redis()

app = dash.Dash(
    #transforms=[OperatorTransform()],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True,
    update_title=None
)



# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("CAID", className="display-4")),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Plateforme de données MQTT.",
                    className="lead",
                ),
                html.Div([dbc.Badge("Online", color="success", className="me-1"), html.Label("Fréquencemètre")]),
                html.Div([dbc.Badge("Offline", color="secondary", className="me-1"), html.Label("Device #2")]),
                html.Div([dbc.Badge("Error", color="danger", className="me-1"), html.Label("Device #3")])
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink(["Accueil"], href="/", active="exact"),
                    dbc.NavLink("Fréquencemètre", href="/page-1", active="exact"),
                    dbc.NavLink("Benchmark MQTT 1/2", href="/page-11", active="exact"),
                    dbc.NavLink("Benchmark MQTT 2/2", href="/page-12", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

content = html.Div(id="page-content")

app.layout = html.Div([
    dcc.Location(id="url"), 
    sidebar, 
    content,
    # benchmark page 1
    # EventSource(id="sse-1", url="http://127.0.0.1:5000/random_data"),
    # benchmark page 2
    EventSource(id="sse-2", url="http://127.0.0.1:5000/random_data_2"),
    ])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return frequencemetre.layout
    elif pathname == "/page-11":
        return stress_test_1.layout
    elif pathname == "/page-12":
        return stress_test_2.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("param-content", "children"), [Input("param-tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-device":
        return frequencemetre.device_card
    elif at == "tab-traces":
        return frequencemetre.traces_card
    elif at == "tab-record":
        return frequencemetre.record_card
    return html.P("This shouldn't ever be displayed...")


# Store traces parameters
@app.callback(
    Output('param-traces', 'data'),
    Input("trace-1-left", "value"),
    Input("trace-2-left", "value"),
    Input("trace-3-left", "value"),
    Input("trace-4-left", "value"),
    Input("trace-1-right", "value"),
    Input("trace-2-right", "value"),
    Input("trace-3-right", "value"),
    Input("trace-4-right", "value"),
    Input("trace-1-offset", "value"),
    Input("trace-2-offset", "value"),
    Input("trace-3-offset", "value"),
    Input("trace-4-offset", "value"),
)
def update_store_traces(
        trace_1_left,
        trace_2_left,
        trace_3_left,
        trace_4_left,
        trace_1_right,
        trace_2_right,
        trace_3_right,
        trace_4_right,
        trace_1_offset,
        trace_2_offset,
        trace_3_offset,
        trace_4_offset): 
    
    return {
            'trace_1_left' : trace_1_left,
            'trace_2_left' : trace_2_left,
            'trace_3_left' : trace_3_left,
            'trace_4_left' : trace_4_left,
            'trace_1_right' : trace_1_right,
            'trace_2_right' : trace_2_right,
            'trace_3_right' : trace_3_right,
            'trace_4_right' : trace_4_right,
            'trace_1_offset' : trace_1_offset,
            'trace_2_offset' : trace_2_offset,
            'trace_3_offset' : trace_3_offset,
            'trace_4_offset' : trace_4_offset
        
        }

# Redessiner le fréquencemètre au changement de paramètres
@app.callback(
    Output('live-update-graph', 'figure'),
    Input('param-traces', 'data'),
    Input('param-device', 'data')
    )
def redraw_frequencemetre(params, _):
    raw_data = r.lrange('random_sin', 0, -1)
    x = [json.loads(d)['timestamp'] for d in raw_data]
     
    layout=go.Layout(
        xaxis=dict(fixedrange=True, type='date'),
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis2=dict(side='right'),
        hovermode="x",
        yaxis=dict(fixedrange=True, side='left', type='category', categoryorder='array', categoryarray=["STOPPED", "STARTING", "RUNNING"]))
    
    offset = [
        float(params['trace_1_offset']),
        float(params['trace_2_offset']),
        float(params['trace_3_offset']),
        float(params['trace_4_offset']),
        0,0,0,0
        ]
    left = [str(params['trace_1_left']),
            str(params['trace_2_left']),
            str(params['trace_3_left']),
            str(params['trace_4_left']),
            "4","5","6","7"
            ]
    
    right = [str(params['trace_1_right']),
            str(params['trace_2_right']),
            str(params['trace_3_right']),
            str(params['trace_4_right']),
            "N","N","N","N"
            ]
    
    traces = []
    for i in range(8):
        if right[i] == "N":
            y = [(json.loads(d)['var_' + left[i]] + offset[i]) for d in raw_data]
        else:
            y = [(json.loads(d)['var_' + left[i]] - json.loads(d)['var_' + right[i]] + offset[i]) for d in raw_data]
        trace = go.Scattergl(
            x=x,
            y=y,
            mode='lines',
            yaxis="y2"
        )
        traces.append(trace)
    
    enum = []
    for d in [(json.loads(d)['enum']) for d in raw_data]:
        if d == 0:
            enum.append("STOPPED")
        if d == 1:
            enum.append("STARTING")
        if d == 2:
            enum.append("RUNNING")
    
    traces.append(go.Scattergl(x = x, y = enum, mode = 'lines', line_shape='hv'))
    
    fig = go.Figure(data=traces, layout=layout)

    
    return fig

# Update Fréquencemètre
@app.callback(
    Output('live-update-graph', 'extendData'),
    Input('interval-component', 'n_intervals'),
    State('param-traces', 'data'),
)
def update_graph_live(n,
        param_traces):   
    
    if param_traces is None:
        param_traces = {
            'trace_1_left' : 1,
            'trace_2_left' : 2,
            'trace_3_left' : 3,
            'trace_4_left' : 4,
            'trace_1_right' : 0,
            'trace_2_right' : 0,
            'trace_3_right' : 0,
            'trace_4_right' : 0,
            'trace_1_offset' : 0,
            'trace_2_offset' : 0,
            'trace_3_offset' : 0,
            'trace_4_offset' : 0
        }
    
    # Collect some data
    data = [json.loads(row) for row in r.lrange('random_sin', -5, -1)]
    var_0 = [d['var_' + str(param_traces['trace_1_left'])] - d['var_' + str(param_traces['trace_1_right'])] + float(param_traces['trace_1_offset']) for d in data]
    var_1 = [d['var_' + str(param_traces['trace_2_left'])] - d['var_' + str(param_traces['trace_2_right'])] + float(param_traces['trace_2_offset']) for d in data]
    var_2 = [d['var_' + str(param_traces['trace_3_left'])] - d['var_' + str(param_traces['trace_3_right'])] + float(param_traces['trace_3_offset']) for d in data]
    var_3 = [d['var_' + str(param_traces['trace_4_left'])] - d['var_' + str(param_traces['trace_4_right'])] + float(param_traces['trace_4_offset']) for d in data]
    var_4 = [d['var_4'] for d in data]
    var_5 = [d['var_5'] for d in data]
    var_6 = [d['var_6'] for d in data]
    var_7 = [d['var_7'] for d in data]
    #enum = [d['enum'] for d in data]
    enum = []
    for d in data:
        if d['enum'] == 0:
            enum.append("STOPPED")
        if d['enum'] == 1:
            enum.append("STARTING")
        if d['enum'] == 2:
            enum.append("RUNNING")
    y =[var_0, var_1, var_2, var_3, var_4, var_5, var_6, var_7, enum]
    return [{'x': [[d['timestamp'] for d in data]] * 9,'y': y}, [x for x in range(9)], NOMBRE_DE_POINTS]

# fft interval
@app.callback(Output('fft-graph', 'figure'),
              Input('fft-interval', 'n_intervals'),
              State('live-update-graph', 'figure')
              )
def update_fft(n, lg_figure):
    data = lg_figure['data'][0]['y']
    
    layout = go.Layout(
                yaxis = dict(title = 'Amplitude'),
                xaxis = dict(title = 'Frequency (Hz)'), 
                margin=dict(l=20, r=20, t=20, b=20)
                )
    
    
    if len(data) >= NOMBRE_DE_POINTS :
        # sample spacing
        T = 1.0 / 10.0
        y = np.asarray(data, dtype=np.float32)
        yf = fftpack.fft(y)
        xf = np.linspace(0.0, 1.0/(2.0*T), NOMBRE_DE_POINTS//2)
        
        trace = [go.Scattergl(
            x= xf,
            y= 2.0/NOMBRE_DE_POINTS * np.abs(yf[:NOMBRE_DE_POINTS//2])
        )]
        
        return go.Figure(data=trace, layout=layout)
    else:
        return dash.no_update

 
@app.callback(
    Output("button-record", "children"),
    [Input("button-record", "n_clicks")],
)
def toggle_record(n):
    if (n % 2) == 0:
        return "Record"
    return ["Recording... ",dbc.Spinner(color="light", type="grow",size="sm")]
       

# stress test 1 
update_graph = """function(msg) {
                  if (!msg) {
                    return {}; // Si aucune donnée n'est fournie, retourner un objet vide
                  }
                
                  const data = JSON.parse(msg); // Analyser les données JSON
                
                  const x = [new Date(data.timestamp)];
                  const y = [
                    [data.var_0],
                    [data.var_1],
                    [data.var_2],
                    [data.var_3],
                    [data.var_4],
                    [data.var_5],
                    [data.var_6],
                    [data.var_7],
                  ];
                
                  return [
                    {
                      x: Array(8).fill(x),
                      y: y,
                    },
                    [0, 1, 2, 3, 4, 5, 6, 7],
                    1000,
                  ];
                } 
    
"""

'''app.clientside_callback(update_graph, 
                        Output('stress-test-graph-1', 'extendData'), 
                        Input("sse-1", "message"))'''
    
# Stress test
@app.callback(Output('stress-test-graph-1', 'extendData'), 
              Input('stress-test-interval-1', 'n_intervals'))
def update_fig_1(n):
        data = json.loads(r.lindex('random_sin', -1))
        var_0 = [data['var_0']]
        var_1 = [data['var_1']]
        var_2 = [data['var_2']]
        var_3 = [data['var_3']]
        var_4 = [data['var_4']]
        var_5 = [data['var_5']]
        var_6 = [data['var_6']]
        var_7 = [data['var_7']]
        y =[var_0, var_1, var_2, var_3, var_4, var_5, var_6, var_7]
        return [{'x': [[data["timestamp"]]] * 8,'y': y}, [x for x in range(8)], NOMBRE_DE_POINTS]


# stress test 1 (graph full load)

@app.callback(
    Output('stress-test-graph-1', 'figure'),
    Input("div-stress-test-1", "children")
)
def update_stress_test_1_page_load(div_children):
    raw_data = r.lrange('random_sin', 0, -1)
    
    x = [json.loads(d)['timestamp'] for d in raw_data]
     
    layout=go.Layout(
        xaxis=dict(fixedrange=True, type='date'),
        margin=dict(l=20, r=50, t=20, b=20),
        yaxis=dict(side="right"),
        yaxis2=dict(side='left',categoryorder='array', categoryarray=["STOPPED", "STARTING", "RUNNING"])
        )
    
    traces = []
    for i in range(7):
        trace = go.Scattergl(
            x=x,
            y=[json.loads(d)[f'var_{i}'] for d in raw_data],
            mode='lines',
        )
        traces.append(trace)
    # variable énuméré
    traces.append(
        go.Scattergl(x = x, y = [json.loads(d)[f'var_{7}'] for d in raw_data], 
                     mode = 'lines+text',  
                     line_shape='hv', 
                     yaxis="y2"))
    
    fig = go.Figure(data=traces, layout=layout)

    
    return fig



# stress test 2 
app.clientside_callback(update_graph, 
                        Output('stress-test-graph-2', 'extendData'), 
                        Input("sse-2", "message"))



# stress test 2 (graph full load)

@app.callback(
    Output('stress-test-graph-2', 'figure'),
    Input("div-stress-test-2", "children")
)
def update_stress_test_2_page_load(div_children):
    raw_data = r.lrange('random_ramp', 0, -1)
    

    layout=go.Layout(
        xaxis=dict(fixedrange=True, type='date'),
        margin=dict(l=20, r=20, t=20, b=20)
        )
      
    traces = []
    for i in range(8):
        trace = go.Scattergl(
            x=[datetime.datetime.fromtimestamp(json.loads(d)['timestamp']/1000.0) for d in raw_data],
            y=[json.loads(d)[f'var_{i}'] for d in raw_data],
            mode='lines',
        )
        traces.append(trace)
    
    fig = go.Figure(data=traces, layout=layout)
        
    return fig


if __name__ == "__main__":
    app.run_server(port=8889, debug=True)