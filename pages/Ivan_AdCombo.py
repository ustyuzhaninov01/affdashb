import numpy as np
import openpyxl as op
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st

st.set_page_config(
    page_title="AFFDASH",
    page_icon=":phone:",
    initial_sidebar_state="expanded",
    layout="wide",
)

def get_data_from_excel():
    df = pd.read_excel(
        io="reports/dar.xlsx",
        engine="openpyxl",
        skiprows=0,
        #usecols="B:R",
        #nrows=1000,
    )

    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')


    return df

df = get_data_from_excel()
st.dataframe(df)

tokens_by_month = df.sort_values(by=["date"], ascending=True).groupby('date').count()

tokens_by_csi = df.groupby(by=["status"]).count()[["id"]]
tokens_by_com = df.groupby(by=["question"]).count()[["id"]]


fig_tokens_by_month = px.bar(
    tokens_by_month,
    x=tokens_by_month.index,
    y="id",
    text="id",
    title="<b>Tokens by day</b>",
    color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
    template="plotly_white",
)

st.plotly_chart(fig_tokens_by_month, use_container_width=True)





# Convert the timestamp column to a datetime object
df["date"] = pd.to_datetime(df["date"])

# Group the data by date and in_out
tokens_by_date_inout = df.groupby([df["date"].dt.date, "in_out"]).count()[["id"]]

# Reset the index to flatten the multi-index dataframe
tokens_by_date_inout = tokens_by_date_inout.reset_index()

# Rename the columns for clarity
tokens_by_date_inout.columns = ["date", "in_out", "count"]

# Create a pivot table to reshape the data for plotting
tokens_by_date_inout_pivot = tokens_by_date_inout.pivot(index="date", columns="in_out", values="count")

# Create the bar chart
fig_tokens_by_date_inout = go.Figure()
fig_tokens_by_date_inout.add_trace(go.Bar(
    x=tokens_by_date_inout_pivot.index,
    y=tokens_by_date_inout_pivot["in"],
    name="in",
    marker_color="#0083B8"
))
fig_tokens_by_date_inout.add_trace(go.Bar(
    x=tokens_by_date_inout_pivot.index,
    y=tokens_by_date_inout_pivot["out"],
    name="out",
    marker_color="#FFA15A"
))
fig_tokens_by_date_inout.update_layout(
    barmode="stack",
    title="<b>Tokens by in_out, by day</b>",
    xaxis=dict(tickmode="linear"),
    yaxis=dict(showgrid=False),
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_tokens_by_date_inout, use_container_width=True)









fig_tokens_by_csi = px.bar(
     tokens_by_csi,
       x=tokens_by_csi.index,
       y="id",
       text="id",
       title="<b>Tokens by status</b>",
       color_discrete_sequence=["#0083B8"] * len(tokens_by_csi),
       template="plotly_white",
    )
fig_tokens_by_csi.update_layout(
       xaxis=dict(tickmode="linear"),
       plot_bgcolor="rgba(0,0,0,0)",
       yaxis=(dict(showgrid=False)),
    )
st.plotly_chart(fig_tokens_by_csi, use_container_width=True)



fig_tokens_by_com = px.bar(
     tokens_by_com,
       x=tokens_by_com.index,
       y="id",
       text="id",
       title="<b>Tokens by question</b>",
       color_discrete_sequence=["#0083B8"] * len(tokens_by_com),
       template="plotly_white",
    )
fig_tokens_by_com.update_layout(
       xaxis=dict(tickmode="linear"),
       plot_bgcolor="rgba(0,0,0,0)",
       yaxis=(dict(showgrid=False)),
    )
st.plotly_chart(fig_tokens_by_com, use_container_width=True)





