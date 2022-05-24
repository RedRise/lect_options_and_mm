import plotly.graph_objs as go
import numpy as np
from numpy.random import default_rng
import src.plot_utils as pl

rng = default_rng(seed=555)

e = rng.binomial(1,0.5,10000)

b = np.cumsum(e-0.5)


layout = go.Layout(
    yaxis=dict(range=[-10, 10]),
    xaxis=dict(range=[0, 300])
)

fig = pl.new_subplot()
fig.add_scatter( y=b)
fig.update_layout(layout)
fig.show()

