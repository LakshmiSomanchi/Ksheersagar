import streamlit as st
import pandas as pd
from datetime import date as dt_date
import os
import random

# --- NEW IMPORT FOR AUTO-GPS ---
try:
    from streamlit_js_eval import get_geolocation
except ImportError:
    st.error("Please install the missing package by running: pip install streamlit-js-eval")

# --- Constants ---
FARM_VISIT_DATA_FILE = "farm_visit_data.csv"

# --- CACHING FIX: Load data only once ---
@st.cache_data
def load_existing_data():
    """Loads existing data from CSV."""
    data_list = []
    if os.path.exists(FARM_VISIT_DATA_FILE):
        try:
            df_existing = pd.read_csv(FARM_VISIT_DATA_FILE)
            data_list.extend(df_existing.to_dict('records'))
        except Exception as e:
            pass
    return data_list

# --- Translation Dictionary ---
translations = {
    'en': {
        'page_title': "🐄 Ksheersagar - Farm Visit Data Entry",
        'page_header': "Please fill out the details for the farm visit below.",
        'language_select': "Select Language",
        'general_info_header': "General Farm Visit Information",
        
        # Geolocation additions
        'geolocation_header': "Geolocation Details (Auto-GPS)",
        'latitude_label': "Latitude (Auto-detected):",
        'longitude_label': "Longitude (Auto-detected):",
        
        'date_label': "Date:",
        'farmer_name_label': "Farmer Name:",
        'farmer_id_label': "Farmer ID:",
        'activity_name_label': "Activity Name:",
        'activity_created_by_label': "Activity Created By:",
        'type_of_farm_label': "Type Of Farm:",
        'farm_area_label': "Farm Area (acres/hectare):",
        'location_header': "Location & Organization Details",
        'organization_label': "Organization:",
        'state_label': "State:",
        'district_label': "District:",
        'other_district_label': "If Others, Specify District:",
        'sub_district_label': "Sub District:",
        'other_sub_district_label': "If Others, Specify Sub District:",
        'collecting_village_label': "Collecting Village:",
        'bmc_label': "BMC:",
        'mcc_label': "MCC Name:",
        'other_bmc_label': "Other BMC Name (Specify):",
        'herd_details_header': "Milk Production & Herd Details",
        'cow_milk_production_label': "Litres of milk from Cows per day:",
        'buffalo_milk_production_label': "Litres of milk from Buffaloes per day:",
        'herd_size_label': "Herd Size:",
        'desi_no_label': "No Of Desi:",
        'cross_breed_no_label': "No Of Cross Breed:",
        'cows_in_milk_no_label': "No. of Cows:",
        'buffaloes_in_milk_no_label': "No. of Buffaloes:",
        'shed_label': "Shed (Provision For Minimum 5 Animals):",
        'loose_housing_label': "Loose Housing:",
        'water_availability_label': "Ad-hoc Water Availability:",
        'floor_mats_label': "Floor Mats:",
        'feed_fodder_header': "Feed & Fodder Management",
        'concentrated_feed_option_label': "Concentrated Feed (If Yes, brand Name Available):",
        'name_of_concentrated_feed_label': "Name Of Concentrated Feed:",
        'specify_other_concentrated_feed': "Specify Other Concentrated Feed:",
        'feed_supplements_label': "Feed Supplements (Mention Names):",
        'dry_fodder_name_label': "Dry Fodder Name:",
        'green_fodder_name_label': "Green Fodder Name:",
        'specify_other_green_fodder': "Specify Other Green Fodder:",
        'silage_label': "Silage:",
        'mineral_mixture_option_label': "Mineral Mixture (If Yes, Brand Name):",
        'name_of_mineral_mixture_label': "Name Of Mineral Mixture:",
        'toxin_binder_label': "Toxin Binder:",
        'cmt_kit_label': "CMT Kit:",
        'dip_cup_label': "Dip Cup With Solution:",
        'manure_pit_label': "Separate Space For Dumping Pit For Manure Waste:",
        'drainage_waste_label': "Provision For Drainage And Waste:",
        'biogas_label': "Biogas Installation:",
        'surplus_milk_label': "100% Surplus Milk Poured To BMC:",
        'photo_1_label': "Photo 1:",
        'other_details_header': "Other Details",
        'source_of_water_label': "Source Of Water:",
        'ai_proximity_label': "Access to AI services in close proximity (doorstep/BMC/ in village/ nearby villages):",
        'sex_semen_label': "Soughted sex-semen:",
        'cmt_testing_freq_label': "Frequency Of CMT Testing (No Of Days):",
        'cleaning_freq_label': "Frequency Of Cleaning Of Milking Machines (No Of Days):",
        'milk_container_type_label': "Type Of Milk Container:",
        'milk_kept_duration_label': "Duration Of Milk Kept At Farm Post Milking (minutes):",
        'recent_outbreak_label': "Any Recent Outbreak Of Contamination/Disease:",
        'overall_hygiene_label': "Overall Hygiene Of The Farm:",
        'space_sick_animal_label': "Space For Sick Animal Segregation:",
        'recent_disease_label': "Recent Disease Reported:",
        'last_disease_date_label': "Last Date Of Reporting Of Disease:",
        'cattle_affected_no_label': "No Of Cattle Affected:",
        'vet_treatment_label': "Most Recent Veterinary Treatment Given:",
        'last_vet_treatment_date_label': "Date Of Last Veterinary Treatment:",
        'moldy_feed_presence_label': "Presence Of Moldy Or Contaminated Feed:",
        'submit_button': "Submit Farm Visit Data",
        'yes': "YES",
        'no': "NO",
        'others': "OTHERS",
        'Download CSV': "Download CSV",
        'options_hygiene': ["POOR", "MODERATE", "GOOD", "BEST"],
        'options_cleaning_freq': ["DAILY", "WEEKLY", "FORTNIGHT", "TWICE IN A WEEK"]
    },
    'mr': {
        'page_title': "🐄 क्षीरसागर - फार्म भेट डेटा एंट्री",
        'page_header': "कृपया खालील फार्म भेटीसाठी तपशील भरा.",
        'language_select': "भाषा निवडा",
        'general_info_header': "सर्वसाधारण फार्म भेट माहिती",
        
        # Geolocation additions
        'geolocation_header': "स्थान तपशील (Auto-GPS)",
        'latitude_label': "अक्षांश (Automatic):",
        'longitude_label': "रेखांश (Automatic):",
        
        'date_label': "तारीख:",
        'farmer_name_label': "शेतकऱ्याचे नाव:",
        'farmer_id_label': "शेतकरी आयडी:",
        'activity_name_label': "ऍक्टिव्हिटीचे नाव:",
        'activity_created_by_label': "ऍक्टिव्हिटी कोणी तयार केली:",
        'type_of_farm_label': "शेतीचा प्रकार:",
        'farm_area_label': "शेतीचे क्षेत्र (एकर/हेक्टेयर):",
        'location_header': "स्थान आणि संस्था तपशील",
        'organization_label': "संस्था:",
        'state_label': "राज्य:",
        'district_label': "जिल्हा:",
        'other_district_label': "इतर असल्यास, जिल्हा नमूद करा:",
        'sub_district_label': "उप-जिल्हा:",
        'other_sub_district_label': "इतर असल्यास, उप-जिल्हा नमूद करा:",
        'collecting_village_label': "संकलन गाव:",
        'bmc_label': "BMC:",
        'mcc_label': "MCC नाव:", 
        'other_bmc_label': "इतर BMC नाव (नमूद करा):",
        'herd_details_header': "दूध उत्पादन आणि कळप तपशील",
        'cow_milk_production_label': "गायींपासून दररोज मिळणारे दूध (लिटरमध्ये):",
        'buffalo_milk_production_label': "म्हशींपासून दररोज मिळणारे दूध (लिटरमध्ये):",
        'herd_size_label': "कळपाचा आकार:",
        'desi_no_label': "देशी जनावरांची संख्या:",
        'cross_breed_no_label': "संकरित जनावरांची संख्या:",
        'cows_in_milk_no_label': "गायींची संख्या:",
        'buffaloes_in_milk_no_label': "म्हशींची संख्या:",
        'shed_label': "शेड (किमान 5 जनावरांची तरतूद):",
        'loose_housing_label': "मोकळा गोठा:",
        'water_availability_label': "पाण्याची उपलब्धता:",
        'floor_mats_label': "फ्लोर मॅट्स:",
        'feed_fodder_header': "चारा आणि खाद्य व्यवस्थापन",
        'concentrated_feed_option_label': "concentrated खाद्य (असल्यास, ब्रँडचे नाव):",
        'name_of_concentrated_feed_label': "Concentrated खाद्याचे नाव:",
        'specify_other_concentrated_feed': "इतर Concentrated खाद्य नमूद करा:",
        'feed_supplements_label': "खाद्य पूरक (नावे नमूद करा):",
        'dry_fodder_name_label': "कोरड्या चाऱ्याचे नाव:",
        'green_fodder_name_label': "हिरव्या चाऱ्याचे नाव:",
        'specify_other_green_fodder': "इतर हिरवा चारा नमूद करा:",
        'silage_label': "मुरघास:",
        'mineral_mixture_option_label': " खनिज मिश्रण (असल्यास, ब्रँडचे नाव):",
        'name_of_mineral_mixture_label': "खनिज मिश्रणाचे नाव:",
        'toxin_binder_label': "विषारी घटक बांधणारे:",
        'cmt_kit_label': "CMT किट:",
        'dip_cup_label': "Dip Cup With Solution:",
        'manure_pit_label': "शेणखत/कचरा टाकण्यासाठी स्वतंत्र जागा:",
        'drainage_waste_label': "पाणी आणि कचरा निचरा करण्याची तरतूद:",
        'biogas_label': "बायोगॅस:",
        'surplus_milk_label': "100% अतिरिक्त दूध BMC ला पुरवले जाते:",
        'photo_1_label': "फोटो 1:",
        'other_details_header': "इतर तपशील",
        'source_of_water_label': "पाण्याचा स्रोत:",
        'ai_proximity_label': "जवळपासच्या परिसरात कृत्रिम रेतन (AI) सेवांची उपलब्धता:",
        'sex_semen_label': "सॉर्टेड सेक्स-सीमेन वापरले का:",
        'cmt_testing_freq_label': "CMT चाचणीची वारंवारता (दिवसांची संख्या):",
        'cleaning_freq_label': "दूध काढणी यंत्रांच्या स्वच्छतेची वारंवारता (दिवसांची संख्या):",
        'milk_container_type_label': "दुधाच्या भांड्याचा प्रकार:",
        'milk_kept_duration_label': "दूध काढल्यानंतर फार्मवर किती वेळ ठेवले जाते (मिनिटे):",
        'recent_outbreak_label': " अलीकडे कोणताही प्रादुर्भाव/रोगराई:",
        'overall_hygiene_label': "शेताची एकूण स्वच्छता:",
        'space_sick_animal_label': " आजारी जनावरांसाठी वेगळी जागा:",
        'recent_disease_label': "अलीकडील नोंदवलेला आजार:",
        'last_disease_date_label': "आजार नोंदवण्याची शेवटची तारीख:",
        'cattle_affected_no_label': "बाधित जनावरांची संख्या:",
        'vet_treatment_label': "सर्वात अलीकडील पशुवैद्यकीय उपचार:",
        'last_vet_treatment_date_label': "शेवटच्या पशुवैद्यकीय उपचाराची तारीख:",
        'moldy_feed_presence_label': "बुरशीजन्य किंवा दूषित चाऱ्याची उपस्थिती:",
        'submit_button': "फार्म भेट डेटा सबमिट करा",
        'yes': "होय",
        'no': "नाही",
        'others': "इतर",
        'Download CSV': "CSV डाउनलोड करा",
        'options_hygiene': ["खराब", "मध्यम", "चांगली", "उत्तम"],
        'options_cleaning_freq': ["दररोज", "आठवड्यातून", "पंधरवड्यातून", "आठवड्यातून दोनदा"]
    },
    'hi': {
        'page_title': "🐄 क्षीरसागर - फार्म विजिट डेटा एंट्री",
        'page_header': "कृपया नीचे दिए गए फॉर्म में फार्म विजिट का विवरण भरें।",
        'language_select': "भाषा चुनें",
        'general_info_header': "सामान्य फार्म विजिट जानकारी",
        
        # Geolocation additions
        'geolocation_header': "जियोलोकेशन विवरण (Auto-GPS)",
        'latitude_label': "अक्षांश (स्वचालित):",
        'longitude_label': "देशांतर (स्वचालित):",
        
        'date_label': "तारीख:",
        'farmer_name_label': "किसान का नाम:",
        'farmer_id_label': "किसान आईडी:",
        'activity_name_label': "गतिविधि का नाम:",
        'activity_created_by_label': "गतिविधि किसके द्वारा बनाई गई:",
        'type_of_farm_label': "फार्म का प्रकार:",
        'farm_area_label': "फार्म क्षेत्र (एकड़/हेक्टेयर):",
        'location_header': "स्थान और संगठन विवरण",
        'organization_label': "संगठन:",
        'state_label': "राज्य:",
        'district_label': "जिला:",
        'other_district_label': "यदि अन्य, तो ज़िला निर्दिष्ट करें:",
        'sub_district_label': "उप-जिला:",
        'other_sub_district_label': "यदि अन्य, तो उप-ज़िला निर्दिष्ट करें:",
        'collecting_village_label': "संग्रहण गांव:",
        'bmc_label': "BMC:",
        'mcc_label': "MCC का नाम:", 
        'other_bmc_label': "अन्य BMC नाम (निर्दिष्ट करें):",
        'herd_details_header': "दुग्ध उत्पादन और झुंड विवरण",
        'cow_milk_production_label': "गायों से प्रतिदिन मिलने वाला दूध (लीटर में):",
        'buffalo_milk_production_label': "भैंसों से प्रतिदिन मिलने वाला दूध (लीटर में):",
        'herd_size_label': "झुंड का आकार:",
        'desi_no_label': "देशी पशुओं की संख्या:",
        'cross_breed_no_label': "क्रॉस ब्रीड की संख्या:",
        'cows_in_milk_no_label': "गायों की संख्या:",
        'buffaloes_in_milk_no_label': "भैंसों की संख्या:",
        'shed_label': "शेड (न्यूनतम 5 पशुओं के लिए व्यवस्था):",
        'loose_housing_label': "लूज हाउसिंग:",
        'water_availability_label': "पानी की उपलब्धता:",
        'floor_mats_label': "फ्लोर मैट्स:",
        'feed_fodder_header': "चारा और आहार प्रबंधन",
        'concentrated_feed_option_label': "सांद्रित आहार (यदि हाँ, तो ब्रांड का नाम):",
        'name_of_concentrated_feed_label': "सांद्रित आहार का नाम:",
        'specify_other_concentrated_feed': "अन्य सांद्रित आहार निर्दिष्ट करें:",
        'feed_supplements_label': "आहार पूरक (नाम बताएं):",
        'dry_fodder_name_label': "सूखे चारे का नाम:",
        'green_fodder_name_label': "हरे चारे का नाम:",
        'specify_other_green_fodder': "अन्य हरा चारा निर्दिष्ट करें:",
        'silage_label': "साइलेज (मुरघास):",
        'mineral_mixture_option_label': "खनिज मिश्रण (यदि हाँ, तो ब्रांड का नाम):",
        'name_of_mineral_mixture_label': "खनिज मिश्रण का नाम:",
        'toxin_binder_label': "टॉक्सिन बाइंडर:",
        'cmt_kit_label': "CMT किट:",
        'dip_cup_label': "डिप कप (घोल के साथ):",
        'manure_pit_label': "खाद/कचरे के लिए अलग जगह:",
        'drainage_waste_label': "निकासी और अपशिष्ट की व्यवस्था:",
        'biogas_label': "बायोगैस स्थापना:",
        'surplus_milk_label': "100% अतिरिक्त दूध BMC को दिया गया:",
        'photo_1_label': "फोटो 1:",
        'other_details_header': "अन्य विवरण",
        'source_of_water_label': "पानी का स्रोत:",
        'ai_proximity_label': "निकटतम क्षेत्र में एआई (AI) सेवाओं तक पहुंच:",
        'sex_semen_label': "सॉर्टेड सेक्स-सीमेन (Sorted Sex-Semen):",
        'cmt_testing_freq_label': "CMT परीक्षण की आवृत्ति (दिनों की संख्या):",
        'cleaning_freq_label': "दुग्ध मशीनों की सफाई की आवृत्ति (दिनों की संख्या):",
        'milk_container_type_label': "दूध के बर्तन का प्रकार:",
        'milk_kept_duration_label': "दुहने के बाद दूध फार्म पर रखने की अवधि (मिनट):",
        'recent_outbreak_label': "हाल ही में कोई बीमारी का प्रकोप:",
        'overall_hygiene_label': "फार्म की समग्र स्वच्छता:",
        'space_sick_animal_label': "बीमार पशु को अलग रखने की जगह:",
        'recent_disease_label': "हाल ही में दर्ज की गई बीमारी:",
        'last_disease_date_label': "बीमारी की रिपोर्ट करने की अंतिम तिथि:",
        'cattle_affected_no_label': "प्रभावित पशुओं की संख्या:",
        'vet_treatment_label': "हाल ही में दिया गया पशु चिकित्सा उपचार:",
        'last_vet_treatment_date_label': "अंतिम पशु चिकित्सा उपचार की तिथि:",
        'moldy_feed_presence_label': "फफूंदयुक्त या दूषित चारे की उपस्थिति:",
        'submit_button': "फार्म विजिट डेटा सबमिट करें",
        'yes': "हाँ",
        'no': "नहीं",
        'others': "अन्य",
        'Download CSV': "CSV डाउनलोड करें",
        'options_hygiene': ["खराब", "सामान्य", "अच्छा", "सबसे अच्छा"],
        'options_cleaning_freq': ["दैनिक", "साप्ताहिक", "पखवाड़े में एक बार", "सप्ताह में दो बार"]
    }
}

