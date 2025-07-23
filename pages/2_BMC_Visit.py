import streamlit as st
import pandas as pd
from datetime import date as dt_date # Import date for setting default today's date

st.set_page_config(layout="centered", page_title="Ksheersagar - BMC Visit Data Entry")

# --- Session State Initialization for this page ---
# This ensures 'bmc_visit_data' exists even if this page is run directly or first
if 'bmc_visit_data' not in st.session_state:
    st.session_state.bmc_visit_data = []
# --------------------------------------------------

st.title("🚚 Ksheersagar - BMC Visit Data Entry")
st.write("Please fill out the details for the BMC visit below.")

# Define BMC names for Govind and SDDPL
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

# Combined list for BMC Name dropdown
ALL_BMC_NAMES = sorted(list(set(GOVIND_BMC_NAMES + SDDPL_BMC_NAMES))) # Use set to remove duplicates and sort

# Cattle Feed Brand Name options
CATTLE_FEED_BRAND_OPTIONS = [
    "Royal Bypro and classic", "Govind Classic Biopro", "Govind Royle Biopro",
    "SDDPL Samruddhi", "SDDPL Samruddhi Plus", "SDDPL Samruddhi Gold",
    "SDDPL Shakti", "Others"
]

# Dropdown options for "Overall Infrastructure" and "BMC Cleaning & Hygiene"
QUALITY_OPTIONS = ["Poor", "Fair", "Good", "Best"]

