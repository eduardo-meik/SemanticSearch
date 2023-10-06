# main.py
import streamlit as st
import qa
from vector_search import find_match
from langsmith import Client

# Langsmith client setup
client = Client()
dataset_name = "QnA Dataset"

try:
    dataset = client.create_dataset(
        dataset_name=dataset_name, description="User questions and system responses.",
    )
except Exception as e:
    print(f"Error creating dataset: {e}")
    # Here you'd ideally list all datasets, loop through them to find your dataset
    # and then get its ID or handle. 
    # For simplicity, I'm just printing the error. Adjust as per your needs.

def log_interaction_to_langsmith(user_query, system_response):
    client.create_example(
        inputs={"user_query": user_query},
        outputs={"system_response": system_response},
        dataset_id=dataset.id,
    )

# Begin Streamlit App
st.header("Asistente para Colegios Particulares Subvencionados en Chile")

# Define conversation log
conversation_log = ""  # Initialize with an empty log or pre-defined logs

# User input for the query
query = st.text_input("Haz tu Consulta", key="query_input_key")  # Assigning a unique key

if query:  # Check if the user entered a query
    # Get the matching chunks of text and their similarity scores using the find_match function
    urls, res, scores = find_match(query, 2)

    # Find the index of the highest score
    max_score_index = scores.index(max(scores))

    # Use the query refiner
    refined_query = qa.query_refiner(conversation_log, query)
    st.write(f"Consulta Refinada: {refined_query}")

    button = st.button("Enviar")

    if button and refined_query:
        # Displaying title (URL), highest scoring context, and its similarity score
        context_display = f"Fuente: {urls[max_score_index]}\n\n{res[max_score_index]}\n\n(Similarity: {scores[max_score_index]*100:.2f}%)"
        st.expander("Contexto").markdown(context_display)  # Using markdown for structured content

        prompt = qa.create_prompt(res[max_score_index], refined_query)  # Use the highest scoring chunk to create a prompt for the OpenAI model
        answer = qa.generate_answer(prompt)
        st.success(f"Respuesta: {answer}")

        # Log the interaction to Langsmith
        log_interaction_to_langsmith(query, answer, "QnA Dataset")

        # Update conversation log (optional)
        conversation_log += f"User: {query}\nAssistant: {answer}\n"








            
            


       
