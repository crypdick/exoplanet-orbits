import plotly
import numpy as np


t = np.linspace(-1, 1, 100)
x = t + t ** 2
y = t - t ** 2
x_min = np.min(x) - 1.5
x_max = np.max(x) + 1.5
y_min = np.min(y) - 1.5
y_max = np.max(y) + 1.5
N = 50
s = np.linspace(-1, 1, N)
xx = s + s ** 2
yy = s - s ** 2

data = [dict(x=x, y=y,
             mode='lines',
             line=dict(width=2, color='blue')
             ),
        dict(x=x, y=y,
             mode='lines',
             line=dict(width=2, color='blue')
             )
        ]

layout = dict(xaxis=dict(range=[x_min, x_max], autorange=False, zeroline=False),
              yaxis=dict(range=[y_min, y_max], autorange=False, zeroline=False),
              title='Kinematic Generation of a Planar Curve',
              hovermode='closest',
              updatemenus=[{'type': 'buttons',
                            'buttons': [{'label': 'Play',
                                         'method': 'animate',
                                         'args': [None]}]}])

frames = [dict(data=[dict(x=[xx[k]],
                          y=[yy[k]],
                          mode='markers',
                          marker=dict(color='red', size=10)
                          )
                     ]) for k in range(N)]

figure1 = dict(data=data, layout=layout, frames=frames)
plotly.plotly.icreate_animations(figure1)