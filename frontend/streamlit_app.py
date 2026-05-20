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

    # Hiển thị message
    with st.chat_message("user"):
        st.write(user_input)

    # Call backen và hiển thị câu trả lời
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            try:
                # Gửi request sang FastAPI
                response = requests.post(
                    f"{API_BASE_URL}/chat/",
                    json = {
                        "user_id": user_id,
                        "message": user_input
                    },
                    timeout=180
                )

                # Status code lỗi thì ráie exception
                response.raise_for_status()

                # Convert JSON response thành dict
                data = response.json()

                # Lấy answer và latency từ backend
                answer = data["answer"]
                latency_ms = data["latency_ms"]

                # hiển thị answer
                st.write(answer)

                # Hiển thị latency
                st.caption(f" Latency: {latency_ms} ms")

                # Hiển thị answer
                st.write(answer)

                # Lưu assistant answer vào session_state
                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content": answer
                    }
                )
            except Exception as e:
                # Nếu backend lỗi, Ollama lỗi hoặc bị timeout
                error_msg = f"Error: {str(e)}"

                st.error(error_msg)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg
                    }
                )

