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
    )
    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    return df


df = get_data_from_excel()

# Identify duplicate "id" rows with "waiting answers" status


tokens_by_month = df.sort_values(by=["date"], ascending=True).groupby('date').count()
# Identify duplicates based on "id"

df['id'] = df['id'].astype(str)

# Display the DataFrame using st.dataframe()
with st.expander("Dataframe"):
    st.dataframe(df)

# Expander 1 - Tokens by day
with st.expander("Tokens by Day"):
    fig_tokens_by_month = px.bar(
        tokens_by_month,
        x=tokens_by_month.index,
        y="id",
        text="id",
        title="<b>Tokens by day</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_month),
        template="plotly_white",
    )
    fig_tokens_by_month.update_layout(
        xaxis=dict(tickmode="auto", nticks=15, tickformat="%b %d" if len(tokens_by_month.index) > 30 else "%b"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_tokens_by_month, use_container_width=True)


# Expander 2 - Tokens by in_out, by day
with st.expander("Tokens by In/Out, by Day"):
    df["date"] = pd.to_datetime(df["date"])
    tokens_by_date_inout = df.groupby([df["date"].dt.date, "in_out"]).count()[["id"]]
    tokens_by_date_inout = tokens_by_date_inout.reset_index()
    tokens_by_date_inout.columns = ["date", "in_out", "count"]
    tokens_by_date_inout_pivot = tokens_by_date_inout.pivot(index="date", columns="in_out", values="count")

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
        xaxis=dict(tickmode="auto", nticks=15, tickformat="%b %d" if len(tokens_by_date_inout_pivot.index) > 30 else "%b"),
        yaxis=dict(showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_tokens_by_date_inout, use_container_width=True)






tokens_by_qd = df.groupby([df["question"], df["date"].dt.date]).count()[["id"]]

# Reset the index to make "question" and "date" accessible as columns
tokens_by_qd = tokens_by_qd.reset_index()

# Expander - Tokens by Question by Day
with st.expander("Tokens by Question by Day!"):
    fig_tokens_by_qd = px.bar(
        tokens_by_qd,
        x="date",
        y="id",
        text="id",
        title="<b>Tokens by Question by Day</b>",
        color="question",
        color_discrete_sequence=px.colors.qualitative.Set1,
        template="plotly_white",
    )
    fig_tokens_by_qd.update_layout(
        xaxis=dict(tickmode="auto", nticks=15, tickformat="%b %d" if len(tokens_by_qd["date"].unique()) > 30 else "%b"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_tokens_by_qd, use_container_width=True)




duplicates = df[df["status"] == "waiting answers"].duplicated(subset="id", keep=False)

# Update the status to "activate" for duplicate "id" rows with "waiting answers" status
# Drop the duplicate "id" rows with "waiting answers" status
df = df.drop_duplicates(subset=["id", "status"])

# Group by "status" and count the occurrences of "id"
tokens_by_csi = df.groupby("status").count()[["id"]]

# Expander 3 - Tokens by status
with st.expander("Tokens by Status"):
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


def get_data_from_excel():
    df1 = pd.read_excel(
        io="reports/dar.xlsx",
        engine="openpyxl",
        skiprows=0,
        sheet_name="Planilha2"
    )
    return df1

df1 = get_data_from_excel()

# Expander 5 - Active/Suspended by month
with st.expander("Active/Suspended by Month"):
    st.dataframe(df1)

    # Create the DataFrame
    data = {
        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dec'],
        'suspended': [236, 330, 251, 172, 160, 61, None, None, None, None, None, None],
        'active': [133, 118, 85, 98, 135, 33, None, None, None, None, None, None]
    }

    df = pd.DataFrame(data)
    # Remove rows with missing values
    df = df.dropna()

    # Create the bar chart
    fig_status_by_month = go.Figure(data=[
        go.Bar(name='Suspended', x=df['month'], y=df['suspended']),
        go.Bar(name='Active', x=df['month'], y=df['active'])
    ])

    fig_status_by_month.update_layout(
        title='Status by Month',
        xaxis_title='Month',
        yaxis_title='Count',
        barmode='group'
    )

    st.plotly_chart(fig_status_by_month, use_container_width=True)









