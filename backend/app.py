from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from ingest import (
    load_documents,
    chunking,
    makeVectors_storeDB,
    generate_pdf_summary
)

from rag_pipeline import (
    load_vectorDB,
    build_retriever,
    build_llm,
    build_prompt,
    load_pdf_summary
)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# global status
current_status = "Idle"

# load llm once
llm = build_llm()


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Server is running"
    })


@app.route("/status", methods=["GET"])
def get_status():

    return jsonify({
        "status": current_status
    })


@app.route("/upload", methods=["POST"])
def upload_pdf():

    global current_status

    # get chatId
    chat_id = request.form.get("chatId")

    if not chat_id:

        return jsonify({
            "error": "chatId is required"
        }), 400

    # check pdf exists
    if "pdf" not in request.files:

        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["pdf"]

    if file.filename == "":

        return jsonify({
            "error": "Empty filename"
        }), 400

    # create unique filename
    filename = f"{chat_id}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    # save file
    file.save(file_path)

    try:

        current_status = "Loading PDF..."
        print(current_status)

        docs = load_documents(file_path)

        current_status = "Chunking document..."
        print(current_status)

        chunks = chunking(docs)

        current_status = "Creating Vector DB..."
        print(current_status)

        # create vector db for this chat
        makeVectors_storeDB(chunks, chat_id)

        current_status = "Generating Summary..."
        print(current_status)

        # save summary for this chat
        generate_pdf_summary(docs, chat_id)

        current_status = "Ready to chat!"
        print(current_status)

        summary = load_pdf_summary(chat_id)

        return jsonify({
            "message": "PDF processed successfully",
            "summary": summary,
            "chatId": chat_id,
            "pdfName": file.filename
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question")
    chat_id = data.get("chatId")

    if not question:

        return jsonify({
            "error": "Question is required"
        }), 400

    if not chat_id:

        return jsonify({
            "error": "chatId is required"
        }), 400

    try:

        # load chat-specific vector db
        vectorstore = load_vectorDB(chat_id)

        retriever = build_retriever(vectorstore)

        # load chat-specific summary
        pdf_summary = load_pdf_summary(chat_id)

        prompt = build_prompt(pdf_summary)

        docs = retriever.invoke(question)

        context = "\n\n".join([
            doc.page_content for doc in docs
        ])

        formatted_prompt = prompt.invoke({
            "context": context,
            "question": question
        })

        response = llm.invoke(formatted_prompt)

        return jsonify({
            "answer": response.content,
            "chatId": chat_id
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)