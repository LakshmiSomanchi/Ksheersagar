import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Farm Visit Form", layout="wide")
    st.title("🚜 Farm Visit Documentation Form")
    st.write("Please fill out the details below to record the farm visit.")

    # Using a form to batch submissions
    with st.form("farm_visit_form"):
        
        ## --- Section 1: Basic Information ---
        st.header("📍 Basic Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            farmer_name = st.text_input("Farmer Name")
            org = st.text_input("Organization")
        with col2:
            activity_name = st.text_input("Activity Name")
            state = st.text_input("State")
        with col3:
            created_by = st.text_input("Activity Created By")
            district = st.text_input("District")

        col4, col5, col6 = st.columns(3)
        with col4:
            sub_district = st.text_input("Sub District")
        with col5:
            village = st.text_input("Collecting Village")
        with col6:
            bmc = st.text_input("BMC")

        ## --- Section 2: Farm Specifics ---
        st.header("🏗️ Farm Details")
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            farm_type = st.selectbox("Type Of Farm", ["Dairy", "Poultry", "Mixed", "Other"])
            farm_size = st.number_input("Farm Area (Acres/Hectare)", min_value=0.0)
        with f_col2:
            milk_prod = st.number_input("Milk Production At Farm (Liters)", min_value=0.0)
            herd_size = st.number_input("Total Herd Size", min_value=0)
        with f_col3:
            water_source = st.text_input("Source Of Water")
            water_avail = st.selectbox("Ad-hoc Water Availability", ["Yes", "No"])

        ## --- Section 3: Livestock Breakdown ---
        st.subheader("🐄 Herd Composition")
        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1:
            no_desi = st.number_input("No. Of Desi", min_value=0)
        with h_col2:
            no_cross = st.number_input("No. Of Cross Breed", min_value=0)
        with h_col3:
            no_in_milk = st.number_input("No. Of Cattle In Milk", min_value=0)

        ## --- Section 4: Infrastructure & Hygiene ---
        st.header("🧼 Infrastructure & Hygiene")
        i_col1, i_col2 = st.columns(2)
        with i_col1:
            shed_provision = st.checkbox("Shed (Min 5 Animals)")
            loose_housing = st.checkbox("Loose Housing")
            floor_mats = st.checkbox("Floor Mats")
            biogas = st.checkbox("Biogas Installation")
        with i_col2:
            drainage = st.checkbox("Provision For Drainage/Waste")
            dumping_pit = st.checkbox("Separate Space/Dumping Pit for Manure")
            overall_hygiene = st.select_slider("Overall Hygiene Of The Farm", options=["Poor", "Average", "Good", "Excellent"])

        ## --- Section 5: Feed & Supplements ---
        st.header("🌾 Feed & Nutrition")
        feed_col1, feed_col2 = st.columns(2)
        with feed_col1:
            conc_feed = st.selectbox("Concentrated Feed Available", ["Yes", "No"])
            conc_feed_name = st.text_input("Name Of Concentrated Feed")
            min_mix = st.selectbox("Mineral Mixture Available", ["Yes", "No"])
            min_mix_name = st.text_input("Name Of Mineral Mixture")
        with feed_col2:
            dry_fodder = st.text_input("Dry Fodder Name")
            green_fodder = st.text_input("Green Fodder Name")
            silage = st.text_input("Silage Name/Type")
            supplements = st.text_area("Feed Supplements (Mention Names)")
            toxin_binder = st.checkbox("Toxin Binder Used")

        ## --- Section 6: Milking & Quality Control ---
        st.header("🧪 Milking & Testing")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            cmt_kit = st.checkbox("CMT Kit Available")
            cmt_freq = st.number_input("Frequency Of CMT Testing (Days)", min_value=0)
            dip_cup = st.checkbox("Dip Cup With Solution")
            moldy_feed = st.checkbox("Presence Of Moldy/Contaminated Feed")
        with m_col2:
            machine_clean = st.number_input("Frequency of Cleaning Machines (Days)", min_value=0)
            milk_container = st.selectbox("Type Of Milk Container", ["Steel", "Plastic", "Aluminum"])
            post_milk_duration = st.text_input("Duration Milk Kept At Farm Post Milking")
            surplus_pour = st.checkbox("100% Surplus Milk Poured To BMC")

        ## --- Section 7: Health & Veterinary ---
        st.header("🩺 Health & Disease Record")
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            recent_outbreak = st.selectbox("Recent Outbreak of Disease?", ["No", "Yes"])
            sick_segregation = st.checkbox("Space For Sick Animal Segregation")
            disease_reported = st.text_input("Recent Disease Reported")
            last_report_date = st.date_input("Last Date Of Reporting Of Disease")
        with h_col2:
            cattle_affected = st.number_input("No Of Cattle Affected", min_value=0)
            vet_treatment = st.text_input("Most Recent Veterinary Treatment")
            vet_date = st.date_input("Date Of Last Veterinary Treatment")

        ## --- Section 8: Multimedia ---
        st.header("📸 Media")
        photo = st.camera_input("Take Photo 1 (Farm/Cattle)")

        # Submit button
        submitted = st.form_submit_button("Submit Farm Visit Data")
        
        if submitted:
            st.success("Form submitted successfully!")
            # Logic to save data (e.g., to CSV or Database) would go here
            data = {
                "Farmer": farmer_name,
                "Herd Size": herd_size,
                "Milk Production": milk_prod,
                # ... include other fields as needed
            }
            st.json(data)

if __name__ == "__main__":
    main()
