import streamlit as st
import pandas as pd
from datetime import date as dt_date
import os
import random

# --- Constants ---
FARM_VISIT_DATA_FILE = "farm_visit_data.csv"

# --- Translation Dictionary (Kept exactly as is) ---
translations = {
    'en': {
        'page_title': "🐄 Ksheersagar - Farm Visit Data Entry",
        'page_header': "Please fill out the details for the farm visit below.",
        'language_select': "Select Language",
        'general_info_header': "General Farm Visit Information",
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
        'sub_district_label': "Sub District:",
        'collecting_village_label': "Collecting Village:",
        'bmc_label': "BMC:",
        'other_bmc_label': "Other BMC Name (Specify):",
        'herd_details_header': "Milk Production & Herd Details",
        'milk_production_label': "Milk Production At Farm:",
        'herd_size_label': "Herd Size:",
        'desi_no_label': "No Of Desi:",
        'cross_breed_no_label': "No Of Cross Breed:",
        'cattle_in_milk_no_label': "No Of Cattle In Milk:",
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
        'cmt_testing_freq_label': "Frequency Of CMT Testing (No Of Days):",
        'cleaning_freq_label': "Frequency Of Cleaning Of Milking Machines (No Of Days):",
        'milk_container_type_label': "Type Of Milk Container:",
        'milk_kept_duration_label': "Duration Of Milk Kept At Farm Post Milking (minutes):",
        'recent_outbreak_label': "Any Recent Outbreak Of Contamination/Disease:",
        'overall_hygiene_label': "Overall Hygiene Of The Farm:",
        'space_sick_animal_label': "Space For Sick Animal Segregation:", # Corrected Key
        'recent_disease_label': "Recent Disease Reported:",
        'last_disease_date_label': "Last Date Of Reporting Of Disease:",
        'cattle_affected_no_label': "No Of Cattle Affected:",
        'vet_treatment_label': "Most Recent Veterinary Treatment Given:",
        'last_vet_treatment_date_label': "Date Of Last Veterinary Treatment:",
        'moldy_feed_presence_label': "Presence Of Moldy Or Contaminated Feed:",
        'submit_button': "Submit Farm Visit Data",
        'yes': "YES",
        'no': "NO",
        'options_hygiene': ["POOR", "MODERATE", "GOOD", "BEST"],
        'options_cleaning_freq': ["DAILY", "WEEKLY", "FORTNIGHT", "TWICE IN A WEEK"]
    },
    'mr': {
        'page_title': "🐄 क्षीरसागर - फार्म भेट डेटा एंट्री",
        'page_header': "कृपया खालील फार्म भेटीसाठी तपशील भरा.",
        'language_select': "भाषा निवडा",
        'general_info_header': "सर्वसाधारण फार्म भेट माहिती",
        'date_label': "तारीख:",
        'farmer_name_label': "शेतकऱ्याचे नाव:",
        'farmer_id_label': "शेतकरी आयडी:",
        'activity_name_label': "ऍक्टिव्हिटीचे नाव:",
        'activity_created_by_label': "ऍक्टिव्हिटी कोणी तयार केली:",
        'type_of_farm_label': "शेतीचा प्रकार:",
        'farm_area_label': "शेतीचे क्षेत्र (एकर/हेक्टर):",
        'location_header': "स्थान आणि संस्था तपशील",
        'organization_label': "संस्था:",
        'state_label': "राज्य:",
        'district_label': "जिल्हा:",
        'sub_district_label': "उप-जिल्हा:",
        'collecting_village_label': "संकलन गाव:",
        'bmc_label': "BMC:",
        'other_bmc_label': "इतर BMC नाव (नमूद करा):",
        'herd_details_header': "दूध उत्पादन आणि कळप तपशील",
        'milk_production_label': "शेतातील दूध उत्पादन:",
        'herd_size_label': "कळपाचा आकार:",
        'desi_no_label': "देशी जनावरांची संख्या:",
        'cross_breed_no_label': "संकरित जनावरांची संख्या:",
        'cattle_in_milk_no_label': "दुधाळ जनावरांची संख्या:",
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
        'mineral_mixture_option_label': " खनिज मिश्रण (असल्याs, ब्रँडचे नाव):",
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
        'cmt_testing_freq_label': "CMT चाचणीची वारंवारता (दिवसांची संख्या):",
        'cleaning_freq_label': "दूध काढणी यंत्रांच्या स्वच्छतेची वारंwarता (दिवसांची संख्या):",
        'milk_container_type_label': "दुधाच्या भांड्याचा प्रकार:",
        'milk_kept_duration_label': "दूध काढल्यानंतर फार्मवर किती वेळ ठेवले जाते (मिनिटे):",
        'recent_outbreak_label': " अलीकडे कोणताही प्रादुर्भाव/रोगराई:",
        'overall_hygiene_label': "शेताची एकूण स्वच्छता:",
        'space_sick_animal_label': " आजारी जनावरांसाठी वेगळी जागा:", # Corrected Key
        'recent_disease_label': "अलीकडील नोंदवलेला आजार:",
        'last_disease_date_label': "आजार नोंदवण्याची शेवटची तारीख:",
        'cattle_affected_no_label': "बाधित जनावरांची संख्या:",
        'vet_treatment_label': "सर्वात अलीकडील पशुवैद्यकीय उपचार:",
        'last_vet_treatment_date_label': "शेवटच्या पशुवैdyakiy उपचाराची तारीख:",
        'moldy_feed_presence_label': "बुरशीजन्य किंवा दूषित चाऱ्याची उपस्थिती:",
        'submit_button': "फार्म भेट डेटा सबमिट करा",
        'yes': "होय",
        'no': "नाही",
        'options_hygiene': ["खराब", "मध्यम", "चांगली", "उत्तम"],
        'options_cleaning_freq': ["दररोज", "आठवड्यातून", "पंधरवड्यातून", "आठवड्यातून दोनदा"]
    }
}

