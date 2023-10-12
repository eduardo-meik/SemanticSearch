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
    refinement_prompt = (f"Given the conversation log and the user query, refine or rephrase the user's query to make it more specific to the knowledge base about Chilean subsidized private schools. "
                         f"Make sure the output is a refined version of the query and not an answer. "
                         f"\n\nCONVERSATION LOG: \n{conversation}\n\nUser Query: {query}\n\nRefined Query:")
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=refinement_prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text'].strip()



