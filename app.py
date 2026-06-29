import streamlit as st
from kpi_engine import generate_kpi_scorecard, parse_kpi_response

# --- SETUP HALAMAN ---
st.set_page_config(page_title="KPI Scorecard Builder | BlueRock", page_icon="📈", layout="wide")

# --- HEADER ---
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>📈 AI KPI Scorecard Builder</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Design precise, data-driven KPI blueprints for Power BI / Looker Studio implementation.</p>", unsafe_allow_html=True)
st.divider()

# --- LAYOUT KIRI (INPUT) & KANAN (OUTPUT) ---
col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.markdown("### 📋 Requirement Brief")
    
    # 1. Input Departemen
    department = st.selectbox(
        "Select Department / Business Unit:",
        ["Sales (B2B/B2C)", "Marketing & Growth", "Customer Success / Support", "Operations & Supply Chain", "Finance & Accounting", "Custom/Other"]
    )
    
    if department == "Custom/Other":
        department = st.text_input("Specify Department Name:")

    # 2. Input Objektif
    objectives = st.text_area(
        "Core Business Objectives:",
        placeholder="Example: We want to reduce customer churn within the first 90 days and track the efficiency of our onboarding team.",
        height=120
    )
    
    # 3. Input Data Sources (Sistem yang dipakai klien)
    data_sources = st.multiselect(
        "Available Data Sources (Tech Stack):",
        ["HubSpot CRM", "Salesforce", "Xero", "Zendesk", "Jira Service Desk", "Google Analytics 4", "Custom SQL Database", "Excel / Flat Files"],
        default=["HubSpot CRM"]
    )
    
    # Tombol Eksekusi
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate KPI Blueprint 🚀", type="primary", use_container_width=True)

with col_output:
    st.markdown("### 📊 Generated Blueprint")
    
    if generate_btn:
        if not objectives.strip():
            st.warning("⚠️ Please define the Core Business Objectives first.")
        else:
            with st.spinner("🧠 Strategizing KPIs and formulating data metrics..."):
                # Konversi list data sources menjadi string koma
                ds_string = ", ".join(data_sources) if data_sources else "Unknown / Not specified"
                
                # Panggil AI Engine
                ai_output = generate_kpi_scorecard(department, objectives, ds_string)
                
                if ai_output.startswith("Error:"):
                    st.error(ai_output)
                else:
                    # Parsing Output
                    alignment, scorecard, integrations = parse_kpi_response(ai_output)
                    
                    st.success("✅ Blueprint Ready for Dashboard Development!")
                    
                    # Tampilkan dalam Tabs
                    tab_align, tab_kpi, tab_tech = st.tabs(["🎯 Strategic Alignment", "📊 Quantifiable Scorecard", "🔌 Data Engineering Notes"])
                    
                    with tab_align:
                        st.markdown(alignment)
                        
                    with tab_kpi:
                        st.markdown(scorecard)
                        st.divider()
                        # Fitur Inovatif: Mockup integrasi ke sistem dokumentasi
                        if st.button("📄 Draft to Confluence Spec (Simulated)", use_container_width=True):
                            st.info("💡 **POC Innovation:** In production, this will push the markdown table directly to a Confluence page for the BI team to pick up as a Power BI / Looker Studio build spec.")
                            
                    with tab_tech:
                        st.markdown(integrations)
    else:
        # Tampilan kosong (placeholder) sebelum tombol ditekan
        st.info("👈 Fill out the requirement brief on the left and click 'Generate KPI Blueprint' to see the magic happen.")