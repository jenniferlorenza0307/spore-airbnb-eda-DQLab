from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime as dt
from dash import dash_table

# Prepare initial data
df_listings = pd.read_csv("./data/DQLab_listings(22Sep2022).csv", index_col=0)
df_reviews = pd.read_csv("./data/DQLab_reviews(22Sep2022).csv", index_col=0)
df_neighbourhoods = pd.read_csv("./data/DQLab_nieghbourhood(22Sep2022).csv", index_col=0)

df_listings = pd.merge(
    df_listings,
    df_neighbourhoods,
    "left",
    on="neighbourhood"
)
df_listings = pd.merge(
    df_listings,
    df_reviews.groupby("listing_id")['date'].agg(["max"]),
    "left",
    left_on="id", right_index=True
).rename(columns={'max': 'last_review_update'})

# Prepare static line-chart
fig_line = px.line(
    df_reviews.groupby("date")['listing_id'].count().reset_index().rename(columns={'listing_id': 'num_review'}),
    x="date", y="num_review"
)
fig_line.add_vline(x=dt.strptime("2020-03-27", "%Y-%m-%d").timestamp() * 1000,
                   line_dash='dash', annotation_text="27 Mar 2020, Covid-19 movement control law",
                   annotation_position="bottom left",
                   annotation_font_size=10)
fig_line.add_vline(x=dt.strptime("2021-09-08", "%Y-%m-%d").timestamp() * 1000,
                   line_dash='dash', annotation_text="8 Sep 2021, Launch of Vaccinated Travel Lanes (VTL)",
                   annotation_position="left",
                   annotation_font_size=10)
fig_line.add_vline(x=dt.strptime("2022-03-24", "%Y-%m-%d").timestamp() * 1000,
                   line_dash='dash', annotation_text="24 Mar 2022, Relaxations for travel & social restrictions",
                   annotation_position="top left",
                   annotation_font_size=10)

# Define Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

