import openai
from langsmith import Client

# Initialize Langsmith client
client = Client()

def create_prompt(context, query):
    header = ("Answer the question as truthfully as possible using the provided context, and if the answer is not contained within "
              "the text and requires some latest information to be updated, print 'No tengo suficiente contexto para responder. Prueba consultarlo de otra manera', "
              "Answer in Spanish to all the questions \n")
    return header + context + "\n\n" + query + "\n"

def generate_answer(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[' END']
    )

    answer = response.choices[0].text.strip()
    
    # Store the prompt and response in Langsmith for traceability
    try:
        client.create_example(
            inputs={"question": prompt},
            outputs={"answer": answer},
            dataset_id=dataset.id,
        )
    except Exception as e:
        print(f"Error storing example in Langsmith: {e}")
        # Again, handle this exception more gracefully in production

    return answer

def query_refiner(conversation, query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base. All answers should be in the Spanish Language \n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text'].strip()

