def classify_intent(message: str):

    msg = message.lower()

    if "python" in msg or "code" in msg or "bug" in msg:
        return {"intent": "code", "confidence": 0.9}

    if "data" in msg or "average" in msg or "statistics" in msg:
        return {"intent": "data", "confidence": 0.9}

    if "paragraph" in msg or "writing" in msg or "sentence" in msg:
        return {"intent": "writing", "confidence": 0.9}

    if "career" in msg or "job" in msg or "resume" in msg:
        return {"intent": "career", "confidence": 0.9}

    return {"intent": "unclear", "confidence": 0.0}