# Home.py - Main Landing Page with Twitter Theme
import streamlit as st
import pandas as pd
from datetime import datetime
# Change
st.set_page_config(
    page_title="Twitter Sentiment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Twitter Theme
st.markdown("""
    <style>
        /* Twitter Color Scheme */
        :root {
            --twitter-blue: #1DA1F2;
            --twitter-dark: #0f1419;
            --twitter-light: #f7f9fa;
            --twitter-border: #eff3f4;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1DA1F2 0%, #1a91da 100%);
            padding-top: 20px;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: white !important;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: white !important;
            font-weight: 600;
            font-size: 16px;
            padding: 10px 15px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        
        [data-testid="stSidebar"] .stRadio > label:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        [data-testid="stSidebar"] .stRadio > div {
            background-color: transparent;
        }
        
        /* Main content area */
        .main-container {
            background-color: #f7f9fa;
            padding: 20px;
        }
        
        /* Header Styling */
        .header-container {
            background: linear-gradient(135deg, #1DA1F2 0%, #1a91da 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(29, 161, 242, 0.3);
        }
        
        .header-title {
            font-size: 3em;
            font-weight: bold;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .header-subtitle {
            font-size: 1.3em;
            margin-top: 10px;
            opacity: 0.95;
        }
        
        /* Metric Cards */
        .metric-container {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #1DA1F2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(29, 161, 242, 0.2);
        }
        
        .metric-label {
            color: #657786;
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #1DA1F2;
        }
        
        /* Info Cards */
        .info-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #eff3f4;
            margin-bottom: 15px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(29, 161, 242, 0.2);
            border-color: #1DA1F2;
        }
        
        .info-card h3 {
            color: #1DA1F2;
            margin-top: 0;
            font-size: 1.3em;
        }
        
        .info-card p {
            color: #0f1419;
            line-height: 1.6;
        }
        
        /* Section Headers */
        .section-header {
            color: #1DA1F2;
            font-size: 1.8em;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #1DA1F2;
        }
        
        /* Story Text */
        .story-text {
            color: #0f1419;
            font-size: 1.05em;
            line-height: 1.8;
            margin: 15px 0;
            padding: 15px;
            background: #f7f9fa;
            border-left: 3px solid #1DA1F2;
            border-radius: 5px;
        }
        
        /* Success Message */
        .success-message {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
            margin-top: 20px;
        }
        
        /* Divider */
        .divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #1DA1F2, transparent);
            margin: 30px 0;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #657786;
            font-size: 0.9em;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid #eff3f4;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation with Twitter Theme
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <p style='color: white; font-size: 1.2em; font-weight: bold; margin: 10px 0;'>Twitter Sentiment</p>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.9em; margin: 0;'>Analysis Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add CSS to style the sidebar radio buttons
    st.markdown("""
        <style>
            [data-testid="stSidebar"] .stRadio > label {
                color: white !important;
            }
            [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("./Data/twitter_dataset.csv")
    return df

try:
    df = load_data()
    
    # Header
    st.markdown("""
        <div class='header-container'>
            <h1 class='header-title'>Twitter Sentiment Intelligence Dashboard</h1>
            <p class='header-subtitle'>Understanding emotions, engagement, and trends in real-time conversations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Story Introduction
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 25px; margin-bottom: 30px; 
                    border-left: 5px solid #1DA1F2; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <p style='color: #0f1419; font-size: 1.05em; line-height: 1.8; margin: 0;'>
                <strong>Welcome to our analysis journey.</strong> Every day, millions of conversations happen on Twitter. 
                Our platform analyzes these conversations to understand what people think, feel, and share. This dashboard 
                tells the story of sentiment patterns, user engagement, and the hidden dynamics behind social media interactions. 
                Whether it's discovering what resonates with audiences or identifying emerging trends, we've equipped you with 
                the tools to see the bigger picture.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick Overview Section
    st.markdown("<h2 class='section-header'>The Numbers Behind the Story</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='story-text'>
            Let's start with the fundamentals. Below you'll see the scale of our analysis - how many conversations 
            we're examining, who's participating, and how much engagement they're generating. These numbers form the 
            foundation of all insights that follow.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Total Conversations</div>
                <div class='metric-value'>{len(df):,}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 5px;'>tweets analyzed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Unique Voices</div>
                <div class='metric-value'>{df['Username'].nunique():,}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 5px;'>participants</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Expressions of Support</div>
                <div class='metric-value'>{df['Likes'].sum():,.0f}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 5px;'>total likes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Message Amplification</div>
                <div class='metric-value'>{df['Retweets'].sum():,.0f}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 5px;'>times shared</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Main Features Section
    st.markdown("<h2 class='section-header'>Your Exploration Path</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='story-text'>
            This dashboard is organized to guide you through a complete understanding of Twitter sentiment. 
            Each section builds on the previous one, revealing deeper insights about how people communicate and 
            what makes content resonate.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='info-card'>
                <h3>Sentiment Analysis</h3>
                <p>Start here to understand the emotional landscape. We classify conversations into positive, 
                negative, and neutral sentiments, revealing the overall tone of discussions and how sentiment 
                varies across topics.</p>
            </div>
            
            <div class='info-card'>
                <h3>Text Analysis</h3>
                <p>Discover what people are actually talking about. Through word frequency analysis and topic 
                visualization, we reveal the linguistic patterns and themes that drive engagement in conversations.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='info-card'>
                <h3>Engagement Metrics</h3>
                <p>See what works. By analyzing likes and retweets, we identify which types of content resonate 
                most with audiences, and how sentiment influences engagement levels.</p>
            </div>
            
            <div class='info-card'>
                <h3>User & Temporal Insights</h3>
                <p>Meet the influencers and understand timing. We identify key users driving conversations and reveal 
                when engagement peaks, helping you understand both who and when matter most.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Key Insights
    st.markdown("<h2 class='section-header'>Quick Insights</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='story-text'>
            Before diving deeper, here are some quick statistics about what we're seeing in the data. 
            These metrics give you an instant sense of engagement levels and participation patterns.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_likes = df['Likes'].mean()
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Average Appreciation</div>
                <div class='metric-value'>{avg_likes:.0f}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 5px;'>likes per conversation</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_retweets = df['Retweets'].mean()
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Average Reach</div>
                <div class='metric-value'>{avg_retweets:.0f}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 5px;'>shares per conversation</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        date_range = f"{df['Timestamp'].min()[:10]} to {df['Timestamp'].max()[:10]}"
        st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-label'>Analysis Period</div>
                <div style='color: #0f1419; font-weight: bold; font-size: 1em; margin-top: 5px;'>{date_range}</div>
                <div style='color: #657786; font-size: 0.85em; margin-top: 8px;'>temporal scope</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Navigation Guide
    st.markdown("<h2 class='section-header'>How to Use This Dashboard</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='story-text'>
            Use the navigation sidebar on the left to explore different sections. Each page is designed to tell 
            a specific part of the story, complete with interactive visualizations that let you drill down into 
            the details that matter to you. Feel free to interact with charts, apply filters, and export data for 
            further analysis.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='info-card'>
            <p style='line-height: 2; margin: 0;'>
                <strong>Start with</strong> Sentiment Analysis to understand the emotional foundation<br><br>
                <strong>Then explore</strong> Engagement Analysis to see what drives interactions<br><br>
                <strong>Dig into</strong> Text Analysis to understand topics and themes<br><br>
                <strong>Meet the players</strong> with User Analysis to identify key participants<br><br>
                <strong>Track the timeline</strong> with Temporal Analysis to spot trends<br><br>
                <strong>Finally, explore</strong> the Data Explorer to examine raw data with custom filters<br>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Success Message
    st.markdown("""
        <div class='success-message'>
            Ready to explore? Select a section from the sidebar to begin your journey through Twitter sentiment intelligence.
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class='footer'>
            <p>Twitter Sentiment Intelligence Dashboard | Powered by Advanced Analytics</p>
            <p>Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </div>
    """, unsafe_allow_html=True)
    
except FileNotFoundError:
    st.error("Error: Dataset not found. Please ensure the CSV file is at: ./Data/twitter_dataset.csv")