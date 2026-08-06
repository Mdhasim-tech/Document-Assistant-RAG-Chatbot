# 📄 DocMind AI (RAG Chatbot)

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and chat with them using natural language.

The application automatically summarizes uploaded documents, stores them securely in the cloud, indexes their contents as vector embeddings, and answers questions using an LLM with context-aware retrieval.

---

## 🚀 Features

- 📂 Upload PDF documents
- 🤖 AI-generated document summary
- 💬 Chat with your documents
- 🔍 Semantic search using embeddings
- 🧠 Retrieval-Augmented Generation (RAG)
- ☁️ Cloud Vector Database (Qdrant Cloud)
- ☁️ Cloud PDF Storage (MongoDB GridFS)
- 📝 Multiple chat sessions
- ✏️ Rename chats
- 🗑 Delete chats
- ⚡ Fast similarity search
- 🎯 Context-aware answers using retrieved chunks

---

# 🏗 Architecture

```
React Frontend
       │
       ▼
 Flask Backend
       │
 ├──────────────► MongoDB Atlas
 │                 ├── Chats
 │                 ├── Messages
 │                 ├── Summaries
 │                 └── GridFS (PDF Storage)
 │
 ├──────────────► Qdrant Cloud
 │                 └── Vector Embeddings
 │
 └──────────────► Groq Llama 3.3
```

---

# 🛠 Tech Stack

### Frontend

- React
- CSS
- Axios

### Backend

- Flask
- LangChain
- PyMuPDF
- Sentence Transformers
- HuggingFace Embeddings

### AI

- Groq (Llama 3.3 70B)
- LangChain RAG Pipeline

### Database

- MongoDB Atlas
- GridFS
- Qdrant Cloud

---

# 📂 Project Structure

```
DocMind AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app.py
│   ├── ingest.py
│   ├── rag_pipeline.py
│   ├── database.py
│   ├── storage_service.py
│   ├── chat_service.py
│   ├── status_service.py
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

# ⚙️ How it Works

## 1. Upload PDF

- User uploads a PDF.
- PDF is stored in MongoDB GridFS.
- Metadata is stored in MongoDB.

## 2. Document Processing

- Extract text using PyMuPDF.
- Split document into chunks.
- Generate embeddings.
- Store vectors in Qdrant Cloud.
- Generate an AI summary.

## 3. Chat

When a user asks a question:

- Relevant chunks are retrieved from Qdrant.
- Retrieved context is combined with the document summary.
- Groq Llama 3.3 generates the final answer.

---

# 🧠 AI Workflow

```
PDF
 │
 ▼
PyMuPDF
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
Qdrant Cloud
 │
 ▼
Retriever
 │
 ▼
Groq Llama 3.3
 │
 ▼
Answer
```

---

# 📦 Environment Variables

Create a `.env` file inside the backend folder.

```env
MONGO_URI=YOUR_MONGODB_URI

GROQ_API_KEY=YOUR_GROQ_API_KEY

QDRANT_URL=YOUR_QDRANT_CLUSTER_URL

QDRANT_API_KEY=YOUR_QDRANT_API_KEY
```

---

# ▶️ Running the Project

## Backend

```bash
cd backend

pip install -r requirements.txt

python app.py
```

---

## Frontend

```bash
cd frontend

npm install

npm start
```

---

# 📸 Screenshots

<img width="1358" height="680" alt="rag1" src="https://github.com/user-attachments/assets/61a0c45e-d701-420c-ad8e-f79d65530a88" />
<img width="1364" height="633" alt="rag4" src="https://github.com/user-attachments/assets/10caf103-4abb-4ebd-8b11-29f05c88a00d" />
<img width="1356" height="638" alt="rag3" src="https://github.com/user-attachments/assets/aea434de-a90e-4def-815c-ecd8430b8639" />
<img width="1358" height="646" alt="rag2" src="https://github.com/user-attachments/assets/7aa5e480-2ee1-4bdc-ac78-927e94b8db87" />

---

# Future Improvements

- Authentication
- Streaming AI responses
- Image understanding inside PDFs
- Citation support
- OCR for scanned documents
- Conversation export
- Multiple document chat
- Hybrid Search (Dense + BM25)

---

# Author

**Md Hasim**

- GitHub: https://github.com/Mdhasim-tech
- LinkedIn: https://www.linkedin.com/in/md-hasim-tech/

---

If you found this project useful, consider giving it a ⭐ on GitHub.
