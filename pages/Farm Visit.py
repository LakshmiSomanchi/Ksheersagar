import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation

# --- TRANSLATION DICTIONARY ---
# Add to this dictionary to translate more fields!
# If a word isn't in the dictionary, the app will automatically just show it in English.
translations = {
    "Hindi": {
        "Farm Visit Form": "किसान और बीएमसी दौरा फॉर्म",
        "Admin Details": "प्रशासनिक विवरण",
        "Farmer & Herd": "किसान और पशुधन",
        "Infrastructure & Hygiene": "बुनियादी ढांचा और स्वच्छता",
        "Feed & Nutrition": "चारा और पोषण",
        "Quality & Vet": "गुणवत्ता और पशु चिकित्सा",
        "Media": "तस्वीरें",
        "Get Location": "वर्तमान स्थान प्राप्त करें",
        "Save Visit Report": "रिपोर्ट सहेजें",
        "Farmer Name": "किसान का नाम",
        "Total Herd Size": "कुल पशुओं की संख्या",
    },
    "Marathi": {
        "Farm Visit Form": "शेतकरी आणि बीएमसी भेट फॉर्म",
        "Admin Details": "प्रशासकीय तपशील",
        "Farmer & Herd": "शेतकरी आणि पशुधन",
        "Infrastructure & Hygiene": "पायाभूत सुविधा आणि स्वच्छता",
        "Feed & Nutrition": "खाद्य आणि पोषण",
        "Quality & Vet": "गुणवत्ता आणि पशुवैद्यकीय",
        "Media": "मीडिया",
        "Get Location": "सध्याचे स्थान मिळवा",
        "Save Visit Report": "अहवाल जतन करा",
        "Farmer Name": "शेतकऱ्याचे नाव",
        "Total Herd Size": "एकूण जनावरांची संख्या",
    }
}

# Page Configuration
st.set_page_config(page_title="Farm Visit Form", layout="wide", initial_sidebar_state="expanded")

