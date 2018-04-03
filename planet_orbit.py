import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import numpy as np
import os

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Div([
        # TODO dynamic title https://dash.plot.ly/live-updates
        html.H2("Solar System"),
        # TODO dynamically change color based on system chosen
        html.Img(
            src="http://www.visioninconsciousness.org/Science-Cosm%20-02%20Hubble/SCN-COSM%20-010903.jpg"),
    ], className='banner'),
    html.Div([
        dcc.Interval(id='interval-component', interval=1000 / 60, n_intervals=0),
    ]),
    html.Div([
        dcc.Graph(id='planet-orbits')
    ])
])

def temp_to_color(temp):
#     TODO implement
    return 'rgba(132, 239, 241, 1)'


def mk_trace_generator(planet, in_habitable_zone=False):
    period, semi, size, temp = planet
    color = temp_to_color(temp)

    if in_habitable_zone:
        line_width = size * 0.1
    else:
        line_width = 0

    time = 0.
    while True:
        phase = 2. * np.pi * time / period
        xs, ys = semi * np.cos(phase), semi * np.sin(phase)
        time += 0.23
        yield (xs, ys, size, color)
        # TODO test making the go downstairs
        # graph_object = go.Scatter(
        #     x=np.array(xs),
        #     y=np.array(ys),
        #     mode='markers',
        #     marker=dict(size=50#,
                        #color="white"#, color#,
                        #line=dict(color='blue',
                        #          width=0.  # line_width
                              #    )
                        # )
        # )
        # yield graph_object


planet1 = (12., 5., 10., 500.)
planet2 = (8., 6., 25., 500.)
planet3 = (12., 10., 20., 500.)
planet4 = (12., 12., 30., 500.)
planet5 = (2., 17., 35., 500.)
planet6 = (1., 20., 25., 500.)
planets = [planet1, planet2, planet3, planet4, planet5, planet6]
n_planets = len(planets)

trace_generators = [mk_trace_generator(planet) for planet in planets]

# TODO maybe instead of generating 1 timept we can generate a small window and take advantage
# of vectorized ops
@app.callback(
    Output('planet-orbits', 'figure'),
    [Input('interval-component', 'n_intervals')])
def move_planets(interval):
    # +1 for the host star
    xs = np.empty(n_planets+1)
    ys = np.empty(n_planets+1)
    sizes = np.empty(n_planets+1)
    colors = []
    payload = [gen.__next__() for gen in trace_generators]
    # TODO: instead of grow
    for i, load in enumerate(payload):
        x, y, size, color = load
        xs[i], ys[i], sizes[i] = x,y,size
        colors.append(color)

    # host star
    xs[-1] = 0
    ys[-1] = 0
    sizes[-1] = 15  # star size TODO: grab from data
    colors.append('rgba(229, 196, 31, 1)')
    # traces.append(go.Scatter(
    #     x=np.array(0),
    #     y=np.array(0),
    #     mode='markers',
    #     marker={'size': 50,  # TODO update w actual stellar radius
    #             'color': 'yellow'}
    # ))

    trace = go.Scattergl(x=xs,
                         y=ys,
                         mode="markers",
                         marker=dict(size=sizes,
                                     color=colors))
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       xaxis=dict(showgrid=False,
                                  zeroline=False,
                                  range=[-20, 20]),
                       yaxis=dict(showgrid=False,
                                  zeroline=False,
                                  scaleanchor='x',  # equal axis ratios
                                  range=[-20, 20])
                       )

    return go.Figure(data= [trace], layout= layout)


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
#
if __name__ == '__main__':
    app.run_server()