app.layout = dbc.Container([
    # Title
    dbc.Row([
        html.H1(["Singapore Airbnb Data ",
                 html.I(className="fas fa-hotel"), " ",
                 html.I(className="fas fa-bed"), " ",
                 html.I(className="fas fa-suitcase-rolling")]),
        html.H2("Dashboard for Exploratory Data Analysis")
    ], align='start', className="mt-4 mb-5 mx-2"),

    # Some intro & background about the data being used
    # Poin-poin yang hendak disampaikan
    dbc.Row([
        html.P("We are part of a data analytics team from a data management company. "
               "Our client is Singaporean property owners who would like to rent out their properties "
               "through Airbnb marketplace.  Given some historical data of Singapore Airbnb listings and reviews, "
               "along with data of Singapore neighbourhoods name, we are asked to analyze and give insights "
               "in order to help our clients make data-driven and (hopefully) profitable decision.")
    ], className="mb-5 mx-2"),

    dbc.Row([
        html.Div([
            html.H3("Listings Distribution Based on Qualitative/Quantitative Variable"),
            html.P(["Following below are bar chart (left) and histogram chart (right), "
                    "provided to show listings distribution based on qualitative and quantitative variable."])
        ]),
        # (1) Bar Chart: untuk menampilkan distribusi bdk. qualitative variables
        dbc.Col([
            html.Label("Qualitative variable"),
            dcc.Dropdown(id="input-bar",
                         clearable=False,
                         options=["room_type", "neighbourhood", "neighbourhood_group"],
                         value="room_type"
                         ),
            dcc.Graph(id="bar-chart")
        ], width=6),

        # (2) Histogram Chart: untuk menampilkan distribusi bdk. quantitative-Ratio variables
        dbc.Col([
            html.Label("Quantitative variable"),
            dcc.Dropdown(id="input-hist",
                         clearable=False,
                         options=["price", "minimum_nights", "availability_365"],
                         value="price"
                         ),
            dcc.Graph(id="hist-chart")
        ], width=6)
    ], justify='around', className="mb-5 mx-2"),

    # (3) Scatter_mapbox Chart: untuk menampilkan lokasi listings
    dbc.Row([
        html.Div([
            html.H3("Listings Distribution Based on Locations"),
            html.P(["Following below is scatter-map chart to show each individual listing's location "
                    "relative to its latitude-longitude data. User may hover to the data point on the map "
                    "to see the listing's id, name, price, room type, number of reviews, etc. "
                    "In the Map Settings, user may also choose scatter-point coloring and adjust map filters "
                    "to only show listings with fulfilling features. Below the map chart, given the "
                    "data table of all listings currently showed on map, and user may sort it based on a column value."
                    ])
        ]),
        dbc.Col([
            # html.Div([
            #     dcc.Tabs([
            #         dcc.Tab(label="Scatter mapbox", value="smpbox"),
            #         dcc.Tab(label="Choropleth mapbox", value="cmpbox")
            #     ], id="input-map-type", value="smpbox")
            # ]),
            html.Div(className="border-bottom p-3 bg-light text-dark fs-5", children=[
                html.Label("Map Settings")
            ]),
            html.Div(title="scatter-point coloring", className="mt-1 mb-1 border border-info rounded-2", children=[
                html.Label("Color based on:"),
                dcc.RadioItems(id="input-smpbox-color",
                               options=[{'label': 'Room Type', 'value': 'room_type'},
                                        {'label': 'Neighbourhood Group', 'value': 'neighbourhood_group'},
                                        {'label': 'Neighbourhood', 'value': 'neighbourhood'}],
                               value='room_type'
                               ),
            ]),
            html.Div(title="map filters", className="mt-1 mb-1 border border-dark rounded-2", children=[
                html.Label("Room Type filter"),
                dcc.Dropdown(id="input-qual-room",
                             multi=True,
                             options=df_listings['room_type'].unique(),
                             value=[]
                             ),

                html.Label("Neighbourhood Group filter"),
                dcc.Dropdown(id="input-qual-ng",
                             multi=True,
                             options=df_neighbourhoods['neighbourhood_group'].unique(),
                             value=[]
                             ),

                html.Label("Neighbourhood filter"),
                dcc.Dropdown(id="input-qual-n",
                             multi=True, value=[]),

                html.Label("Maximum Price: "),
                # dcc.Dropdown(id="input-quan-price",
                #              multi=True,
                #              options=[{'label': '< $50', 'value': [0,50]},
                #                       {'label': '$50 to < $100', 'value': [50,100]},
                #                       {'label': '$100 to < $200', 'value': [100,200]},
                #                       {'label': '$200 to < $500', 'value': [200,500]},
                #                       {'label': '≥ $500', 'value': [500, df_listings['price'].max()+1]}],
                #              value=[0,50]
                #              ),
                dcc.Input(id="input-quan-price",
                          type='number',
                          value=100,
                          min=0),

                html.Label("Minimum night(s) to stay"),
                dcc.RangeSlider(id="input-quan-mn",
                                min=1,
                                max=df_listings['minimum_nights'].max(),
                                step=3,
                                value=[1, 7],
                                marks={
                                    30: '30',
                                    90: '90',
                                    180: '180',
                                   360: '360'
                                },
                                tooltip={"placement": "bottom", "always_visible": True}),

                html.Label("Availability 365 days"),
                dcc.RangeSlider(id="input-quan-av",
                                min=0,
                                max=365,
                                value=[360, 365],
                                marks={
                                    30: '30',
                                    90: '90',
                                    180: '180',
                                   360: '360'
                                    },
                                tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label("Date range for Last Reviews Update filter"),
                dcc.DatePickerRange(
                    id="input-quan-lru",
                    display_format="YYYY-MMM-DD",
                    minimum_nights=0,
                    clearable=True,
                    updatemode='bothdates',
                    min_date_allowed=dt.strptime(df_reviews['date'].min(), '%Y-%m-%d'),
                    max_date_allowed=dt.strptime(df_reviews['date'].max(), '%Y-%m-%d')
                ),
                dcc.Checklist(
                    [{'label': 'Filter out listings with no reviews given', 'value': True}],
                    id="input-quan-lru_none",
                    value=[]
                ),

                html.Label("Date range for Num. Reviews calculation"),
                dcc.DatePickerRange(
                    id="input-quan-nr",
                    display_format="YYYY-MMM-DD",
                    minimum_nights=0,
                    clearable=True,
                    updatemode='bothdates',
                    min_date_allowed=dt.strptime(df_reviews['date'].min(), '%Y-%m-%d'),
                    max_date_allowed=dt.strptime(df_reviews['date'].max(), '%Y-%m-%d')
                ),
            ]),
            html.Div(title="scorecard", className="mt-3 mb-3 border border-success rounded-3", children=[
                html.P("Total number of listings displayed on map", className="mb-1 fst-italic text-center"),
                html.P(id='output-card-nlistings', className="mt-0 mb-1 fw-bolder fs-1 text text-center")
            ])
        ], width=4),
        dbc.Col([
            dcc.Graph(id="mpbox-chart"),
        ], width=8),

        # Add data table to show data detail from map
        html.Div([
            html.Label("Listings Detail Information", className="fst-italic"),
            dash_table.DataTable(id="mpbox-datatable",
                                sort_action='native',
                                page_size=5,
                                style_table={'overflowX':'auto'}
                                ),
        ]),
    ], className="mb-5 mx-2"),
    dbc.Row([
        html.Div([
            html.H3("Listings Rental Trend, 2018-2022"),
            html.P(["Although the data provided does not include listings rental transactions, ",
                    "it is possible to infer listings total rent activities based on ",
                    "the total number of listings' user reviews."
                    ])
        ]),
        dcc.Graph(id="line-chart", figure=fig_line)
    ], className="mb-5 mx-2")
], fluid=True)


@app.callback(
    Output(component_id="bar-chart", component_property="figure"),
    Input(component_id="input-bar", component_property="value")
)
def update_barchart(variable_name):
    dff = df_listings.groupby(by=[variable_name]).id.count().reset_index().sort_values(by="id")
    fig = px.bar(dff, x="id", y=variable_name, orientation="h",
                 labels={'id': 'Number of listings'})
    return fig



@app.callback(
    Output(component_id="hist-chart", component_property="figure"),
    Input(component_id="input-hist", component_property="value")
)
def update_histchart(variable_name):
    fig = px.histogram(df_listings, x=variable_name)
    return fig



@app.callback(
    Output("input-qual-n", "options"),
    Input("input-qual-ng", "value")
)
def update_qual_n_options(filter_ng):
    if filter_ng:
        q = "neighbourhood_group in " + str(filter_ng)
        options = df_neighbourhoods.query(q)['neighbourhood']
        return options
    else:
        return df_neighbourhoods['neighbourhood']


@app.callback(
    Output(component_id="mpbox-chart", component_property="figure"),
    Output("output-card-nlistings", "children"),
    [Output("mpbox-datatable", "data"),
     Output("mpbox-datatable", "columns"),
     Output("mpbox-datatable", "tooltip_data")],
    Input(component_id="input-smpbox-color", component_property="value"),
    Input("input-qual-room", "value"),
    Input("input-qual-ng", "value"),
    Input("input-qual-n", "value"),
    Input("input-quan-price", "value"),
    Input("input-quan-mn", "value"),
    Input("input-quan-av", "value"),
    [Input("input-quan-lru", "start_date"), Input("input-quan-lru", "end_date")],
    Input("input-quan-lru_none", "value"),
    [Input("input-quan-nr", "start_date"), Input("input-quan-nr", "end_date")],
)
def update_mpboxchart(color_var, filter_room, filter_ng, filter_n, price_max, mn_thres, av_thres,
                       lru_start, lru_end, drop_lru_none, nr_start, nr_end):
    d1 = df_listings.copy(deep=True)

    # Filtering for room_type
    if filter_room:
        q = "room_type in " + str(filter_room)
        d1 = d1.query(q)

    # Filtering for neighbourhood_group
    if filter_ng:
        q = "neighbourhood_group in " + str(filter_ng)
        d1 = d1.query(q)

    # Filtering for neighbourhood
    if filter_n:
        q = "neighbourhood in " + str(filter_n)
        d1 = d1.query(q)

    # Filtering for price
    if price_max is not None:
        d1 = d1[d1['price'].between(0, price_max)]

    # Filtering for minimum_nights
    d1 = d1[d1['minimum_nights'].between(mn_thres[0], mn_thres[1])]

    # Filtering for availability_365
    d1 = d1[d1['availability_365'].between(av_thres[0], av_thres[1])]

    # Filtering for last_review_update
    if lru_start and lru_end:
        d1 = d1[d1['last_review_update'].between(lru_start, lru_end) | d1['last_review_update'].isna()]
    if drop_lru_none:
        d1 = d1[d1['last_review_update'].notna()]
    d1['last_review_update'] = d1['last_review_update'].fillna("N/A")

    # Filtering for & calculating num_reviews
    if nr_start and nr_end:
        d1 = pd.merge(d1,
                      df_reviews[df_reviews['date'].between(nr_start, nr_end)].groupby("listing_id").agg(["count"])["date"],
                      "left", left_on="id", right_index=True
                      ).rename(columns={'count': 'num_review'})
    else:
        d1 = pd.merge(d1,
                      df_reviews.groupby("listing_id").agg(["count"])["date"],
                      "left", left_on="id", right_index=True
                      ).rename(columns={'count': 'num_review'})
    d1['num_review'] = d1['num_review'].fillna(0)

    # print(d1.neighbourhood_group.unique())
    # print(d1.neighbourhood.unique())
    # print(d1.room_type.unique())
    # print(df_listings.minimum_nights.min())
    # print(type(price_max))
    # print(type(lru_start), lru_start, type(lru_end), lru_end)

    fig = px.scatter_mapbox(d1, lat="latitude", lon="longitude",
                            hover_name="id",
                            color=color_var,
                            hover_data=["name", "price", "minimum_nights",
                                        "availability_365", "room_type",
                                        "last_review_update", "num_review"],
                            mapbox_style="open-street-map",
                            height=700
                            )

    # Prepare for mpbox-datatable output
    cols = [{"name": i, "id": i} for i in d1.columns]
    tooltip_data = [
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in d1.to_dict(orient='records')
    ]

    return fig, d1["id"].count(), d1.to_dict(orient='record'), cols, tooltip_data



if __name__ == "__main__":
    app.run_server(port=8050, debug=True)