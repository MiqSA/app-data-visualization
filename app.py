import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import requests
from pandas import json_normalize

# Databases
data = pd.read_csv("data-science/datasets/f_comex.csv", sep=';')
# API products
url = 'http://127.0.0.1:5000/products'
data_url = requests.get(url)
# Store the API response in a variable.
available_data = data_url.json()
data_d_sh2 = json_normalize(available_data)


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
                                for product in data_d_sh2.NO_NCM_POR.apply(lambda x: x[0:30]+' ...' if len(x)>=30 else x).unique()
                            ],
                            value='Outras obras de plásticos',
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),

            ],
            className="menu",
        ),

        html.Br(),
        html.Div(
            children=[
                html.H1(className="header-total", id="card_num1"),
                html.P(
                    children="Total Movimentado",
                    className="header-description-total",
                ),
            ],
            className="wrapper"
        ),

        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="movements-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="via-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.H2(children="Total por Estado", className="header-total"),
                html.Br(),
                html.Div(id="table-states", className="table-wrapper", ),

            ],
            className="wrapper",
        ),
        html.Br(),
        html.Br(),
        html.Br(),
    ]
)


@app.callback(
    [
        Output('card_num1', 'children'),
        Output("movements-chart", "figure"),
        Output("via-chart", "figure"),
        Output('table-states', 'children'),

    ],
    [
        Input("year-filter", "value"),
        Input("movements-filter", "value"),
        Input("product-filter", "value"),
    ],
)
def update_charts(year, movement_type, product):
    # API vias
    url = 'http://127.0.0.1:5000/vias'
    data_url = requests.get(url)
    # Store the API response in a variable.
    available_data = data_url.json()
    data_d_via = json_normalize(available_data)

    product_list = data_d_sh2.NO_NCM_POR.apply(lambda x: x[0:30] + ' ...' if len(x) >= 30 else x)
    product_list = product_list.to_frame().rename(columns={'NO_NCM_POR': 'PRODUCT_LIST'})
    new_data_d_sh2 = pd.concat([data_d_sh2, product_list], axis=1)
    product_find = new_data_d_sh2.query(f"PRODUCT_LIST == '{product}'")['CO_NCM']

    # print('\nproduct_find', product_find)

    product_NCM = int(product_find)

    mask = (
            (data.ANO == year)
            & (data.MOVIMENTACAO == movement_type)
            & (data.COD_NCM == product_NCM)
    )
    filtered_data = data.loc[mask, :]
    data_normal = pd.crosstab([filtered_data['MOVIMENTACAO']], filtered_data['MES'], )


    old = list(data_d_via['CO_VIA'].apply(lambda x: int(x)))
    new = list(data_d_via['NO_VIA'])
    via_filtered = filtered_data['COD_VIA'].replace(old, new)
    via_filtered = via_filtered.to_frame().rename(columns={'COD_VIA': 'VIA'})
    result = pd.concat([filtered_data, via_filtered], axis=1)
    total = sum(filtered_data['VL_QUANTIDADE'])

    total_state = filtered_data['SG_UF'].value_counts(normalize=True)
    total_normal = total_state.to_frame()
    total_state = filtered_data['SG_UF'].value_counts()
    total_state = total_state.to_frame()
    total_state['INFLUENCIA'] = total_normal
    total_state.reset_index(level=0, inplace=True)
    total_state.rename(columns={'index': 'ESTADO', 'SG_UF': 'VALOR'}, inplace=True)
    total_state['INFLUENCIA'] = total_state['INFLUENCIA'].apply(lambda x: f'{round(x * 100, 2)}%')

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

    via_figure = {
        "data": [
            {
                "values": result['VL_QUANTIDADE'],
                "labels": result['VIA'],
                "type": "pie",
                "insidetextfont": {"color": "white"},
                "texttemplate": "%{percent:.2%f}",
            }
        ],
        "layout": {
            "title": {
                "text": "Utilização da VIA",
                "x": 0.05,
                "xanchor": "left",
            },
            "legend": {"x": 0, "y": 0},
        },

    }
    table = html.Table(className="table-wrapper",
                       children=[
                           html.Thead(
                               html.Tr(
                                   children=[
                                       html.Th(col.title()) for col in total_state.columns.values],
                                   style={'background-color': 'rgb(0, 158, 225)',
                                          'font-size': 18,
                                          'text-align': 'center', },

                               )
                           ),
                           html.Tbody(
                               [

                                   html.Tr(
                                       children=[
                                           html.Td(data) for data in d
                                       ],
                                   )
                                   for d in total_state.values.tolist()])
                       ]
                       )

    return total, movements_hist_figure, via_figure, table


if __name__ == "__main__":
    app.run_server(debug=True)
