import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="CAR Education Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================================
# LOAD DATA FROM HTML FILES
# ============================================================================

@st.cache_data
def load_table_from_html(filename, table_id):
    """Load data from HTML file"""
    try:
        df = pd.read_html(filename, attrs={'id': table_id})[0]
        return df
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return pd.DataFrame()

@st.cache_data
def load_html_content(filename):
    """Load raw HTML content for display"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading {filename}: {e}")
        return ""

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_table_metrics(df, title):
    """Display table statistics"""
    st.markdown(f"### {title}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Missing Data", f"{missing_pct:.2f}%")

def display_html_table(html_file, table_id, title, color):
    """Display HTML table with styling"""
    # Load dataframe for metrics
    df = load_table_from_html(html_file, table_id)
    
    if df.empty:
        st.error(f"Could not load data from {html_file}")
        return
    
    # Display metrics
    display_table_metrics(df, title)
    
    # Quick stats
    with st.expander(f"📊 Quick Statistics for {title}"):
        st.dataframe(df.describe(), use_container_width=True)
    
    # Display the actual HTML table
    st.markdown(f"**Table ID for scraping:** `{table_id}`")
    
    # Load and inject styled HTML
    html_content = load_html_content(html_file)
    
    styled_html = f"""
    <style>
        .table-wrapper {{
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
    <div class="table-wrapper">
        {df.to_html(index=False, table_id=table_id, border=1, escape=False)}
    </div>
    """
    
    st.markdown(styled_html, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

st.title("🎓 CAR Education Data Portal")
st.markdown("### Cordillera Administrative Region - Education Statistics")

st.info("""
**📊 Web Scraping Practice Portal - Pre-loaded Data**

This portal provides **realistic, large-scale educational data** for web scraping practice.

**✨ Features:**
- ✅ Fast loading (pre-generated HTML files)
- ✅ 1000+ records per table
- ✅ Realistic Philippine education data (CAR region)
- ✅ Perfect for R (rvest), Python (pandas), web scraping practice

**📋 Available Tables:**
1. `enrollment_data_table` - Student enrollment data
2. `graduates_data_table` - Graduate statistics  
3. `infrastructure_data_table` - School facilities
4. `performance_data_table` - Academic performance
""")

# Check if HTML files exist
html_files = {
    'enrollment': 'enrollment.html',
    'graduates': 'graduates.html',
    'infrastructure': 'infrastructure.html',
    'performance': 'performance.html'
}

missing_files = [f for f in html_files.values() if not Path(f).exists()]

if missing_files:
    st.error(f"⚠️ Missing data files: {', '.join(missing_files)}")
    st.info("Please ensure all HTML data files are uploaded alongside app.py")
    st.stop()

# Load all datasets for summary
with st.spinner("📂 Loading datasets..."):
    df_enrollment = load_table_from_html('enrollment.html', 'enrollment_data_table')
    df_graduates = load_table_from_html('graduates.html', 'graduates_data_table')
    df_infrastructure = load_table_from_html('infrastructure.html', 'infrastructure_data_table')
    df_performance = load_table_from_html('performance.html', 'performance_data_table')

total_records = len(df_enrollment) + len(df_graduates) + len(df_infrastructure) + len(df_performance)

st.success(f"""
✅ **Loaded {total_records:,} total records**
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
    display_html_table('enrollment.html', 'enrollment_data_table', 
                      '📚 School Enrollment Data', '#4CAF50')

with tab2:
    display_html_table('graduates.html', 'graduates_data_table', 
                      '🎓 Graduates Data', '#2196F3')

with tab3:
    display_html_table('infrastructure.html', 'infrastructure_data_table', 
                      '🏫 School Infrastructure Data', '#FF9800')

with tab4:
    display_html_table('performance.html', 'performance_data_table', 
                      '📈 School Performance Data', '#9C27B0')

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

# Method 2: Scrape all tables
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
    print(f"{table_id}: {len(df):,} rows")

# Save to CSV
enrollment_df.to_csv('enrollment_data.csv', index=False)
    """, language="python")
    
    st.markdown("### 📦 R (rvest)")
    
    st.code("""
library(rvest)
library(dplyr)

# Your Streamlit URL
url <- "https://your-app.streamlit.app"
page <- read_html(url)

# Scrape specific table
enrollment <- page %>%
  html_element("#enrollment_data_table") %>%
  html_table()

cat("Enrollment rows:", nrow(enrollment), "\\n")

# Scrape all tables
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

# Save to CSV
write.csv(enrollment, "enrollment_data.csv", row.names = FALSE)
    """, language="r")

# Download section
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

# Summary metrics
st.markdown("---")
st.markdown("### 📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Enrollment", f"{len(df_enrollment):,}", 
              delta=f"{len(df_enrollment.columns)} columns")

with col2:
    st.metric("🎓 Graduates", f"{len(df_graduates):,}", 
              delta=f"{len(df_graduates.columns)} columns")

with col3:
    st.metric("🏫 Schools", f"{len(df_infrastructure):,}", 
              delta=f"{len(df_infrastructure.columns)} columns")

with col4:
    st.metric("📈 Performance", f"{len(df_performance):,}", 
              delta=f"{len(df_performance.columns)} columns")

st.markdown("---")
st.caption("🎓 CAR Education Data Portal | Data Science Education | Fast-Loading Version")
