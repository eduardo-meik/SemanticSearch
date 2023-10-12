import streamlit as st
import qa
from vector_search import find_match
from doclist import DOCLIST  # Import DOCLIST

st.markdown(
    """
    <style>
    input[type="text"] {
        border: 1px solid rgb(255, 75, 75);
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        # Try to retrieve title and link from DOCLIST using urls[max_score_index] as key
        file_info = DOCLIST.get(urls[max_score_index])
        if file_info:
            link = file_info["link"]
            title = file_info["title"]
            title_with_link = f'<a href="{link}" target="_blank">{title}</a>'
        else:
            title_with_link = urls[max_score_index]

        # Displaying title with link, highest scoring context, and its similarity score
        context_display = f"Fuente: {title_with_link}\n\n{res[max_score_index]}\n\n(Similarity: {scores[max_score_index]*100:.2f}%)"
        st.expander("Contexto").markdown(context_display, unsafe_allow_html=True)  # Using markdown for structured content

        # We'll use the highest scoring chunk as the context and the refined query as the query for the assistant
        context = res[max_score_index]
        answer = qa.generate_answer(context, refined_query)  # Adjusted call here
        st.success(f"Respuesta: {answer}")

        # Update conversation log (optional)
        conversation_log += f"User: {query}\nAssistant: {answer}\n"













            
            


       
