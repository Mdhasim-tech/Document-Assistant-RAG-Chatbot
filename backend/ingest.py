from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PayloadSchemaType,
)
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from database import summaries_collection
from datetime import datetime, timezone
import os
load_dotenv()

# Global embedding model (loaded once)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
summary_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=300,
    api_key=os.getenv("GROQ_API_KEY"),
)
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
# ---------- Create collection if it doesn't exist ----------
# ---------- Create collection if it doesn't exist ----------

if not client.collection_exists("documents"):

    client.create_collection(
        collection_name="documents",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )

# ---------- Create payload index if missing ----------

try:

    client.create_payload_index(
        collection_name="documents",
        field_name="metadata.chatId",
        field_schema=PayloadSchemaType.KEYWORD,
    )

except Exception:
    pass
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
def load_documents(pdf_path):

    loader = PyMuPDFLoader(pdf_path)

    doc = loader.load()

    return doc


def chunking(documents):

    chunks = text_splitter.split_documents(documents)

    print(f"Generated {len(chunks)} chunks")

    return chunks


def generate_pdf_summary(pages, chat_id):

    intro_text = " ".join([
        p.page_content for p in pages[:3]
    ])[:3000]

    summary_prompt = f"""
    Read the following text from the beginning of a document and answer in 3-4 sentences:

    - What is this document about?
    - What are the main topics it covers?

    Text:
    {intro_text}

    Summary:
    """

    response = summary_llm.invoke(summary_prompt)

    summary = response.content.strip()

    # create summaries folder
    summaries_collection.update_one(
        {"chatId": chat_id},
        {
            "$set": {
                "chatId": chat_id,
                "summary": summary,
                "updatedAt": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )

    print(f"PDF Summary generated:\n{summary}")

    return summary


def makeVectors_storeDB(chunks, chat_id):

    if len(chunks) == 0:
        raise ValueError("No chunks were generated.")

    for chunk in chunks:
        chunk.metadata["chatId"] = chat_id

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="documents",
        embedding=embedding_model,
    )

    vectorstore.add_documents(chunks)

    print(f"Stored {len(chunks)} chunks for {chat_id}")

    return vectorstore
