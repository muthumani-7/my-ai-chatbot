
import streamlit as st
from google import genai

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.caption("Ask me anything!")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("API key missing. Check secrets.toml.")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("＋ New Chat"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message here...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

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
                        "Answer clearly and honestly.\n\n"
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
            "Konjam neram wait pannitu retry pannunga."
        )
    elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
        st.warning(
            "API usage limit reach aagirukkalaam. "
            "Konjam neram kazhichu try pannunga."
        )
    else:
        st.error("Sorry, response generate panna mudiyala.")
        st.caption(f"Error type: {type(e).__name__}")
