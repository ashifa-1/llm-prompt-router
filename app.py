import os
from dotenv import load_dotenv
from classifier import classify_intent
from router import route_and_respond
from logger import log_route


def main():
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        print("\n[WARNING] GROQ_API_KEY is not set.")
        print("Please create a .env file from .env.example with your GROQ_API_KEY to interact with the LLM.\n")

    print("=========================================")
    print("      LLM Prompt Router Started          ")
    print(" Type 'exit' or 'quit' to end the session")
    print("=========================================")

    while True:
        try:
            user_message = input("\nUser: ").strip()

            if not user_message:
                continue

            if user_message.lower() in {"exit", "quit", "q"}:
                print("Exiting LLM Prompt Router. Goodbye!")
                break

            intent_data = classify_intent(user_message)

            response = route_and_respond(user_message, intent_data)

            log_route(
                intent_data["intent"],
                intent_data["confidence"],
                user_message,
                response
            )

            print(f"\n[Detected Intent: {intent_data['intent']} | Confidence: {intent_data['confidence']:.2f}]")
            print("Assistant:", response)

        except (KeyboardInterrupt, EOFError):
            print("\n\nSession terminated. Goodbye!")
            break


if __name__ == "__main__":
    main()
