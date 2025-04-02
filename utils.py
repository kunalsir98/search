import streamlit as st 
import os
import base64
import io
from datetime import datetime

def setup_page():
    """Configure the Streamlit page settings with a modern UI."""
    st.set_page_config(
        page_title="Multi-Agent AI Search Engine",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Enhanced styling for better UI
    st.markdown("""
    <style>
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f4f4f4;
    }
    .stApp {
        padding: 2rem;
    }
    .block-container {
        max-width: 1100px;
        margin: auto;
    }
    h1 {
        text-align: center;
        font-size: 2.5rem;
        color: #333;
    }
    .stButton>button {
        background-color: #6C63FF;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #574bff;
    }
    .search-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .result-card {
        border-left: 4px solid #6C63FF;
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .source-badge {
        background-color: #6C63FF;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_image_download_link(fig, filename="visualization.png", text="Download Visualization"):
    """Generate a styled link to download a matplotlib figure."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    href = f'<a href="data:image/png;base64,{image_base64}" download="{filename}" class="stButton">{text}</a>'
    return href

def display_results(search_results, report, visualization_data):
    """Display search results, report, and visualizations in a structured format."""
    tabs = st.tabs(["📊 Report", "🔍 Search Results", "📈 Visualization"])
    
    with tabs[0]:
        st.markdown("<div class='search-card'>", unsafe_allow_html=True)
        st.markdown(report, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.header("Search Results from Multiple Sources")
        if search_results and 'results' in search_results:
            for result in search_results['results']:
                with st.expander(f"{result.get('title', 'No title')}"):
                    st.markdown(f"""
                    <div class='result-card'>
                        <h4>{result.get('title', 'No title')}</h4>
                        <p><strong>Link:</strong> <a href="{result.get('link', '#')}" target="_blank">{result.get('link', '#')}</a></p>
                        <p><strong>Snippet:</strong> {result.get('snippet', 'No snippet')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No search results available.")
    
    with tabs[2]:
        st.header("Data Visualization")
        if visualization_data and 'figure' in visualization_data:
            st.pyplot(visualization_data['figure'])
            st.markdown(get_image_download_link(visualization_data['figure']), unsafe_allow_html=True)
        else:
            st.warning("No visualization available.")
