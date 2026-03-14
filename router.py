import os
from dotenv import load_dotenv
from groq import Groq
from prompts import SYSTEM_PROMPTS

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def route_and_respond(message: str, intent_data: dict):

    intent = intent_data["intent"]
    confidence = intent_data["confidence"]

    if confidence < 0.7:
        intent = "unclear"

    if intent == "unclear":
        return "I'm not sure what you need. Are you asking about coding, data analysis, writing help, or career advice?"
    system_prompt = SYSTEM_PROMPTS.get(intent)

    try:

        response = client.chat.completions.create(
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