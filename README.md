# 📄 PDF Q&A Chatbot

An AI-powered chatbot that lets you upload any PDF document and ask questions about it in plain English. The chatbot reads your document, understands its content, and answers your questions using only the information found inside — powered by a large language model (LLM).

## 🎯 What This Project Does

Instead of manually searching through long PDF files, this app lets you:
1. Upload any PDF (reports, notes, resumes, research papers, etc.)
2. Ask questions in natural language
3. Get instant, accurate answers pulled directly from the document
4. See your past questions saved in a sidebar, just like a chat history

## ✨ Features

- **📤 PDF Upload** — Upload any PDF file directly through the browser
- **🤖 AI-Powered Answers** — Uses a free, fast LLM (via Groq API) to understand and answer questions
- **🔍 Smart Search** — Breaks the PDF into chunks and finds the most relevant parts before answering (Retrieval-Augmented Generation / RAG)
- **🕘 Chat History** — See your recent questions in a sidebar
- **🔐 Simple Login** — Each user gets their own separate chat history
- **🎨 Clean, Professional UI** — Custom-styled interface for a polished look

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web app framework (UI) |
| LangChain | Connects the PDF, search, and AI model together |
| Groq API | Fast, free LLM for generating answers |
| FAISS | Vector database for searching document chunks |
| HuggingFace Embeddings | Converts text into searchable "meaning" vectors |
| PyPDF | Reads and extracts text from PDF files |

## 🧠 How It Works

1. The uploaded PDF is split into small text chunks
2. Each chunk is converted into a numerical representation (embedding) that captures its meaning
3. These embeddings are stored in a searchable vector database (FAISS)
4. When you ask a question, the app finds the most relevant chunks from the PDF
5. Those chunks + your question are sent to the LLM, which generates an answer based only on that content

This approach is called **RAG (Retrieval-Augmented Generation)** — a common real-world pattern used in modern AI applications.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/SHOAIB8788/pdf-qa-chatbot.git
cd pdf-qa-chatbot

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Set up your API key

Set your Groq API key as an environment variable:
```bash
setx GROQ_API_KEY "your_key_here"      # Windows
export GROQ_API_KEY="your_key_here"    # Mac/Linux
```

### Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📸 How to Use

1. Log in with any username
2. Upload a PDF file
3. Wait a few seconds while it's processed
4. Type your question in the chat box
5. View your past questions anytime in the sidebar

## 🔮 Future Improvements

- Persistent chat history (saved even after closing the browser)
- Support for multiple PDFs at once
- Real authentication with passwords
- Export chat history as a file

## 👤 Author

**Muhammad Shoaib Ubaid**
BS Artificial Intelligence, Islamia University Bahawalpur

## 📝 License

This project is open source and available for learning purposes.