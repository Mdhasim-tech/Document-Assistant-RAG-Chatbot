import { useState } from "react";

function Sidebar({
  chats,
  setChats,
  currentChatId,
  setCurrentChatId,
}) {
  const [editingChatId, setEditingChatId] =
    useState(null);

  const [editedName, setEditedName] =
    useState("");

  const handleNewChat = () => {
    const newChat = {
      chatId: crypto.randomUUID(),
      chatName: "New Chat",
      messages: [],
    };

    setChats((prev) => [
      ...prev,
      newChat,
    ]);

    setCurrentChatId(newChat.chatId);
  };

  const handleDelete = (chatId) => {
    setChats((prev) => {
      const updatedChats = prev.filter(
        (chat) => chat.chatId !== chatId
      );

      if (currentChatId === chatId) {
        setCurrentChatId(
          updatedChats.length > 0
            ? updatedChats[0].chatId
            : null
        );
      }

      return updatedChats;
    });
  };

  const handleRename = (
    chatId,
    currentName
  ) => {
    setEditingChatId(chatId);
    setEditedName(currentName);
  };

  const saveRename = (chatId) => {
    const trimmedName =
      editedName.trim();

    if (!trimmedName) {
      setEditingChatId(null);
      return;
    }

    setChats((prev) =>
      prev.map((chat) =>
        chat.chatId === chatId
          ? {
              ...chat,
              chatName: trimmedName,
            }
          : chat
      )
    );

    setEditingChatId(null);
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
            className={`chat-item ${
              currentChatId === chat.chatId
                ? "active-chat"
                : ""
            }`}
            onClick={() =>
              setCurrentChatId(
                chat.chatId
              )
            }
          >
            {editingChatId ===
            chat.chatId ? (
              <input
                className="rename-input"
                value={editedName}
                onChange={(e) =>
                  setEditedName(
                    e.target.value
                  )
                }
                onBlur={() =>
                  saveRename(
                    chat.chatId
                  )
                }
                onKeyDown={(e) => {
                  if (
                    e.key ===
                    "Enter"
                  ) {
                    saveRename(
                      chat.chatId
                    );
                  }
                }}
                autoFocus
              />
            ) : (
              <span className="chat-name">
                {chat.chatName}
              </span>
            )}

            <button
              className="rename-btn"
              onClick={(e) => {
                e.stopPropagation();

                handleRename(
                  chat.chatId,
                  chat.chatName
                );
              }}
            >
              ✏️
            </button>

            <button
              className="delete-btn"
              onClick={(e) => {
                e.stopPropagation();

                handleDelete(
                  chat.chatId
                );
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