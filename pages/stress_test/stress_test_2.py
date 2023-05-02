from dash_extensions import EventSource
from dash_extensions.enrich import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

num = 2


graph_card = dbc.Card([
    dbc.CardHeader("1 graphique de 8 courbes à 10Hz"),
    dbc.CardBody([
        dcc.Graph(id='stress-test-graph-' + str(num),
                    figure=go.Figure(data = [go.Scattergl(
                       x = [], y = [], mode = 'lines'
                    )]*8,
                    layout=go.Layout(
                        xaxis=dict(fixedrange=True, type='date'),
                        margin=dict(l=20, r=20, t=20, b=20))),
                ),  
    ]
)])



layout = html.Div([
        dbc.Row([
            dbc.Col(graph_card)
            ])
        ], id="div-stress-test-2")
    