# --- Function to get translated text ---
def t(key):
    # This function is the source of the KeyError, ensured the caller uses the correct key
    return translations[st.session_state.language][key]

st.set_page_config(layout="centered", page_title="Ksheersagar - Data Entry")

# --- Language Selection ---
if 'language' not in st.session_state:
    st.session_state.language = 'en' # Default to English

# Place language selector in the sidebar
st.sidebar.header(translations['en']['language_select'] + " / " + translations['mr']['language_select'])
lang_options = ["English", "Marathi"]
# Check if the session state language is capitalized or not and find index safely
current_lang_capitalized = st.session_state.language.capitalize() if st.session_state.language else 'English'
if current_lang_capitalized not in lang_options:
    current_lang_capitalized = "English" # Fallback
lang_index = lang_options.index(current_lang_capitalized)

selected_lang_display = st.sidebar.radio("Language", lang_options, index=lang_index)


# Update session state language based on selection
if selected_lang_display == "English":
    st.session_state.language = 'en'
else:
    st.session_state.language = 'mr'

# --- Session State Initialization and Data Loading ---
if 'farm_visit_data' not in st.session_state:
    st.session_state.farm_visit_data = []
    if os.path.exists(FARM_VISIT_DATA_FILE):
        try:
            df_existing = pd.read_csv(FARM_VISIT_DATA_FILE)
            st.session_state.farm_visit_data.extend(df_existing.to_dict('records'))
        except Exception as e:
            st.error(f"Error loading existing data: {e}")
            st.session_state.farm_visit_data = []

# --------------------------------------------------

st.title(t('page_title'))
st.write(t('page_header'))

