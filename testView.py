from dash import Dash, Input, Output, html, dcc
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.MORPH], title="IoT", suppress_callback_exceptions=True)


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f2f1ed",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dashboard", className="display-5"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Login", href="/", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#Light Card
lightCard = dbc.Card(
    [
        dbc.CardImg(id="lightImg", src="/assets/lightOff.jpg", top=True),
        dbc.CardBody(
            [
                dbc.Button("Turn On", color="primary", id="lightButton"),
            ]
        ),
    ],
    style={"width": "18rem"},
    className="bg-info"
)

row = dbc.Row(
    [
        dbc.Col(html.Div(lightCard)),
        dbc.Col(html.Div("One of three columns")),
        dbc.Col(html.Div("One of three columns")),
    ],
    className="pad-row",
    align="center"
)
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return row
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        
        className="p-3 bg-light rounded-3",
    )


#Turn on/off light
@app.callback(
    Output("lightImg", "src"),
    Output("lightButton", "children"),
    Input("lightButton", "n_clicks"),
)
def on_button_click(n_clicks):
    if n_clicks is None:
        return '/assets/lightOff.jpg', "Turn On"
    if n_clicks % 2 == 1:
        return '/assets/lightOn.jpg', "Turn Off"
    else:
        return '/assets/lightOff.jpg', "Turn On"


if __name__ == '__main__':
    app.run(debug=True)