import os
from dotenv import load_dotenv
from groq import Groq
from prompts import SYSTEM_PROMPTS

load_dotenv()

client = None


def get_client():
    global client
    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it in your .env file or environment variables."
            )
        client = Groq(api_key=api_key)
    return client


def route_and_respond(message: str, intent_data: dict):

    intent = intent_data.get("intent", "unclear")
    confidence = float(intent_data.get("confidence", 0.0))

    if confidence < 0.7 or intent not in SYSTEM_PROMPTS:
        intent = "unclear"

    if intent == "unclear":
        return "I'm not sure what you need. Are you asking about coding, data analysis, writing help, or career advice?"

    system_prompt = SYSTEM_PROMPTS.get(intent)
    if not system_prompt:
        return "I'm not sure what you need. Are you asking about coding, data analysis, writing help, or career advice?"

    try:
        active_client = get_client()

        response = active_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        print("Router error:", e)

        return "Sorry, something went wrong while generating the response."
