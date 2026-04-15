import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation

# --- TRANSLATION DICTIONARY ---
# You can expand this dictionary with all your form fields
translations = {
    "English": {
        "title": "🚜 Farmer & BMC Visit Documentation",
        "info": "This digital form replaces the AppSheet checklist for field visits.",
        "admin_details": "📍 Administrative Details",
        "farmer_profile": "🐄 Farmer & Livestock Profile",
        "farmer_name": "Farmer Name",
        "village": "Collecting Village",
        "district": "District",
        "herd_size": "Total Herd Size",
        "milk_prod": "Milk Production (Ltrs/Day)",
        "save_btn": "Save Visit Report",
        "location": "Get Current Location",
        "success": "Visit has been recorded!"
    },
    "Hindi": {
        "title": "🚜 किसान और बीएमसी दौरा दस्तावेज़ीकरण",
        "info": "यह डिजिटल फॉर्म फील्ड विजिट के लिए ऐपशीट चेकलिस्ट की जगह लेता है।",
        "admin_details": "📍 प्रशासनिक विवरण",
        "farmer_profile": "🐄 किसान और पशुधन प्रोफ़ाइल",
        "farmer_name": "किसान का नाम",
        "village": "एकत्रित करने वाला गाँव",
        "district": "ज़िला",
        "herd_size": "कुल पशुओं की संख्या",
        "milk_prod": "दूध उत्पादन (लीटर/दिन)",
        "save_btn": "रिपोर्ट सहेजें",
        "location": "वर्तमान स्थान प्राप्त करें",
        "success": "दौरा दर्ज कर लिया गया है!"
    },
    "Marathi": {
        "title": "🚜 शेतकरी आणि बीएमसी भेट दस्तऐवजीकरण",
        "info": "हा डिजिटल फॉर्म फील्ड भेटीसाठी ॲपशीट चेकलिस्टची जागा घेतो.",
        "admin_details": "📍 प्रशासकीय तपशील",
        "farmer_profile": "🐄 शेतकरी आणि पशुधन प्रोफाइल",
        "farmer_name": "शेतकऱ्याचे नाव",
        "village": "संकलन करणारे गाव",
        "district": "जिल्हा",
        "herd_size": "एकूण जनावरांची संख्या",
        "milk_prod": "दूध उत्पादन (लिटर/दिवस)",
        "save_btn": "अहवाल जतन करा",
        "location": "सध्याचे स्थान मिळवा",
        "success": "भेट नोंदवली गेली आहे!"
    }
}

# Page Configuration
st.set_page_config(page_title="Farmer Visit Checklist", layout="wide")

def main():
    # --- SIDEBAR: LANGUAGE SELECTION ---
    with st.sidebar:
        st.header("Settings / सेटिंग्ज / सेटिंग्स")
        lang = st.selectbox("Select Language", ["English", "Hindi", "Marathi"])
    
    # Helper function to get translated text
    def t(key):
        # Returns the translated text, or the key itself if it's missing from the dictionary
        return translations[lang].get(key, key)

    st.title(t("title"))
    st.info(t("info"))

    # --- GEOLOCATION SECTION ---
    st.subheader(t("location"))
    location = streamlit_geolocation()
    
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    
    if latitude and longitude:
        st.success(f"📍 Lat: {latitude}, Lon: {longitude}")
    else:
        st.warning("Please click the button above to capture GPS coordinates.")

    # --- MAIN FORM ---
    with st.form("main_farm_form", clear_on_submit=False):
        
        # Section 1: Admin
        st.header(t("admin_details"))
        col1, col2 = st.columns(2)
        with col1:
            district = st.text_input(t("district"))
        with col2:
            village = st.text_input(t("village"))

        st.markdown("---")

        # Section 2: Farmer Metrics
        st.header(t("farmer_profile"))
        f1, f2, f3 = st.columns(3)
        with f1:
            farmer_name = st.text_input(t("farmer_name"))
        with f2:
            herd_size = st.number_input(t("herd_size"), min_value=0)
        with f3:
            milk_prod = st.number_input(t("milk_prod"), min_value=0.0)

        # Note: You can continue adding the rest of your form fields here
        # using the `t("your_key")` format!
        
        # Submit Button
        submit_button = st.form_submit_button(t("save_btn"))

    if submit_button:
        # Check if location was captured before saving
        if not latitude or not longitude:
            st.error("Cannot save: GPS location is required!")
        else:
            st.success(f"✅ {t('success')}")
            
            # Preview the collected data
            data = {
                "Farmer Name": farmer_name,
                "Village": village,
                "Herd Size": herd_size,
                "Latitude": latitude,
                "Longitude": longitude
            }
            st.json(data)

if __name__ == "__main__":
    main()
