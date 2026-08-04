from datetime import datetime, timezone
from database import messages_collection
from database import chats_collection
import shutil
from database import summaries_collection
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from storage_service import delete_pdf_from_gridfs
from database import summaries_collection

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def save_message(chat_id, role, content):
    """
    Save one message in MongoDB.
    """

    messages_collection.insert_one(
        {
            "chatId": chat_id,
            "role": role,
            "content": content,
            "createdAt": datetime.now(timezone.utc),
        }
    )


def get_chat_history(chat_id):
    """
    Return all messages of a chat.
    """

    messages = list(
        messages_collection.find({"chatId": chat_id}, {"_id": 0}).sort("createdAt", 1)
    )

    return messages


def get_all_chats():

    chats = list(chats_collection.find({}, {"_id": 0}).sort("uploadedAt", -1))

    for chat in chats:

        summary = summaries_collection.find_one(
            {"chatId": chat["chatId"]}, {"_id": 0, "summary": 1}
        )

        chat["summary"] = summary["summary"] if summary else ""

    return chats


def delete_chat(chat_id):

    chat = chats_collection.find_one({"chatId": chat_id})

    if chat and "pdfFileId" in chat:
        delete_pdf_from_gridfs(chat["pdfFileId"])

    vectorstore = Chroma(
        persist_directory="chroma_langchain_db",
        embedding_function=embedding_model,
        collection_name="documents",
    )

    collection = vectorstore._collection

    results = collection.get(where={"chatId": chat_id}, include=[])

    ids = results["ids"]

    if ids:
        collection.delete(ids=ids)

    messages_collection.delete_many({"chatId": chat_id})

    summaries_collection.delete_one({"chatId": chat_id})

    chats_collection.delete_one({"chatId": chat_id})


def rename_chat(chat_id, title):
    """
    Rename a chat.
    """

    chats_collection.update_one({"chatId": chat_id}, {"$set": {"title": title}})

    return True


def get_chat_summary(chat_id):

    summary = summaries_collection.find_one(
        {"chatId": chat_id}, {"_id": 0, "summary": 1}
    )

    if summary:
        return summary["summary"]

    return ""
