# pages/04_User_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

st.set_page_config(page_title="User Analysis", layout="wide")

# Twitter Theme Styling
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1DA1F2 0%, #1a91da 100%);
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: white !important;
            font-weight: 600;
            padding: 10px 15px;
            border-radius: 20px;
        }
        
        .page-header {
            background: linear-gradient(135deg, #1DA1F2 0%, #1a91da 100%);
            color: white;
            padding: 30px 20px;
            border-radius: 12px;
            margin-bottom: 25px;
        }
        
        .page-header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #1DA1F2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #eff3f4;
            margin-bottom: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }
        
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
        
        .insight-box {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #1DA1F2;
            margin: 10px 0;
            color: #0f1419;
        }
        
        .user-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #1DA1F2;
            margin-bottom: 15px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    df = pd.read_csv("./Data/twitter_dataset.csv")
    df['Sentiment'] = df['Text'].apply(lambda x: 'Positive' if TextBlob(str(x)).sentiment.polarity > 0.1 
                                       else ('Negative' if TextBlob(str(x)).sentiment.polarity < -0.1 else 'Neutral'))
    return df

st.markdown("""
    <div class='page-header'>
        <h1>Meet the Players: Understanding Key Users and Influencers</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Identifying who drives conversations and shapes discourse</p>
    </div>
""", unsafe_allow_html=True)

df = load_and_process_data()

