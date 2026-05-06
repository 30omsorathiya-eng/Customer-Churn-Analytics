import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Churn Analytics", layout="wide")

st.title("Customer Churn Analytics Dashboard")
st.write("Customer Engagement & Product Utilization Analytics for Retention Strategy")

# Load data
df = pd.read_excel("Customer Engagement & Product Utilization Analytics for Retention Strategy.xlsx")

# Basic rename if needed
if "Exited" in df.columns:
    df["Churn Status"] = df["Exited"].map({1: "Churned", 0: "Retained"})

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

# KPIs
total_customers = filtered_df["CustomerId"].count()
churned_customers = filtered_df["Exited"].sum()
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
    product_chart = filtered_df.groupby(["NumOfProducts", "Churn Status"]).size().reset_index(name="Count")
    fig3 = px.bar(
        product_chart,
        x="NumOfProducts",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    st.subheader("Churn by Active Member")
    active_chart = filtered_df.groupby(["IsActiveMember", "Churn Status"]).size().reset_index(name="Count")
    active_chart["IsActiveMember"] = active_chart["IsActiveMember"].map({1: "Active", 0: "Inactive"})
    fig4 = px.bar(
        active_chart,
        x="IsActiveMember",
        y="Count",
        color="Churn Status",
        barmode="group",
        text="Count",
        color_discrete_map={"Churned": "red", "Retained": "green"}
    )
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Churn by Age")
fig5 = px.histogram(
    filtered_df,
    x="Age",
    color="Churn Status",
    barmode="group",
    color_discrete_map={"Churned": "red", "Retained": "green"}
)
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))
