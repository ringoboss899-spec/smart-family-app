import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config & Title (100% English UI)
st.set_page_config(
    page_title="Smart Family Assistant", 
    page_icon="🤖", 
    layout="wide"
)

# --- LEFT SIDEBAR (Navigation & Controls) ---
with st.sidebar:
    st.title("🤖 Assistant Menu")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Media & File Attachments Section
    with st.expander("📎 Attach Files & Media", expanded=True):
        st.write("Upload images, videos, audio, or files for analysis:")
        
        # Audio / Voice Recording Input
        audio_file = st.audio_input("🎤 Voice Input")
        
        # File Uploader (Images, Videos, PDFs, Text)
        uploaded_files = st.file_uploader(
            "📁 Upload Images, Videos or Documents",
            type=["png", "jpg", "jpeg", "mp4", "mp3", "wav", "pdf", "txt"],
            accept_multiple_files=True
        )

    st.markdown("---")

    # Library / Chat History
    with st.expander("📚 Library & History", expanded=False):
        if "messages" in st.session_state and len(st.session_state.messages) > 0:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.caption(f"💬 {msg['content'][:25]}...")
        else:
            st.caption("No history yet.")

    # Settings Option
    with st.expander("⚙️ Settings", expanded=False):
        st.info("API Key securely loaded from Secrets 🔒")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption("Powered by Gemini AI 🚀")

# --- MAIN CHAT INTERFACE ---
st.title("🤖 Smart Family Assistant")

# English Welcome Banner
st.markdown("""
<div style="background-color: #e8f0fe; border-left: 5px solid #1a73e8; padding: 16px; border-radius: 8px; color: #1f1f1f; margin-bottom: 25px;">
    <h4 style="margin: 0; color: #1a73e8;">✨ Welcome to Smart Family Assistant!</h4>
    <p style="margin: 6px 0 0 0; font-size: 15px; font-weight: 500;">
        🏠 Ask anything in any language—from daily routines and recipes to study help, images, audio, and video analysis!
    </p>
</div>
""", unsafe_allow_html=True)

# Fetch API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ API Key not found! Please add `GEMINI_API_KEY` in Settings > Secrets.")
else:
    client = genai.Client(api_key=api_key)

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Box at the bottom
    if user_prompt := st.chat_input("Ask anything about your home or uploads..."):
        
        # Display and save user message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate Multilingual & Multimodal AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 💡"):
                # System prompt forcing multilingual capability & friendly demeanor
                system_instruction = """
                You are a Smart Family Assistant. You help all family members with daily tasks, schedules, 
                recipes, education, text, code, images, videos, and general knowledge.
                You MUST automatically detect and respond in whatever language the user speaks to you 
                (English, Urdu, Hindi, Arabic, Spanish, French, etc.).
                Keep your tone respectful, friendly, and helpful at all times.
                """
                
                # Prepare content payload
                contents_payload = [f"{system_instruction}\n\nUser Question: {user_prompt}"]
                
                # Append media files if uploaded via Sidebar
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        bytes_data = uploaded_file.read()
                        mime_type = uploaded_file.type
                        contents_payload.append(
                            types.Part.from_bytes(data=bytes_data, mime_type=mime_type)
                        )
                
                # Generate Content via Gemini API
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents_payload
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
