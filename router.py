from prompts import SYSTEM_PROMPTS


def route_and_respond(message: str, intent_data: dict):

    intent = intent_data["intent"]

    if intent == "unclear":
        return "I'm not sure what you need. Are you asking about coding, data analysis, writing help, or career advice?"

    system_prompt = SYSTEM_PROMPTS.get(intent)

    response = f"[{intent.upper()} EXPERT RESPONSE]\n\nUser message: {message}\n\nSystem prompt used:\n{system_prompt}"

    return response