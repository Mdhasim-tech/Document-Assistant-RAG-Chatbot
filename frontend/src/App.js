import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./styles/app.css";
import { useState } from "react";

function App() {

  const [chats, setChats] = useState([]);

  const [currentChatId, setCurrentChatId] = useState(null);

  return (
    <div className="app">

      <Sidebar
        chats={chats}
        currentChatId={currentChatId}
        setCurrentChatId={setCurrentChatId}
        setChats={setChats}
      />

      <ChatWindow
        chats={chats}
        setChats={setChats}
        currentChatId={currentChatId}
      />

    </div>
  );
}

export default App;