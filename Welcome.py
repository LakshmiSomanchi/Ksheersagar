# Welcome.py (in the root directory)
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered", page_title="Ksheersagar Project - Welcome") # You can change the title as desired

# Initialize session state for storing data from both forms
# This ensures data persists across page navigations within the same session
if 'farm_visit_data' not in st.session_state:
    st.session_state.farm_visit_data = [] # List to store farm visit submissions

if 'bmc_visit_data' not in st.session_state:
    st.session_state.bmc_visit_data = [] # List to store BMC visit submissions

st.title("Welcome to Ksheersagar Data Entry Portal") # This is your main page title
st.write("Please select a page from the sidebar to begin:")
st.markdown("---")
st.write("### Instructions:")
st.write("- Use the sidebar on the left to navigate between 'Farm Visit Data Entry' and 'BMC Visit Data Entry'.")
st.write("- Fill out the forms with the relevant information.")
st.write("- Click 'Submit' to see the collected data on the respective page.")
st.write("- **Important:** Data is stored per session. To view or download previous submissions, revisit the respective form page. For persistent storage across sessions/users, a database integration would be required.")

st.subheader("Combined Data Overview (Current Session)")
if st.session_state.farm_visit_data or st.session_state.bmc_visit_data:
    st.info("Navigate to individual pages (Farm Visit / BMC Visit) in the sidebar to view and download specific data sets collected in this session.")
    # Optional: Display a small summary of collected data here
    # if st.session_state.farm_visit_data:
    #     st.write("#### Recent Farm Visit Submissions:")
    #     st.dataframe(pd.DataFrame(st.session_state.farm_visit_data).tail()) # Show last few entries
    # if st.session_state.bmc_visit_data:
    #     st.write("#### Recent BMC Visit Submissions:")
    #     st.dataframe(pd.DataFrame(st.session_state.bmc_visit_data).tail()) # Show last few entries
else:
    st.info("No data submitted yet in this session.")
