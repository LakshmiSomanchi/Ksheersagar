import streamlit as st
import pandas as pd
from datetime import date as dt_date
import os

# --- Constants ---
BMC_VISIT_DATA_FILE = "bmc_visit_data.csv"

# --- CACHING FIX: Load data only once ---
@st.cache_data
def load_existing_data():
    """Loads existing data from CSV, using caching for performance."""
    data_list = []
    if os.path.exists(BMC_VISIT_DATA_FILE):
        try:
            df_existing = pd.read_csv(BMC_VISIT_DATA_FILE, dtype=str)
            data_list.extend(df_existing.to_dict('records'))
        except Exception as e:
            st.warning(f"Warning: Could not load existing BMC data file. Starting fresh. Error: {e}")
    return data_list

# --- Translation Dictionary (Definitions remain the same) ---
translations = {
    'en': {
        'page_title': "🚚 Ksheersagar - BMC Visit Data Entry",
        'page_header': "Please fill out the details for the BMC visit below.",
        'language_select': "Select Language",
        'admin_access_header': "Admin Access",
        'admin_username_prompt': "Enter Admin Username to View Data:",
        'admin_invalid_warning': "Invalid Admin Username.",
        'general_info_header': "General BMC Visit Information",
        'bmc_code_label': "BMC Code:",
        'start_date_label': "SCHEDULED START DATE:",
        'organization_label': "Organization:",
        'bmc_name_label': "BMC Name:",
        'other_bmc_name_label': "If Others, Specify BMC Name:",
        'activity_created_by_label': "ACTIVITY CREATED BY:",
        'state_label': "State:",
        'district_label': "District:",
        'sub_district_label': "Sub District:",
        'other_district_label': "If Others, Specify District:",
        'other_sub_district_label': "If Others, Specify Sub District:",
        'collecting_village_label': "Collecting Village (No.):", 
        'village_label': "Village:",
        'other_village_label': "If Others, Specify Village:",
        
        'bcf_details_header': "BCF (Bulk Milk Cooler Farmer) Details",
        'bcf_name_label': "BCF Name:",
        'bcf_gender_label': "BCF Gender:",
        'education_label': "Education:",
        'other_education_label': "If Others, Specify Education:",
        'bcf_mobile_label': "BCF Mobile Number:",
        'operating_staff_label': "Operating Staff (No.):",
        'distance_from_ho_label': "Distance From HO (KM):",
        
        # Farmer Metrics
        'total_farmers_label': "Total Registered Farmer (No.):",
        'total_women_farmers_label': "No. of Women Farmers (Total Registered):",
        'total_men_farmers_label': "No. of Men Farmers (Total Registered):",
        'active_farmers_label': "Active Farmer (No.):",
        'active_women_farmers_label': "No. of Women Farmers (Active Farmers):",
        'active_men_farmers_label': "No. of Men Farmers (Active Farmers):",
        
        'capacity_header': "Capacity & Collection Details",
        'total_tank_capacity_label': "Total Tank Capacity:",
        'tank_1_capacity_label': "Total Capacity (Tank 1):",
        'tank_2_capacity_label': "Total Capacity (Tank 2):",
        'tank_3_capacity_label': "Total Capacity (Tank 3):",
        'tank_4_capacity_label': "Total Capacity (Tank 4):",
        'segregation_tank_space_label': "Space available for Segregation Tank:",
        'milk_segregated_label': "MILK SEGREGATED (LPD):",
        'morning_collection_time_label': "MORNING MILK COLLECTION END TIME (e.g., 9.3 for 9:30 AM):",
        'morning_milk_lpd_label': "MORNING MILK (LPD):",
        'morning_farmers_label': "No. of Farmers (Morning Milk Collected):",
        'evening_collection_time_label': "EVENING MILK COLLECTION END TIME (e.g., 9 for 9:00 PM):",
        'evening_milk_lpd_label': "EVENING MILK (LPD):",
        'evening_farmers_label': "No. of Farmers (Evening Milk Collected):",

        'quality_payment_header': "Milk Quality & Payment",
        'fat_label': "FAT:",
        'snf_label': "SNF:",
        'payment_cycle_label': "FARMER PAYMENT CYCLE (DAYS):",
        'direct_pouring_label': "Direct Farmer pouring (No.):",
        'inward_vehicle_route_label': "Inward Vehicle Route (No.):",
        'inward_route_farmer_label': "Inward Route Farmer (No.):",
        'inward_route_milk_label': "Inward Route Milk (LPD):",
        
        'infra_compliance_header': "Infrastructure & Compliance",
        'overall_infra_label': "Overall Infrastructure:",
        'remark_infra_label': "Remark (Infrastructure):",
        'bmc_cleaning_label': "BMC Cleaning & Hygiene:",
        'air_curtain_label': "Air curtain:",
        'fly_catcher_label': "Fly Catcher:",
        'wash_basin_label': "Wash Basin:",
        'opening_window_door_label': "Opening (Window/Door):",
        'intact_floor_label': "Intact Floor in BMC Premise:",
        'digitize_system_label': "Digitize System:",
        'fssai_licence_label': "FSSAI Licence:",
        'remark_fssai_label': "Remark (FSSAI):",
        'wg_scale_licence_label': "Wg Scale Licence:",
        'sops_label': "SOP's:",
        'sop_available_label': "Is SOP Available:",
        'hot_water_available_label': "Is Hot Water Available:",
        'notice_board_available_label': "Is Notice Board Available:",
        'awareness_poster_label': "Awareness Poster:",
        'other_awareness_poster_label': "If Others, Specify Awareness Poster:",
        'stirrer_label': "Stirrer/Ekomilk/Indifoss:",
        'remark_stirrer_label': "Remark (Stirrer/Ekomilk/Indifoss):",
        'sampler_label': "Sampler/Dipper/Plunger:",
        'remark_sampler_label': "Remark (Sampler/Dipper/Plunger):",
        'milk_temp_check_label': "Milk Temp Check:",
        'remark_milk_temp_label': "Remark (Milk Temp):",
        'cleaning_chemicals_label': "Cleaning Chemicals:",
        'remark_cleaning_chemicals_label': "Remark (Cleaning Chemicals):",
        'hot_water_source_label': "Hot Water Source:",
        'remark_hot_water_label': "Remark (Hot Water Source):",
        'strainer_label': "Strainer/Nylon cloth available:",
        'sample_bottle_label': "Sample Bottle:",

        'payment_header': "Payment",
        'payment_schedule_label': "Payment Schedule:",
        'payment_method_label': "Payment Method:",
        
        'farmer_competitor_header': "Farmer & Competitor Details",
        'animal_welfare_farm_label': "Animal Welfare Farm (No.):",
        'farmer_use_cattle_feed_label': "FARMER USE (compliant CATTLE FEED):",
        'cattle_feed_bag_sale_label': "Compliant Cattle Feed bag sale (month):",
        'cattle_feed_brand_label': "Cattle Feed Brand Name:",
        'other_cattle_feed_brand_label': "If Others, Specify Cattle Feed Brand Name:",
        'farmer_use_mineral_mixture_label': "FARMER USE (MINERAL MIXTURE) Quantity:",
        'mineral_mixture_brand_label': "MINERAL MIXTURE BRAND NAME:",
        'farmer_use_evm_rtu_label': "FARMER USE (EVM RTU) Quantity:",
        'evm_rtu_label': "EVM RTU:",
        'biogas_installed_label': "BIOGAS INSTALLED:",
        'bank_linkage_label': "ANY BANK LINKAGE:",
        'competitor_details_subheader': "Competitor Details",
        'competitor1_name_label': "COMPETITOR 1 NAME:",
        'competitor1_milk_label': "COMPETITOR 1 MILK (LPD):",
        'competitor2_name_label': "Competitor 2 Name:",
        'competitor2_milk_label': "Competitor 2 MILK (LPD):",
        'competitor3_name_label': "Competitor 3 Name:",
        'competitor3_milk_label': "Competitor 3 MILK (LPD):",
        'competitor4_name_label': "Competitor 4 Name:",
        'competitor4_milk_label': "Competitor 4 MILK (LPD):",
        
        'photo_upload_header': "BMC Photos",
        'photo_overall_label': "Photo 1: Overall BMC Structure",
        'photo_platform_label': "Photo 2: Platform/Entry Area",
        'photo_inside_label': "Photo 3: BMC Cooling Area (Inside)",
        'submit_button': "Submit BMC Visit Data",
        'yes': "YES",
        'no': "NO",
        'others': "OTHERS",
        'options_gender': ["MALE", "FEMALE"],
        'options_education': ["10th pass", "12th pass", "Graduation", "Post graduation", "OTHERS"], 
        'options_quality': ["Poor", "Fair", "Good", "Best"],
        'options_payment_schedule': ["Every 10th day in a month", "Twice a month", "Once a month", "No specific schedule"],
        'options_payment_method': ["Cash", "Bank Transfer", "Both"], 
        'options_awareness_poster': ["afm", "ab", "cmp", "OTHERS"]
    },
    'mr': {
        'page_title': "🚚 क्षीरसागर - BMC भेट डेटा एंट्री",
        'page_header': "कृपया खालील BMC भेटीसाठी तपशील भरा.",
        'language_select': "भाषा निवडा",
        'admin_access_header': "प्रशासक प्रवेश",
        'admin_username_prompt': "डेटा पाहण्यासाठी प्रशासक वापरकर्तानाव प्रविष्ट करा:",
        'admin_invalid_warning': "अवैध प्रशासक वापरकर्तानाव.",
        'general_info_header': "सर्वसाधारण BMC भेट माहिती",
        'bmc_code_label': "BMC कोड:",
        'start_date_label': "नियोजित प्रारंभ तारीख:",
        'organization_label': "संस्था:",
        'bmc_name_label': "BMC नाव:",
        'other_bmc_name_label': "इतर असल्यास, BMC नाव नमूद करा:",
        'activity_created_by_label': "ऍक्टिव्हिटी कोणी तयार केली:",
        'state_label': "राज्य:",
        'district_label': "जिल्हा:",
        'sub_district_label': "उप-जिल्हा:",
        'other_district_label': "इतर असल्यास, जिल्हा नमूद करा:",
        'other_sub_district_label': "इतर असल्यास, उप-जिल्हा नमूद करा:",
        'collecting_village_label': "संकलन गाव (संख्या):",
        'village_label': "गाव:",
        'other_village_label': "इतर असल्यास, गाव नमूद करा:",
        
        'bcf_details_header': "BCF (बल्क मिल्क कूलर शेतकरी) तपशील",
        'bcf_name_label': "BCF नाव:",
        'bcf_gender_label': "BCF लिंग:",
        'education_label': "शिक्षण:",
        'other_education_label': "इतर असल्यास, शिक्षण नमूद करा:",
        'bcf_mobile_label': "BCF मोबाईल नंबर:",
        'operating_staff_label': "कार्यरत कर्मचारी (संख्या):",
        'distance_from_ho_label': "HO पासून अंतर (किमी):",
        
        # Farmer Metrics
        'total_farmers_label': "एकूण नोंदणीकृत शेतकरी (संख्या):",
        'total_women_farmers_label': "महिला शेतकरी (एकूण नोंदणीकृत):",
        'total_men_farmers_label': "पुरुष शेतकरी (एकूण नोंदणीकृत):",
        'active_farmers_label': "सक्रिय शेतकरी (संख्या):",
        'active_women_farmers_label': "महिला शेतकरी (सक्रिय शेतकरी):",
        'active_men_farmers_label': "पुरुष शेतकरी (सक्रिय शेतकरी):",
        
        'capacity_header': "क्षमता आणि संकलन तपशील",
        'total_tank_capacity_label': "एकूण टाकी क्षमता:",
        'tank_1_capacity_label': "एकूण क्षमता (टाकी 1):",
        'tank_2_capacity_label': "एकूण क्षमता (टाकी 2):",
        'tank_3_capacity_label': "एकूण क्षमता (टाकी 3):",
        'tank_4_capacity_label': "एकूण क्षमता (टाकी 4):",
        'segregation_tank_space_label': "विलगीकरण टाकीसाठी जागा उपलब्ध आहे:",
        'milk_segregated_label': "दूध वेगळे केले (LPD):",
        'morning_collection_time_label': "सकाळच्या दूध संकलनाची शेवटची वेळ (उदा. 9.3 म्हणजे 9:30 AM):",
        'morning_milk_lpd_label': "सकाळचे दूध (LPD):",
        'morning_farmers_label': "शेतकऱ्यांची संख्या (सकाळचे दूध संकलन):",
        'evening_collection_time_label': "संध्याकाळच्या दूध संकलनाची शेवटची वेळ (उदा. 9 म्हणजे 9:00 PM):",
        'evening_milk_lpd_label': "संध्याकाळचे दूध (LPD):",
        'evening_farmers_label': "शेतकऱ्यांची संख्या (संध्याकाळचे दूध संकलन):",

        'quality_payment_header': "दुधाची गुणवत्ता आणि पेमेंट",
        'fat_label': "FAT:",
        'snf_label': "SNF:",
        'payment_cycle_label': "शेतकरी पेमेंट सायकल (दिवस):",
        'direct_pouring_label': "थेट शेतकरी ओतणे (संख्या):",
        'inward_vehicle_route_label': "येणारे वाहन मार्ग (संख्या):",
        'inward_route_farmer_label': "येणारे मार्ग शेतकरी (संख्या):",
        'inward_route_milk_label': "येणारे मार्ग दूध (LPD):",
        
        'infra_compliance_header': "पायाभूत सुविधा आणि अनुपालन",
        'overall_infra_label': "एकूण पायाभूत सुविधा:",
        'remark_infra_label': "टीप (पायाभूत सुविधा):",
        'bmc_cleaning_label': "BMC स्वच्छता आणि आरोग्य:",
        'air_curtain_label': "एअर पडदा:",
        'fly_catcher_label': "माशी पकडणारा:",
        'wash_basin_label': "वॉश बेसिन:",
        'opening_window_door_label': "उघडणे (खिडकी/दार):",
        'intact_floor_label': "BMC परिसरात अखंड मजला:",
        'digitize_system_label': "डिजिटायझ प्रणाली:",
        'fssai_licence_label': "FSSAI परवाना:",
        'remark_fssai_label': "टीप (FSSAI):",
        'wg_scale_licence_label': "वजन काटा परवाना:",
        'sops_label': "SOP's:",
        'sop_available_label': "SOP उपलब्ध आहे का:",
        'hot_water_available_label': "गरम पाणी उपलब्ध आहे का:",
        'notice_board_available_label': "नोटीस बोर्ड उपलब्ध आहे का:",
        'awareness_poster_label': "जागरूकता पोस्टर:",
        'other_awareness_poster_label': "इतर असल्यास, जागरूकता पोस्टर नमूद करा:",
        'stirrer_label': "Stirrer/Ekomilk/Indifoss:",
        'remark_stirrer_label': "टीप (Stirrer/Ekomilk/Indifoss):",
        'sampler_label': "Sampler/Dipper/Plunger:",
        'remark_sampler_label': "टीप (Sampler/Dipper/Plunger):",
        'milk_temp_check_label': "दुधाचे तापमान तपासणे:",
        'remark_milk_temp_label': "टीप (Milk Temp):",
        'cleaning_chemicals_label': "स्वच्छता रसायने:",
        'remark_cleaning_chemicals_label': "टीप (Cleaning Chemicals):",
        'hot_water_source_label': "गरम पाण्याचा स्रोत:",
        'remark_hot_water_label': "टीप (Hot Water Source):",
        'strainer_label': "गाळणी/नायलॉन कापड उपलब्ध:",
        'sample_bottle_label': "नमुना बाटली:",

        'payment_header': "पेमेंट",
        'payment_schedule_label': "पेमेंट वेळापत्रक:",
        'payment_method_label': "पेमेंट पद्धत:",
        
        'farmer_competitor_header': "शेतकरी आणि स्पर्धक तपशील",
        'animal_welfare_farm_label': "पशु कल्याण फार्म (संख्या):",
        'farmer_use_cattle_feed_label': "शेतकरी वापर (compliant CATTLE FEED):",
        'cattle_feed_bag_sale_label': "Compliant Cattle Feed बॅग विक्री (महिना):",
        'cattle_feed_brand_label': "Cattle Feed ब्रँड नाव:",
        'other_cattle_feed_brand_label': "इतर असल्यास, Cattle Feed ब्रँड नाव नमूद करा:",
        'farmer_use_mineral_mixture_label': "शेतकरी वापर (MINERAL MIXTURE) प्रमाण:",
        'mineral_mixture_brand_label': "MINERAL MIXTURE ब्रँड नाव:",
        'farmer_use_evm_rtu_label': "शेतकरी वापर (EVM RTU) प्रमाण:",
        'evm_rtu_label': "EVM RTU:",
        'biogas_installed_label': "बायोगॅस स्थापित:",
        'bank_linkage_label': "कोणतेही बँक लिंकेज:",
        'competitor_details_subheader': "स्पर्धक तपशील",
        'competitor1_name_label': "स्पर्धक 1 नाव:",
        'competitor1_milk_label': "स्पर्धक 1 दूध (LPD):",
        'competitor2_name_label': "स्पर्धक 2 नाव:",
        'competitor2_milk_label': "स्पर्धक 2 दूध (LPD):",
        'competitor3_name_label': "स्पर्धक 3 नाव:",
        'competitor3_milk_label': "स्पर्धक 3 दूध (LPD):",
        'competitor4_name_label': "स्पर्धक 4 नाव:",
        'competitor4_milk_label': "स्पर्धक 4 दूध (LPD):",
        
        'photo_upload_header': "BMC फोटो",
        'photo_overall_label': "फोटो 1: एकूण BMC रचना",
        'photo_platform_label': "फोटो 2: प्लॅटफॉर्म/प्रवेश क्षेत्र",
        'photo_inside_label': "फोटो 3: BMC कूलिंग क्षेत्र (आत)",
        'submit_button': "BMC भेट डेटा सबमिट करा",
        'yes': "होय",
        'no': "नाही",
        'others': "इतर",
        'options_gender': ["पुरुष", "महिला"],
        'options_education': ["10वी पास", "12वी पास", "पदवी", "पदव्युत्तर", "इतर"],
        'options_quality': ["खराब", "ठीक", "चांगली", "उत्तम"],
        'options_payment_schedule': ["महिन्यातून प्रत्येक 10 व्या दिवशी", "महिन्यातून दोनदा", "महिन्यातून एकदा", "विशिष्ट वेळापत्रक नाही"],
        'options_payment_method': ["रोख", "बँक ट्रान्सफर", "दोन्ही"],
        'options_awareness_poster': ["एएफएम", "एबी", "सीएमपी", "इतर"]
    }
}

