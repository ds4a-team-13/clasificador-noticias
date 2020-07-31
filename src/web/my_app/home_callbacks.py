import dash
from dash.dependencies import State, Input, Output
import dash_html_components as html
import plotly.express as px


def register_callbacks(app):
	@app.callback(
		Output("diaries", "children"),
		[
			Input('none', 'children'),
		],
		)
	def image_test1(none):
		return html.Img(
			src=app.get_asset_url("periodicos.png"),
			style={
			"height": "280px",
			"width": "auto",
			"margin-bottom": "25px",
			"margin-left": "100px",
			})
	@app.callback(
		Output("categories", "children"),
		[
			Input('none', 'children'),
		],
		)
	def image_test2(none):
		return html.Img(
			src=app.get_asset_url("dia.GIF"),
			style={
			"height": "280px",
			"width": "auto",
			"margin-bottom": "25px",
			"margin-left": "100px",
			})
	@app.callback(
		Output("umap", "children"),
		[
			Input('none', 'children'),
		],
		)
	def image_test3(none):
		return html.Img(
			src=app.get_asset_url("UMAP400_12_8.png"),
			style={
			"height": "600px",
			"width": "600px",
			"margin-bottom": "25px",
			})
	@app.callback(
		Output("wordclouds", "children"),
		[
			Input('none', 'children'),
		],
		)
	def image_test4(none):
		return html.Img(
			src=app.get_asset_url("WordClouds400_12_8.png"),
			style={
			"height": "600px",
			"width": "600px",
			"margin-bottom": "25px",
			})