from classifier import classify_intent
from router import route_and_respond
from logger import log_route


def main():

    print("LLM Prompt Router Started")

    while True:

        user_message = input("\nUser: ")

        intent_data = classify_intent(user_message)

        response = route_and_respond(user_message, intent_data)

        log_route(
            intent_data["intent"],
            intent_data["confidence"],
            user_message,
            response
        )

        print("\nAssistant:", response)


if __name__ == "__main__":
    main()