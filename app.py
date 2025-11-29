import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="CAR Education Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

@st.cache_data
def generate_enrollment_data():
    """Generate 1000+ enrollment records"""
    np.random.seed(42)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    
    # Municipalities per province
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
                    # Base enrollment varies by province and municipality
                    base = np.random.randint(500, 5000)
                    
                    # Seasonal variation (enrollment peaks in June-August)
                    month_factor = 1.2 if month in [6, 7, 8] else 1.0 if month in [9, 10, 11, 12, 1] else 0.9
                    
                    # Year trend (slight growth)
                    year_factor = 1.0 + (year - 2015) * 0.02
                    
                    # COVID impact
                    if year == 2020:
                        covid_factor = 0.92
                    elif year == 2021:
                        covid_factor = 0.88
                    else:
                        covid_factor = 1.0
                    
                    total = int(base * month_factor * year_factor * covid_factor)
                    elementary = int(total * 0.48)
                    secondary = int(total * 0.52)
                    
                    data.append({
                        'Province': province,
                        'Municipality': municipality,
                        'School_Year': f'{year}-{year+1}',
                        'Month': month,
                        'Elementary_Enrollment': elementary,
                        'Secondary_Enrollment': secondary,
                        'Total_Enrollment': total
                    })
    
    return pd.DataFrame(data)

@st.cache_data
def generate_graduates_data():
    """Generate 1000+ graduate records"""
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
    tracks = ['Elementary', 'JHS', 'STEM', 'ABM', 'HUMSS', 'TVL']
    
    data = []
    
    for province in provinces:
        for municipality in municipalities[province]:
            for year in years:
                for track in tracks:
                    if track == 'Elementary':
                        grads = np.random.randint(20, 200)
                    elif track == 'JHS':
                        grads = np.random.randint(15, 150)
                    else:  # SHS tracks
                        grads = np.random.randint(5, 80)
                    
                    data.append({
                        'Province': province,
                        'Municipality': municipality,
                        'School_Year': f'{year-1}-{year}',
                        'Track': track,
                        'Elementary_Graduates': grads if track == 'Elementary' else 0,
                        'Secondary_Graduates': grads if track != 'Elementary' else 0,
                        'Total_Graduates': grads
                    })
    
    return pd.DataFrame(data)

@st.cache_data
def generate_infrastructure_data():
    """Generate 1000+ infrastructure records (individual schools)"""
    np.random.seed(44)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    
    # Number of schools per province
    school_counts = {
        'Abra': 185,
        'Apayao': 142,
        'Benguet': 298,
        'Ifugao': 168,
        'Kalinga': 176,
        'Mountain Province': 135
    }
    
    data = []
    
    for province in provinces:
        num_schools = school_counts[province]
        
        for i in range(1, num_schools + 1):
            school_id = f"{province[:3].upper()}-{i:04d}"
            
            total_schools_val = 1  # Each row is 1 school
            has_electricity = np.random.choice([0, 1], p=[0.07, 0.93])
            has_internet = np.random.choice([0, 1], p=[0.35, 0.65])
            needs_repair = np.random.choice([0, 1], p=[0.72, 0.28])
            
            data.append({
                'Province': province,
                'School_ID': school_id,
                'Total_Schools': total_schools_val,
                'Schools_With_Electricity': has_electricity,
                'Schools_With_Internet': has_internet,
                'Schools_Needing_Repair': needs_repair
            })
    
    return pd.DataFrame(data)

@st.cache_data
def generate_performance_data():
    """Generate 1000+ performance records"""
    np.random.seed(45)
    
    provinces = ['Abra', 'Apayao', 'Benguet', 'Ifugao', 'Kalinga', 'Mountain Province']
    years = list(range(2015, 2025))
    grade_levels = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
                    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']
    subjects = ['Math', 'Science', 'English', 'Filipino']
    
    # Base scores by province (higher for Benguet)
    base_scores = {
        'Abra': 75.8,
        'Apayao': 72.4,
        'Benguet': 81.2,
        'Ifugao': 76.9,
        'Kalinga': 74.6,
        'Mountain Province': 78.3
    }
    
    data = []
    
    for province in provinces:
        base = base_scores[province]
        
        for year in years:
            for grade in grade_levels:
                for subject in subjects:
                    # Add variation
                    score = base + np.random.uniform(-5, 8)
                    score = max(60, min(95, score))
                    
                    passing_rate = (score - 55) / 40 * 100
                    passing_rate = max(65, min(98, passing_rate))
                    
                    literacy = 94 + np.random.uniform(0, 4)
                    dropout = 5 - (score - 70) / 10
                    dropout = max(1.5, min(7, dropout))
                    
                    data.append({
                        'Province': province,
                        'School_Year': f'{year-1}-{year}',
                        'Grade_Level': grade,
                        'Subject': subject,
                        'Average_NAT_Score': round(score, 1),
                        'Passing_Rate_Percent': round(passing_rate, 1),
                        'Literacy_Rate_Percent': round(literacy, 1),
                        'Dropout_Rate_Percent': round(dropout, 1)
                    })
    
    return pd.DataFrame(data)

