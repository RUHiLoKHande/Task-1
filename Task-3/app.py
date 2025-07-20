import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from datetime import datetime

st.set_page_config(page_title="Simple Chatbot Analytics", layout="wide")

class ChatbotAnalytics:
    def __init__(self):
        self.chat_logs = []

    def log_interaction(self, user_id, query, response, feedback=None):
        self.chat_logs.append({
            "user_id": user_id,
            "timestamp": datetime.now(),
            "query": query,
            "response": response,
            "feedback": feedback
        })

    def get_dataframe(self):
        return pd.DataFrame(self.chat_logs)

    def get_common_queries(self, n=5):
        if not self.chat_logs:
            return []
        queries = [log["query"] for log in self.chat_logs]
        return Counter(queries).most_common(n)

    def get_avg_feedback(self):
        feedbacks = [log["feedback"] for log in self.chat_logs if log["feedback"] is not None]
        if not feedbacks:
            return None, 0
        return round(sum(feedbacks) / len(feedbacks), 1), len(feedbacks)

    def get_user_stats(self):
        df = self.get_dataframe()
        if df.empty:
            return 0, 0
        total_users = df['user_id'].nunique()
        avg_queries = round(df['user_id'].value_counts().mean(), 1)
        return total_users, avg_queries

    def get_activity_data(self):
        df = self.get_dataframe()
        if df.empty:
            return None
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        return df

analytics = ChatbotAnalytics()

sample_data = [
    ("user1", "What is AI?", "AI is Artificial Intelligence.", 4),
    ("user2", "How to use pandas?", "Pandas is used for data analysis.", 5),
    ("user1", "What is NumPy?", "NumPy helps with numerical calculations.", 3),
    ("user3", "Explain machine learning", "ML is a subset of AI.", 4),
    ("user2", "What is Streamlit?", "Streamlit is for building data apps.", 5),
]
for entry in sample_data:
    analytics.log_interaction(*entry)

st.title("🤖 Simple Chatbot Analytics Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Queries", len(analytics.chat_logs))
avg_feedback, count = analytics.get_avg_feedback()
col2.metric("Avg Rating", f"{avg_feedback} ★" if avg_feedback else "N/A", f"{count} ratings")
users, avg_queries = analytics.get_user_stats()
col3.metric("Unique Users", users)
col4.metric("Avg Queries/User", avg_queries)

st.markdown("---")

st.subheader("📌 Most Common Queries")
common_queries = analytics.get_common_queries()
if common_queries:
    queries, counts = zip(*common_queries)
    fig, ax = plt.subplots()
    ax.barh(queries, counts, color='skyblue')
    ax.set_xlabel("Frequency")
    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.info("No queries yet.")

st.subheader("⭐ Satisfaction Ratings")
df = analytics.get_dataframe()
if not df.empty and df['feedback'].notna().any():
    feedback = df['feedback'].dropna()
    fig, ax = plt.subplots()
    ax.hist(feedback, bins=[1, 2, 3, 4, 5, 6], color='lightgreen', edgecolor='black')
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xlabel("Rating (1–5)")
    st.pyplot(fig)
else:
    st.info("No feedback available.")

st.subheader("📈 Query Activity Over Time")
df_activity = analytics.get_activity_data()
if df_activity is not None:
    tab1, tab2 = st.tabs(["By Date", "By Hour"])
    with tab1:
        daily = df_activity.groupby("date").size()
        st.line_chart(daily)
    with tab2:
        hourly = df_activity.groupby("hour").size()
        st.bar_chart(hourly)
else:
    st.info("No activity data.")

st.subheader("📄 All Chat Logs")
st.dataframe(analytics.get_dataframe(), use_container_width=True)

st.sidebar.header("Admin Controls")

if st.sidebar.button("➕ Add Random Data"):
    for _ in range(5):
        analytics.log_interaction(
            user_id=f"user{np.random.randint(100)}",
            query=np.random.choice(["What is clustering?", "Explain data structures", "Use of Scikit-learn"]),
            response="Auto response",
            feedback=np.random.randint(1, 6)
        )
    st.rerun()

if st.sidebar.button("🧹 Clear Logs"):
    analytics.chat_logs = []
    st.rerun()