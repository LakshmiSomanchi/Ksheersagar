# app.py (Heritage Specific Streamlit Dairy Survey)

import streamlit as st
import pandas as pd
import datetime
import os
import json # To save/load session state as JSON

# Ensure save folder exists
SAVE_DIR = 'survey_responses'
os.makedirs(SAVE_DIR, exist_ok=True)

# Define a directory for auto-saved drafts
DRAFT_DIR = os.path.join(SAVE_DIR, 'drafts')
os.makedirs(DRAFT_DIR, exist_ok=True)

# Streamlit Page Config - THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Heritage Dairy Survey", page_icon="🐄", layout="centered")


# --- Multilingual Translations ---
dict_translations = {
    'English': {
        'Language': 'Language', 'Farmer Profile': 'Farmer Profile', 'VLCC Name': 'VLCC Name',
        'HPC/MCC Code': 'HPC/MCC Code', 'Types': 'Type', 'HPC': 'HPC', 'MCC': 'MCC',
        'Farmer Name': 'Farmer Name', 'Farmer Code': 'Farmer Code / Pourer ID', 'Gender': 'Gender',
        'Male': 'Male', 'Female': 'Female', 'Farm Details': 'Farm Details',
        'Number of Cows': 'Number of Cows', 'No. of Cattle in Milk': 'No. of Cattle in Milk',
        'No. of Calves/Heifers': 'No. of Calves/Heifers', 'No. of Desi cows': 'No. of Desi cows',
        'No. of Cross breed cows': 'No. of Cross breed cows', 'No. of Buffalo': 'No. of Buffalo',
        'Milk Production': 'Milk Production (liters/day)', 'Specific Questions': 'Specific Questions',
        'Green Fodder': 'Green Fodder', 'Type of Green Fodder': 'Type of Green Fodder (Multiple Select)',
        'Quantity of Green Fodder': 'Quantity of Green Fodder (Kg/day)',
        'Dry Fodder': 'Dry Fodder', 'Type of Dry Fodder': 'Type of Dry Fodder (Multiple Select)',
        'Quantity of Dry Fodder': 'Quantity of Dry Fodder (Kg/day)',
        'Pellet Feed': 'Pellet Feed', 'Pellet Feed Brand': 'Pellet Feed Brand (Multiple Select)',
        'Quantity of Pellet Feed': 'Quantity of Pellet Feed (Kg/day)',
        'Mineral Mixture': 'Mineral Mixture',
        'Mineral Mixture Brand': 'Mineral Mixture Brand',
        'Quantity of Mineral Mixture': 'Quantity of Mineral Mixture (gm/day)',
        'Silage': 'Silage', 'Source and Price of Silage': 'Source and Price of Silage',
        'Quantity of Silage': 'Quantity of Silage (Kg/day)', 'Source of Water': 'Source of Water (Multiple Select)',
        'Name': 'Name', 'Date of Visit': 'Date of Visit',
        'Submit': 'Submit', 'Yes': 'Yes', 'No': 'No', 'Download CSV': 'Download CSV',
        'Auto-saved!': 'Auto-saved! You can resume filling the form even if you refresh or lose internet temporarily.',
        'Other (Specify)': 'Other (Specify)',
        'Other Farmer Name': 'Other Farmer Name (Specify)',
        'Other VLCC Name': 'Other VLCC Name (Specify)',
        'Other Pellet Brand': 'Other Pellet Brand (Specify)',
        'Other Mineral Brand': 'Other Mineral Brand (Specify)',
        'Other Water Source': 'Other Water Source (Specify)',
        'Other Surveyor Name': 'Other Surveyor Name (Specify)',
    },
    'Hindi': {
        'Language': 'भाषा', 'Farmer Profile': 'किसान प्रोफ़ाइल', 'VLCC Name': 'वीएलसीसी नाम',
        'HPC/MCC Code': 'एचपीसी/एमसीसी कोड', 'Types': 'प्रकार', 'HPC': 'एचपीसी', 'MCC': 'एमसीसी',
        'Farmer Name': 'किसान का नाम', 'Farmer Code': 'किसान कोड/दूधदाता आईडी', 'Gender': 'लिंग',
        'Male': 'पुरुष', 'Female': 'महिला', 'Farm Details': 'फार्म विवरण',
        'Number of Cows': 'गायों की संख्या', 'No. of Cattle in Milk': 'दूध देने वाले मवेशी',
        'No. of Calves/Heifers': 'बछड़े/बछड़ियां', 'No. of Desi cows': 'देसी गायों की संख्या',
        'No. of Cross breed cows': 'क्रॉसब्रीड गायों की संख्या', 'No. of Buffalo': 'भैंसों की संख्या',
        'Milk Production': 'दूध उत्पादन (लीटर/दिन)', 'Specific Questions': 'विशिष्ट प्रश्न',
        'Green Fodder': 'हरा चारा', 'Type of Green Fodder': 'हरे चारे का प्रकार (एकाधिक चयन)',
        'Quantity of Green Fodder': 'हरे चारे की मात्रा (किलो/दिन)',
        'Dry Fodder': 'सूखा चारा', 'Type of Dry Fodder': 'सूखे चारे का प्रकार (एकाधिक चयन)',
        'Quantity of Dry Fodder': 'सूखे चारे की मात्रा (किलो/दिन)',
        'Pellet Feed': 'पेलेट फ़ीड', 'Pellet Feed Brand': 'पेलेट फ़ीड ब्रांड (एकाधिक चयन)',
        'Quantity of Pellet Feed': 'पेलेट फ़ीड मात्रा (किलो/दिन)',
        'Mineral Mixture': 'खनिज मिश्रण',
        'Mineral Mixture Brand': 'खनिज मिश्रण ब्रांड',
        'Quantity of Mineral Mixture': 'खनिज मिश्रण मात्रा (ग्राम/दिन)',
        'Silage': 'सायलेज', 'Source and Price of Silage': 'सायलेज स्रोत और मूल्य',
        'Quantity of Silage': 'सायलेज मात्रा (किलो/दिन)', 'Source of Water': 'पानी का स्रोत (एकाधिक चयन)',
        'Name': 'सर्वेक्षक का नाम', 'Date of Visit': 'दौरे की तिथि',
        'Submit': 'जमा करें', 'Yes': 'हाँ', 'No': 'नहीं', 'Download CSV': 'CSV डाउनलोड करें',
        'Auto-saved!': 'स्वतः सहेजा गया! आप फ़ॉर्म भरना जारी रख सकते हैं, भले ही आप ताज़ा करें या अस्थायी रूप से इंटरनेट खो दें!',
        'Other (Specify)': 'अन्य (निर्दिष्ट करें)',
        'Other Farmer Name': 'अन्य किसान का नाम (निर्दिष्ट करें)',
        'Other VLCC Name': 'अन्य वीएलसीसी नाम (निर्दिष्ट करें)',
        'Other Pellet Brand': 'अन्य पेलेट ब्रांड (निर्दिष्ट करें)',
        'Other Mineral Brand': 'अन्य खनिज ब्रांड (निर्दिष्ट करें)',
        'Other Water Source': 'अन्य जल स्रोत (निर्दिष्ट करें)',
        'Other Surveyor Name': 'अन्य सर्वेक्षक का नाम (निर्दिष्ट करें)',
    },
    'Marathi': {
        "Language": "भाषा",
        "Farmer Profile": "शेतकरी प्रोफाइल",
        "VLCC Name": "वीएलसीसी नाव",
        "HPC/MCC Code": "एचपीसी/एमसीसी कोड",
        "Types": "प्रकार",
        "HPC": "एचपीसी",
        "MCC": "एमसीसी",
        "Farmer Name": "शेतकऱ्याचे नाव",
        "Farmer Code": "शेतकरी कोड/दूध देणारा आयडी",
        "Gender": "लिंग",
        "Male": "पुरुष",
        "Female": "महिला",
        "Farm Details": "फार्म तपशील",
        "Number of Cows": "गायींची संख्या",
        "No. of Cattle in Milk": "दूध देणाऱ्या जनावरांची संख्या",
        "No. of Calves/Heifers": "वासरे/वषाडांची संख्या",
        "No. of Desi cows": "देशी गायींची संख्या",
        "No. of Cross breed cows": "संकरित गायींची संख्या",
        "No. of Buffalo": "म्हशींची संख्या",
        "Milk Production": "दूध उत्पादन (लिटर/दिवस)",
        "Specific Questions": "विशिष्ट प्रश्न",
        "Green Fodder": "हिरवा चारा",
        "Type of Green Fodder": "हिरव्या चाऱ्याचा प्रकार (अनेक निवडा)",
        "Quantity of Green Fodder": "हिरव्या चाऱ्याचे प्रमाण (किलो/दिवस)",
        "Dry Fodder": "कोरडा चारा",
        "Type of Dry Fodder": "कोरड्या चाऱ्याचा प्रकार (अनेक निवडा)",
        "Quantity of Dry Fodder": "कोरड्या चाऱ्याचे प्रमाण (किलो/दिवस)",
        "Pellet Feed": "गोळी खाद्य",
        "Pellet Feed Brand": "गोळी खाद्य ब्रँड (अनेक निवडा)",
        "Quantity of Pellet Feed": "गोळी खाद्यचे प्रमाण (किलो/दिवस)",
        "Mineral Mixture": "खनिज मिश्रण",
        "Mineral Mixture Brand": "खनिज मिश्रण ब्रँड",
        "Quantity of Mineral Mixture": "खनिज मिश्रणाचे प्रमाण (ग्राम/दिवस)",
        "Silage": "सायलेज",
        "Source and Price of Silage": "सायलेजचा स्त्रोत आणि किंमत",
        "Quantity of Silage": "सायलेजचे प्रमाण (किलो/दिवस)",
        "Type of Farm": "शेताचा प्रकार",
        "Other Type of Farm (if selected above)": "इतर शेताचा प्रकार (वर निवडल्यास)",
        "Source of Water": "पाण्याचा स्त्रोत (अनेक निवडा)",
        "Name": "सर्वेक्षकाचे नाव",
        "Date of Visit": "भेटीची तारीख",
        "Submit": "सादर करा",
        "Yes": "होय",
        "No": "नाही",
        "Download CSV": "CSV डाउनलोड करा",
        'Auto-saved!': 'स्वयं-जतन केले! आपण रिफ्रेश केले किंवा तात्पुरते इंटरनेट गमावले तरीही आपण फॉर्म भरणे सुरू ठेवू शकता.',
        'Other (Specify)': 'इतर (निर्दिष्ट करा)',
        'Other Farmer Name': 'इतर शेतकऱ्याचे नाव (निर्दिष्ट करा)',
        'Other VLCC Name': 'इतर वीएलसीसी नाव (निर्दिष्ट करा)',
        'Other Pellet Brand': 'इतर गोळी खाद्य ब्रँड (निर्दिष्ट करा)',
        'Other Mineral Brand': 'इतर खनिज ब्रँड (निर्दिष्ट करा)',
        'Other Water Source': 'इतर पाण्याचा स्त्रोत (निर्दिष्ट करा)',
        'Other Surveyor Name': 'इतर सर्वेक्षकचे नाव (निर्दिष्ट करा)',
    }
}


