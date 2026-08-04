import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./styles/app.css";
import { useState, useEffect, useCallback } from "react";

function App() {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);

  // ---------------------------
  // Load all chats
  // ---------------------------

  const fetchChats = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:5000/chats");

      const data = await response.json();

      console.log("Chats from backend:", data);

      const formattedChats = data.map((chat) => ({
        chatId: chat.chatId,
        title: chat.title || chat.pdfName || "New Chat",
        pdfName: chat.pdfName,
        summary: chat.summary || "",
        status: chat.status,
        uploadedAt: chat.uploadedAt,
      }));

      setChats(formattedChats);
    } catch (err) {
      console.error(err);
    }
  }, []);

  useEffect(() => {
    fetchChats();
  }, [fetchChats]);

  // ---------------------------
  // Load messages only
  // ---------------------------

  useEffect(() => {
    if (!currentChatId) {
      setMessages([]);
      return;
    }

    const fetchMessages = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/chat/${currentChatId}`
        );

        const data = await response.json();

        const formattedMessages = data.map((msg) => ({
          sender: msg.role,
          text: msg.content,
        }));

        setMessages(formattedMessages);
      } catch (err) {
        console.error(err);
      }
    };

    fetchMessages();
  }, [currentChatId]);

  return (
    <div className="app">
      <Sidebar
        chats={chats}
        setChats={setChats}
        currentChatId={currentChatId}
        setCurrentChatId={setCurrentChatId}
        setMessages={setMessages}
        fetchChats={fetchChats}
      />

      <ChatWindow
        chats={chats}
        setChats={setChats}
        messages={messages}
        setMessages={setMessages}
        currentChatId={currentChatId}
        fetchChats={fetchChats}
      />
    </div>
  );
}

export default App;