# --- Function to get translated text ---
def t(key):
    return translations[st.session_state.language][key]

# --- HELPER FUNCTION FOR CONDITIONAL UI (Permanent Specify Field) ---
def render_select_with_specify_permanent(container, label_key, options_list, select_key, specify_label_key, is_multi=False):
    col_select, col_specify = container.columns([0.5, 0.5])
    specify_key = f"{select_key}_specify"
    if specify_key not in st.session_state:
        st.session_state[specify_key] = ""
    with col_select:
        if is_multi:
            select_output = st.multiselect(t(label_key), options_list, key=select_key, default=[])
        else:
            select_output = st.selectbox(t(label_key), options_list, key=select_key, index=0)
    with col_specify:
        specify_output = st.text_input(t(specify_label_key), key=specify_key, label_visibility="visible")
    return select_output, specify_output


st.set_page_config(layout="centered", page_title="Ksheersagar - Data Entry")

# --- Language Selection ---
if 'language' not in st.session_state:
    st.session_state.language = 'en'

st.sidebar.header("Language / भाषा / भाषा")
lang_map = {"English": "en", "Marathi": "mr", "Hindi": "hi"}
selected_lang_display = st.sidebar.radio(
    "Select Language", 
    list(lang_map.keys()), 
    index=list(lang_map.values()).index(st.session_state.language)
)

