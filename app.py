import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

st.set_page_config(
    page_title="CAR Education Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================================
# DATA GENERATION FUNCTIONS - GUARANTEED 1000+ RECORDS EACH
# ============================================================================

@st.cache_data
def generate_enrollment_data():
    """Generate 1000+ enrollment records with realistic variations"""
    np.random.seed(42)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    
    municipalities = {
        'Abra': ['Bangued', 'Boliney', 'Bucay', 'Bucloc', 'Daguioman', 'Danglas', 
                 'Dolores', 'La Paz', 'Lacub', 'Lagangilang', 'Lagayan', 'Langiden',
                 'Licuan-Baay', 'Luba', 'Malibcong', 'Manabo', 'Peñarrubia', 'Pidigan',
                 'Pilar', 'Sallapadan', 'San Isidro', 'San Juan', 'San Quintin', 
                 'Tayum', 'Tineg', 'Tubo', 'Villaviciosa'],
        'Apayao': ['Calanasan', 'Conner', 'Flora', 'Kabugao', 'Luna', 'Pudtol', 'Santa Marcela'],
        'Benguet': ['Atok', 'Baguio City', 'Bakun', 'Bokod', 'Buguias', 'Itogon', 
                    'Kabayan', 'Kapangan', 'Kibungan', 'La Trinidad', 'Mankayan', 
                    'Sablan', 'Tuba', 'Tublay'],
        'Ifugao': ['Aguinaldo', 'Alfonso Lista', 'Asipulo', 'Banaue', 'Hingyon', 
                   'Hungduan', 'Kiangan', 'Lagawe', 'Lamut', 'Mayoyao', 'Tinoc'],
        'Kalinga': ['Balbalan', 'Lubuagan', 'Pasil', 'Pinukpuk', 'Rizal', 'Tabuk City', 
                    'Tanudan', 'Tinglayan'],
        'Mountain Province': ['Barlig', 'Bauko', 'Besao', 'Bontoc', 'Natonin', 
                              'Paracelis', 'Sabangan', 'Sadanga', 'Sagada', 'Tadian']
    }
    
    years = list(range(2015, 2025))
    months = list(range(1, 13))
    
    data = []
    
    for province in provinces:
        for municipality in municipalities[province]:
            for year in years:
                for month in months:
                    # Province-specific base enrollment
                    if province == 'Benguet':
                        base = np.random.randint(800, 6000)
                    elif province == 'Abra':
                        base = np.random.randint(600, 4500)
                    else:
                        base = np.random.randint(400, 3500)
                    
                    # Municipality size factor
                    if municipality in ['Baguio City', 'Tabuk City', 'Bangued', 'La Trinidad']:
                        base *= 1.8
                    
                    # Seasonal variation (enrollment peaks in June-August)
                    if month in [6, 7, 8]:
                        month_factor = 1.15
                    elif month in [9, 10, 11, 12, 1]:
                        month_factor = 1.0
                    else:
                        month_factor = 0.85
                    
                    # Year trend (slight growth with variations)
                    year_factor = 1.0 + (year - 2015) * 0.025
                    
                    # COVID impact (2020-2021)
                    if year == 2020:
                        covid_factor = 0.88
                    elif year == 2021:
                        covid_factor = 0.82
                    elif year == 2022:
                        covid_factor = 0.93
                    else:
                        covid_factor = 1.0
                    
                    # Typhoon/disaster impact (random years)
                    disaster_factor = 0.95 if (year == 2018 and month in [9, 10]) else 1.0
                    
                    total = int(base * month_factor * year_factor * covid_factor * disaster_factor)
                    
                    # Elementary/Secondary split with some variation
                    elem_ratio = 0.58 + np.random.uniform(-0.05, 0.05)
                    elementary = int(total * elem_ratio)
                    secondary = total - elementary
                    
                    # Add some missing data for teaching data cleaning
                    if np.random.random() < 0.02:  # 2% missing data
                        elementary = None
                        secondary = None
                        total = None
                    
                    data.append({
                        'Province': province,
                        'Municipality': municipality,
                        'School_Year': f'{year}-{year+1}',
                        'Month': month,
                        'Month_Name': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month-1],
                        'Elementary_Enrollment': elementary,
                        'Secondary_Enrollment': secondary,
                        'Total_Enrollment': total,
                        'Data_Source': np.random.choice(['DepEd', 'LGU', 'School Report'], p=[0.7, 0.2, 0.1])
                    })
    
    df = pd.DataFrame(data)
    print(f"Enrollment records generated: {len(df):,}")
    return df

