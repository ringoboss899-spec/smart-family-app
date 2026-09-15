import streamlit as st
from google import genai

# Page setup
st.title("🏡 Smart Family Assistant")
st.write("Aapke ghar ka apna AI assistant!")

# API Key input
api_key = st.text_input("Apni Gemini API Key yahan dalein:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    # User message input
    user_prompt = st.text_input("Ghar ke baare mein kuch bhi poochein:")
    
    if user_prompt:
        # Prompt definition
        system_instruction = """
        Aap ek Smart Family Assistant hain. Aap ghar ke tamaam afraad ki madad karte hain.
        Aapko ghar ke rules, schedules, aur aam sawal-jawab mein madad karni hai.
        Aapka lehja hamesha respectful, friendly aur helpful hona chahiye.
        """
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{system_instruction}\n\nUser Question: {user_prompt}"
        )
        st.write("### Jawab:")
        st.write(response.text)