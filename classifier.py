import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

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


CLASSIFIER_PROMPT = """
Your task is to classify the user's intent into exactly ONE category.

Available categories:
- code: Programming help, debugging, writing code or functions, syntax, algorithms, technical explanations of code, SQL queries (e.g. SELECT, JOIN, database schemas), and software development. Note: requests asking to explain, analyze, or debug code/SQL belong in 'code', not 'writing'.
- data: Data analysis, statistics (e.g. mean, median, correlation, distributions), interpreting datasets, metrics, and data visualization recommendations.
- writing: Critiquing or improving written prose/essays, checking clarity, grammar, tone, flow, structure, or proofreading human language text. Note: this is for human language/prose feedback, not code or SQL.
- career: Career advice, job searching, resume or CV reviews, interview preparation, career transitions, and workplace guidance.
- unclear: Greetings, chit-chat, ambiguous requests, gibberish, or requests that do not clearly fit any of the categories above.

Respond ONLY with valid JSON in this exact structure:
{
 "intent": "<category>",
 "confidence": <number between 0.0 and 1.0>
}
"""

VALID_INTENTS = {"code", "data", "writing", "career", "unclear"}


def classify_intent(message: str):

    try:
        active_client = get_client()

        # JSON-mode formatting via response_format parameter
        response = active_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Markdown stripping: clean ```json ... ``` or ``` ... ``` fences if present
        if "```" in content:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
            if match:
                content = match.group(1).strip()
            else:
                content = content.replace("```", "").strip()

        parsed = json.loads(content)

        intent = str(parsed.get("intent", "unclear")).strip().lower()
        if intent not in VALID_INTENTS:
            intent = "unclear"

        confidence = float(parsed.get("confidence", 0.0))
        confidence = max(0.0, min(1.0, confidence))

        return {
            "intent": intent,
            "confidence": confidence
        }

    except Exception as e:

        print("Classifier error:", e)

        return {
            "intent": "unclear",
            "confidence": 0.0
        }
