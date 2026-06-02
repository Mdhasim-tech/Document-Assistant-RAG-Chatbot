from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os
import json

load_dotenv()


def load_documents(pdf_path):

    loader = PyMuPDFLoader(pdf_path)

    doc = loader.load()

    return doc


def is_useful_chunk(
    text: str,
    min_length: int = 200
) -> bool:

    lines = text.strip().split('\n')

    non_empty_lines = [
        l for l in lines if l.strip()
    ]

    if len(text.strip()) < min_length:

        return False

    short_lines = [
        l for l in non_empty_lines
        if len(l.strip()) < 60
    ]

    if (
        len(non_empty_lines) > 0 and
        (len(short_lines) / len(non_empty_lines)) > 0.75
    ):

        return False

    return True


def chunking(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    filtered_chunks = [

        doc for doc in chunks

        if is_useful_chunk(doc.page_content)
    ]

    print(
        "-------------------Chunking has been done!----------------------------------"
    )

    return filtered_chunks


def generate_pdf_summary(pages, chat_id):

    intro_text = " ".join([
        p.page_content for p in pages[:3]
    ])[:3000]

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=300,
        api_key=os.getenv("GROQ_API_KEY")
    )

    summary_prompt = f"""
    Read the following text from the beginning of a document and answer in 3-4 sentences:

    - What is this document about?
    - What are the main topics it covers?

    Text:
    {intro_text}

    Summary:
    """

    response = llm.invoke(summary_prompt)

    summary = response.content.strip()

    # create summaries folder
    os.makedirs("summaries", exist_ok=True)

    summary_path = f"summaries/{chat_id}.json"

    # save summary
    with open(summary_path, "w") as f:

        json.dump({
            "summary": summary
        }, f)

    print(f"PDF Summary generated:\n{summary}")

    return summary


def makeVectors_storeDB(chunks, chat_id):

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    persist_path = f"chroma_langchain_db/{chat_id}"

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_path
    )

    print(f"Vector DB created for chat: {chat_id}")

    return vectorstore