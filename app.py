from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Rutas de datos
DATA_MUJERES_STEM = "data/Mujeres STEM Bolivia ofi.csv"
DATA_PAPERS_STEM = "data/Papers_proyectos STEM.csv"

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")

# Página Mujeres STEM
@app.route("/mujeres_stem")
def mujeres_stem():
    df = pd.read_csv(DATA_MUJERES_STEM)
    fig = px.scatter_mapbox(
        df,
        lat="Latitud",
        lon="Longitud",
        color_discrete_sequence=px.colors.qualitative.Prism,
        hover_data={"Nombre": True, "Campo STEM": True, "Institución": True},
        zoom=5,
    )
    fig.update_layout(mapbox_style="carto-positron", margin={"r": 0, "t": 0, "l": 0, "b": 0})
    plot_html = fig.to_html(full_html=False)
    return render_template("mujeres_stem.html", plot_html=plot_html)

# Página Papers STEM
@app.route("/papers_stem")
def papers_stem():
    df = pd.read_csv(DATA_PAPERS_STEM)
    df_clean = df.dropna(subset=["TÍTULO", "CATEGORÍA"])
    return render_template("papers_stem.html", tables=df_clean.to_html(classes='table table-striped'), titles=df_clean.columns.values)

# Página de Inicio con botones de acceso
@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

server = app.server

# Servidor Flask principal
if __name__ == "__main__":
    app.run(debug=True, port=5000)