# Define BMC names (kept in English for data consistency)
GOVIND_BMC_NAMES = [
    "VIGHNAHARTA VIDNI COOLER", "NIRAI DUDH SANKALAN KEND.PANCABIGA", "PAWAR DAIRY ASU",
    "AJAY DUDH", "JAY HANUMAN BMC NAIKBOMWADI", "SHREE GANESH SASTEWADI BMC",
    "GOVIND DUDH SANKALAN KENDRA HOL", "JITOBA BULK COOLER JINTI", "JAY MHALLAR DUDH KALAJ",
    "WAGHESHWARI SASWAD", "BHAIRAVNATH DUDH HINGANGAON", "GOVIND DUDH SANKALAN KENDRA SASWAD",
    "SHREENATH MILK SANKALAN", "RAJMUDRA DUDH WATHARPHATA BMC", "ROKDESHWAR MILK SANKALAN",
    "BHAIRAVNATH MANDAVKHADAK COOLER", "SAYALI, MUNJAWADI", "JAY HANUMAN BARAD",
    "SHIVSHANKAR DUDH BARAD", "CHANDRABHAGA MILK SANKALAN", "KARCHE SAMPAT",
    "DURGADEVI DUDH ZIRAPVASTI COOLER", "JANAI DUDH SANKALAN KENDRA BMC",
    "GOKUL DUDH MATHACHIWADI", "GOVIND MAHILA SHVETKRANTI MILK SANKALAN",
    "VAJUBAI MILK SANKALAN", "SHRIRAM DUDH SANKALAN & SHIT.BHUINJ",
    "YASHODHAN MILK & MILK PROD. PACWAD", "OM BHAKTI DUDH WAI COW", "MAYURESHWAR DAIRY",
    "YOGESHWARI MILK SANKALAN", "JAY BHAVANI ANBHULEWADI", "MAHALAXMI MILK",
    "SHREENATH MILK", "MAHALAXMI DUDH MOHI", "SANCHALIT SUDARSHAN MILK",
    "MAULI DUDH SANKALAN KENDR.BHALAWADI", "SUPRIYA MILK", "JAGDAMBA DUDH BHATKI",
    "SHRI GANESH DUDH SAK VARKUTE MASWAD", "DAHIWADI DOCK", "SHREE JAYHARI RANAND PHALTAN COOLER",
    "SHIVAM DUDH BUDH", "GOMATA DUDH SANKALAN KEND.CHILEWADI", "REVANSIDDHA MILK SANKALAN",
    "VENKATESH AGRO PROCESSING CO.", "SHIVRAJ DUDH SANKALAN KENDRA",
    "SHIRAM DUDH PIMPRE DHAIGUDEMALA", "VANGNA DUDH HIVRE COW MILK",
    "GOWARDHAN MILK COLLECTION", "SHRI DATT DOODH DAIRY ANPATWADI",
    "JYOTIRLING DUDH SANKALAN KENDRA BORJAIWADI", "SHREE DATT MILK DAIRY AZADPUR",
    "SHIVKRUPA BMC", "SANT BHAGWANBABA AKOLE", "HINDAVI DAIRY FARM KHADAKI DAUND",
    "SHIVTEJ DUDH PAWARWASTI BORIBEL", "JAY HANUMAN DUDH VITTHALNAGAR",
    "BHAIRAVNATH DEVULGOAN RAJE", "A.S.DAIRY FARM", "VENKATESH AGRO PROCESSING CO.",
    "AKASH DUDH SANKALAN KENDRA", "BHAIRAVNATH MILK SANKALAN", "GOVIND SADASHIVNAGAR",
    "GOVIND WANIMALA", "GOVIND MILK SANKALAN", "LOKRAJ MILK SANKALAN",
    "SHAMBHU MAHADEV PHONDSHIRAS", "VISHNU NARAYAN DUDH", "JYOTIRLING DOODH SANKALAN EKSHIV"
]

