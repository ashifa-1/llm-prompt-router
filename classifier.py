import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CLASSIFIER_PROMPT = """
Your task is to classify the user's intent.

Choose ONE label from:
code
data
writing
career
unclear

Respond ONLY with JSON in this format:

{
 "intent": "label",
 "confidence": number between 0 and 1
}

Do not include explanations.
"""


def classify_intent(message: str):

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        parsed = json.loads(content)

        return {
            "intent": parsed.get("intent", "unclear"),
            "confidence": float(parsed.get("confidence", 0.0))
        }

    except Exception as e:

        print("Classifier error:", e)

        return {
            "intent": "unclear",
            "confidence": 0.0
        }