# --- Heritage Specific Data (Syntactically Corrected) ---
# NOTE: This data is now provided as a single block for better syntax control.
VLCC_NAMES = [
    "3025-K.V.PALLE", "3026-KOTHA PALLE", "3028-BONAMVARIPALLE", "3029-BOMMAICHERUVUPALLI", "3030-BADDALAVARIPALLI", 
    "3033-CHINNAGOTTIGALLU", "3034-VODDIPALLE", "3036-MUDUPULAVEMULA", "3037-BAYYAREDDYGARIPALLE", "3038-DODDIPALLE", 
    "3040-MARAMREDDYGARIPALLE", "3041-GUTTAPALEM", "3042-CHERUVUMUNDARAPALLI", "3044-VARAMPATIVARIPALLE",
    "3045-ROMPICHERLA", "3046-BANDAKINDAPALLE", "3047-MARASANIVARIPALLI",
    "3024-DEVALAVARIPALLE", "3002-KHAMBAMMITTAPALLE", "3004-MARRIMAKULAPALLE", "3005-NAGARIMADUGUVARIPALLE", "3006-KOORAPARTHIVARIPALLE", 
    "3008-IRRIVANDLAPALLE", "3009-PATHEGADA (U.I)", "3011-PULICHERLA", "3013-GUDAREVUPALLE", "3014-ENUMALAVARIPALLE", 
    "3015-MUNTHAVANDLAPALLE", "3016-REGALLU",
    "3018-REDDIVARIPALLE", "3019-MAJJIGAVANDLAPALLE", "3020-VENKATADASARAPALLE", "3021-BURRAVANDLAPALLE", "3022-KODEKAMBAMVARIPALLI", 
    "3023-SEENAPPAGARIPALLE", "3071-KOTAKADAPALLE", "3072-KOTAKADAPALLE", "3074-PODALAKUNTALAPALLE", "3075-SOMALA", 
    "3076-SOMALA", "3077-SOMALA", "3078-CHINNAGOTTIGALLU", "3079-MATLOLLPALLAI",
    "3080-POLIKIMAKULAPALLE", "3081-K.GOLLAPALLE", "3082-CHERUKUVARIPALLE", "3083-SODUM", "3084-PILER", "3085-CHERUKUVARIPALLE", 
    "3086-SOMALA", "3087-SODUM", "3088-YERRAVARIPALEM",
    "3089-GUDAREVUPALLE", "3090-SOMALA", "3091-PUTTAVARIPALLE", "3092-VAGALLA", "3048-R.KUMMARA PALLE", "3049-HANUMANTHARAYUNIPETA", 
    "3050-CHENCHAMAREDDIGARIPALLE", "3051-BODUMALLUVARIPALLE", "3052-BANDAKINDAPALLE", "3055-NAKKALADINNEVODDIPALLE", "3057-KUKKALODDU",
    "3059-GUNDLAKADAPALLI", "3070-PEDDAPANJANI", "3069-PEDDAPALLI", "3068-KADIRAKUNTA", "3067-KOTALA", "3066-VLLIGATLA(U.I)", 
    "3060-BALIREDDIGARIPALLE", "3061-SODUM", "3062-GONGIVARIPALLE", "3064-SRINADHAPURAM", "3063-GANGUVARIPALLE", "1664-DEVALAMPETA", 
    "1651-YERRAGUNTLAVARIPALLE", "1740-KALIKIRI", "1718-KOTHA PALLE",
    "1542-HARIJANAWADA", "1937-KAMMAPALLE", "1993-T.SANDRAVARIPALLE", "1959-MANCHOORIVARIPALLE", "1812-GANGIREDDIGARIPALLE", 
    "1781-ROMPICHERLA", "1773-SREERAMULAVADDIPALLE", "1770-THATIGUNTAPALEM", "1868-ROMPICHERLA", "1824-YERRAGUNTLAVARIPALLE", 
    "0884-KOTHAPALLE", "0881-ROMPICHERLA", "0880-MUREVANDLAPALLE", "0878-KALIKIRI", "0876-DIGUVAJUPALLI",
    "0874-KONDAREDDIGARIPALLE", "0871-ROMPICHERLA", "0868-NAGARIMADUGUVARIPALLE", "0863-KHAMBAMMITTAPALLE", "0906-REDDIVARIPALLE", 
    "0900-GOLLAPALLE", "0895-PEDDAMALLELA", "0893-PEDDIREDDIGARIPALLE", "0888-BANDARALAVARIPALLE", "0887-ELLAMPALLE", 
    "0830-REGALLU", "0826-MUNIREDDIGARIPALLE", "0824-PILER",
    "0859-KRIHSNAREDDIGARIPALLE", "0851-GYARAMPALLE", "0848-ELLAREDDIGARIPALLE", "0846-KURAVAPALLE", "0842-PEDDAMALLELA", 
    "0839-BANDAMVARIPALLE", "1058-CHERUKUVARIPALLE", "1057-CHERUKUVARIPALLE", "1052-NANJAMPETA", "1017-KHAMBAMVARIPALLE", 
    "1003-PUTTAVANDLAPALLE THANDA", "1272-USTIKAYALAPENTA",
    "1240-MITTAPALLE", "0916-AGRAHARAM", "0915-CHALLAVARIPALLE", "0982-KUCHAMVARIPALLE", "2388-SAGGAMVARI ENDLU", "2380-PILER",
    "2374-PILER", "2437-MARRIMAKULAPALLE", "2421-MATLOLLPALLAI", "2314-KUMMARAPALLE", "2338-SETTIPALLEVANDLAPALLE", "2500-KAMMAPALLE", 
    "2530-AVULAPEDDIREDDIGARIPALL", "2528-MARAMREDDIGARIPALLE", "2526-AVULAPEDDIREDDIGARIPALL", "2463-BOMMAIAHGARIPALLE", 
    "2444-ROMPICHERLA", "2440-BASIREDDIGARIPALLE",
    "2013-THOTIMALAPALLE", "2083-RAJUVARIPALLI H/W", "2045-RAJUVARIPALLI", "2288-RAJUVARIPALLI", "2272-THATIGUNTAPALEM", 
    "2186-KANTAMVARIPALLE", "2183-REGALLU", "2178-SANKENIGUTTAPALLE", "2173-MUNELLAPALLE", "2160-V.K.THURPUPALLE", 
    "2228-GAJULAVARIPALLI", "0296-BESTAPALLE",
    "0335-MATLOLLPALLAI", "0326-LOKAVARIPALLE", "0256-VOOTUPALLE", "0245-BETAPALLE", "0237-BATTUVARIPALLE", "0417-ROMPICHERLA", 
    "0414-BODIPATIVARIPALLE", "0441-BODIPATIVARIPALLE", "0440-VARANASIVARIPALLE",
    "0360":"CHICHILIVARIPALLE",
    "0357":"AKKISANIVARIPALLE", "0394":"SETTIPALLEVANDLAPALLE", "0072":"VAGALLA",
    "0056":"LEMATIVARIPALLE", "0108":"KONDAREDDIGARIPALLE","0016":"ROMPICHERLA",
    "0030":"MELLAVARIPALLE", "0197":"BASIREDDIGARIPALLE", "0173":"MORAVAPALLE",
    "0221":"KURABAPALLE", "0130":"PATHAKURVAPALLE", "0165":"AGRAHARAM",
    "0151":"BONAMVARIPALLE", "0649":"PILER", "0645":"NADIMPALLE",
    "0643":"SAVVALAVARIPALLE", "0636":"KURAPATHIVARIPALLE", "0689":"VANKAVODDIPALLE",
    "0688":"BADDALAVARIPALLI H.W.","0685":"NAGARIMADUGUVARIPALLE", "0668":"KANDUR",
    "0663":"DEVALAVARIPALLE", "0585":"SRIVARAMPURAM", "0575":"RAMREDDIGARIPALLE",
    "0572":"LOKAVARIPALLE", "0613":"NAGAVANDLAPALLI", "0611":"BODIPATIVARIPALLE",
    "0610":"ROMPICHERLA", "0604":"NAGAVANDLAPALLI", "0782":"CHICHILIVARIPALLE",
    "0770":"DEVALAVARIPALLE", "0767":"PEDDAGOTTIGALLU", "0764":"K.V.PALLE",
    "0762":"JAGADAMVARIPALLE", "0753":"BOLLINANIVARIPALLI", "0813":"ROMPICHERLA",
    "0811":"ALAKAMVARIPALLE", "0809":"KOTAKADAPALLE", "0794":"PEDDAGOTTIGALLU",
    "0793":"DIGUVAJUPALLI", "0789":"SODUM", "0788":"BURUJUPALLE",
    "0786":"PEDDAGOTTIGALLU CROSS", "0719":"NADIMPALLE", "0718":"PEDDAGOTTIGALLU",
    "0714":"BODIPATIVARIPALLE", "0709":"REDDIVARIPALLE", "0700":"RAMIREDDIGARIPALLE",
    "0721":"SODUM", "0747":"KURAVAPALLE", "0745":"ETUKURIVARIPALLE",
    "0743":"ROMPICHERLA", "0736":"VOOTUPALLE", "0732":"ROMPICHERLA",
    "0727":"DUSSAVANDLA PALLI", "0726":"SAVVALAVARIPALLE", "0508":"MUREVANDLAPALLE",
    "0490":"MATAMPALLE", "0551":"TALUPULA", "0512":"BONAMVARIPALLE",
    "0473":"KURAVAPALLE", "0477":"VARANASIVARIPALLE"
]