SDDPL_BMC_NAMES = [
    "SHELKEWASTI", "HAKEWASTI", "KUSEGAON", "NYAWASTI", "NANGAON-2", "PARGAON-1",
    "PARGAON-2", "PIMPALGAON", "YAWAT", "CHANDANWADI", "DALIMB", "NANDUR",
    "DELAWADI", "KANGAON", "BETWADI", "KHADKI", "ROTI", "SONAWADI",
    "GOPALWADI", "HOLEWASTI", "MIRADE", "JAWALI", "VIDANI", "BARAD",
    "GUNWARE", "SOMANTHALI", "CHAUDHARWADI", "SANGAVI-MOHITEWASTI",
    "RAUTVASTI VIDANI", "PHADTARWADI", "KAPASHI", "MALEWADI", "SAKHARWADI",
    "RAVADI", "NIMBLAK", "ASU", "TAMKHADA", "HANUMANTWADI", "KHATAKEVASTI",
    "SATHEPHATA", "GANEGAONDUMALA", "VADGAON RASAI", "RANJANGAON SANDAS",
    "BHAMBURDE", "INAMGAON6", "NAGARGAON PHATA", "AJNUJ", "INAMGAON5",
    "PHARATEWADI", "KURULII", "SHINDODI", "GOLEGAON", "NAGARGAON", "NIMONE",
    "AMBALE 3", "KARDE", "KANHUR MESAI", "MAHADEVWADI", "NIMGAON MHALUNGI",
    "DHANORE", "TALEGAON DHAMDHERE", "MANDAVGAN PHARATA", "GUNAT", "KASHTI",
    "GHADAGEMALA", "INAMGAON3", "WANGDHARI", "URALGAONI"
]

# Define options for dropdowns (kept in English for data consistency)
SUB_DISTRICT_OPTIONS = ["Phaltan", "malshiras", "Baramati", "Indapur", "Daund", "Purander", "Pachgani", "Man", "Khatav", "Koregaon", "Khandala", "Shirur"]
DISTRICT_OPTIONS = ["Satara", "Pune", "Ahmednagar", "Solapur"]
CONCENTRATED_FEED_OPTIONS = [
    "1. Govind Classic Biopro", "2. Govind Royle Biopro", "3. SDDPL Samruddhi",
    "4. SDDPL Samruddhi Plus", "5. SDDPL Samruddhi Gold", "6. SDDPL Shakti", "Others"
]
GREEN_FODDER_OPTIONS = [
    "Sugarcane tops", "Silage", "Napier", "Maize", "Jawar",
    "super Napier", "Sugarcane", "Sugargraze", "Lucerne",
    "berseem", "Methigrass", "others"
]

