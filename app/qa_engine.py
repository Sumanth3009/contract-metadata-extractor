from transformers import pipeline

qa = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2"
)

def ask(context, question):
    return qa(question=question, context=context)["answer"]
