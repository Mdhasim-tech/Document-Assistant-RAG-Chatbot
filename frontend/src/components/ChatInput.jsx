import { useState } from "react";
import axios from "axios";

const API_URL =
  "http://localhost:5000";

function ChatInput({

  currentChatId,
  messages,
  setMessages

}) {

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || !currentChatId || loading) {
      return;
    }

    const userMessage = {
      sender: "user",
      text: trimmedQuestion
    };

    // Show user message immediately
    setMessages(prev => [
      ...prev,
      userMessage
    ]);

    setQuestion("");
    setLoading(true);

    try {

      const response = await axios.post(
        `${API_URL}/ask`,
        {
          question: trimmedQuestion,
          chatId: currentChatId
        }
      );

      const aiMessage = {
        sender: "assistant",
        text: response.data.answer
      };

      setMessages(prev => [
        ...prev,
        aiMessage
      ]);

    } catch (error) {

      console.error(error);

      // Remove the optimistic user message if request failed
      setMessages(prev => prev.slice(0, -1));

      alert("Failed to get response from the server.");

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="chat-input-container">

      <input
        type="text"
        placeholder="Ask something about the document..."
        value={question}
        disabled={loading}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleAsk();
          }
        }}
      />

      <button
        onClick={handleAsk}
        disabled={loading || !currentChatId}
      >
        {loading ? "Thinking..." : "Send"}
      </button>

    </div>

  );
}

export default ChatInput;