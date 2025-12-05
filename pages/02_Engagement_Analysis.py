# pages/02_Engagement_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

st.set_page_config(page_title="Engagement Analysis", layout="wide")

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
        <h1>What Drives Engagement: Likes, Shares, and Reach</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Understanding which conversations resonate most with audiences</p>
    </div>
""", unsafe_allow_html=True)

df = load_and_process_data()

st.markdown("""
    <div class='story-text'>
        <strong>Engagement is the currency of social media.</strong> It's not enough for people to see your message - 
        they need to care enough to like it or share it with others. This section reveals what captures attention and 
        drives action. We'll see how sentiment influences engagement, and which types of conversations get amplified.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Key Engagement Metrics
st.subheader("The Engagement Numbers")

st.markdown("""
    <div class='story-text'>
        First, let's understand the scale. These numbers show total engagement across all conversations, plus averages 
        that tell us what a typical interaction looks like. If the average is much lower than the maximum, there are 
        outlier conversations getting disproportionate attention.
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Likes</div>
            <div style='font-size: 2em; font-weight: bold; color: #e74c3c; margin: 10px 0;'>{df['Likes'].sum():,.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>expressions of support</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Retweets</div>
            <div style='font-size: 2em; font-weight: bold; color: #2ecc71; margin: 10px 0;'>{df['Retweets'].sum():,.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>times amplified</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Avg Likes/Tweet</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{df['Likes'].mean():.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>typical response</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Avg Retweets/Tweet</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{df['Retweets'].mean():.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>typical share rate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        Look at the ratio between total and average. A large difference suggests that a few conversations are getting 
        massive engagement while others fall flat. This concentration pattern is important for content strategy.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sentiment's Impact
st.subheader("The Sentiment Effect: What Emotion Drives Engagement?")

st.markdown("""
    <div class='story-text'>
        Now for the crucial question: Does sentiment matter for engagement? Do people like and share positive content more? 
        Or does controversy drive engagement regardless of sentiment? The bars below reveal whether positive conversations 
        genuinely outperform negative ones, or if it's more nuanced than that.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    #
    st.write("**Average Likes by Sentiment Type**")
    st.write("Which sentiment gets the most appreciation?")
    
    likes_by_sentiment = df.groupby('Sentiment')['Likes'].mean().sort_values(ascending=False)
    fig_likes = px.bar(x=likes_by_sentiment.index, y=likes_by_sentiment.values,
                       color=likes_by_sentiment.index,
                       color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                       title="Which Sentiment Gets More Likes?",
                       labels={'x': 'Sentiment', 'y': 'Average Likes'})
    fig_likes.update_layout(showlegend=False)
    st.plotly_chart(fig_likes, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    #
    st.write("**Average Retweets by Sentiment Type**")
    st.write("Which sentiment gets shared the most?")
    
    rt_by_sentiment = df.groupby('Sentiment')['Retweets'].mean().sort_values(ascending=False)
    fig_rt = px.bar(x=rt_by_sentiment.index, y=rt_by_sentiment.values,
                    color=rt_by_sentiment.index,
                    color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                    title="Which Sentiment Gets More Shares?",
                    labels={'x': 'Sentiment', 'y': 'Average Retweets'})
    fig_rt.update_layout(showlegend=False)
    st.plotly_chart(fig_rt, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>The Finding:</strong> """ + f"Positive content gets {(likes_by_sentiment['Positive'] / likes_by_sentiment.min() - 1) * 100:.0f}% more likes" + """ 
        than lower-performing sentiment types. This suggests audiences actively prefer constructive, positive discussions over critical or neutral ones.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Interactive Correlation Analysis
st.subheader("Exploring the Relationship Between Likes and Retweets")

st.markdown("""
    <div class='story-text'>
        Are likes and retweets connected? If someone likes something, do they also share it? Or are these independent 
        actions? The interactive scatter plot below lets you explore this relationship by filtering for different sentiment types.
    </div>
""", unsafe_allow_html=True)

#

# Interactive filter
sentiment_filter = st.multiselect(
    "Show me engagement for these sentiment types:",
    df['Sentiment'].unique(),
    default=df['Sentiment'].unique(),
    key="engagement_scatter"
)

filtered_engagement = df[df['Sentiment'].isin(sentiment_filter)]

fig_scatter = px.scatter(filtered_engagement, x='Retweets', y='Likes', 
                         color='Sentiment',
                         color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': "#4fa7d3"},
                         size='Likes',
                         title="The Relationship: Retweets vs Likes (bubble size = like volume)",
                         labels={'Retweets': 'Times Shared (Retweets)', 'Likes': 'Times Appreciated (Likes)'})
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        If points cluster along a diagonal line, it means likes and retweets are strongly correlated. If scattered, 
        they're independent - some conversations get liked without being shared, or vice versa. This tells us if 
        appreciation and amplification come from the same audience behavior.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Distribution Analysis
st.subheader("How Engagement is Distributed")

st.markdown("""
    <div class='story-text'>
        Are engagement opportunities equally distributed, or does success follow a "winner takes most" pattern? 
        These histograms show whether most conversations get similar engagement (even distribution) or if a few 
        outliers dominate (skewed distribution).
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    #
    st.write("**Distribution of Likes**")
    st.write("How varied are like counts across tweets?")
    
    fig_likes_dist = px.histogram(df, x='Likes', nbins=40,
                                  title="Spread of Likes Across Conversations",
                                  color_discrete_sequence=['#ff6b6b'],
                                  labels={'Likes': 'Number of Likes', 'count': 'Number of Tweets'})
    fig_likes_dist.update_xaxes(title_text="Likes per Tweet")
    fig_likes_dist.update_yaxes(title_text="Number of Tweets")
    st.plotly_chart(fig_likes_dist, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    #
    st.write("**Distribution of Retweets**")
    st.write("How varied are retweet counts across tweets?")
    
    fig_rt_dist = px.histogram(df, x='Retweets', nbins=40,
                               title="Spread of Retweets Across Conversations",
                               color_discrete_sequence=['#00b894'],
                               labels={'Retweets': 'Number of Retweets', 'count': 'Number of Tweets'})
    fig_rt_dist.update_xaxes(title_text="Retweets per Tweet")
    fig_rt_dist.update_yaxes(title_text="Number of Tweets")
    st.plotly_chart(fig_rt_dist, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        Right-skewed distributions (most tweets get few likes/retweets, with a long tail of high performers) are normal 
        in social media. This is the reality of content distribution - consistency beats virality.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Top Performers
st.subheader("The Top Conversations")

st.markdown("""
    <div class='story-text'>
        Every dataset has outliers - conversations that perform exceptionally well. Below are the top 10 most-liked 
        tweets. What do they have in common? Can you spot patterns in their sentiment or content?
    </div>
""", unsafe_allow_html=True)

top_tweets = df.nlargest(10, 'Likes')[['Text', 'Likes', 'Retweets', 'Sentiment', 'Username']]

for idx, (i, row) in enumerate(top_tweets.iterrows(), 1):
    sentiment_color = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'}[row['Sentiment']]
    
    st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid {sentiment_color};'>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <p style='margin: 0; font-weight: bold; color: #0f1419;'>Top {idx} - by {row['Username']}</p>
                    <p style='margin: 8px 0; color: #0f1419; line-height: 1.5;'>{row['Text'][:150]}...</p>
                </div>
            </div>
            <div style='display: flex; gap: 20px; color: #657786; font-size: 0.9em; margin-top: 10px;'>
                <span>Likes: <strong>{row['Likes']}</strong></span>
                <span>Retweets: <strong>{row['Retweets']}</strong></span>
                <span>Sentiment: <strong>{row['Sentiment']}</strong></span>
            </div>
        </div>
    """, unsafe_allow_html=True)