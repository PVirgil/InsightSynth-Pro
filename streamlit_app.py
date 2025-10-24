import streamlit as st

# Simulated backend modules
class DataIngestor:
    @staticmethod
    def ingest(source: str, payload: dict) -> str:
        return f"Data from {source} ingested."

class InsightGenerator:
    @staticmethod
    def generate_for_user(user_id: str):
        return [
            "Customer satisfaction down 10%",
            "Spike in support tickets for Feature Y",
            "NPS dropping in Tier A segment"
        ]

class ChatAgent:
    @staticmethod
    def reply(user_id: str, message: str) -> str:
        return f"You said: '{message}'. Here's a recommendation: Improve Feature Y based on recent feedback."

class DashboardAPI:
    @staticmethod
    def get_dashboard(user_id: str):
        return {
            "churn_rate": "12.5%",
            "NPS": 34,
            "support_tickets": 47
        }

# Streamlit UI
st.set_page_config(page_title="InsightSynth Pro", layout="centered")
st.title("📊 InsightSynth Pro")

user_id = st.text_input("Enter User ID")

if user_id:
    st.subheader("🧠 Chat with Insight AI")
    if 'chat' not in st.session_state:
        st.session_state.chat = []

    user_msg = st.text_input("Type your message")
    if st.button("Send") and user_msg:
        response = ChatAgent.reply(user_id, user_msg)
        st.session_state.chat.append((user_msg, response))

    for i, (u, r) in enumerate(st.session_state.chat):
        st.markdown(f"**You:** {u}")
        st.markdown(f"**AI:** {r}")

    st.subheader("📈 Insights")
    if st.button("Generate Insights"):
        insights = InsightGenerator.generate_for_user(user_id)
        for i in insights:
            st.markdown(f"- {i}")

    st.subheader("📊 Dashboard Metrics")
    if st.button("Show Dashboard"):
        metrics = DashboardAPI.get_dashboard(user_id)
        st.json(metrics)