st.markdown("""
    <div class='story-text'>
        <strong>Not all participants are created equal.</strong> Some users consistently get more engagement, 
        shape conversations, and influence others. By identifying these key players, we understand who drives 
        the narrative and what makes their content stand out. This section reveals the influencers and power users 
        in our network.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# User Statistics
user_stats = df.groupby('Username').agg({
    'Tweet_ID': 'count',
    'Likes': ['sum', 'mean'],
    'Retweets': ['sum', 'mean'],
    'Sentiment': lambda x: (x == 'Positive').sum()
}).round(2)

user_stats.columns = ['Total_Tweets', 'Total_Likes', 'Avg_Likes', 'Total_Retweets', 'Avg_Retweets', 'Positive_Tweets']
user_stats = user_stats.sort_values('Total_Likes', ascending=False)

# Key Metrics
st.subheader("The User Landscape")

st.markdown("""
    <div class='story-text'>
        First, let's understand the scale of participation. How many unique voices are in our dataset? 
        What's their average activity level? These metrics set the context for understanding individual influencers.
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Users</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{len(user_stats)}</div>
            <div style='color: #657786; font-size: 0.9em;'>unique voices</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Avg Tweets/User</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{user_stats['Total_Tweets'].mean():.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>typical activity level</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    max_tweets_user = user_stats['Total_Tweets'].idxmax()
    max_tweets = int(user_stats['Total_Tweets'].max())
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Most Active</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{max_tweets}</div>
            <div style='color: #657786; font-size: 0.9em;'>tweets by {max_tweets_user}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    total_engagement = user_stats['Total_Likes'].sum() + user_stats['Total_Retweets'].sum()
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Engagement</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{int(total_engagement):,}</div>
            <div style='color: #657786; font-size: 0.9em;'>combined interactions</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# Top Users by Likes
st.subheader("Who Gets the Most Appreciation?")

st.markdown("""
    <div class='story-text'>
        This ranking shows users ordered by total likes received. High numbers mean consistent engagement or 
        a few viral tweets. By comparing with other metrics, we'll see if success comes from volume (many tweets) 
        or quality (high engagement per tweet).
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
top_users_likes = user_stats.head(10)
fig_likes = px.bar(x=top_users_likes.index, y=top_users_likes['Total_Likes'],
                   title="Top 10 Users by Total Likes",
                   color=top_users_likes['Total_Likes'],
                   color_continuous_scale='Blues',
                   labels={'y': 'Total Likes', 'index': 'Username'})
fig_likes.update_xaxes(tickangle=-45)
st.plotly_chart(fig_likes, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        Notice the pattern: Does engagement correlate with participation (more tweets = more likes), 
        or do some users consistently outperform? This tells us if success is about quantity or quality.
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# User Activity Comparison
st.subheader("How Different Users Succeed")

st.markdown("""
    <div class='story-text'>
        Different metrics tell different stories. One user might be active (lots of tweets) but not get much engagement. 
        Another might be selective (few tweets) but highly effective. The charts below help us categorize users into different types.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.write("**Who Posts Most?**")
    st.write("Users ranked by number of tweets they've written")
    
    top_tweets_users = user_stats.nlargest(10, 'Total_Tweets').sort_values('Total_Tweets', ascending=True)
    fig_tweets = px.bar(
        x=top_tweets_users['Total_Tweets'],
        y=top_tweets_users.index,
        orientation='h',
        title="Top 10 Most Active Users (by Tweet Count)",
        color=top_tweets_users['Total_Tweets'],
        color_continuous_scale='Viridis',
        labels={'x': 'Number of Tweets', 'y': 'Username'}
    )

    st.plotly_chart(fig_tweets, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.write("**Who Gets Most Shares?**")
    st.write("Users ranked by total retweets their content generates")
    
    top_retweets_users = user_stats.nlargest(10, 'Total_Retweets').sort_values('Total_Retweets', ascending=True)
    fig_retweets = px.bar(
        x=top_retweets_users['Total_Retweets'],
        y=top_retweets_users.index,
        orientation='h',
        title="Top 10 Users by Total Retweets",
        color=top_retweets_users['Total_Retweets'],
        color_continuous_scale='Plasma',
        labels={'x': 'Total Retweets', 'y': 'Username'}
    )

    st.plotly_chart(fig_retweets, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Engagement Efficiency
st.subheader("Engagement Efficiency: Quality Over Quantity")

st.markdown("""
    <div class='story-text'>
        Raw totals can be misleading - a user with 100 tweets might have less engagement per tweet than someone 
        with 10 tweets. The charts below show AVERAGE engagement, revealing who creates content that consistently 
        resonates with audiences.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.write("**Average Likes Per Tweet**")
    st.write("Who creates content that gets liked most consistently?")
    
    top_avg_likes = user_stats.nlargest(10, 'Avg_Likes').sort_values('Avg_Likes', ascending=True)
    fig_avg_likes = px.bar(
        x=top_avg_likes['Avg_Likes'],
        y=top_avg_likes.index,
        orientation='h',
        title="Top 10 Users - Avg Likes per Tweet",
        color=top_avg_likes['Avg_Likes'],
        color_continuous_scale='RdYlGn',
        labels={'x': 'Average Likes', 'y': 'Username'}
    )

    st.plotly_chart(fig_avg_likes, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.write("**Average Retweets Per Tweet**")
    st.write("Who creates content that gets shared most consistently?")
    
    top_avg_retweets = user_stats.nlargest(10, 'Avg_Retweets').sort_values('Avg_Retweets', ascending=True)
    fig_avg_retweets = px.bar(
            x=top_avg_retweets['Avg_Retweets'],
            y=top_avg_retweets.index,
            orientation='h',
            title="Top 10 Users - Avg Retweets per Tweet",
            color=top_avg_retweets['Avg_Retweets'],
            color_continuous_scale='Blues',
            labels={'x': 'Average Retweets', 'y': 'Username'}
    )

    st.plotly_chart(fig_avg_retweets, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>Key Finding:</strong> The users with highest average engagement are the true influencers. 
        They might not post most frequently, but when they do, people listen and engage.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Top User Profiles
st.subheader("Detailed Profiles: Meet the Top 5 Users")

st.markdown("""
    <div class='story-text'>
        Here are the five users driving the most total engagement. Their profiles show a complete picture - 
        how many tweets, total appreciation, average per tweet, and sentiment tendency. These are your key players.
    </div>
""", unsafe_allow_html=True)

for idx, (username, stats) in enumerate(user_stats.head(5).iterrows(), 1):
    st.markdown(f"""
        <div class='user-card'>
            <h4 style='margin: 0; color: #1DA1F2;'>Rank #{idx}: {username}</h4>
            <div style='display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px; margin-top: 15px;'>
                <div>
                    <p style='margin: 0; color: #657786; font-size: 0.85em; text-transform: uppercase; font-weight: 600;'>Activity</p>
                    <p style='margin: 8px 0; color: #0f1419; font-weight: bold; font-size: 1.2em;'>{int(stats['Total_Tweets'])}</p>
                    <p style='margin: 0; color: #657786; font-size: 0.85em;'>tweets</p>
                </div>
                <div>
                    <p style='margin: 0; color: #657786; font-size: 0.85em; text-transform: uppercase; font-weight: 600;'>Total Appreciation</p>
                    <p style='margin: 8px 0; color: #e74c3c; font-weight: bold; font-size: 1.2em;'>{int(stats['Total_Likes']):,}</p>
                    <p style='margin: 0; color: #657786; font-size: 0.85em;'>likes</p>
                </div>
                <div>
                    <p style='margin: 0; color: #657786; font-size: 0.85em; text-transform: uppercase; font-weight: 600;'>Avg Engagement</p>
                    <p style='margin: 8px 0; color: #1DA1F2; font-weight: bold; font-size: 1.2em;'>{stats['Avg_Likes']:.1f}</p>
                    <p style='margin: 0; color: #657786; font-size: 0.85em;'>likes per tweet</p>
                </div>
                <div>
                    <p style='margin: 0; color: #657786; font-size: 0.85em; text-transform: uppercase; font-weight: 600;'>Positive Tweets</p>
                    <p style='margin: 8px 0; color: #2ecc71; font-weight: bold; font-size: 1.2em;'>{int(stats['Positive_Tweets'])}</p>
                    <p style='margin: 0; color: #657786; font-size: 0.85em;'>optimistic</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
    <div class='insight-box'>
        <strong>What This Means:</strong> These top users are your key influencers. Engaging with them, 
        understanding their messaging strategy, and learning what makes their content successful can inform 
        your overall communication strategy.
    </div>
""", unsafe_allow_html=True)