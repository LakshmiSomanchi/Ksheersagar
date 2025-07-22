# streamlit_app.py
import streamlit as st

st.set_page_config(layout="centered", page_title="Ksheersagar Project")

st.title("Welcome to Ksheersagar Data Entry Portal")
st.write("Please select a page from the sidebar to begin:")
st.markdown("---")
st.write("### Instructions:")
st.write("- Use the sidebar on the left to navigate between 'Farm Visit Data Entry' and 'BMC Visit Data Entry'.")
st.write("- Fill out the forms with the relevant information.")
st.write("- Click 'Submit' to see the collected data.")
