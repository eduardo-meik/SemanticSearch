#vector_search.py
import streamlit as st
import pinecone
import openai

# Access secrets from secrets.toml using st.secrets
pinecone_api_key = st.secrets["pinecone"]["api_key"]
pinecone_environment = st.secrets["pinecone"]["environment"]
index_name = st.secrets["pinecone"]["index_name"]

# Initialize OpenAI client with the API key
openai.api_key = st.secrets["openai"]["api_key"]

def get_openai_embedding(text):
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    return response["data"][0]["embedding"]

pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment) 
index = pinecone.Index(index_name)

def addData(corpusData, url):
    id = index.describe_index_stats()['total_vector_count']
    for i in range(len(corpusData)):
        chunk = corpusData[i]
        chunkInfo = (
            str(id+i),
            get_openai_embedding(chunk),  # Use the new embedding function
            {'title': url, 'link': '<LINK_GOES_HERE>', 'context': chunk} # assuming <LINK_GOES_HERE> is replaced with the actual link
        )
        index.upsert(vectors=[chunkInfo])


def find_match(query, k):
    query_em = get_openai_embedding(query)  # Use the new embedding function
    result = index.query(query_em, top_k=k, includeMetadata=True)
    
    urls = [result['matches'][i]['metadata']['title'] for i in range(k)]  # changed from 'source' to 'title'
    links = [result['matches'][i]['metadata']['link'] for i in range(k)]
    contexts = [result['matches'][i]['metadata']['context'] for i in range(k)]
    scores = [result['matches'][i]['score'] for i in range(k)]  # Collect similarity scores
    
    return urls, links, contexts, scores

