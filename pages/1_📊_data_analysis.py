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

# Initialize session state for delete confirmations
if 'delete_confirmations' not in st.session_state:
    st.session_state.delete_confirmations = {}

# List and manage existing generated pages
generated_dir = Path("pages")
if generated_dir.exists():
    existing_pages = list(generated_dir.glob("*.py"))
    # Don't consider the pre-built pages for listing
    existing_pages = [page for page in existing_pages if page.stem[0] not in ("1", "2")]

    if existing_pages:
        st.subheader("Manage Analysis Pages")
        
        # Create a container for the list
        pages_container = st.container()
        
        # Create columns for each page
        for page in existing_pages:
            page_id = page.stem
            
            # Initialize this page's confirmation state if not exists
            if page_id not in st.session_state.delete_confirmations:
                st.session_state.delete_confirmations[page_id] = False
                
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📊 {page_id}")
            
            with col2:
                # Extract category from filename
                category = page_id.split('_')[-2] if '_' in page_id else 'Unknown'
                st.caption(f"Category: {category}")
            
            with col3:
                if not st.session_state.delete_confirmations[page_id]:
                    # Show delete button first
                    if st.button("🗑️ Delete", key=f"delete_{page_id}"):
                        st.session_state.delete_confirmations[page_id] = True
                        st.rerun()
                else:
                    # Show confirm/cancel buttons
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Confirm", key=f"confirm_{page_id}"):
                            try:
                                page.unlink()  # Delete the file
                                st.success(f"Deleted {page_id}")
                                # Reset confirmation state
                                st.session_state.delete_confirmations[page_id] = False
                                # Rerun to update the page list
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting page: {str(e)}")
                    with c2:
                        if st.button("❌ Cancel", key=f"cancel_{page_id}"):
                            st.session_state.delete_confirmations[page_id] = False
                            st.rerun()
            
            # Add a separator line
            st.markdown("---")
    else:
        st.info("No analysis pages generated yet. Use the form above to create your first analysis page.")