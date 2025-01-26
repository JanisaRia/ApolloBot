"""constants.py - Stores reusable values"""

# OpenAI API Key (replace with env variables in production)
OPENAI_API_KEY = "your-openai-api-key"

# Embedding Model Names
SENTENCE_TRANSFORMER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OPENAI_ADA_MODEL = "text-embedding-ada-002"

#Batch size for generate embeddings
BATCH_SIZE = batch_size

# FAISS Index Parameters
FAISS_TOP_K = top_number  # Number of top results to retrieve

# Chatbot Model
GPT_MODEL = "gpt-model"
GPT_MAX_TOKENS = 250
GPT_TEMPERATURE = 0.2  # Lower value for factual responses

CHATBOT_PROMPT = """
            You are a banking assistant chatbot for Apollo Bank. 
            A user has this query:{user_query}.
            And below are some of the relevant pieces of information, from the bank documentation for this {doc_query{
            Consider the query and the info I have provided and give me a response that I can post as an answer to the user.
         """

STREAMLIT_URL = "streamlit-url"
