from ddgs import DDGS
def search_web(query):
    print(f"\n Searching web for: {query}")
    results = []
    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=5
        )
        for result in search_results:
            results.append({
                'title':result.get("title"),
                'url': result.get('href'),
                'snippet': result.get('body')
            })
    return results

def calculator(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Calculation error: {e}"