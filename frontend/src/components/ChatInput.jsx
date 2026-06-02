import { useState } from "react";
import axios from "axios";

function ChatInput({

  chats,
  setChats,
  currentChatId

}) {

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {

    if (!question.trim()) return;

    const userMessage = {

      sender: "user",

      text: question

    };

    // add user message to correct chat
    setChats((prev) =>

      prev.map((chat) =>

        chat.chatId === currentChatId

          ? {
              ...chat,

              messages: [
                ...chat.messages,
                userMessage
              ]
            }

          : chat
      )
    );

    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/ask",
        {
          question: question,

          chatId: currentChatId
        }
      );

      const aiMessage = {

        sender: "ai",

        text: response.data.answer
      };

      // add ai message to correct chat
      setChats((prev) =>

        prev.map((chat) =>

          chat.chatId === currentChatId

            ? {
                ...chat,

                messages: [
                  ...chat.messages,
                  aiMessage
                ]
              }

            : chat
        )
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

      setQuestion("");

    }
  };

  return (

    <div className="chat-input-container">

      <input
        type="text"
        placeholder="Ask something about the document..."
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
      />

      <button onClick={handleAsk}>

        {loading ? "Thinking..." : "Send"}

      </button>

    </div>
  );
}

export default ChatInput;