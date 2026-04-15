import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Farmer Visit Checklist", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stHeader { color: #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🚜 Farmer & BMC Visit Documentation")
    st.info("This digital form replaces the AppSheet checklist for field visits.")

    with st.form("main_farm_form", clear_on_submit=False):
        
        # --- SECTION 1: USER & LOCATION ---
        st.header("📍 Administrative Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            activity_name = st.text_input("Activity Name", "Farm Visit Checklist")
            created_by = st.text_input("Activity Created By (Staff Name)")
            org = st.selectbox("Organization", ["Select Org", "Company A", "Company B", "NGO Partner"])
        with col2:
            state = st.selectbox("State", ["Andhra Pradesh", "Karnataka", "Maharashtra", "Punjab", "Tamil Nadu", "Other"])
            district = st.text_input("District")
            sub_district = st.text_input("Sub District")
        with col3:
            village = st.text_input("Collecting Village")
            bmc = st.text_input("BMC (Bulk Milk Chiller) Name/ID")
            visit_date = st.date_input("Date of Visit", datetime.now())

        st.markdown("---")

        # --- SECTION 2: FARMER & HERD METRICS ---
        st.header("🐄 Farmer & Livestock Profile")
        f1, f2, f3 = st.columns(3)
        with f1:
            farmer_name = st.text_input("Farmer Name")
            farm_type = st.selectbox("Type Of Farm", ["Small (1-5)", "Medium (6-20)", "Large (>20)", "Commercial"])
            farm_size = st.number_input("Farm Area (Acres)", min_value=0.0, step=0.1)
        with f2:
            herd_size = st.number_input("Total Herd Size", min_value=0)
            no_desi = st.number_input("No Of Desi", min_value=0)
            no_cross = st.number_input("No Of Cross Breed", min_value=0)
        with f3:
            no_in_milk = st.number_input("No Of Cattle In Milk", min_value=0)
            milk_prod = st.number_input("Milk Production (Ltrs/Day)", min_value=0.0)
            surplus_pour = st.radio("100% Surplus Milk Poured To BMC?", ["Yes", "No"])

        st.markdown("---")

        # --- SECTION 3: INFRASTRUCTURE & FEEDING ---
        st.header("🌾 Infrastructure & Nutrition")
        i1, i2 = st.columns(2)
        with i1:
            st.subheader("Housing")
            shed = st.checkbox("Shed (Min 5 Animals Provision)")
            loose_housing = st.checkbox("Loose Housing")
            mats = st.checkbox("Floor Mats")
            biogas = st.checkbox("Biogas Installation")
            drainage = st.checkbox("Provision For Drainage & Waste")
            manure_pit = st.checkbox("Separate Dumping Pit for Manure")
            
            st.subheader("Water")
            water_source = st.selectbox("Source Of Water", ["Borewell", "Open Well", "River/Pond", "Tap Water"])
            water_adhoc = st.selectbox("Ad-hoc Water Availability", ["Sufficient", "Partial", "Scarce"])
            
        with i2:
            st.subheader("Feeding")
            conc_feed = st.radio("Concentrated Feed Available?", ["Yes", "No"])
            conc_name = st.text_input("Name Of Concentrated Feed")
            min_mix = st.radio("Mineral Mixture Available?", ["Yes", "No"])
            min_mix_name = st.text_input("Name Of Mineral Mixture")
            toxin_binder = st.checkbox("Toxin Binder")
            moldy_feed = st.checkbox("Presence of Moldy/Contaminated Feed")
            
            st.write("**Fodder Types Used:**")
            dry_fodder = st.text_input("Dry Fodder Name")
            green_fodder = st.text_input("Green Fodder Name")
            silage = st.text_input("Silage Name")
            supplements = st.text_area("Feed Supplements")

        st.markdown("---")

        # --- SECTION 4: HYGIENE & QUALITY CONTROL ---
        st.header("🧪 Hygiene & Quality")
        h1, h2 = st.columns(2)
        with h1:
            hygiene_score = st.select_slider("Overall Farm Hygiene", options=["Poor", "Average", "Good", "Excellent"])
            cmt_kit = st.checkbox("CMT Kit Available")
            cmt_freq = st.number_input("CMT Testing Frequency (Days)", min_value=0)
            dip_cup = st.checkbox("Dip Cup With Solution Used")
        with h2:
            clean_freq = st.number_input("Milking Machine Cleaning (Days)", min_value=0)
            container = st.selectbox("Milk Container Type", ["Stainless Steel", "Aluminum", "Plastic (Not Recommended)"])
            post_milk_dur = st.text_input("Duration Post-Milking at Farm")

        st.markdown("---")

        # --- SECTION 5: VETERINARY & HEALTH ---
        st.header("🩺 Veterinary & Disease Tracking")
        v1, v2 = st.columns(2)
        with v1:
            outbreak = st.selectbox("Recent Outbreak", ["None", "FMD", "Lumpy Skin", "HS/BQ", "Mastitis", "Other"])
            sick_sep = st.checkbox("Space for Sick Animal Segregation")
            disease_reported = st.text_input("Specific Disease Reported")
            last_report_date = st.date_input("Last Date of Disease Reporting")
        with v2:
            cattle_affected = st.number_input("No. of Cattle Affected", min_value=0)
            vet_treatment = st.text_input("Most Recent Vet Treatment")
            vet_date = st.date_input("Date of Last Vet Treatment")

        st.header("📸 Evidence")
        photo_1 = st.camera_input("Take Farm Photo")

        # SUBMIT
        submit_button = st.form_submit_button("Save Visit Report")

    if submit_button:
        st.success(f"✅ Visit for {farmer_name} at {bmc} has been recorded!")
        # Here you would typically write to a database or Google Sheet
        st.balloons()

if __name__ == "__main__":
    main()