# --- Function to get translated text ---
def t(key):
    return translations[st.session_state.language].get(key, key)

# --- HELPER FUNCTION FOR CONDITIONAL UI (Permanent Specify Field) ---
def render_select_with_specify_permanent(container, label_key, options_list, select_key, specify_label_key, is_multi=False):
    """
    Renders a select widget and a PERMANENT, editable specify text input 
    in a clean two-column layout. The text input remains active regardless of selection.
    
    Returns: (select_output, specify_output)
    """
    
    col_select, col_specify = container.columns([0.5, 0.5])
    specify_key = f"{select_key}_specify"
    
    # Initialize specify state
    if specify_key not in st.session_state:
        st.session_state[specify_key] = ""
    
    with col_select:
        # 1. Render the Select Widget
        if is_multi:
            select_output = st.multiselect(
                t(label_key),
                options_list,
                key=select_key,
                default=[]
            )
        else:
            select_output = st.selectbox(
                t(label_key),
                options_list,
                key=select_key,
                index=0
            )

    with col_specify:
        # 2. Render the *permanent and editable* text input
        # Note: This textbox is ALWAYS editable and visible
        specify_output = st.text_input(
            t(specify_label_key), 
            key=specify_key, 
            label_visibility="visible"
        )
    
    return select_output, specify_output


