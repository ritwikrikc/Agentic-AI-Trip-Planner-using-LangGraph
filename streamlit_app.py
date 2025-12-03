import streamlit as st
import requests
import datetime
import html

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="🌍 AI Travel Planner",
    layout="centered",
    page_icon="🧭",
)

# Inject CSS so text is visible on dark themes
st.markdown(
    """
    <style>
    .stApp { background-color: #0f1115; }
    .message-user {
        background: linear-gradient(180deg, #e7f1ff 0%, #d7e9ff 100%);
        color: #06121a;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .message-ai {
        background: linear-gradient(180deg, #efffed 0%, #e7ffe8 100%);
        color: #052b12;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .meta-info {
        background: rgba(255,255,255,0.02);
        color: #cdd6e0;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    .stChatInput { z-index: 9999; }
    .message-ai, .message-user {
        max-height: 480px;
        overflow: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===== Sidebar =====
with st.sidebar:
    st.title("🌍 Trip Planner Agent")
    st.write("Plan your next trip with AI ✈️🏖️🌆")
    st.markdown("---")
    st.info("👨‍💻 Built by Ritwik Chowdhury")
    st.markdown("⭐ If you like this, star the repo!")

# ===== Title =====
st.markdown("<h1 style='text-align:center;color:#e6eefc'>AI Trip Planner 🤖🧳</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#cdd6e0'>Tell me your destination, budget, duration, etc.</p>", unsafe_allow_html=True)

# ===== Chat history state =====
if "chat" not in st.session_state:
    st.session_state.chat = []

# ===== Input box (handle input first) =====
user_input = st.chat_input("Where do you want to go? 🗺️")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    with st.spinner("🧠 Generating your travel plan..."):
        try:
            response = requests.post(f"{BASE_URL}/query", json={"query": user_input}, timeout=60)
            if response.status_code == 200:
                answer = response.json().get("answer", "")
                formatted_answer = f"🗓️ Generated On: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{answer}\n\n---\n⚠️ Verify locations, timings, and prices before booking."
                st.session_state.chat.append({"role": "assistant", "content": formatted_answer})
            else:
                err_text = response.text
                st.session_state.chat.append({"role": "assistant", "content": f"❌ API Error: {err_text}"})
        except requests.exceptions.RequestException as e:
            st.session_state.chat.append({"role": "assistant", "content": f"⚠️ Failed to get response: {e}"})

# ===== Display messages (after input handling) =====
for message in st.session_state.chat:
    role = message.get("role", "")
    content = message.get("content", "")
    safe_content = html.escape(content).replace("\n", "<br>")
    if role == "user":
        st.markdown(
            f"""
            <div class="message-user">
                <strong>You 👤:</strong><br>{safe_content}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="message-ai">
                <strong>AI 🌐:</strong><br>{safe_content}
            </div>
            """,
            unsafe_allow_html=True,
        )