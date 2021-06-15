import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("data-science/datasets/f_comex.csv", sep=';')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Análise do Comércio Exterior"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🤝", className="header-emoji"),
                html.H1(
                    children="Análise do Comércio Exterior", className="header-title"
                ),
                html.P(
                    children="Análise das movimentações do comércio exterior entre 2018 a 2020 com o Brasil.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Ano", className="menu-title"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[
                                {"label": year, "value": year}
                                for year in np.sort(data.ANO.unique())
                            ],
                            value=2020,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Movimentação", className="menu-title"),
                        dcc.Dropdown(
                            id="movements-filter",
                            options=[
                                {"label": movement_type, "value": movement_type}
                                for movement_type in data.MOVIMENTACAO.unique()
                            ],
                            value="Exportação",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Produto", className="menu-title"),
                        dcc.Dropdown(
                            id="product-filter",
                            options=[
                                {"label": product, "value": product}
                                for product in data.COD_NCM.unique()
                            ],
                            value=39269090,
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="movements-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("movements-chart", "figure"),
    [
        Input("year-filter", "value"),
        Input("movements-filter", "value"),
        Input("product-filter", "value"),
    ],
)
def update_charts(year, movement_type, product):
    mask = (
            (data.ANO == year)
            & (data.MOVIMENTACAO == movement_type)
            & (data.COD_NCM == product)
    )
    filtered_data = data.loc[mask, :]
    data_normal = pd.crosstab([filtered_data['MOVIMENTACAO']], filtered_data['MES'], )

    movements_hist_figure = {
        "data": [
            {"y": pd.Series(data_normal.values[0]),
             "x": ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'],
             "type": "bar",
             "hovertemplate": "%{y:.2f}<extra></extra>",
             },
        ],
        "layout": {
            "title": {
                "text": "Quantidade de Produtos Movimentados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#09a0db"],
            "bargap": 0.2,
        },
    }

    return movements_hist_figure


if __name__ == "__main__":
    app.run_server(debug=True)
