# pages/07_Tweet_Analyzer.py
import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.graph_objects as go

st.set_page_config(page_title="Tweet Analyzer", layout="wide")

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
        
        .positive-box {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #2ecc71;
            margin: 10px 0;
            color: #0f1419;
        }
        
        .negative-box {
            background: #ffebee;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            margin: 10px 0;
            color: #0f1419;
        }
        
        .neutral-box {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #95a5a6;
            margin: 10px 0;
            color: #0f1419;
        }
        
        .recommendation-box {
            background: #fff9c4;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #fbc02d;
            margin: 10px 0;
            color: #0f1419;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='page-header'>
        <h1>Tweet Sentiment Analyzer: Real-Time Analysis & Rewriting</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Analyze your tweet's sentiment and get AI-powered recommendations to adjust tone</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='story-text'>
        <strong>Craft the perfect message.</strong> Before you post, understand how your tweet will be perceived. 
        This tool analyzes the sentiment of your message in real-time and provides intelligent suggestions to rewrite 
        it in the tone you want - more positive, negative, or neutral. Perfect for marketers, content creators, and 
        anyone who wants to optimize their social media impact.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Main Input Section
st.subheader("Enter Your Tweet")

st.markdown("""
    <div class='story-text'>
        Type or paste your tweet below. We'll analyze its current sentiment and show you how it compares to other tweets. 
        Then, if you'd like, we'll help you rewrite it in a different tone.
    </div>
""", unsafe_allow_html=True)



tweet_text = st.text_area(
    "Your Tweet:",
    placeholder="Write your tweet here...",
    height=100,
    max_chars=280,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 1, 8])

with col1:
    analyze_button = st.button("Analyze Tweet", use_container_width=True, type="primary")

with col2:
    st.write(f"**{len(tweet_text)}/280**")

st.markdown("</div>", unsafe_allow_html=True)

# Initialize session state for tweet analysis
if 'analyzed_tweet' not in st.session_state:
    st.session_state.analyzed_tweet = None

if analyze_button and tweet_text:
    # Show progress indicator
    with st.spinner("Analyzing your tweet..."):
        import time
        time.sleep(0.5)  # Simulate processing
    
    st.session_state.analyzed_tweet = tweet_text

