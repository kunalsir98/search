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

# Initialize session state variables if they don't exist
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'report' not in st.session_state:
    st.session_state.report = None
if 'search_completed' not in st.session_state:
    st.session_state.search_completed = False
if 'visualization_data' not in st.session_state:
    st.session_state.visualization_data = None
if 'agents' not in st.session_state:
    st.session_state.agents = None

# Title and description
st.title("🔍 Multi-Agent AI Search-Engine by kunal")
st.markdown("""
This advanced search engine utilizes multiple AI agents to:
1. Retrieve information from across the web
2. Analyze and summarize findings
3. Generate comprehensive reports
4. Create data visualizations

Enter a topic below to begin your search!
""")

# Input for search query
search_query = st.text_input("Enter your search topic:", 
                          placeholder="E.g., Tesla stock price, COVID-19 vaccines, AI advancements")

# Toggle for advanced options
show_advanced = st.checkbox("Show advanced options")

# Model selection
if show_advanced:
    model_option = st.selectbox(
        "Select LLM Model:",
        ["Groq LLM-Groq", "Anthropic Claude 3 Haiku", "Mistral Large", "Llama 3 70B"],
        index=0
    )
    
    if model_option == "Groq LLM-Groq":
        model_name = "llama3-8b-8192"
    elif model_option == "Anthropic Claude 3 Haiku":
        model_name = "claude-3-haiku-20240307"
    elif model_option == "Mistral Large":
        model_name = "mixtral-8x7b-32768"
    elif model_option == "Llama 3 70B":
        model_name = "llama3-70b-8192"
    else:
        model_name = "llama3-8b-8192"  # Default model
else:
    model_name = "llama3-8b-8192"  # Default model

# Groq API key input
groq_api_key = st.text_input("Enter your Groq API key:", 
                           type="password", 
                           placeholder="gsk_...")

st.markdown("""
> **Note**: You need a Groq API key to use this application. If you don't have one, you can get a free key by signing up at [groq.com](https://www.groq.com).
""")

# Search button
if st.button("Search", disabled=not search_query or not groq_api_key):
    with st.spinner("Initializing AI agents..."):
        # Configure LLM with Groq
        llm_config = {
            "config_list": [{"model": model_name, "api_key": groq_api_key, "base_url": "https://api.groq.com/openai/v1"}],
            "cache_seed": 42
        }
        
        # Create and store agents
        agents = create_search_agents(llm_config)
        st.session_state.agents = agents
    
    with st.spinner(f"Searching for information about '{search_query}'..."):
        try:
            # Run the search with the query
            st.session_state.search_results = run_search(
                agents, 
                search_query, 
                current_date=datetime.now().strftime('%Y-%m-%d')
            )
            st.session_state.search_completed = True
            
            # Generate visualization data if applicable
            st.session_state.visualization_data = create_visualization(search_query, st.session_state.search_results)
            
            # Generate report
            st.session_state.report = generate_report(agents, st.session_state.search_results)
            
            st.success("Search completed! Displaying results below.")
        except Exception as e:
            st.error(f"An error occurred during the search: {str(e)}")

# Display results section (only shows if search has been completed)
if st.session_state.search_completed:
    display_results(
        st.session_state.search_results, 
        st.session_state.report, 
        st.session_state.visualization_data
    )
    
    # Export button
    if st.download_button(
        label="Download Report as Markdown",
        data=st.session_state.report,
        file_name=f"report_{search_query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    ):
        st.success("Report downloaded successfully!")

# Footer
st.markdown("---")
st.markdown("""
**How it works:** This app uses AutoGen to coordinate multiple AI agents working together:
- A Researcher agent that retrieves information
- A Writer agent that crafts well-structured reports
- Multiple review agents that ensure quality, consistency, and accuracy
- Visualization capabilities for relevant data

**Powered by Groq** for fast, efficient AI processing through their API.
""")

# Sidebar with information
with st.sidebar:
    st.header("About This Application")
    st.markdown("""
    This Multi-Agent AI Search Engine uses a system of specialized AI agents to search,
    analyze, and report on any topic you're interested in.
    
    ### Key Features
    - **Web Information Retrieval**: Gets relevant data from multiple sources
    - **AI-Powered Analysis**: Processes and makes sense of complex information
    - **Visualization**: Creates charts and graphs to illustrate key points
    - **Comprehensive Reports**: Generates well-structured, detailed reports
    
    ### Using the App
    1. Enter your search topic in the search field
    2. Enter your Groq API key
    3. Click "Search" to start the process
    4. View and download your results
    
    ### Models Available
    - **Llama 3 (8B)**: Default model, good balance of speed and quality
    - **Claude 3 Haiku**: Fast and efficient for most tasks
    - **Mixtral 8x7B**: Strong analytical capabilities
    - **Llama 3 (70B)**: Most powerful option for complex analysis
    
    All processing is done via the Groq API for optimal speed and performance.
    """)