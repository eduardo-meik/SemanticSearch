# qa.py
import openai

def create_prompt(context, query):
    header = ("Answer the question as truthfully as possible using the provided context, "
              "and if the answer is not contained within the text and requires some latest information to be updated, "
              "print 'No tengo suficiente contexto para responder. Prueba consultarlo de otra manera', "
              "Answer in Spanish all the questions \n")
    return header + context + "\n\n" + query + "\n"

def generate_answer(prompt):
    response = openai.Completion.create(
        model="ft:gpt-3.5-turbo-0613:personal::88asXE7W",  # updated model identifier
        prompt=prompt,
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[' END']
    )
    return response.choices[0].text.strip()

def query_refiner(conversation, query):
    response = openai.Completion.create(
        model="ft:gpt-3.5-turbo-0613:personal::88asXE7W",  # updated model identifier
        prompt=(f"Using the provided user query and conversation log, craft a relevant question for a knowledge base answer. "
                "All responses should be in Spanish and pertain only to Chilean subsidized private schools.  \n\n"
                f"CONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:"),
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text'].strip()

