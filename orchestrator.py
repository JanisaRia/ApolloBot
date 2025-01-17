"""orchestrator.py - Manages chatbot execution logic."""

import faiss
import numpy as mp
from chatbot import extract_text_from_pdf, split_into_sentences, generate_embeddings, create_faiss_index, search_faiss_index, get_chatbot_response
from constants import FAISS_TOP_K

class ChatbotOrchestrator:
    """
    Manages document processing and chatbot query execution.
    
    Attributes:
        embedding_method (str): Chosen embedding model ("sentence_transformer" or "openai_ada").
        index (faiss.IndexFlatIP or None): FAISS index for search (None if uninitialised).
        sentences (list[str]): List of extracted document sentences.
    """
    
    def __init__(self, embedding_method="openai_ada"):
        """
        Initialises the orchestrator with the chosen embedding method.
        
        Args:
            embedding_method(str): "sentence_transformer" or "openai_ada".
        """
        self.embedding_method = embedding_method
        self.index = None
        self.sentences = []
     
    def process_pdf(self, pdf_file):
        """
        Extracts text from a PDF and processes it into FAISS embedding.
        
        Args:
            pdf_file(BytesIO): The uploaded PDF file.
            
        Returns:
            bool: True if processing was successful, False otherwise.
        """
        try:
            #Extract text
            text = extract_text_from_pdf(pdf_file)
            
            # Split into sentences
            self.sentences = split_into_sentences(text)
            
            # Generate embeddings
            embeddings = generate_embeddings(self.sentences, method=self.embedding_method)
            
            #Create FAISS index
            self.index = create_faiss_index(embeddings)
            
            return True
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False

    def handle_query(self, query):
        """
        Handles user queries by retrieving relevant document matches and generating a response.

        Args:
            query (str): The user's question.

        Returns:
            str: The AI-generated response based on retrieved document context.
        """
        if not self.index or not self.sentences:
            return "Please upload and process a PDF first."

        try:
            query_embedding = generate_embeddings([query], method=self.embedding_method)

            # Ensure FAISS search returns only sentences (not tuples)
            relevant_sentences = search_faiss_index(self.index, query_embedding, self.sentences)

            # Ensure relevant_sentences contains only strings
            relevant_sentences = [str(sent) for sent in relevant_sentences]

            # Format context correctly
            context = "\n".join(relevant_sentences)

            print(f"🔎 Retrieved Context: {context}")  # Debug log

            # Call GPT
            response = get_chatbot_response(query, context)
            return response
        except Exception as e:
            return f"Error handling query: {e}"
        
    def recompute_embeddings(self):
        """
        Recomputes embeddings for the uploaded document based on the current embedding method.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if not self.sentences:
                raise ValueError("No document has been processed yet.")

            # Generate new embeddings
            embeddings = generate_embeddings(self.sentences, method=self.embedding_method)

            # Update the FAISS index
            self.index = create_faiss_index(embeddings)

            return True
        except Exception as e:
            print(f"Error recomputing embeddings: {e}")
            return False