import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import pandas as pd
import os
import sqlite3
import datetime as dt

app = dash.Dash('streaming-wind-app')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H2("Wind Speed Streaming"),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png"),
    ], className='banner'),
    html.Div([
        html.Div([
            html.H3("WIND SPEED (mph)")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='wind-speed'),
        ], className='twelve columns wind-speed'),
        dcc.Interval(id='wind-speed-update', interval=1000, n_intervals=0),
    ], className='row wind-speed-row'),
])


@app.callback(Output('wind-speed', 'figure'), [Input('wind-speed-update', 'n_intervals')])
def gen_wind_speed(interval):
    # now = dt.datetime.now()
    # sec = now.second
    # minute = now.minute
    # hour = now.hour

    # total_time = (hour * 3600) + (minute * 60) + (sec)

    # con = sqlite3.connect("./Data/wind-data.db")
    # df = pd.read_sql_query('SELECT Speed, SpeedError, Direction from Wind where\
    #                         rowid > "{}" AND rowid <= "{}";'
    #                         .format(total_time-200, total_time), con)

    df = pd.DataFrame(np.random.randint(0, 100, size=(200, 2)),
                      columns=['Speed', 'SpeedError'])

    trace = Scatter(
        y=df['Speed'],
        line=Line(
            color='#42C4F7'
        ),
        hoverinfo='skip',
        error_y=ErrorY(
            type='data',
            array=df['SpeedError'],
            thickness=1.5,
            width=2,
            color='#B4E8FC'
        ),
        mode='lines'
    )

    layout = Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)',
            color='#fff'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10)),
            color='#fff'
        ),
        margin=Margin(
            t=45,
            l=50,
            r=50
        ),
        paper_bgcolor='rgba(1,1,1,1)',
        plot_bgcolor='rgba(1,1,1,1)'
    )

    return Figure(data=[trace], layout=layout)

#
# @app.callback(Output('wind-histogram', 'figure'),
#               [Input('wind-speed-update', 'n_intervals')],
#               [State('wind-speed', 'figure'),
#                State('bin-slider', 'value'),
#                State('bin-auto', 'values')])
# def gen_wind_histogram(interval, wind_speed_figure, sliderValue, auto_state):
#     wind_val = []
#
#     # Check to see whether wind-speed has been plotted yet
#     if wind_speed_figure is not None:
#         wind_val = wind_speed_figure['data'][0]['y']
#     if 'Auto' in auto_state:
#         bin_val = np.histogram(wind_val, bins=range(int(round(min(wind_val))),
#                                int(round(max(wind_val)))))
#     else:
#         bin_val = np.histogram(wind_val, bins=sliderValue)
#
#     avg_val = float(sum(wind_val))/len(wind_val)
#     median_val = np.median(wind_val)
#
#     pdf_fitted = rayleigh.pdf(bin_val[1], loc=(avg_val)*0.55,
#                               scale=(bin_val[1][-1] - bin_val[1][0])/3)
#
#     y_val = pdf_fitted * max(bin_val[0]) * 20,
#     y_val_max = max(y_val[0])
#     bin_val_max = max(bin_val[0])
#
#     trace = Bar(
#         x=bin_val[1],
#         y=bin_val[0],
#         marker=Marker(
#             color='#7F7F7F'
#         ),
#         showlegend=False,
#         hoverinfo='x+y'
#     )
#     trace1 = Scatter(
#         x=[bin_val[int(len(bin_val)/2)]],
#         y=[0],
#         mode='lines',
#         line=Line(
#             dash='dash',
#             color='#2E5266'
#         ),
#         marker=Marker(
#             opacity=0,
#         ),
#         visible=True,
#         name='Average'
#     )
#     trace2 = Scatter(
#         x=[bin_val[int(len(bin_val)/2)]],
#         y=[0],
#         line=Line(
#             dash='dot',
#             color='#BD9391'
#         ),
#         mode='lines',
#         marker=Marker(
#             opacity=0,
#         ),
#         visible=True,
#         name='Median'
#     )
#     trace3 = Scatter(
#         mode='lines',
#         line=Line(
#             color='#42C4F7'
#         ),
#         y=y_val[0],
#         x=bin_val[1][:len(bin_val[1])],
#         name='Rayleigh Fit'
#     )
#     layout = Layout(
#         xaxis=dict(
#             title='Wind Speed (mph)',
#             showgrid=False,
#             showline=False,
#             fixedrange=True
#         ),
#         yaxis=dict(
#             showgrid=False,
#             showline=False,
#             zeroline=False,
#             title='Number of Samples',
#             fixedrange=True
#         ),
#         margin=Margin(
#             t=50,
#             b=20,
#             r=50
#         ),
#         autosize=True,
#         bargap=0.01,
#         bargroupgap=0,
#         hovermode='closest',
#         legend=Legend(
#             x=0.175,
#             y=-0.2,
#             orientation='h'
#         ),
#         shapes=[
#             dict(
#                 xref='x',
#                 yref='y',
#                 y1=int(max(bin_val_max, y_val_max))+0.5,
#                 y0=0,
#                 x0=avg_val,
#                 x1=avg_val,
#                 type='line',
#                 line=Line(
#                     dash='dash',
#                     color='#2E5266',
#                     width=5
#                 )
#             ),
#             dict(
#                 xref='x',
#                 yref='y',
#                 y1=int(max(bin_val_max, y_val_max))+0.5,
#                 y0=0,
#                 x0=median_val,
#                 x1=median_val,
#                 type='line',
#                 line=Line(
#                     dash='dot',
#                     color='#BD9391',
#                     width=5
#                 )
#             )
#         ]
#     )
#     return Figure(data=[trace, trace1, trace2, trace3], layout=layout)
#


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    app.run_server()