st.set_page_config(layout="centered", page_title="Ksheersagar - BMC Visit")

# --- Language Selection (persists across pages) ---
if 'language' not in st.session_state:
    st.session_state.language = 'en'

st.sidebar.header(translations['en']['language_select'] + " / " + translations['mr']['language_select'])
lang_options = ["English", "Marathi"]
current_lang_capitalized = st.session_state.language.capitalize()
lang_index = lang_options.index(current_lang_capitalized) if current_lang_capitalized in lang_options else 0

selected_lang_display = st.sidebar.radio("Language", lang_options, index=lang_index, key="lang_radio_bmc")

if selected_lang_display == "English":
    st.session_state.language = 'en'
else:
    st.session_state.language = 'mr'

# --- Data Loading and Initialization ---
if 'bmc_visit_data' not in st.session_state:
    st.session_state.bmc_visit_data = load_existing_data()

# Define static lists (for data consistency)
GOVIND_BMC_NAMES = ["VIGHNAHARTA VIDNI COOLER", "NIRAI DUDH SANKALAN KEND.PANCABIGA", "PAWAR DAIRY ASU", "AJAY DUDH", "JAY HANUMAN BMC NAIKBOMWADI", "SHREE GANESH SASTEWADI BMC", "GOVIND DUDH SANKALAN KENDRA HOL", "JITOBA BULK COOLER JINTI", "JAY MHALLAR DUDH KALAJ", "WAGHESHWARI SASWAD", "BHAIRAVNATH DUDH HINGANGAON", "GOVIND DUDH SANKALAN KENDRA SASWAD", "SHREENATH MILK SANKALAN", "RAJMUDRA DUDH WATHARPHATA BMC", "ROKDESHWAR MILK SANKALAN", "BHAIRAVNATH MANDAVKHADAK COOLER", "SAYALI, MUNJAWADI", "JAY HANUMAN BARAD", "SHIVSHANKAR DUDH BARAD", "CHANDRABHAGA MILK SANKALAN", "KARCHE SAMPAT", "DURGADEVI DUDH ZIRAPVASTI COOLER", "JANAI DUDH SANKALAN KENDRA BMC", "GOKUL DUDH MATHACHIWADI", "GOVIND MAHILA SHVETKRANTI MILK SANKALAN", "VAJUBAI MILK SANKALAN", "SHRIRAM DUDH SANKALAN & SHIT.BHUINJ", "YASHODHAN MILK & MILK PROD. PACWAD", "OM BHAKTI DUDH WAI COW", "MAYURESHWAR DAIRY", "YOGESHWARI MILK SANKALAN", "JAY BHAVANI ANBHULEWADI", "MAHALAXMI MILK", "SHREENATH MILK", "MAHALAXMI DUDH MOHI", "SANCHALIT SUDARSHAN MILK", "MAULI DUDH SANKALAN KENDR.BHALAWADI", "SUPRIYA MILK", "JAGDAMBA DUDH BHATKI", "SHRI GANESH DUDH SAK VARKUTE MASWAD", "DAHIWADI DOCK", "SHREE JAYHARI RANAND PHALTAN COOLER", "SHIVAM DUDH BUDH", "GOMATA DUDH SANKALAN KEND.CHILEWADI", "REVANSIDDHA MILK SANKALAN", "VENKATESH AGRO PROCESSING CO.", "SHIVRAJ DUDH SANKALAN KENDRA", "SHIRAM DUDH PIMPRE DHAIGUDEMALA", "VANGNA DUDH HIVRE COW MILK", "GOWARDHAN MILK COLLECTION", "SHRI DATT DOODH DAIRY ANPATWADI", "JYOTIRLING DUDH SANKALAN KENDRA BORJAIWADI", "SHREE DATT MILK DAIRY AZADPUR", "SHIVKRUPA BMC", "SANT BHAGWANBABA AKOLE", "HINDAVI DAIRY FARM KHADAKI DAUND", "SHIVTEJ DUDH PAWARWASTI BORIBEL", "JAY HANUMAN DUDH VITTHALNAGAR", "BHAIRAVNATH DEVULGOAN RAJE", "A.S.DAIRY FARM", "VENKATESH AGRO PROCESSING CO.", "AKASH DUDH SANKALAN KENDRA", "BHAIRAVNATH MILK SANKALAN", "GOVIND SADASHIVNAGAR", "GOVIND WANIMALA", "GOVIND MILK SANKALAN", "LOKRAJ MILK SANKALAN", "SHAMBHU MAHADEV PHONDSHIRAS", "VISHNU NARAYAN DUDH", "JYOTIRLING DOODH SANKALAN EKSHIV"]
SDDPL_BMC_NAMES = ["SHELKEWASTI", "HAKEWASTI", "KUSEGAON", "NYAWASTI", "NANGAON-2", "PARGAON-1", "PARGAON-2", "PIMPALGAON", "YAWAT", "CHANDANWADI", "DALIMB", "NANDUR", "DELAWADI", "KANGAON", "BETWADI", "KHADKI", "ROTI", "SONAWADI", "GOPALWADI", "HOLEWASTI", "MIRADE", "JAWALI", "VIDANI", "BARAD", "GUNWARE", "SOMANTHALI", "CHAUDHARWADI", "SANGAVI-MOHITEWASTI", "RAUTVASTI VIDANI", "PHADTARWADI", "KAPASHI", "MALEWADI", "SAKHARWADI", "RAVADI", "NIMBLAK", "ASU", "TAMKHADA", "HANUMANTWADI", "KHATAKEVASTI", "SATHEPHATA", "GANEGAONDUMALA", "VADGAON RASAI", "RANJANGAON SANDAS", "BHAMBURDE", "INAMGAON6", "NAGARGAON PHATA", "AJNUJ", "INAMGAON5", "PHARATEWADI", "KURULII", "SHINDODI", "GOLEGAON", "NAGARGAON", "NIMONE", "AMBALE 3", "KARDE", "KANHUR MESAI", "MAHADEVWADI", "NIMGAON MHALUNGI", "DHANORE", "TALEGAON DHAMDHERE", "MANDAVGAN PHARATA", "GUNAT", "KASHTI", "GHADAGEMALA", "INAMGAON3", "WANGDHARI", "URALGAONI", "JAI BHAVANI DUDH SANKLAN KENDRA PIMPRI S", 
"DATTAKRUPA DUDH SANKLAN KENDRA BORGAON ARJ", 
"SHREE SAI SAMARTH DUDH SANKALAN KENDRA", 
"JAY BAJRANGBALI DUDH SANKALAN KENDRA", 
"BHAIRAVNATH DUDH SANKALAN AND SHITKARAN KENDRA", 
"SWARAJ DUDH SANKALAN SHITAKENDR", 
"DYNAMIX DUDH SANKALAN AND SHITKARAN KENDRA", 
"SAMRUDDHI DUDH SANKALAN V SHITKARAN KENDRA", 
"DATTAKRUPA MILK DAIRY", 
"NARENDRA MAULI DUDH SANKALAN SHITKARAN KENDRA", 
"GURUDEV DUDH SANKALAN KENDRA", 
"VILAS NARAYAN GHORPADE", 
"SUNIL NAMDEORAO SAKHARE", 
"BHAIRAVNATHKRUPA DUDHA SANKALAN KENDRA", 
"YUVARAJ DUDH SANKALAN KENDRA", 
"SAMPADA DAIRY DUDH SANKALAN KENDRA", 
"GURUKRUPA DUDH SANKALAN KENDRA DAHIGAON", 
"NAGESHWAR DHUDH SANKALAN V SHITKARAN KENDRA", 
"RUCHI DAIRY", 
"SHREE GANESH CHILLING PLANT", 
"PAVANSAGAR MILK COLLECTION CENTER", 
"BHAIRAVNATH MILK COLLECTION AND CHILLING CENTRE", 
"HANGESHVAR DAIRY", 
"BHAIRAVNATH DUDH SANKLAN KENDRA RAYGAVHAN", 
"SULTANPUR CHILLING CENTRE", 
"SHRI DATTA DIGAMBAR SAHAKARI DUDH SANSTHA", 
"KRUSHIRAJ DUDH SANKALAN KENDRA", 
"BHAIRAVNATH DUDH DAIRY", 
"ANANDRAO BHIVA DHAIGUDE", 
"BIROBA DUDH SANKALAN V SHITKARAN KENDRA", 
"SHIVGANGA MILK CENTER", 
"SHRIKRUSHNA DAIRY", 
"SAI AMRUT DUDH SANKALAN KENDRA", 
 ]
