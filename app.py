
import pandas as pd
import streamlit as st

st.title("Generateur de scenarios AEB")

donnees = pd.read_csv("resultats.csv", sep=";")

toutes_les_routes = list(donnees["route"].unique())
routes_choisies = st.multiselect("Route", toutes_les_routes, default=toutes_les_routes)

filtre = donnees[donnees["route"].isin(routes_choisies)]
nombre_collisions = int((filtre["verdict"] == "collision").sum())

st.metric("Scenarios", len(filtre))
st.metric("Collisions", nombre_collisions)

st.dataframe(filtre)