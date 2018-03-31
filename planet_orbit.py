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
print("layout done")

# def temp_to_color(temp):
#     TODO implement
    # return 'white'


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
        time += 0.23
        print("generated")
        yield (xs, ys)
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


planet1 = (1.5, 1, 30., 500.)
planet2 = (4.1, 0.5, 30., 500.)
planets = [planet1, planet2]
n_planets = len(planets)

trace_generators = [mk_trace_generator(planet) for planet in planets]


@app.callback(
    Output('planet-orbits', 'figure'),
    [Input('interval-component', 'n_intervals')])
def move_planets(interval):
    print("moving planets")
    xs = np.empty(n_planets)
    ys = np.empty(n_planets)
    payload = [gen.__next__() for gen in trace_generators]
    for i, load in enumerate(payload):
        x,y = load
        xs[i], ys[i] = x,y

    print(xs, ys)
    # host star
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
                         )
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       xaxis=dict(showgrid=False,
                                  zeroline=False,
                                  range=[-5, 5]),
                       yaxis=dict(showgrid=False,
                                  zeroline=False,
                                  range=[-5, 5])
                       )

    return go.Figure(data= [trace], layout= layout)


# external_css = [
#     "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
#     "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
#     "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
#     "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]
#
# for css in external_css:
#     app.css.append_css({"external_url": css})
#
# app.css.append_css({'external_url': 'https://codepen.io/plotly/pen/YeqjLb.css'})
# app.css.append_css({
#                        'external_url': 'https://raw.githubusercontent.com/crypdick/exoplanet-orbits/master/exoplanet.css'})
#
# if 'DYNO' in os.environ:
#     app.scripts.append_script({
#         'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
#     })
#
if __name__ == '__main__':
    app.run_server()
