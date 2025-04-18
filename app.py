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

# Custom CSS for modern UI (Glassmorphism design)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background: rgba(16, 18, 27, 0.95) !important;
            backdrop-filter: blur(12px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 32px 64px rgba(0, 0, 0, 0.25);
        }
        
        .stTextInput input, .stSelectbox select, .stTextArea textArea {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .stTextInput input:focus, .stSelectbox select:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
            color: white !important;
            border: none;
            padding: 16px 32px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(99, 102, 241, 0.3);
        }
        
        .stButton > button::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.1),
                transparent
            );
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { left: -50%; }
            100% { left: 150%; }
        }
        
        .stMarkdown h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #6366f1, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
        }
        
        .stAlert {
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .data-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin: 16px 0;
            transition: transform 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .data-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
        }
        
        @media (max-width: 768px) {
            .main { margin: 0.5rem; }
            .stButton > button { width: 100%; }
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
for key in ["search_results", "report", "search_completed", "visualization_data", "agents"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "search_completed" else False

# Main content container
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🔍 AI Search Nexus</h1>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem; color: #94a3b8;'>
                Next-Generation Intelligent Search Platform
            </div>
        """, unsafe_allow_html=True)

        # Search input section
        with st.form(key='search_form'):
            search_query = st.text_input(
                "Enter your search query:",
                placeholder="E.g., Quantum computing breakthroughs 2024",
                key="main_search"
            )
            
            with st.expander("Advanced Settings", expanded=False):
                model_option = st.selectbox(
                    "AI Model Selection:",
                    ["Groq LLM-Groq", "Anthropic Claude 3 Haiku", "Mistral Large", "Llama 3 70B"],
                    index=0
                )
                
                # Model name mapping
                model_name = {
                    "Groq LLM-Groq": "llama3-8b-8192",
                    "Anthropic Claude 3 Haiku": "claude-3-haiku-20240307",
                    "Mistral Large": "mixtral-8x7b-32768",
                    "Llama 3 70B": "llama3-70b-8192"
                }[model_option]
                
                groq_api_key = st.text_input(
                    "Groq API Key:", type="password",
                    placeholder="Enter your API key",
                    help="Required for accessing Groq's AI models"
                )
            
            submitted = st.form_submit_button("🚀 Launch Search", use_container_width=True)

        if submitted:
            if not search_query or not groq_api_key:
                st.error("🔑 Both search query and API key are required!")
            else:
                with st.spinner("🌌 Initializing neural networks..."):
                    llm_config = {
                        "config_list": [{
                            "model": model_name,
                            "api_key": groq_api_key,
                            "base_url": "https://api.groq.com/openai/v1"
                        }],
                        "cache_seed": 42
                    }
                    st.session_state.agents = create_search_agents(llm_config)
                
                progress_bar = st.progress(0, text="🚀 Launching AI agents...")
                status_text = st.empty()

                try:
                    progress_bar.progress(25, text="🔍 Gathering intelligence...")
                    st.session_state.search_results = run_search(
                        st.session_state.agents,
                        search_query,
                        current_date=datetime.now().strftime('%Y-%m-%d')
                    )
                    
                    progress_bar.progress(60, text="📊 Crafting visualizations...")
                    st.session_state.visualization_data = create_visualization(
                        search_query,
                        st.session_state.search_results
                    )
                    
                    progress_bar.progress(80, text="📝 Generating final report...")
                    st.session_state.report = generate_report(
                        st.session_state.agents,
                        st.session_state.search_results
                    )
                    
                    progress_bar.progress(100, text="✅ Mission accomplished!")
                    st.session_state.search_completed = True
                    st.balloons()
                except Exception as e:
                    st.error(f"⚠️ Critical error: {str(e)}")
                    progress_bar.empty()

# Results display
if st.session_state.search_completed:
    with st.container():
        st.markdown("""
            <div class='data-card'>
                <h3 style='margin-bottom: 1rem; color: #6366f1'>📈 Insights Dashboard</h3>
                {}
            </div>
        """.format(display_results(st.session_state.search_results, st.session_state.report, st.session_state.visualization_data)), unsafe_allow_html=True)

    # Export controls
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Export Report (MD)",
            data=st.session_state.report,
            file_name=f"report_{search_query.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        st.download_button(
            label="📊 Export Data (JSON)",
            data=json.dumps(st.session_state.search_results),
            file_name=f"data_{search_query.replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )

# Feature highlights
st.markdown("---")
with st.container():
    st.markdown("""
        <div style='text-align: center; margin: 3rem 0;'>
            <h2>✨ Platform Highlights</h2>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    features = [
        {"icon": "🤖", "title": "Multi-Agent Architecture", "desc": "Collaborative AI agents working in tandem"},
        {"icon": "⚡", "title": "Realtime Processing", "desc": "Groq-powered lightning fast responses"},
        {"icon": "🔮", "title": "Predictive Analytics", "desc": "Advanced forecasting capabilities"},
        {"icon": "🛡️", "title": "Enterprise Security", "desc": "Military-grade encryption"}
    ]
    
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
                <div class='data-card' style='text-align: center; padding: 1.5rem;'>
                    <div style='font-size: 2rem; margin-bottom: 1rem;'>{feature['icon']}</div>
                    <h4>{feature['title']}</h4>
                    <p style='color: #94a3b8; font-size: 0.9rem;'>{feature['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

# Sidebar enhancements
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>🚀 AI Search Nexus</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>v2.1.0</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 Search History")
    # Add search history component here
    
    st.markdown("### 🏆 Leaderboard")
    # Add user statistics component here
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>
            Powered by Groq LPU™ Inference Engine<br>
            © 2024 AI Search Nexus. All rights reserved.
        </div>
    """, unsafe_allow_html=True)