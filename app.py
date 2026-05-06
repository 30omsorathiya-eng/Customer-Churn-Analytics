import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Churn Analytics", layout="wide")

st.title("Customer Churn Analytics Dashboard")
st.write("Customer Engagement & Product Utilization Analytics for Retention Strategy")

# Load dataset
df = pd.read_excel("Customer Engagement & Product Utilization Analytics for Retention Strategy.xlsx")

# Fix column names
df.columns = df.columns.str.strip()

# KPI calculations
total_customers = df["CustomerId"].count()
churned_customers = df["exited"].sum()
retained_customers = total_customers - churned_customers
churn_rate = (churned_customers / total_customers) * 100

# Sidebar filters
st.sidebar.header("Filters")

geography = st.sidebar.multiselect(
    "Select Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[
    (df["Geography"].isin(geography)) &
    (df["Gender"].isin(gender))
]

# KPI after filter
total_customers = filtered_df["CustomerId"].count()
churned_customers = filtered_df["exited"].sum()
retained_customers = total_customers - churned_customers
churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Retained Customers", f"{retained_customers:,}")
col3.metric("Churned Customers", f"{churned_customers:,}")
col4.metric("Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# Charts
col5, col6 = st.columns(2)

with col5:
    st.subheader("Churn by Geography")
    geo_chart = filtered_df.groupby(["Geography", "Churn Status"]).size().reset_index(name="Count")
    fig1 = px.bar(
        geo_chart,
        x="Geography",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("Churn by Gender")
    gender_chart = filtered_df.groupby(["Gender", "Churn Status"]).size().reset_index(name="Count")
    fig2 = px.bar(
        gender_chart,
        x="Gender",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig2, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    st.subheader("Churn by Number of Products")
    product_chart = filtered_df.groupby(["Number of products", "Churn Status"]).size().reset_index(name="Count")
    fig3 = px.bar(
        product_chart,
        x="Number of products",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    st.subheader("Churn by Active Member")
    active_chart = filtered_df.groupby(["member status", "Churn Status"]).size().reset_index(name="Count")
    fig4 = px.bar(
        active_chart,
        x="member status",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig4, use_container_width=True)

col9, col10 = st.columns(2)

with col9:
    st.subheader("Churn by Age Group")
    age_chart = filtered_df.groupby(["age group", "Churn Status"]).size().reset_index(name="Count")
    fig5 = px.bar(
        age_chart,
        x="age group",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig5, use_container_width=True)

with col10:
    st.subheader("Churn by Balance Group")
    balance_chart = filtered_df.groupby(["balance group", "Churn Status"]).size().reset_index(name="Count")
    fig6 = px.bar(
        balance_chart,
        x="balance group",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig6, use_container_width=True)

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))
