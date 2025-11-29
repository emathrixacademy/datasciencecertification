import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CAR Education Portal",
    page_icon="🎓",
    layout="wide"
)

# Data
enrollment_data = {
    'Province': ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province'],
    'School_Year': ['2023-2024'] * 6,
    'Elementary_Enrollment': [28500, 18200, 52000, 24800, 26500, 19800],
    'Secondary_Enrollment': [15200, 9800, 28500, 13200, 14100, 10500],
    'Total_Enrollment': [43700, 28000, 80500, 38000, 40600, 30300]
}

graduates_data = {
    'Province': ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province'],
    'School_Year': ['2022-2023'] * 6,
    'Elementary_Graduates': [4200, 2650, 7800, 3600, 3850, 2900],
    'Secondary_Graduates': [2800, 1820, 5200, 2400, 2580, 1950],
    'Total_Graduates': [7000, 4470, 13000, 6000, 6430, 4850]
}

infrastructure_data = {
    'Province': ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province'],
    'Total_Schools': [185, 142, 298, 168, 176, 135],
    'Schools_With_Electricity': [172, 125, 295, 155, 162, 128],
    'Schools_With_Internet': [98, 65, 215, 85, 92, 72],
    'Schools_Needing_Repair': [45, 52, 38, 48, 43, 39]
}

performance_data = {
    'Province': ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province'],
    'Average_NAT_Score': [75.8, 72.4, 81.2, 76.9, 74.6, 78.3],
    'Passing_Rate_Percent': [82.5, 79.3, 88.7, 83.8, 81.2, 85.4],
    'Literacy_Rate_Percent': [96.2, 94.5, 98.1, 95.8, 95.3, 97.2],
    'Dropout_Rate_Percent': [3.8, 5.2, 2.1, 3.5, 4.2, 2.9]
}

st.title("🎓 CAR Education Data Portal")
st.markdown("### Cordillera Administrative Region - Education Statistics")

st.info("""
**📊 Web Scraping Practice Portal**

All tables have unique IDs for easy scraping:
- `enrollment_data_table`
- `graduates_data_table`
- `infrastructure_data_table`
- `performance_data_table`
""")

# ENROLLMENT TABLE
st.markdown("---")
st.markdown("### 📚 School Enrollment Data")
df1 = pd.DataFrame(enrollment_data)
html1 = df1.to_html(index=False, table_id="enrollment_data_table", border=1)
st.markdown(f"""
<style>
#enrollment_data_table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}}
#enrollment_data_table th {{
    background-color: #4CAF50;
    color: white;
    padding: 8px;
    text-align: left;
}}
#enrollment_data_table td {{
    border: 1px solid #ddd;
    padding: 8px;
}}
#enrollment_data_table tr:nth-child(even) {{
    background-color: #f2f2f2;
}}
</style>
{html1}
""", unsafe_allow_html=True)

# GRADUATES TABLE
st.markdown("---")
st.markdown("### 🎓 Graduates Data")
df2 = pd.DataFrame(graduates_data)
html2 = df2.to_html(index=False, table_id="graduates_data_table", border=1)
st.markdown(f"""
<style>
#graduates_data_table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}}
#graduates_data_table th {{
    background-color: #2196F3;
    color: white;
    padding: 8px;
    text-align: left;
}}
#graduates_data_table td {{
    border: 1px solid #ddd;
    padding: 8px;
}}
#graduates_data_table tr:nth-child(even) {{
    background-color: #f2f2f2;
}}
</style>
{html2}
""", unsafe_allow_html=True)

# INFRASTRUCTURE TABLE
st.markdown("---")
st.markdown("### 🏫 School Infrastructure Data")
df3 = pd.DataFrame(infrastructure_data)
html3 = df3.to_html(index=False, table_id="infrastructure_data_table", border=1)
st.markdown(f"""
<style>
#infrastructure_data_table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}}
#infrastructure_data_table th {{
    background-color: #FF9800;
    color: white;
    padding: 8px;
    text-align: left;
}}
#infrastructure_data_table td {{
    border: 1px solid #ddd;
    padding: 8px;
}}
#infrastructure_data_table tr:nth-child(even) {{
    background-color: #f2f2f2;
}}
</style>
{html3}
""", unsafe_allow_html=True)

# PERFORMANCE TABLE
st.markdown("---")
st.markdown("### 📈 School Performance Data")
df4 = pd.DataFrame(performance_data)
html4 = df4.to_html(index=False, table_id="performance_data_table", border=1)
st.markdown(f"""
<style>
#performance_data_table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}}
#performance_data_table th {{
    background-color: #9C27B0;
    color: white;
    padding: 8px;
    text-align: left;
}}
#performance_data_table td {{
    border: 1px solid #ddd;
    padding: 8px;
}}
#performance_data_table tr:nth-child(even) {{
    background-color: #f2f2f2;
}}
</style>
{html4}
""", unsafe_allow_html=True)

st.markdown("---")
st.success(f"✅ All tables loaded | Total records: {len(df1) + len(df2) + len(df3) + len(df4)}")

with st.expander("🔍 Scraping Examples"):
    st.code("""
# R Example
library(rvest)
url <- "YOUR_STREAMLIT_URL"
page <- read_html(url)
data <- html_table(html_element(page, "#enrollment_data_table"))

# Python Example
import pandas as pd
url = "YOUR_STREAMLIT_URL"
tables = pd.read_html(url, attrs={'id': 'enrollment_data_table'})
df = tables[0]
    """)
