# qa.py
import openai
import streamlit as st
from langsmith import Client

# Load the secrets
LANGCHAIN_TRACING_V2 = st.secrets["langsmith"]["LANGCHAIN_TRACING_V2"]
LANGCHAIN_ENDPOINT = st.secrets["langsmith"]["LANGCHAIN_ENDPOINT"]
LANGCHAIN_API_KEY = st.secrets["langsmith"]["LANGCHAIN_API_KEY"]
LANGCHAIN_PROJECT = st.secrets["langsmith"]["LANGCHAIN_PROJECT"]

# Initialize Langsmith client
client = Client(
    endpoint=LANGCHAIN_ENDPOINT,
    api_key=LANGCHAIN_API_KEY
)

def create_prompt(context, query):
    header = ("Answer the question as truthfully as possible using the provided context, "
              "and if the answer is not contained within the text and requires some latest "
              "information to be updated, print 'No tengo suficiente contexto para responder. "
              "Prueba consultarlo de otra manera', Answer in Spanish all the questions \n")
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

    # Log the response in Langsmith for traceability (if required)
    # You can adjust this part as per your needs.
    try:
        client.create_example(
            inputs={"question": prompt},
            outputs={"answer": answer},
            dataset_id="YOUR_DATASET_ID_HERE",  # replace with your dataset ID
        )
    except Exception as e:
        print(f"Error storing example in Langsmith: {e}")

    return answer

def query_refiner(conversation, query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given the following user query and conversation log, formulate a question that "
               f"would be the most relevant to provide the user with an answer from a knowledge base. "
               f"All answers should be in the Spanish Language \n\nCONVERSATION LOG: \n{conversation}\n\n"
               f"Query: {query}\n\nRefined Query:",
        temperature=0.1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text'].strip()



