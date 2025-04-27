# ApolloBot: Elite Banking AI Assistant

ApolloBot is an intelligent banking assistant that leverages natural language processing and semantic search to answer user questions based on official bank policy documents. This application uses a RAG (Retrieval-Augmented Generation) architecture to deliver accurate, context-aware responses based on the content of uploaded PDF documents.

## 🌟 Features

- **Document Processing**: Upload and process official bank policy PDFs
- **Semantic Search**: Find relevant document sections using advanced embedding techniques
- **Intelligent Responses**: Generate concise, accurate answers using OpenAI's language models
- **Choice of Embeddings**: Select between Sentence Transformer (local) or OpenAI Ada embeddings
- **Interactive UI**: Clean, professional interface built with Streamlit

## 🔧 Technology Stack

- **Frontend**: Streamlit
- **Backend**: Flask with CORS support
- **AI Models**:
  - OpenAI GPT models for response generation
  - Sentence Transformers or OpenAI Ada for document embeddings
- **Vector Database**: FAISS for efficient similarity search
- **Document Processing**: PyPDF2, spaCy, NLTK for text extraction and processing

## 📋 System Architecture

The system follows a RAG (Retrieval-Augmented Generation) architecture:

1. **Document Ingestion**: PDFs are uploaded and processed into sentences
2. **Embedding Generation**: Sentences are converted to vector embeddings
3. **Similarity Search**: User queries are matched against the document's sentences
4. **Response Generation**: Relevant sentences are used as context for GPT to generate responses

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/apollobot.git
   cd apollobot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```


## 🏃‍♂️ Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

The Flask server will automatically start the Streamlit application and redirect you to the UI.

## 📊 Usage

1. **Upload Document**: Use the file uploader to submit a bank policy PDF
2. **Choose Embedding Method**: Select between Sentence Transformer (local) or OpenAI Ada embeddings
3. **Process Document**: Click the "Process Document" button to analyze the PDF
4. **Ask Questions**: Type your query in the input field and click "Ask ApolloBot"

## 🔍 Component Details

### app.py
Flask application that manages the startup of the Streamlit interface and handles routing.

### interface.py
Streamlit-based user interface with styling and interactive elements.

### orchestrator.py
Manages the workflow between document processing, embedding generation, and query handling.

### chatbot.py
Core functionality for PDF text extraction, embedding generation, similarity search, and OpenAI API integration.

### constants.py (not included)
Configuration parameters for models, API keys, and system settings.

## ⚙️ Configuration Options

- **Embedding Methods**:
  - `sentence_transformer`: Local embedding generation (faster, no API costs)
  - `openai_ada`: OpenAI's Ada embeddings (potentially more accurate)

- **FAISS_TOP_K**: Number of most relevant sentences to retrieve (default: 5)
- **GPT_TEMPERATURE**: Controls randomness in responses (lower = more deterministic)
- **GPT_MAX_TOKENS**: Maximum length of generated responses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- OpenAI for GPT and embedding models
- Facebook Research for FAISS
- Hugging Face for Transformers and Sentence Transformers
- Streamlit team for the amazing UI framework
