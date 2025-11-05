# app_minimal.py
# (קובץ Streamlit מינימלי לצ'אט בלבד)

import streamlit as st
from vertexai.generative_models import Content, Part

# מייבאים את שירות ה-Gemini שיצרנו
import gemini_service as gemini_service

# 1. הגדרות עמוד
# (מוגדר פעם אחת בתחילת הריצה)
st.set_page_config(
    page_title="חוקר | רשות התחרות (MVP)",
    page_icon="🤖"
)

st.title("מערכת חקירות (גרסת MVP - צ'אט בלבד)")

# 2. אתחול ה-Session State
# אנו שומרים את היסטוריית הצ'אט בזיכרון של הסשן
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. הצגת היסטוריית הצ'אט
# עובר על כל ההודעות השמורות ומציג אותן
for message in st.session_state.chat_history:
    # כל 'message' הוא אובייקט Content של Vertex
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# 4. קבלת קלט מהמשתמש
prompt = st.chat_input("שאל אותי כל דבר על חוק התחרות או שיטות חקירה...")

if prompt:
    # א. הצג את הודעת המשתמש
    st.chat_message("user").markdown(prompt)
    
    # ב. הוסף את הודעת המשתמש להיסטוריה (בפורמט הנדרש ע"י Vertex)
    st.session_state.chat_history.append(Content(role="user", parts=[Part.from_text(prompt)]))

    # ג. קבלת תגובה מהמודל
    try:
        with st.spinner("חושב..."):
            # שימוש בפונקציה מהשירות שיצרנו
            response_text = gemini_service.get_chat_response(
                st.session_state.chat_history,
                prompt
            )

        # ד. הצג את תגובת המודל
        st.chat_message("model").markdown(response_text)
        
        # ה. הוסף את תגובת המודל להיסטוריה
        st.session_state.chat_history.append(Content(role="model", parts=[Part.from_text(response_text)]))

    except Exception as e:
        st.error(f"אירעה שגיאה בפנייה ל-Vertex AI: {e}")