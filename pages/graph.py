import numpy as np
import openpyxl as op
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt


# Load data from Excel
def get_data_from_excel():
    df5 = pd.read_excel(
        io="reports/stats.xlsx",
        engine="openpyxl",
        skiprows=0,
        sheet_name="stats-2023-10-03 17_58",
    )
    return df5

df5 = get_data_from_excel()


tokens_by_sales = df5
# Identify duplicates based on "id"

df5['offer_id'] = df5['offer_id'].astype(str)

# Expander 1 - Tokens by sales
with st.expander("Top 10 offers of the week by sales(Approval rate)"):

    fig_tokens_by_sales = px.bar(
        tokens_by_sales,
        x="offer_id",
        y="approve",  # Используем процент от общей суммы на y-ось
        text="approve",  # Отображаем проценты на графике
        title="<b>Top 10 offers of the week by apprvoe</b>",
        color_discrete_sequence=["#0083B8"] * len(tokens_by_sales),
        template="plotly_white",
    )
    fig_tokens_by_sales.update_layout(
        xaxis=dict(tickmode="auto", nticks=10, tickformat="%b %d" if len(tokens_by_sales.index) > 10 else "%b"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, tickformat="%"),  # Устанавливаем формат в процентах
    )
    st.plotly_chart(fig_tokens_by_sales, use_container_width=True)



def get_data_from_excel():
    df6 = pd.read_excel(
        io="reports/stats.xlsx",
        engine="openpyxl",
        skiprows=0,
        sheet_name="stats-2023-10-03 17_58",
    )
    return df6

df6 = get_data_from_excel()


tokens_by_sales1 = df6
# Identify duplicates based on "id"

df5['offer_id'] = df5['offer_id'].astype(str)

# Expander 2 - Pie Chart for Tokens by sales
with st.expander("Top 10 offers of the week by sales (Pie Chart)"):
    # Вычисляем сумму всех продаж
    total_sales = tokens_by_sales1["sales"].sum()

    # Вычисляем процент от общей суммы для каждой строки
    tokens_by_sales1["percent_of_total_sales"] = (tokens_by_sales1["sales"] / total_sales) * 100

    fig_pie_chart = px.pie(
        tokens_by_sales1,
        names="offer_id",
        values="percent_of_total_sales",  # Используем процент от общей суммы как значения
        title="<b>Top 10 offers of the week by sales (Pie Chart)</b>",
        template="plotly_white",
    )

    # Добавляем проценты на куски пирога
    fig_pie_chart.update_traces(textinfo="percent+label")

    st.plotly_chart(fig_pie_chart, use_container_width=True)


with st.expander("Top 10 offers of the week by sales (Heatmap)"):
    # Создайте тепловую карту на основе процентов от общей суммы продаж
    fig_heatmap = px.imshow(
        [tokens_by_sales1["percent_of_total_sales"]],
        x=tokens_by_sales["offer_id"],
        y=["Percentage of Total Sales"],
        color_continuous_scale="Viridis",  # Выберите нужную палитру цветов
        color_continuous_midpoint=13,  # Настройте середину цветовой палитры
        title="<b>Top 10 offers of the week by sales (Heatmap)</b>",
    )
    fig_heatmap.update_xaxes(title="Offer ID")
    fig_heatmap.update_yaxes(title="Percentage of Total Sales")
    fig_heatmap.update_layout(
        xaxis_nticks=len(tokens_by_sales["offer_id"]),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


pivot_table = pd.pivot_table(tokens_by_sales,
                             values='percent_of_total_sales',  # Значения для агрегации
                             index='offer_id',  # Колонка, по которой группируем данные
                             aggfunc='sum')  # Функция агрегации, в данном случае сумма



# Создайте тепловую карту на основе размеров продаж с текстом скрытым по умолчанию
fig_heatmap = px.scatter(tokens_by_sales, x='approve', y='percent_of_total_sales', text=None, color='percent_of_total_sales',
                            title='<b>Top 10 offers of the week by sales (Heatmap)</b>',
                            color_continuous_scale="Viridis",
                            hover_data=['offer_id'])  # Укажите 'offer_id' в hover_data
fig_heatmap.update_traces(textposition='top center', marker=dict(size=20, opacity=0.6))
fig_heatmap.update_xaxes(title='X')
fig_heatmap.update_yaxes(title='Y')

# Совместите график с вашим Streamlit приложением
st.plotly_chart(fig_heatmap, use_container_width=True)


n_offers = 10000
offer_data = {
    'offer_id': range(1, n_offers + 1),
    'x': np.random.randint(1, 101, n_offers),  # Случайные значения по оси X
    'y': np.random.randint(1, 101, n_offers),  # Случайные значения по оси Y
}

df = pd.DataFrame(offer_data)

# Создайте тепловую карту
fig_heatmap_2d = px.scatter(df, x='x', y='y', text='offer_id', title='100x100 Grid of Offers')
fig_heatmap_2d.update_traces(textposition='top center', marker=dict(size=10, opacity=0.6))
fig_heatmap_2d.update_xaxes(title='X')
fig_heatmap_2d.update_yaxes(title='Y')
fig_heatmap_2d.update_layout(showlegend=False)

st.plotly_chart(fig_heatmap_2d, use_container_width=True)



