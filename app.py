import streamlit as st
import altair as alt
from vega_datasets import data
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Exocomet Exploration", layout="wide")
st.title("Boxplot Prototype")
st.write("Explore the Minimum and Maximum Radii for the Distributions with this boxplot. This application allows you to explore exocomets in our local galaxy.")
df = pd.read_csv('midtermdata.csv')

df_alt = df.melt(value_vars=["x1", "x2"], var_name="type", value_name="radius")

box = (
    alt.Chart(df_alt)
    .mark_boxplot(extent="min-max")
    .encode(
        x=alt.X("type:N", title="Minimum and Maximum Radii"),
        y=alt.Y("radius:Q", title="Radius (km)"),
        color=alt.Color("type:N", legend=None),
        tooltip=[
            alt.Tooltip("mean(radius):Q", format=".2f", title="Mean"),
            alt.Tooltip("median(radius):Q", format=".2f", title="Median"),
            alt.Tooltip("q1(radius):Q", format=".2f", title="Q1"),
            alt.Tooltip("q3(radius):Q", format=".2f", title="Q3"),
            alt.Tooltip("min(radius):Q", format=".2f", title="Min"),
            alt.Tooltip("max(radius):Q", format=".2f", title="Max"),
            alt.Tooltip("count():Q", title="N"),],))
means_df = df_alt.groupby("type", as_index=False)["radius"].mean().rename(columns={"radius": "mean_radius"})
means = (
    alt.Chart(means_df)
    .mark_point(filled=True, size=80, color="black")
    .encode(
        x=alt.X("type:N"),
        y=alt.Y("mean_radius:Q"),
        tooltip=[alt.Tooltip("mean_radius:Q", format=".2f", title="Mean")],))
chart = alt.layer(box, means).properties(width=700, height=400) 
st.altair_chart(chart, use_container_width=True)
