import ollama
import json 
from tools import calculator

conversation = []
def run_agent(user_question):
    # 1. Add User's question to conversation memory
    conversation.append({
            "role":"user",
            "content": user_question
        })
    # ask Gemma what it wants to do
    prompt = f"""
    You are an AI Agent.
    Decide wheather the user's question requires a calculator.
    if calculation is required, return only this JSON:
        {{
        "action": "calculator",
        "expression": "mathematical expression"
        }}
    if calculation is not required, return only this JSON:
        {{
            "action":"answer",
            "answer": "your answer"
        }}
    User question:
    {user_question}    
    """
    response = ollama.chat(
        model="gemma4:12b",
        messages=[
            {
                "role":"system",
                "content": prompt
            },
            *conversation
        ]
    )
    
    decision_text = response["message"]["content"]
    print("\nGemma decision:")
    print(decision_text)

    # 3 Convert gemma's JSON response into python data
    try:
        decision_text = decision_text.replace("```json", "")
        decision_text = decision_text.replace("```", "")
        decision_text = decision_text.strip()

        decision = json.loads(decision_text)
    except json.JSONDecodeError:
        return "I couldn't understand the agent decision."

    # 4. if gemma chooses a calculator
    if decision["action"] == "calculator":
        expression = decision["expression"]

        print("\nUsing calculator....")
        print("Expression:", expression)

        #  run the python calculator tool
        result = calculator(expression)
        print('calculator result:', result)

        # 5. give calculator result back to gemma
        conversation.append({
            "role":"assistant",
            "content":decision_text
        })
        conversation.append({
            "role":"user",
            "content": f"""
the calculator tool returned this result:
{result}
give the final answer to the user in a simple way
"""
        })
        final_response = ollama.chat(
            model="gemma4:12b",
            messages=conversation
        )
        answer = final_response["message"]["content"]

        # 6. if no tool is needed
    elif decision["action"] == "answer":
        answer = decision["answer"]
    else:
        answer = "Unknown Action"
    #  7. save gemma's final answer in memeory
    conversation.append({
        "role":"assistant",
        "content": answer
    })
    return answer