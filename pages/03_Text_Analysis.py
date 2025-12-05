# pages/03_Text_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Text Analysis", layout="wide")

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

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return ' '.join(text.split())

@st.cache_data
def load_and_process_data():
    df = pd.read_csv("./Data/twitter_dataset.csv")
    df['Cleaned_Text'] = df['Text'].apply(clean_text)
    df['Text_Length'] = df['Cleaned_Text'].apply(lambda x: len(x.split()))
    df['Sentiment'] = df['Text'].apply(lambda x: 'Positive' if TextBlob(str(x)).sentiment.polarity > 0.1 
                                       else ('Negative' if TextBlob(str(x)).sentiment.polarity < -0.1 else 'Neutral'))
    return df

st.markdown("""
    <div class='page-header'>
        <h1>What Are People Talking About? Unveiling Topics and Themes</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Understanding the words, phrases, and topics that drive conversations</p>
    </div>
""", unsafe_allow_html=True)

df = load_and_process_data()

st.markdown("""
    <div class='story-text'>
        <strong></strong> Understanding WHAT people are discussing is just as 
        important as understanding HOW they feel about it. This section analyzes the actual words and themes in our conversations, 
        revealing the topics that capture attention and what matters most to our audience.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Text Metrics
st.subheader("The Basics: Tweet Length and Vocabulary")

st.markdown("""
    <div class='story-text'>
        Length matters in social media. Some conversations are brief and punchy, others are lengthy and detailed. 
        Below we see how much people typically say, and how varied their vocabulary is across all conversations.
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Avg Words/Tweet</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{df['Text_Length'].mean():.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>words on average</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Longest Tweet</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{df['Text_Length'].max():.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>words in longest</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Shortest Tweet</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{df['Text_Length'].min():.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>words in shortest</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    all_words = ' '.join(df['Cleaned_Text']).split()
    unique_words = len(set(all_words))
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Unique Words</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{unique_words:,}</div>
            <div style='color: #657786; font-size: 0.9em;'>distinct terms used</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

st.markdown("---")

# Tweet Length Distribution
st.subheader("How Long Are Tweets?")

st.markdown("""
    <div class='story-text'>
        Does tweet length affect engagement? This histogram shows whether people prefer brevity or substance. 
        If most tweets cluster at one length, there's a clear preference. If spread out, there's diversity in 
        how people express themselves.
    </div>
""", unsafe_allow_html=True)

#
fig_length = px.histogram(df, x='Text_Length', nbins=30,
                          title="How Many Words in a Typical Tweet?",
                          color_discrete_sequence=['#1DA1F2'],
                          labels={'Text_Length': 'Number of Words', 'count': 'Number of Tweets'})
fig_length.update_xaxes(title_text="Words per Tweet")
fig_length.update_yaxes(title_text="Number of Tweets")
st.plotly_chart(fig_length, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Word Frequency with Interactive Control
st.subheader("The Most Talked-About Words")

st.markdown("""
    <div class='story-text'>
        Word frequency reveals what's on everyone's mind. Which words appear most often? Are they specific keywords 
        or generic terms? Use the slider to adjust how many words to see - fewer words show what REALLY dominates, 
        while more words show broader themes.
    </div>
""", unsafe_allow_html=True)


all_words = ' '.join(df['Cleaned_Text']).split()
word_freq = Counter(all_words)

top_n = st.slider("How many top words would you like to see?", 5, 50, 20, step=5)
top_words = dict(word_freq.most_common(top_n))

fig_words = px.bar(x=list(top_words.keys()), y=list(top_words.values()),
                   title=f"The {top_n} Most Frequently Used Words",
                   color=list(range(len(top_words))),
                   color_continuous_scale='Blues_r',
                   labels={'x': 'Word', 'y': 'Frequency'})
fig_words.update_xaxes(tickangle=-45)
fig_words.update_yaxes(title_text="How Many Times it Appears")
st.plotly_chart(fig_words, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>What This Tells Us:</strong> Frequently used words indicate the core topics and themes. 
        If you see specific industry terms, the audience is specialized. If you see generic words, 
        conversations are broad and varied.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Word Cloud Visualization
st.subheader("Visual Theme: Word Cloud")

st.markdown("""
    <div class='story-text'>
        Word clouds provide an intuitive visual representation where word size represents frequency. 
        The larger the word, the more often it appears. This visual format makes patterns instantly recognizable.
    </div>
""", unsafe_allow_html=True)

#

all_text = ' '.join(df['Cleaned_Text'])
wordcloud = WordCloud(width=900, height=400, 
                      background_color='white',
                      colormap='Blues',
                      relative_scaling=0.5).generate(all_text)

fig, ax = plt.subplots(figsize=(12, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig, use_container_width=True)

st.write("Overall Theme Cloud - Larger words are discussed more frequently")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Sentiment-Specific Word Clouds
st.subheader("What Different Sentiments Discuss")

st.markdown("""
    <div class='story-text'>
        Do positive and negative conversations focus on different topics? By comparing word clouds across sentiments, 
        we can see what themes drive each emotion. This reveals whether criticism focuses on specific issues, 
        or if praise and negativity touch the same topics differently.
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["Positive Conversations", "Negative Conversations", "Neutral Conversations"])

sentiments = ['Positive', 'Negative', 'Neutral']
colors = ['Greens', 'Reds', 'Greys']

for tab, sentiment, color in zip(tabs, sentiments, colors):
    with tab:
        #
        
        sentiment_text = ' '.join(df[df['Sentiment'] == sentiment]['Cleaned_Text'])
        
        if len(sentiment_text.split()) > 0:
            wordcloud = WordCloud(width=900, height=400,
                                 background_color='white',
                                 colormap=color,
                                 relative_scaling=0.5).generate(sentiment_text)
            
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)
            
            st.write(f"What {sentiment} conversations discuss most")
        else:
            st.info(f"No {sentiment} tweets found")
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Text Length by Sentiment
st.subheader("Do Certain Sentiments Use More Words?")

st.markdown("""
    <div class='story-text'>
        Interesting question: Do positive people write longer messages? Or does criticism require more explanation? 
        The box plot shows the range of lengths for each sentiment, revealing stylistic differences.
    </div>
""", unsafe_allow_html=True)

#
fig_length_sentiment = px.box(df, x='Sentiment', y='Text_Length',
                              color='Sentiment',
                              color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
                              title="Tweet Length by Sentiment Type",
                              labels={'Text_Length': 'Words per Tweet', 'Sentiment': 'Sentiment'})
fig_length_sentiment.update_layout(height=400)
st.plotly_chart(fig_length_sentiment, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='insight-box'>
        <strong>Pattern Recognition:</strong> If the boxes are different heights, it means some sentiments 
        vary more in their expression. If boxes are at different heights, it means some sentiments tend to use 
        more or fewer words on average.
    </div>
""", unsafe_allow_html=True)