ALL_BMC_NAMES = sorted(list(set(GOVIND_BMC_NAMES + SDDPL_BMC_NAMES)))
CATTLE_FEED_BRAND_OPTIONS = ["Royal Bypro and classic", "Govind Classic Biopro", "Govind Royle Biopro", "SDDPL Samruddhi", "SDDPL Samruddhi Plus", "SDDPL Samruddhi Gold", "SDDPL Shakti", t('others')]

# NEW Sub-District List (Consolidated and Sorted)
NEW_SUB_DISTRICTS = list(set([
    "PHULAMBRI", "KANNAD", "SILLOD", "AURANGABAD", "PATHARDI", "NEWASA", 
    "AHMEDNAGAR", "PARNER", "SHRIGONDA", "KHULTABAD", "KOREGAON", 
    "KHANDALA", "MANN", "KOPARGAON"
]))
SUB_DISTRICT_OPTIONS = sorted(NEW_SUB_DISTRICTS + [t('others')])

# Village List
VILLAGE_NAMES = [
    "ALAND", "BORGAON ARJ", "MOHARA", "KAIGAON", "VIRAMGAON", "BANKINHOLA", "SHEKTA", 
    "WADOD BAJAR", "SULTANWADI", "BABHULGAON", "LEHA", "KAUDGAON JAMB", "KARANJI", 
    "KHANDGAON", "KAUDGAON", "CHICHONDI SHIRAL", "DAHIGAON", "BHENDA", "JAKHANGAON", 
    "PARNER", "DEODAITHAN", "PANOLI 2", "CHIMBHALE", "RAYGAVHAN", "SULTANPUR", 
    "RANDULLABAD", "PARGAON", "SUKHED", "KHED (BK)", "MOGARALE", 
    "PADHEGAON", "JAVALKE"
]
VILLAGE_OPTIONS = sorted(VILLAGE_NAMES + [t('others')])

