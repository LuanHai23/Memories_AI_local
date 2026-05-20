import streamlit as st
import requests

# URL của backend API
API_BASE_URL = "http://127.0.0.1:8000"

# Cấu hình của streamlit
st.set_page_config(
    page_title="Memories Agent",
    page_icon="🧠",
    layout="wide"
)

# Title app
st.title("🧠 Memories Agent")
st.caption("Local-first RAG Agent with Long-Term Memory and Observability")

# Sidebar
# Nhập thủ công
user_id = st.sidebar.text_input("User ID", value="LunaCbum")

st.sidebar.markdown("System Status")
st.sidebar.write("Backend:", API_BASE_URL)

# Session state
# Lưu conversation history trong session state để hiển thị
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị history chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input chat

user_input = st.chat_input("Ask MemoRAG something")

# Khi user gửi câu hỏi
if user_input:
    # Lưu message user vào session_state để hiển thị trên UI
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


