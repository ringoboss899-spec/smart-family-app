import streamlit as st
from google import genai

# Page config & Title
st.set_page_config(page_title="Smart Family Assistant", page_icon="🤖")
st.title("🤖 Smart Family Assistant")

# Gemini jaisa Blue & White Note Box
st.markdown("""
<div style="background-color: #e8f0fe; border-left: 5px solid #1a73e8; padding: 15px; border-radius: 8px; color: #1f1f1f; margin-bottom: 25px;">
    <h4 style="margin: 0; color: #1a73e8;">💡 Welcome to Smart Family Assistant!</h4>
    <p style="margin: 5px 0 0 0; font-size: 14px;">
        Ask anything about home routines, recipes, study help, or daily tasks. Your key is safely saved in Secrets!
    </p>st.markdown("""
<div style="background-color: #e8f0fe; border-left: 5px solid #1a73e8; padding: 15px; border-radius: 8px; color: #1f1f1f; margin-bottom: 25px;">
    <h4 style="margin: 0; color: #1a73e8;">✨ Welcome to Smart Family Assistant!</h4>
    <p style="margin: 5px 0 0 0; font-size: 15px; font-weight: 500;">
        🏠 Ask anything about your home—from daily routines and recipes to study help and fun ideas!
    </p>
</div>
""", unsafe_allow_html=True)
</div>
""", unsafe_allow_html=True)

# Streamlit Secrets se API Key automatic load karna
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key nahi mili! Settings > Secrets mein GEMINI_API_KEY add karein.")
else:
    client = genai.Client(api_key=api_key)

    # Chat history session storage
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Upar Purane Answers aur Questions Show Karna
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Neeche ChatGPT/Gemini jaisa Input Box
    if user_prompt := st.chat_input("Ghar ke baare mein kuch bhi poochein..."):
        # User message display aur save karna
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # AI Response generate karna
        with st.chat_message("assistant"):
            system_instruction = """
            Aap ek Smart Family Assistant hain. Aap ghar ke tamaam afraad ki madad karte hain. 
            Aapko ghar ke rules, schedules, aur aam sawal-jawab mein madad karni hai. 
            Aapka lehja hamesha respectful, friendly aur helpful hona chahiye.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"{system_instruction}\n\nUser Question: {user_prompt}"
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
