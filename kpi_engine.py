# kpi_engine.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompt_config import KPI_SYSTEM_PROMPT

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_kpi_scorecard(department, objectives, data_sources):
    """
    Mengirimkan konteks bisnis ke Gemini API untuk menghasilkan modul KPI yang presisi.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash", 
            system_instruction=KPI_SYSTEM_PROMPT
        )
        
        # Menyusun user prompt yang padat konteks
        user_context = f"""
        DEPARTMENT / ROLE: {department}
        BUSINESS OBJECTIVES: {objectives}
        CURRENT AVAILABLE DATA SOURCES: {data_sources}
        """
        
        response = model.generate_content(user_context)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def parse_kpi_response(response_text):
    """
    Memotong teks output AI berdasarkan tag khusus untuk dimasukkan ke tab UI.
    """
    try:
        if "[STRATEGIC_ALIGNMENT]" not in response_text:
            return response_text, "Failed to parse KPI Table.", "Failed to parse Integrations."
            
        parts = response_text.split("[STRATEGIC_ALIGNMENT]")
        content_after_alignment = parts[1]
        
        table_split = content_after_alignment.split("[KPI_TABLE]")
        alignment_text = table_split[0].strip()
        
        integration_split = table_split[1].split("[ACTIONABLE_INTEGRATIONS]")
        table_text = integration_split[0].strip()
        integration_text = integration_split[1].strip()
        
        return alignment_text, table_text, integration_text
    except Exception as e:
        return response_text, "Error parsing table data.", "Error parsing integration data."