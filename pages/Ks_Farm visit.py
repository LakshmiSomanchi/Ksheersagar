# pages/1_Farm_Visit.py
import streamlit as st
import pandas as pd

# This config should still be present in each page for independent running
st.set_page_config(layout="centered", page_title="Ksheersagar - Farm Visit Data Entry")

st.title("🐄 Ksheersagar - Farm Visit Data Entry")
st.write("Please fill out the details for the farm visit below.")

# Use a form container for better organization and submission handling
with st.form(key='farm_visit_form'):

    st.header("General Farm Visit Information")

    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date:", pd.to_datetime("2025-05-07"))
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
            ["Schreiber Dynamix", "Govind", "SDDPL"],
            index=0 # Default to Schreiber Dynamix
        )
        state = st.text_input("State:", "Maharashtra")
        district = st.text_input("District:", "Satara")
    with col4:
        sub_district = st.text_input("Sub District:", "Phaltan")
        collecting_village = st.text_input("Collecting Village:", "SAKHARWADi")
        bmc = st.selectbox(
            "BMC:",
            ["JYOTIRLING DUDH SANKALAN VA SHITKARAN KENDRA"],
            index=0
        )

    st.header("Milk Production & Herd Details")
    col5, col6 = st.columns(2)
    with col5:
        milk_production = st.number_input("Milk Production At Farm:", min_value=0, value=95)
        herd_size = st.number_input("Herd Size:", min_value=0, value=16)
        no_of_desi = st.number_input("No Of Desi:", min_value=0, value=0)
        no_of_cross_breed = st.number_input("No Of Cross Breed:", min_value=0, value=16)
        no_of_cattle_in_milk = st.number_input("No Of Cattle In Milk:", min_value=0, value=8)

    with col6:
        shed = st.radio("Shed (Provision For Minimum 5 Animals):", ["YES", "NO"], index=0)
        loose_housing = st.radio("Loose Housing:", ["YES", "NO"], index=0)
        ad_hoc_water_availability = st.radio("Ad-hoc Water Availability:", ["YES", "NO"], index=0)
        floor_mats = st.radio("Floor Mats:", ["YES", "NO"], index=0)


    st.header("Feed & Fodder Management")

    concentrated_feed_option = st.selectbox(
        "Concentrated Feed (If Yes, brand Name Available):",
        ["YES", "NO"],
        index=0 # Default to YES
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
            index=3 # Default to SDDPL Samruddhi Plus
        )

    feed_supplements = st.selectbox("Feed Supplements (Mention Names):", ["No", "Yes"], index=0)
    dry_fodder_name = st.text_input("Dry Fodder Name:", "Not Available")

    green_fodder_name = st.selectbox(
        "Green Fodder Name:",
        [
            "Sugarcane tops", "Silage", "Napier", "Maize", "Jawar",
            "super Napier", "Sugarcane", "Sugargraze", "Lucerne",
            "berseem", "Methigrass", "others (specify)"
        ],
        index=0 # Default to Sugarcane tops
    )

    silage = st.radio("Silage:", ["YES", "NO"], index=0)

    mineral_mixture_option = st.radio("Mineral Mixture (If Yes, Brand Name):", ["NO", "YES"], index=0)
    name_of_mineral_mixture = None
    if mineral_mixture_option == "YES":
        name_of_mineral_mixture = st.text_input("Name Of Mineral Mixture:", "")

    toxin_binder = st.radio("Toxin Binder:", ["YES", "NO"], index=0)
    cmt_kit = st.radio("CMT Kit:", ["NO", "YES"], index=0)
    dip_cup = st.radio("Dip Cup With Solution:", ["NO", "YES"], index=0)

    separate_space_manure = st.radio("Separate Space For Dumping Pit For Manure Waste:", ["YES", "NO"], index=0)
    provision_drainage_waste = st.radio("Provision For Drainage And Waste:", ["YES", "NO"], index=0)
    biogas_installation = st.radio("Biogas Installation:", ["NO", "YES"], index=0)
    surplus_milk_bmc = st.radio("100% Surplus Milk Poured To BMC:", ["YES", "NO"], index=0)

    photo_1 = st.file_uploader("Photo 1:", type=["jpg", "jpeg", "png"])


    st.header("Other Details")

    source_of_water = st.text_input("Source Of Water:", "Biar water")
    freq_cmt_testing = st.number_input("Frequency Of CMT Testing (No Of Days):", min_value=0, value=0)
    freq_cleaning_milking_machines = st.number_input("Frequency Of Cleaning Of Milking Machines (No Of Days):", min_value=0, value=2)
    type_milk_container = st.text_input("Type Of Milk Container:", "PLASTIC")
    duration_milk_kept = st.number_input("Duration Of Milk Kept At Farm Post Milking (minutes):", min_value=0, value=15)
    recent_outbreak = st.text_input("Any Recent Outbreak Of Contamination/Disease:", "No recent contamination")
    overall_hygiene = st.text_input("Overall Hygiene Of The Farm:", "HIGH")
    space_sick_animal = st.radio("Space For Sick Animal Segregation:", ["YES", "NO"], index=0)

    recent_disease_reported_option = st.text_input("Recent Disease Reported:", "OTHERS")
    other_recent_disease = None
    if recent_disease_reported_option == "OTHERS": # Assuming "OTHERS" will trigger input
        other_recent_disease = st.text_input("Other Recent Disease Reported (Specify):", "No")

    last_date_reporting_disease = st.date_input("Last Date Of Reporting Of Disease:", None)
    no_of_cattle_affected = st.number_input("No Of Cattle Affected:", min_value=0, value=0)

    most_recent_vet_treatment_option = st.text_input("Most Recent Veterinary Treatment Given:", "OTHER")
    other_most_recent_vet_treatment = None
    if most_recent_vet_treatment_option == "OTHER": # Assuming "OTHER" will trigger input
        other_most_recent_vet_treatment = st.text_input("Other Most Recent Veterinary Treatment Given (Specify):", "Artificial Incimiantion")

    date_last_vet_treatment = st.date_input("Date Of Last Veterinary Treatment:", pd.to_datetime("2025-04-22"))
    presence_moldy_contaminated_feed = st.radio("Presence Of Moldy Or Contaminated Feed:", ["NO", "YES"], index=0)


    st.markdown("---") # Separator
    submit_button = st.form_submit_button(label='Submit Farm Visit Data')

    if submit_button:
        st.success("Form Submitted Successfully!")
        # Collect data into a dictionary
        submitted_data = {
            "Date": date,
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
            "BMC": bmc,
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
            "Photo 1": photo_1.name if photo_1 else "No file uploaded",
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
            "Last Date Of Reporting Of Disease": last_date_reporting_disease,
            "No Of Cattle Affected": no_of_cattle_affected,
            "Most Recent Veterinary Treatment Given": most_recent_vet_treatment_option,
            "Other Most Recent Veterinary Treatment Given (Specify)": other_most_recent_vet_treatment,
            "Date Of Last Veterinary Treatment": date_last_vet_treatment,
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
    st.dataframe(df_farm_visit)

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
    st.info("No Farm Visit data submitted yet in this session.")
