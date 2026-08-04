import axios from "axios";
import { useState, useEffect } from "react";

function UploadBox({
  currentChatId,
  fetchChats,
}) {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  useEffect(() => {
    setFile(null);
    setStatus("");
  }, [currentChatId]);

  const handleUpload = async () => {

    if (!file) {
      alert("Choose a PDF first.");
      return;
    }

    const formData = new FormData();

    formData.append("pdf", file);
    formData.append("chatId", currentChatId);

    let interval;

    try {

      setLoading(true);

      interval = setInterval(async () => {

        try {

          const res = await axios.get(
            `http://127.0.0.1:5000/status/${currentChatId}`
          );

          setStatus(res.data.status);

        } catch (err) {

          console.error(err);

        }

      }, 1000);

      await axios.post(
        "http://127.0.0.1:5000/upload",
        formData
      );

      clearInterval(interval);

      setStatus("Ready to chat!");

      // Reload chats so title/pdfName/summary are updated
      await fetchChats();

    } catch (error) {

      console.error(error);

      if (interval) clearInterval(interval);

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
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        <div className="selected-file">
          {file ? file.name : "No file selected"}
        </div>

        <button
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "Processing..." : "Upload PDF"}
        </button>

      </div>

      {status && (
        <p className="status-text">
          {status}
        </p>
      )}

    </div>

  );

}

export default UploadBox;