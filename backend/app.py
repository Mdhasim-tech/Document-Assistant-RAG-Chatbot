from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
from datetime import datetime, timezone


from ingest import (
    load_documents,
    chunking,
    makeVectors_storeDB,
    generate_pdf_summary,

)

from database import (
    chats_collection,
)

from chat_service import (
    save_message,
    get_chat_history,
    get_all_chats,
    delete_chat,
    rename_chat,
    get_chat_summary,
)

from rag_pipeline import (
    load_vectorDB,
    build_retriever,
    build_llm,
    build_prompt,
    load_pdf_summary,

)

from status_service import (
    update_status,
    get_status,
)

from storage_service import (
    save_pdf_to_gridfs,
    download_pdf_from_gridfs,
    delete_temp_file,
)

app = Flask(__name__)
CORS(app)


# Load LLM once
llm = build_llm()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is running"})


@app.route("/status/<chat_id>", methods=["GET"])
def chat_status(chat_id):

    return jsonify({"status": get_status(chat_id)})


@app.route("/upload", methods=["POST"])
def upload_pdf():

    chat_id = request.form.get("chatId")

    if not chat_id:
        return jsonify({"error": "chatId is required"}), 400

    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    temp_pdf_path = None

    try:

        update_status(chat_id, "Uploading PDF...")

        # Save PDF to GridFS
        pdf_file_id = save_pdf_to_gridfs(file)

        # Download it temporarily for PyMuPDF
        temp_pdf_path = download_pdf_from_gridfs(pdf_file_id)

        update_status(chat_id, "Loading PDF...")

        docs = load_documents(temp_pdf_path)

        update_status(chat_id, "Chunking document...")

        chunks = chunking(docs)

        update_status(chat_id, "Creating Vector DB...")

        makeVectors_storeDB(chunks, chat_id)

        update_status(chat_id, "Generating Summary...")

        generate_pdf_summary(docs, chat_id)

        summary = load_pdf_summary(chat_id)

        chats_collection.update_one(
            {"chatId": chat_id},
            {
                "$set": {
                    "chatId": chat_id,
                    "title": file.filename,
                    "pdfName": file.filename,
                    "pdfFileId": pdf_file_id,
                    "uploadedAt": datetime.now(timezone.utc),
                    "status": "Ready",
                }
            },
            upsert=True,
        )

        update_status(chat_id, "Ready")

        return jsonify(
            {
                "message": "PDF processed successfully",
                "summary": summary,
                "chatId": chat_id,
                "pdfName": file.filename,
            }
        )

    except Exception as e:

        traceback.print_exc()

        update_status(chat_id, "Failed")

        return jsonify({"error": str(e)}), 500

    finally:

        if temp_pdf_path:
            delete_temp_file(temp_pdf_path)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question")
    chat_id = data.get("chatId")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    if not chat_id:
        return jsonify({"error": "chatId is required"}), 400

    try:

        save_message(chat_id, "user", question)

        vectorstore = load_vectorDB()

        retriever = build_retriever(
            vectorstore,
            chat_id
        )

        pdf_summary = load_pdf_summary(chat_id)

        prompt = build_prompt(pdf_summary)

        docs = retriever.invoke(question)

        context = "\n\n".join(doc.page_content for doc in docs)

        formatted_prompt = prompt.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = llm.invoke(formatted_prompt)

        save_message(
            chat_id,
            "assistant",
            response.content,
        )

        return jsonify(
            {
                "answer": response.content,
                "chatId": chat_id,
            }
        )

    except Exception as e:

        traceback.print_exc()

        return jsonify({"error": str(e)}), 500


@app.route("/chat/<chat_id>", methods=["GET"])
def get_chat(chat_id):

    history = get_chat_history(chat_id)

    return jsonify(history)


@app.route("/chat/<chat_id>", methods=["DELETE"])
def delete_chat_route(chat_id):

    try:

        delete_chat(chat_id)

        return jsonify({"message": "Chat deleted successfully"})

    except Exception as e:

        traceback.print_exc()

        return jsonify({"error": str(e)}), 500


@app.route("/chat/<chat_id>/rename", methods=["PATCH"])
def rename_chat_route(chat_id):

    try:

        data = request.get_json()

        title = data.get("title")

        if not title:

            return jsonify({"error": "Title required"}), 400

        rename_chat(chat_id, title)

        return jsonify({"message": "Renamed successfully"})

    except Exception as e:

        traceback.print_exc()

        return jsonify({"error": str(e)}), 500


@app.route("/chats", methods=["GET"])
def get_chats():

    chats = get_all_chats()

    return jsonify(chats)


@app.route("/summary/<chat_id>", methods=["GET"])
def get_summary(chat_id):

    summary = get_chat_summary(chat_id)

    return jsonify({"summary": summary})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )
