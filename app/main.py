from app.agent import run_agent

def main():
    print("🤖 AI Agent Started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Agent stopped. Goodbye!")
            break

        try:
            response = run_agent(user_input)
            print("Agent:", response)
        except Exception as e:
            print("⚠️ Error:", str(e))


if __name__ == "__main__":
    main()