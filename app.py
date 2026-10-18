
import streamlit as st
from google import genai

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Secure API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API key setup check pannunga: Streamlit Secrets.")
    st.stop()

# Session setup
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 1

# Sidebar
with st.sidebar:
    st.title("🤖 My AI Chatbot")
    st.caption("Your personal AI assistant")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count += 1
        st.rerun()

    st.divider()
    st.subheader("About")
    st.write("Ask questions, learn Python, and explore ideas.")
    st.caption("Chat history is kept for this session only.")

# Main page
st.title("🤖 My AI Chatbot")
st.caption("Ask me anything — Python, studies, projects and more!")

# Show existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Send recent conversation context
    history = []
    for msg in st.session_state.messages[-12:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history.append(f"{role}: {msg['content']}")

    conversation = "\n".join(history)

    try:
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=(
                        "You are a helpful AI assistant. "
                        "Answer clearly, honestly, and simply. "
                        "If the user asks for Thanglish, use Thanglish.\n\n"
                        + conversation
                    )
                )

                answer = response.text or "No answer generated."
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        error_text = str(e)

        if "503" in error_text or "UNAVAILABLE" in error_text:
            st.warning(
                "AI server busy-a irukku. "
                "Konjam wait pannitu try pannunga."
            )
        elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            st.warning(
                "API usage limit reach aagirukkalaam. "
                "Konjam neram kazhichu try pannunga."
            )
        else:
            st.error("Response generate panna mudiyala.")
            st.caption(f"Error type: {type(e).__name__}")
