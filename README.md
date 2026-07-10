# 📄 Document Assistant RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents and ask natural language questions about their contents. The application retrieves relevant information from uploaded documents using vector search and generates accurate, context-aware responses using Groq LLM.

---

## 🚀 Features

- 📄 Upload PDF and text documents
- 🤖 AI-powered question answering
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Vector embeddings with ChromaDB
- 💬 Interactive chat interface
- 📚 Context-aware responses
- ⚡ Fast document retrieval using LangChain
- 📱 Responsive React frontend

---

## 🛠️ Tech Stack

### Frontend
- React
- Axios
- CSS
- React Hooks

### Backend
- Python
- Flask
- LangChain
- ChromaDB
- Groq API
- Sentence Transformers
- PyPDF

---

## 📂 Project Structure

```
Document-Assistant-RAG-Chatbot/
│
├── backend/
│   ├── chroma_langchain_db/
│   ├── data/
│   ├── uploads/
│   ├── summaries/
│   ├── app.py
│   ├── ingest.py
│   ├── rag_pipeline.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mdhasim-tech/Document-Assistant-RAG-Chatbot.git
cd Document-Assistant-RAG-Chatbot
```

---

### 2. Backend Setup

```bash
cd backend

pip install -r requirements.txt

python app.py
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install

npm start
```

---

## 🔐 Environment Variables

Create a `.env` file inside the backend folder.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 🏗️ How It Works

1. User uploads a document.
2. The document is split into smaller chunks.
3. Embeddings are generated for each chunk.
4. Chunks are stored in ChromaDB.
5. User asks a question.
6. Relevant document chunks are retrieved using vector search.
7. Groq LLM generates an answer using the retrieved context.
8. The response is displayed in the chat interface.

---

## 📌 Future Improvements

- Multiple document support
- Conversation history
- Authentication
- Source citation highlighting
- Streaming AI responses
- Drag-and-drop document upload
- Dark mode
- Support for DOCX and PPT files

---

## 👨‍💻 Author

**Md Hasim**

GitHub: https://github.com/Mdhasim-tech