@st.cache_data
def generate_graduates_data():
    """Generate 1000+ graduate records with realistic variations"""
    np.random.seed(43)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    municipalities = {
        'Abra': ['Bangued', 'Boliney', 'Bucay', 'Bucloc', 'Daguioman', 'Danglas', 
                 'Dolores', 'La Paz', 'Lacub', 'Lagangilang', 'Lagayan', 'Langiden',
                 'Licuan-Baay', 'Luba', 'Malibcong', 'Manabo', 'Peñarrubia', 'Pidigan',
                 'Pilar', 'Sallapadan', 'San Isidro', 'San Juan', 'San Quintin', 
                 'Tayum', 'Tineg', 'Tubo', 'Villaviciosa'],
        'Apayao': ['Calanasan', 'Conner', 'Flora', 'Kabugao', 'Luna', 'Pudtol', 'Santa Marcela'],
        'Benguet': ['Atok', 'Baguio City', 'Bakun', 'Bokod', 'Buguias', 'Itogon', 
                    'Kabayan', 'Kapangan', 'Kibungan', 'La Trinidad', 'Mankayan', 
                    'Sablan', 'Tuba', 'Tublay'],
        'Ifugao': ['Aguinaldo', 'Alfonso Lista', 'Asipulo', 'Banaue', 'Hingyon', 
                   'Hungduan', 'Kiangan', 'Lagawe', 'Lamut', 'Mayoyao', 'Tinoc'],
        'Kalinga': ['Balbalan', 'Lubuagan', 'Pasil', 'Pinukpuk', 'Rizal', 'Tabuk City', 
                    'Tanudan', 'Tinglayan'],
        'Mountain Province': ['Barlig', 'Bauko', 'Besao', 'Bontoc', 'Natonin', 
                              'Paracelis', 'Sabangan', 'Sadanga', 'Sagada', 'Tadian']
    }
    
    years = list(range(2015, 2025))
    tracks = ['Elementary', 'JHS', 'STEM', 'ABM', 'HUMSS', 'TVL', 'GAS', 'ARTS_DESIGN']
    
    data = []
    
    for province in provinces:
        for municipality in municipalities[province]:
            for year in years:
                for track in tracks:
                    # Base graduates by track
                    if track == 'Elementary':
                        base_grads = np.random.randint(30, 250)
                    elif track == 'JHS':
                        base_grads = np.random.randint(20, 180)
                    elif track == 'STEM':
                        base_grads = np.random.randint(10, 100)
                    elif track in ['ABM', 'HUMSS']:
                        base_grads = np.random.randint(8, 85)
                    else:  # TVL, GAS, ARTS
                        base_grads = np.random.randint(5, 70)
                    
                    # Urban area multiplier
                    if municipality in ['Baguio City', 'Tabuk City', 'Bangued', 'La Trinidad']:
                        base_grads = int(base_grads * 2.2)
                    
                    # COVID impact
                    if year in [2020, 2021]:
                        base_grads = int(base_grads * 0.95)
                    
                    # Gender distribution
                    male_grads = int(base_grads * (0.48 + np.random.uniform(-0.05, 0.05)))
                    female_grads = base_grads - male_grads
                    
                    # Honors graduates (10-15% of total)
                    honors = int(base_grads * np.random.uniform(0.10, 0.15))
                    
                    data.append({
                        'Province': province,
                        'Municipality': municipality,
                        'School_Year': f'{year-1}-{year}',
                        'Track': track,
                        'Level': 'Elementary' if track == 'Elementary' else 'Secondary',
                        'Male_Graduates': male_grads,
                        'Female_Graduates': female_grads,
                        'Total_Graduates': base_grads,
                        'With_Honors': honors,
                        'Completion_Rate': round(np.random.uniform(88, 98), 1)
                    })
    
    df = pd.DataFrame(data)
    print(f"Graduate records generated: {len(df):,}")
    return df

