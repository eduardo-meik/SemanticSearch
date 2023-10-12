# qa.py
import openai

def create_prompt(context, query):
    header = ("Answer the question as truthfully as possible using the provided context, "
              "and if the answer is not contained within the text and requires some latest information to be updated, "
              "print 'No tengo suficiente contexto para responder. Prueba consultarlo de otra manera'. "
              "Answer in Spanish all the questions \n")
    return header + context + "\n\n" + query + "\n"

def generate_answer(context, query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides answers in Spanish about Chilean subsidized private schools."},
        {"role": "user", "content": context},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::88asXE7W",
        messages=messages
    )

    return response.choices[0].message['content'].strip()

def query_refiner(conversation, query):
    messages = [
        {"role": "system", "content": "Your role is to refine the user's query to be clearer and more specific, especially concerning Chilean subsidized private schools. Do not answer the query, just refine it. All refined queries must be in spanish language"},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::88asXE7W",
        messages=messages
    )

    return response.choices[0].message['content'].strip()