# Extracted Farmer Names and Member Codes from the image
FARMER_DATA = {
    "0005": "GUBBALA ANAMMA", "0003": "G.REDDY SEKHAR",
    "0012":"V. Devaki", "0008": "D. PRASAD REDDY", "0006":"G.Ratnamma",
    "0013": "M.GANGULU", "0014": "K VARADHA NAIDU", "0007": "INDRAVATHI RAMADEVI",
    "0017": "B SAMPURNA", "0015": "J.GANGULU", "0002": "KRISHNAMA NAIDU",
    "0021": "M.S.CHOWDARY", "0029": "DASARI VENKATAIAH", "0030": "K.M.KANTHAMMA",
    "0036": "D.BALAKRISHNA", "0037": "C.SURYA PRAKASH", "0039": "D.CHANDRAMMA",
    "0041": "G.NARASIMHA NAIDU", "0043": "REDDI RAMADEVI", "0044": "D.CHANDRAMMA",
    "0045": "S.PEDDAIAH", "0046": "D.PEDDAIAH", "0047": "K.K.KADIRAMMA",
    "0001": "M.NARAYANAMMA", "0002": "S.K.SUBBAIAH", "0004": "C.M.NARAYANA",
    "0005": "D.MALLAIAH", "0006": "G.CHANDRAIAH", "0008": "J.RAMADEVI",
    "0009": "G.SWARNAMMA", "0011": "J.ESWARAMMA", "0013": "K.GURAVAIAH",
    "0014": "P.DEVAKI DEVI", "0015": "K.NARASIMHULU", "0016": "P REDDY PRASAD",
    "0018": "D.DEVAKI RAMADEVI", "0019": "P.SATYAMMA", "0020": "B.SAMPURNA",
    "0021": "P.PEDDAIAH", "0022": "REDDISEKHAR", "0023": "V.SUBRAMANYAM",
    "0071": "V.REDDY RANI", "0072": "B.GANGULU", "0074": "K.YASHODHA",
    "0075": "D.RAMADEVI", "0076": "H.RAMADEVI", "0077": "R.RAMADEVI",
    "0078": "B.RANI", "0079": "K.VENKATAIAH", "0080": "P.SREERAM REDDY",
    "0081": "M.RAMADEVI", "0082": "M.PENCHALAMAIAH", "0083": "M.M.RATHNAMMA",
    "0084": "N.GANGULU", "0085": "N.RAMALINGAM", "0086": "N.RAMADEVI",
    "0087": "V.CHANDRAIAH", "0088": "N.SRINIVASULU", "0089": "M.RAMADEVI",
    "0090": "B.MURALI", "0091": "S.CHANDRAIAH", "0092": "S.SABEEN TAJ",
    "0048": "P.LAKSHMAMMA", "0049": "V.RANI", "0050": "K.PEDDAMMA",
    "0051": "C.VENKATA SUBBA REDDY", "0052": "S.NAGARJUNA", "0055": "E.CHANDRAIAH",
    "0057": "S.KASAMMA", "0059": "K.NARASIMHA", "0070": "K.NARAYANA",
    "0069": "K.NARASIMHULU", "0068": "K.RAJAMMA", "0067": "P.CHANDRAIAH",
    "0066": "M.RAJAMMA", "0060": "P.BHARATHAMMA", "0061": "V.VENKATA RAMANA",
    "0062": "P.BHARATHAMMA", "0064": "V.PADMAVATHI", "0063": "V.PADMAVATHI",
    "1664": "G.RAMADEVI", "1651": "P.GIRI BABU", "1740": "G.SUBRAMANYAM",
    "1718": "M.BABU", "1542": "S.BABU", "1937": "SREENIVASULU",
    "1993": "J.CHANDRAMMA", "1959": "A.CHANDRAMMA", "1812": "S.BHARATHI",
    "1781": "A.RAMADEVI", "1773": "P.SYAMALAMMA", "1770": "M.DEVAMMA",
    "1868": "T.LAKSHMINARI", "1824": "P.BHARATHAMMA", "0884": "M.DEVAMMA",
    "0881": "M.DEVASENEV", "0880": "M.LAKSHMINARIMMA", "0878": "M.LAKSHMINARIMMA",
    "0876": "N.NAGARATHNAM", "0874": "N.VENKATARAMANA", "0871": "C.RAMADEVI",
    "0868": "M.LAKSHMINARIMMA", "0863": "G.PEDDAIAH", "0906": "K.GANGAMMA",
    "0900": "R.SATYAMMA", "0895": "V.PADMAVATHI", "0893": "G.BALAKRISHNA",
    "0888": "C.RAMADEVI", "0887": "K.GANGAMMA", "0830": "K.ESWARAMMA",
    "0826": "G.NARASIMHULU", "0824": "M.VENKATAIAH", "0859": "G.NARASIMHULU",
    "0851": "K.KRISHNA REDDY", "0848": "G.CHANDRAIAH", "0846": "V.GANGAMMA",
    "0842": "K.SWARNAMMA", "0839": "B.SATYAMMA", "1058": "P.RAMADEVI",
    "1057": "K.RAMANAIAH", "1052": "P.RAMADEVI", "1017": "N.NARAYANAMMA",
    "1003": "N.PEDDI REDDY", "1272": "G.PEDDI REDDY", "1240": "K.PEDDI REDDY",
    "0916": "M.KRISHNAMA NAIDU", "0915": "S.BALAKRISHNA REDDY", "0982": "C.MUNIREDDY",
    "2388": "G.PEDDI REDDY", "2380": "K.MUNIREDDY", "2374": "N.RAJAGOPAL",
    "2437": "M.ADILAKSHMI", "2421": "M.MUNIREDDY", "2314": "K.CHANDRAIAH",
    "2338": "A.CHANDRAMMA", "2500": "T.VENKATAIAH", "2530": "A.RAMADEVI",
    "2528": "M.SUBRAMANYAM", "2526": "A.GANGAMMA", "2463": "B.BUMMAIAHGARIPALLE",
    "2444": "C.RAMADEVI", "2440": "B.SWARNAMMA",
    "2013": "THOTIMALAPALLE",
    "2083": "RAJUVARIPALLI H/W", "2045": "RAJUVARIPALLI", "2288": "RAJUVARIPALLI",
    "2272": "THATIGUNTAPALEM", "2186": "KANTAMVARIPALLE", "2183": "REGALLU",
    "2178": "SANKENIGUTTAPALLE", "2173": "MUNELLAPALLE", "2160": "V.K.THURPUPALLE",
    "2228": "GAJULAVARIPALLI", "0296": "BESTAPALLE",
    "0335": "MATLOLLPALLAI", "0326": "LOKAVARIPALLE", "0256": "VOOTUPALLE", "0245": "BETAPALLE",
    "0237": "BATTUVARIPALLE", "0417": "ROMPICHERLA", "0414": "BODIPATIVARIPALLE",
    "0441": "BODIPATIVARIPALLE", "0440": "VARANASIVARIPALLE",
    "0360":"CHICHILIVARIPALLE",
    "0357":"AKKISANIVARIPALLE", "0394":"SETTIPALLEVANDLAPALLE", "0072":"VAGALLA",
    "0056":"LEMATIVARIPALLE", "0108":"KONDAREDDIGARIPALLE","0016":"ROMPICHERLA",
    "0030":"MELLAVARIPALLE", "0197":"BASIREDDIGARIPALLE", "0173":"MORAVAPALLE",
    "0221":"KURABAPALLE", "0130":"PATHAKURVAPALLE", "0165":"AGRAHARAM",
    "0151":"BONAMVARIPALLE", "0649":"PILER", "0645":"NADIMPALLE",
    "0643":"SAVVALAVARIPALLE", "0636":"KURAPATHIVARIPALLE", "0689":"VANKAVODDIPALLE",
    "0688":"BADDALAVARIPALLI H.W.","0685":"NAGARIMADUGUVARIPALLE", "0668":"KANDUR",
    "0663":"DEVALAVARIPALLE", "0585":"SRIVARAMPURAM", "0575":"RAMREDDIGARIPALLE",
    "0572":"LOKAVARIPALLE", "0613":"NAGAVANDLAPALLI", "0611":"BODIPATIVARIPALLE",
    "0610":"ROMPICHERLA", "0604":"NAGAVANDLAPALLI", "0782":"CHICHILIVARIPALLE",
    "0770":"DEVALAVARIPALLE", "0767":"PEDDAGOTTIGALLU", "0764":"K.V.PALLE",
    "0762":"JAGADAMVARIPALLE", "0753":"BOLLINANIVARIPALLI", "0813":"ROMPICHERLA",
    "0811":"ALAKAMVARIPALLE", "0809":"KOTAKADAPALLE", "0794":"PEDDAGOTTIGALLU",
    "0793":"DIGUVAJUPALLI", "0789":"SODUM", "0788":"BURUJUPALLE",
    "0786":"PEDDAGOTTIGALLU CROSS", "0719":"NADIMPALLE", "0718":"PEDDAGOTTIGALLU",
    "0714":"BODIPATIVARIPALLE", "0709":"REDDIVARIPALLE", "0700":"RAMIREDDIGARIPALLE",
    "0721":"SODUM", "0747":"KURAVAPALLE", "0745":"ETUKURIVARIPALLE",
    "0743":"ROMPICHERLA", "0736":"VOOTUPALLE", "0732":"ROMPICHERLA",
    "0727":"DUSSAVANDLA PALLI", "0726":"SAVVALAVARIPALLE", "0508":"MUREVANDLAPALLE",
    "0490":"MATAMPALLE", "0551":"TALUPULA", "0512":"BONAMVARIPALLE",
    "0473":"KURAVAPALLE", "0477":"VARANASIVARIPALLE"
]


