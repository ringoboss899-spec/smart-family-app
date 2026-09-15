import streamlit as st
from google import genai
from google.genai import types

# Page Config
st.set_page_config(
    page_title="Smart Family Assistant", 
    page_icon="🤖", 
    layout="wide"
)

# --- LEFT SIDEBAR ---
with st.sidebar:
    st.title("🤖 Assistant Menu")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    with st.expander("📎 Attach Files & Media", expanded=True):
        st.write("Upload images, videos, audio, or files for analysis:")
        audio_file = st.audio_input("🎤 Voice Input")
        uploaded_files = st.file_uploader(
            "📁 Upload Images, Videos or Documents",
            type=["png", "jpg", "jpeg", "mp4", "mp3", "wav", "pdf", "txt"],
            accept_multiple_files=True
        )

    st.markdown("---")

    with st.expander("📚 Library & History", expanded=False):
        if "messages" in st.session_state and len(st.session_state.messages) > 0:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.caption(f"💬 {msg['content'][:25]}...")
        else:
            st.caption("No history yet.")

    with st.expander("⚙️ Settings", expanded=False):
        st.info("API Key securely loaded from Secrets 🔒")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption("Powered by Gemini AI 🚀")

# --- MAIN CHAT INTERFACE ---
st.title("🤖 Smart Family Assistant")

st.markdown("""
<div style="background-color: #e8f0fe; border-left: 5px solid #1a73e8; padding: 16px; border-radius: 8px; color: #1f1f1f; margin-bottom: 25px;">
    <h4 style="margin: 0; color: #1a73e8;">✨ Welcome to Smart Family Assistant!</h4>
    <p style="margin: 6px 0 0 0; font-size: 15px; font-weight: 500;">
        🏠 Ask anything in any language—from daily routines and recipes to study help, images, audio, and video analysis!
    </p>
</div>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please add `GEMINI_API_KEY` in Settings > Secrets.")
else:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask anything about your home or uploads..."):
        
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking... 💡"):
                sys_instruct = (
                    "You are a Smart Family Assistant. You help all family members with daily tasks, schedules, "
                    "recipes, education, text, code, images, videos, and general knowledge. "
                    "You MUST automatically detect and respond in whatever language the user speaks to you. "
                    "Keep your tone respectful, friendly, and helpful at all times."
                )
                
                # Payload setup
                contents_payload = []
                
                # Add text input
                contents_payload.append(types.Part.from_text(text=user_prompt))
                
                # Add uploaded files if available
                if uploaded_files:
                    for uf in uploaded_files:
                        contents_payload.append(
                            types.Part.from_bytes(data=uf.read(), mime_type=uf.type)
                        )
                
                # Add audio recording if available
                if audio_file:
                    contents_payload.append(
                        types.Part.from_bytes(data=audio_file.read(), mime_type=audio_file.type)
                    )

                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_payload,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_instruct
                        )
                    )
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error generating response: {e}")
