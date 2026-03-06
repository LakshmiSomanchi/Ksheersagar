import streamlit as st
import pandas as pd
from datetime import date as dt_date
import os

# --- NEW IMPORT FOR AUTO-GPS ---
# You must run: pip install streamlit-js-eval
try:
    from streamlit_js_eval import get_geolocation
except ImportError:
    st.error("Please install the missing package by running: pip install streamlit-js-eval")

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

# --- Translation Dictionary ---
translations = {
    'en': {
        'page_title': "🚚 Ksheersagar - BMC/MCC Visit Data Entry",
        'page_header': "Please fill out the details for the BMC/MCC visit below.",
        'language_select': "Select Language",
        'general_info_header': "General BMC/MCC Visit Information",
        'bmc_code_label': "BMC/MCC Code:",
        'start_date_label': "SCHEDULED START DATE:",
        'organization_label': "Organization:",
        
        'bmc_name_label': "BMC Name:", 
        'other_bmc_name_label': "If Others, Specify BMC Name:",
        'mcc_name_label': "MCC Name:", 
        'other_mcc_name_label': "If Others, Specify MCC Name:",
        
        'activity_created_by_label': "ACTIVITY CREATED BY:",
        'state_label': "State:",
        'district_label': "District:",
        'sub_district_label': "Sub District:",
        'other_district_label': "If Others, Specify District:",
        'other_sub_district_label': "If Others, Specify Sub District:",
        'collecting_village_label': "Collecting Village (No.):", 
        'village_label': "Village:",
        'other_village_label': "If Others, Specify Village:",
        'geolocation_header': "Geolocation Details (Auto-GPS)",
        'latitude_label': "Latitude (Auto-detected):",
        'longitude_label': "Longitude (Auto-detected):",
        
        'bcf_details_header': "BCF/MCC In-charge Details",
        'bcf_name_label': "BCF/In-charge Name:",
        'bcf_gender_label': "Gender:",
        'education_label': "Education:",
        'other_education_label': "If Others, Specify Education:",
        'bcf_mobile_label': "Mobile Number:",
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
        'total_routes_label': "Total No. of Routes:",
        'total_vlcs_label': "Total No. of VLCs:",
        'offline_vlcs_label': "Offline VLCs:",
        'online_vlcs_label': "Online VLCs:",
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

        'quality_payment_header': "Testing & Quality",
        'afm_tested_label': "AFM tested at BMC level:",
        'afm_quantity_label': "If yes, what is the quantity?",
        'afm_season_label': "If yes, in which season it comes positive?",
        'mb_scanner_label': "MB scanner available:",
        'mbrt_time_label': "Avg testing time of MBRT:",
        
        'infra_compliance_header': "Infrastructure & Compliance",
        'overall_infra_label': "Overall Infrastructure:",
        'remark_infra_label': "Remark (Infrastructure):",
        'bmc_cleaning_label': "BMC/MCC Cleaning & Hygiene:",
        'air_curtain_label': "Air curtain:",
        'fly_catcher_label': "Fly Catcher:",
        'wash_basin_label': "Wash Basin:",
        'opening_window_door_label': "Opening (Window/Door):",
        'intact_floor_label': "Intact Floor in Premise:",
        
        'digitize_system_label': "Digitize System:",
        'digitize_system_brand_label': "If Yes - Indifoss or Ekomilk:",
        
        'mbrt_facility_label': "MBRT Testing Facility:",
        'data_recorded_label': "How is dairy data processed and recorded?",
        'software_used_label': "If digitally, which software is used?",
        
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
        
        'farmer_competitor_header': "Farmer Services & Competitor Details",
        'health_camp_freq_label': "Frequency of health camps organized by BMC:",
        'helpdesk_label': "Is there a helpdesk set-up in your BMC?",
        'mastitis_drive_label': "Are Mastitis preventive drives conducted?",
        'training_label': "Are there regular trainings conducted for trainers?",
        
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
        'other_services_label': "Other Services:", 
        
        'competitor_details_subheader': "Competitor Details",
        'competitor1_name_label': "COMPETITOR 1 NAME:",
        'competitor1_milk_label': "COMPETITOR 1 MILK (LPD):",
        'competitor2_name_label': "Competitor 2 Name:",
        'competitor2_milk_label': "Competitor 2 MILK (LPD):",
        'competitor3_name_label': "Competitor 3 Name:",
        'competitor3_milk_label': "Competitor 3 MILK (LPD):",
        'competitor4_name_label': "Competitor 4 Name:",
        'competitor4_milk_label': "Competitor 4 MILK (LPD):",
        
        'photo_upload_header': "BMC/MCC Photos",
        'photo_overall_label': "Photo 1: Overall Structure",
        'photo_platform_label': "Photo 2: Platform/Entry Area",
        'photo_inside_label': "Photo 3: Cooling Area (Inside)",
        'submit_button': "Submit Visit Data",
        'yes': "YES",
        'no': "NO",
        'others': "OTHERS",
        'options_gender': ["MALE", "FEMALE"],
        'options_education': ["10th pass", "12th pass", "Graduation", "Post graduation", "OTHERS"], 
        'options_quality': ["Poor", "Fair", "Good", "Best"],
        'options_payment_schedule': ["Every 10th day in a month", "Twice a month", "Once a month", "No specific schedule"],
        'options_payment_method': ["Cash", "Bank Transfer", "Both"], 
        'options_awareness_poster': ["afm", "ab", "cmp", "OTHERS"],
        'options_health_camp': ["Monthly", "Quarterly", "Yearly", "No specific schedule"],
        'options_data_recorded': ["Manually", "Digitally", "Both"],
        'options_seasons': ["Summer", "Monsoon", "Winter", "All"],
        'options_mbrt_facility': ["None", "MBRT Scanner", "MBRT Water bath"]
    },
    'mr': {
        'page_title': "🚚 क्षीरसागर - BMC/MCC भेट डेटा एंट्री",
        'page_header': "कृपया खालील BMC/MCC भेटीसाठी तपशील भरा.",
        'language_select': "भाषा निवडा",
        'general_info_header': "सर्वसाधारण BMC/MCC भेट माहिती",
        'bmc_code_label': "BMC/MCC कोड:",
        'start_date_label': "नियोजित प्रारंभ तारीख:",
        'organization_label': "संस्था:",
        
        'bmc_name_label': "BMC नाव:",
        'other_bmc_name_label': "इतर असल्यास, BMC नाव नमूद करा:",
        'mcc_name_label': "MCC नाव:", 
        'other_mcc_name_label': "इतर असल्यास, MCC नाव नमूद करा:",
        
        'activity_created_by_label': "ऍक्टिव्हिटी कोणी तयार केली:",
        'state_label': "राज्य:",
        'district_label': "जिल्हा:",
        'sub_district_label': "उप-जिल्हा:",
        'other_district_label': "इतर असल्यास, जिल्हा नमूद करा:",
        'other_sub_district_label': "इतर असल्यास, उप-जिल्हा नमूद करा:",
        'collecting_village_label': "संकलन गाव (संख्या):",
        'village_label': "गाव:",
        'other_village_label': "इतर असल्यास, गाव नमूद करा:",
        'geolocation_header': "स्थान तपशील (Auto-GPS)",
        'latitude_label': "अक्षांश (Automatic):",
        'longitude_label': "रेखांश (Automatic):",
        
        'bcf_details_header': "BCF/MCC प्रमुख तपशील",
        'bcf_name_label': "BCF/प्रमुख नाव:",
        'bcf_gender_label': "लिंग:",
        'education_label': "शिक्षण:",
        'other_education_label': "इतर असल्यास, शिक्षण नमूद करा:",
        'bcf_mobile_label': "मोबाईल नंबर:",
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
        'total_routes_label': "एकूण मार्ग (Routes):",
        'total_vlcs_label': "एकूण VLC (संख्या):",
        'offline_vlcs_label': "ऑफलाइन VLC:",
        'online_vlcs_label': "ऑनलाइन VLC:",
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

        'quality_payment_header': "चाचणी आणि गुणवत्ता (Testing & Quality)",
        'afm_tested_label': "BMC स्तरावर AFM तपासले जाते का:",
        'afm_quantity_label': "जर होय, तर प्रमाण किती आहे?",
        'afm_season_label': "जर होय, कोणत्या ऋतूत ते पॉझिटिव्ह येते?",
        'mb_scanner_label': "MB स्कॅनर उपलब्ध आहे का:",
        'mbrt_time_label': "MBRT ची सरासरी चाचणी वेळ:",

        'infra_compliance_header': "पायाभूत सुविधा आणि अनुपालन",
        'overall_infra_label': "एकूण पायाभूत सुविधा:",
        'remark_infra_label': "टीप (पायाभूत सुविधा):",
        'bmc_cleaning_label': "BMC/MCC स्वच्छता आणि आरोग्य:",
        'air_curtain_label': "एअर पडदा:",
        'fly_catcher_label': "माशी पकडणारा:",
        'wash_basin_label': "वॉश बेसिन:",
        'opening_window_door_label': "उघडणे (खिडकी/दार):",
        'intact_floor_label': "BMC परिसरात अखंड मजला:",
        
        'digitize_system_label': "डिजिटायझ प्रणाली:",
        'digitize_system_brand_label': "जर होय - Indifoss किंवा Ekomilk:", 
        
        'mbrt_facility_label': "MBRT चाचणी सुविधा:",
        'data_recorded_label': "डेअरी डेटा कसा प्रोसेस आणि रेकॉर्ड केला जातो?",
        'software_used_label': "जर डिजिटल पद्धतीने, तर कोणते सॉफ्टवेअर वापरले जाते?",
        
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
        
        'farmer_competitor_header': "शेतकरी सेवा आणि स्पर्धक तपशील",
        'health_camp_freq_label': "BMC द्वारे आयोजित आरोग्य शिबिरांची वारंवारता:",
        'helpdesk_label': "तुमच्या BMC मध्ये हेल्पडेस्क आहे का?",
        'mastitis_drive_label': "स्तनदाह (Mastitis) प्रतिबंधक मोहीम राबवली जाते का?",
        'training_label': "प्रशिक्षकांसाठी नियमित प्रशिक्षण दिले जाते का?",
        
        'animal_welfare_farm_label': "पशु कल्याण फार्म (संख्या):",
        'farmer_use_cattle_feed_label': "शेतकरी वापर (compliant CATTLE FEED):",
        'cattle_feed_bag_sale_label': "Compliant Cattle Feed बॅग विक्री (महिना):",
        'cattle_feed_brand_label': "Cattle Feed ब्रँड नाव:",
        'other_cattle_feed_brand_label': "इतर असल्यास, Cattle Feed ब्रँड नाव नमूद करा:",
        'farmer_use_mineral_mixture_label': "शेतकरी वापर (MINERAL MIXTURE) प्रमाण:",
        'mineral_mixture_brand_label': "MINERAL MIXTURE ब्रँड नाव:",
        'farmer_use_evm_rtu_label': "शेतकरी वापर (EVM RTU) प्रमाण:",
        'evm_rtu_label': "EVM RTU:",
        'biogas_installed_label': "बायोगैस स्थापित:",
        'bank_linkage_label': "कोणतेही बँक लिंकेज:",
        'other_services_label': "इतर सेवा:", 
        'competitor_details_subheader': "स्पर्धक तपशील",
        'competitor1_name_label': "स्पर्धक 1 नाव:",
        'competitor1_milk_label': "स्पर्धक 1 दूध (LPD):",
        'competitor2_name_label': "स्पर्धक 2 नाव:",
        'competitor2_milk_label': "स्पर्धक 2 दूध (LPD):",
        'competitor3_name_label': "स्पर्धक 3 नाव:",
        'competitor3_milk_label': "स्पर्धक 3 दूध (LPD):",
        'competitor4_name_label': "स्पर्धक 4 नाव:",
        'competitor4_milk_label': "स्पर्धक 4 दूध (LPD):",
        
        'photo_upload_header': "BMC/MCC Photos",
        'photo_overall_label': "फोटो 1: एकूण रचना",
        'photo_platform_label': "फोटो 2: प्लॅटफॉर्म/प्रवेश क्षेत्र",
        'photo_inside_label': "फोटो 3: कूलिंग क्षेत्र (आत)",
        'submit_button': "भेट डेटा सबमिट करा",
        'yes': "होय",
        'no': "नाही",
        'others': "इतर",
        'options_gender': ["पुरुष", "महिला"],
        'options_education': ["10वी पास", "12वी पास", "पदवी", "पदव्युत्तर", "इतर"],
        'options_quality': ["खराब", "ठीक", "चांगली", "उत्तम"],
        'options_payment_schedule': ["महिन्यातून प्रत्येक 10 व्या दिवशी", "महिन्यातून दोनदा", "महिन्यातून एकदा", "विशिष्ट वेळापत्रक नाही"],
        'options_payment_method': ["रोख", "बँक ट्रान्सफर", "दोन्ही"],
        'options_awareness_poster': ["एएफएम", "एबी", "सीएमपी", "इतर"],
        'options_health_camp': ["मासिक", "त्रैमासिक", "वार्षिक", "विशिष्ट वेळापत्रक नाही"],
        'options_data_recorded': ["मॅन्युअली (Manually)", "डिजिटली (Digitally)", "दोन्ही (Both)"],
        'options_seasons': ["उन्हाळा", "पावसाळा", "हिवाळा", "सर्व"],
        'options_mbrt_facility': ["काहीही नाही (None)", "MBRT स्कॅनर (MBRT Scanner)", "MBRT वॉटर बाथ (MBRT Water bath)"]
    },
    'hi': {
        'page_title': "🚚 क्षीरसागर - BMC/MCC विजिट डेटा एंट्री",
        'page_header': "कृपया नीचे BMC/MCC विजिट के विवरण भरें।",
        'language_select': "भाषा चुनें",
        'general_info_header': "सामान्य BMC/MCC विजिट जानकारी",
        'bmc_code_label': "BMC/MCC कोड:",
        'start_date_label': "निर्धारित प्रारंभ तिथि:",
        'organization_label': "संगठन:",
        
        'bmc_name_label': "BMC का नाम:",
        'other_bmc_name_label': "यदि अन्य, तो BMC का नाम निर्दिष्ट करें:",
        'mcc_name_label': "MCC का नाम:", 
        'other_mcc_name_label': "यदि अन्य, तो MCC का नाम निर्दिष्ट करें:",
        
        'activity_created_by_label': "गतिविधि किसके द्वारा बनाई गई:",
        'state_label': "राज्य:",
        'district_label': "ज़िला:",
        'sub_district_label': "उप-ज़िला:",
        'other_district_label': "यदि अन्य, तो ज़िला निर्दिष्ट करें:",
        'other_sub_district_label': "यदि अन्य, तो उप-ज़िला निर्दिष्ट करें:",
        'collecting_village_label': "कलेक्शन गाँव (संख्या):",
        'village_label': "गाँव:",
        'other_village_label': "यदि अन्य, तो गाँव निर्दिष्ट करें:",
        'geolocation_header': "जियोलोकेशन विवरण (Auto-GPS)",
        'latitude_label': "अक्षांश (स्वचालित):",
        'longitude_label': "देशांतर (स्वचालित):",
        
        'bcf_details_header': "BCF/MCC प्रभारी विवरण",
        'bcf_name_label': "BCF/प्रभारी का नाम:",
        'bcf_gender_label': "लिंग:",
        'education_label': "शिक्षा:",
        'other_education_label': "यदि अन्य, तो शिक्षा निर्दिष्ट करें:",
        'bcf_mobile_label': "मोबाइल नंबर:",
        'operating_staff_label': "ऑपरेटिंग स्टाफ (संख्या):",
        'distance_from_ho_label': "HO से दूरी (किमी):",
        
        # Farmer Metrics
        'total_farmers_label': "कुल पंजीकृत किसान (संख्या):",
        'total_women_farmers_label': "महिला किसानों की संख्या (कुल पंजीकृत):",
        'total_men_farmers_label': "पुरुष किसानों की संख्या (कुल पंजीकृत):",
        'active_farmers_label': "सक्रिय किसान (संख्या):",
        'active_women_farmers_label': "महिला किसानों की संख्या (सक्रिय किसान):",
        'active_men_farmers_label': "पुरुष किसानों की संख्या (सक्रिय किसान):",
        
        'capacity_header': "क्षमता और संकलन (कलेक्शन) विवरण",
        'total_routes_label': "रूट्स की कुल संख्या:",
        'total_vlcs_label': "VLCs की कुल संख्या:",
        'offline_vlcs_label': "ऑफ़लाइन VLCs:",
        'online_vlcs_label': "ऑनलाइन VLCs:",
        'total_tank_capacity_label': "कुल टैंक क्षमता:",
        'tank_1_capacity_label': "कुल क्षमता (टैंक 1):",
        'tank_2_capacity_label': "कुल क्षमता (टैंक 2):",
        'tank_3_capacity_label': "कुल क्षमता (टैंक 3):",
        'tank_4_capacity_label': "कुल क्षमता (टैंक 4):",
        'segregation_tank_space_label': "सेग्रीगेशन टैंक के लिए उपलब्ध स्थान:",
        'milk_segregated_label': "दूध सेग्रीगेट किया गया (LPD):",
        'morning_collection_time_label': "सुबह के दूध संकलन का अंतिम समय (उदा. 9:30 AM के लिए 9.3):",
        'morning_milk_lpd_label': "सुबह का दूध (LPD):",
        'morning_farmers_label': "किसानों की संख्या (सुबह का दूध):",
        'evening_collection_time_label': "शाम के दूध संकलन का अंतिम समय (उदा. 9:00 PM के लिए 9):",
        'evening_milk_lpd_label': "शाम का दूध (LPD):",
        'evening_farmers_label': "किसानों की संख्या (शाम का दूध):",

        'quality_payment_header': "परीक्षण और गुणवत्ता (Testing & Quality)",
        'afm_tested_label': "BMC स्तर पर AFM का परीक्षण किया गया:",
        'afm_quantity_label': "यदि हाँ, तो मात्रा क्या है?",
        'afm_season_label': "यदि हाँ, तो किस मौसम में यह पॉज़िटिव आता है?",
        'mb_scanner_label': "MB स्कैनर उपलब्ध है:",
        'mbrt_time_label': "MBRT का औसत परीक्षण समय:",

        'infra_compliance_header': "बुनियादी ढांचा (Infrastructure) और अनुपालन",
        'overall_infra_label': "संपूर्ण बुनियादी ढांचा:",
        'remark_infra_label': "टिप्पणी (बुनियादी ढांचा):",
        'bmc_cleaning_label': "BMC/MCC सफाई और स्वच्छता:",
        'air_curtain_label': "एयर कर्टेन:",
        'fly_catcher_label': "फ्लाई कैचर (मक्खी पकड़ने वाला):",
        'wash_basin_label': "वॉश बेसिन:",
        'opening_window_door_label': "ओपनिंग (खिड़की/दरवाजा):",
        'intact_floor_label': "परिसर में फर्श बरकरार है:",
        
        'digitize_system_label': "डिजिटाइज़ सिस्टम:",
        'digitize_system_brand_label': "यदि हाँ - Indifoss या Ekomilk:", 
        
        'mbrt_facility_label': "MBRT परीक्षण सुविधा:",
        'data_recorded_label': "डेयरी डेटा कैसे प्रोसेस और रिकॉर्ड किया जाता है?",
        'software_used_label': "यदि डिजिटल रूप से, तो कौन सा सॉफ्टवेयर उपयोग किया जाता है?",
        
        'fssai_licence_label': "FSSAI लाइसेंस:",
        'remark_fssai_label': "टिप्पणी (FSSAI):",
        'wg_scale_licence_label': "वजन कांटा लाइसेंस:",
        'sops_label': "SOP's:",
        'sop_available_label': "क्या SOP उपलब्ध है:",
        'hot_water_available_label': "क्या गर्म पानी उपलब्ध है:",
        'notice_board_available_label': "क्या नोटिस बोर्ड उपलब्ध है:",
        'awareness_poster_label': "जागरूकता पोस्टर:",
        'other_awareness_poster_label': "यदि अन्य, तो जागरूकता पोस्टर निर्दिष्ट करें:",
        'stirrer_label': "स्टिरर/इकोमिल्क/इंडिफॉस:",
        'remark_stirrer_label': "टिप्पणी (स्टिरर/इकोमिल्क/इंडिफॉस):",
        'sampler_label': "सैम्पलर/डिपर/प्लंजर:",
        'remark_sampler_label': "टिप्पणी (सैम्पलर/डिपर/प्लंजर):",
        'milk_temp_check_label': "दूध का तापमान जांच:",
        'remark_milk_temp_label': "टिप्पणी (दूध का तापमान):",
        'cleaning_chemicals_label': "सफाई रसायन (केमिकल्स):",
        'remark_cleaning_chemicals_label': "टिप्पणी (सफाई रसायन):",
        'hot_water_source_label': "गर्म पानी का स्रोत:",
        'remark_hot_water_label': "टिप्पणी (गर्म पानी का स्रोत):",
        'strainer_label': "छलनी/नायलॉन का कपड़ा उपलब्ध है:",
        'sample_bottle_label': "सैंपल बोतल:",

        'payment_header': "भुगतान (Payment)",
        'payment_schedule_label': "भुगतान अनुसूची:",
        'payment_method_label': "भुगतान का तरीका:",
        
        'farmer_competitor_header': "किसान सेवाएं और प्रतियोगी विवरण",
        'health_camp_freq_label': "BMC द्वारा आयोजित स्वास्थ्य शिविरों की आवृत्ति:",
        'helpdesk_label': "क्या आपके BMC में हेल्पडेस्क है?",
        'mastitis_drive_label': "क्या थनैला (Mastitis) निवारक अभियान चलाए जाते हैं?",
        'training_label': "क्या प्रशिक्षकों के लिए नियमित प्रशिक्षण आयोजित किए जाते हैं?",
        
        'animal_welfare_farm_label': "पशु कल्याण फार्म (संख्या):",
        'farmer_use_cattle_feed_label': "किसानों का उपयोग (कैटल फीड):",
        'cattle_feed_bag_sale_label': "कैटल फीड बैग की बिक्री (महीना):",
        'cattle_feed_brand_label': "कैटल फीड ब्रांड का नाम:",
        'other_cattle_feed_brand_label': "यदि अन्य, तो कैटल फीड ब्रांड निर्दिष्ट करें:",
        'farmer_use_mineral_mixture_label': "किसानों का उपयोग (मिनरल मिक्चर) मात्रा:",
        'mineral_mixture_brand_label': "मिनरल मिक्चर ब्रांड का नाम:",
        'farmer_use_evm_rtu_label': "किसानों का उपयोग (EVM RTU) मात्रा:",
        'evm_rtu_label': "EVM RTU:",
        'biogas_installed_label': "बायोगैस स्थापित:",
        'bank_linkage_label': "कोई बैंक लिंकेज:",
        'other_services_label': "अन्य सेवाएं:", 
        'competitor_details_subheader': "प्रतियोगी (कम्पेटिटर) विवरण",
        'competitor1_name_label': "प्रतियोगी 1 का नाम:",
        'competitor1_milk_label': "प्रतियोगी 1 का दूध (LPD):",
        'competitor2_name_label': "प्रतियोगी 2 का नाम:",
        'competitor2_milk_label': "प्रतियोगी 2 का दूध (LPD):",
        'competitor3_name_label': "प्रतियोगी 3 का नाम:",
        'competitor3_milk_label': "प्रतियोगी 3 का दूध (LPD):",
        'competitor4_name_label': "प्रतियोगी 4 का नाम:",
        'competitor4_milk_label': "प्रतियोगी 4 का दूध (LPD):",
        
        'photo_upload_header': "BMC/MCC तस्वीरें",
        'photo_overall_label': "फोटो 1: सम्पूर्ण ढांचा",
        'photo_platform_label': "फोटो 2: प्लेटफॉर्म/प्रवेश क्षेत्र",
        'photo_inside_label': "फोटो 3: कूलिंग क्षेत्र (अंदर)",
        'submit_button': "विजिट डेटा सबमिट करें",
        'yes': "हाँ",
        'no': "नहीं",
        'others': "अन्य",
        'options_gender': ["पुरुष", "महिला"],
        'options_education': ["10वीं पास", "12वीं पास", "ग्रेजुएशन", "पोस्ट ग्रेजुएशन", "अन्य"],
        'options_quality': ["ख़राब", "ठीक", "अच्छा", "सबसे अच्छा"],
        'options_payment_schedule': ["महीने के हर 10वें दिन", "महीने में दो बार", "महीने में एक बार", "कोई निश्चित अनुसूची नहीं"],
        'options_payment_method': ["नकद", "बैंक ट्रांसफर", "दोनों"],
        'options_awareness_poster': ["एएफएम", "एबी", "सीएमपी", "अन्य"],
        'options_health_camp': ["मासिक", "त्रैमासिक", "वार्षिक", "कोई निश्चित अनुसूची नहीं"],
        'options_data_recorded': ["मैन्युअल रूप से (Manually)", "डिजिटल रूप से (Digitally)", "दोनों (Both)"],
        'options_seasons': ["गर्मी", "मानसून", "सर्दी", "सभी"],
        'options_mbrt_facility': ["कोई नहीं (None)", "MBRT स्कैनर (MBRT Scanner)", "MBRT वाटर बाथ (MBRT Water bath)"]
    }
}

