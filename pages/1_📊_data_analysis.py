import streamlit as st
from utils import DataManager, generate_analysis_page
import os
from pathlib import Path

st.set_page_config(page_title="Data Analysis", page_icon="📊")

st.title("Data Analysis Hub 📊")

# Initialize data manager
data_manager = DataManager()

# Category selection
st.subheader("Generate Analysis Page")
selected_category = st.selectbox(
    "Select Data Category",
    data_manager.get_categories(),
    help="Choose a category to generate a detailed analysis page"
)

# Display category information
category_info = data_manager.get_category_info(selected_category)
st.write("Available Metrics:", ", ".join(category_info['metrics']))
st.write("Available Dimensions:", ", ".join(category_info['dimensions']))

# Generate page button
if st.button("Generate Analysis Page"):
    generated_page = generate_analysis_page(selected_category)
    st.success(f"Analysis page generated successfully! Navigate to {generated_page.name} in the sidebar.")
    
    # Optional: Add automatic navigation
    st.info("Please refresh the page to see the new analysis in the sidebar.")

# List existing generated pages
generated_dir = Path("pages/generated")
if generated_dir.exists():
    existing_pages = [p.stem for p in generated_dir.glob("*.py")]
    if existing_pages:
        st.subheader("Existing Analysis Pages")
        for page in existing_pages:
            st.write(f"- {page}")
