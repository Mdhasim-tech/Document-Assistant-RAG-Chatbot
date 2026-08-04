from database import chats_collection


def update_status(chat_id, status):

    chats_collection.update_one(
        {"chatId": chat_id}, {"$set": {"status": status}}, upsert=True
    )


def get_status(chat_id):

    chat = chats_collection.find_one({"chatId": chat_id}, {"_id": 0, "status": 1})

    if chat:

        return chat.get("status", "Idle")

    return "Idle"