# --- Function to get translated text ---
def t(key):
    return translations[st.session_state.language].get(key, key)

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

st.set_page_config(layout="centered", page_title="Ksheersagar - BMC/MCC Visit")

# --- Language Selection ---
if 'language' not in st.session_state:
    st.session_state.language = 'en'

st.sidebar.header("Language / भाषा / भाषा")
lang_options = ["English", "Marathi", "Hindi"]

# Convert the stored 'en'/'mr'/'hi' back to selection index
if st.session_state.language == 'en':
    lang_index = 0
elif st.session_state.language == 'mr':
    lang_index = 1
else:
    lang_index = 2

selected_lang_display = st.sidebar.radio("Select Language", lang_options, index=lang_index, key="lang_radio_bmc")

# Update session state based on selection
if selected_lang_display == "English":
    st.session_state.language = 'en'
elif selected_lang_display == "Marathi":
    st.session_state.language = 'mr'
else:
    st.session_state.language = 'hi'

# --- Data Loading ---
if 'bmc_visit_data' not in st.session_state:
    st.session_state.bmc_visit_data = load_existing_data()

# --- DATA LISTS (Separated) ---

# 1. LACTALIS DATA (EXTRACTED)
LACTALIS_BMC_NAMES = sorted([
    'Modnimb', 'Malkhambi', 'Akole BDK', 'Anjangaon', 'Bhambewadi', 'Bhosare', 'Chobhe pimpari', 'Degaon', 'Ekrukhe', 'Footjalgaon', 
    'Khuneshwar', 'Mandrup', 'Masale Chaudhari', 'Pathari', 'Peertakali', 'Pimpalner', 'Shelave', 'Tulashi', 'PADALI RANJANGAON', 'Bhandgaon', 
    'Ozar', 'Belpimpalgaon', 'Kanurpathar', 'Waghwadi', 'Koregaon', 'Akolner', 'ASHWI BDK', 'Dhavlagaon', 'Ghospuri', 'Kadus', 
    'Kharatwadi', 'NimgaonJali', 'Nirmalpimpari', 'PimpariKolander', 'Samnapur', 'Yadavwadi', 'Yelpane', 'JAKHORI', 'RALEGAN THERPAL', 'NANDUR SHIKARI', 
    'Malunje', 'Gundegaon', 'SHEDGAON', 'Dharangaon', 'BELWANDI MHVTR', 'SHIRDI MHVTR', 'BHOYAE KRD MHVTR', 'MATHACHIWADI', 'BERWADI', 'CHINCHOLI', 
    'KASARI', 'MALWADI', 'Kohakadi', 'VADANGALI', 'DAPUR', 'PAREGAON', 'KHOPODI', 'KHOKAR', 'WADNER HAVELI PRVTN', 'NIMONE PRVTN', 
    'PARGAON PRVTN', 'RANJANI PRVTN', 'LONI HAWELI PRVTN', 'DAHIGAON NE PRVTN', 'Shevgaon', 'Hivargaon Ambre', 'Dhamangaon pat', 'Mandave', 'Samsherpur', 
    'Shrirampur MIDC', 'Rahuri', 'Pratappur', 'Miri', 'Mehenduri', 'Kalas'
])
LACTALIS_SUB_DISTRICTS = sorted([
    'Madha', 'Malshiras', 'Mohol', 'South Solapur', 'North Solapur', 'Pandharpur', 'Parner', 'Nagar', 'Sangamner', 'Newasa', 
    'Shrigonda', 'Shrigondra', 'Rahata', 'Nashik', 'Kopergaon', 'Shevgaon', 'Sinnar', 'Shirur', 'Yeola', 'Shrirampur', 
    'Daund', 'Akole', 'Rahuri', 'Pathardi'
])
LACTALIS_DISTRICTS = sorted(['Solapur', 'Ahilyanagar', 'Nashik', 'Pune'])
LACTALIS_VILLAGES = LACTALIS_BMC_NAMES # Use BMC names as villages

