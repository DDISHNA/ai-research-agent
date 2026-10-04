from agent import run_agent
while True:
    question = input("\nYou: ")
    if question.lower() == "exit":
        break
    answer = run_agent(question)

    print("\n AI Agent:")
    print(answer)