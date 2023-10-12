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
        {"role": "system", "content": "You are a helpful assistant that provides answers in Spanish about Chilean subsidized private schools. Answer in Spanish all the questions"},
        {"role": "user", "content": context},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::88asXE7W",
        messages=messages,
        max_tokens=256,  # Limit response to 150 tokens, but you can adjust this as needed.
        temperature=0.7,  # A typical value; adjust for more or less randomness.
        frequency_penalty=0.0,  # No penalty for frequent tokens. Adjust as needed.
        presence_penalty=0.0,  # No penalty for new tokens. Adjust as needed.
        stop=["\n"],  # Stop when a newline character is encountered. Adjust as needed.
    )

    return response.choices[0].message['content'].strip()


def query_refiner(conversation, query):
    messages = [
        {"role": "system", "content": "Your role is to refine the user's query to be clearer and more specific, especially concerning Chilean subsidized private schools. Do not answer the query, just refine it. All refined queries must be in Spanish language."},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::88asXE7W",
        messages=messages,
        max_tokens=39,  # Limit response to 39 tokens
        temperature=0.5,
    )

    return response.choices[0].message['content'].strip()



