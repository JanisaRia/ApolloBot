"""interface.py - ApolloBot - The Strict, High-End Banking AI Assistant"""

import streamlit as st
from orchestrator import ChatbotOrchestrator

# Page Configuration
st.set_page_config(
    page_title="ApolloBot 🤖",
    page_icon="🏦",
    layout="wide",
)

# Custom Styles
st.markdown(
    """
    <style>
        body {
            background-color: #F5F7FA !important;
            color: #2C3E50 !important;
        }
        .title {
            font-size: 38px !important;
            font-weight: bold !important;
            color: #D4AF37 !important;
            text-align: center;
            margin-bottom: 10px;
        }
        .tagline {
            font-size: 20px !important;
            color: #2C3E50 !important;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton > button {
            background-color: #2C3E50 !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 6px !important;
            padding: 12px !important;
        }
        .stButton > button:hover {
            background-color: #D4AF37 !important;
        }
        .chatbox {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-left: 6px solid #D4AF37;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Bank Logo and Main Title
st.markdown('<p class="title">ApolloBot 🤖 - Elite Banking AI</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Your 24/7 Money Ally, Just One Chat Away.</p>', unsafe_allow_html=True)

# Session State Setup
if "embedding_done" not in st.session_state:
    st.session_state.embedding_done = False
if "embedding_method" not in st.session_state:
    st.session_state.embedding_method = "sentence_transformer"
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = ChatbotOrchestrator()

# File Upload
uploaded_file = st.file_uploader("📂 Upload Official Bank Policies (PDF)", type=["pdf"])

if uploaded_file:
    st.success("✅ Official document uploaded successfully.")

    # Embedding Options
    st.markdown("### ⚙️ Choose an Embedding Method:")
    selected_method = st.radio(
        "Select embedding method:",
        options=("Sentence Transformer", "OpenAI Ada"),
        index=0 if st.session_state.embedding_method == "sentence_transformer" else 1,
    )

    # Detect if embedding method is changed
    method_changed = (
        selected_method == "OpenAI Ada"
        and st.session_state.embedding_method != "openai_ada"
    ) or (
        selected_method == "Sentence Transformer"
        and st.session_state.embedding_method != "sentence_transformer"
    )

    # Process Document Button
    if not st.session_state.embedding_done:
        if st.button("📂 Process Document"):
            with st.spinner("🔄 Processing document... Please wait."):
                try:
                    # Update embedding method in session state
                    st.session_state.embedding_method = (
                        "openai_ada"
                        if selected_method == "OpenAI Ada"
                        else "sentence_transformer"
                    )
                    orchestrator = st.session_state.orchestrator
                    success = orchestrator.process_pdf(uploaded_file)
                    if success:
                        st.session_state.embedding_done = True
                        st.success("✅ Document processed successfully. ApolloBot is ready!")
                    else:
                        st.error("❌ Document processing failed. Please check the file.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # Reprocess Document Button (Only appears if the method has changed)
    if st.session_state.embedding_done and method_changed:
        if st.button("📂 Reprocess Document with New Embedding Method"):
            with st.spinner("🔄 Recomputing embeddings... Please wait."):
                try:
                    # Update embedding method
                    st.session_state.embedding_method = (
                        "openai_ada"
                        if selected_method == "OpenAI Ada"
                        else "sentence_transformer"
                    )
                    orchestrator = st.session_state.orchestrator
                    success = orchestrator.recompute_embeddings()
                    if success:
                        st.session_state.embedding_done = True
                        st.success("✅ Reprocessing completed successfully!")
                    else:
                        st.error("❌ Reprocessing failed. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Query Input
query = st.text_input("💬 Ask ApolloBot:", label_visibility="hidden")

# Query Button
if st.button("🚀 Ask ApolloBot"):
    if not st.session_state.embedding_done:
        st.error("❌ Please process the official document first.")
    elif not query.strip():
        st.warning("⚠️ Query cannot be empty.")
    else:
        with st.spinner("🤖 Fetching response... Please wait."):
            try:
                orchestrator = st.session_state.orchestrator
                response = orchestrator.handle_query(query)
                st.markdown("### 🤖 ApolloBot:")
                st.markdown(
                    f"""
                    <div class="chatbox">
                        <p style="font-size:18px;">{response}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