# Initialize placeholder for Geolocation data (removed feature)
bmc_location = "N/A (Geolocation Feature Removed for Optimization)" 

# --- UI START ---
st.title(t('page_title'))
st.write(t('page_header'))

with st.form(key='bmc_visit_form'):
    
    # --- PHOTO UPLOAD SECTION ---
    st.header(t('photo_upload_header'))
    
    col_photo1, col_photo2, col_photo3 = st.columns(3)
    with col_photo1:
        photo_overall = st.file_uploader(t('photo_overall_label'), type=['jpg', 'jpeg', 'png'], key="photo_overall_upload")
    with col_photo2:
        photo_platform = st.file_uploader(t('photo_platform_label'), type=['jpg', 'jpeg', 'png'], key="photo_platform_upload")
    with col_photo3:
        photo_inside = st.file_uploader(t('photo_inside_label'), type=['jpg', 'jpeg', 'png'], key="photo_inside_upload")

    st.markdown("---")
    
    # --- General Info ---
    st.header(t('general_info_header'))
    
    # BMC Name (Using render_select_with_specify_permanent)
    bmc_name_option, other_bmc_name = render_select_with_specify_permanent(
        st, 
        'bmc_name_label', 
        ["SELECT"] + ALL_BMC_NAMES + [t('others')], 
        'bmc_name_select',
        'other_bmc_name_label'
    )
    actual_bmc_name = other_bmc_name if bmc_name_option == t('others') else bmc_name_option

    # Row 2 (BMC Code, Date, Organization, Activity Creator)
    col1, col2 = st.columns(2)
    
    with col1:
        bmc_code = st.text_input(t('bmc_code_label'))
        scheduled_start_date = st.date_input(t('start_date_label'), value=dt_date(2025, 5, 7))
        organization = st.selectbox(t('organization_label'), ["Govind Milk", "SDDPL"], index=0)
        
        # Surveyor Name (Dr. Shyam fix)
        activity_created_by = st.selectbox(t('activity_created_by_label'), ["Dr. Shyam", "Dr Sachin", "bhusan", "subhrat", "aniket", "ritesh"], index=0)

    with col2:
        # State (UNLOCKED)
        state = st.text_input(t('state_label'), "Maharashtra", disabled=False)
        
        # District (Using render_select_with_specify_permanent)
        district_option, other_district_input = render_select_with_specify_permanent(
            st, 
            'district_label', 
            ["Satara", "Pune", "Ahmednagar", "Solapur", t('others')], 
            'district_select',
            'other_district_label'
        )
        actual_district = other_district_input if district_option == t('others') else district_option

        # Sub District (Using render_select_with_specify_permanent)
        sub_district_option, other_sub_district_input = render_select_with_specify_permanent(
            st, 
            'sub_district_label', 
            SUB_DISTRICT_OPTIONS, # NEW LIST USED HERE
            'sub_district_select',
            'other_sub_district_label'
        )
        actual_sub_district = other_sub_district_input if sub_district_option == t('others') else sub_district_option
        
        # Collecting Village (Numeric)
        collecting_village = st.number_input(t('collecting_village_label'), min_value=0, value=15)
        
        # Village Dropdown (Using render_select_with_specify_permanent)
        village_option, other_village_name = render_select_with_specify_permanent(
            st,
            'village_label',
            VILLAGE_OPTIONS,
            'village_select',
            'other_village_label'
        )
        actual_village = other_village_name if village_option == t('others') else village_option


    # --- BCF Details ---
    st.header(t('bcf_details_header'))
    
    col_farmer1, col_farmer2 = st.columns(2)

    with col_farmer1:
        bcf_name = st.text_input(t('bcf_name_label'), "Sachin Shahuraje Bhosale")
        bcf_gender = st.selectbox(t('bcf_gender_label'), t('options_gender'), index=0)
        
        # Education (Using render_select_with_specify_permanent)
        education, other_education = render_select_with_specify_permanent(
            st, 
            'education_label', 
            t('options_education'), 
            'education_select',
            'other_education_label'
        )
        actual_education = other_education if education == t('others') else education
        
        bcf_mobile_number = st.text_input(t('bcf_mobile_label'), "9096807277")

    with col_farmer2:
        operating_staff_no = st.number_input(t('operating_staff_label'), min_value=0, value=2)
        distance_from_ho_km = st.number_input(t('distance_from_ho_label'), min_value=0, value=25)

    st.subheader("Farmer Counts")
    col_counts1, col_counts2 = st.columns(2)

    with col_counts1:
        st.markdown("**Total Registered Farmers**")
        total_registered_farmer_no = st.number_input(t('total_farmers_label'), min_value=0, value=93, key="total_reg")
        total_men_farmer_no = st.number_input(t('total_men_farmers_label'), min_value=0, value=78, key="total_men")
        total_women_farmer_no = st.number_input(t('total_women_farmers_label'), min_value=0, value=15, key="total_women")
    
    with col_counts2:
        st.markdown("**Active Farmers**")
        active_farmer_no = st.number_input(t('active_farmers_label'), min_value=0, value=65, key="active_reg")
        active_men_farmer_no = st.number_input(t('active_men_farmers_label'), min_value=0, value=55, key="active_men")
        active_women_farmer_no = st.number_input(t('active_women_farmers_label'), min_value=0, value=10, key="active_women")

    # --- Capacity & Collection ---
    st.header(t('capacity_header'))
    col5, col6 = st.columns(2)
    with col5:
        total_tank_capacity = st.number_input(t('total_tank_capacity_label'), min_value=0, value=2500)
        total_capacity_tank1 = st.number_input(t('tank_1_capacity_label'), min_value=0, value=2000)
        total_capacity_tank2 = st.number_input(t('tank_2_capacity_label'), min_value=0, value=500)
        total_capacity_tank3 = st.number_input(t('tank_3_capacity_label'), min_value=0, value=0)
        total_capacity_tank4 = st.number_input(t('tank_4_capacity_label'), min_value=0, value=0)
        space_segregation_tank = st.text_input(t('segregation_tank_space_label'), "500 lit segregation tank available")
    with col6:
        milk_segregated_lpd = st.number_input(t('milk_segregated_label'), min_value=0, value=320)
        morning_collection_time_label = st.number_input(t('morning_collection_time_label'), min_value=0.0, value=9.3, step=0.1)
        morning_milk_lpd = st.number_input(t('morning_milk_lpd_label'), min_value=0, value=1250)
        morning_farmers_no = st.number_input(t('morning_farmers_label'), min_value=0, value=40)
        evening_collection_time_label = st.number_input(t('evening_collection_time_label'), min_value=0.0, value=9.0, step=0.1)
        evening_milk_lpd = st.number_input(t('evening_milk_lpd_label'), min_value=0, value=1100)
        evening_farmers_no = st.number_input(t('evening_farmers_label'), min_value=0, value=25)
    
    # --- Infrastructure & Compliance ---
    st.header(t('infra_compliance_header'))
    overall_infrastructure = st.selectbox(t('overall_infra_label'), t('options_quality'), index=2)
    remark_infra = st.text_area(t('remark_infra_label'), "Good infrastructure, seprate room for cattle feed")
    bmc_cleaning_hygiene = st.selectbox(t('bmc_cleaning_label'), t('options_quality'), index=2)

    col_infra1, col_infra2, col_infra3, col_infra4 = st.columns(4)
    yes_no_options = [t('yes'), t('no')]
    with col_infra1:
        air_curtain = st.radio(t('air_curtain_label'), yes_no_options, index=0, key="air_curtain_bmc")
        fly_catcher = st.radio(t('fly_catcher_label'), yes_no_options, index=0, key="fly_catcher_bmc")
    with col_infra2:
        wash_basin = st.radio(t('wash_basin_label'), yes_no_options, index=0, key="wash_basin_bmc")
        opening_window_door = st.radio(t('opening_window_door_label'), yes_no_options, index=0, key="opening_window_door_bmc")
    with col_infra3:
        intact_floor = st.radio(t('intact_floor_label'), yes_no_options, index=0, key="intact_floor_bmc")
        digitize_system = st.radio(t('digitize_system_label'), yes_no_options, index=0, key="digitize_system_bmc")
    with col_infra4:
        fssai_licence = st.radio(t('fssai_licence_label'), yes_no_options, index=0, key="fssai_licence_bmc")
        wg_scale_licence = st.radio(t('wg_scale_licence_label'), yes_no_options, index=1, key="wg_scale_licence_bmc")

    # New Yes/No Questions and Awareness Poster
    col_new_infra1, col_new_infra2, col_new_infra3, col_new_infra4 = st.columns(4)
    with col_new_infra1:
        sop_available = st.radio(t('sop_available_label'), yes_no_options, index=0, key="sop_available_bmc")
    with col_new_infra2:
        hot_water_available = st.radio(t('hot_water_available_label'), yes_no_options, index=0, key="hot_water_available_bmc")
    with col_new_infra3:
        notice_board_available = st.radio(t('notice_board_available_label'), yes_no_options, index=0, key="notice_board_available_bmc")
    with col_new_infra4:
        # Awareness Poster (Using render_select_with_specify_permanent)
        awareness_poster, other_awareness_poster = render_select_with_specify_permanent(
            st, 
            'awareness_poster_label', 
            t('options_awareness_poster'), 
            'awareness_poster_select',
            'other_awareness_poster_label',
            is_multi=True
        )


    # --- Payment Section ---
    st.header(t('payment_header'))
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        payment_schedule = st.radio(t('payment_schedule_label'), t('options_payment_schedule'), index=0, key="payment_schedule_bmc")
    with col_pay2:
        payment_method = st.multiselect(t('payment_method_label'), t('options_payment_method'), default=[t('options_payment_method')[0]])


    # --- Farmer & Competitor Details ---
    st.header(t('farmer_competitor_header'))
    col9, col10 = st.columns(2)
    with col9:
        animal_welfare_farm_no = st.number_input(t('animal_welfare_farm_label'), min_value=0, value=9)
        farmer_use_cattle_feed = st.number_input(t('farmer_use_cattle_feed_label'), min_value=0, value=58)
        cattle_feed_bag_sale_month = st.number_input(t('cattle_feed_bag_sale_label'), min_value=0, value=250)
        
        # Cattle Feed Brand (Using render_select_with_specify_permanent)
        cattle_feed_brand_name, other_cattle_feed_brand_name = render_select_with_specify_permanent(
            st, 
            'cattle_feed_brand_label', 
            CATTLE_FEED_BRAND_OPTIONS, 
            'cattle_feed_brand_select',
            'other_cattle_feed_brand_label',
            is_multi=True
        )
        
        farmer_use_mineral_mixture_qty = st.number_input(t('farmer_use_mineral_mixture_label'), min_value=0, value=14)
        mineral_mixture_brand_name = st.text_input(t('mineral_mixture_brand_label'), "Govind Chileted")
        farmer_use_evm_rtu_qty = st.number_input(t('farmer_use_evm_rtu_label'), min_value=0, value=0)
        evm_rtu = st.text_input(t('evm_rtu_label'), "NA")
        biogas_installed = st.number_input(t('biogas_installed_label'), min_value=0, value=8)
        any_bank_linkage = st.text_input(t('bank_linkage_label'), "No")
    with col10:
        st.subheader(t('competitor_details_subheader'))
        competitor1_name = st.text_input(t('competitor1_name_label'), "Heritage")
        competitor1_milk_lpd = st.number_input(t('competitor1_milk_label'), min_value=0, value=1300, key="comp1_milk_lpd")
        competitor2_name = st.text_input(t('competitor2_name_label'), "Amul")
        competitor2_milk_lpd = st.number_input(t('competitor2_milk_label'), min_value=0, value=2500, key="comp2_milk_lpd")
        competitor3_name = st.text_input(t('competitor3_name_label'), "Dynamix")
        competitor3_milk_lpd = st.number_input(t('competitor3_milk_label'), min_value=0, value=1100, key="comp3_milk_lpd")
        competitor4_name = st.text_input(t('competitor4_name_label'))
        competitor4_milk_lpd = st.number_input(t('competitor4_milk_label'), min_value=0, value=0, key="comp4_milk_lpd")

    st.markdown("---")
    # FINAL SUBMIT BUTTON
    submit_button = st.form_submit_button(label=t('submit_button'))

    if submit_button:
        # Convert translated answers back to English for data consistency
        yes_en, no_en = translations['en']['yes'], translations['en']['no']
        
        submitted_data = {
            "Geolocation (Lat, Long)": bmc_location,
            "Photo 1 (Overall BMC)": photo_overall.name if 'photo_overall' in locals() and photo_overall else "N/A",
            "Photo 2 (Platform)": photo_platform.name if 'photo_platform' in locals() and photo_platform else "N/A",
            "Photo 3 (Inside BMC)": photo_inside.name if 'photo_inside' in locals() and photo_inside else "N/A",
            
            # --- General Info ---
            "BMC Code": bmc_code,
            "SCHEDULED START DATE": scheduled_start_date.isoformat() if scheduled_start_date else None,
            "BMC Name": actual_bmc_name,
            "Other BMC Name": other_bmc_name,
            "ACTIVITY CREATED BY": activity_created_by,
            "Organization": organization,
            "State": state,
            "District": actual_district,
            "Other District": other_district_input,
            "Sub District": actual_sub_district,
            "Other Sub District": other_sub_district_input,
            "Collecting Village": collecting_village, 
            "Village": village_option, 
            "Other Village": other_village_name, 
            
            # --- BCF Details ---
            "BCF Name": bcf_name,
            "BCF Gender": translations['en']['options_gender'][t('options_gender').index(bcf_gender)],
            "Education": actual_education,
            "Other Education": other_education,
            "BCF Mobile Number": bcf_mobile_number,
            "Operating Staff (No.)": operating_staff_no,
            "Distance From HO (KM)": distance_from_ho_km,
            
            # Farmer Counts (Data Capture)
            "Total Registered Farmer (No.)": total_registered_farmer_no,
            "No. of Women Farmers (Total Registered)": total_women_farmer_no, 
            "No. of Men Farmers (Total Registered)": total_men_farmer_no, 
            "Active Farmer (No.)": active_farmer_no,
            "No. of Women Farmers (Active Farmers)": active_women_farmer_no, 
            "No. of Men Farmers (Active Farmers)": active_men_farmer_no, 
            
            # --- Capacity & Collection ---
            "Total Tank Capacity": total_tank_capacity,
            "Total Capacity (Tank 1)": total_capacity_tank1,
            "Total Capacity (Tank 2)": total_capacity_tank2,
            "Total Capacity (Tank 3)": total_capacity_tank3,
            "Total Capacity (Tank 4)": total_capacity_tank4,
            "Space available for Segregation Tank": space_segregation_tank,
            "MILK SEGREGATED (LPD)": milk_segregated_lpd,
            "MORNING MILK COLLECTION END TIME": morning_collection_time_label,
            "MORNING MILK (LPD)": morning_milk_lpd,
            "No. of Farmers (Morning Milk Collected)": morning_farmers_no, 
            "EVENING MILK COLLECTION END TIME": evening_collection_time_label,
            "EVENING MILK (LPD)": evening_milk_lpd,
            "No. of Farmers (Evening Milk Collected)": evening_farmers_no, 
            
            # --- Infrastructure & Compliance ---
            "Overall Infrastructure": overall_infrastructure,
            "Remark (Infrastructure)": remark_infra,
            "BMC Cleaning & Hygiene": bmc_cleaning_hygiene,
            "Air curtain": yes_en if air_curtain == t('yes') else no_en,
            "Fly Catcher": yes_en if fly_catcher == t('yes') else no_en,
            "Wash Basin": yes_en if wash_basin == t('yes') else no_en,
            "Opening(Window/Door)": yes_en if opening_window_door == t('yes') else no_en,
            "Intact Floor in BMC Premise": yes_en if intact_floor == t('yes') else no_en,
            "Digitize System": yes_en if digitize_system == t('yes') else no_en,
            "FSSAI Licence": yes_en if fssai_licence == t('yes') else no_en,
            "Wg Scale Licence": yes_en if wg_scale_licence == t('yes') else no_en,
            
            # New Yes/No Questions Data
            "Is SOP Available": yes_en if sop_available == t('yes') else no_en,
            "Is Hot Water Available": yes_en if hot_water_available == t('yes') else no_en,
            "Is Notice Board Available": yes_en if notice_board_available == t('yes') else no_en,
            
            # Awareness Poster Data
            "Awareness Poster": ', '.join(awareness_poster),
            "Other Awareness Poster": other_awareness_poster,

            # --- Payment Section ---
            "Payment Schedule": payment_schedule,
            "Payment Method": ', '.join(payment_method),
            
            # --- Farmer & Competitor Details ---
            "Animal Welfare Farm (No.)": animal_welfare_farm_no,
            "FARMER USE (compliant CATTLE FEED)": farmer_use_cattle_feed,
            "Compliant Cattle Feed bag sale (month)": cattle_feed_bag_sale_month,
            "Cattle Feed Brand Name": ', '.join(cattle_feed_brand_name),
            "Other Cattle Feed Brand Name": other_cattle_feed_brand_name,
            "FARMER USE (MINERAL MIXTURE) Quantity": farmer_use_mineral_mixture_qty, 
            "MINERAL MIXTURE BRAND NAME": mineral_mixture_brand_name,
            "FARMER USE (EVM RTU) Quantity": farmer_use_evm_rtu_qty,
            "EVM RTU": evm_rtu,
            "BIOGAS INSTALLED": biogas_installed,
            "ANY BANK LINKAGE": any_bank_linkage,
            "COMPETITOR 1 NAME": competitor1_name,
            "COMPETITOR 1 MILK (LPD)": competitor1_milk_lpd,
            "Competitor 2 Name": competitor2_name,
            "Competitor 2 MILK (LPD)": competitor2_milk_lpd,
            "Competitor 3 Name": competitor3_name,
            "Competitor 3 MILK (LPD)": competitor3_milk_lpd,
            "Competitor 4 Name": competitor4_name,
            "Competitor 4 MILK (LPD)": competitor4_milk_lpd,
        }
        
        st.session_state.bmc_visit_data.append(submitted_data)
        
        df_new_entry = pd.DataFrame([submitted_data])
        if not os.path.exists(BMC_VISIT_DATA_FILE):
             df_new_entry.to_csv(BMC_VISIT_DATA_FILE, index=False)
        else:
             df_new_entry.to_csv(BMC_VISIT_DATA_FILE, mode='a', index=False, header=False)
        
        st.success("BMC Visit data submitted and saved!")

# --- Data Viewing and Admin Section ---
st.header("Real-time View & Download")
if st.session_state.bmc_visit_data:
    st.subheader("All Submitted BMC Visit Entries:")
    df_bmc_visit_all = pd.DataFrame(st.session_state.bmc_visit_data).astype(str)
    st.dataframe(df_bmc_visit_all, use_container_width=True)
    csv_bmc_visit_all = df_bmc_visit_all.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download All BMC Visit Data as CSV",
        data=csv_bmc_visit_all,
        file_name="all_bmc_visit_data.csv",
        mime="text/csv",
    )
else:
    st.info("No BMC Visit data submitted yet.")