def main():
    # --- SIDEBAR: LANGUAGE SELECTION ---
    with st.sidebar:
        st.header("Language / भाषा")
        lang = st.selectbox("Select Language", ["English", "Hindi", "Marathi"])
    
    # Helper function: translates text based on dictionary. 
    # Falls back to the English key if translation is missing.
    def t(key):
        if lang == "English":
            return key
        return translations.get(lang, {}).get(key, key)

    # --- HEADER & GEOLOCATION ---
    st.title(f"🚜 {t('Farm Visit Form')}")
    
    st.markdown(f"**📍 {t('Get Location')}**")
    location = streamlit_geolocation()
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    
    if latitude and longitude:
        st.success(f"Location Captured: Lat {latitude}, Lon {longitude}")
    else:
        st.warning("Please capture GPS coordinates before submitting the form.")

    # --- MAIN FORM ---
    with st.form("main_farm_form", clear_on_submit=False):
        
        # 1. Admin Section
        st.header(t("Admin Details"))
        col1, col2, col3 = st.columns(3)
        with col1:
            farmer_name = st.text_input(t("Farmer Name"))
            activity_name = st.text_input("Activity Name")
            created_by = st.text_input("Activity Created By")
            org = st.text_input("Organization")
        with col2:
            state = st.selectbox("State", ["Select", "State 1", "State 2", "Other"])
            district = st.text_input("District")
            sub_district = st.text_input("Sub District")
        with col3:
            village = st.text_input("Collecting Village")
            bmc = st.text_input("BMC")
            visit_date = st.date_input("Date of Visit", datetime.now())

        st.markdown("---")

        # 2. Herd Section
        st.header(t("Farmer & Herd"))
        f1, f2, f3 = st.columns(3)
        with f1:
            farm_type = st.selectbox("Type Of Farm", ["Small Holder", "Commercial", "Other"])
            farm_size = st.number_input("Farm Area (Acres/Hectare)", min_value=0.0)
            herd_size = st.number_input(t("Total Herd Size"), min_value=0)
        with f2:
            no_desi = st.number_input("No Of Desi", min_value=0)
            no_cross = st.number_input("No Of Cross Breed", min_value=0)
            no_in_milk = st.number_input("No Of Cattle In Milk", min_value=0)
        with f3:
            milk_prod = st.number_input("Milk Production At Farm", min_value=0.0)
            surplus_pour = st.radio("100% Surplus Milk Poured To BMC?", ["Yes", "No"])

        st.markdown("---")

        # 3. Infrastructure Section
        st.header(t("Infrastructure & Hygiene"))
        i1, i2, i3 = st.columns(3)
        with i1:
            shed = st.checkbox("Shed (Provision For Min 5 Animals)")
            loose_housing = st.checkbox("Loose Housing")
            mats = st.checkbox("Floor Mats")
            biogas = st.checkbox("Biogas Installation")
        with i2:
            drainage = st.checkbox("Provision For Drainage And Waste")
            manure_pit = st.checkbox("Separate Space For Dumping Pit For Manure Waste")
            overall_hygiene = st.select_slider("Overall Hygiene Of The Farm", ["Poor", "Average", "Good", "Excellent"])
        with i3:
            water_source = st.text_input("Source Of Water")
            water_adhoc = st.selectbox("Ad-hoc Water Availability", ["Yes", "No"])
            container = st.selectbox("Type Of Milk Container", ["Steel", "Plastic", "Aluminum"])
            post_milk_dur = st.text_input("Duration Of Milk Kept At Farm Post Milking")

        st.markdown("---")

        # 4. Feed & Nutrition
        st.header(t("Feed & Nutrition"))
        feed1, feed2 = st.columns(2)
        with feed1:
            conc_feed = st.radio("Concentrated Feed Available?", ["Yes", "No"])
            conc_name = st.text_input("Name Of Concentrated Feed")
            min_mix = st.radio("Mineral Mixture Available?", ["Yes", "No"])
            min_mix_name = st.text_input("Name Of Mineral Mixture")
            supplements = st.text_area("Feed Supplements (Mention Names)")
        with feed2:
            dry_fodder = st.text_input("Dry Fodder Name")
            green_fodder = st.text_input("Green Fodder Name")
            silage = st.text_input("Silage Name")
            toxin_binder = st.checkbox("Toxin Binder Used")
            moldy_feed = st.checkbox("Presence Of Moldy Or Contaminated Feed")

        st.markdown("---")

        # 5. Quality & Vet Section
        st.header(t("Quality & Vet"))
        v1, v2 = st.columns(2)
        with v1:
            cmt_kit = st.checkbox("CMT Kit Available")
            cmt_freq = st.number_input("Frequency Of CMT Testing (No Of Days)", min_value=0)
            machine_clean = st.number_input("Frequency Of Cleaning Milking Machines (Days)", min_value=0)
            dip_cup = st.checkbox("Dip Cup With Solution")
            sick_sep = st.checkbox("Space For Sick Animal Segregation")
        with v2:
            outbreak = st.selectbox("Any Recent Outbreak Of Contamination/Disease", ["None", "Yes"])
            disease_reported = st.text_input("Recent Disease Reported (Other)")
            last_report_date = st.date_input("Last Date Of Reporting Of Disease")
            cattle_affected = st.number_input("No Of Cattle Affected", min_value=0)
            vet_treatment = st.text_input("Most Recent Veterinary Treatment Given (Other)")
            vet_date = st.date_input("Date Of Last Veterinary Treatment")

        st.markdown("---")

        # 6. Media
        st.header(t("Media"))
        photo_1 = st.camera_input("Photo 1")

        # Submit Button
        submit_button = st.form_submit_button(t("Save Visit Report"))

    # --- SUBMISSION LOGIC ---
    if submit_button:
        if not latitude or not longitude:
            # Gatekeeper: stops the save if GPS is missing
            st.error("⚠️ Cannot save: Please click 'Get Location' at the top of the form before submitting!")
        else:
            st.success("✅ Form submitted successfully!")
            
            # Example payload of the collected data
            collected_data = {
                "Farmer Name": farmer_name,
                "Village": village,
                "Herd Size": herd_size,
                "Milk Production": milk_prod,
                "Latitude": latitude,
                "Longitude": longitude,
                "Visit Date": visit_date.strftime("%Y-%m-%d")
            }
            # Displaying the data JSON as proof of collection
            st.json(collected_data)

if __name__ == "__main__":
    main()
