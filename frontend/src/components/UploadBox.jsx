import axios from "axios";
import { useState,useEffect } from "react";

function UploadBox({

  chats,
  setChats,
  currentChatId

}) {


  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const [status, setStatus] = useState("");

  //When currect chat id changes reset these states
  useEffect(() => {

  setFile(null);
  console.log(file);
  setStatus("");
  console.log(status)

}, [currentChatId]);

  // current active chat
  const currentChat = chats.find(
    (chat) => chat.chatId === currentChatId
  );

  const handleUpload = async () => {

    if (!file) {

      alert("Choose PDF first");

      return;
    }

    const formData = new FormData();

    formData.append("pdf", file);

    // VERY IMPORTANT
    formData.append("chatId", currentChatId);

    try {

      setLoading(true);

      // polling backend status
      const interval = setInterval(async () => {

        try {

          const res = await axios.get(
            "http://127.0.0.1:5000/status"
          );

          setStatus(res.data.status);

        } catch (err) {

          console.log(err);

        }

      }, 1000);

      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData
      );

      clearInterval(interval);

      setStatus("Ready to chat!");

      // update correct chat
      setChats((prev) =>{
        console.log(prev)
        return prev.map((chat) =>

          chat.chatId === currentChatId

            ? {

                ...chat,

                chatName: file.name,        //pdfName to chatName

                summary: response.data.summary,

                messages: [
                  ...chat.messages,

                  {
                    sender: "ai",

                    text:
                      "Document uploaded successfully. You can now ask questions."
                  }
                ]
              }

            : chat
        )}
      );

    } catch (error) {

      console.error(error);

      setStatus("Upload failed");

    } finally {

      setLoading(false);

    }
  };

  return (

  <div className="upload-box">

    <div className="upload-container">

      <label
        htmlFor="pdf-upload"
        className="file-label"
      >
        Choose PDF
      </label>

      <input
        id="pdf-upload"
        type="file"
        accept=".pdf"
        onChange={(e) => {
          setFile(e.target.files[0]);
        }}
      />

      <div className="selected-file">

        {
          file
            ? file.name
            : "No file selected"
        }

      </div>

      <button onClick={handleUpload}>

        {
          loading
            ? "Processing..."
            : "Upload PDF"
        }

      </button>

    </div>

    {
      status && (
        <p className="status-text">
          {status}
        </p>
      )
    }

    {
      currentChat?.summary && (

        <div className="summary-box">

          <h3>Document Summary</h3>

          <p>{currentChat.summary}</p>

        </div>
      )
    }

  </div>
);
}

export default UploadBox;