# Extracted Farmer Names and Member Codes from the image
FARMER_DATA = {
    "0005": "GUBBALA ANAMMA", "0003": "G.REDDY SEKHAR",
    "0012":"V. Devaki", "0008": "D. PRASAD REDDY", "0006":"G.Ratnamma",
    "0013": "M.GANGULU", "0014": "K VARADHA NAIDU", "0007": "INDRAVATHI RAMADEVI",
    "0017": "B SAMPURNA", "0015": "J.GANGULU", "0002": "KRISHNAMA NAIDU",
    "0021": "M.S.CHOWDARY", "0029": "DASARI VENKATAIAH", "0030": "K.M.KANTHAMMA",
    "0036": "D.BALAKRISHNA", "0037": "C.SURYA PRAKASH", "0039": "D.CHANDRAMMA",
    "0041": "G.NARASIMHA NAIDU", "0043": "REDDI RAMADEVI", "0044": "D.CHANDRAMMA",
    "0045": "S.PEDDAIAH", "0046": "D.PEDDAIAH", "0047": "K.K.KADIRAMMA",
    "0001": "M.NARAYANAMMA", "0002": "S.K.SUBBAIAH", "0004": "C.M.NARAYANA",
    "0005": "D.MALLAIAH", "0006": "G.CHANDRAIAH", "0008": "J.RAMADEVI",
    "0009": "G.SWARNAMMA", "0011": "J.ESWARAMMA", "0013": "K.GURAVAIAH",
    "0014": "P.DEVAKI DEVI", "0015": "K.NARASIMHULU", "0016": "P REDDY PRASAD",
    "0018": "D.DEVAKI RAMADEVI", "0019": "P.SATYAMMA", "0020": "B.SAMPURNA",
    "0021": "P.PEDDAIAH", "0022": "REDDISEKHAR", "0023": "V.SUBRAMANYAM",
    "0071": "V.REDDY RANI", "0072": "B.GANGULU", "0074": "K.YASHODHA",
    "0075": "D.RAMADEVI", "0076": "H.RAMADEVI", "0077": "R.RAMADEVI",
    "0078": "B.RANI", "0079": "K.VENKATAIAH", "0080": "P.SREERAM REDDY",
    "0081": "M.RAMADEVI", "0082": "M.PENCHALAMAIAH", "0083": "M.M.RATHNAMMA",
    "0084": "N.GANGULU", "0085": "N.RAMALINGAM", "0086": "N.RAMADEVI",
    "0087": "V.CHANDRAIAH", "0088": "N.SRINIVASULU", "0089": "M.RAMADEVI",
    "0090": "B.MURALI", "0091": "S.CHANDRAIAH", "0092": "S.SABEEN TAJ",
    "0048": "P.LAKSHMAMMA", "0049": "V.RANI", "0050": "K.PEDDAMMA",
    "0051": "C.VENKATA SUBBA REDDY", "0052": "S.NAGARJUNA", "0055": "E.CHANDRAIAH",
    "0057": "S.KASAMMA", "0059": "K.NARASIMHA", "0070": "K.NARAYANA",
    "0069": "K.NARASIMHULU", "0068": "K.RAJAMMA", "0067": "P.CHANDRAIAH",
    "0066": "M.RAJAMMA", "0060": "P.BHARATHAMMA", "0061": "V.VENKATA RAMANA",
    "0062": "P.BHARATHAMMA", "0064": "V.PADMAVATHI", "0063": "V.PADMAVATHI",
    "1664": "G.RAMADEVI", "1651": "P.GIRI BABU", "1740": "G.SUBRAMANYAM",
    "1718": "M.BABU", "1542": "S.BABU", "1937": "SREENIVASULU",
    "1993": "J.CHANDRAMMA", "1959": "A.CHANDRAMMA", "1812": "S.BHARATHI",
    "1781": "A.RAMADEVI", "1773": "P.SYAMALAMMA", "1770": "M.DEVAMMA",
    "1868": "T.LAKSHMINARI", "1824": "P.BHARATHAMMA", "0884": "M.DEVAMMA",
    "0881": "M.DEVASENEV", "0880": "M.LAKSHMINARIMMA", "0878": "M.LAKSHMINARIMMA",
    "0876": "N.NAGARATHNAM", "0874": "N.VENKATARAMANA", "0871": "C.RAMADEVI",
    "0868": "M.LAKSHMINARIMMA", "0863": "G.PEDDAIAH", "0906": "K.GANGAMMA",
    "0900": "R.SATYAMMA", "0895": "V.PADMAVATHI", "0893": "G.BALAKRISHNA",
    "0888": "C.RAMADEVI", "0887": "K.GANGAMMA", "0830": "K.ESWARAMMA",
    "0826": "G.NARASIMHULU", "0824": "M.VENKATAIAH", "0859": "G.NARASIMHULU",
    "0851": "K.KRISHNA REDDY", "0848": "G.CHANDRAIAH", "0846": "V.GANGAMMA",
    "0842": "K.SWARNAMMA", "0839": "B.SATYAMMA", "1058": "P.RAMADEVI",
    "1057": "K.RAMANAIAH", "1052": "P.RAMADEVI", "1017": "N.NARAYANAMMA",
    "1003": "N.PEDDI REDDY", "1272": "G.PEDDI REDDY", "1240": "K.PEDDI REDDY",
    "0916": "M.KRISHNAMA NAIDU", "0915": "S.BALAKRISHNA REDDY", "0982": "C.MUNIREDDY",
    "2388": "G.PEDDI REDDY", "2380": "K.MUNIREDDY", "2374": "N.RAJAGOPAL",
    "2437": "M.ADILAKSHMI", "2421": "M.MUNIREDDY", "2314": "K.CHANDRAIAH",
    "2338": "A.CHANDRAMMA", "2500": "T.VENKATAIAH", "2530": "A.RAMADEVI",
    "2528": "M.SUBRAMANYAM", "2526": "A.GANGAMMA", "2463": "B.BUMMAIAHGARIPALLE",
    "2444": "C.RAMADEVI", "2440": "B.SWARNAMMA",
    "2013": "THOTIMALAPALLE",
    "2083": "RAJUVARIPALLI H/W", "2045": "RAJUVARIPALLI", "2288": "RAJUVARIPALLI",
    "2272": "THATIGUNTAPALEM", "2186": "KANTAMVARIPALLE", "2183": "REGALLU",
    "2178": "SANKENIGUTTAPALLE", "2173": "MUNELLAPALLE", "2160": "V.K.THURPUPALLE",
    "2228": "GAJULAVARIPALLI", "0296": "BESTAPALLE",
    "0335": "MATLOLLPALLAI", "0326": "LOKAVARIPALLE", "0256": "VOOTUPALLE", "0245": "BETAPALLE",
    "0237": "BATTUVARIPALLE", "0417": "ROMPICHERLA", "0414": "BODIPATIVARIPALLE",
    "0441": "BODIPATIVARIPALLE", "0440": "VARANASIVARIPALLE",
    "0360":"CHICHILIVARIPALLE",
    "0357":"AKKISANIVARIPALLE", "0394":"SETTIPALLEVANDLAPALLE", "0072":"VAGALLA",
    "0056":"LEMATIVARIPALLE", "0108":"KONDAREDDIGARIPALLE","0016":"ROMPICHERLA",
    "0030":"MELLAVARIPALLE", "0197":"BASIREDDIGARIPALLE", "0173":"MORAVAPALLE",
    "0221":"KURABAPALLE", "0130":"PATHAKURVAPALLE", "0165":"AGRAHARAM",
    "0151":"BONAMVARIPALLE", "0649":"PILER", "0645":"NADIMPALLE",
    "0643":"SAVVALAVARIPALLE", "0636":"KURAPATHIVARIPALLE", "0689":"VANKAVODDIPALLE",
    "0688":"BADDALAVARIPALLI H.W.","0685":"NAGARIMADUGUVARIPALLE", "0668":"KANDUR",
    "0663":"DEVALAVARIPALLE", "0585":"SRIVARAMPURAM", "0575":"RAMREDDIGARIPALLE",
    "0572":"LOKAVARIPALLE", "0613":"NAGAVANDLAPALLI", "0611":"BODIPATIVARIPALLE",
    "0610":"ROMPICHERLA", "0604":"NAGAVANDLAPALLI", "0782":"CHICHILIVARIPALLE",
    "0770":"DEVALAVARIPALLE", "0767":"PEDDAGOTTIGALLU", "0764":"K.V.PALLE",
    "0762":"JAGADAMVARIPALLE", "0753":"BOLLINANIVARIPALLI", "0813":"ROMPICHERLA",
    "0811":"ALAKAMVARIPALLE", "0809":"KOTAKADAPALLE", "0794":"PEDDAGOTTIGALLU",
    "0793":"DIGUVAJUPALLI", "0789":"SODUM", "0788":"BURUJUPALLE",
    "0786":"PEDDAGOTTIGALLU CROSS", "0719":"NADIMPALLE", "0718":"PEDDAGOTTIGALLU",
    "0714":"BODIPATIVARIPALLE", "0709":"REDDIVARIPALLE", "0700":"RAMIREDDIGARIPALLE",
    "0721":"SODUM", "0747":"KURAVAPALLE", "0745":"ETUKURIVARIPALLE",
    "0743":"ROMPICHERLA", "0736":"VOOTUPALLE", "0732":"ROMPICHERLA",
    "0727":"DUSSAVANDLA PALLI", "0726":"SAVVALAVARIPALLE", "0508":"MUREVANDLAPALLE",
    "0490":"MATAMPALLE", "0551":"TALUPULA", "0512":"BONAMVARIPALLE",
    "0473":"KURAVAPALLE", "0477":"VARANASIVARIPALLE"
}


