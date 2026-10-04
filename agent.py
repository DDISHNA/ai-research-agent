import ollama
conversation = []
def run_agent(user_question):
    conversation.append({
        "role":"user",
        "content": user_question
    })

    response = ollama.chat(
        model="gemma4:12b",
        messages=conversation
    )
    answer = response["message"]["content"]
    conversation.append({
        "role":"assistant",
        "content":answer
    })
    return answer