# 2. THE MCC LIST (Strictly from the Left Table in Image - Paras)
PARAS_MCC_LIST = sorted([
    "Ghodegaon", "Anatarwali", "Chedgaon", "Umbari", "Pimparne", "Madve",
    "Wadegavhan", "Shrigonda", "Mahijalgaon", "Belapur", "Sarola Advai",
    "Tandulwadi", "Nepatgaon", "Medshingi", "Khandali"
])

# 3. THE SPECIFIC PARAS BMC LIST (Strictly from the Right Table in Image)
PARAS_BMC_LIST = [
    "Khadki", "Hivre", "Palve", "Kadus", "Padalirajangaon",
    "Deodaithan", "Dhawalgaon", "Walki"
]

# 4. OTHER BMC LISTS
GOVIND_BMC_NAMES = ["VIGHNAHARTA VIDNI COOLER", "NIRAI DUDH SANKALAN KEND.PANCABIGA", "PAWAR DAIRY ASU", "AJAY DUDH", "JAY HANUMAN BMC NAIKBOMWADI", "SHREE GANESH SASTEWADI BMC", "GOVIND DUDH SANKALAN KENDRA HOL", "JITOBA BULK COOLER JINTI", "JAY MHALLAR DUDH KALAJ", "WAGHESHWARI SASWAD", "BHAIRAVNATH DUDH HINGANGAON", "GOVIND DUDH SANKALAN KENDRA SASWAD", "SHREENATH MILK SANKALAN", "RAJMUDRA DUDH WATHARPHATA BMC", "ROKDESHWAR MILK SANKALAN", "BHAIRAVNATH MANDAVKHADAK COOLER", "SAYALI, MUNJAWADI", "JAY HANUMAN BARAD", "SHIVSHANKAR DUDH BARAD", "CHANDRABHAGA MILK SANKALAN", "KARCHE SAMPAT", "DURGADEVI DUDH ZIRAPVASTI COOLER", "JANAI DUDH SANKALAN KENDRA BMC", "GOKUL DUDH MATHACHIWADI", "GOVIND MAHILA SHVETKRANTI MILK SANKALAN", "VAJUBAI MILK SANKALAN", "SHRIRAM DUDH SANKALAN & SHIT.BHUINJ", "YASHODHAN MILK & MILK PROD. PACWAD", "OM BHAKTI DUDH WAI COW", "MAYURESHWAR DAIRY", "YOGESHWARI MILK SANKALAN", "JAY BHAVANI ANBHULEWADI", "MAHALAXMI MILK", "SHREENATH MILK", "MAHALAXMI DUDH MOHI", "SANCHALIT SUDARSHAN MILK", "MAULI DUDH SANKALAN KENDR.BHALAWADI", "SUPRIYA MILK", "JAGDAMBA DUDH BHATKI", "SHRI GANESH DUDH SAK VARKUTE MASWAD", "DAHIWADI DOCK", "SHREE JAYHARI RANAND PHALTAN COOLER", "SHIVAM DUDH BUDH", "GOMATA DUDH SANKALAN KEND.CHILEWADI", "REVANSIDDHA MILK SANKALAN", "VENKATESH AGRO PROCESSING CO.", "SHIVRAJ DUDH SANKALAN KENDRA", "SHIRAM DUDH PIMPRE DHAIGUDEMALA", "VANGNA DUDH HIVRE COW MILK", "GOWARDHAN MILK COLLECTION", "SHRI DATT DOODH DAIRY ANPATWADI", "JYOTIRLING DUDH SANKALAN KENDRA BORJAIWADI", "SHREE DATT MILK DAIRY AZADPUR", "SHIVKRUPA BMC", "SANT BHAGWANBABA AKOLE", "HINDAVI DAIRY FARM KHADAKI DAUND", "SHIVTEJ DUDH PAWARWASTI BORIBEL", "JAY HANUMAN DUDH VITTHALNAGAR", "BHAIRAVNATH DEVULGOAN RAJE", "A.S.DAIRY FARM", "VENKATESH AGRO PROCESSING CO.", "AKASH DUDH SANKALAN KENDRA", "BHAIRAVNATH MILK SANKALAN", "GOVIND SADASHIVNAGAR", "GOVIND WANIMALA", "GOVIND MILK SANKALAN", "LOKRAJ MILK SANKALAN", "SHAMBHU MAHADEV PHONDSHIRAS", "VISHNU NARAYAN DUDH", "JYOTIRLING DOODH SANKALAN EKSHIV"]
SDDPL_BMC_NAMES = ["SHELKEWASTI", "HAKEWASTI", "KUSEGAON", "NYAWASTI", "NANGAON-2", "PARGAON-1", "PARGAON-2", "PIMPALGAON", "YAWAT", "CHANDANWADI", "DALIMB", "NANDUR", "DELAWADI", "KANGAON", "BETWADI", "KHADKI", "ROTI", "SONAWADI", "GOPALWADI", "HOLEWASTI", "MIRADE", "JAWALI", "VIDANI", "BARAD", "GUNWARE", "SOMANTHALI", "CHAUDHARWADI", "SANGAVI-MOHITEWASTI", "RAUTVASTI VIDANI", "PHADTARWADI", "KAPASHI", "MALEWADI", "SAKHARWADI", "RAVADI", "NIMBLAK", "ASU", "TAMKHADA", "HANUMANTWADI", "KHATAKEVASTI", "SATHEPHATA", "GANEGAONDUMALA", "VADGAON RASAI", "RANJANGAON SANDAS", "BHAMBURDE", "INAMGAON6", "NAGARGAON PHATA", "AJNUJ", "INAMGAON5", "PHARATEWADI", "KURULII", "SHINDODI", "GOLEGAON", "NAGARGAON", "NIMONE", "AMBALE 3", "KARDE", "KANHUR MESAI", "MAHADEVWADI", "NIMGAON MHALUNGI", "DHANORE", "TALEGAON DHAMDHERE", "MANDAVGAN PHARATA", "GUNAT", "KASHTI", "GHADAGEMALA", "INAMGAON3", "WANGDHARI", "URALGAONI", "JAI BHAVANI DUDH SANKLAN KENDRA PIMPRI S", "DATTAKRUPA DUDH SANKLAN KENDRA BORGAON ARJ", "SHREE SAI SAMARTH DUDH SANKALAN KENDRA", "JAY BAJRANGBALI DUDH SANKALAN KENDRA", "BHAIRAVNATH DUDH SANKALAN AND SHITKARAN KENDRA", "SWARAJ DUDH SANKALAN SHITAKENDR", "DYNAMIX DUDH SANKALAN AND SHITKARAN KENDRA", "SAMRUDDHI DUDH SANKALAN V SHITKARAN KENDRA", "DATTAKRUPA MILK DAIRY", "NARENDRA MAULI DUDH SANKALAN SHITKARAN KENDRA", "GURUDEV DUDH SANKALAN KENDRA", "VILAS NARAYAN GHORPADE", "SUNIL NAMDEORAO SAKHARE", "BHAIRAVNATHKRUPA DUDHA SANKALAN KENDRA", "YUVARAJ DUDH SANKALAN KENDRA", "SAMPADA DAIRY DUDH SANKALAN KENDRA", "GURUKRUPA DUDH SANKALAN KENDRA DAHIGAON", "NAGESHWAR DHUDH SANKALAN V SHITKARAN KENDRA", "RUCHI DAIRY", "SHREE GANESH CHILLING PLANT", "PAVANSAGAR MILK COLLECTION CENTER", "BHAIRAVNATH MILK COLLECTION AND CHILLING CENTRE", "HANGESHVAR DAIRY", "BHAIRAVNATH DUDH SANKLAN KENDRA RAYGAVHAN", "SULTANPUR CHILLING CENTRE", "SHRI DATTA DIGAMBAR SAHAKARI DUDH SANSTHA", "KRUSHIRAJ DUDH SANKALAN KENDRA", "BHAIRAVNATH DUDH DAIRY", "ANANDRAO BHIVA DHAIGUDE", "BIROBA DUDH SANKALAN V SHITKARAN KENDRA", "SHIVGANGA MILK CENTER", "SHRIKRUSHNA DAIRY", "SAI AMRUT DUDH SANKALAN KENDRA"]

