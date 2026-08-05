from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from database import summaries_collection
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import os

load_dotenv()

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)


def load_vectorDB():

    return QdrantVectorStore(
        client=client,
        collection_name="documents",
        embedding=embedding_model,
    )


def load_pdf_summary(chat_id):

    doc = summaries_collection.find_one(
        {"chatId": chat_id},
        {"_id": 0, "summary": 1},
    )

    if doc:
        return doc["summary"]

    return "This is a document. No summary was generated during ingestion."


def build_retriever(vectorstore, chat_id):

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "filter": Filter(
                must=[
                    FieldCondition(
                        key="metadata.chatId",
                        match=MatchValue(value=chat_id),
                    )
                ]
            ),
        },
    )

    return retriever


def build_llm():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=1024,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    return llm


def build_prompt(pdf_summary):

    template = """
You are an intelligent AI assistant.

You are helping a user understand the contents of a specific document.

Document overview:
{pdf_summary}

Use the retrieved context below to answer the user's question.

Guidelines:

- If the user asks what the document is about, use the Document overview above
- Start with a clear direct answer
- Then elaborate using the retrieved context
- Use bullet points where useful
- Keep the answer concise but complete
- If context is insufficient, say so clearly

Context:
{context}

Question:
{question}

Answer:
"""

    return PromptTemplate.from_template(template.replace("{pdf_summary}", pdf_summary))
