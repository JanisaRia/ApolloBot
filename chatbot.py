"""chatbot.py - Handles embeddings, FAISS DB, and GPT-3.5-turbo calls."""

import openai
import faiss
import numpy as np
import PyPDF2
import spacy
from transformers import AutoTokenizer, AutoModel
import torch
from nltk.tokenize import sent_tokenize
from constants import (
    OPENAI_API_KEY,
    SENTENCE_TRANSFORMER_MODEL,
    OPENAI_ADA_MODEL,
    BATCH_SIZE,
    FAISS_TOP_K,
    GPT_MODEL,
    GPT_MAX_TOKENS,
    GPT_TEMPERATURE,
    CHATBOT_PROMPT
)

nlp = spacy.load("en_core_web_sm")

openai.api_key = OPENAI_API_KEY

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    
    Args:
        pdf_file (BytesIO): The uploaded PDF file.
    
    Returns:
        str: Extracted text from all pages of the PDF.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def split_into_sentences(text, method = "spacy"):
    """
    Splits text into sentences using either spaCy or NLTK.
    
    Args:
        text (str): The input text to split.
        method (str): The method to use for sentence segmentation. Options:
                      - "spacy": Uses spaCy for sentence segmentation.
                      - "nltk": Uses NLTK's `sent_tokenize` method.

    Returns:
        list[str]: List of extracted sentences.
    """
    if method == "spacy":
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences
    
    elif method == "nltk":
        sentences = sent_tokenize(text)
        return sentences
    
def generate_embeddings(sentences, method = "sentence_transformer"):
    """Generates embeddings using either Sentence Transformer or OpenAI Ada."""
    if method == "sentence_transformer":
        tokenizer = AutoTokenizer.from_pretrained(SENTENCE_TRANSFORMER_MODEL)
        model = AutoModel.from_pretrained(SENTENCE_TRANSFORMER_MODEL)
        embeddings = []
        for i in range(0, len(sentences), BATCH_SIZE):
            batch = sentences[i:i+BATCH_SIZE]
            inputs = tokenizer(batch, return_tensors="pt", truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = model(**inputs)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            embeddings.append(batch_embeddings)
        return np.vstack(embeddings)
    
    elif method == "openai_ada":
        client = openai.Client(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            model=OPENAI_ADA_MODEL,
            input=sentences
        )
        return np.array([embedding.embedding for embedding in response.data])

def normalize_vectors(vectors):
    """Normalizes vectors for cosine similarity."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms

def create_faiss_index(embeddings):
    """Creates a FAISS index for efficient similarity search.

    Args:
        embeddings (numpy.ndarray): A matrix where each row is an embedding.

    Returns:
        faiss.IndexFlatIP: A FAISS index for fast similarity search.
    """
    embeddings = normalize_vectors(embeddings)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index

def search_faiss_index(index, query_embedding, sentences):
    """Searches the FAISS index for the most relevant sentences.

    Args:
        index (faiss.IndexFlatIP): The FAISS index for searching.
        query_embedding (numpy.ndarray): The embedding of the query sentence.
        sentences (list[str]): The original sentences corresponding to embeddings.

    Returns:
        list[str]: The top-matching sentences from the FAISS search.
    """
    query_embedding = normalize_vectors(query_embedding)
    similarities, indices = index.search(query_embedding, k=FAISS_TOP_K)
    
    # Ensure we return only sentences, not tuples
    results = [sentences[indices[0][i]] for i in range(len(indices[0]))]  

    print(f"🔎 FAISS Search Results: {results}")  # Debug log
    return results  # Ensure only strings are returned

def get_chatbot_response(user_query, context):
    """Generates a chatbot response using GPT-3.5-Turbo.

    Args:
        user_query (str): The user's input query.
        context (str): The relevant retrieved text from the document.

    Returns:
        str: The chatbot's response generated by GPT-3.5-Turbo.
    """
    prompt = CHATBOT_PROMPT.format(user_query=user_query, doc_context = context)
    try:
        client = openai.Client(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": prompt}                
            ],
            max_tokens=GPT_MAX_TOKENS,
            temperature=GPT_TEMPERATURE  # Ensuring factual and structured responses
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {e}"
    