@st.cache_data
def generate_infrastructure_data():
    """Generate 1000+ infrastructure records (individual schools)"""
    np.random.seed(44)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    
    # Increased school counts to ensure 1000+ records
    school_counts = {
        'Abra': 195,
        'Apayao': 155,
        'Benguet': 320,
        'Ifugao': 180,
        'Kalinga': 188,
        'Mountain Province': 145
    }
    
    school_types = ['Elementary', 'Secondary', 'Integrated']
    
    data = []
    
    for province in provinces:
        num_schools = school_counts[province]
        
        for i in range(1, num_schools + 1):
            school_id = f"{province[:3].upper()}-{i:04d}"
            school_type = np.random.choice(school_types, p=[0.60, 0.25, 0.15])
            
            # Infrastructure probabilities vary by province
            if province == 'Benguet':
                p_electricity = 0.97
                p_internet = 0.75
                p_water = 0.95
                p_repair = 0.22
            elif province in ['Abra', 'Kalinga']:
                p_electricity = 0.92
                p_internet = 0.62
                p_water = 0.88
                p_repair = 0.30
            else:
                p_electricity = 0.88
                p_internet = 0.55
                p_water = 0.82
                p_repair = 0.35
            
            has_electricity = np.random.choice([0, 1], p=[1-p_electricity, p_electricity])
            has_internet = np.random.choice([0, 1], p=[1-p_internet, p_internet])
            has_water = np.random.choice([0, 1], p=[1-p_water, p_water])
            needs_repair = np.random.choice([0, 1], p=[1-p_repair, p_repair])
            
            # Classroom data
            total_classrooms = np.random.randint(6, 45)
            functional_classrooms = int(total_classrooms * np.random.uniform(0.85, 1.0))
            
            # Toilet facilities
            total_toilets = np.random.randint(4, 20)
            functional_toilets = int(total_toilets * np.random.uniform(0.75, 1.0))
            
            # Teacher data
            num_teachers = np.random.randint(8, 65)
            
            # Student-classroom ratio
            avg_class_size = np.random.randint(25, 48)
            
            data.append({
                'Province': province,
                'School_ID': school_id,
                'School_Type': school_type,
                'Total_Classrooms': total_classrooms,
                'Functional_Classrooms': functional_classrooms,
                'Total_Toilets': total_toilets,
                'Functional_Toilets': functional_toilets,
                'Number_of_Teachers': num_teachers,
                'Has_Electricity': has_electricity,
                'Has_Internet': has_internet,
                'Has_Water_Supply': has_water,
                'Needs_Major_Repair': needs_repair,
                'Has_Library': np.random.choice([0, 1], p=[0.35, 0.65]),
                'Has_Computer_Lab': np.random.choice([0, 1], p=[0.58, 0.42]),
                'Average_Class_Size': avg_class_size,
                'Last_Inspection_Year': np.random.randint(2020, 2025)
            })
    
    df = pd.DataFrame(data)
    print(f"Infrastructure records generated: {len(df):,}")
    return df

