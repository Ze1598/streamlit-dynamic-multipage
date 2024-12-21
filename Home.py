import streamlit as st

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
    layout="wide"
)

st.title("Welcome to the Dashboard! 👋")
st.sidebar.success("Select a page above.")

st.markdown("""
## About this app
This is a sample multipage Streamlit application that demonstrates:
- Data analysis capabilities
- Interactive visualizations
- Customizable settings

Choose a page from the sidebar to explore different features!
""")

# Sample data display
if st.checkbox("Show sample data"):
    st.write("Here's some sample data:")
    data = {
        'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 34, 29, 32],
        'City': ['New York', 'Paris', 'London', 'Tokyo']
    }
    st.dataframe(data)
