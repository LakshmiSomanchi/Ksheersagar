# pages/1_Farm_Visit.py
import streamlit as st
import pandas as pd
from datetime import date as dt_date # Import date for setting default today's date

st.set_page_config(layout="centered", page_title="Ksheersagar - Farm Visit Data Entry")

# --- Session State Initialization for this page ---
# This ensures 'farm_visit_data' exists even if this page is run directly or first
if 'farm_visit_data' not in st.session_state:
    st.session_state.farm_visit_data = []
# --------------------------------------------------

st.title("🐄 Ksheersagar - Farm Visit Data Entry")
st.write("Please fill out the details for the farm visit below.")

# Define BMC names for Govind and SDDPL (re-using these for consistency)
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


# Use a form container for better organization and submission handling
with st.form(key='farm_visit_form'):

    st.header("General Farm Visit Information")

    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date:", value=dt_date(2025, 5, 7)) # Using 2025-05-07 as per example
        activity_type = st.text_input("Activity Type:", "FARM Visit")
        farmer_name = st.text_input("Farmer Name:", "Sarika Pawar")
        farmer_id = st.text_input("Farmer ID:", "123-02-BB-00768", help="Format: 123-02-BB-00768")

    with col2:
        activity_name = st.text_input("Activity Name:", "TNS- Farm Activity")
        activity_created_by = st.selectbox(
            "Activity Created By:",
            ["Dr Sachin", "bhusan", "nilesh", "subhrat", "aniket", "ritesh"],
            index=0 # Default to Dr Sachin
        )
        type_of_farm = st.text_input("Type Of Farm:", "Conventional")
        farm_area = st.number_input("Farm Area (acres/hectare):", min_value=0.0, value=1.52, step=0.01)


    st.header("Location & Organization Details")

    col3, col4 = st.columns(2)
    with col3:
        organization = st.selectbox(
            "Organization:",
            ["Govind", "SDDPL", "Schreiber Dynamix"], # Reordered for better flow with BMC dropdown
            index=0 # Default to Govind
        )
        state = st.text_input("State:", "Maharashtra")
        district = st.text_input("District:", "Satara")
    with col4:
        sub_district = st.text_input("Sub District:", "Phaltan")
        collecting_village = st.text_input("Collecting Village:", "SAKHARWADi")
        
        # Determine BMC name options based on selected organization
        bmc_options = []
        if organization == "Govind":
            bmc_options = ["SELECT"] + GOVIND_BMC_NAMES + ["OTHERS"]
        elif organization == "SDDPL":
            bmc_options = ["SELECT"] + SDDPL_BMC_NAMES + ["OTHERS"]
        else: # For "Schreiber Dynamix" or any other case, provide "OTHERS" or a generic option
            bmc_options = ["SELECT", "OTHERS"]

        bmc_selected = st.selectbox(
            "BMC:",
            bmc_options,
            index=0,
            key="bmc_fv"
        )
        # Conditional text input for "OTHERS" BMC
        other_bmc_name_fv = None
        if bmc_selected == "OTHERS":
            other_bmc_name_fv = st.text_input("Other BMC Name (Specify):", "", key="other_bmc_name_fv_input")


    st.header("Milk Production & Herd Details")
    col5, col6 = st.columns(2)
    with col5:
        milk_production = st.number_input("Milk Production At Farm:", min_value=0, value=95)
        herd_size = st.number_input("Herd Size:", min_value=0, value=16)
        no_of_desi = st.number_input("No Of Desi:", min_value=0, value=0)
        no_of_cross_breed = st.number_input("No Of Cross Breed:", min_value=0, value=16)
        no_of_cattle_in_milk = st.number_input("No Of Cattle In Milk:", min_value=0, value=8)

    with col6:
        shed = st.radio("Shed (Provision For Minimum 5 Animals):", ["YES", "NO"], index=0, key="shed_fv")
        loose_housing = st.radio("Loose Housing:", ["YES", "NO"], index=0, key="loose_housing_fv")
        ad_hoc_water_availability = st.radio("Ad-hoc Water Availability:", ["YES", "NO"], index=0, key="ad_hoc_water_fv")
        floor_mats = st.radio("Floor Mats:", ["YES", "NO"], index=0, key="floor_mats_fv")


    st.header("Feed & Fodder Management")

    concentrated_feed_option = st.selectbox(
        "Concentrated Feed (If Yes, brand Name Available):",
        ["YES", "NO"],
        index=0, # Default to YES
        key="concentrated_feed_option_fv"
    )

    name_of_concentrated_feed = None
    if concentrated_feed_option == "YES":
        name_of_concentrated_feed = st.selectbox(
            "Name Of Concentrated Feed:",
            [
                "1. Govind Classic Biopro",
                "2. Govind Royle Biopro",
                "3. SDDPL Samruddhi",
                "4. SDDPL Samruddhi Plus",
                "5. SDDPL Samruddhi Gold",
                "6. SDDPL Shakti",
                "7. Others"
            ],
            index=3, # Default to SDDPL Samruddhi Plus
            key="name_of_concentrated_feed_fv"
        )

    feed_supplements = st.selectbox("Feed Supplements (Mention Names):", ["No", "Yes"], index=0, key="feed_supplements_fv")
    dry_fodder_name = st.text_input("Dry Fodder Name:", "Not Available")

    green_fodder_name = st.selectbox(
        "Green Fodder Name:",
        [
            "Sugarcane tops", "Silage", "Napier", "Maize", "Jawar",
            "super Napier", "Sugarcane", "Sugargraze", "Lucerne",
            "berseem", "Methigrass", "others (specify)"
        ],
        index=0, # Default to Sugarcane tops
        key="green_fodder_name_fv"
    )

    silage = st.radio("Silage:", ["YES", "NO"], index=0, key="silage_fv")

    mineral_mixture_option = st.radio("Mineral Mixture (If Yes, Brand Name):", ["NO", "YES"], index=0, key="mineral_mixture_option_fv")
    name_of_mineral_mixture = None
    if mineral_mixture_option == "YES":
        name_of_mineral_mixture = st.text_input("Name Of Mineral Mixture:", "")

    toxin_binder = st.radio("Toxin Binder:", ["YES", "NO"], index=0, key="toxin_binder_fv")
    cmt_kit = st.radio("CMT Kit:", ["NO", "YES"], index=0, key="cmt_kit_fv")
    dip_cup = st.radio("Dip Cup With Solution:", ["NO", "YES"], index=0, key="dip_cup_fv")

    separate_space_manure = st.radio("Separate Space For Dumping Pit For Manure Waste:", ["YES", "NO"], index=0, key="separate_space_manure_fv")
    provision_drainage_waste = st.radio("Provision For Drainage And Waste:", ["YES", "NO"], index=0, key="provision_drainage_waste_fv")
    biogas_installation = st.radio("Biogas Installation:", ["NO", "YES"], index=0, key="biogas_installation_fv")
    surplus_milk_bmc = st.radio("100% Surplus Milk Poured To BMC:", ["YES", "NO"], index=0, key="surplus_milk_bmc_fv")

    photo_1 = st.file_uploader("Photo 1:", type=["jpg", "jpeg", "png"])


    st.header("Other Details")

    source_of_water = st.text_input("Source Of Water:", "Biar water")
    freq_cmt_testing = st.number_input("Frequency Of CMT Testing (No Of Days):", min_value=0, value=0)
    freq_cleaning_milking_machines = st.number_input("Frequency Of Cleaning Of Milking Machines (No Of Days):", min_value=0, value=2)
    type_milk_container = st.text_input("Type Of Milk Container:", "PLASTIC")
    duration_milk_kept = st.number_input("Duration Of Milk Kept At Farm Post Milking (minutes):", min_value=0, value=15)
    recent_outbreak = st.text_input("Any Recent Outbreak Of Contamination/Disease:", "No recent contamination")
    overall_hygiene = st.text_input("Overall Hygiene Of The Farm:", "HIGH")
    space_sick_animal = st.radio("Space For Sick Animal Segregation:", ["YES", "NO"], index=0, key="space_sick_animal_fv")

    recent_disease_reported_option = st.text_input("Recent Disease Reported:", "OTHERS")
    other_recent_disease = None
    # Adjusting logic for "OTHERS" or specific text entry based on typical use
    if recent_disease_reported_option.lower() == "others":
        other_recent_disease = st.text_input("Other Recent Disease Reported (Specify):", "No")
    elif recent_disease_reported_option.strip() == "": # If empty, it's not reported
        other_recent_disease = "Not Reported"
    else: # If a specific text is entered directly
        other_recent_disease = recent_disease_reported_option

    last_date_reporting_disease = st.date_input("Last Date Of Reporting Of Disease:", value=None) # No default example given
    no_of_cattle_affected = st.number_input("No Of Cattle Affected:", min_value=0, value=0)

    most_recent_vet_treatment_option = st.text_input("Most Recent Veterinary Treatment Given:", "OTHER")
    other_most_recent_vet_treatment = None
    # Adjusting logic for "OTHER" or specific text entry based on typical use
    if most_recent_vet_treatment_option.lower() == "other":
        other_most_recent_vet_treatment = st.text_input("Other Most Recent Veterinary Treatment Given (Specify):", "Artificial Incimiantion")
    elif most_recent_vet_treatment_option.strip() == "": # If empty, no treatment
        other_most_recent_vet_treatment = "No Treatment"
    else: # If a specific text is entered directly
        other_most_recent_vet_treatment = most_recent_vet_treatment_option

    date_last_vet_treatment = st.date_input("Date Of Last Veterinary Treatment:", value=dt_date(2025, 4, 22))
    presence_moldy_contaminated_feed = st.radio("Presence Of Moldy Or Contaminated Feed:", ["NO", "YES"], index=0, key="presence_moldy_contaminated_feed_fv")


    st.markdown("---") # Separator
    submit_button = st.form_submit_button(label='Submit Farm Visit Data')

    if submit_button:
        st.success("Form Submitted Successfully!")
        # Collect data into a dictionary
        submitted_data = {
            "Date": date.isoformat() if date else None, # Convert date to ISO format string
            "Activity Type": activity_type,
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
            "BMC": bmc_selected, # Use the selected BMC name
            "Other BMC Name (Farm Visit)": other_bmc_name_fv, # Include the "Other" BMC name if specified
            "Milk Production At Farm": milk_production,
            "Herd Size": herd_size,
            "No Of Desi": no_of_desi,
            "No Of Cross Breed": no_of_cross_breed,
            "No Of Cattle In Milk": no_of_cattle_in_milk,
            "Shed (Provision For Minimum 5 Animals)": shed,
            "Loose Housing": loose_housing,
            "Ad-hoc Water Availability": ad_hoc_water_availability,
            "Floor Mats": floor_mats,
            "Concentrated Feed (If Yes, brand Name Available)": concentrated_feed_option,
            "Name Of Concentrated Feed": name_of_concentrated_feed,
            "Feed Supplements (Mention Names)": feed_supplements,
            "Dry Fodder Name": dry_fodder_name,
            "Green Fodder Name": green_fodder_name,
            "Silage": silage,
            "Mineral Mixture (If Yes, Brand Name)": mineral_mixture_option,
            "Name Of Mineral Mixture": name_of_mineral_mixture,
            "Toxin Binder": toxin_binder,
            "CMT Kit": cmt_kit,
            "Dip Cup With Solution": dip_cup,
            "Separate Space For Dumping Pit For Manure Waste": separate_space_manure,
            "Provision For Drainage And Waste": provision_drainage_waste,
            "Biogas Installation": biogas_installation,
            "100% Surplus Milk Poured To BMC": surplus_milk_bmc,
            "Photo 1": photo_1.name if photo_1 else "No file uploaded", # Display file name if uploaded
            "Source Of Water": source_of_water,
            "Frequency Of CMT Testing (No Of Days)": freq_cmt_testing,
            "Frequency Of Cleaning Of Milking Machines (No Of Days)": freq_cleaning_milking_machines,
            "Type Of Milk Container": type_milk_container,
            "Duration Of Milk Kept At Farm Post Milking (minutes)": duration_milk_kept,
            "Any Recent Outbreak Of Contamination/Disease": recent_outbreak,
            "Overall Hygiene Of The Farm": overall_hygiene,
            "Space For Sick Animal Segregation": space_sick_animal,
            "Recent Disease Reported": recent_disease_reported_option,
            "Other Recent Disease Reported (Specify)": other_recent_disease,
            "Last Date Of Reporting Of Disease": last_date_reporting_disease.isoformat() if last_date_reporting_disease else None,
            "No Of Cattle Affected": no_of_cattle_affected,
            "Most Recent Veterinary Treatment Given": most_recent_vet_treatment_option,
            "Other Most Recent Veterinary Treatment Given (Specify)": other_most_recent_vet_treatment,
            "Date Of Last Veterinary Treatment": date_last_vet_treatment.isoformat() if date_last_vet_treatment else None,
            "Presence Of Moldy Or Contaminated Feed": presence_moldy_contaminated_feed
        }
        # Append the collected data to the session state list
        st.session_state.farm_visit_data.append(submitted_data)
        st.success("Farm Visit data recorded for this session!")

# --- Real-time View and Download Option for Farm Visit Data ---
st.header("Real-time View & Download (Current Session)")

if st.session_state.farm_visit_data:
    st.subheader("Submitted Farm Visit Entries:")
    df_farm_visit = pd.DataFrame(st.session_state.farm_visit_data)
    # Ensure all columns are strings for consistent display and CSV export
    df_farm_visit = df_farm_visit.astype(str)
    st.dataframe(df_farm_visit, use_container_width=True) # Make dataframe wide

    csv_farm_visit = df_farm_visit.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Farm Visit Data as CSV",
        data=csv_farm_visit,
        file_name="farm_visit_data.csv",
        mime="text/csv",
        help="Download all Farm Visit data collected in this session."
    )
    st.info(f"Total Farm Visit entries submitted in this session: {len(st.session_state.farm_visit_data)}")
else:
    st.info("No Farm Visit data submitted yet in this session. Submit the form above to see data here.")
