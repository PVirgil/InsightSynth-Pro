import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Simulated dashboard logic
class InsightGenerator:
    @staticmethod
    def generate_from_data(df: pd.DataFrame):
        if df.empty:
            return ["No data uploaded."]
        return [
            f"Dataset has {len(df)} rows.",
            "Example insight: High churn in Segment B",
            "Feature Y usage down 12% in Q2"
        ]

class ChatAgent:
    @staticmethod
    def reply(user_id: str, message: str) -> str:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a business intelligence assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

class DashboardAPI:
    @staticmethod
    def get_metrics(df: pd.DataFrame):
        return {
            "row_count": len(df),
            "columns": list(df.columns)
        } if not df.empty else {"info": "No data"}

# Streamlit UI
st.set_page_config(page_title="InsightSynth Pro", layout="centered")
st.title("📊 InsightSynth Pro")

user_id = st.text_input("Enter User ID")

uploaded_file = st.file_uploader("Upload CSV Data", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.DataFrame()

if user_id:
    st.subheader("🧠 Chat with Insight AI")
    if 'chat' not in st.session_state:
        st.session_state.chat = []

    user_msg = st.text_input("Type your message")
    if st.button("Send") and user_msg:
        response = ChatAgent.reply(user_id, user_msg)
        st.session_state.chat.append((user_msg, response))

    for u, r in st.session_state.chat:
        st.markdown(f"**You:** {u}")
        st.markdown(f"**AI:** {r}")

    st.subheader("📈 Insights from Your Data")
    if st.button("Generate Insights"):
        insights = InsightGenerator.generate_from_data(df)
        for i in insights:
            st.markdown(f"- {i}")

    st.subheader("📊 Dashboard Metrics")
    if st.button("Show Dashboard"):
        metrics = DashboardAPI.get_metrics(df)
        st.json(metrics)

    if not df.empty:
        st.download_button("📥 Download Uploaded Data", df.to_csv(index=False), file_name="uploaded_data.csv")
