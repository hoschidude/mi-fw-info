import streamlit as st
import json
import os
from datetime import datetime

file_path = "data.json"
modification_date = os.path.getmtime(file_path)

data = None
with open(file_path) as f:
    data = json.load(f)


# Function to convert upload_time to UTC datetime
def convert_to_utc(timestamp):
    utc_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return utc_time


st.title("Mi Firmware Info")
st.text(f"Snapshot: {convert_to_utc(modification_date)}")

# Extract models for the dropdown menu
names = {item['name']: item['model'] for item in data}

# Create a dropdown menu for selecting the model
name_selected = st.selectbox("**Select Model**", sorted(names.keys()))

# Display the corresponding data based on the selected model
if name_selected:
    model_selected = names[name_selected]
    selected_data = next(item for item in data if item['model'] == model_selected)

    st.header(name_selected)
    st.subheader('General')
    st.write(f"**Model ID**: {model_selected}")
    st.write(f"**Change Date (UTC)**: {convert_to_utc(selected_data['firmware']['upload_time'])}")
    if selected_data['firmware']['changeLog']:
        st.write(f"**Change Log**: {selected_data['firmware']['changeLog']}")

    st.subheader('Firmware Details')
    st.write(f"**Version**: {selected_data['firmware']['version']}")
    st.write(f"**MD5**: {selected_data['firmware']['md5']}")
    st.write(f"**Update URL**: [Download Firmware]({selected_data['firmware']['safe_url']})")

    if 'mcu_md5' in selected_data['firmware']:
        st.subheader('MCU Firmware Details')
        st.write(f"**Version**: {selected_data['firmware']['mcu_version']}")
        st.write(f"**MD5**: {selected_data['firmware']['mcu_md5']}")
        st.write(f"**Update URL**: [Download MCU Firmware]({selected_data['firmware']['mcu_safe_url']})")


st.header("Disclaimer")
st.write("""The links to firmware files provided on this site are sourced directly from content delivery network of the respective manufacturers. These links are intended for informational purposes only and are not hosted or controlled by us. We do not claim ownership of the firmware files nor do we endorse or guarantee their content, functionality, or safety.

 1. Purpose and Intent:
The links provided on this website lead to firmware downloads for various devices. The purpose of sharing these links is to facilitate access to firmware updates that may be necessary for maintaining or upgrading your devices. These links are intended for informational and educational purposes only.

 2. No Endorsement or Warranty:
We do not endorse or guarantee the accuracy, legality, or safety of the firmware files accessible through these links. The firmware is provided by the original manufacturers and is subject to their terms and conditions. We are not responsible for any issues arising from the use of these firmware files, including but not limited to damage to devices, data loss, or incompatibility issues.

 3. Manufacturer's Terms and Conditions:
Please be aware that the use and distribution of firmware may be governed by the terms and conditions set forth by the respective manufacturers. Users are advised to review and adhere to these terms before downloading or using any firmware.

 4. Intellectual Property Rights:
The firmware files linked from this site are the property of their respective copyright holders. By providing these links, we do not claim any ownership or rights to the firmware. Any use of the firmware must comply with the copyright and licensing terms specified by the manufacturers.

 5. No Liability:
We are not liable for any direct or indirect damages or losses resulting from the use of the firmware or the links provided. Users assume full responsibility for their use of the linked firmware and for ensuring compliance with any relevant laws and manufacturer guidelines.

 6. Content Accuracy:
While we strive to ensure that the links are accurate and up-to-date, we make no warranties or representations regarding the correctness of the information provided. Users are encouraged to verify the integrity and authenticity of any firmware before downloading and installing it.

 7. Legal Compliance:
The publication of these links is intended to comply with applicable laws and regulations. If you have any legal concerns or believe that any of the content on this site infringes on your rights, please contact us immediately so that we can address the issue.

By accessing and using the links provided on this website, you acknowledge that you have read, understood, and agree to this disclaimer.""")
