# pages/06_Data_Explorer.py
import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import io

st.set_page_config(page_title="Data Explorer", layout="wide")

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
        
        .filter-container {
            background: white;
            padding: 25px;
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
def load_data():
    df = pd.read_csv("./Data/twitter_dataset.csv")
    df['Sentiment'] = df['Text'].apply(lambda x: 'Positive' if TextBlob(str(x)).sentiment.polarity > 0.1 
                                       else ('Negative' if TextBlob(str(x)).sentiment.polarity < -0.1 else 'Neutral'))
    return df

st.markdown("""
    <div class='page-header'>
        <h1>Raw Data Explorer: Dive Deep into Individual Conversations</h1>
        <p style='margin: 10px 0 0 0; opacity: 0.95;'>Filter, search, and export the complete dataset with custom queries</p>
    </div>
""", unsafe_allow_html=True)

df = load_data()

st.markdown("""
    <div class='story-text'>
        While our analysis pages show patterns and trends, 
        this explorer lets you drill down into individual conversations. Want to see all negative tweets? Search for 
        specific users? Find high-engagement tweets? You control the filters, and you can export results for further analysis.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Overview Statistics
st.subheader("Complete Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Records</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{len(df):,}</div>
            <div style='color: #657786; font-size: 0.9em;'>conversations</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Data Columns</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{len(df.columns)}</div>
            <div style='color: #657786; font-size: 0.9em;'>fields per record</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Unique Users</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{df['Username'].nunique():,}</div>
            <div style='color: #657786; font-size: 0.9em;'>participants</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Time Span</div>
            <div style='font-size: 1.2em; font-weight: bold; color: #0f1419; margin: 10px 0;'>{df['Timestamp'].min()[:10]} to {df['Timestamp'].max()[:10]}</div>
            <div style='color: #657786; font-size: 0.9em;'>analysis period</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Filters Section
st.subheader("Build Your Custom Query")

st.markdown("""
    <div class='story-text'>
        Use the controls below to filter the data exactly how you want it. Start broad and narrow down, or be specific 
        from the start. The table updates instantly to show matching conversations.
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='filter-container'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    selected_users = st.multiselect(
        "Filter by User:",
        sorted(df['Username'].unique()),
        max_selections=10,
        help="Leave empty to include all users"
    )

with col2:
    sentiment_filter = st.multiselect(
        "Filter by Sentiment:",
        sorted(df['Sentiment'].unique()),
        default=sorted(df['Sentiment'].unique()),
        help="Select which sentiment types to include"
    )

with col3:
    min_likes = st.slider(
        "Minimum Likes:",
        int(df['Likes'].min()),
        int(df['Likes'].max()),
        int(df['Likes'].min()),
        help="Only show tweets with at least this many likes"
    )

col4, col5, col6 = st.columns(3)

with col4:
    min_retweets = st.slider(
        "Minimum Retweets:",
        int(df['Retweets'].min()),
        int(df['Retweets'].max()),
        int(df['Retweets'].min()),
        help="Only show tweets with at least this many retweets"
    )

with col5:
    sort_options = ["Likes (Most First)", "Retweets (Most First)", "Date (Newest)", "Date (Oldest)"]
    sort_by = st.selectbox("Sort By:", sort_options)

with col6:
    st.write("")  # Spacing
    st.write("")  # Spacing
    col_apply, col_clear = st.columns(2)
    with col_apply:
        apply_btn = st.button("Apply Filters", use_container_width=True)
    with col_clear:
        clear_btn = st.button("Clear Filters", use_container_width=True)
        if clear_btn:
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Apply Filters
filtered_df = df.copy()

if selected_users:
    filtered_df = filtered_df[filtered_df['Username'].isin(selected_users)]

filtered_df = filtered_df[filtered_df['Sentiment'].isin(sentiment_filter)]
filtered_df = filtered_df[filtered_df['Likes'] >= min_likes]
filtered_df = filtered_df[filtered_df['Retweets'] >= min_retweets]

# Sort Data
if sort_by == "Likes (Most First)":
    filtered_df = filtered_df.sort_values('Likes', ascending=False)
elif sort_by == "Retweets (Most First)":
    filtered_df = filtered_df.sort_values('Retweets', ascending=False)
elif sort_by == "Date (Newest)":
    filtered_df = filtered_df.sort_values('Timestamp', ascending=False)
else:
    filtered_df = filtered_df.sort_values('Timestamp', ascending=True)

st.markdown("---")

# Results Summary
st.subheader("Your Query Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Matching Records</div>
            <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{len(filtered_df):,}</div>
            <div style='color: #657786; font-size: 0.9em;'>of {len(df):,} total</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Likes</div>
            <div style='font-size: 2em; font-weight: bold; color: #e74c3c; margin: 10px 0;'>{filtered_df['Likes'].sum():,.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>in results</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='metric-card'>
            <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Total Retweets</div>
            <div style='font-size: 2em; font-weight: bold; color: #2ecc71; margin: 10px 0;'>{filtered_df['Retweets'].sum():,.0f}</div>
            <div style='color: #657786; font-size: 0.9em;'>in results</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    if len(filtered_df) > 0:
        avg_eng = (filtered_df['Likes'].mean() + filtered_df['Retweets'].mean())
        st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Avg Engagement</div>
                <div style='font-size: 2em; font-weight: bold; color: #1DA1F2; margin: 10px 0;'>{avg_eng:.0f}</div>
                <div style='color: #657786; font-size: 0.9em;'>per tweet</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Avg Engagement</div>
                <div style='font-size: 2em; font-weight: bold; color: #999; margin: 10px 0;'>N/A</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Data Table
st.subheader("Conversation Details")

if len(filtered_df) > 0:
    st.markdown("""
        <div class='story-text'>
            Below is your filtered dataset. Click column headers to sort, or use the search box to find specific conversations.
        </div>
    """, unsafe_allow_html=True)
    
    display_df = filtered_df[['Username', 'Text', 'Likes', 'Retweets', 'Sentiment', 'Timestamp']].copy()
    st.dataframe(display_df, use_container_width=True, height=400)
else:
    st.warning("No conversations match your filters. Try adjusting your criteria.")

st.markdown("---")

# Download Section
st.subheader("Export Your Results")

st.markdown("""
    <div class='story-text'>
        Export your filtered results in multiple formats for use in other tools, further analysis, or reporting.
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="twitter_data_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    try:
        excel_buffer = io.BytesIO()
        filtered_df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        st.download_button(
            label="Download as Excel",
            data=excel_buffer,
            file_name="twitter_data_filtered.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
    except:
        st.info("Excel export requires openpyxl: pip install openpyxl")

with col3:
    json_data = filtered_df.to_json(orient='records', indent=2)
    st.download_button(
        label="Download as JSON",
        data=json_data,
        file_name="twitter_data_filtered.json",
        mime="application/json",
        use_container_width=True
    )

st.markdown("---")

# Statistics by Selection
if len(filtered_df) > 0:
    st.subheader("Quick Analysis of Your Selection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Sentiment Breakdown</div>
        """, unsafe_allow_html=True)
        
        sentiment_counts = filtered_df['Sentiment'].value_counts()
        for sentiment, count in sentiment_counts.items():
            pct = count / len(filtered_df) * 100
            st.write(f"**{sentiment}:** {count} ({pct:.1f}%)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div style='color: #657786; font-size: 0.85em; font-weight: 600; text-transform: uppercase;'>Engagement Stats</div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Avg Likes:** {filtered_df['Likes'].mean():.1f}")
        st.write(f"**Avg Retweets:** {filtered_df['Retweets'].mean():.1f}")
        st.write(f"**Max Likes:** {filtered_df['Likes'].max():.0f}")
        st.write(f"**Max Retweets:** {filtered_df['Retweets'].max():.0f}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No data to analyze. Try adjusting your filters.")