# Extracted Farmer Names and Member Codes from the image
FARMER_DATA = {
    "0005": "GUBBALA ANAMMA", "0003": "G.REDDY SEKHAR",
    "0012":"V. Devaki", "0008": "D. PRASAD REDDY", "0006":"G.Ratnamma",
    "0013": "M.GANGULU", "0014": "K VARADHA NAIDU", "0007": "INDRAVATHI RAMADEVI",
    "0017": "B SAMPURNA", "0015": "J.GANGULU", "0002": "KRISHNAMA NAIDU",
    "0021": "M.S.CHOWDARY", "0029": "DASARI VENKATAIAH", "0030": "K.M.KANTHAMMA",
    "0036": "D.BALAKRISHNA", "0037": "C.SURYA PRAKASH", "0039": "D.CHANDRAMMA",
    "0041": "G.NARASIMHA NAIDU", "0043": "REDDI RAMADEVI", "0044": "D.CHANDRAMMA",
    "0045": "S.PEDDAIAH", "0046": "D.PEDDAIAH", "0047": "K.K.KADIRAMMA",
    "0001": "M.NARAYANAMMA", "0002": "S.K.SUBBAIAH", "0004": "C.M.NARAYANA",
    "0005": "D.MALLAIAH", "0006": "G.CHANDRAIAH", "0008": "J.RAMADEVI",
    "0009": "G.SWARNAMMA", "0011": "J.ESWARAMMA", "0013": "K.GURAVAIAH",
    "0014": "P.DEVAKI DEVI", "0015": "K.NARASIMHULU", "0016": "P REDDY PRASAD",
    "0018": "D.DEVAKI RAMADEVI", "0019": "P.SATYAMMA", "0020": "B.SAMPURNA",
    "0021": "P.PEDDAIAH", "0022": "REDDISEKHAR", "0023": "V.SUBRAMANYAM",
    "0071": "V.REDDY RANI", "0072": "B.GANGULU", "0074": "K.YASHODHA",
    "0075": "D.RAMADEVI", "0076": "H.RAMADEVI", "0077": "R.RAMADEVI",
    "0078": "B.RANI", "0079": "K.VENKATAIAH", "0080": "P.SREERAM REDDY",
    "0081": "M.RAMADEVI", "0082": "M.PENCHALAMAIAH", "0083": "M.M.RATHNAMMA",
    "0084": "N.GANGULU", "0085": "N.RAMALINGAM", "0086": "N.RAMADEVI",
    "0087": "V.CHANDRAIAH", "0088": "N.SRINIVASULU", "0089": "M.RAMADEVI",
    "0090": "B.MURALI", "0091": "S.CHANDRAIAH", "0092": "S.SABEEN TAJ",
    "0048": "P.LAKSHMAMMA", "0049": "V.RANI", "0050": "K.PEDDAMMA",
    "0051": "C.VENKATA SUBBA REDDY", "0052": "S.NAGARJUNA", "0055": "E.CHANDRAIAH",
    "0057": "S.KASAMMA", "0059": "K.NARASIMHA", "0070": "K.NARAYANA",
    "0069": "K.NARASIMHULU", "0068": "K.RAJAMMA", "0067": "P.CHANDRAIAH",
    "0066": "M.RAJAMMA", "0060": "P.BHARATHAMMA", "0061": "V.VENKATA RAMANA",
    "0062": "P.BHARATHAMMA", "0064": "V.PADMAVATHI", "0063": "V.PADMAVATHI",
    "1664": "G.RAMADEVI", "1651": "P.GIRI BABU", "1740": "G.SUBRAMANYAM",
    "1718": "M.BABU", "1542": "S.BABU", "1937": "SREENIVASULU",
    "1993": "J.CHANDRAMMA", "1959": "A.CHANDRAMMA", "1812": "S.BHARATHI",
    "1781": "A.RAMADEVI", "1773": "P.SYAMALAMMA", "1770": "M.DEVAMMA",
    "1868": "T.LAKSHMINARI", "1824": "P.BHARATHAMMA", "0884": "M.DEVAMMA",
    "0881": "M.DEVASENEV", "0880": "M.LAKSHMINARIMMA", "0878": "M.LAKSHMINARIMMA",
    "0876": "N.NAGARATHNAM", "0874": "N.VENKATARAMANA", "0871": "C.RAMADEVI",
    "0868": "M.LAKSHMINARIMMA", "0863": "G.PEDDAIAH", "0906": "K.GANGAMMA",
    "0900": "R.SATYAMMA", "0895": "V.PADMAVATHI", "0893": "G.BALAKRISHNA",
    "0888": "C.RAMADEVI", "0887": "K.GANGAMMA", "0830": "K.ESWARAMMA",
    "0826": "G.NARASIMHULU", "0824": "M.VENKATAIAH", "0859": "G.NARASIMHULU",
    "0851": "K.KRISHNA REDDY", "0848": "G.CHANDRAIAH", "0846": "V.GANGAMMA",
    "0842": "K.SWARNAMMA", "0839": "B.SATYAMMA", "1058": "P.RAMADEVI",
    "1057": "K.RAMANAIAH", "1052": "P.RAMADEVI", "1017": "N.NARAYANAMMA",
    "1003": "N.PEDDI REDDY", "1272": "G.PEDDI REDDY", "1240": "K.PEDDI REDDY",
    "0916": "M.KRISHNAMA NAIDU", "0915": "S.BALAKRISHNA REDDY", "0982": "C.MUNIREDDY",
    "2388": "G.PEDDI REDDY", "2380": "K.MUNIREDDY", "2374": "N.RAJAGOPAL",
    "2437": "M.ADILAKSHMI", "2421": "M.MUNIREDDY", "2314": "K.CHANDRAIAH",
    "2338": "A.CHANDRAMMA", "2500": "T.VENKATAIAH", "2530": "A.RAMADEVI",
    "2528": "M.SUBRAMANYAM", "2526": "A.GANGAMMA", "2463": "B.BUMMAIAHGARIPALLE",
    "2444": "C.RAMADEVI", "2440": "B.SWARNAMMA",
    "2013": "THOTIMALAPALLE",
    "2083": "RAJUVARIPALLI H/W", "2045": "RAJUVARIPALLI", "2288": "RAJUVARIPALLI",
    "2272": "THATIGUNTAPALEM", "2186": "KANTAMVARIPALLE", "2183": "REGALLU",
    "2178": "SANKENIGUTTAPALLE", "2173": "MUNELLAPALLE", "2160": "V.K.THURPUPALLE",
    "2228": "GAJULAVARIPALLI", "0296": "BESTAPALLE",
    "0335": "MATLOLLPALLAI", "0326": "LOKAVARIPALLE", "0256": "VOOTUPALLE", "0245": "BETAPALLE",
    "0237": "BATTUVARIPALLE", "0417": "ROMPICHERLA", "0414": "BODIPATIVARIPALLE",
    "0441": "BODIPATIVARIPALLE", "0440": "VARANASIVARIPALLE",
    "0360":"CHICHILIVARIPALLE",
    "0357":"AKKISANIVARIPALLE", "0394":"SETTIPALLEVANDLAPALLE", "0072":"VAGALLA",
    "0056":"LEMATIVARIPALLE", "0108":"KONDAREDDIGARIPALLE","0016":"ROMPICHERLA",
    "0030":"MELLAVARIPALLE", "0197":"BASIREDDIGARIPALLE", "0173":"MORAVAPALLE",
    "0221":"KURABAPALLE", "0130":"PATHAKURVAPALLE", "0165":"AGRAHARAM",
    "0151":"BONAMVARIPALLE", "0649":"PILER", "0645":"NADIMPALLE",
    "0643":"SAVVALAVARIPALLE", "0636":"KURAPATHIVARIPALLE", "0689":"VANKAVODDIPALLE",
    "0688":"BADDALAVARIPALLI H.W.","0685":"NAGARIMADUGUVARIPALLE", "0668":"KANDUR",
    "0663":"DEVALAVARIPALLE", "0585":"SRIVARAMPURAM", "0575":"RAMREDDIGARIPALLE",
    "0572":"LOKAVARIPALLE", "0613":"NAGAVANDLAPALLI", "0611":"BODIPATIVARIPALLE",
    "0610":"ROMPICHERLA", "0604":"NAGAVANDLAPALLI", "0782":"CHICHILIVARIPALLE",
    "0770":"DEVALAVARIPALLE", "0767":"PEDDAGOTTIGALLU", "0764":"K.V.PALLE",
    "0762":"JAGADAMVARIPALLE", "0753":"BOLLINANIVARIPALLI", "0813":"ROMPICHERLA",
    "0811":"ALAKAMVARIPALLE", "0809":"KOTAKADAPALLE", "0794":"PEDDAGOTTIGALLU",
    "0793":"DIGUVAJUPALLI", "0789":"SODUM", "0788":"BURUJUPALLE",
    "0786":"PEDDAGOTTIGALLU CROSS", "0719":"NADIMPALLE", "0718":"PEDDAGOTTIGALLU",
    "0714":"BODIPATIVARIPALLE", "0709":"REDDIVARIPALLE", "0700":"RAMIREDDIGARIPALLE",
    "0721":"SODUM", "0747":"KURAVAPALLE", "0745":"ETUKURIVARIPALLE",
    "0743":"ROMPICHERLA", "0736":"VOOTUPALLE", "0732":"ROMPICHERLA",
    "0727":"DUSSAVANDLA PALLI", "0726":"SAVVALAVARIPALLE", "0508":"MUREVANDLAPALLE",
    "0490":"MATAMPALLE", "0551":"TALUPULA", "0512":"BONAMVARIPALLE",
    "0473":"KURAVAPALLE", "0477":"VARANASIVARIPALLE"
}


