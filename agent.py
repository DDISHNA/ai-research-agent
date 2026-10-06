import ollama
import json
from tools import calculator, search_web

conversation = []


def run_agent(user_question, tool_callback=None):

    # --------------------------------
    # 1. Save user's question
    # --------------------------------

    conversation.append({
        "role": "user",
        "content": user_question
    })

    system_prompt = """
You are an AI Agent.

You have access to two tools.

1. calculator
   Use for mathematical calculations.

2. web_search
   Use when current or internet information is required.

You MUST return ONLY valid JSON.

For calculator:

{
    "action": "calculator",
    "expression": "mathematical expression"
}

For web search:

{
    "action": "web_search",
    "query": "search query"
}

If you have enough information to answer:

{
    "action": "answer",
    "answer": "final answer"
}
"""

    # --------------------------------
    # 2. Internal messages
    # --------------------------------

    agent_messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        *conversation
    ]

    # --------------------------------
    # 3. Agent loop
    # --------------------------------

    while True:

        response = ollama.chat(
            model="gemma4:12b",
            messages=agent_messages
        )

        decision_text = response["message"]["content"]

        print("\nGemma decision:")
        print(decision_text)

        # Remove Markdown code fences
        decision_text = decision_text.replace("```json", "")
        decision_text = decision_text.replace("```", "")
        decision_text = decision_text.strip()

        # --------------------------------
        # 4. Convert JSON → Python dict
        # --------------------------------

        try:

            decision = json.loads(decision_text)

        except json.JSONDecodeError:

            # Gemma sometimes gives a normal text answer
            # instead of JSON after using a tool.

            answer = decision_text

            conversation.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        action = decision.get("action")

        # --------------------------------
        # 5. Final answer
        # --------------------------------

        if action == "answer":

            answer = decision["answer"]

            conversation.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        # --------------------------------
        # 6. Calculator
        # --------------------------------

        elif action == "calculator":

            expression = decision["expression"]

            print("\nUsing calculator...")
            print("Expression:", expression)

            if tool_callback:
                tool_callback(f"🔢 using calculator: `{expression}`")

            result = calculator(expression)

            print("Calculator result:", result)

        # --------------------------------
        # 7. Web search
        # --------------------------------

        elif action == "web_search":

            query = decision["query"]

            print("\nUsing web search...")
            print("Query:", query)

            if tool_callback:
                tool_callback(f"🔎 Searching the web: `{query}`")

            result = search_web(query)

            print("\nSearch results:")
            print(result)

        else:

            return "Unknown Action"

        # --------------------------------
        # 8. Give tool result to Gemma
        # --------------------------------

        agent_messages.append({
            "role": "assistant",
            "content": decision_text
        })

        agent_messages.append({
            "role": "user",
            "content": f"""
The tool returned this result:

{result}

Use this result to continue solving the original question.

If you need another tool, choose one.

If you have enough information, provide the final answer.
"""
        })