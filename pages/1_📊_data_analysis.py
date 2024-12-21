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

# List and manage existing generated pages
generated_dir = Path("pages")
if generated_dir.exists():
    existing_pages = list(generated_dir.glob("*.py"))
    if existing_pages:
        st.subheader("Manage Analysis Pages")
        
        # Create a container for the list
        pages_container = st.container()
        
        # Create columns for each page
        for page in existing_pages:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📊 {page.stem}")
            
            with col2:
                # Extract category from filename
                category = page.stem.split('_')[-2] if '_' in page.stem else 'Unknown'
                st.caption(f"Category: {category}")
            
            with col3:
                # Delete button with confirmation
                delete_placeholder = st.empty()
                if delete_placeholder.button("🗑️ Delete", key=f"delete_{page.stem}"):
                    confirm_placeholder = st.empty()
                    if confirm_placeholder.button("✅ Confirm Delete", key=f"confirm_{page.stem}"):
                        try:
                            page.unlink()  # Delete the file
                            st.success(f"Deleted {page.stem}")
                            # Clear the confirmation button
                            confirm_placeholder.empty()
                            # Rerun the app to update the sidebar
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting page: {str(e)}")
                    # Add cancel button
                    if st.button("❌ Cancel", key=f"cancel_{page.stem}"):
                        confirm_placeholder.empty()
                        st.rerun()
            
            # Add a separator line
            st.markdown("---")
    else:
        st.info("No analysis pages generated yet. Use the form above to create your first analysis page.")

