# LLM-Powered Prompt Router for Intent Classification

## Overview

This project implements a prompt routing system powered by Large Language Models (LLMs).
Instead of using a single monolithic prompt, the system first classifies the user’s intent and then routes the request to a specialized AI persona.

The system follows a two-stage architecture:

1. **Intent Classification** – A lightweight LLM call detects the user's intent and returns structured JSON.
2. **Prompt Routing** – The request is routed to a specialized expert prompt (e.g., code expert, writing coach).

This architecture improves accuracy, modularity, and maintainability compared to single-prompt systems.

---

## Architecture

User Message
→ Intent Classifier
→ Intent + Confidence
→ Prompt Router
→ Expert Persona Prompt
→ Final LLM Response

```
User → classify_intent() → route_and_respond() → Expert Prompt → Response
```

---

## Supported Intents

The classifier identifies the following intents:

* **code** – Programming help, debugging, SQL queries
* **data** – Data analysis, statistics, averages, data interpretation
* **writing** – Writing feedback, clarity improvement, tone analysis
* **career** – Career guidance, interviews, resume advice
* **unclear** – Ambiguous or unsupported requests

If the intent is **unclear**, the system asks the user for clarification instead of guessing.

---

## Project Structure

```
llm-prompt-router/
│
├── app.py         
├── classifier.py  
├── router.py      
├── prompts.py    
├── logger.py     
│
├── route_log.jsonl 
├── requirements.txt
│
├── Dockerfile
├── docker-compose.yml
│
├── .env.example    
└── README.md
```

---

## Expert Personas

The system defines specialized prompts for different tasks:

- Code Expert-- Provides production-quality code and debugging assistance.
- Data Analyst-- Interprets datasets using statistical reasoning and suggests visualizations.
- Writing Coach-- Analyzes writing clarity, tone, and structure without rewriting the text.
- Career Advisor-- Provides practical career advice and asks clarifying questions before giving recommendations.

---

## Logging

All requests are logged in **JSON Lines format** (`route_log.jsonl`).

Each entry contains:

```
{
 "intent": "code",
 "confidence": 0.92,
 "user_message": "sort python list",
 "final_response": "..."
}
```

This provides observability and debugging capability.

---

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/ashifa-1/llm-prompt-router
cd llm-prompt-router
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file based on `.env.example`.

```
GROQ_API_KEY=your_api_key_here
```

---

### 4. Run the Application

```
python app.py
```

You should see:

```
LLM Prompt Router Started
User:
```

---

## Running with Docker

Build and run the container:

```
docker compose up
```

If running manually:

```
docker build -t prompt-router .
docker run -it --env-file .env prompt-router
```

---

## Testing

The system was tested with multiple prompts covering all intent categories.

Example test prompts:

```
how do i sort a list of objects in python?
fix this bug: for i in range(10) print(i)
what's the average of these numbers: 12, 45, 23, 67, 34
This paragraph sounds awkward, can you help me fix it?
I'm preparing for a job interview, any tips?
```

Testing results are recorded in:

```
route_log.jsonl
```

---

## Conclusion

This project demonstrates a **production-style LLM routing architecture** where user requests are classified and routed to specialized AI personas. The design improves response quality and reflects patterns commonly used in modern AI applications.