# Create lists for dropdowns
FARMER_CODES = sorted(list(FARMER_DATA.keys()))
FARMER_NAMES_RAW = sorted(list(FARMER_DATA.values()))
FARMER_NAMES_WITH_OTHER = sorted(FARMER_NAMES_RAW + ["Other (Specify)"])

GREEN_FODDER_OPTIONS = ["Napier", "Maize", "Sorghum"]
DRY_FODDER_OPTIONS = ["Paddy Straw", "Maize Straw", "Ragi Straw", "Ground Nut Crop Residues"]
PELLET_FEED_BRANDS_RAW = ["Heritage Milk Rich", "Heritage Milk Joy", "Heritage Power Plus", "Kamadhenu", "Godrej", "Sreeja", "Vallabha-Panchamruth", "Vallabha-Subham Pusti"]
PELLET_FEED_BRANDS = sorted(PELLET_FEED_BRANDS_RAW + ["Other (Specify)"])
MINERAL_MIXTURE_BRANDS_RAW = ["Herita Vit", "Herita Min"]
MINERAL_MIXTURE_BRANDS = sorted(MINERAL_MIXTURE_BRANDS_RAW + ["Other (Specify)"])
WATER_SOURCE_OPTIONS = ["Panchayat", "Borewell", "Water Streams", "Other (Specify)"]
SURVEYOR_NAMES_RAW = ["Shiva Shankaraiah", "Reddisekhar", "Balakrishna", "Somasekhar", "Mahesh Kumar", "Dr Swaran Raj Nayak", "Ram Prasad", "K Balaji"]
SURVEYOR_NAMES = sorted(SURVEYOR_NAMES_RAW + ["Other (Specify)"])

VLCC_NAMES_WITH_OTHER = sorted(VLCC_NAMES + ["Other (Specify)"])
# -----------------------------

# Define initial_values_defaults at the global scope, before any functions use it
initial_values_defaults = {
    'lang_select': "English",
    'vlcc_name': VLCC_NAMES_WITH_OTHER[0] if VLCC_NAMES_WITH_OTHER else None,
    'vlcc_name_specify': '', 
    'hpc_code': '',
    'types': "HPC",
    'farmer_name': FARMER_NAMES_WITH_OTHER[0] if FARMER_NAMES_WITH_OTHER else None,
    'other_farmer_name_specify': '', 
    'farmer_code': FARMER_CODES[0] if FARMER_CODES else None,
    'gender': "Male",
    'cows': 0,
    'cattle_in_milk': 0,
    'calves': 0,
    'desi_cows': 0,
    'crossbreed_cows': 0,
    'buffalo': 0,
    'milk_production': 0.0,
    'green_fodder': "Yes",
    'green_fodder_types': [],
    'green_fodder_qty': 0.0,
    'dry_fodder': "Yes",
    'dry_fodder_types': [],
    'dry_fodder_qty': 0.0,
    'pellet_feed': "Yes",
    'pellet_feed_brands': [],
    'pellet_feed_brands_specify': '', 
    'mineral_mixture': "Yes",
    'mineral_brand': MINERAL_MIXTURE_BRANDS[0] if MINERAL_MIXTURE_BRANDS else None,
    'mineral_brand_specify': '', 
    'mineral_qty': 0.0,
    'silage': "Yes",
    'silage_source': '',
    'silage_qty': 0.0,
    'water_sources': [],
    'water_sources_specify': '', 
    'surveyor_name': SURVEYOR_NAMES[0] if SURVEYOR_NAMES else None,
    'surveyor_name_specify': '', 
    'visit_date': datetime.date.today()
}

# Function to save current form data to a draft file
def save_draft():
    draft_filename = os.path.join(DRAFT_DIR, "current_draft.json")

    keys_to_save = list(initial_values_defaults.keys()) + ['other_farmer_name_specify', 'vlcc_name_specify', 'pellet_feed_brands_specify', 'mineral_brand_specify', 'water_sources_specify', 'surveyor_name_specify']
    draft_data = {key: st.session_state[key] for key in keys_to_save if key in st.session_state}

    if 'visit_date' in draft_data and isinstance(draft_data['visit_date'], datetime.date):
        draft_data['visit_date'] = draft_data['visit_date'].isoformat()

    try:
        with open(draft_filename, 'w') as f:
            json.dump(draft_data, f, indent=4)
        st.session_state.last_saved_time_persistent = datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        st.error(f"Error saving draft: {e}")

# Function to load draft data into session state
def load_draft():
    draft_filename = os.path.join(DRAFT_DIR, "current_draft.json")
    if os.path.exists(draft_filename):
        try:
            with open(draft_filename, 'r') as f:
                loaded_data = json.load(f)

            for key, value in loaded_data.items():
                if key == 'visit_date' and isinstance(value, str):
                    try:
                        st.session_state[key] = datetime.date.fromisoformat(value)
                    except ValueError:
                        st.session_state[key] = initial_values_defaults.get(key, datetime.date.today())
                elif key in ['green_fodder_types', 'dry_fodder_types', 'pellet_feed_brands', 'water_sources']:
                    st.session_state[key] = list(value) if isinstance(value, list) else []
                else:
                    st.session_state[key] = value

            current_labels = dict_translations.get(st.session_state.get('lang_select', 'English'), dict_translations['English'])

            if 'types' in st.session_state and st.session_state['types'] not in (current_labels['HPC'], current_labels['MCC']):
                st.session_state['types'] = current_labels['HPC']
            if 'gender' in st.session_state and st.session_state['gender'] not in (current_labels['Male'], current_labels['Female']):
                st.session_state['gender'] = current_labels['Male']
            if 'green_fodder' in st.session_state and st.session_state['green_fodder'] not in (current_labels['Yes'], current_labels['No']):
                st.session_state['green_fodder'] = current_labels['Yes']
            if 'dry_fodder' in st.session_state and st.session_state['dry_fodder'] not in (current_labels['Yes'], current_labels['No']):
                st.session_state['dry_fodder'] = current_labels['Yes']
            if 'pellet_feed' in st.session_state and st.session_state['pellet_feed'] not in (current_labels['Yes'], current_labels['No']):
                st.session_state['pellet_feed'] = current_labels['Yes']
            if 'mineral_mixture' in st.session_state and st.session_state['mineral_mixture'] not in (current_labels['Yes'], current_labels['No']):
                st.session_state['mineral_mixture'] = current_labels['Yes']
            if 'silage' in st.session_state and st.session_state['silage'] not in (current_labels['Yes'], current_labels['No']):
                st.session_state['silage'] = current_labels['Yes']

            st.toast("Draft loaded successfully!")
            return True
        except Exception as e:
            st.error(f"Error loading draft: {e}. Please try clearing local storage or starting a new draft.")
            return False
    return False

# Initialize session state with default values, or load from draft
if st.session_state.get('app_initialized_flag', False) is False:
    st.session_state.app_initialized_flag = True

    st.session_state.last_saved_time_persistent = None

    loaded_a_draft = load_draft()

    if not loaded_a_draft:
        for key, default_value in initial_values_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

# Language Selection
initial_lang_options = ("English", "Hindi", "Marathi")
initial_lang_index = initial_lang_options.index(st.session_state.lang_select) if st.session_state.lang_select in initial_lang_options else 0
lang = st.selectbox(
    "Language / भाषा / भाषा",
    initial_lang_options,
    index=initial_lang_index,
    key="lang_select",
)
labels = dict_translations.get(lang, dict_translations['English'])

st.title(labels['Farmer Profile'])

if st.session_state.last_saved_time_persistent:
    st.info(f"{labels['Auto-saved!']} Last saved: {st.session_state.last_saved_time_persistent}")
else:
    st.info("No auto-saved draft found, or draft cleared. Start filling the form!")


