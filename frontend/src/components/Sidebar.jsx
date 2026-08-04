import { useState } from "react";

function Sidebar({
  chats,
  setChats,
  currentChatId,
  setCurrentChatId,
  setMessages,
}) {
  const [editingChatId, setEditingChatId] = useState(null);

  const [editedName, setEditedName] = useState("");

  const handleNewChat = () => {
    const newChat = {
      chatId: crypto.randomUUID(),
      title: "New Chat",
    };

    setChats((prev) => [...prev, newChat]);

    setCurrentChatId(newChat.chatId);

    // Clear messages so welcome screen appears
    setMessages([]);
  };

  const handleRename = (chatId, currentName) => {
    setEditingChatId(chatId);
    setEditedName(currentName);
  };

  const saveRename = (chatId) => {
    const trimmedName = editedName.trim();

    if (!trimmedName) {
      setEditingChatId(null);
      return;
    }

    // Local update for now
    setChats((prev) =>
      prev.map((chat) =>
        chat.chatId === chatId
          ? {
            ...chat,
            title: trimmedName,
          }
          : chat
      )
    );

    // Backend API later
    // axios.patch(`/chat/${chatId}/rename`, { title: trimmedName });

    setEditingChatId(null);
  };

  const handleDelete = (chatId) => {
    console.log("Delete:", chatId);

    // Backend API later
    // axios.delete(`/chat/${chatId}`);

    setChats((prev) => prev.filter((chat) => chat.chatId !== chatId));

    if (currentChatId === chatId) {
      setCurrentChatId(null);
      setMessages([]);
    }
  };

  return (
    <div className="sidebar">
      <h2>RAG Chat</h2>

      <button
        className="new-chat-btn"
        onClick={handleNewChat}
      >
        + New Chat
      </button>

      <div className="documents">
        {chats.map((chat) => (
          <div
            key={chat.chatId}
            className={`chat-item ${currentChatId === chat.chatId
                ? "active-chat"
                : ""
              }`}
            onClick={() =>
              setCurrentChatId(chat.chatId)
            }
          >
            {editingChatId === chat.chatId ? (
              <input
                className="rename-input"
                value={editedName}
                onChange={(e) =>
                  setEditedName(e.target.value)
                }
                onBlur={() =>
                  saveRename(chat.chatId)
                }
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    saveRename(chat.chatId);
                  }
                }}
                autoFocus
              />
            ) : (
              <span className="chat-name">
                {chat.title ||
                  chat.pdfName ||
                  "New Chat"}
              </span>
            )}

            <button
              className="rename-btn"
              onClick={(e) => {
                e.stopPropagation();

                handleRename(
                  chat.chatId,
                  chat.title ||
                  chat.pdfName ||
                  "New Chat"
                );
              }}
            >
              ✏️
            </button>

            <button
              className="delete-btn"
              onClick={(e) => {
                e.stopPropagation();
                handleDelete(chat.chatId);
              }}
            >
              🗑️
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Sidebar;