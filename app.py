import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "PASTE_YOUR_KEY_HERE")

st.title("📄 PDF Q&A Chatbot")
st.markdown("""
<style>
/* Overall app background */
.stApp {
    background-color: #FFFFFF;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1E3A5F;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Page title */
h1 {
    color: #1E3A5F !important;
}

/* Subheaders */
h2, h3 {
    color: #1E3A5F !important;
}

/* File uploader box */
[data-testid="stFileUploaderDropzone"] {
    background-color: #FFFFFF;
    border: 2px dashed #2A9D8F;
    border-radius: 10px;
}
[data-testid="stFileUploaderDropzone"] * {
    color: #1E3A5F !important;
}

/* Chat input box */
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #1E3A5F !important;
    border-radius: 8px !important;
    border: 2px solid #2A9D8F !important;
}

/* Text input (login box) */
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #1E3A5F !important;
    border: 2px solid #2A9D8F !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton button {
    background-color: #2A9D8F !important;
    color: #FFFFFF !important;
    font-weight: bold;
    border-radius: 8px !important;
    border: none !important;
}
.stButton button:hover {
    background-color: #1E3A5F !important;
}

/* Chat message bubbles */
[data-testid="stChatMessage"] {
    background-color: #F1F5F9;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    border: 1px solid #2A9D8F;
}
[data-testid="stChatMessage"] p {
    color: #1E3A5F !important;
}
</style>
""", unsafe_allow_html=True)
# ---- Step 1: Simple Login ----
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    st.subheader("🔐 Login")
    name_input = st.text_input("Enter your name to continue")
    if st.button("Login"):
        if name_input.strip() != "":
            st.session_state.username = name_input.strip()
            st.rerun()
        else:
            st.warning("Please enter a name.")
    st.stop()  # Stops the rest of the app from loading until logged in

# ---- Step 2: Set up per-user chat history ----
if "all_users_messages" not in st.session_state:
    st.session_state.all_users_messages = {}

username = st.session_state.username
if username not in st.session_state.all_users_messages:
    st.session_state.all_users_messages[username] = []

# Shortcut: this user's own messages
user_messages = st.session_state.all_users_messages[username]

# ---- Sidebar ----
with st.sidebar:
    st.write(f"👤 Logged in as: **{username}**")
    if st.button("Logout"):
        st.session_state.username = None
        st.rerun()

    st.header("🕘 Recent Questions")
    if len(user_messages) > 0:
        past_questions = [m["content"] for m in user_messages if m["role"] == "user"]
        for i, q in enumerate(reversed(past_questions), 1):
            st.write(f"{i}. {q}")
    else:
        st.write("No questions yet.")

    if st.button("🗑️ Clear History"):
        st.session_state.all_users_messages[username] = []
        st.rerun()

# ---- File upload ----
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    @st.cache_resource
    def load_pdf_and_build_search(file_name):
        loader = PyPDFLoader("temp_uploaded.pdf")
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(pages)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embeddings)
        return vector_db

    with st.spinner("Reading your PDF..."):
        vector_db = load_pdf_and_build_search(uploaded_file.name)

    st.success("PDF loaded! Ask me anything about it.")

    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile")

    for msg in user_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_question = st.chat_input("Ask a question about your PDF...")

    if user_question:
        user_messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        relevant_chunks = vector_db.similarity_search(user_question, k=3)
        context_text = "\n\n".join([doc.page_content for doc in relevant_chunks])

        prompt = f"""Answer the question using ONLY the information below from the PDF.
If the answer isn't in the PDF, say "I couldn't find that in the document."

PDF Content:
{context_text}

Question: {user_question}
"""
        response = llm.invoke(prompt)
        answer = response.content

        user_messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

else:
    st.info("👆 Upload a PDF to get started.")