# ============================================================================
# DISPLAY FUNCTION
# ============================================================================

def display_table(df, table_id, title, color):
    """Display table with proper styling"""
    st.markdown(f"### {title}")
    st.caption(f"**Table ID:** `{table_id}` | **Records:** {len(df):,}")
    
    html = df.to_html(index=False, table_id=table_id, border=1)
    
    st.markdown(f"""
    <style>
    #{table_id} {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        font-size: 14px;
    }}
    #{table_id} th {{
        background-color: {color};
        color: white;
        padding: 8px;
        text-align: left;
        position: sticky;
        top: 0;
    }}
    #{table_id} td {{
        border: 1px solid #ddd;
        padding: 6px;
    }}
    #{table_id} tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
    #{table_id} tr:hover {{
        background-color: #ddd;
    }}
    </style>
    <div style="max-height: 400px; overflow-y: auto;">
    {html}
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

st.title("🎓 CAR Education Data Portal")
st.markdown("### Cordillera Administrative Region - Education Statistics")

st.info("""
**📊 Web Scraping Practice Portal - LARGE DATASET VERSION**

Each table contains **1,000+ records** for realistic web scraping practice.

**Available Tables:**
- `enrollment_data_table` - Student enrollment data
- `graduates_data_table` - Graduate statistics
- `infrastructure_data_table` - School facilities
- `performance_data_table` - Academic performance
""")

# Generate data
with st.spinner("🔄 Generating large datasets..."):
    df_enrollment = generate_enrollment_data()
    df_graduates = generate_graduates_data()
    df_infrastructure = generate_infrastructure_data()
    df_performance = generate_performance_data()

total_records = len(df_enrollment) + len(df_graduates) + len(df_infrastructure) + len(df_performance)
st.success(f"✅ Loaded {total_records:,} total records across 4 tables")

# Display tables
st.markdown("---")
display_table(df_enrollment, "enrollment_data_table", "📚 School Enrollment Data", "#4CAF50")

st.markdown("---")
display_table(df_graduates, "graduates_data_table", "🎓 Graduates Data", "#2196F3")

st.markdown("---")
display_table(df_infrastructure, "infrastructure_data_table", "🏫 School Infrastructure Data", "#FF9800")

st.markdown("---")
display_table(df_performance, "performance_data_table", "📈 School Performance Data", "#9C27B0")

# Footer with scraping examples
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Enrollment Records", f"{len(df_enrollment):,}")
with col2:
    st.metric("Graduate Records", f"{len(df_graduates):,}")
with col3:
    st.metric("Infrastructure Records", f"{len(df_infrastructure):,}")
with col4:
    st.metric("Performance Records", f"{len(df_performance):,}")

with st.expander("🔍 Web Scraping Examples"):
    st.markdown("**R (rvest):**")
    st.code("""
library(rvest)
url <- "YOUR_STREAMLIT_URL"
page <- read_html(url)

# Scrape enrollment table
enrollment <- html_table(html_element(page, "#enrollment_data_table"))
print(paste("Rows:", nrow(enrollment)))

# Scrape all tables
tables <- c(
  enrollment = "#enrollment_data_table",
  graduates = "#graduates_data_table",
  infrastructure = "#infrastructure_data_table",
  performance = "#performance_data_table"
)

all_data <- lapply(tables, function(id) {
  html_table(html_element(page, id))
})
    """, language="r")
    
    st.markdown("**Python (pandas - easiest):**")
    st.code("""
import pandas as pd

url = "YOUR_STREAMLIT_URL"

# Scrape specific table
enrollment = pd.read_html(url, attrs={'id': 'enrollment_data_table'})[0]
print(f"Rows: {len(enrollment):,}")

# Scrape all tables
table_ids = [
    'enrollment_data_table',
    'graduates_data_table', 
    'infrastructure_data_table',
    'performance_data_table'
]

all_data = {}
for table_id in table_ids:
    df = pd.read_html(url, attrs={'id': table_id})[0]
    all_data[table_id] = df
    print(f"{table_id}: {len(df):,} rows")
    """, language="python")

with st.expander("📥 Download Data (Optional)"):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.download_button(
            "📥 Enrollment CSV",
            df_enrollment.to_csv(index=False),
            "enrollment_data.csv",
            "text/csv"
        )
    
    with col2:
        st.download_button(
            "📥 Graduates CSV",
            df_graduates.to_csv(index=False),
            "graduates_data.csv",
            "text/csv"
        )
    
    with col3:
        st.download_button(
            "📥 Infrastructure CSV",
            df_infrastructure.to_csv(index=False),
            "infrastructure_data.csv",
            "text/csv"
        )
    
    with col4:
        st.download_button(
            "📥 Performance CSV",
            df_performance.to_csv(index=False),
            "performance_data.csv",
            "text/csv"
        )