# Use a form container for better organization and submission handling
with st.form(key='farm_visit_form'):
    st.header(t('general_info_header'))
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input(t('date_label'), value=dt_date(2025, 5, 7))
        farmer_name = st.text_input(t('farmer_name_label'), "Sarika Pawar")
        farmer_id = st.text_input(t('farmer_id_label'), "123-02-BB-00768", help="Format: 123-02-BB-00768")
    with col2:
        activity_name = st.text_input(t('activity_name_label'), "TNS- Farm Activity")
        activity_created_by = st.selectbox(
            t('activity_created_by_label'),
            ["Dr Sachin", "bhusan", "nilesh", "subhrat", "aniket", "ritesh"], index=0
        )
        type_of_farm = st.text_input(t('type_of_farm_label'), "Conventional")
        farm_area = st.number_input(t('farm_area_label'), min_value=0.0, value=1.52, step=0.01)

    st.header(t('location_header'))
    col3, col4 = st.columns(2)
    with col3:
        organization = st.selectbox(
            t('organization_label'),
            ["Govind", "SDDPL", "Schreiber Dynamix"], index=0
        )
        state = st.text_input(t('state_label'), "Maharashtra", disabled=True)
        district = st.selectbox(t('district_label'), DISTRICT_OPTIONS, index=0)
    with col4:
        sub_district = st.selectbox(t('sub_district_label'), SUB_DISTRICT_OPTIONS, index=0)
        collecting_village = st.text_input(t('collecting_village_label'), "SAKHARWADi")
        
        bmc_options = []
        if organization == "Govind":
            bmc_options = ["SELECT"] + GOVIND_BMC_NAMES + ["OTHERS"]
        elif organization == "SDDPL":
            bmc_options = ["SELECT"] + SDDPL_BMC_NAMES + ["OTHERS"]
        else:
            bmc_options = ["SELECT", "OTHERS"]
        bmc_selected = st.selectbox(t('bmc_label'), bmc_options, index=0, key="bmc_fv")

        other_bmc_name_fv = None
        if bmc_selected == "OTHERS":
            other_bmc_name_fv = st.text_input(t('other_bmc_label'), "", key="other_bmc_name_fv_input")

    st.header(t('herd_details_header'))
    col5, col6 = st.columns(2)
    with col5:
        milk_production = st.number_input(t('milk_production_label'), min_value=0, value=95)
        herd_size = st.number_input(t('herd_size_label'), min_value=0, value=16)
        no_of_desi = st.number_input(t('desi_no_label'), min_value=0, value=0)
        no_of_cross_breed = st.number_input(t('cross_breed_no_label'), min_value=0, value=16)
        no_of_cattle_in_milk = st.number_input(t('cattle_in_milk_no_label'), min_value=0, value=8)
    with col6:
        shed = st.radio(t('shed_label'), [t('yes'), t('no')], index=0, key="shed_fv")
        loose_housing = st.radio(t('loose_housing_label'), [t('yes'), t('no')], index=0, key="loose_housing_fv")
        ad_hoc_water_availability = st.radio(t('water_availability_label'), [t('yes'), t('no')], index=0, key="ad_hoc_water_fv")
        floor_mats = st.radio(t('floor_mats_label'), [t('yes'), t('no')], index=0, key="floor_mats_fv")

    st.header(t('feed_fodder_header'))
    concentrated_feed_option = st.selectbox(
        t('concentrated_feed_option_label'),
        [t('yes'), t('no')], index=0, key="concentrated_feed_option_fv"
    )
    
    name_of_concentrated_feed = []
    other_concentrated_feed_text = None
    if concentrated_feed_option == t('yes'):
        selected_concentrated_feeds = st.multiselect(
            t('name_of_concentrated_feed_label'),
            CONCENTRATED_FEED_OPTIONS,
            default=["4. SDDPL Samruddhi Plus"], key="name_of_concentrated_feed_fv"
        )
        if "Others" in selected_concentrated_feeds:
            other_concentrated_feed_text = st.text_input(t('specify_other_concentrated_feed'), "")
        name_of_concentrated_feed = selected_concentrated_feeds

    feed_supplements = st.selectbox(t('feed_supplements_label'), [t('no'), t('yes')], index=0, key="feed_supplements_fv")
    dry_fodder_name = st.text_input(t('dry_fodder_name_label'), "Not Available")
    
    green_fodder_name = []
    other_green_fodder_text = None
    selected_green_fodders = st.multiselect(
        t('green_fodder_name_label'),
        GREEN_FODDER_OPTIONS,
        default=["Sugarcane tops"], key="green_fodder_name_fv"
    )
    if "others" in selected_green_fodders:
        other_green_fodder_text = st.text_input(t('specify_other_green_fodder'), "")
    green_fodder_name = selected_green_fodders

    silage = st.radio(t('silage_label'), [t('yes'), t('no')], index=0, key="silage_fv")
    mineral_mixture_option = st.radio(t('mineral_mixture_option_label'), [t('no'), t('yes')], index=0, key="mineral_mixture_option_fv")
    
    name_of_mineral_mixture = None
    if mineral_mixture_option == t('yes'):
        name_of_mineral_mixture = st.text_input(t('name_of_mineral_mixture_label'), "")

    toxin_binder = st.radio(t('toxin_binder_label'), [t('yes'), t('no')], index=0, key="toxin_binder_fv")
    cmt_kit = st.radio(t('cmt_kit_label'), [t('no'), t('yes')], index=0, key="cmt_kit_fv")
    dip_cup = st.radio(t('dip_cup_label'), [t('no'), t('yes')], index=0, key="dip_cup_fv")
    separate_space_manure = st.radio(t('manure_pit_label'), [t('yes'), t('no')], index=0, key="separate_space_manure_fv")
    provision_drainage_waste = st.radio(t('drainage_waste_label'), [t('yes'), t('no')], index=0, key="provision_drainage_waste_fv")
    biogas_installation = st.radio(t('biogas_label'), [t('no'), t('yes')], index=0, key="biogas_installation_fv")
    surplus_milk_bmc = st.radio(t('surplus_milk_label'), [t('yes'), t('no')], index=0, key="surplus_milk_bmc_fv")
    photo_1 = st.file_uploader(t('photo_1_label'), type=["jpg", "jpeg", "png"])

    st.header(t('other_details_header'))
    source_of_water = st.text_input(t('source_of_water_label'), "Bore well")
    freq_cmt_testing = st.number_input(t('cmt_testing_freq_label'), min_value=0, value=0)
    freq_cleaning_milking_machines = st.selectbox(
        t('cleaning_freq_label'),
        t('options_cleaning_freq'), index=0, key="freq_cleaning_milking_machines_fv"
    )
    type_milk_container = st.text_input(t('milk_container_type_label'), "PLASTIC")
    duration_milk_kept = st.number_input(t('milk_kept_duration_label'), min_value=0, value=15)
    recent_outbreak = st.text_input(t('recent_outbreak_label'), "No recent contamination")
    overall_hygiene = st.selectbox(
        t('overall_hygiene_label'),
        t('options_hygiene'), index=2, key="overall_hygiene_fv"
    )
    
    space_sick_animal = st.radio(t('space_sick_animal_label'), [t('yes'), t('no')], index=0, key="space_sick_animal_fv")
    recent_disease_reported = st.text_input(t('recent_disease_label'), "No")
    last_date_reporting_disease = st.date_input(t('last_disease_date_label'), value=None)
    no_of_cattle_affected = st.number_input(t('cattle_affected_no_label'), min_value=0, value=0)
    most_recent_vet_treatment_given = st.text_input(t('vet_treatment_label'), "Artificial Insemination")
    date_last_vet_treatment = st.date_input(t('last_vet_treatment_date_label'), value=dt_date(2025, 4, 22))
    presence_moldy_contaminated_feed = st.radio(t('moldy_feed_presence_label'), [t('no'), t('yes')], index=0, key="presence_moldy_contaminated_feed_fv")

    st.markdown("---")
    # This is the single, correctly placed submit button for the form
    submit_button = st.form_submit_button(label=t('submit_button'))

    if submit_button:
        # Convert translated 'yes'/'no' back to English for consistent data storage
        yes_str_en, no_str_en = translations['en']['yes'], translations['en']['no']
        
        submitted_data = {
            "Date": date.isoformat() if date else None,
            "Activity Type": "FARM Visit",
            "Farmer Name": farmer_name,
            "Farmer ID": farmer_id,
            "Activity Name": activity_name,
            "Activity Created By": activity_created_by,
            "Type Of Farm": type_of_farm,
            "Farm Area (acres/hectare)": farm_area,
            "Organization": organization,
            "State": state,
            "District": district,
            "Sub District": sub_district,
            "Collecting Village": collecting_village,
            "BMC": bmc_selected,
            "Other BMC Name (Farm Visit)": other_bmc_name_fv,
            "Milk Production At Farm": milk_production,
            "Herd Size": herd_size,
            "No Of Desi": no_of_desi,
            "No Of Cross Breed": no_of_cross_breed,
            "No Of Cattle In Milk": no_of_cattle_in_milk,
            "Shed (Provision For Minimum 5 Animals)": yes_str_en if shed == t('yes') else no_str_en,
            "Loose Housing": yes_str_en if loose_housing == t('yes') else no_str_en,
            "Ad-hoc Water Availability": yes_str_en if ad_hoc_water_availability == t('yes') else no_str_en,
            "Floor Mats": yes_str_en if floor_mats == t('yes') else no_str_en,
            "Concentrated Feed (If Yes, brand Name Available)": yes_str_en if concentrated_feed_option == t('yes') else no_str_en,
            "Name Of Concentrated Feed": ", ".join(name_of_concentrated_feed) if name_of_concentrated_feed else "",
            "Other Concentrated Feed (Specify)": other_concentrated_feed_text,
            "Feed Supplements (Mention Names)": yes_str_en if feed_supplements == t('yes') else no_str_en,
            "Dry Fodder Name": dry_fodder_name,
            "Green Fodder Name": ", ".join(green_fodder_name) if green_fodder_name else "",
            "Other Green Fodder (Specify)": other_green_fodder_text,
            "Silage": yes_str_en if silage == t('yes') else no_str_en,
            "Mineral Mixture (If Yes, Brand Name)": yes_str_en if mineral_mixture_option == t('yes') else no_str_en,
            "Name Of Mineral Mixture": name_of_mineral_mixture,
            "Toxin Binder": yes_str_en if toxin_binder == t('yes') else no_str_en,
            "CMT Kit": yes_str_en if cmt_kit == t('yes') else no_str_en,
            "Dip Cup With Solution": yes_str_en if dip_cup == t('yes') else no_str_en,
            "Separate Space For Dumping Pit For Manure Waste": yes_str_en if separate_space_manure == t('yes') else no_str_en,
            "Provision For Drainage And Waste": yes_str_en if provision_drainage_waste == t('yes') else no_str_en,
            "Biogas Installation": yes_str_en if biogas_installation == t('yes') else no_str_en,
            "100% Surplus Milk Poured To BMC": yes_str_en if surplus_milk_bmc == t('yes') else no_str_en,
            "Photo 1": photo_1.name if photo_1 else "No file uploaded",
            "Source Of Water": source_of_water,
            "Frequency Of CMT Testing (No Of Days)": freq_cmt_testing,
            "Frequency Of Cleaning Of Milking Machines (No Of Days)": freq_cleaning_milking_machines,
            "Type Of Milk Container": type_milk_container,
            "Duration Of Milk Kept At Farm Post Milking (minutes)": duration_milk_kept,
            "Any Recent Outbreak Of Contamination/Disease": recent_outbreak,
            "Overall Hygiene Of The Farm": overall_hygiene,
            "Space For Sick Animal Segregation": yes_str_en if space_sick_animal == t('yes') else no_str_en,
            "Recent Disease Reported": recent_disease_reported,
            "Last Date Of Reporting Of Disease": last_date_reporting_disease.isoformat() if last_date_reporting_disease else None,
            "No Of Cattle Affected": no_of_cattle_affected,
            "Most Recent Veterinary Treatment Given": most_recent_vet_treatment_given,
            "Date Of Last Veterinary Treatment": date_last_vet_treatment.isoformat() if date_last_vet_treatment else None,
            "Presence Of Moldy Or Contaminated Feed": yes_str_en if presence_moldy_contaminated_feed == t('yes') else no_str_en
        }
        
        st.session_state.farm_visit_data.append(submitted_data)
        
        df_new_entry = pd.DataFrame([submitted_data])
        # Save to CSV (Corrected implementation logic)
        header = not os.path.exists(FARM_VISIT_DATA_FILE)
        df_new_entry.to_csv(FARM_VISIT_DATA_FILE, mode='a', index=False, header=header)
        st.success("Farm Visit data submitted and saved!")

# --- Real-time View and Download Option (Restored: No Login Required) ---
st.header("Real-time View & Download")
if st.session_state.farm_visit_data:
    st.subheader("All Submitted Farm Visit Entries:")
    df_all_farm_visit = pd.DataFrame(st.session_state.farm_visit_data)
    df_all_farm_visit = df_all_farm_visit.astype(str)
    st.dataframe(df_all_farm_visit, use_container_width=True)
    csv_all_farm_visit = df_all_farm_visit.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download All Farm Visit Data as CSV",
        data=csv_all_farm_visit,
        file_name="all_farm_visit_data.csv",
        mime="text/csv"
    )
else:
    st.info("No Farm Visit data has been submitted yet.")
