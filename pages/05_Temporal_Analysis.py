# pages/05_Temporal_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

st.set_page_config(page_title="Temporal Analysis", layout="wide")

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
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    df['Month'] = df['Timestamp'].dt.to_period('M')
    df['Hour'] = df['Timestamp'].dt.hour
    df['DayOfWeek'] = df['Timestamp'].dt.day_name()
    df['Sentiment'] = df['Text'].apply(lambda x: 'Positive' if TextBlob(str(x)).sentiment.polarity > 0.1 
                                       else ('Negative' if TextBlob(str(x)).sentiment.polarity < -0.1 else 'Neutral'))
    return df

st.markdown("""
    <div class='page-header'>
        <h1>Timing is Everything: Trends, Patterns, and Peak Moments</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Understanding when conversations peak and how sentiment evolves</p>
    </div>
""", unsafe_allow_html=True)

df = load_and_process_data()

st.markdown("""
    <div class='story-text'>
        <strong>Timing matters as much as content.</strong> When do people engage most? Do trends change over time? 
        Is there a best day or hour to post? This section tracks sentiment and engagement across time, revealing 
        patterns that help you understand when audiences are most receptive and what trends are emerging.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Key Temporal Metrics
st.subheader("The Time Frame of Our Analysis")

st.markdown("""
    <div class='story-text'>
        First, let's establish the scope. What period are we analyzing? How much data do we have, and is it 
        concentrated or spread throughout the period? These questions establish the foundation for all temporal analysis.
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    start_date = df['Timestamp'].min().date()
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Start Date</div>
            <div style='font-size: 1.2em; font-weight: bold; color: #0f1419; margin: 10px 0;'>{start_date}</div>
            <div style='color: #657786; font-size: 0.85em;'>earliest conversation</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    end_date = df['Timestamp'].max().date()
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>End Date</div>
            <div style='font-size: 1.2em; font-weight: bold; color: #0f1419; margin: 10px 0;'>{end_date}</div>
            <div style='color: #657786; font-size: 0.85em;'>latest conversation</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    date_range = (df['Timestamp'].max() - df['Timestamp'].min()).days
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Duration</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{date_range}</div>
            <div style='color: #657786; font-size: 0.85em;'>days analyzed</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_daily = len(df) / max(date_range, 1)
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Daily Average</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{avg_daily:.1f}</div>
            <div style='color: #657786; font-size: 0.85em;'>tweets per day</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# Tweet Volume Over Time
st.subheader("Conversation Activity Over Time")

st.markdown("""
    <div class='story-text'>
        Does engagement stay constant, or do conversations peak at certain times? The line chart below shows daily 
        volume - peaks might correspond to news events, product launches, or recurring cycles. Valleys might indicate 
        slower periods or when the audience is less active.
    </div>
""", unsafe_allow_html=True)

tweets_by_date = df.groupby('Date').size()

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
fig_volume = px.line(x=tweets_by_date.index, y=tweets_by_date.values,
                     title="Daily Tweet Volume: Are There Peaks and Valleys?",
                     markers=True,
                     color_discrete_sequence=['#1DA1F2'],
                     labels={'x': 'Date', 'y': 'Number of Tweets'})
fig_volume.update_layout(hovermode='x unified', height=400)
fig_volume.update_yaxes(title_text="Number of Tweets")
st.plotly_chart(fig_volume, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>Pattern Recognition:</strong> Sharp spikes often indicate major events or announcements. 
        Steady growth suggests growing interest. Sudden drops might indicate changes in the topic or audience.
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# Sentiment Trend
st.subheader("How Sentiment Evolves Over Time")

st.markdown("""
    <div class='story-text'>
        Are people getting more positive or negative over time? Or does sentiment stay stable? This stacked line chart 
        shows how each sentiment type changes day by day, revealing whether the audience mood is shifting or consistent.
    </div>
""", unsafe_allow_html=True)

sentiment_by_date = df.groupby(['Date', 'Sentiment']).size().unstack(fill_value=0)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
fig_sentiment = px.line(sentiment_by_date,
                        title="Sentiment Evolution: Is the Mood Changing?",
                        markers=True,
                        color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                        labels={'value': 'Number of Tweets', 'index': 'Date'})
fig_sentiment.update_layout(hovermode='x unified', height=400)
st.plotly_chart(fig_sentiment, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>What to Look For:</strong> Diverging lines mean sentiment is shifting. Parallel lines mean proportions 
        stay constant. Understanding these patterns helps you anticipate and respond to mood changes in your audience.
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# When Do People Engage Most?
st.subheader("Prime Time: When Does Engagement Peak?")

st.markdown("""
    <div class='story-text'>
        Social media has rhythms. Some hours are busier than others - morning rush, lunch breaks, evening wind-down. 
        Understanding these patterns helps you post when audiences are most attentive. Let's explore both hourly and 
        daily patterns.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.write("**Best Hours of the Day**")
    st.write("When do most conversations happen?")
    
    tweets_by_hour = df.groupby('Hour').size()
    fig_hour = px.bar(x=tweets_by_hour.index, y=tweets_by_hour.values,
                      title="Tweet Activity by Hour of Day",
                      color=tweets_by_hour.values,
                      color_continuous_scale='Blues',
                      labels={'x': 'Hour of Day (24-hour format)', 'y': 'Number of Tweets'})
    fig_hour.update_xaxes(title_text="Hour of Day")
    st.plotly_chart(fig_hour, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.write("**Best Days of the Week**")
    st.write("Does the day of week matter for engagement?")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tweets_by_day = df.groupby('DayOfWeek').size()
    tweets_by_day = tweets_by_day.reindex([d for d in day_order if d in tweets_by_day.index])
    
    fig_day = px.bar(x=tweets_by_day.index, y=tweets_by_day.values,
                     title="Tweet Activity by Day of Week",
                     color=tweets_by_day.values,
                     color_continuous_scale='Blues',
                     labels={'x': 'Day of Week', 'y': 'Number of Tweets'})
    fig_day.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>Content Strategy Tip:</strong> Peak hours show maximum audience presence. But engagement metrics 
        (likes/retweets per tweet) might peak at different times when competition for attention is lower.
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# Interactive Engagement Over Time
st.subheader("How Engagement Quality Changes Over Time")

st.markdown("""
    <div class='story-text'>
        Finally, let's see if engagement metrics (likes and retweets per tweet) change over time. Does content get 
        more or less engagement as time progresses? Use the toggle below to choose which metric interests you most.
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

metric_choice = st.radio(
    "Which engagement metric interests you?",
    ["Average Likes", "Average Retweets", "Both"],
    horizontal=True
)

monthly_likes = df.groupby('Month')['Likes'].mean()
monthly_retweets = df.groupby('Month')['Retweets'].mean()

if metric_choice == "Average Likes":
    fig_engage = px.line(x=monthly_likes.index.astype(str), y=monthly_likes.values,
                         title="Average Likes per Tweet Over Time",
                         markers=True,
                         color_discrete_sequence=['#ff6b6b'],
                         labels={'x': 'Month', 'y': 'Average Likes'})
elif metric_choice == "Average Retweets":
    fig_engage = px.line(x=monthly_retweets.index.astype(str), y=monthly_retweets.values,
                         title="Average Retweets per Tweet Over Time",
                         markers=True,
                         color_discrete_sequence=['#00b894'],
                         labels={'x': 'Month', 'y': 'Average Retweets'})
else:
    fig_engage = go.Figure()
    fig_engage.add_trace(go.Scatter(x=monthly_likes.index.astype(str), y=monthly_likes.values,
                                    mode='lines+markers', name='Avg Likes', line=dict(color='#ff6b6b')))
    fig_engage.add_trace(go.Scatter(x=monthly_retweets.index.astype(str), y=monthly_retweets.values,
                                    mode='lines+markers', name='Avg Retweets', line=dict(color='#00b894')))
    fig_engage.update_layout(title="Engagement Trends Over Time", hovermode='x unified')

fig_engage.update_xaxes(tickangle=-45)
st.plotly_chart(fig_engage, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>Key Insight:</strong> Rising trends suggest improving content quality or growing audience interest. 
        Declining trends might indicate audience fatigue or changing topic relevance. Flat trends suggest stability and predictability.
    </div>
""", unsafe_allow_html=True)