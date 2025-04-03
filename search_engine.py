import autogen
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import random

def create_search_agents(llm_config):
    """Create and configure all the necessary agents for the search engine"""
    
    # AI task assistant
    ai_task_assistant = autogen.AssistantAgent(
        name='Ai_task_assistant',
        llm_config=llm_config,
    )

    # Research assistant
    research_assistant = autogen.AssistantAgent(
        name='Researcher',
        llm_config=llm_config,
        system_message="""
            You are a skilled research agent specialized in gathering timely and relevant information.
            Your task is to:
            1. Search for current information on the requested topic
            2. Gather at least 10 relevant news headlines or information points
            3. Organize the information in a structured format
            4. Be thorough and verify information before presenting it
            
            If the topic relates to financial markets, gather relevant stock prices, trends and news.
            If the topic relates to healthcare, gather latest studies, statistics and breakthroughs.
            For technology topics, focus on innovations, company news, and market trends.
            For Art and Culture, focus on latest Ancient Discovery, Historical culture, Historical inovations.
            For Entertainment ,focus on Top 10 movies in world, entertainment news, Celibrity Information and various other things.
            For Sports, focus on Track live scores and upcoming matches,Provide player and team statistics,Predict match outcomes using AI models,Analyze historical sports trends,Recommend training programs and techniques for athletes.
            For Top News Live Provide real-time updates on global and regional news,Categorize news into Business, Politics, Technology, Health, and more,Summarize key headlines and breaking stories,Offer AI-driven sentiment analysis of trending news,Allow users to personalize their news feed based on interests.
        """
    )

    # Writer
    writer = autogen.AssistantAgent(
        name='writer',
        llm_config=llm_config,
        system_message="""
            You are a professional writer, known for your engaging, data-driven, and insightful reports.  
            Your goal is to craft well-structured, analytical, and compelling content based on the provided information.  
            
            🔹 Writing Objectives:  
            - Present a clear, structured, and professional report.  
            - Ensure accuracy, coherence, and data-driven insights.  
            - Use engaging storytelling and real-world examples when possible.  
            - Maintain a logical flow with appropriate headings and subheadings.  
            - If visuals (charts, tables, figures) are provided, refer to them in the analysis.  

            🔹 Financial & Market Analysis:  
            - Summarize market trends, stock performances, and financial news.  
            - Compare key fundamental ratios and provide insights.  
            - Identify risks, opportunities, and future trends.  
            - If data is missing, suggest alternative research approaches.  

            🔹 Technology & Healthcare Reports:  
            - Analyze the latest tech advancements, medical innovations, and scientific breakthroughs.  
            - Compare companies, treatments, or strategies in a concise yet detailed manner.  
            - Offer insights into future developments and potential impacts.  

            🔹 Marketing & Business Analysis:  
            - Evaluate customer behavior, market dynamics, and competitive strategies.  
            - Provide a comparative analysis of businesses, campaigns, or trends.  
            - Recommend actionable strategies for better business growth.  

            🔹Art and Culture:
            - Evaluate Ancient art and Technologies.
            - Analyze and compare different ancient art styles?
            -Provide historical context on ancient technologies?
            -Use AI to restore or recreate ancient artworks?
            -Suggest modern applications of ancient technologies?
            
            🔹Entertainment
            -Recommend movies, music, and books based on user preferences.
            -Analyze trends in cinema, music, and gaming.
            -Generate AI-driven scripts, lyrics, or creative content.
            -Track box office performance and music charts.
            -Provide behind-the-scenes insights into entertainment industries

            🔹Sports
            -Track live scores and upcoming matches.
            -Provide player and team statistics.
            -Predict match outcomes using AI models.
            -Analyze historical sports trends.
            -Recommend training programs and techniques for athletes.

            🔹Top News Live
            -Provide real-time updates on global and regional news.
            -Categorize news into Business, Politics, Technology, Health, and more.
            -Summarize key headlines and breaking stories.
            -Offer AI-driven sentiment analysis of trending news.
            -Allow users to personalize their news feed based on interests.

            🔹 Writing Guidelines:  
            - Use precise, engaging, and professional language.  
            - Break down complex concepts into easy-to-understand sections.  
            - Always summarize key takeaways in a conclusion.  

        """
    )

    # Critic agent
    critic = autogen.AssistantAgent(
        name="Critic",
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
        llm_config=llm_config,
        system_message="""
            You are a critical reviewer, responsible for evaluating the overall quality of the written content.  
            Your goal is to ensure clarity, coherence, depth, and relevance of the report.  

            🔹 Review Guidelines:  
            - Provide constructive feedback for improvement.  
            - Identify unclear sections, missing insights, or logical flaws.  
            - Check for concise, professional, and engaging language.  
            - Suggest enhancements in data interpretation and structure.  
        """
    )

    # Legal Reviewer
    legal_reviewer = autogen.AssistantAgent(
        name="Legal_Reviewer",
        llm_config=llm_config,
        system_message="""
            You are a legal compliance reviewer, responsible for ensuring the content is legally sound.  

            🔹 Review Guidelines:  
            - Identify potential legal issues, such as misinformation or risky claims.  
            - Ensure compliance with financial, healthcare, and data privacy regulations.  
            - Provide precise, to-the-point feedback in just 3 bullet points.  
            - Begin the review by clearly stating your role.  
        """
    )

    # Consistency Reviewer
    consistency_reviewer = autogen.AssistantAgent(
        name="Consistency_Reviewer",
        llm_config=llm_config,
        system_message="""
            You are a consistency reviewer, responsible for ensuring that data and facts remain uniform throughout the report.  

            🔹 Review Guidelines:  
            - Check for contradictions in numbers, data, and statements.  
            - Ensure consistency in terminology, formatting, and references.  
            - If multiple versions of a fact exist, determine the most accurate one.  
            - Provide concise, structured feedback in 3 bullet points.  
            - Begin the review by clearly stating your role.  
        """
    )

    # Text Alignment Reviewer
    textalignment_reviewer = autogen.AssistantAgent(
        name="Text_Alignment_Reviewer",
        llm_config=llm_config,
        system_message="""
            You are a text alignment reviewer, ensuring that narrative descriptions accurately reflect numerical data.  

            🔹 Review Guidelines:  
            - Verify that the written text aligns correctly with the figures and statistics.  
            - Identify discrepancies between textual claims and numerical insights.  
            - Ensure that key financial and statistical references are clear and correct.  
            - Provide concise, structured feedback in 3 bullet points.  
            - Begin the review by clearly stating your role.  
        """
    )

    # Completion Reviewer
    completion_reviewer = autogen.AssistantAgent(
        name="Completion_Reviewer",
        llm_config=llm_config,
        system_message="""
            You are a content completion reviewer, ensuring that all required elements are present in financial reports.  

            🔹 Required Elements:  
            - A news report on each relevant asset.  
            - A table comparing fundamental ratios.  
            - A description of price trends and risks.  
            - An analysis of possible future scenarios.  
            - At least one visual representation (chart, graph, or figure).  

            🔹 Review Guidelines:  
            - Ensure the report contains all essential elements.  
            - Identify any missing data, sections, or critical insights.  
            - Provide concise, structured feedback in 3 bullet points.  
            - Begin the review by clearly stating your role.  
        """
    )

    # Meta Reviewer
    meta_reviewer = autogen.AssistantAgent(
        name="Meta_Reviewer",
        llm_config=llm_config,
        system_message="""
            You are a meta reviewer, responsible for aggregating feedback from all reviewers and providing a final assessment.  

            🔹 Review Process:  
            - Synthesize all reviewers' insights into a final, balanced critique.  
            - Prioritize major issues, contradictions, and gaps.  
            - Ensure the report meets high professional and analytical standards.  
            - Provide a structured summary of all key improvements needed.  
        """
    )

    # Export Assistant
    export_assistant = autogen.AssistantAgent(
        name='Exporter',
        llm_config=llm_config,
        system_message="""
            You are responsible for saving the final report to a markdown file.
            Make sure all formatting is preserved and the file is properly named.
        """
    )

    # User Proxy
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "coding",
            "use_docker": False,
        },
    )

    # Set up reviewer chat flow
    def reflection_message(recipient, messages, sender, config):
        return f'''Review the following content. 
                \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

    review_chats = [
        {
            "recipient": legal_reviewer, 
            "message": reflection_message, 
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Return review into a JSON object only: {'Reviewer': '', 'Review': ''}."
            },
            "max_turns": 1
        },
        {
            "recipient": textalignment_reviewer, 
            "message": reflection_message, 
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Return review into a JSON object only: {'reviewer': '', 'review': ''}"
            },
            "max_turns": 1
        },
        {
            "recipient": consistency_reviewer, 
            "message": reflection_message, 
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Return review into a JSON object only: {'reviewer': '', 'review': ''}"
            },
            "max_turns": 1
        },
        {
            "recipient": completion_reviewer, 
            "message": reflection_message, 
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Return review into a JSON object only: {'reviewer': '', 'review': ''}"
            },
            "max_turns": 1
        },
        {
            "recipient": meta_reviewer, 
            "message": "Aggregate feedback from all reviewers and give final suggestions on the writing.", 
            "max_turns": 1
        },
    ]

    critic.register_nested_chats(
        review_chats,
        trigger=writer,
    )

    return {
        "ai_task_assistant": ai_task_assistant,
        "research_assistant": research_assistant,
        "writer": writer,
        "critic": critic,
        "legal_reviewer": legal_reviewer,
        "consistency_reviewer": consistency_reviewer,
        "textalignment_reviewer": textalignment_reviewer,
        "completion_reviewer": completion_reviewer,
        "meta_reviewer": meta_reviewer,
        "export_assistant": export_assistant,
        "user_proxy": user_proxy
    }

def search_web(query, num_results=15):
    """
    Perform a comprehensive web search for the given query and return results from multiple sources
    """
    search_results = []
    
    # Try multiple search sources to get diverse results
    google_results = search_google(query, num_results=num_results//2)
    search_results.extend(google_results)
    
    # Try to fetch additional data from other sources
    wikipedia_results = search_wikipedia(query, num_results=3)
    search_results.extend(wikipedia_results)
    
    news_results = search_news(query, num_results=num_results//3)
    search_results.extend(news_results)
    
    # Remove any duplicates based on URLs
    seen_urls = set()
    unique_results = []
    for result in search_results:
        if result['link'] not in seen_urls:
            seen_urls.add(result['link'])
            unique_results.append(result)
    
    # Return the top results
    return unique_results[:num_results]

def search_google(query, num_results=10):
    """Search Google for the given query"""
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    
    # Headers to mimic a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract search results
        search_results = []
        for result in soup.select('div.g'):
            title_element = result.select_one('h3')
            link_element = result.select_one('a')
            snippet_element = result.select_one('div.IsZvec')
            
            if title_element and link_element and snippet_element:
                title = title_element.text
                link = link_element['href'] if link_element.has_attr('href') else ""
                snippet = snippet_element.text
                
                # Fix Google redirects if present
                if isinstance(link, str) and link.startswith('/url?q='):
                    link = link.split('/url?q=')[1].split('&')[0]
                
                search_results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'source': 'Google Search'
                })
                
                if len(search_results) >= num_results:
                    break
        
        return search_results
    except Exception as e:
        print(f"Error searching Google: {str(e)}")
        return []

def search_wikipedia(query, num_results=3):
    """Search Wikipedia for the given query"""
    # Format the query for Wikipedia search
    search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={quote_plus(query)}&limit={num_results}&namespace=0&format=json"
    
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Wikipedia API returns a list of 4 lists: [query, titles, descriptions, urls]
        titles = data[1]
        descriptions = data[2]
        urls = data[3]
        
        search_results = []
        for i in range(min(len(titles), len(descriptions), len(urls))):
            title = titles[i]
            snippet = descriptions[i]
            link = urls[i]
            
            # Fetch a bit more content for the snippet if it's too short
            if len(snippet) < 100:
                try:
                    article_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles={quote_plus(title)}&format=json"
                    article_response = requests.get(article_url, timeout=10)
                    article_data = article_response.json()
                    
                    # Extract the page content
                    pages = article_data['query']['pages']
                    page_id = list(pages.keys())[0]
                    if 'extract' in pages[page_id]:
                        extract = pages[page_id]['extract']
                        snippet = extract[:250] + "..." if len(extract) > 250 else extract
                except Exception as e:
                    print(f"Error fetching Wikipedia article: {str(e)}")
            
            search_results.append({
                'title': title,
                'link': link,
                'snippet': snippet,
                'source': 'Wikipedia'
            })
        
        return search_results
    except Exception as e:
        print(f"Error searching Wikipedia: {str(e)}")
        return []

def search_news(query, num_results=5):
    """Search for news related to the query"""
    # Simulate fetching news results from Google News
    search_url = f"https://news.google.com/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract news articles
        search_results = []
        articles = soup.select('article')
        
        for article in articles[:num_results]:
            try:
                # Extract title
                title_element = article.select_one('h3 a, h4 a')
                if not title_element:
                    continue
                title = title_element.text
                
                # Extract link
                link = title_element.get('href', '')
                if link and isinstance(link, str) and link.startswith('./'):
                    link = f"https://news.google.com{link[1:]}"
                
                # Extract snippet
                snippet_element = article.select_one('p, span.HO8did')
                snippet = snippet_element.text if snippet_element else "News article related to the search query."
                
                # Add time if available
                time_element = article.select_one('time')
                if time_element:
                    time_text = time_element.get('datetime', '') or time_element.text
                    snippet = f"{time_text} - {snippet}"
                
                search_results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'source': 'News'
                })
            except Exception as e:
                print(f"Error parsing news article: {str(e)}")
                continue
                
        return search_results
    except Exception as e:
        print(f"Error searching News: {str(e)}")
        return []

def run_search(agents, query, current_date):
    """Execute the search using the multi-agent system"""
    
    # Format the AI task prompt
    ai_task_prompt = f"""
    Today is {current_date}.
    You are an advanced AI agent capable of retrieving, analyzing, and summarizing information across multiple domains, including stock markets, finance, marketing, technology, healthcare, and more.

    ### Your Tasks:  
    1. Information Retrieval:  
       - Search for the latest news headlines and trends related to: {query}  
       - Retrieve at least 10 relevant news headlines for the given topic.  
       - If the initial search results are unclear, modify the query and retry.  
       - Do not use solutions that require an API key.  

    2. Detailed Report Generation:  
       - Provide a well-structured, insightful summary of the retrieved information.  
       - Include relevant data points, key insights, and explanations.  

    3. Data Visualization:  
       - Generate and save relevant visualizations based on the retrieved data.  
       - If the topic is related to stock prices, plot price trends.  
       - If related to healthcare, show relevant statistical insights.  

    4. Smart Search Engine Behavior:  
       - Act as an AI-powered search engine, fetching reliable information across multiple domains.  
       - Ensure accuracy by verifying sources before presenting data.  

    Rules & Constraints:  
    - Do not use APIs that require an API key.  
    - If data is unclear or incomplete, refine the search query and try again.  
    """
    
    writing_task = """Develop a comprehensive and engaging report based on all the provided information. 
       
       🔹 Key Requirements:  
       - Rely primarily on the given data and figures.  
       - Include any relevant figures (e.g., charts, visualizations, or saved images).  
       - Organize the report in a structured, professional format.  

       🔹 Financial Analysis (if applicable):  
       - Create a comparative table of fundamental ratios, financial metrics, or stock performance.  
       - Provide comments and interpretations of financial ratios and stock trends.  
       - Analyze stock correlations, risks, and investment opportunities.  
       - Summarize recent financial news and their potential impact on the market.  
       - Connect news trends with fundamental financial metrics to provide deeper insights.  
       - Offer predictions and possible future market scenarios based on data.  

       🔹 Healthcare & Technology Analysis (if applicable):  
       - Summarize breakthroughs, trends, or innovations in the field.  
       - Compare technologies, treatments, or companies based on provided metrics.  
       - Analyze potential future developments and market impacts.  

       🔹 Marketing & Business Analysis (if applicable):  
       - Evaluate market trends, customer behavior, and industry shifts.  
       - Compare key marketing strategies, advertising approaches, or consumer insights.  
       - Offer strategic recommendations for business growth.  

       🔹 General Guidelines:  
       - Ensure all data-driven insights are clear and well-explained.  
       - Write in a professional, analytical, and engaging tone.  
       - Summarize key takeaways in a concise conclusion section. 

       🔹Art and Culture:
        - Evaluate Ancient art and Technologies.
        - Analyze and compare different ancient art styles?
        -Provide historical context on ancient technologies?
        -Use AI to restore or recreate ancient artworks?
        -Suggest modern applications of ancient technologies?
            
        🔹Entertainment
        -Recommend movies, music, and books based on user preferences.
        -Analyze trends in cinema, music, and gaming.
        -Generate AI-driven scripts, lyrics, or creative content.
        -Track box office performance and music charts.
        -Provide behind-the-scenes insights into entertainment industries

        🔹Sports
        -Track live scores and upcoming matches.
        -Provide player and team statistics.
        -Predict match outcomes using AI models.
        -Analyze historical sports trends.
        -Recommend training programs and techniques for athletes.

        🔹Top News Live
        -Provide real-time updates on global and regional news.
        -Categorize news into Business, Politics, Technology, Health, and more.
         -Summarize key headlines and breaking stories.
        -Offer AI-driven sentiment analysis of trending news.
        -Allow users to personalize their news feed based on interests.
 
    """
    
    # In a real implementation, we would use the agents to perform the search
    # For now, we'll simulate the search with our search_web function
    search_results = search_web(query)
    
    # Prepare the results to return
    result_package = {
        'query': query,
        'search_date': current_date,
        'results': search_results,
        'analysis_prompt': writing_task
    }
    
    return result_package