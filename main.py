import streamlit as st
import qa
from vector_search import find_match

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
        context_display = f"Title: {urls[max_score_index]}\n\n{res[max_score_index]}\n\n(Similarity: {scores[max_score_index]*100:.2f}%)"
        st.expander("Contexto").markdown(context_display)  # Using markdown for structured content

        prompt = qa.create_prompt(res[max_score_index], refined_query)  # Use the highest scoring chunk to create a prompt for the OpenAI model
        answer = qa.generate_answer(prompt)
        st.success(f"Respuesta: {answer}")

        # Update conversation log (optional)
        conversation_log += f"User: {query}\nAssistant: {answer}\n"







            
            


       
