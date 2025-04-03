import streamlit as st
import os
import json
from datetime import datetime
import autogen
from utils import setup_page, display_results
from search_engine import create_search_agents, run_search
from report_generator import generate_report
from visualizations import create_visualization

# Create a folder for code execution if it doesn't exist
if not os.path.exists("coding"):
    os.makedirs("coding")

# Page configuration
setup_page()

# Custom CSS for aesthetic UI (Dark mode with interactive design)
st.markdown("""
    <style>
        body { font-family: 'Poppins', sans-serif; }
        .main {
            background-color: #1e1e2e;
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        }
        .stTextInput, .stSelectbox, .stCheckbox, .stButton > button {
            border-radius: 12px;
            padding: 14px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            font-size: 18px;
            font-weight: bold;
            transition: background 0.3s, transform 0.2s;
            border: none;
            padding: 14px 20px;
            border-radius: 8px;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
        }
        .stButton > button:hover {
            background-color: #0056b3;
            transform: scale(1.07);
        }
        .stMarkdown, .stTitle { text-align: center; }
        
        @media (max-width: 768px) {
            .main { padding: 15px; }
            .stButton > button { font-size: 16px; padding: 12px 18px; }
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
for key in ["search_results", "report", "search_completed", "visualization_data", "agents"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "search_completed" else False

# Title and description
st.title("🔍 AI-Powered Multi-Agent Search Engine")
st.markdown("""
    **🚀 Experience an interactive search with AI agents that:**
    - Retrieve and analyze real-time data
    - Summarize key insights into reports
    - Generate rich, interactive visualizations
    
    **Start your intelligent search now!**
""")

# Input for search query
search_query = st.text_input(
    "Enter your search topic:", placeholder="E.g., Tesla stock price, COVID-19 vaccines, AI advancements"
)

# Advanced options toggle
show_advanced = st.checkbox("Show advanced options")

# Model selection dropdown
if show_advanced:
    model_option = st.selectbox(
        "Select LLM Model:",
        ["Groq LLM-Groq", "Anthropic Claude 3 Haiku", "Mistral Large", "Llama 3 70B"],
        index=0
    )
    model_name = {
        "Groq LLM-Groq": "llama3-8b-8192",
        "Anthropic Claude 3 Haiku": "claude-3-haiku-20240307",
        "Mistral Large": "mixtral-8x7b-32768",
        "Llama 3 70B": "llama3-70b-8192"
    }.get(model_option, "llama3-8b-8192")
else:
    model_name = "llama3-8b-8192"

# API key input
groq_api_key = st.text_input(
    "Enter your Groq API key:", type="password", placeholder="gsk_..."
)

st.info("🔑 You need a Groq API key to use this application. Get one at [groq.com](https://www.groq.com).")

# Search button
if st.button("🚀 Start Search", disabled=not search_query or not groq_api_key):
    with st.spinner("🔄 Initializing AI agents..."):
        llm_config = {"config_list": [{"model": model_name, "api_key": groq_api_key, "base_url": "https://api.groq.com/openai/v1"}], "cache_seed": 42}
        st.session_state.agents = create_search_agents(llm_config)
    
    with st.spinner(f"🔎 Searching for '{search_query}'..."):
        try:
            st.session_state.search_results = run_search(st.session_state.agents, search_query, current_date=datetime.now().strftime('%Y-%m-%d'))
            st.session_state.visualization_data = create_visualization(search_query, st.session_state.search_results)
            st.session_state.report = generate_report(st.session_state.agents, st.session_state.search_results)
            st.session_state.search_completed = True
            st.success("✅ Search completed! Displaying results below.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Display results
if st.session_state.search_completed:
    display_results(st.session_state.search_results, st.session_state.report, st.session_state.visualization_data)
    
    # Export button
    if st.download_button(
        label="📥 Download Report as Markdown",
        data=st.session_state.report,
        file_name=f"report_{search_query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    ):
        st.success("✅ Report downloaded successfully!")

# Footer
st.markdown("---")
st.markdown("""
    **🛠️ How It Works:**
    - **Researcher AI** gathers relevant data.
    - **Writer AI** structures the report.
    - **Reviewers** ensure accuracy & consistency.
    - **Visualization Engine** creates meaningful, interactive charts.

    **🚀 Powered by Groq for ultra-fast AI processing.**
""")

# Sidebar with app info
with st.sidebar:
    st.header("📌 About This App")
    st.markdown("""
    **Multi-Agent AI Search Engine** uses smart AI agents to search, analyze, and summarize any topic.
    
    🏆 **Key Features**
    - Web info retrieval
    - AI-powered analysis
    - Data visualizations
    - Detailed reports
    
    🎯 **How to Use**
    1. Enter your search topic
    2. Provide your Groq API key
    3. Click **Start Search**
    4. View & download the results
    
    🔥 **Available AI Models**
    - **Llama 3 (8B & 70B)**
    - **Claude 3 Haiku**
    - **Mixtral 8x7B**
    
    **All processing is powered by Groq API.**
""")
