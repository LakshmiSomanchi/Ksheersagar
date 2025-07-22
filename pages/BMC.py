# pages/2_BMC_Visit.py
import streamlit as st
import pandas as pd # For date handling and potential data display

st.set_page_config(layout="centered", page_title="Ksheersagar - BMC Visit Data Entry")

st.title("🚚 Ksheersagar - BMC Visit Data Entry")
st.write("Please fill out the details for the BMC visit below.")

# Use a form container for better organization and submission handling
with st.form(key='bmc_visit_form'):

    st.header("General BMC Visit Information")

    col1, col2 = st.columns(2)
    with col1:
        crop = st.text_input("CROP:")
        scheduled_start_date = st.date_input("SCHEDULED START DATE:", pd.to_datetime("2025-05-07"))
        bmc_name_option = st.selectbox(
            "BMC Name:",
            ["GOVIND SHWETKRANTI ABHIYAN HOL", "OTHERS"]
            + ["JYOTIRLING DUDH SANKALAN VA SHITKARAN KENDRA"], # Example from previous page
            index=0
        )
        activity_created_by = st.selectbox(
            "ACTIVITY CREATED BY:",
            ["Dhanwate Nilesh", "Dr Sachin", "bhusan", "nilesh", "subhrat", "aniket", "ritesh"],
            index=0
        )
        organization = st.selectbox("Organization:", ["Govind Milk", "SDDPL", "GOVIND"], index=0)

    with col2:
        state = st.text_input("State:", "Maharashtra")
        district_option = st.selectbox(
            "District:",
            ["Satara", "Pune", "Ahmednagar", "Solapur"],
            index=0
        )
        sub_district_option = st.selectbox(
            "Sub District:",
            ["Phaltan", "malshiras", "Baramati", "Indapur", "Daund", "Purander", "Pachgani", "Man",
             "Khatav", "Koregaon", "Khandala", "Shirur"],
            index=0
        )
        collecting_village = st.text_input("Collecting Village:", "Hol")
        village = st.text_input("Village:", "HOL")

    # Conditional fields for "OTHERS" BMC name / District / Sub District
    other_bmc_name = None
    if bmc_name_option == "OTHERS":
        other_bmc_name = st.text_input("Other BMC Name (Specify):", "Govind Swetkranti Dudh")

    other_village = st.text_input("Other Village (Specify if not in list):", "") # Assuming this is separate from 'Village'

    tehsil = st.text_input("Tehsil:", "PHALTAN")
    other_tehsil = st.text_input("Other Tehsil (Specify if not in list):", "") # Assuming this is separate from 'Tehsil'

    district_text_input = st.text_input("District (Text):", "SATARA") # Separate from dropdown if "OTHERS" chosen
    other_district = st.text_input("Other District (Specify if not in list):", "") # Assuming this is separate from 'District' dropdown


    st.header("BCF (Bulk Milk Cooler Farmer) Details")
    col3, col4 = st.columns(2)
    with col3:
        bcf_name = st.text_input("BCF Name:", "Sachin Shahuraje Bhosale")
        bcf_gender = st.selectbox("BCF Gender:", ["MALE", "FEMALE"], index=0)
        education = st.selectbox(
            "Education:",
            ["10th pass", "12th pass", "Graduation", "Post graduation", "Others (Specify)"],
            index=2 # Default to Graduation
        )
        # Conditional input for "Others (Specify)" education
        other_education = None
        if education == "Others (Specify)":
            other_education = st.text_input("Other Education (Specify):", "")

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
    overall_infrastructure = st.text_input("Overall Infrastructure:", "OK")
    remark_infra = st.text_area("Remark (Infrastructure):", "Good infrastructure, seprate room for cattle feed")
    bmc_cleaning_hygiene = st.text_input("BMC Cleaning & Hygiene:", "3-GOOD")

    col_infra1, col_infra2, col_infra3, col_infra4 = st.columns(4)
    with col_infra1:
        air_curtain = st.radio("Air curtain:", ["YES", "NO"], index=0)
        fly_catcher = st.radio("Fly Catcher:", ["YES", "NO"], index=0)
    with col_infra2:
        wash_basin = st.radio("Wash Basin:", ["YES", "NO"], index=0)
        opening_window_door = st.radio("Opening (Window/Door):", ["YES", "NO"], index=0)
    with col_infra3:
        intact_floor = st.radio("Intact Floor in BMC Premise:", ["YES", "NO"], index=0)
        digitize_system = st.radio("Digitize System:", ["YES", "NO"], index=0)
    with col_infra4:
        fssai_licence = st.radio("FSSAI Licence:", ["YES", "NO"], index=0)
        remark_fssai = st.text_area("Remark (FSSAI):", "Shourya software using for farmer milk data collection")

    wg_scale_licence = st.radio("Wg Scale Licence:", ["NO", "YES"], index=0)
    sops = st.radio("SOP's:", ["YES", "NO"], index=0)

    stirrer_ekosilk_indifoss = st.radio("Stirrer/Ekomilk/Indifoss:", ["YES", "NO"], index=0)
    remark_stirrer = st.text_area("Remark (Stirrer/Ekomilk/Indifoss):", "")

    sampler_dipper_plunger = st.radio("Sampler/Dipper/Plunger:", ["YES", "NO"], index=0)
    remark_sampler = st.text_area("Remark (Sampler/Dipper/Plunger):", "")

    milk_temp_check = st.radio("Milk Temp Check:", ["YES", "NO"], index=0)
    remark_milk_temp = st.text_area("Remark (Milk Temp):", "9°c temp of gold tank at the time of visit 8.49AM")

    cleaning_chemicals = st.radio("Cleaning Chemicals:", ["YES", "NO"], index=0)
    remark_cleaning_chemicals = st.text_area("Remark (Cleaning Chemicals):", "")

    hot_water_source = st.radio("Hot Water Source:", ["YES", "NO"], index=0)
    remark_hot_water = st.text_area("Remark (Hot Water Source):", "Electric water heater using for hot water")

    strainer_nylon_cloth = st.radio("Strainer/Nylon cloth available:", ["YES", "NO"], index=0)
    sample_bottle = st.radio("Sample Bottle:", ["YES", "NO"], index=0)

    st.header("Farmer & Competitor Details")
    col9, col10 = st.columns(2)
    with col9:
        animal_welfare_farm_no = st.number_input("Animal Welfare Farm (No.):", min_value=0, value=9)
        farmer_use_cattle_feed = st.number_input("FARMER USE (CATTLE FEED):", min_value=0, value=58)
        cattle_feed_bag_sale_month = st.number_input("Cattle Feed bag sale (month):", min_value=0, value=250)
        cattle_feed_brand_name = st.selectbox(
            "Cattle Feed Brand Name:",
            [
                "Royal Bypro and classic", "1. Govind Classic Biopro", "2. Govind Royle Biopro",
                "3. SDDPL Samruddhi", "4. SDDPL Samruddhi Plus", "5. SDDPL Samruddhi Gold",
                "6. SDDPL Shakti", "7. Others"
            ],
            index=0
        )
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
        st.write("---")
        st.subheader("Collected Data for BMC Visit:")

        # Display all collected data
        data = {
            "CROP": crop,
            "SCHEDULED START DATE": scheduled_start_date,
            "BMC Name (Option)": bmc_name_option,
            "Other BMC Name": other_bmc_name,
            "ACTIVITY CREATED BY": activity_created_by,
            "Organization": organization,
            "State": state,
            "District (Option)": district_option,
            "Other District": other_district, # Captures manual entry if needed
            "Sub District (Option)": sub_district_option,
            "Collecting Village": collecting_village,
            "Village": village,
            "Other Village": other_village, # Captures manual entry if needed
            "Tehsil": tehsil,
            "Other Tehsil": other_tehsil, # Captures manual entry if needed
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
            "FARMER USE (CATTLE FEED)": farmer_use_cattle_feed,
            "Cattle Feed bag sale (month)": cattle_feed_bag_sale_month,
            "Cattle Feed Brand Name": cattle_feed_brand_name,
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
        st.json(data)