@st.cache_data
def generate_performance_data():
    """Generate 1000+ performance records with realistic variations"""
    np.random.seed(45)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    years = list(range(2015, 2025))
    grade_levels = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
                    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
    subjects = ['Math', 'Science', 'English', 'Filipino', 'Araling Panlipunan']
    
    # Base scores by province
    base_scores = {
        'Abra': 75.2,
        'Apayao': 71.8,
        'Benguet': 82.5,
        'Ifugao': 76.4,
        'Kalinga': 74.1,
        'Mountain Province': 77.9
    }
    
    data = []
    
    for province in provinces:
        base = base_scores[province]
        
        for year in years:
            # COVID impact on scores
            if year in [2020, 2021]:
                covid_penalty = -3.5
            elif year == 2022:
                covid_penalty = -1.8
            else:
                covid_penalty = 0
            
            for grade in grade_levels:
                for subject in subjects:
                    # Subject difficulty variation
                    if subject == 'Math':
                        subject_modifier = -2.5
                    elif subject == 'Science':
                        subject_modifier = -1.8
                    elif subject == 'English':
                        subject_modifier = -0.5
                    else:
                        subject_modifier = 0
                    
                    # Grade level variation (higher grades slightly lower scores)
                    grade_num = int(grade.split()[1])
                    grade_penalty = -0.3 * (grade_num - 6)
                    
                    score = base + subject_modifier + covid_penalty + grade_penalty
                    score += np.random.uniform(-4, 6)
                    score = max(62, min(96, score))
                    
                    # Passing rate correlates with score
                    passing_rate = (score - 50) / 45 * 100
                    passing_rate = max(68, min(99, passing_rate))
                    
                    # Literacy rate (generally high)
                    literacy = 93 + np.random.uniform(0, 5)
                    
                    # Dropout rate (inversely related to score)
                    dropout = 7 - (score - 65) / 8
                    dropout = max(0.8, min(8.5, dropout))
                    
                    # Number of students tested
                    students_tested = np.random.randint(120, 850)
                    
                    data.append({
                        'Province': province,
                        'School_Year': f'{year-1}-{year}',
                        'Grade_Level': grade,
                        'Subject': subject,
                        'Students_Tested': students_tested,
                        'Average_Score': round(score, 1),
                        'Passing_Rate_Percent': round(passing_rate, 1),
                        'Literacy_Rate_Percent': round(literacy, 1),
                        'Dropout_Rate_Percent': round(dropout, 2),
                        'Perfect_Scores': int(students_tested * np.random.uniform(0.01, 0.05))
                    })
    
    df = pd.DataFrame(data)
    print(f"Performance records generated: {len(df):,}")
    return df

# ============================================================================
# DISPLAY FUNCTION
# ============================================================================

def display_table(df, table_id, title, color):
    """Display table with proper styling and statistics"""
    st.markdown(f"### {title}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Missing Data", f"{missing_pct:.2f}%")
    
    # Quick stats
    with st.expander(f"📊 Quick Statistics for {title}"):
        st.dataframe(df.describe(), use_container_width=True)
    
    # Display using Streamlit's native dataframe with proper table ID in HTML
    st.markdown(f"**Table ID for scraping:** `{table_id}`")
    
    # Create scrollable container with the table
    html_table = f"""
    <style>
        .table-container-{table_id} {{
            max-height: 500px;
            overflow-y: auto;
            border: 2px solid {color};
            border-radius: 5px;
            margin: 10px 0;
        }}
        #{table_id} {{
            border-collapse: collapse;
            width: 100%;
            font-size: 13px;
            font-family: Arial, sans-serif;
        }}
        #{table_id} th {{
            background-color: {color};
            color: white;
            padding: 10px;
            text-align: left;
            position: sticky;
            top: 0;
            font-weight: bold;
            border: 1px solid #ddd;
        }}
        #{table_id} td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        #{table_id} tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        #{table_id} tr:hover {{
            background-color: #e8f4f8;
        }}
    </style>
    <div class="table-container-{table_id}">
        {df.to_html(index=False, table_id=table_id, border=1, na_rep='NULL', escape=False)}
    </div>
    """
    
    st.markdown(html_table, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

st.title("🎓 CAR Education Data Portal")
st.markdown("### Cordillera Administrative Region - Comprehensive Education Statistics")

st.info("""
**📊 Professional Web Scraping Practice Portal - GUARANTEED 1000+ Records Per Table**

This portal provides **realistic, large-scale educational data** for web scraping practice, data analysis, and machine learning exercises.

**✨ Features:**
- ✅ Each table contains **1000+ records** (guaranteed)
- ✅ Realistic data variations (COVID impact, seasonal trends, missing data)
- ✅ Philippine localization (CAR provinces and municipalities)
- ✅ Perfect for teaching: data cleaning, web scraping, statistical analysis
- ✅ Compatible with R (rvest), Python (pandas, BeautifulSoup), and other tools

**📋 Available Tables:**
1. `enrollment_data_table` - Monthly student enrollment (1000+ records)
2. `graduates_data_table` - Graduate statistics by track (1000+ records)
3. `infrastructure_data_table` - Individual school facilities (1000+ records)
4. `performance_data_table` - Academic performance by subject (1000+ records)
""")

# Generate data
with st.spinner("🔄 Generating comprehensive datasets..."):
    df_enrollment = generate_enrollment_data()
    df_graduates = generate_graduates_data()
    df_infrastructure = generate_infrastructure_data()
    df_performance = generate_performance_data()

total_records = len(df_enrollment) + len(df_graduates) + len(df_infrastructure) + len(df_performance)

st.success(f"""
✅ **Successfully loaded {total_records:,} total records**
- Enrollment: {len(df_enrollment):,} records
- Graduates: {len(df_graduates):,} records  
- Infrastructure: {len(df_infrastructure):,} records
- Performance: {len(df_performance):,} records
""")

# Navigation
st.markdown("---")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📚 Enrollment", 
    "🎓 Graduates", 
    "🏫 Infrastructure", 
    "📈 Performance",
    "🔍 Scraping Guide"
])

