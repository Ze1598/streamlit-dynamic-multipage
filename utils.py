import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

class DataManager:
    def __init__(self):
        self.categories = {
            'sales': {
                'metrics': ['revenue', 'units_sold', 'average_order_value'],
                'dimensions': ['product_category', 'region', 'channel']
            },
            'marketing': {
                'metrics': ['clicks', 'impressions', 'conversion_rate'],
                'dimensions': ['campaign', 'platform', 'audience']
            },
            'customer': {
                'metrics': ['lifetime_value', 'churn_rate', 'satisfaction_score'],
                'dimensions': ['segment', 'location', 'age_group']
            }
        }
        
    def get_categories(self):
        return list(self.categories.keys())
    
    def get_category_info(self, category):
        return self.categories.get(category, {})

def load_sample_data(category=None):
    """Generate sample data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    base_data = {
        'date': dates,
    }
    
    if category == 'sales':
        base_data.update({
            'revenue': np.random.normal(1000, 150, len(dates)),
            'units_sold': np.random.normal(100, 15, len(dates)),
            'average_order_value': np.random.normal(50, 5, len(dates)),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Food'], len(dates)),
            'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
            'channel': np.random.choice(['Online', 'Store', 'Partner'], len(dates))
        })
    elif category == 'marketing':
        base_data.update({
            'clicks': np.random.normal(5000, 500, len(dates)),
            'impressions': np.random.normal(50000, 5000, len(dates)),
            'conversion_rate': np.random.uniform(0.01, 0.05, len(dates)),
            'campaign': np.random.choice(['Summer', 'Holiday', 'Flash'], len(dates)),
            'platform': np.random.choice(['Facebook', 'Google', 'Email'], len(dates)),
            'audience': np.random.choice(['Young', 'Adult', 'Senior'], len(dates))
        })
    elif category == 'customer':
        base_data.update({
            'lifetime_value': np.random.normal(500, 100, len(dates)),
            'churn_rate': np.random.uniform(0.05, 0.15, len(dates)),
            'satisfaction_score': np.random.normal(4.2, 0.3, len(dates)),
            'segment': np.random.choice(['Premium', 'Standard', 'Basic'], len(dates)),
            'location': np.random.choice(['Urban', 'Suburban', 'Rural'], len(dates)),
            'age_group': np.random.choice(['18-25', '26-35', '36-50', '50+'], len(dates))
        })
    else:
        base_data.update({
            'sales': np.random.normal(100, 15, len(dates)),
            'visitors': np.random.normal(500, 50, len(dates)),
            'conversion_rate': np.random.uniform(0.1, 0.3, len(dates))
        })
    
    return pd.DataFrame(base_data)

def calculate_metrics(df, category=None):
    """Calculate basic metrics from the data"""
    if category == 'sales':
        return {
            'total_revenue': df['revenue'].sum(),
            'total_units': df['units_sold'].sum(),
            'avg_order_value': df['average_order_value'].mean()
        }
    elif category == 'marketing':
        return {
            'total_clicks': df['clicks'].sum(),
            'total_impressions': df['impressions'].sum(),
            'avg_conversion': df['conversion_rate'].mean()
        }
    elif category == 'customer':
        return {
            'avg_lifetime_value': df['lifetime_value'].mean(),
            'avg_churn_rate': df['churn_rate'].mean(),
            'avg_satisfaction': df['satisfaction_score'].mean()
        }
    return {
        'total_sales': df['sales'].sum(),
        'avg_daily_visitors': df['visitors'].mean(),
        'avg_conversion_rate': df['conversion_rate'].mean()
    }

def generate_analysis_page(category):
    """Generate a new analysis page for the given category"""
    template_path = Path('templates/analysis_template.py')
    output_dir = Path('pages/generated')
    output_path = output_dir / f"{len(os.listdir(output_dir)) + 1}_📊_{category}_analysis.py"
    
    # Create template if it doesn't exist
    template_path.parent.mkdir(exist_ok=True)
    if not template_path.exists():
        template_content = """
import streamlit as st
import plotly.express as px
from utils import load_sample_data, calculate_metrics

# Configuration
CATEGORY = "{{category}}"
st.set_page_config(page_title=f"{CATEGORY.title()} Analysis", page_icon="📊")

# Title
st.title(f"{CATEGORY.title()} Analysis Dashboard 📊")

# Load data
df = load_sample_data(CATEGORY)
metrics = calculate_metrics(df, CATEGORY)

# Display metrics
st.subheader("Key Metrics")
cols = st.columns(len(metrics))
for col, (metric, value) in zip(cols, metrics.items()):
    with col:
        st.metric(
            metric.replace('_', ' ').title(),
            f"{value:,.2f}" if isinstance(value, (int, float)) else value
        )

# Time series analysis
st.subheader("Time Series Analysis")
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
selected_metric = st.selectbox("Select Metric", numeric_cols)

fig = px.line(df, x='date', y=selected_metric, title=f'{selected_metric.replace("_", " ").title()} Over Time')
st.plotly_chart(fig, use_container_width=True)

# Dimensional analysis
st.subheader("Dimensional Analysis")
dimension_cols = df.select_dtypes(include=['object']).columns
selected_dimension = st.selectbox("Select Dimension", dimension_cols)

# Aggregated bar chart
agg_data = df.groupby(selected_dimension)[selected_metric].mean().reset_index()
fig = px.bar(agg_data, x=selected_dimension, y=selected_metric,
             title=f'Average {selected_metric.replace("_", " ").title()} by {selected_dimension.replace("_", " ").title()}')
st.plotly_chart(fig, use_container_width=True)

# Distribution analysis
st.subheader("Distribution Analysis")
fig = px.histogram(df, x=selected_metric, nbins=30,
                  title=f'Distribution of {selected_metric.replace("_", " ").title()}')
st.plotly_chart(fig, use_container_width=True)

# Raw data viewer
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(df)
"""
        template_path.write_text(template_content)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Generate new page from template
    template_content = template_path.read_text()
    page_content = template_content.replace("{{category}}", category)
    output_path.write_text(page_content)
    
    return output_path
