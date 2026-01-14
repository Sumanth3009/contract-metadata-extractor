from .qa_engine import ask

QUESTIONS = {
    "Agreement Value": "What is the agreement value?",
    "Agreement Start Date": "When does the agreement start?",
    "Agreement End Date": "When does the agreement end?",
    "Renewal Notice (Days)": "How many days notice is required for renewal?",
    "Party One": "Who is the first party in the agreement?",
    "Party Two": "Who is the second party in the agreement?"
}

def extract_fields(text):
    result = {}
    for field, question in QUESTIONS.items():
        result[field] = ask(text, question)
    return result