with tab1:
    display_table(df_enrollment, "enrollment_data_table", 
                 "📚 School Enrollment Data", "#4CAF50")

with tab2:
    display_table(df_graduates, "graduates_data_table", 
                 "🎓 Graduates Data", "#2196F3")

with tab3:
    display_table(df_infrastructure, "infrastructure_data_table", 
                 "🏫 School Infrastructure Data", "#FF9800")

with tab4:
    display_table(df_performance, "performance_data_table", 
                 "📈 School Performance Data", "#9C27B0")

with tab5:
    st.markdown("## 🔍 Complete Web Scraping Guide")
    
    st.markdown("### 🐍 Python (Recommended - Easiest)")
    
    st.code("""
import pandas as pd

# Replace with your actual Streamlit URL
url = "https://your-app.streamlit.app"

# Method 1: Scrape specific table by ID
enrollment_df = pd.read_html(url, attrs={'id': 'enrollment_data_table'})[0]
print(f"Enrollment: {len(enrollment_df):,} rows")

# Method 2: Scrape all tables at once
all_tables = pd.read_html(url)
print(f"Found {len(all_tables)} tables")

# Method 3: Scrape with error handling
try:
    table_ids = [
        'enrollment_data_table',
        'graduates_data_table',
        'infrastructure_data_table',
        'performance_data_table'
    ]
    
    datasets = {}
    for table_id in table_ids:
        df = pd.read_html(url, attrs={'id': table_id})[0]
        datasets[table_id] = df
        print(f"{table_id}: {len(df):,} rows × {len(df.columns)} columns")
        
    # Now you have all data in 'datasets' dictionary
    enrollment = datasets['enrollment_data_table']
    
except Exception as e:
    print(f"Error: {e}")

# Save to CSV
enrollment_df.to_csv('enrollment_data.csv', index=False)
    """, language="python")
    
    st.markdown("### 📦 R (rvest)")
    
    st.code("""
library(rvest)
library(dplyr)

# Your Streamlit URL
url <- "https://your-app.streamlit.app"

# Read the page
page <- read_html(url)

# Method 1: Scrape specific table
enrollment <- page %>%
  html_element("#enrollment_data_table") %>%
  html_table()

cat("Enrollment rows:", nrow(enrollment), "\\n")

# Method 2: Scrape all tables
table_ids <- c(
  "enrollment_data_table",
  "graduates_data_table",
  "infrastructure_data_table",
  "performance_data_table"
)

all_data <- lapply(table_ids, function(id) {
  page %>%
    html_element(paste0("#", id)) %>%
    html_table()
})

names(all_data) <- table_ids

# Access specific table
enrollment <- all_data$enrollment_data_table
cat("Enrollment:", nrow(enrollment), "rows ×", ncol(enrollment), "columns\\n")

# Save to CSV
write.csv(enrollment, "enrollment_data.csv", row.names = FALSE)
    """, language="r")
    
    st.markdown("### 🌐 BeautifulSoup (Advanced Python)")
    
    st.code("""
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://your-app.streamlit.app"

# Get page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find specific table
enrollment_table = soup.find('table', {'id': 'enrollment_data_table'})

# Extract data
data = []
headers = [th.text.strip() for th in enrollment_table.find_all('th')]

for row in enrollment_table.find_all('tr')[1:]:  # Skip header
    cols = [td.text.strip() for td in row.find_all('td')]
    if cols:
        data.append(cols)

# Create DataFrame
df = pd.DataFrame(data, columns=headers)
print(f"Scraped {len(df):,} rows")
    """, language="python")

