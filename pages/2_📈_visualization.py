import streamlit as st
import plotly.express as px
from utils import load_sample_data

st.set_page_config(page_title="Visualization", page_icon="📈")

st.title("Data Visualization 📈")

# Load data
df = load_sample_data()

# Time series plot
st.subheader("Sales Over Time")
fig = px.line(df, x='date', y='sales', title='Daily Sales Trend')
st.plotly_chart(fig, use_container_width=True)

# Scatter plot
st.subheader("Visitors vs Sales")
fig = px.scatter(df, x='visitors', y='sales', 
                 title='Correlation between Visitors and Sales',
                 trendline="ols")
st.plotly_chart(fig, use_container_width=True)

# Distribution plot
st.subheader("Sales Distribution")
fig = px.histogram(df, x='sales', nbins=30, title='Sales Distribution')
st.plotly_chart(fig, use_container_width=True)
