from flask import Flask
import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Crear la aplicación Flask principal
server = Flask(__name__)

# ----------------------------- #
# Dash App 1 - Página Principal #
# ----------------------------- #
app_dash_inicio = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix="/inicio/"
)
app_dash_inicio.layout = html.Div([
    html.H1("Bienvenido al Portal Mujeres STEM Bolivia"),
    html.P("Explora nuestras secciones dedicadas a mujeres en STEM."),
    html.Div([
        dcc.Link("Mapa Interactivo de Mujeres STEM", href="/mujeres_stem/", style={'display': 'block'}),
        dcc.Link("Papers y Proyectos STEM", href="/papers_stem/", style={'display': 'block'})
    ])
])

# ------------------------------ #
# Dash App 2 - Mapa Mujeres STEM #
# ------------------------------ #
app_dash_mujeres = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix="/mujeres_stem/"
)
df_mujeres = pd.read_csv("data/Mujeres STEM Bolivia ofi.csv")
fig_mujeres = px.scatter_mapbox(
    df_mujeres,
    lat="Latitud",
    lon="Longitud",
    color="Campo STEM",
    hover_name="Nombre",
    zoom=5
)
fig_mujeres.update_layout(mapbox_style="carto-positron")

app_dash_mujeres.layout = html.Div([
    html.H1("Mapa Interactivo de Mujeres STEM"),
    dcc.Graph(figure=fig_mujeres),
    dcc.Link("Volver al Inicio", href="/inicio/")
])

# ----------------------------- #
# Dash App 3 - Papers STEM      #
# ----------------------------- #
app_dash_papers = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix="/papers_stem/"
)
df_papers = pd.read_csv("data/Papers_proyectos STEM.csv")
df_papers = df_papers.dropna(subset=["TÍTULO", "CATEGORÍA"])

app_dash_papers.layout = html.Div([
    html.H1("Papers y Proyectos STEM"),
    html.Table([
        html.Tr([html.Th(col) for col in df_papers.columns]),
        *[html.Tr([html.Td(df_papers.iloc[i][col]) for col in df_papers.columns])
          for i in range(len(df_papers))]
    ]),
    dcc.Link("Volver al Inicio", href="/inicio/")
])

# ---------------------------- #
# Rutas Flask para Redirección #
# ---------------------------- #
@server.route("/")
def redirect_inicio():
    return """<meta http-equiv="refresh" content="0; URL='/inicio/'" />"""

# ---------------------------- #
# Iniciar Servidor Flask       #
# ---------------------------- #
if __name__ == "__main__":
    server.run(debug=True, port=5000)
