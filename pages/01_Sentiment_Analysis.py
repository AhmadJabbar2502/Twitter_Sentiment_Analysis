# pages/01_Sentiment_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

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
    df['Polarity'] = df['Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df['Subjectivity'] = df['Text'].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
    return df

st.markdown("""
    <div class='page-header'>
        <h1>Emotional Landscape: Understanding Sentiment</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Exploring the emotional tone and sentiment patterns in conversations</p>
    </div>
""", unsafe_allow_html=True)

df = load_and_process_data()

st.markdown("""
    <div class='story-text'>
        <strong>What people feel matters.</strong> Every conversation carries an emotional undertone - optimism, 
        criticism, neutrality. By analyzing sentiment, we can understand not just what people are saying, but how 
        they feel about it. This section breaks down the emotional landscape of our data, revealing whether 
        discussions lean positive, negative, or neutral.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Key Metrics Section
st.subheader("The Emotional Breakdown")

st.markdown("""
    <div class='story-text'>
        Here's the first question: What's the overall mood? These numbers tell us the distribution of emotions 
        across all conversations. If most are positive, we're looking at an optimistic audience. If many are negative, 
        there might be criticism or concerns worth addressing.
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    positive_count = (df['Sentiment'] == 'Positive').sum()
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Positive Sentiment</div>
            <div style='font-size: 2em; font-weight: bold; color: #2ecc71; margin: 10px 0;'>{positive_count}</div>
            <div style='color: #657786; font-size: 0.9em;'>{positive_count/len(df)*100:.1f}% of all</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    neutral_count = (df['Sentiment'] == 'Neutral').sum()
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Neutral Sentiment</div>
            <div style='font-size: 2em; font-weight: bold; color: #95a5a6; margin: 10px 0;'>{neutral_count}</div>
            <div style='color: #657786; font-size: 0.9em;'>{neutral_count/len(df)*100:.1f}% of all</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    negative_count = (df['Sentiment'] == 'Negative').sum()
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Negative Sentiment</div>
            <div style='font-size: 2em; font-weight: bold; color: #e74c3c; margin: 10px 0;'>{negative_count}</div>
            <div style='color: #657786; font-size: 0.9em;'>{negative_count/len(df)*100:.1f}% of all</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_polarity = df['Polarity'].mean()
    polarity_label = "Optimistic" if avg_polarity > 0.1 else ("Pessimistic" if avg_polarity < -0.1 else "Balanced")
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Overall Tone</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{avg_polarity:.3f}</div>
            <div style='color: #657786; font-size: 0.9em;'>{polarity_label}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Sentiment Distribution Visualization
st.subheader("How Sentiment is Distributed")

st.markdown("""
    <div class='story-text'>
        The charts below show how conversations spread across the three sentiment categories. The first shows 
        proportions (useful for understanding the overall mix), while the second shows absolute numbers (useful 
        for seeing the volume of each sentiment).
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    sentiment_counts = df['Sentiment'].value_counts()
    fig_pie = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                     color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                     title="Sentiment Distribution")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    sentiment_counts = df['Sentiment'].value_counts()
    fig_bar = px.bar(x=sentiment_counts.index, y=sentiment_counts.values,
                     color=sentiment_counts.index,
                     color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                     title="Sentiment Count",
                     labels={'x': 'Sentiment', 'y': 'Count'})
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        The sentiment distribution shows the foundation of all engagement. With """ + f"{positive_count/len(df)*100:.0f}% positive" + 
        """ conversations, we're seeing an audience that tends toward constructive engagement. Understanding this 
        baseline helps us interpret all other metrics.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Polarity & Subjectivity Analysis
st.subheader("The Depth: Polarity and Subjectivity")

st.markdown("""
    <div class='story-text'>
        Beyond simple categories, we measure two dimensions: <strong>Polarity</strong> (how positive or negative) 
        and <strong>Subjectivity</strong> (how much opinion vs. fact). A conversation can be factual and positive, 
        or opinion-based and negative. These dimensions reveal more nuance about communication patterns.
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    #
    
    st.write("**What is Polarity?** It measures how positive (-1) to negative (+1) a piece of text is.")
    fig_polarity = px.histogram(df, x='Polarity', nbins=40,
                                title="Distribution of Polarity Scores",
                                color_discrete_sequence=['#1DA1F2'],
                                labels={'Polarity': 'Polarity Score', 'count': 'Frequency'})
    fig_polarity.update_xaxes(title_text="Polarity Score")
    fig_polarity.update_yaxes(title_text="Number of Tweets")
    st.plotly_chart(fig_polarity, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    #
    
    st.write("**What is Subjectivity?** It measures how much opinion (1) vs. fact (0) a piece of text contains.")
    fig_subjectivity = px.histogram(df, x='Subjectivity', nbins=40,
                                    title="Distribution of Subjectivity Scores",
                                    color_discrete_sequence=['#ff6b6b'],
                                    labels={'Subjectivity': 'Subjectivity Score', 'count': 'Frequency'})
    fig_subjectivity.update_xaxes(title_text="Subjectivity Score")
    fig_subjectivity.update_yaxes(title_text="Number of Tweets")
    st.plotly_chart(fig_subjectivity, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Interactive Statistics
st.subheader("Detailed Metrics Explorer")

st.markdown("Use the toggles below to select which metrics you want to see:")

col1, col2 = st.columns(2)

with col1:
    show_polarity_stats = st.checkbox("Show Polarity Statistics", value=True)

with col2:
    show_subjectivity_stats = st.checkbox("Show Subjectivity Statistics", value=True)

col1, col2 = st.columns(2)

if show_polarity_stats:
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Polarity Statistics</div>
                <div style='margin-top: 15px;'>
                    <p style='margin: 8px 0;'><strong>Mean (Average):</strong> {df['Polarity'].mean():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Median (Middle Value):</strong> {df['Polarity'].median():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Standard Deviation:</strong> {df['Polarity'].std():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Minimum:</strong> {df['Polarity'].min():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Maximum:</strong> {df['Polarity'].max():.3f}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

if show_subjectivity_stats:
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Subjectivity Statistics</div>
                <div style='margin-top: 15px;'>
                    <p style='margin: 8px 0;'><strong>Mean (Average):</strong> {df['Subjectivity'].mean():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Median (Middle Value):</strong> {df['Subjectivity'].median():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Standard Deviation:</strong> {df['Subjectivity'].std():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Minimum:</strong> {df['Subjectivity'].min():.3f}</p>
                    <p style='margin: 8px 0;'><strong>Maximum:</strong> {df['Subjectivity'].max():.3f}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Advanced Visualization
st.subheader("The Relationship Between Polarity and Subjectivity")

st.markdown("""
    <div class='story-text'>
        This scatter plot reveals an important relationship: Can something be factual and very positive? 
        Or is emotional content necessarily subjective? The pattern here shows which combinations are most common 
        in our conversations.
    </div>
""", unsafe_allow_html=True)

#

# Interactive selection for scatter plot
sentiment_filter = st.multiselect(
    "Filter by Sentiment Type:",
    df['Sentiment'].unique(),
    default=df['Sentiment'].unique(),
    key="sentiment_scatter"
)

filtered_scatter = df[df['Sentiment'].isin(sentiment_filter)]

fig_scatter = px.scatter(filtered_scatter, x='Polarity', y='Subjectivity', 
                         color='Sentiment',
                         color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                         title="Polarity vs Subjectivity: How Emotions are Expressed",
                         labels={'Polarity': 'Polarity Score (Negative to Positive)', 
                                'Subjectivity': 'Subjectivity Score (Factual to Opinion-Based)'},
                         hover_data=['Text'])
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        Notice how sentiments cluster in different regions of this plot. This tells us something important about 
        how people express different emotions - are positive feelings typically expressed as facts or opinions? 
        Is criticism usually driven by emotions or evidence?
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Polarity by Sentiment
st.subheader("Comparing Polarity Across Sentiment Categories")

st.markdown("""
    <div class='story-text'>
        Finally, let's look at this relationship: Each sentiment category should have different polarity distributions, 
        but how much variation is there within each category? This box plot shows the range and concentration of polarity 
        scores within positive, negative, and neutral conversations.
    </div>
""", unsafe_allow_html=True)

#
fig_box = px.box(df, x='Sentiment', y='Polarity',
                 color='Sentiment',
                 color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                 title="Range of Polarity Within Each Sentiment Category",
                 labels={'Sentiment': 'Sentiment Category', 'Polarity': 'Polarity Score'})
fig_box.update_layout(height=400)
st.plotly_chart(fig_box, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>Key Takeaway:</strong> The heights of these boxes show us how consistent or variable each sentiment is. 
        A tall box means that sentiment category has wide variation in how strongly it's expressed. A short box means 
        people express that sentiment consistently.
    </div>
""", unsafe_allow_html=True)