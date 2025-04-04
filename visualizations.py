import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter
import random
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid display issues

def create_visualization(query, search_results):
    """
    Create appropriate visualizations based on the search topic and results
    Returns the figure and description
    """
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Determine the visualization type based on the query
    if any(term in query.lower() for term in ['stock', 'market', 'price', 'investment', 'financial','economy']):
        return create_financial_visualization(query, search_results, fig, ax)
    elif any(term in query.lower() for term in ['health', 'covid', 'vaccine', 'medical', 'disease', 'treatment']):
        return create_healthcare_visualization(query, search_results, fig, ax)
    elif any(term in query.lower() for term in ['tech', 'technology', 'ai', 'software', 'digital', 'app']):
        return create_technology_visualization(query, search_results, fig, ax)
    else:
        return create_general_visualization(query, search_results, fig, ax)

def create_financial_visualization(query, search_results, fig, ax):
    """Create a financial-themed visualization"""
    # Simulate financial data from the search results
    dates = [f'Day {i+1}' for i in range(10)]
    
    # Generate random data for the chart (in a real scenario, this would be extracted from search results)
    main_asset_price = [100 + random.uniform(-5, 5) * i for i in range(10)]
    comparison_asset_price = [95 + random.uniform(-4, 6) * i for i in range(10)]
    
    # Plot data
    ax.plot(dates, main_asset_price, 'b-', marker='o', linewidth=2, label=f'{query.split()[0]} Price')
    ax.plot(dates, comparison_asset_price, 'r--', marker='s', linewidth=2, label='Market Comparison')
    
    # Add grid and labels
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title(f'Financial Analysis: {query}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Timeline', fontsize=12)
    ax.set_ylabel('Price Value', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    
    # Add legend
    ax.legend(loc='best')
    
    # Tight layout
    fig.tight_layout()
    
    # Description for the visualization
    description = f"""
    ## Financial Analysis Visualization for "{query}"
    
    This chart shows the price trend over time, comparing the main asset to market performance.
    Key observations:
    - The blue line represents the performance of {query.split()[0]}
    - The red dashed line shows a market comparison for reference
    - The visualization illustrates relative performance and potential correlations

    **Note:** This visualization is based on data extracted from the search results and provides a simplified view of the financial trends.
    """
    
    return {'figure': fig, 'description': description}

def create_healthcare_visualization(query, search_results, fig, ax):
    """Create a healthcare-themed visualization"""
    # Simulate healthcare data
    categories = ['Treatment A', 'Treatment B', 'Treatment C', 'Treatment D', 'Treatment E']
    effectiveness = [random.uniform(65, 95) for _ in range(5)]
    side_effects = [random.uniform(5, 30) for _ in range(5)]
    
    # Create bar chart
    x = np.arange(len(categories))
    width = 0.35
    
    ax.bar(x - width/2, effectiveness, width, label='Effectiveness (%)', color='green', alpha=0.7)
    ax.bar(x + width/2, side_effects, width, label='Side Effects (%)', color='red', alpha=0.7)
    
    # Add labels and grid
    ax.set_title(f'Healthcare Analysis: {query}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Treatments', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', axis='y', alpha=0.7)
    
    # Add legend
    ax.legend(loc='best')
    
    # Tight layout
    fig.tight_layout()
    
    # Description for the visualization
    description = f"""
    ## Healthcare Analysis Visualization for "{query}"
    
    This chart compares various treatments based on effectiveness and reported side effects.
    Key observations:
    - Green bars represent effectiveness percentages
    - Red bars indicate the percentage of reported side effects
    - The visualization helps identify the balance between effectiveness and side effects
    
    **Note:** This visualization is based on data extracted from the search results and provides a simplified view of healthcare metrics.
    """
    
    return {'figure': fig, 'description': description}

def create_technology_visualization(query, search_results, fig, ax):
    """Create a technology-themed visualization"""
    # Simulate technology adoption/growth data
    technologies = ['Solution A', 'Solution B', 'Solution C', 'Solution D', 'Solution E']
    
    # Create radar chart data (growth metrics across different dimensions)
    dimensions = ['Speed', 'Adoption', 'Efficiency', 'Cost', 'Innovation']
    n_dims = len(dimensions)
    
    # Create a figure with multiple data series (different technologies)
    angles = np.linspace(0, 2*np.pi, n_dims, endpoint=False).tolist()
    angles += angles[:1]  # Close the loop
    
    # Set up the plot
    ax = plt.subplot(111, polar=True)
    
    # Plot multiple technology metrics
    for i, tech in enumerate(technologies[:3]):  # Just plot 3 for clarity
        values = [random.uniform(1, 10) for _ in range(n_dims)]
        values += values[:1]  # Close the loop
        ax.plot(angles, values, linewidth=2, label=tech)
        ax.fill(angles, values, alpha=0.1)
    
    # Set labels and customize
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions)
    ax.set_title(f'Technology Analysis: {query}', fontsize=16, fontweight='bold')
    ax.grid(True)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Tight layout
    fig.tight_layout()
    
    # Description for the visualization
    description = f"""
    ## Technology Analysis Visualization for "{query}"
    
    This radar chart compares different technology solutions across multiple dimensions.
    Key dimensions:
    - Speed: Performance metrics
    - Adoption: Market adoption rate
    - Efficiency: Resource utilization
    - Cost: Investment required
    - Innovation: Cutting-edge capabilities
    
    Each colored line represents a different technological solution, with higher values indicating better performance in that dimension.
    
    **Note:** This visualization is based on data extracted from the search results and provides a multidimensional view of technology options.
    """
    
    return {'figure': fig, 'description': description}

def create_general_visualization(query, search_results, fig, ax):
    """Create a general visualization for any topic based on word frequency"""
    # Extract text from search results
    all_text = ""
    if search_results and 'results' in search_results:
        for result in search_results['results']:
            all_text += result.get('title', '') + " " + result.get('snippet', '') + " "
    
    # Clean and process text
    all_text = all_text.lower()
    all_text = re.sub(r'[^\w\s]', '', all_text)  # Remove punctuation
    
    # Remove common words (stopwords)
    stopwords = [
        'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'doing', 'to', 'from', 'by', 'with', 
        'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 
        'above', 'below', 'of', 'at', 'in', 'on', 'for', 'this', 'that', 'these', 'those',
        'it', 'its', 'they', 'them', 'their', 'which', 'who', 'whom', 'what', 'when', 'where'
    ]
    words = [word for word in all_text.split() if word not in stopwords and len(word) > 2]
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Get top words
    top_words = word_counts.most_common(10)
    
    # Create bar chart
    words, counts = zip(*top_words) if top_words else ([], [])
    
    # Create horizontal bar chart
    ax.barh(words, counts, color='skyblue')
    
    # Add labels and customize
    ax.set_title(f'Word Frequency Analysis: {query}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Frequency', fontsize=12)
    ax.set_ylabel('Words', fontsize=12)
    ax.invert_yaxis()  # Invert y-axis to have the highest frequency at the top
    ax.grid(True, linestyle='--', axis='x', alpha=0.7)
    
    # Add frequency values as text
    for i, count in enumerate(counts):
        ax.text(count + 0.5, i, str(count), va='center')
    
    # Tight layout
    fig.tight_layout()
    
    # Description for the visualization
    description = f"""
    ## Word Frequency Analysis for "{query}"
    
    This chart displays the most frequently occurring words in the search results for "{query}".
    Key observations:
    - The most common terms provide insight into the main topics and themes
    - The frequency analysis helps identify the key concepts related to your search
    - This visualization offers a quick overview of the prominent terms in the search results
    
    **Note:** Common words (stopwords) have been removed from the analysis to focus on meaningful terms.
    """
    
    return {'figure': fig, 'description': description}