# 5. FINAL LISTS
ALL_MCC_NAMES = sorted(list(set(PARAS_MCC_LIST))) 
ALL_BMC_NAMES = sorted(list(set(GOVIND_BMC_NAMES + SDDPL_BMC_NAMES + PARAS_BMC_LIST + LACTALIS_BMC_NAMES))) 

# Other Data
PARAS_DISTRICTS = sorted(["Ahilyanagar", "Solapur", "Bulandshahr", "Merath"])
PARAS_SUB_DISTRICTS = sorted([
    "Newasa", "Pathardi", "Rahuri", "Sangamner", "Parner", 
    "Shrigonda", "Karjat", "Shrirampur", "Pandharpur", 
    "Sangola", "Mohol", "Ahilyanagar"
])
PARAS_VILLAGES = sorted([
    "Ghodegaon", "Tisgaon", "Chedgaon", "Kanadagaon", "Pimparne", 
    "Mandve", "Wadegavhan", "Shrigonda", "Mulewadi", "Belapur", 
    "Sarola Advai", "Wakhari", "Nepatgaon", "Medshingi", "Roplae",
    "Khadki", "Hivre", "Palve", "Kadus", "Padalirajangaon",
    "Deodaithan", "Dhawalgaon", "Walki"
])

CATTLE_FEED_BRAND_OPTIONS = ["Royal Bypro and classic", "Govind Classic Biopro", "Govind Royle Biopro", "SDDPL Samruddhi", "SDDPL Samruddhi Plus", "SDDPL Samruddhi Gold", "SDDPL Shakti", t('others')]
EXISTING_SUB_DISTRICTS = ["PHULAMBRI", "KANNAD", "SILLOD", "AURANGABAD", "PATHARDI", "NEWASA", "AHMEDNAGAR", "PARNER", "SHRIGONDA", "KHULTABAD", "KOREGAON", "KHANDALA", "MANN", "KOPARGAON"]
SUB_DISTRICT_OPTIONS = sorted(list(set(EXISTING_SUB_DISTRICTS + PARAS_SUB_DISTRICTS + LACTALIS_SUB_DISTRICTS + [t('others')])))
EXISTING_VILLAGES = ["ALAND", "BORGAON ARJ", "MOHARA", "KAIGAON", "VIRAMGAON", "BANKINHOLA", "SHEKTA", "WADOD BAJAR", "SULTANWADI", "BABHULGAON", "LEHA", "KAUDGAON JAMB", "KARANJI", "KHANDGAON", "KAUDGAON", "CHICHONDI SHIRAL", "DAHIGAON", "BHENDA", "JAKHANGAON", "PARNER", "DEODAITHAN", "PANOLI 2", "CHIMBHALE", "RAYGAVHAN", "SULTANPUR", "RANDULLABAD", "PARGAON", "SUKHED", "KHED (BK)", "MOGARALE", "PADHEGAON", "JAVALKE"]
VILLAGE_OPTIONS = sorted(list(set(EXISTING_VILLAGES + PARAS_VILLAGES + LACTALIS_VILLAGES + [t('others')])))

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

