import ollama

def call_ollama_analysis(content: str):
    # Specialized prompt for the "Scientific Instrument" feel
    response = ollama.chat(model='llama3.1:8b', messages=[
        {'role': 'system', 'content': 'Analyze the entry. Return ONLY JSON: sentiment (0-1), topics (list), cognitive_load (string), summary (string).'},
        {'role': 'user', 'content': content},
    ], format='json')
    
    return response['message']['content']