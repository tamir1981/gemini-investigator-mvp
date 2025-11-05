# app/backend/services/gemini_service.py
# (מותאם למינימום, כפי שנדרש בתוכנית)

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Content

# אנו מייבאים את ההגדרות מהקובץ שהגדרנו
import project_settings as settings

# 1. אתחול Vertex AI
# זה קורה פעם אחת כשהמודול נטען (יעיל עבור Cloud Run)
vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)

# 2. טעינת הפרומפט והגדרת המודל
# אנו מגדירים את המודל פעם אחת עם הפרומפט המערכתי
SYSTEM_INSTRUCTION = settings.get_system_prompt('chat')

MODEL = GenerativeModel(
    settings.GEMINI_MODEL,
    system_instruction=SYSTEM_INSTRUCTION
)

# 3. הגדרות יצירת הטקסט
GENERATION_CONFIG = GenerationConfig(
    max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
    temperature=settings.GEMINI_TEMPERATURE,
    top_p=settings.GEMINI_TOP_P
)

def get_chat_response(history: list[Content], new_prompt: str) -> str:
    """
    מקבל היסטוריית צ'אט והנחיה חדשה, ומחזיר את תגובת המודל.
    
    Args:
        history: רשימה של אובייקטי Content (היסטוריית הצ'אט)
        new_prompt: ההודעה החדשה של המשתמש

    Returns:
        תגובת המודל כטקסט
    """
    # 4. יצירת סשן צ'אט על בסיס ההיסטוריה
    # המודל עצמו כבר מוגדר עם הפרומפט המערכתי
    chat_session = MODEL.start_chat(history=history)
    
    # 5. שליחת ההודעה החדשה וקבלת תשובה
    response = chat_session.send_message(
        new_prompt,
        generation_config=GENERATION_CONFIG
    )
    
    return response.text