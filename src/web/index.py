import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import my_app.temporal_callbacks as tc
import my_app.spatial_callbacks  as spc
import my_app.home_callbacks as hoc
import my_app.temporal_layout as tl
import my_app.spatial_layout  as spl
import my_app.home_layout as hol

external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app.title='UVict'


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Analisis Temporal", href="/temporal")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Analisis espacial", href="/spatial"),
                dbc.DropdownMenuItem("Home", href="/home"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="UVict", brand_href="#", color="primary", dark=True,
)

app.layout = dbc.Container(fluid=True, children=[
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.Br(),
    ## Top
    html.H1(children = 'Repositorio de noticias',
        style = {'textAlign': 'center'}
    ),
    html.Br(),
    navbar,

    # content will be rendered in this element
    html.Div(id='page-content')
])

# Activa la ventanita
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/temporal':
        return tl.content
    elif pathname == "/spatial":
        return spl.content
    elif pathname == "/home":
        return hol.content
    return tl.content


tc.register_callbacks(app)
spc.register_callbacks(app)
hoc.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
