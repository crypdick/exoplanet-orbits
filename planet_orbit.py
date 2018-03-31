import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import numpy as np
import os

app = dash.Dash('planetary-orbits')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H2("Solar System"),
        # TODO dynamically change color based on system chosen
        html.Img(
            src="http://www.visioninconsciousness.org/Science-Cosm%20-02%20Hubble/SCN-COSM%20-010903.jpg"),
    ], className='banner'),
    html.Div([
        dcc.Interval(id='orbit-position-update', interval=1000 / 60,
                     n_intervals=0),
    ], className='row wind-speed-row'),
    html.Div([
        dcc.Graph(id='planet-orbits')
    ])
])


def temp_to_color(temp):
    # TODO implement
    return 'white'


def mk_trace_generator(planet, in_habitable_zone=False):
    period, semi, size, temp = planet
    # color = temp_to_color(temp)
    #
    # if in_habitable_zone:
    #     line_width = size * 0.1
    # else:
    #     line_width = 0

    time = 0.
    while True:
        phase = 2. * np.pi * time / period
        xs, ys = semi * np.cos(phase), semi * np.sin(phase)
        print(xs, ys)
        time += 0.23
        # TODO test making the go downstairs
        graph_object = go.Scatter(
            x=np.array(xs),
            y=np.array(ys),
            mode='markers',
            marker=dict(#size=size,
                        color="white"#, color#,
                        #line=dict(color='blue',
                        #          width=0.  # line_width
                              #    )
                        )
        )
        yield graph_object


planet1 = (1.5, 1, 30., 500.)
planet2 = (4.1, 0.5, 30., 500.)
planets = [planet1]#, planet2]

trace_generators = [mk_trace_generator(planet) for planet in planets]


@app.callback(
    dash.dependencies.Output('planet-orbits', 'figure'),
    [Input('orbit-position-update', 'n_intervals')])
def move_planets(interval):
    traces = [gen.__next__() for gen in trace_generators]
    # host star
    # traces.append(go.Scatter(
    #     x=np.array(0),
    #     y=np.array(0),
    #     mode='markers',
    #     marker={'size': 50,  # TODO update w actual stellar radius
    #             'color': 'yellow'}
    # ))

    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       xaxis=dict(showgrid=False,
                                  zeroline=False,
                                  range=[-5, 5]),
                       yaxis=dict(showgrid=False,
                                  zeroline=False,
                                  range=[-5, 5])
                       )

    return {
        'data': traces,
        'layout': layout
    }


external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
    "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
    "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

for css in external_css:
    app.css.append_css({"external_url": css})

app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/YeqjLb.css'})
app.css.append_css({
                       'external_url': 'https://raw.githubusercontent.com/crypdick/exoplanet-orbits/master/exoplanet.css'})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    app.run_server()