# Form Start
with st.form("survey_form"):
    st.header(labels['Farmer Profile'])

    # VLCC Name (with Other Specify)
    vlcc_name_default_idx = 0
    if st.session_state.vlcc_name in VLCC_NAMES_WITH_OTHER:
        vlcc_name_default_idx = VLCC_NAMES_WITH_OTHER.index(st.session_state.vlcc_name)
    elif VLCC_NAMES_WITH_OTHER:
        st.session_state.vlcc_name = VLCC_NAMES_WITH_OTHER[0]
    else:
        st.session_state.vlcc_name = None

    vlcc_name = st.selectbox(
        labels['VLCC Name'], VLCC_NAMES_WITH_OTHER,
        index=vlcc_name_default_idx,
        key="vlcc_name",
        disabled=(not VLCC_NAMES_WITH_OTHER)
    )

    # Conditional text input for Other VLCC Name
    if vlcc_name == labels['Other (Specify)']:
        st.text_input(
            labels['Other VLCC Name'],
            value=st.session_state.vlcc_name_specify,
            key="vlcc_name_specify"
        )
    else:
        if 'vlcc_name_specify' in st.session_state:
            st.session_state.vlcc_name_specify = ''


    # HPC/MCC Code
    hpc_code = st.text_input(
        labels['HPC/MCC Code'],
        value=st.session_state.hpc_code,
        key="hpc_code"
    )

    # Types
    types_options = (labels['HPC'], labels['MCC'])
    types_default_idx = types_options.index(st.session_state.types) if st.session_state.types in types_options else 0
    types = st.selectbox(
        labels['Types'], types_options,
        index=types_default_idx,
        key="types"
    )

    # Dropdown for Farmer Name (with Other Specify)
    farmer_name_default_idx = 0
    if st.session_state.farmer_name in FARMER_NAMES_WITH_OTHER:
        farmer_name_default_idx = FARMER_NAMES_WITH_OTHER.index(st.session_state.farmer_name)
    elif FARMER_NAMES_WITH_OTHER:
        st.session_state.farmer_name = FARMER_NAMES_WITH_OTHER[0]
    else:
        st.session_state.farmer_name = None

    farmer_name = st.selectbox(
        labels['Farmer Name'], options=FARMER_NAMES_WITH_OTHER,
        index=farmer_name_default_idx,
        key="farmer_name",
        disabled=(not FARMER_NAMES_WITH_OTHER)
    )

    # Conditional text input for "Other Farmer Name"
    if farmer_name == labels['Other (Specify)']:
        st.text_input(
            labels['Other Farmer Name'],
            value=st.session_state.other_farmer_name_specify,
            key="other_farmer_name_specify"
        )
    else:
        if 'other_farmer_name_specify' in st.session_state:
            st.session_state.other_farmer_name_specify = ''


    # Dropdown for Farmer Code
    farmer_code_default_idx = 0
    if st.session_state.farmer_code in FARMER_CODES:
        farmer_code_default_idx = FARMER_CODES.index(st.session_state.farmer_code)
    elif FARMER_CODES:
        st.session_state.farmer_code = FARMER_CODES[0]
    else:
        st.session_state.farmer_code = None

    farmer_code = st.selectbox(
        labels['Farmer Code'], options=FARMER_CODES,
        index=farmer_code_default_idx,
        key="farmer_code",
        disabled=(not FARMER_CODES)
    )

    # Gender
    gender_options = (labels['Male'], labels['Female'])
    gender_default_idx = gender_options.index(st.session_state.gender) if st.session_state.gender in gender_options else 0
    gender = st.selectbox(
        labels['Gender'], gender_options,
        index=gender_default_idx,
        key="gender"
    )

    st.header(labels['Farm Details'])
    # Number of Cows
    cows = st.number_input(
        labels['Number of Cows'], min_value=0,
        value=int(st.session_state.cows),
        key="cows"
    )
    # No. of Cattle in Milk
    cattle_in_milk = st.number_input(
        labels['No. of Cattle in Milk'], min_value=0,
        value=int(st.session_state.cattle_in_milk),
        key="cattle_in_milk"
    )
    # No. of Calves/Heifers
    calves = st.number_input(
        labels['No. of Calves/Heifers'], min_value=0,
        value=int(st.session_state.calves),
        key="calves"
    )
    # No. of Desi cows
    desi_cows = st.number_input(
        labels['No. of Desi cows'], min_value=0,
        value=int(st.session_state.desi_cows),
        key="desi_cows"
    )
    # No. of Cross breed cows
    crossbreed_cows = st.number_input(
        labels['No. of Cross breed cows'], min_value=0,
        value=int(st.session_state.crossbreed_cows),
        key="crossbreed_cows"
    )
    # No. of Buffalo
    buffalo = st.number_input(
        labels['No. of Buffalo'], min_value=0,
        value=int(st.session_state.buffalo),
        key="buffalo"
    )
    # Milk Production
    milk_production = st.number_input(
        labels['Milk Production'], min_value=0.0,
        value=float(st.session_state.milk_production),
        key="milk_production"
    )

    st.header(labels['Specific Questions'])
    # Green Fodder
    green_fodder_options = (labels['Yes'], labels['No'])
    green_fodder_default_idx = green_fodder_options.index(st.session_state.green_fodder) if st.session_state.green_fodder in green_fodder_options else 0
    green_fodder = st.selectbox(
        labels['Green Fodder'], green_fodder_options,
        index=green_fodder_default_idx,
        key="green_fodder"
    )
    # Type of Green Fodder
    green_fodder_types = st.multiselect(
        labels['Type of Green Fodder'], GREEN_FODDER_OPTIONS,
        default=st.session_state.green_fodder_types,
        key="green_fodder_types"
    )
    # Quantity of Green Fodder
    green_fodder_qty = st.number_input(
        labels['Quantity of Green Fodder'], min_value=0.0,
        value=float(st.session_state.green_fodder_qty),
        key="green_fodder_qty"
    )
    # Dry Fodder
    dry_fodder_options = (labels['Yes'], labels['No'])
    dry_fodder_default_idx = dry_fodder_options.index(st.session_state.dry_fodder) if st.session_state.dry_fodder in dry_fodder_options else 0
    dry_fodder = st.selectbox(
        labels['Dry Fodder'], dry_fodder_options,
        index=dry_fodder_default_idx,
        key="dry_fodder"
    )
    # Type of Dry Fodder
    dry_fodder_types = st.multiselect(
        labels['Type of Dry Fodder'], DRY_FODDER_OPTIONS,
        default=st.session_state.dry_fodder_types,
        key="dry_fodder_types"
    )
    # Quantity of Dry Fodder
    dry_fodder_qty = st.number_input(
        labels['Quantity of Dry Fodder'], min_value=0.0,
        value=float(st.session_state.dry_fodder_qty),
        key="dry_fodder_qty"
    )

    # Pellet Feed
    pellet_feed_options = (labels['Yes'], labels['No'])
    pellet_feed_default_idx = pellet_feed_options.index(st.session_state.pellet_feed) if st.session_state.pellet_feed in pellet_feed_options else 0
    pellet_feed = st.selectbox(
        labels['Pellet Feed'], pellet_feed_options,
        index=pellet_feed_default_idx,
        key="pellet_feed"
    )
    # Pellet Feed Brand (Multiselect with Other Specify)
    pellet_feed_brands = st.multiselect(
        labels['Pellet Feed Brand'], PELLET_FEED_BRANDS,
        default=st.session_state.pellet_feed_brands,
        key="pellet_feed_brands"
    )
    # Conditional text input for Other Pellet Brand
    if labels['Other (Specify)'] in pellet_feed_brands:
        st.text_input(
            labels['Other Pellet Brand'],
            value=st.session_state.pellet_feed_brands_specify,
            key="pellet_feed_brands_specify"
        )
    else:
        if 'pellet_feed_brands_specify' in st.session_state:
            st.session_state.pellet_feed_brands_specify = ''


    # Quantity of Pellet Feed
    pellet_feed_qty = st.number_input(
        labels['Quantity of Pellet Feed'], min_value=0.0,
        value=float(st.session_state.pellet_feed_qty),
        key="pellet_feed_qty"
    )

    # Mineral Mixture
    mineral_mixture_options = (labels['Yes'], labels['No'])
    mineral_mixture_default_idx = mineral_mixture_options.index(st.session_state.mineral_mixture) if st.session_state.mineral_mixture in mineral_mixture_options else 0
    mineral_mixture = st.selectbox(
        labels['Mineral Mixture'], mineral_mixture_options,
        index=mineral_mixture_default_idx,
        key="mineral_mixture"
    )
    # Mineral Mixture Brand (Selectbox with Other Specify)
    mineral_brand_default_idx = 0
    if st.session_state.mineral_brand in MINERAL_MIXTURE_BRANDS:
        mineral_brand_default_idx = MINERAL_MIXTURE_BRANDS.index(st.session_state.mineral_brand)
    elif MINERAL_MIXTURE_BRANDS:
        st.session_state.mineral_brand = MINERAL_MIXTURE_BRANDS[0]
    else:
        st.session_state.mineral_brand = None

    mineral_brand = st.selectbox(
        labels['Mineral Mixture Brand'], MINERAL_MIXTURE_BRANDS,
        index=mineral_brand_default_idx,
        key="mineral_brand",
        disabled=(not MINERAL_MIXTURE_BRANDS)
    )

    # Conditional text input for Other Mineral Brand
    if mineral_brand == labels['Other (Specify)']:
        st.text_input(
            labels['Other Mineral Brand'],
            value=st.session_state.mineral_brand_specify,
            key="mineral_brand_specify"
        )
    else:
        if 'mineral_brand_specify' in st.session_state:
            st.session_state.mineral_brand_specify = ''


    # Quantity of Mineral Mixture
    mineral_qty = st.number_input(
        labels['Quantity of Mineral Mixture'], min_value=0.0,
        value=float(st.session_state.mineral_qty),
        key="mineral_qty"
    )

    # Silage
    silage_options = (labels['Yes'], labels['No'])
    silage_default_idx = silage_options.index(st.session_state.silage) if st.session_state.silage in silage_options else 0
    silage = st.selectbox(
        labels['Silage'], silage_options,
        index=silage_default_idx,
        key="silage"
    )
    # Source and Price of Silage
    silage_source = st.text_input(
        labels['Source and Price of Silage'],
        value=st.session_state.silage_source,
        key="silage_source"
    )
    # Quantity of Silage
    silage_qty = st.number_input(
        labels['Quantity of Silage'], min_value=0.0,
        value=float(st.session_state.silage_qty),
        key="silage_qty"
    )

    # Source of Water (Multiselect with Other Specify)
    water_sources = st.multiselect(
        labels['Source of Water'], WATER_SOURCE_OPTIONS,
        default=st.session_state.water_sources,
        key="water_sources"
    )
    # Conditional text input for Other Water Source
    if labels['Other (Specify)'] in water_sources:
        st.text_input(
            labels['Other Water Source'],
            value=st.session_state.water_sources_specify,
            key="water_sources_specify"
        )
    else:
        if 'water_sources_specify' in st.session_state:
            st.session_state.water_sources_specify = ''

    # Name of Surveyor (Selectbox with Other Specify)
    surveyor_name_default_idx = 0
    if st.session_state.surveyor_name in SURVEYOR_NAMES:
        surveyor_name_default_idx = SURVEYOR_NAMES.index(st.session_state.surveyor_name)
    elif SURVEYOR_NAMES:
        st.session_state.surveyor_name = SURVEYOR_NAMES[0]
    else:
        st.session_state.surveyor_name = None

    surveyor_name = st.selectbox(
        labels['Name'], SURVEYOR_NAMES,
        index=surveyor_name_default_idx,
        key="surveyor_name",
        disabled=(not SURVEYOR_NAMES)
    )
    # Conditional text input for Other Surveyor Name
    if surveyor_name == labels['Other (Specify)']:
        st.text_input(
            labels['Other Surveyor Name'],
            value=st.session_state.surveyor_name_specify,
            key="surveyor_name_specify"
        )
    else:
        if 'surveyor_name_specify' in st.session_state:
            st.session_state.surveyor_name_specify = ''


    # Date of Visit
    visit_date = st.date_input(
        labels['Date of Visit'],
        value=st.session_state.visit_date,
        key="visit_date"
    )

    # Photo Upload - placed before submit and uses a unique key
    st.subheader("Upload Farm Photo")
    st.info("Note: Uploaded photos are not auto-saved across sessions/reloads. Please re-upload if you refresh the page before final submission.")
    farm_photo = st.file_uploader("Choose a farm photo (JPG/PNG)", type=["jpg", "jpeg", "png"], key="farm_photo_uploader")

    # The submit button
    submit_button = st.form_submit_button(labels['Submit'])

