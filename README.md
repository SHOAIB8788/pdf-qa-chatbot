# 📄 PDF Q&A Chatbot

Upload a PDF, ask questions about it, get answers straight from the document. Built this as a hands-on way to learn how LLM apps actually work under the hood — not just calling an API, but combining it with search so the AI only answers from your file, not random guesses.

## How it works

The PDF gets split into small chunks, and each chunk is turned into a vector (basically a number that represents its meaning). When you ask something, the app finds the chunks most related to your question and hands those to the LLM, which then answers based only on that content. This pattern is called RAG (Retrieval-Augmented Generation), and it's how most real-world document AI tools work.

## Features

- Upload any PDF and ask questions about it in plain English
- Answers are grounded in your document, not the model's general knowledge
- Sidebar shows your recent questions during the session
- Basic name-based login to separate chat histories while you're using the app (see note below)
- Clean, simple interface

## A note on the login

The "login" just asks for a name to keep chat histories separate while you're using the app — it's not real authentication. There's no password, no database, nothing saved permanently. Close the tab or restart the app, and the history is gone. Good enough for a demo, not for a real product. Adding real accounts and persistent history is on the list below.

## Tech stack

- **Streamlit** – the web interface
- **LangChain** – ties the PDF, search, and LLM together
- **Groq API** – runs the LLM (fast and free)
- **FAISS** – searches the document chunks
- **HuggingFace embeddings** – turns text into searchable vectors
- **PyPDF** – reads text out of the PDF

## Running it locally

```bash
git clone https://github.com/SHOAIB8788/pdf-qa-chatbot.git
cd pdf-qa-chatbot

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Get a free API key from [Groq](https://console.groq.com), then create a `.env` file in the project folder with:
```
GROQ_API_KEY=your_key_here
```

Run it:
```bash
streamlit run app.py
```

It'll open at `http://localhost:8501`.

## What's next

- Real per-user accounts and permanent chat history (would need a proper login system + a database like SQLite)
- Support for multiple PDFs at once
- Option to export chat history

## Author

Muhammad Shoaib Ubaid — BS Artificial Intelligence, Islamia University Bahawalpur