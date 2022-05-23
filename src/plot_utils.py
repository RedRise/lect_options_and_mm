import plotly.graph_objects as go
from plotly.subplots import make_subplots


def new_subplot():
    return make_subplots(specs=[[{"secondary_y": True}]])


def add_serie(fig, df, colname, go_fun=go.Scatter, second_axis=False, displayed=True):

    name = "{0} ({1})".format(colname, "right" if second_axis else "left")
    visible = "legendonly" if not displayed else True

    fig.add_trace(go_fun(x=df.index, y=df[colname],
                         name=name, visible=visible), secondary_y=second_axis)