# Use a form container for better organization and submission handling
with st.form(key='bmc_visit_form'):

    st.header("General BMC Visit Information")

    col1, col2 = st.columns(2)
    with col1:
        # Renamed "Crop" to "BMC Code"
        bmc_code = st.text_input("BMC Code:")
        scheduled_start_date = st.date_input("SCHEDULED START DATE:", value=dt_date(2025, 5, 7))
        
        # Corrected "Organization" options
        organization = st.selectbox(
            "Organization:",
            ["Govind Milk", "SDDPL"], # Combined Govind Milk and GOVIND
            index=0,
            key="organization_bmc"
        )

        # Determine BMC name options based on selected organization
        # The prompt asked for "Names of all BMCs (Refer list in "BMC Names" sheet) Dropdown"
        # Since I don't have the sheet, I'm combining the two lists you provided.
        bmc_options_dropdown = ["SELECT"] + ALL_BMC_NAMES + ["OTHERS"]
        
        # BMC Name as Dropdown
        bmc_name_option = st.selectbox(
            "BMC Name:",
            bmc_options_dropdown,
            index=0,
            key="bmc_name_option_bmc" # Unique key
        )
        # Conditional input for "OTHERS" BMC name
        other_bmc_name = None
        if bmc_name_option == "OTHERS":
            other_bmc_name = st.text_input("Other BMC Name (Specify):", "", key="other_bmc_name_input")

        # Corrected "Activity Created by" options
        activity_created_by = st.selectbox(
            "ACTIVITY CREATED BY:",
            ["Nilesh", "Dr Sachin", "bhusan", "subhrat", "aniket", "ritesh"], # Combined Dhanwate Nilesh and nilesh
            index=0,
            key="activity_created_by_bmc" # Unique key
        )

    with col2:
        # "State" as Freeze (display only, not editable)
        state = st.text_input("State:", "Maharashtra", disabled=True) 
        district_option = st.selectbox(
            "District:",
            ["Satara", "Pune", "Ahmednagar", "Solapur", "OTHERS"],
            index=0,
            key="district_option_bmc" # Unique key
        )
        sub_district_option = st.selectbox(
            "Sub District:",
            ["Phaltan", "malshiras", "Baramati", "Indapur", "Daund", "Purander", "Pachgani", "Man",
             "Khatav", "Koregaon", "Khandala", "Shirur", "OTHERS"],
            index=0,
            key="sub_district_option_bmc" # Unique key
        )
        collecting_village = st.text_input("Collecting Village:", "Hol")
        village = st.text_input("Village:", "HOL")

    # Conditional fields for "OTHERS" District / Sub District / Village
    other_district_input = None
    if district_option == "OTHERS":
        other_district_input = st.text_input("Other District (Specify):", "", key="other_district_input")
    actual_district = other_district_input if district_option == "OTHERS" and other_district_input else district_option

    other_sub_district_input = None
    if sub_district_option == "OTHERS":
        other_sub_district_input = st.text_input("Other Sub District (Specify):", "", key="other_sub_district_input")
    actual_sub_district = other_sub_district_input if sub_district_option == "OTHERS" and other_sub_district_input else sub_district_option

    # Conditional 'other_village' based on explicitly typed "OTHERS" in original village fields
    other_village_input = None
    if "OTHERS" in [collecting_village.upper(), village.upper()]:
        other_village_input = st.text_input("Other Village (Specify if not in list):", "", key="other_village_input")
    other_village = other_village_input if other_village_input else None

    # Removed Tehsil question as requested
    tehsil = None # Set to None as it's removed

    st.header("BCF (Bulk Milk Cooler Farmer) Details")
    col3, col4 = st.columns(2)
    with col3:
        bcf_name = st.text_input("BCF Name:", "Sachin Shahuraje Bhosale")
        bcf_gender = st.selectbox("BCF Gender:", ["MALE", "FEMALE"], index=0, key="bcf_gender_bmc")
        education = st.selectbox(
            "Education:",
            ["10th pass", "12th pass", "Graduation", "Post graduation", "Others (Specify)"],
            index=2, # Default to Graduation
            key="education_bmc" # Unique key
        )
        # Conditional input for "Others (Specify)" education
        other_education = None
        if education == "Others (Specify)":
            other_education = st.text_input("Other Education (Specify):", "", key="other_education_input")

        bcf_mobile_number = st.text_input("BCF Mobile Number:", "9096807277")

    with col4:
        operating_staff_no = st.number_input("Operating Staff (No.):", min_value=0, value=2)
        distance_from_ho_km = st.number_input("Distance From HO (KM):", min_value=0, value=25)
        total_registered_farmer_no = st.number_input("Total Registered Farmer (No.):", min_value=0, value=93)
        active_farmer_no = st.number_input("Active Farmer (No.):", min_value=0, value=65)

    st.header("Capacity & Collection Details")
    col5, col6 = st.columns(2)
    with col5:
        total_tank_capacity = st.number_input("Total Tank Capacity:", min_value=0, value=2500)
        total_capacity_tank1 = st.number_input("Total Capacity (Tank 1):", min_value=0, value=2000)
        total_capacity_tank2 = st.number_input("Total Capacity (Tank 2):", min_value=0, value=500)
        total_capacity_tank3 = st.number_input("Total Capacity (Tank 3):", min_value=0, value=0)
        total_capacity_tank4 = st.number_input("Total Capacity (Tank 4):", min_value=0, value=0)
        space_segregation_tank = st.text_input("Space available for Segregation Tank:", "500 lit segregation tank available")

    with col6:
        milk_segregated_lpd = st.number_input("MILK SEGREGATED (LPD):", min_value=0, value=320)
        morning_milk_collection_end_time = st.number_input("MORNING MILK COLLECTION END TIME (e.g., 9.3 for 9:30 AM):", min_value=0.0, value=9.3, step=0.1)
        morning_milk_lpd = st.number_input("MORNING MILK (LPD):", min_value=0, value=1250)
        evening_milk_collection_end_time = st.number_input("EVENING MILK COLLECTION END TIME (e.g., 9 for 9:00 PM):", min_value=0.0, value=9.0, step=0.1)
        evening_milk_lpd = st.number_input("EVENING MILK (LPD):", min_value=0, value=1100)

    st.header("Milk Quality & Payment")
    col7, col8 = st.columns(2)
    with col7:
        fat = st.number_input("FAT:", min_value=0.0, value=3.5, step=0.1)
        snf = st.number_input("SNF:", min_value=0.0, value=8.1, step=0.1)
        farmer_payment_cycle_days = st.number_input("FARMER PAYMENT CYCLE (DAYS):", min_value=0, value=10)
        direct_farmer_pouring_no = st.number_input("Direct Farmer pouring (No.):", min_value=0, value=30)
    with col8:
        inward_vehicle_route_no = st.number_input("Inward Vehicle Route (No.):", min_value=0, value=1)
        inward_route_farmer_no = st.number_input("Inward Route Farmer (No.):", min_value=0, value=35)
        inward_route_milk_lpd = st.number_input("Inward Route Milk (LPD):", min_value=0, value=800)


    st.header("Infrastructure & Compliance")
    # "Overall Infrastructure" as Dropdown
    overall_infrastructure = st.selectbox("Overall Infrastructure:", QUALITY_OPTIONS, index=2) # Default to Good
    remark_infra = st.text_area("Remark (Infrastructure):", "Good infrastructure, seprate room for cattle feed")
    # "BMC Cleaning & Hygiene" as Dropdown
    bmc_cleaning_hygiene = st.selectbox("BMC Cleaning & Hygiene:", QUALITY_OPTIONS, index=2) # Default to Good

    col_infra1, col_infra2, col_infra3, col_infra4 = st.columns(4)
    with col_infra1:
        air_curtain = st.radio("Air curtain:", ["YES", "NO"], index=0, key="air_curtain_bmc")
        fly_catcher = st.radio("Fly Catcher:", ["YES", "NO"], index=0, key="fly_catcher_bmc")
    with col_infra2:
        wash_basin = st.radio("Wash Basin:", ["YES", "NO"], index=0, key="wash_basin_bmc")
        opening_window_door = st.radio("Opening (Window/Door):", ["YES", "NO"], index=0, key="opening_window_door_bmc")
    with col_infra3:
        intact_floor = st.radio("Intact Floor in BMC Premise:", ["YES", "NO"], index=0, key="intact_floor_bmc")
        digitize_system = st.radio("Digitize System:", ["YES", "NO"], index=0, key="digitize_system_bmc")
    with col_infra4:
        fssai_licence = st.radio("FSSAI Licence:", ["YES", "NO"], index=0, key="fssai_licence_bmc")
        remark_fssai = st.text_area("Remark (FSSAI):", "Shourya software using for farmer milk data collection")

    wg_scale_licence = st.radio("Wg Scale Licence:", ["NO", "YES"], index=0, key="wg_scale_licence_bmc")
    sops = st.radio("SOP's:", ["YES", "NO"], index=0, key="sops_bmc")

    stirrer_ekosilk_indifoss = st.radio("Stirrer/Ekomilk/Indifoss:", ["YES", "NO"], index=0, key="stirrer_ekosilk_indifoss_bmc")
    remark_stirrer = st.text_area("Remark (Stirrer/Ekomilk/Indifoss):", "")

    sampler_dipper_plunger = st.radio("Sampler/Dipper/Plunger:", ["YES", "NO"], index=0, key="sampler_dipper_plunger_bmc")
    remark_sampler = st.text_area("Remark (Sampler/Dipper/Plunger):", "")

    milk_temp_check = st.radio("Milk Temp Check:", ["YES", "NO"], index=0, key="milk_temp_check_bmc")
    remark_milk_temp = st.text_area("Remark (Milk Temp):", "9°c temp of gold tank at the time of visit 8.49AM")

    cleaning_chemicals = st.radio("Cleaning Chemicals:", ["YES", "NO"], index=0, key="cleaning_chemicals_bmc")
    remark_cleaning_chemicals = st.text_area("Remark (Cleaning Chemicals):", "")

    hot_water_source = st.radio("Hot Water Source:", ["YES", "NO"], index=0, key="hot_water_source_bmc")
    remark_hot_water = st.text_area("Remark (Hot Water Source):", "Electric water heater using for hot water")

    strainer_nylon_cloth = st.radio("Strainer/Nylon cloth available:", ["YES", "NO"], index=0, key="strainer_nylon_cloth_bmc")
    sample_bottle = st.radio("Sample Bottle:", ["YES", "NO"], index=0, key="sample_bottle_bmc")

    st.header("Farmer & Competitor Details")
    col9, col10 = st.columns(2)
    with col9:
        animal_welfare_farm_no = st.number_input("Animal Welfare Farm (No.):", min_value=0, value=9)
        # Renamed "FARMER USE (CATTLE FEED)"
        farmer_use_cattle_feed = st.number_input("FARMER USE (compliant CATTLE FEED):", min_value=0, value=58)
        # Renamed "Cattle Feed bag sale (month)"
        cattle_feed_bag_sale_month = st.number_input("Compliant Cattle Feed bag sale (month):", min_value=0, value=250)
        
        # "Cattle Feed Brand Name" as Multi-select
        cattle_feed_brand_name = st.multiselect(
            "Cattle Feed Brand Name:",
            CATTLE_FEED_BRAND_OPTIONS,
            default=["Royal Bypro and classic"], # Set a default if appropriate
            key="cattle_feed_brand_name_bmc"
        )
        # Conditional input for "Others" option in multi-select
        other_cattle_feed_brand_name = None
        if "Others" in cattle_feed_brand_name:
            other_cattle_feed_brand_name = st.text_input("Other Cattle Feed Brand Name (Specify):", "", key="other_cattle_feed_brand_name_input")

        farmer_use_mineral_mixture_qty = st.number_input("FARMER USE (MINERAL MIXTURE) Quantity:", min_value=0, value=14)
        mineral_mixture_brand_name = st.text_input("MINERAL MIXTURE BRAND NAME:", "Govind Chileted")
        farmer_use_evm_rtu_qty = st.number_input("FARMER USE (EVM RTU) Quantity:", min_value=0, value=0)
        evm_rtu = st.text_input("EVM RTU:", "NA")
        biogas_installed = st.number_input("BIOGAS INSTALLED:", min_value=0, value=8)
        any_bank_linkage = st.text_input("ANY BANK LINKAGE:", "No")

    with col10:
        st.subheader("Competitor Details")
        competitor1_name = st.text_input("COMPETITOR 1 NAME:", "Heritage")
        competitor1_milk_lpd = st.number_input("COMPETITOR 1 MILK (LPD):", min_value=0, value=1300)
        competitor2_name = st.text_input("Competitor 2 Name:", "Amul")
        competitor2_milk_lpd = st.number_input("COMPETITOR 2 MILK (LPD):", min_value=0, value=2500)
        competitor3_name = st.text_input("Competitor 3 Name:", "Dynamix")
        competitor3_milk_lpd = st.number_input("COMPETITOR 3 MILK (LPD):", min_value=0, value=1100)
        competitor4_name = st.text_input("Competitor 4 Name:")
        competitor4_milk_lpd = st.number_input("COMPETITOR 4 MILK (LPD):", min_value=0, value=0)


    st.markdown("---") # Separator
    submit_button = st.form_submit_button(label='Submit BMC Visit Data')

    if submit_button:
        st.success("BMC Visit Data Submitted Successfully!")
        # Collect data into a dictionary
        submitted_data = {
            "BMC Code": bmc_code, # Renamed
            "SCHEDULED START DATE": scheduled_start_date.isoformat() if scheduled_start_date else None,
            "BMC Name (Option)": bmc_name_option,
            "Other BMC Name": other_bmc_name,
            "ACTIVITY CREATED BY": activity_created_by,
            "Organization": organization,
            "State": state,
            "District (Option)": district_option,
            "Other District": actual_district if district_option == "OTHERS" else None, # Store actual value if "OTHERS" chosen
            "Sub District (Option)": sub_district_option,
            "Other Sub District": actual_sub_district if sub_district_option == "OTHERS" else None,
            "Collecting Village": collecting_village,
            "Village": village,
            "Other Village": other_village,
            "Tehsil": "Removed", # Indicate that Tehsil field was removed
            "BCF Name": bcf_name,
            "BCF Gender": bcf_gender,
            "Education": education,
            "Other Education (Specify)": other_education,
            "BCF Mobile Number": bcf_mobile_number,
            "Operating Staff (No.)": operating_staff_no,
            "Distance From HO (KM)": distance_from_ho_km,
            "Total Registered Farmer (No.)": total_registered_farmer_no,
            "Active Farmer (No.)": active_farmer_no,
            "Total Tank Capacity": total_tank_capacity,
            "Total Capacity(Tank 1)": total_capacity_tank1,
            "Total Capacity(Tank 2)": total_capacity_tank2,
            "Total Capacity(Tank 3)": total_capacity_tank3,
            "Total Capacity(Tank 4)": total_capacity_tank4,
            "Space available for Segregation Tank": space_segregation_tank,
            "MILK SEGREGATED (LPD)": milk_segregated_lpd,
            "MORNING MILK COLLECTION END TIME": morning_milk_collection_end_time,
            "MORNING MILK (LPD)": morning_milk_lpd,
            "EVENING MILK COLLECTION END TIME": evening_milk_collection_end_time,
            "EVENING MILK (LPD)": evening_milk_lpd,
            "FAT": fat,
            "SNF": snf,
            "FARMER PAYMENT CYCLE (DAYS)": farmer_payment_cycle_days,
            "Direct Farmer pouring (No.)": direct_farmer_pouring_no,
            "Inward Vehicle Route (No.)": inward_vehicle_route_no,
            "Inward Route Farmer (No.)": inward_route_farmer_no,
            "Inward Route Milk (LPD)": inward_route_milk_lpd,
            "Overall Infrastructure": overall_infrastructure,
            "Remark (Infrastructure)": remark_infra,
            "BMC Cleaning & Hygiene": bmc_cleaning_hygiene,
            "Air curtain": air_curtain,
            "Fly Catcher": fly_catcher,
            "Wash Basin": wash_basin,
            "Opening(Window/Door)": opening_window_door,
            "Intact Floor in BMC Premise": intact_floor,
            "Digitize System": digitize_system,
            "FSSAI Licence": fssai_licence,
            "Remark (FSSAI)": remark_fssai,
            "Wg Scale Licence": wg_scale_licence,
            "SOP's": sops,
            "Stirrer/Ekomilk/Indifoss": stirrer_ekosilk_indifoss,
            "Remark (Stirrer/Ekomilk/Indifoss)": remark_stirrer,
            "Sampler/Dipper/Plunger": sampler_dipper_plunger,
            "Remark (Sampler/Dipper/Plunger)": remark_sampler,
            "Milk Temp Check": milk_temp_check,
            "Remark (Milk Temp)": remark_milk_temp,
            "Cleaning Chemicals": cleaning_chemicals,
            "Remark (Cleaning Chemicals)": remark_cleaning_chemicals,
            "Hot Water Source": hot_water_source,
            "Remark (Hot Water Source)": remark_hot_water,
            "Strainer/Nylon cloth available": strainer_nylon_cloth,
            "Sample Bottle": sample_bottle,
            "Animal Welfare Farm (No.)": animal_welfare_farm_no,
            "FARMER USE (compliant CATTLE FEED)": farmer_use_cattle_feed, # Renamed
            "Compliant Cattle Feed bag sale (month)": cattle_feed_bag_sale_month, # Renamed
            "Cattle Feed Brand Name": ", ".join(cattle_feed_brand_name), # Join selected options for storage
            "Other Cattle Feed Brand Name (Specify)": other_cattle_feed_brand_name, # Store specified name
            "FARMER USE(MINERAL MIXTURE) Quantity": farmer_use_mineral_mixture_qty,
            "MINERAL MIXTURE BRAND NAME": mineral_mixture_brand_name,
            "FARMER USE(EVM RTU) Quantity": farmer_use_evm_rtu_qty,
            "EVM RTU": evm_rtu,
            "BIOGAS INSTALLED": biogas_installed,
            "ANY BANK LINKAGE": any_bank_linkage,
            "COMPETITOR 1 NAME": competitor1_name,
            "COMPETITOR 1 MILK (LPD)": competitor1_milk_lpd,
            "Competitor 2 Name": competitor2_name,
            "COMPETITOR 2 MILK (LPD)": competitor2_milk_lpd,
            "Competitor 3 Name": competitor3_name,
            "COMPETITOR 3 MILK (LPD)": competitor3_milk_lpd,
            "Competitor 4 Name": competitor4_name,
            "COMPETITOR 4 MILK (LPD)": competitor4_milk_lpd,
        }
        # Append the collected data to the session state list
        st.session_state.bmc_visit_data.append(submitted_data)
        st.success("BMC Visit data recorded for this session!")

# --- Real-time View and Download Option for BMC Visit Data ---
st.header("Real-time View & Download (Current Session)")

if st.session_state.bmc_visit_data:
    st.subheader("Submitted BMC Visit Entries:")
    df_bmc_visit = pd.DataFrame(st.session_state.bmc_visit_data)
    # Ensure all columns are strings for consistent display and CSV export
    df_bmc_visit = df_bmc_visit.astype(str)
    st.dataframe(df_bmc_visit, use_container_width=True) # Make dataframe wide

    csv_bmc_visit = df_bmc_visit.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download BMC Visit Data as CSV",
        data=csv_bmc_visit,
        file_name="bmc_visit_data.csv",
        mime="text/csv",
        help="Download all BMC Visit data collected in this session."
    )
    st.info(f"Total BMC Visit entries submitted in this session: {len(st.session_state.bmc_visit_data)}")
else:
    st.info("No BMC Visit data submitted yet in this session. Submit the form above to see data here.")