st.session_state.language = lang_map[selected_lang_display]

# --- Session State Initialization ---
if 'farm_visit_data' not in st.session_state:
    st.session_state.farm_visit_data = load_existing_data()

st.title(t('page_title'))
st.write(t('page_header'))

# --- AUTO GEOLOCATION FIX (Infinite Loop Prevention) ---
st.header(t('geolocation_header'))

if 'auto_lat' not in st.session_state:
    st.session_state.auto_lat = "Not Detected"
    st.session_state.auto_lon = "Not Detected"

# Only attempt to get GPS once per session to prevent infinite reloads
if st.session_state.auto_lat == "Not Detected":
    st.info("Please allow location access if prompted. Fetching GPS...")
    try:
        geo_location = get_geolocation()
        if geo_location:
            st.session_state.auto_lat = str(geo_location['coords']['latitude'])
            st.session_state.auto_lon = str(geo_location['coords']['longitude'])
            st.rerun() # Refresh the page once to lock in the location and hide the fetcher
    except Exception as e:
        st.error(f"GPS Error: {e}")
else:
    st.success(f"GPS Locked: {st.session_state.auto_lat}, {st.session_state.auto_lon}")

auto_lat = st.session_state.auto_lat
auto_lon = st.session_state.auto_lon

st.markdown("---")