# Auto-save logic: this runs on every rerun (after any widget interaction)
if st.session_state.app_initialized_flag:
    current_form_values = {key: st.session_state.get(key, initial_values_defaults.get(key)) for key in initial_values_defaults.keys()}
    
    # Include all 'specify' fields in current_form_values for comparison
    for key in ['other_farmer_name_specify', 'vlcc_name_specify', 'pellet_feed_brands_specify', 'mineral_brand_specify', 'water_sources_specify', 'surveyor_name_specify']:
        if key in st.session_state:
            current_form_values[key] = st.session_state[key]
    
    if isinstance(current_form_values.get('visit_date'), datetime.date):
        current_form_values['visit_date'] = current_form_values['visit_date'].isoformat()

    draft_filename = os.path.join(DRAFT_DIR, "current_draft.json")
    last_saved_draft_data = {}
    if os.path.exists(draft_filename):
        try:
            with open(draft_filename, 'r') as f:
                last_saved_draft_data = json.load(f)
            if 'visit_date' in last_saved_draft_data and isinstance(last_saved_draft_data['visit_date'], datetime.date):
                last_saved_draft_data['visit_date'] = last_saved_draft_data['visit_date'].isoformat()
        except Exception:
            last_saved_draft_data = {}

    if current_form_values != last_saved_draft_data:
        save_draft()

# Process submission (this block runs after the form is submitted via submit_button)
if submit_button:
    now = datetime.datetime.now()

    # --- Determine Final Values for Submission ---
    other_specify_label = dict_translations.get(st.session_state.lang_select, dict_translations['English'])['Other (Specify)']

    final_vlcc_name = st.session_state.vlcc_name
    if final_vlcc_name == other_specify_label and st.session_state.vlcc_name_specify:
        final_vlcc_name = st.session_state.vlcc_name_specify
    
    final_farmer_name = st.session_state.farmer_name
    if final_farmer_name == other_specify_label and st.session_state.other_farmer_name_specify:
        final_farmer_name = st.session_state.other_farmer_name_specify

    final_surveyor_name = st.session_state.surveyor_name
    if final_surveyor_name == other_specify_label and st.session_state.surveyor_name_specify:
        final_surveyor_name = st.session_state.surveyor_name_specify
        
    final_mineral_brand = st.session_state.mineral_brand
    if final_mineral_brand == other_specify_label and st.session_state.mineral_brand_specify:
        final_mineral_brand = st.session_state.mineral_brand_specify

    # --- Handle Multiselect + Specify Fields ---
    def process_multiselect_with_other(multiselect_list, specify_field):
        processed_list = list(multiselect_list)
        if other_specify_label in processed_list and specify_field:
            processed_list.remove(other_specify_label)
            processed_list.append(f"Other: {specify_field}")
        return processed_list

    pellet_brands_list = process_multiselect_with_other(st.session_state.pellet_feed_brands, st.session_state.pellet_feed_brands_specify)
    water_sources_list = process_multiselect_with_other(st.session_state.water_sources, st.session_state.water_sources_specify)


    # Collect all data directly from st.session_state which holds the latest values
    data = {
        'Timestamp': now.isoformat(),
        'Language': st.session_state.lang_select,
        'VLCC Name': final_vlcc_name,
        'HPC/MCC Code': st.session_state.hpc_code,
        'Types': st.session_state.types,
        'Farmer Name': final_farmer_name,
        'Farmer Code': st.session_state.farmer_code,
        'Gender': st.session_state.gender,
        'Number of Cows': st.session_state.cows,
        'No. of Cattle in Milk': st.session_state.cattle_in_milk,
        'No. of Calves/Heifers': st.session_state.calves,
        'No. of Desi cows': st.session_state.desi_cows,
        'No. of Cross breed cows': st.session_state.crossbreed_cows,
        'No. of Buffalo': st.session_state.buffalo,
        'Milk Production (liters/day)': st.session_state.milk_production,
        'Green Fodder': st.session_state.green_fodder,
        'Type of Green Fodder': ", ".join(st.session_state.green_fodder_types),
        'Quantity of Green Fodder (Kg/day)': st.session_state.green_fodder_qty,
        'Dry Fodder': st.session_state.dry_fodder,
        'Type of Dry Fodder': ", ".join(st.session_state.dry_fodder_types),
        'Quantity of Dry Fodder (Kg/day)': st.session_state.dry_fodder_qty,
        'Pellet Feed': st.session_state.pellet_feed,
        'Pellet Feed Brand': ", ".join(pellet_brands_list),
        'Quantity of Pellet Feed (Kg/day)': st.session_state.pellet_feed_qty,
        'Mineral Mixture': st.session_state.mineral_mixture,
        'Mineral Mixture Brand': final_mineral_brand,
        'Quantity of Mineral Mixture (gm/day)': st.session_state.mineral_qty,
        'Silage': st.session_state.silage,
        'Source and Price of Silage': st.session_state.silage_source,
        'Quantity of Silage (Kg/day)': st.session_state.silage_qty,
        'Source of Water': ", ".join(water_sources_list),
        'Surveyor Name': final_surveyor_name,
        'Date of Visit': st.session_state.visit_date.isoformat()
    }

    if farm_photo is not None:
        photo_path = os.path.join(SAVE_DIR, f"farm_photo_{now.strftime('%Y%m%d_%H%M%S')}_{farm_photo.name}")
        with open(photo_path, "wb") as f:
            f.write(farm_photo.getbuffer())
        st.success("Farm photo uploaded successfully!")
        data['Farm Photo Filename'] = photo_path
    else:
        data['Farm Photo Filename'] = "No photo uploaded"


    df = pd.DataFrame([data])
    filename = f"survey_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(os.path.join(SAVE_DIR, filename), index=False, encoding='utf-8')
    st.success("📈 Survey Submitted and Saved!")

    # Clear session state data and the draft file after successful submission to clear the form
    for key, default_value in initial_values_defaults.items():
        if key in st.session_state:
            st.session_state[key] = default_value
    st.session_state.last_saved_time_persistent = None

    # Delete the persistent draft file
    draft_filename = os.path.join(DRAFT_DIR, "current_draft.json")
    if os.path.exists(draft_filename):
        os.remove(draft_filename)
        st.info("Draft cleared.")


    with st.expander("🔍 Click to Review Your Submission"):
        for section, keys in {
            "📄 Farmer Profile": [
                'VLCC Name', 'HPC/MCC Code', 'Types', 'Farmer Name', 'Farmer Code', 'Gender'
            ],
            "🐄 Farm Details": [
                'Number of Cows', 'No. of Cattle in Milk', 'No. of Calves/Heifers',
                'No. of Desi cows', 'No. of Cross breed cows', 'No. of Buffalo', 'Milk Production (liters/day)'
            ],
            "🌿 Feed Details": [
                'Green Fodder', 'Type of Green Fodder', 'Quantity of Green Fodder (Kg/day)',
                'Dry Fodder', 'Type of Dry Fodder', 'Quantity of Dry Fodder (Kg/day)',
                'Pellet Feed', 'Pellet Feed Brand', 'Quantity of Pellet Feed (Kg/day)',
                'Mineral Mixture', 'Mineral Mixture Brand', 'Quantity of Mineral Mixture (gm/day)',
                'Silage', 'Source and Price of Silage', 'Quantity of Silage (Kg/day)'
            ],
            "😀 Water & Survey": [
                'Source of Water', 'Surveyor Name', 'Date of Visit', 'Language', 'Farm Photo Filename'
            ]
        }.items():
            st.subheader(section)
            for k in keys:
                st.markdown(f"**{k}**: {data.get(k)}")
st.divider()
st.header("🔐 Admin Real-Time Access")

# Allowed Emails
ALLOWED_EMAILS = ["shifalis@tns.org", "rmukherjee@tns.org","rsomanchi@tns.org", "mkaushal@tns.org"]
admin_email = st.text_input("Enter your Admin Email to unlock extra features:")

if admin_email in ALLOWED_EMAILS:
    st.success("✅ Admin access granted! Real-time view enabled.")
    # Add image access for admin
    if st.checkbox("🖼️ View and Download Uploaded Images"):
        # List all image files in the SAVE_DIR folder
        image_files = [f for f in os.listdir(SAVE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if image_files:
            for img_file in image_files:
                img_path = os.path.join(SAVE_DIR, img_file)

                # Display image
                st.image(img_path, caption=img_file, use_column_width=True)

                # Provide download button for the image
                with open(img_path, "rb") as img:
                    st.download_button(
                        label=f"⬇️ Download {img_file}",
                        data=img,
                        file_name=img_file,
                        mime="image/jpeg" if img_file.lower().endswith('.jpg') else "image/png"
                    )
        else:
            st.warning("⚠️ No images found.")
else:
    if admin_email:
        st.error("❌ Not an authorized admin.")

if st.checkbox("📄 View Past Submissions"):
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.csv')]
    if files:
        all_data = pd.concat([pd.read_csv(os.path.join(SAVE_DIR, f)) for f in files], ignore_index=True)
        st.dataframe(all_data)

        csv = all_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download All Responses",
            data=csv,
            file_name='all_survey_responses.csv',
            mime='text/csv',
            key='public_csv_download'
        )
    else:
        st.warning("⚠️ No submissions found yet.")
