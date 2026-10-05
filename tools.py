def search_web(query):
    print(f"searching for: {query}")
    return f"search bresults for:{query}"
def calculator(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Calculation error: {e}"