# --- SPECIFIC LISTS ADDED ---
MCC_NAMES_LIST = ["Barla", "Budhana", "Bulandshahr", "Jhadwan", "Jhangirabad", "Khurja", "Kuchesar Chopla", "Mawana", "Miranpur", "Najibabad"]
ORGANIZATION_LIST = ["Govind", "Paras", "Lactalis", "NDDB", "NDDB (Harit Pradesh)", "Parag", "Schreiber"]

# Districts List Updated
EXISTING_DISTRICTS = ["Satara", "Pune", "Ahmednagar", "Solapur"]
NEW_DISTRICTS = ["Barla", "Budhana", "Jhadwan", "Jhangirabad", "Khurja", "Kuchesar Chopla", "Mawana", "Miranpur", "Najibabad", "Merath", "Bulandshahr"]
ALL_DISTRICTS = sorted(list(set(EXISTING_DISTRICTS + NEW_DISTRICTS)))

# --- Form Implementation ---
with st.form(key='farm_visit_form'):
    
    # Display Captured GPS (ReadOnly) in the form so it is clear to the user
    col_geo1, col_geo2 = st.columns(2)
    with col_geo1:
        st.text_input(t('latitude_label'), value=auto_lat, disabled=True)
    with col_geo2:
        st.text_input(t('longitude_label'), value=auto_lon, disabled=True)
    
    st.markdown("---")

    st.header(t('general_info_header'))
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input(t('date_label'), value=dt_date.today())
        farmer_name = st.text_input(t('farmer_name_label'), "Sarika Pawar")
        farmer_id = st.text_input(t('farmer_id_label'), "123-02-BB-00768")
    with col2:
        activity_name = st.text_input(t('activity_name_label'), "TNS- Farm Activity")
        activity_created_by = st.selectbox(t('activity_created_by_label'), ["Dr Sachin", "bhusan", "nilesh", "subhrat", "aniket", "ritesh"])
        type_of_farm = st.text_input(t('type_of_farm_label'), "Conventional")
        farm_area = st.number_input(t('farm_area_label'), min_value=0.0, value=1.52)

    st.header(t('location_header'))
    col3, col4 = st.columns(2)
    with col3:
        organization = st.selectbox(t('organization_label'), ORGANIZATION_LIST)
        state = st.selectbox(t('state_label'), ["Maharashtra", "UP"], index=0)
        
        district_option, other_district_input = render_select_with_specify_permanent(
            st, 'district_label', ALL_DISTRICTS + [t('others')], 'district_select', 'other_district_label'
        )
        actual_district = other_district_input if district_option == t('others') else district_option
        
        mcc_selected = st.selectbox(t('mcc_label'), ["SELECT"] + MCC_NAMES_LIST + ["OTHERS"])
        
    with col4:
        sub_districts_list = ["Phaltan", "malshiras", "Baramati", "Indapur", "Daund", "Purander", "Pachgani", "Man", "Khatav", "Koregaon", "Khandala", "Shirur"]
        sub_district_option, other_sub_district_input = render_select_with_specify_permanent(
            st, 'sub_district_label', sub_districts_list + [t('others')], 'sub_district_select', 'other_sub_district_label'
        )
        actual_sub_district = other_sub_district_input if sub_district_option == t('others') else sub_district_option
        
        collecting_village = st.text_input(t('collecting_village_label'), "SAKHARWADi")
        bmc_selected = st.selectbox(t('bmc_label'), ["SELECT", "OTHERS"]) 

    st.header(t('herd_details_header'))
    col5, col6 = st.columns(2)
    with col5:
        cow_milk_production = st.number_input(t('cow_milk_production_label'), min_value=0.0, value=50.0)
        buffalo_milk_production = st.number_input(t('buffalo_milk_production_label'), min_value=0.0, value=45.0)
        herd_size = st.number_input(t('herd_size_label'), min_value=0, value=16)
    with col6:
        cows_in_milk = st.number_input(t('cows_in_milk_no_label'), min_value=0, value=8)
        buffaloes_in_milk = st.number_input(t('buffaloes_in_milk_no_label'), min_value=0, value=6)
        shed = st.radio(t('shed_label'), [t('yes'), t('no')])
        loose_housing = st.radio(t('loose_housing_label'), [t('yes'), t('no')])

    st.header(t('other_details_header'))
    ai_proximity = st.radio(t('ai_proximity_label'), [t('yes'), t('no')], key="ai_proximity_fv")
    sex_semen = st.radio(t('sex_semen_label'), [t('yes'), t('no')], key="sex_semen_fv")
    
    source_of_water = st.text_input(t('source_of_water_label'), "Bore well")
    overall_hygiene = st.selectbox(t('overall_hygiene_label'), t('options_hygiene'), index=2)
    presence_moldy_contaminated_feed = st.radio(t('moldy_feed_presence_label'), [t('no'), t('yes')])

    submit_button = st.form_submit_button(label=t('submit_button'))

    if submit_button:
        yes_en, no_en = translations['en']['yes'], translations['en']['no']
        
        submitted_data = {
            "Latitude": auto_lat,
            "Longitude": auto_lon,
            "Date": date.isoformat() if date else None,
            "Farmer Name": farmer_name,
            "Farmer ID": farmer_id,
            "Organization": organization,
            "State": state,
            "District": actual_district,
            "Sub District": actual_sub_district,
            "MCC Name": mcc_selected, 
            "BMC Name": bmc_selected,
            "Cow Milk Production (L/day)": cow_milk_production,
            "Buffalo Milk Production (L/day)": buffalo_milk_production,
            "Cows": cows_in_milk,
            "Buffaloes": buffaloes_in_milk,
            "Herd Size": herd_size,
            "AI Service Proximity": yes_en if ai_proximity == t('yes') else no_en,
            "Soughted Sex-Semen": yes_en if sex_semen == t('yes') else no_en,
            "Overall Hygiene": overall_hygiene,
            "Moldy Feed": yes_en if presence_moldy_contaminated_feed == t('yes') else no_en
        }
        
        st.session_state.farm_visit_data.append(submitted_data)
        pd.DataFrame([submitted_data]).to_csv(FARM_VISIT_DATA_FILE, mode='a', index=False, header=not os.path.exists(FARM_VISIT_DATA_FILE))
        st.success("Data Saved!")

# --- View Data & Download Section ---
if st.session_state.farm_visit_data:
    st.markdown("---")
    st.subheader("Submitted Data")
    
    # Convert data into DataFrame
    df_display = pd.DataFrame(st.session_state.farm_visit_data)
    st.dataframe(df_display)
    
    # Generate CSV byte data
    csv = df_display.to_csv(index=False).encode('utf-8')
    
    # Download Button placed safely outside the form logic
    st.download_button(
        label=t('Download CSV'),
        data=csv,
        file_name=f"farm_visit_data_{dt_date.today()}.csv",
        mime="text/csv",
        key="download_csv_button"
    )
