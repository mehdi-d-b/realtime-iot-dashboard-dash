from dash_extensions import EventSource
from dash_extensions.enrich import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


num = 1

fig = go.Figure(data = [go.Scattergl(
   x = [], y = [], mode = 'lines'
)]*7 + [go.Scattergl(x = [], y = [], mode = 'lines',  line_shape='hv',yaxis="y2")],
layout=go.Layout(
    xaxis=dict(fixedrange=True, type='date'),
    margin=dict(l=20, r=20, t=20, b=20),
    yaxis2=dict(side='right',type='category',categoryorder='array', categoryarray=["STOPPED", "STARTING", "RUNNING"])
))

graph_card = dbc.Card([
    dbc.CardHeader("1 graphique de 8 courbes à 10Hz"),
    dbc.CardBody([
        dcc.Graph(id='stress-test-graph-' + str(num),
                    figure=fig,
                ),  
        dcc.Interval(
            id='stress-test-interval-' + str(num),
            interval=0.1*1000, # in milliseconds
            n_intervals=0
            ) 
    ]
)])



layout = html.Div([
        dbc.Row([
            dbc.Col(graph_card)
            ])
        ], id="div-stress-test-1")

