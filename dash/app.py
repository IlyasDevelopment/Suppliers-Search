import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parents[0]
load_dotenv(os.path.join(BASE_DIR, ".env"))


st.set_page_config(page_title="Suppliers Dashboard", page_icon=":bar_chart:", layout="wide")


@st.experimental_memo(ttl=600)
def get_data(name):
    return pd.read_sql(name, os.environ["DB_URL"])


df = get_data("item")
df_products = get_data("product")

# MAIN PAGE
st.title(":bar_chart: Поиск поставщиков")
st.markdown("##")

st.sidebar.header("Панель для фильтрации")

products_set = df_products["product"].unique()

# PREPROCESSING
df["fair_business_rating"] = df["fair_business_rating"].astype("float")
df["fair_business_rating_comment"] = df["fair_business_rating_comment"].fillna("Без оценки")
df["registration_date"] = pd.to_datetime(df["registration_date"].fillna("01.01.1900"), format="%d.%m.%Y")
df["domain"] = df["domain"].str.lower()
df_products["domain"] = df_products["domain"].str.lower()

df_jl_unfilled = df.merge(df_products, on="domain").groupby(["domain"]).agg({"product": lambda x: x.tolist()}).reset_index()
df_jl = df_jl_unfilled.merge(df, on="domain").drop(columns=["id"])

domain_filter = st.sidebar.text_input(
    label="/",
    label_visibility="collapsed",
    placeholder="Введите домен компании...",
)

products_filter = st.sidebar.multiselect(
    "Выберите желаемые товары:",
    options=products_set,
    default=products_set,
)

fair_business_rating_comment_filter = st.sidebar.multiselect(
    "Выберите необходимую оценку от организации \"За честный бизнес\":",
    options=df["fair_business_rating_comment"].unique(),
    default=df["fair_business_rating_comment"].unique(),
    help="Всероссийская система проверки контрагентов. Самый популярный портал о бизнесе в РФ",
)

years_filter = st.sidebar.select_slider(
    label="Выберите наиболее позднюю дату регистрации компании:",
    options=[f"{year}-01-01" for year in range(1980, datetime.now().year + 1)],
    value=f"{datetime.now().year}-01-01",
)

df_selection_1 = df_products.query(
    "product in @products_filter & "
    "domain.str.contains(@domain_filter.lower())"
)

df_selection_2 = df_jl.query(
    "fair_business_rating_comment == @fair_business_rating_comment_filter & "
    "registration_date <= @years_filter"
)

filtered_domains = df_selection_1["domain"].unique()
df_selection = df_selection_2[df_selection_2["domain"].isin(filtered_domains)].rename(columns={"product": "products"})

st.dataframe(df_selection)

# TOP KPI's
total_suppliers = int(df_selection.shape[0])
average_rating = round(df_selection["fair_business_rating"].mean(), 2)
star_rating = ":star:" * int(round(average_rating, 0)) if not pd.isnull(average_rating) else ":star:"

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Суммарное количество поставщиков:")
    st.subheader(f"{total_suppliers:,} :factory:")
with right_column:
    st.subheader("Средний рейтинг:")
    st.subheader(f"{average_rating} {star_rating}")

st.markdown("""---""")

# SUPPLIERS NUMS BY PRODUCT [BAR CHART]
suppliers_amt_by_products = (
    df_selection.explode("products").groupby(["products"]).count()[["domain"]].sort_values(by="domain")
)
fig_suppliers_nums_by_products = px.bar(
    suppliers_amt_by_products,
    x="domain",
    y=suppliers_amt_by_products.index,
    orientation="h",
    title="<b>Количество поставщиков по товарам</b>",
    color_discrete_sequence=["#0083B8"] * len(suppliers_amt_by_products),
    template="plotly_white",
    height=800,
)
fig_suppliers_nums_by_products.update_layout(xaxis={"title": "Suppliers amount"})

# SUPPLIERS NUMS BY FAIR BUSINESS RATING [BAR CHART]
suppliers_amt_by_fair_business_rating = (
    df_selection["fair_business_rating"].value_counts().sort_index()
)
fig_suppliers_nums_by_fair_business_rating = px.bar(
    suppliers_amt_by_fair_business_rating,
    x=suppliers_amt_by_fair_business_rating.index if not suppliers_amt_by_fair_business_rating.empty else [0],
    y=suppliers_amt_by_fair_business_rating.to_list() or [0],
    orientation="v",
    title="<b>Количество поставщиков по числовому рейтингу</b>",
    color_discrete_sequence=(
        ["#234B9B"] * len(suppliers_amt_by_fair_business_rating) if not suppliers_amt_by_fair_business_rating.empty else None
    ),
    template="plotly_white",
)
fig_suppliers_nums_by_fair_business_rating.update_layout(
    yaxis={"title": "Suppliers amount"},
    xaxis={"title": "Fair Business Rating"},
)

# SUPPLIERS NUMS BY FAIR BUSINESS RATING COMMENT [PIE CHART]
suppliers_amt_by_fair_business_rating_comment = (
    df_selection["fair_business_rating_comment"].value_counts()
)

# colors = ["#00AAA0", "#FFB85F", "#FF7A5A", "#8ED2C9"]
colors = ["0F2D69", "E61E3C", "CD5A5A", "F5C3C3"]
fig_suppliers_nums_by_fair_business_rating_comment = px.pie(
    suppliers_amt_by_fair_business_rating_comment,
    values=suppliers_amt_by_fair_business_rating_comment.to_list(),
    names=suppliers_amt_by_fair_business_rating_comment.index,
    title="<b>Распределение поставщиков по оценке</b>",
    color=suppliers_amt_by_fair_business_rating_comment.index,
    color_discrete_map=dict(zip(list(suppliers_amt_by_fair_business_rating_comment.index), colors)),
)

# PLACEHOLDERS
placeholder = st.empty()
placeholder.plotly_chart(fig_suppliers_nums_by_products, use_container_width=True)

placeholder_1, placeholder_2 = st.columns(2)
placeholder_1.plotly_chart(fig_suppliers_nums_by_fair_business_rating_comment, use_container_width=True)
placeholder_2.plotly_chart(fig_suppliers_nums_by_fair_business_rating, use_container_width=True)

# HIDE STREAMLIT STYLE
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
