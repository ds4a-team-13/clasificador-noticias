import dash
from dash.dependencies import State, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

from datetime import datetime as dt
from datetime import timezone
import re


#df = read_news()
#df = df.iloc[0:10]

def pp(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.DatetimeIndex((10**9*np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))

samples = 10000
dates = pp(pd.to_datetime('2015-01-01'),pd.to_datetime('2019-02-01'),samples)
coords = np.random.rand(samples, 2) * 10
size = np.random.rand(samples, 1) * 480
color = np.random.randint(low=1, high = 5, size=samples)

d = {'dates': dates , 'x': coords[:,0],'y': coords[:,1], 'frequencies': size.flatten(), 'color': color.flatten().astype(str)}
df_test = pd.DataFrame(data=d)

#start_date = dt(2018,8,1)
#end_date = dt(2019,1,20)

def register_callbacks(app):
	@app.callback(
	    Output("cluster-graph", "figure"),
	    [
	        dash.dependencies.Input('my-date-picker-range', 'start_date'),
	        dash.dependencies.Input('my-date-picker-range', 'end_date'),
	        Input("clase_value", "value")
	    ],
	)
	def make_graph(date_start, date_end, class_value):
	    toplot = df_test[(df_test['dates'] > date_start) & (df_test['dates'] <= date_end)].copy()
	    toplot['frequencies'] = (toplot['frequencies']/(toplot['frequencies'].max()-toplot['frequencies'].min()))*10

	    fig = px.scatter(toplot, x="x", y="y",
	             size="frequencies", color="color",
	                 hover_name="color")

	    fig.update_traces(marker=dict(line=dict(width=2,
	                                        color='DarkSlateGrey')),
	                  selector=dict(mode='markers'))
	    return fig