with st.form(key='bmc_visit_form'):
    
    col_geo1, col_geo2 = st.columns(2)
    with col_geo1:
        st.text_input(t('latitude_label'), value=auto_lat, disabled=True)
    with col_geo2:
        st.text_input(t('longitude_label'), value=auto_lon, disabled=True)

    st.header(t('photo_upload_header'))
    col_photo1, col_photo2, col_photo3 = st.columns(3)
    with col_photo1:
        photo_overall = st.file_uploader(t('photo_overall_label'), type=['jpg', 'jpeg', 'png'], key="photo_overall_upload")
    with col_photo2:
        photo_platform = st.file_uploader(t('photo_platform_label'), type=['jpg', 'jpeg', 'png'], key="photo_platform_upload")
    with col_photo3:
        photo_inside = st.file_uploader(t('photo_inside_label'), type=['jpg', 'jpeg', 'png'], key="photo_inside_upload")

    st.markdown("---")
    st.header(t('general_info_header'))
    
    col_bmc_name, col_mcc_name = st.columns(2)
    with col_bmc_name:
        bmc_name_option, other_bmc_name = render_select_with_specify_permanent(st, 'bmc_name_label', ["SELECT"] + ALL_BMC_NAMES + [t('others')], 'bmc_name_select', 'other_bmc_name_label')
        actual_bmc_name = other_bmc_name if bmc_name_option == t('others') else bmc_name_option
    with col_mcc_name:
        mcc_name_option, other_mcc_name = render_select_with_specify_permanent(st, 'mcc_name_label', ["SELECT"] + ALL_MCC_NAMES + [t('others')], 'mcc_name_select', 'other_mcc_name_label')
        actual_mcc_name = other_mcc_name if mcc_name_option == t('others') else mcc_name_option

    col1, col2 = st.columns(2)
    with col1:
        bmc_code = st.text_input(t('bmc_code_label'))
        scheduled_start_date = st.date_input(t('start_date_label'), value=dt_date(2025, 5, 7))
        organization = st.selectbox(t('organization_label'), ["Govind Milk", "SDDPL", "Paras", "Lactalis"], index=0)
        activity_created_by = st.selectbox(t('activity_created_by_label'), ["Dr. Shyam", "Dr Sachin", "bhusan", "subhrat", "aniket", "ritesh"], index=0)

    with col2:
        state = st.text_input(t('state_label'), "Maharashtra", disabled=False)
        district_list = sorted(list(set(["Satara", "Pune", "Ahmednagar", "Solapur", "Aurangabad"] + PARAS_DISTRICTS + LACTALIS_DISTRICTS + [t('others')])))
        district_option, other_district_input = render_select_with_specify_permanent(st, 'district_label', district_list, 'district_select', 'other_district_label')
        actual_district = other_district_input if district_option == t('others') else district_option

        sub_district_option, other_sub_district_input = render_select_with_specify_permanent(st, 'sub_district_label', SUB_DISTRICT_OPTIONS, 'sub_district_select', 'other_sub_district_label')
        actual_sub_district = other_sub_district_input if sub_district_option == t('others') else sub_district_option
        
        collecting_village = st.number_input(t('collecting_village_label'), min_value=0, value=15)
        village_option, other_village_name = render_select_with_specify_permanent(st, 'village_label', VILLAGE_OPTIONS, 'village_select', 'other_village_label')
        actual_village = other_village_name if village_option == t('others') else village_option

    st.header(t('bcf_details_header'))
    col_farmer1, col_farmer2 = st.columns(2)
    with col_farmer1:
        bcf_name = st.text_input(t('bcf_name_label'), "Sachin Shahuraje Bhosale")
        bcf_gender = st.selectbox(t('bcf_gender_label'), t('options_gender'), index=0)
        education, other_education = render_select_with_specify_permanent(st, 'education_label', t('options_education'), 'education_select', 'other_education_label')
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

    st.header(t('capacity_header'))
    col_routes1, col_routes2 = st.columns(2)
    with col_routes1:
        total_routes = st.number_input(t('total_routes_label'), min_value=0)
        offline_vlcs = st.number_input(t('offline_vlcs_label'), min_value=0)
    with col_routes2:
        total_vlcs = st.number_input(t('total_vlcs_label'), min_value=0)
        online_vlcs = st.number_input(t('online_vlcs_label'), min_value=0)
        
    st.markdown("---")
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
    
    # --- TESTING & QUALITY SECTION ---
    st.header(t('quality_payment_header'))
    yes_no_options = [t('yes'), t('no')]
    
    afm_tested = st.radio(t('afm_tested_label'), yes_no_options, index=1, key="afm_tested_radio")
    
    col_afm1, col_afm2 = st.columns(2)
    with col_afm1:
        afm_quantity = st.text_input(t('afm_quantity_label'))
    with col_afm2:
        afm_season = st.multiselect(t('afm_season_label'), t('options_seasons'))

    st.markdown("---")
    
    mb_scanner = st.radio(t('mb_scanner_label'), yes_no_options, index=1, key="mb_scanner_radio")
    mbrt_time = st.text_input(t('mbrt_time_label'))

    # --- INFRASTRUCTURE & COMPLIANCE ---
    st.header(t('infra_compliance_header'))
    overall_infrastructure = st.selectbox(t('overall_infra_label'), t('options_quality'), index=2)
    remark_infra = st.text_area(t('remark_infra_label'), "Good infrastructure, seprate room for cattle feed")
    bmc_cleaning_hygiene = st.selectbox(t('bmc_cleaning_label'), t('options_quality'), index=2)

    col_infra1, col_infra2, col_infra3, col_infra4 = st.columns(4)
    with col_infra1:
        air_curtain = st.radio(t('air_curtain_label'), yes_no_options, index=0, key="air_curtain_bmc")
        fly_catcher = st.radio(t('fly_catcher_label'), yes_no_options, index=0, key="fly_catcher_bmc")
    with col_infra2:
        wash_basin = st.radio(t('wash_basin_label'), yes_no_options, index=0, key="wash_basin_bmc")
        opening_window_door = st.radio(t('opening_window_door_label'), yes_no_options, index=0, key="opening_window_door_bmc")
    with col_infra3:
        intact_floor = st.radio(t('intact_floor_label'), yes_no_options, index=0, key="intact_floor_bmc")
        digitize_system = st.radio(t('digitize_system_label'), yes_no_options, index=1, key="digitize_system_bmc")
        digitize_system_brand = st.radio(t('digitize_system_brand_label'), ["Indifoss", "Ekomilk"], key="digit_brand_select")

    with col_infra4:
        fssai_licence = st.radio(t('fssai_licence_label'), yes_no_options, index=0, key="fssai_licence_bmc")
        wg_scale_licence = st.radio(t('wg_scale_licence_label'), yes_no_options, index=1, key="wg_scale_licence_bmc")

    st.markdown("---")
    # NEW MBRT FACILITY DROPDOWN ADDED HERE
    mbrt_facility = st.selectbox(t('mbrt_facility_label'), t('options_mbrt_facility'), index=0)
    st.markdown("---")

    # Data Processing Questions
    data_recorded = st.radio(t('data_recorded_label'), t('options_data_recorded'), index=0, horizontal=True)
    software_used = st.text_input(t('software_used_label'))
    st.markdown("---")

    col_new_infra1, col_new_infra2, col_new_infra3, col_new_infra4 = st.columns(4)
    with col_new_infra1:
        sop_available = st.radio(t('sop_available_label'), yes_no_options, index=0, key="sop_available_bmc")
    with col_new_infra2:
        hot_water_available = st.radio(t('hot_water_available_label'), yes_no_options, index=0, key="hot_water_available_bmc")
    with col_new_infra3:
        notice_board_available = st.radio(t('notice_board_available_label'), yes_no_options, index=0, key="notice_board_available_bmc")
    with col_new_infra4:
        awareness_poster, other_awareness_poster = render_select_with_specify_permanent(st, 'awareness_poster_label', t('options_awareness_poster'), 'awareness_poster_select', 'other_awareness_poster_label', is_multi=True)

    st.header(t('payment_header'))
    col_pay1, col_pay2 = st.columns(2)
    with col_pay1:
        payment_schedule = st.radio(t('payment_schedule_label'), t('options_payment_schedule'), index=0, key="payment_schedule_bmc")
    with col_pay2:
        payment_method = st.multiselect(t('payment_method_label'), t('options_payment_method'), default=[t('options_payment_method')[0]])

    # --- FARMER SERVICES & COMPETITOR DETAILS ---
    st.header(t('farmer_competitor_header'))
    
    # Services and Trainings
    health_camp_freq = st.selectbox(t('health_camp_freq_label'), t('options_health_camp'))
    col_srv1, col_srv2, col_srv3 = st.columns(3)
    with col_srv1:
        helpdesk_setup = st.radio(t('helpdesk_label'), yes_no_options, index=1, key="helpdesk_radio")
    with col_srv2:
        mastitis_drive = st.radio(t('mastitis_drive_label'), yes_no_options, index=1, key="mastitis_radio")
    with col_srv3:
        training_conducted = st.radio(t('training_label'), yes_no_options, index=1, key="training_radio")

    st.markdown("---")

    col9, col10 = st.columns(2)
    with col9:
        animal_welfare_farm_no = st.number_input(t('animal_welfare_farm_label'), min_value=0, value=9)
        farmer_use_cattle_feed = st.number_input(t('farmer_use_cattle_feed_label'), min_value=0, value=58)
        cattle_feed_bag_sale_month = st.number_input(t('cattle_feed_bag_sale_label'), min_value=0, value=250)
        cattle_feed_brand_name, other_cattle_feed_brand_name = render_select_with_specify_permanent(st, 'cattle_feed_brand_label', CATTLE_FEED_BRAND_OPTIONS, 'cattle_feed_brand_select', 'other_cattle_feed_brand_label', is_multi=True)
        farmer_use_mineral_mixture_qty = st.number_input(t('farmer_use_mineral_mixture_label'), min_value=0, value=14)
        mineral_mixture_brand_name = st.text_input(t('mineral_mixture_brand_label'), "Govind Chileted")
        farmer_use_evm_rtu_qty = st.number_input(t('farmer_use_evm_rtu_label'), min_value=0, value=0)
        evm_rtu = st.text_input(t('evm_rtu_label'), "NA")
        biogas_installed = st.number_input(t('biogas_installed_label'), min_value=0, value=8)
        any_bank_linkage = st.text_input(t('bank_linkage_label'), "No")
        other_services_text = st.text_area(t('other_services_label'))

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
    submit_button = st.form_submit_button(label=t('submit_button'))

    if submit_button:
        yes_en, no_en = translations['en']['yes'], translations['en']['no']
        
        # Helper to convert translated Yes/No back to English for consistent CSV saving
        def to_en_yesno(val):
            return yes_en if val == t('yes') else no_en

        submitted_data = {
            "Photo 1 (Overall)": photo_overall.name if 'photo_overall' in locals() and photo_overall else "N/A",
            "Photo 2 (Platform)": photo_platform.name if 'photo_platform' in locals() and photo_platform else "N/A",
            "Photo 3 (Inside)": photo_inside.name if 'photo_inside' in locals() and photo_inside else "N/A",
            "BMC/MCC Code": bmc_code,
            "SCHEDULED START DATE": scheduled_start_date.isoformat() if scheduled_start_date else None,
            "BMC Name": actual_bmc_name, 
            "Other BMC Name": other_bmc_name,
            "MCC Name": actual_mcc_name, 
            "Other MCC Name": other_mcc_name,
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
            "Latitude": auto_lat,
            "Longitude": auto_lon,
            
            "BCF/In-charge Name": bcf_name,
            "Gender": translations['en']['options_gender'][t('options_gender').index(bcf_gender)],
            "Education": actual_education,
            "Other Education": other_education,
            "Mobile Number": bcf_mobile_number,
            "Operating Staff (No.)": operating_staff_no,
            "Distance From HO (KM)": distance_from_ho_km,
            
            "Total Registered Farmer (No.)": total_registered_farmer_no,
            "No. of Women Farmers (Total Registered)": total_women_farmer_no, 
            "No. of Men Farmers (Total Registered)": total_men_farmer_no, 
            "Active Farmer (No.)": active_farmer_no,
            "No. of Women Farmers (Active Farmers)": active_women_farmer_no, 
            "No. of Men Farmers (Active Farmers)": active_men_farmer_no, 
            
            "Total No. of Routes": total_routes,
            "Total No. of VLCs": total_vlcs,
            "Offline VLCs": offline_vlcs,
            "Online VLCs": online_vlcs,
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
            
            "AFM Tested": to_en_yesno(afm_tested),
            "AFM Quantity": afm_quantity,
            "AFM Positive Season": ', '.join(afm_season) if afm_season else "N/A",
            "MB Scanner Available": to_en_yesno(mb_scanner),
            "Avg MBRT Testing Time": mbrt_time,
            
            "Overall Infrastructure": overall_infrastructure,
            "Remark (Infrastructure)": remark_infra,
            "BMC/MCC Cleaning & Hygiene": bmc_cleaning_hygiene,
            "Air curtain": to_en_yesno(air_curtain),
            "Fly Catcher": to_en_yesno(fly_catcher),
            "Wash Basin": to_en_yesno(wash_basin),
            "Opening(Window/Door)": to_en_yesno(opening_window_door),
            "Intact Floor in Premise": to_en_yesno(intact_floor),
            "Digitize System": to_en_yesno(digitize_system),
            "Digitize System Brand": digitize_system_brand,
            
            "MBRT Testing Facility": mbrt_facility,
            
            "Data Recorded Method": data_recorded,
            "Software Used": software_used,
            
            "FSSAI Licence": to_en_yesno(fssai_licence),
            "Wg Scale Licence": to_en_yesno(wg_scale_licence),
            "Is SOP Available": to_en_yesno(sop_available),
            "Is Hot Water Available": to_en_yesno(hot_water_available),
            "Is Notice Board Available": to_en_yesno(notice_board_available),
            "Awareness Poster": ', '.join(awareness_poster),
            "Other Awareness Poster": other_awareness_poster,
            
            "Payment Schedule": payment_schedule,
            "Payment Method": ', '.join(payment_method),
            
            "Frequency of Health Camps": health_camp_freq,
            "Helpdesk Setup": to_en_yesno(helpdesk_setup),
            "Mastitis Preventive Drive": to_en_yesno(mastitis_drive),
            "Regular Training Conducted": to_en_yesno(training_conducted),

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
            "Other Services": other_services_text,
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
        st.success("Visit data submitted and saved!")

st.header("Real-time View & Download")
if st.session_state.bmc_visit_data:
    st.subheader("All Submitted Visit Entries:")
    df_bmc_visit_all = pd.DataFrame(st.session_state.bmc_visit_data).astype(str)
    st.dataframe(df_bmc_visit_all, use_container_width=True)
    csv_bmc_visit_all = df_bmc_visit_all.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download All Data as CSV", data=csv_bmc_visit_all, file_name="all_visit_data.csv", mime="text/csv")
else:
    st.info("No Visit data submitted yet.")