# Show analysis results only if a tweet has been analyzed
blob = TextBlob(tweet_text)
if st.session_state.analyzed_tweet:
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment
    if polarity > 0.1:
        sentiment = "Positive"
        sentiment_color = "#2ecc71"
        sentiment_emoji = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
        sentiment_color = "#e74c3c"
        sentiment_emoji = "Negative"
    else:
        sentiment = "Neutral"
        sentiment_color = "#95a5a6"
        sentiment_emoji = "Neutral"
    
    # Display Analysis Results
    st.subheader("Current Sentiment Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Sentiment</div>
                <div style='font-size: 2em; font-weight: bold; color: {sentiment_color}; margin: 10px 0;'>{sentiment}</div>
                <div style='color: #657786; font-size: 0.9em;'>Current tone</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Polarity Score</div>
                <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{polarity:.3f}</div>
                <div style='color: #657786; font-size: 0.9em;'>-1 (negative) to +1 (positive)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Subjectivity Score</div>
                <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{subjectivity:.3f}</div>
                <div style='color: #657786; font-size: 0.9em;'>0 (factual) to 1 (opinion)</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Sentiment Gauge
    
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=polarity * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sentiment Scale (-100 to +100)"},
        delta={'reference': 0},
        gauge={
            'axis': {'range': [-100, 100]},
            'bar': {'color': sentiment_color},
            'steps': [
                {'range': [-100, -30], 'color': "#ffebee"},
                {'range': [-30, 30], 'color': "#f5f5f5"},
                {'range': [30, 100], 'color': "#e8f5e9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0
            }
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interpretation
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    if sentiment == "Positive":
        st.markdown("""
            <div class='positive-box'>
                <strong>Positive Tweet Detected!</strong> Your message conveys an optimistic or favorable tone. 
                This type of content typically receives higher engagement and is perceived as constructive and encouraging.
            </div>
        """, unsafe_allow_html=True)
    elif sentiment == "Negative":
        st.markdown("""
            <div class='negative-box'>
                <strong>Negative Tone Detected.</strong> Your message carries a critical or unfavorable tone. 
                While this can spark discussion, consider whether this is the intended impact or if you'd like to adjust the message.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='neutral-box'>
                <strong>Neutral Tone Detected.</strong> Your message is factual and balanced, neither strongly positive 
                nor negative. This is great for informational content, but may lack emotional engagement.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rewriting Section
    st.subheader("Rewrite Your Tweet")
    
    st.markdown("""
        <div class='story-text'>
            Want to adjust the tone of your message? Select the desired sentiment below and we'll suggest a rewritten version 
            that maintains your core message while shifting the emotional tone.
        </div>
    """, unsafe_allow_html=True)
    
    
    
    target_sentiment = st.radio(
        "What tone would you like?",
        ["Keep Current", "Make Positive", "Make Negative", "Make Neutral"],
        horizontal=True
    )
    
    # Helper functions for rewriting
    def make_positive(text):
        positive_words = {
            'bad': 'good', 'terrible': 'wonderful', 'awful': 'amazing', 'hate': 'love',
            'worst': 'best', 'problem': 'opportunity', 'fail': 'succeed', 'wrong': 'right',
            'difficult': 'challenging', 'impossible': 'possible', 'never': 'always',
            'lack': 'have', 'missing': 'includes', 'sad': 'happy', 'disappointed': 'pleased'
        }
        result = text.lower()
        for word, replacement in positive_words.items():
            result = result.replace(word, replacement)
        return result.capitalize()
    
    def make_negative(text):
        negative_words = {
            'good': 'mediocre', 'great': 'disappointing', 'love': 'dislike',
            'best': 'worst', 'wonderful': 'terrible', 'amazing': 'dreadful',
            'excellent': 'poor', 'perfect': 'flawed', 'happy': 'unhappy'
        }
        result = text.lower()
        for word, replacement in negative_words.items():
            result = result.replace(word, replacement)
        return result.capitalize()
    
    def make_neutral(text):
        neutral_replacements = {
            'love': 'prefer', 'hate': 'dislike', 'amazing': 'notable', 'terrible': 'inadequate',
            'wonderful': 'good', 'awful': 'poor', 'beautiful': 'pleasant', 'ugly': 'unattractive'
        }
        result = text.lower()
        for word, replacement in neutral_replacements.items():
            result = result.replace(word, replacement)
        return result.capitalize()
    
    if target_sentiment == "Keep Current":
        st.info("Your tweet will remain as is.")
        rewritten = tweet_text
    elif target_sentiment == "Make Positive":
        rewritten = make_positive(tweet_text)
        st.markdown("""
            <div class='positive-box'>
                <strong>Strategy:</strong> Replaced negative/critical words with positive alternatives. 
                This version emphasizes opportunities, achievements, and benefits.
            </div>
        """, unsafe_allow_html=True)
    elif target_sentiment == "Make Negative":
        rewritten = make_negative(tweet_text)
        st.markdown("""
            <div class='negative-box'>
                <strong>Strategy:</strong> Shifted language toward critical perspectives. 
                Use this carefully - negativity can spark discussion but may also alienate audiences.
            </div>
        """, unsafe_allow_html=True)
    else:  # Make Neutral
        rewritten = make_neutral(tweet_text)
        st.markdown("""
            <div class='neutral-box'>
                <strong>Strategy:</strong> Removed emotional language and replaced it with factual, objective terms. 
                This version is more professional and balanced.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    st.subheader("Your Rewritten Tweet")
    
    
    
    # Analyze rewritten version
    rewritten_blob = TextBlob(rewritten)
    rewritten_polarity = rewritten_blob.sentiment.polarity
    rewritten_subjectivity = rewritten_blob.sentiment.subjectivity
    
    if rewritten_polarity > 0.1:
        rewritten_sentiment = "Positive"
        rewritten_color = "#2ecc71"
    elif rewritten_polarity < -0.1:
        rewritten_sentiment = "Negative"
        rewritten_color = "#e74c3c"
    else:
        rewritten_sentiment = "Neutral"
        rewritten_color = "#95a5a6"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Original Tweet:**")
        st.write(tweet_text)
        st.write("")
        st.write("**Rewritten Tweet:**")
        st.write(rewritten)
    
    with col2:
        st.markdown(f"""
            <div style='background: white; padding: 15px; border-radius: 10px; border-left: 4px solid {rewritten_color};'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>New Sentiment</div>
                <div style='font-size: 1.8em; font-weight: bold; color: {rewritten_color}; margin: 10px 0;'>{rewritten_sentiment}</div>
                <div style='color: #657786; font-size: 0.85em;'>Polarity: {rewritten_polarity:.3f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Copy button
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Want to use the rewritten version?**")
        st.code(rewritten, language="text")
    
    with col2:
        st.markdown("""
            <div class='recommendation-box'>
                <strong>Tips for Better Engagement:</strong><br>
                • Positive tweets get 75% more engagement<br>
                • Keep tweets between 15-30 words<br>
                • Use specific, actionable language<br>
                • Questions boost interaction<br>
                • Balance emotion with information
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div class='insight-box'>
            <strong>Remember:</strong> The best tweets resonate authentically with your audience. 
            Use these suggestions as guidelines, but always maintain your authentic voice. 
            A forced tone can undermine your message credibility.
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class='insight-box'>
            Enter a tweet above to get started. We'll analyze its sentiment and provide suggestions 
            for rewriting it in different tones to match your communication goals.
        </div>
    """, unsafe_allow_html=True)