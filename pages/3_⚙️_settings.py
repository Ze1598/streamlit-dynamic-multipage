import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("Settings ⚙️")

# Theme settings
st.subheader("Display Settings")
theme = st.selectbox(
    "Choose Theme",
    ["Light", "Dark"],
    key="theme"
)

# Data settings
st.subheader("Data Settings")
data_update_frequency = st.slider(
    "Data Update Frequency (minutes)",
    min_value=1,
    max_value=60,
    value=5
)

# Notification settings
st.subheader("Notification Settings")
email_notifications = st.checkbox("Enable Email Notifications")
if email_notifications:
    email = st.text_input("Email Address")
    notification_types = st.multiselect(
        "Select Notification Types",
        ["Daily Reports", "Anomaly Alerts", "System Updates"]
    )

# Save settings button
if st.button("Save Settings"):
    st.success("Settings saved successfully!")
