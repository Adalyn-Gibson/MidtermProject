import streamlit as st
import altair as alt
from vega_datasets import data
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Exocomet Exploration", layout="wide")
st.image("/Users/adalyngibson/Documents/Github/MidtermProject/figures/comet_picture.jpg", caption="Comet Illustration from Star Walk")
st.write("What is an exocomet? An exocomet is like any comet in our solar system, think of the icy spherical bodies with large tails as pictured above, but the exo means it exists in another stellar systems, orbiting a star other than our Sun. Scientists care about gaining an understanding of exocomets because of their applications to planet formation science and to interstellar object science. Interstellar objects are exocomets that have escaped their system and have ended up in ours!")


st.title("Distribution of Exocomet and Comet Radii")
st.write("Explore the Minimum and Maximum Radii for the Distributions with this boxplot. This application allows you to explore exocomets in our local galaxy by viewing the distributions of the minimum and maximum radii for all populations. Click on the boxes to view details of the minimum and maximum radii.")


df = pd.read_csv('/Users/adalyngibson/Documents/Github/MidtermProject/data/midtermdata.csv')


df_alt = df.melt(value_vars=["x1", "x2"], var_name="type_raw", value_name="radius")
df_alt["type"] = df_alt["type_raw"].map({"x1": "Min Radius", "x2": "Max Radius"})

box = (
    alt.Chart(df_alt)
    .mark_boxplot(extent="min-max", size=60)
    .encode(
        x=alt.X("type:N", title="Minimum and Maximum Radii Across All Populations", sort=["Min Radius", "Max Radius"], axis=alt.Axis(labelFontSize=22, titleFontSize=22, labelAngle=0)),
        y=alt.Y("radius:Q", title="Radius of (Exo)Comet(km)", axis=alt.Axis(labelFontSize=22, titleFontSize=22)),
        color=alt.Color("type:N", scale=alt.Scale(
                domain=["Min Radius", "Max Radius"],
                range=["#70D6FF", "#FF9770"] 
            ),legend=None), stroke=alt.value("white")))

chart_box = (alt.layer(box).properties(width=800, height=450, title="Radius Distribution for all Populations").configure_title(fontSize=22).configure_axis(labelFontSize=22, titleFontSize=22))

st.altair_chart(chart_box, use_container_width=True)
#display(chart_box)
# adapting from matplotlib to altair
# bp = beta pic
# rz = rz psc

st.title("Cumulative Size Distribution of Exocomet and Comet Radii")
st.write("Explore what the size distribution of exocomets in the local galaxy look like. This visualization shows how many exocomets exist in a system above a certain radius (units of kilometers (km) - 1 km is the size of a soccer field). RZ Psc has two populations of exocomets represented by the broken size distribution in blue. The dotted lines represent the different solar system comet populations and the solid lines represent the different exocomet systems. Click on the line to view specifics of the system.")


df_bp = df[df["TIC_ID"] == 270577175].copy()
row_bp = df_bp.iloc[0]

df_rz = df[df["TIC_ID"] == 15693497].copy()
row_rz_0 = df_rz.iloc[0]
row_rz_1 = df_rz.iloc[1]

df_solor = df[(df["TIC_ID"] != 270577175) & (df["TIC_ID"] != 15693497)].copy()

bp_df = pd.DataFrame([{
    "star": row_bp["star"],
    "spec_type": row_bp["spec_type"],
    "telescope": row_bp["telescope"],
    "x1": row_bp["x1"],
    "x2": row_bp["x2"],
    "y1": row_bp["y1"],
    "y2": row_bp["y2"]
}])


rz_df = pd.DataFrame([
    {
        "star": row_rz_0["star"],
        "spec_type": row_rz_0["spec_type"],
        "telescope": row_rz_0["telescope"],
        "x1": row_rz_0["x1"],
        "x2": row_rz_0["x2"],
        "y1": row_rz_0["y1"],
        "y2": row_rz_0["y2"]
    },
    {
        "star": row_rz_1["star"],
        "spec_type": row_rz_1["spec_type"],
        "telescope": row_rz_1["telescope"],
        "x1": row_rz_1["x1"],
        "x2": row_rz_1["x2"],
        "y1": row_rz_1["y1"],
        "y2": row_rz_1["y2"]
    }
])


solar_df = df_solor[["star", "spec_type", "telescope", "x1", "x2", "y1", "y2"]].copy()


bp_chart = (
    alt.Chart(bp_df)
    .mark_rule(color="white", strokeWidth=2)
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(type="log"), title="Radius of (Exo)Comet(km)", axis=alt.Axis(titleFontSize=22)), 
        x2="x2:Q",
        y=alt.Y("y1:Q", scale=alt.Scale(type="log"), title="Cumulative Number of Excomets / day (>R)", axis=alt.Axis(titleFontSize=22)),
        y2="y2:Q",
        tooltip=["star:N", "spec_type:N", "telescope:N"]
    )
)

rz_chart = (
    alt.Chart(rz_df)
    .mark_rule(color="black", strokeWidth=2)
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(type="log")),
        x2="x2:Q",
        y=alt.Y("y1:Q", scale=alt.Scale(type="log")),
        y2="y2:Q",
        color=alt.Color("star:N", legend=None),
        tooltip=["star:N", "spec_type:N", "telescope:N"]
    )
)


solar_chart = (
    alt.Chart(solar_df)
    .mark_rule(color="lightgray", opacity=0.7, strokeDash=[6, 3])
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(type="log")),
        x2="x2:Q",
        y=alt.Y("y1:Q", scale=alt.Scale(type="log")),
        y2="y2:Q",
        tooltip=["star:N", "spec_type:N", "telescope:N"]
    )
)

chart_scat = (
    solar_chart
    + rz_chart
    + bp_chart
).properties(
    width=800,
    height=800,
    title=alt.TitleParams(
        text="Beta Pictoris vs. RZ Psc vs. Solar System Populations",
        fontSize=22)
).interactive()
st.altair_chart(chart_scat)
#display(chart_scat)
