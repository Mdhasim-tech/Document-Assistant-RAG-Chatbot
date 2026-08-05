from datetime import datetime, timezone
import os

from database import (
    messages_collection,
    chats_collection,
    summaries_collection,
)
from storage_service import delete_pdf_from_gridfs

from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)


def save_message(chat_id, role, content):
    messages_collection.insert_one(
        {
            "chatId": chat_id,
            "role": role,
            "content": content,
            "createdAt": datetime.now(timezone.utc),
        }
    )


def get_chat_history(chat_id):
    return list(
        messages_collection.find(
            {"chatId": chat_id},
            {"_id": 0},
        ).sort("createdAt", 1)
    )


def get_all_chats():

    chats = list(
        chats_collection.find(
            {},
            {"_id": 0},
        ).sort("uploadedAt", -1)
    )

    for chat in chats:

        summary = summaries_collection.find_one(
            {"chatId": chat["chatId"]},
            {"_id": 0, "summary": 1},
        )

        chat["summary"] = summary["summary"] if summary else ""

    return chats


def delete_chat(chat_id):

    # ---------------- Delete PDF ----------------
    chat = chats_collection.find_one({"chatId": chat_id})

    if chat and "pdfFileId" in chat:
        delete_pdf_from_gridfs(chat["pdfFileId"])

    # ---------------- Delete vectors from Qdrant ----------------
    client.delete(
        collection_name="documents",
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.chatId",
                    match=MatchValue(value=chat_id),
                )
            ]
        ),
    )

    # ---------------- Delete MongoDB data ----------------
    messages_collection.delete_many({"chatId": chat_id})

    summaries_collection.delete_one({"chatId": chat_id})

    chats_collection.delete_one({"chatId": chat_id})

    print(f"Deleted chat {chat_id} completely.")


def rename_chat(chat_id, title):

    chats_collection.update_one(
        {"chatId": chat_id},
        {"$set": {"title": title}},
    )

    return True


def get_chat_summary(chat_id):

    summary = summaries_collection.find_one(
        {"chatId": chat_id},
        {"_id": 0, "summary": 1},
    )

    if summary:
        return summary["summary"]

    return ""