# Footer with download options
st.markdown("---")
st.markdown("### 📥 Download Complete Datasets")

col1, col2, col3, col4 = st.columns(4)

with col1:
    csv_enrollment = df_enrollment.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Enrollment CSV",
        csv_enrollment,
        "car_enrollment_data.csv",
        "text/csv",
        key='download-enrollment'
    )

with col2:
    csv_graduates = df_graduates.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Graduates CSV",
        csv_graduates,
        "car_graduates_data.csv",
        "text/csv",
        key='download-graduates'
    )

with col3:
    csv_infrastructure = df_infrastructure.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Infrastructure CSV",
        csv_infrastructure,
        "car_infrastructure_data.csv",
        "text/csv",
        key='download-infrastructure'
    )

with col4:
    csv_performance = df_performance.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Performance CSV",
        csv_performance,
        "car_performance_data.csv",
        "text/csv",
        key='download-performance'
    )

# Summary Statistics
st.markdown("---")
st.markdown("### 📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Enrollment Records", 
        f"{len(df_enrollment):,}",
        delta=f"{len(df_enrollment.columns)} columns"
    )

with col2:
    st.metric(
        "🎓 Graduate Records", 
        f"{len(df_graduates):,}",
        delta=f"{len(df_graduates.columns)} columns"
    )

with col3:
    st.metric(
        "🏫 School Records", 
        f"{len(df_infrastructure):,}",
        delta=f"{len(df_infrastructure.columns)} columns"
    )

with col4:
    st.metric(
        "📈 Performance Records", 
        f"{len(df_performance):,}",
        delta=f"{len(df_performance.columns)} columns"
    )

# Educational use case suggestions
st.markdown("---")
with st.expander("💡 Educational Use Cases for Data Science Training"):
    st.markdown("""
    **Perfect for teaching:**
    
    1. **Web Scraping Fundamentals**
       - HTML table extraction
       - Data parsing and cleaning
       - Handling missing values (2% NULL values included)
    
    2. **Data Analysis & Visualization**
       - Time series analysis (2015-2024)
       - Geographic comparisons (6 provinces)
       - Trend identification (COVID impact, seasonal patterns)
    
    3. **Statistical Analysis**
       - Correlation analysis (infrastructure vs performance)
       - Hypothesis testing (urban vs rural differences)
       - Regression modeling (enrollment predictors)
    
    4. **Machine Learning Projects**
       - Enrollment prediction models
       - Performance classification
       - Dropout risk assessment
       - Infrastructure needs forecasting
    
    5. **Data Cleaning & Preparation**
       - Handling NULL values
       - Data type conversions
       - Outlier detection
       - Data validation
    
    **Philippine Context Features:**
    - ✅ Real CAR provinces and municipalities
    - ✅ COVID-19 impact on education (2020-2022)
    - ✅ Typhoon/disaster effects simulation
    - ✅ Urban-rural disparities (Baguio City vs remote municipalities)
    - ✅ K-12 curriculum tracks (STEM, ABM, HUMSS, TVL, etc.)
    """)

st.markdown("---")
st.caption("🎓 CAR Education Data Portal | Created for Data Science Education | Version 2.0")
st.caption("⚡ Optimized for web scraping practice with realistic Philippine education data")
