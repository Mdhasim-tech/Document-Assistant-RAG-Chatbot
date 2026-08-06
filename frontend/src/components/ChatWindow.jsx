import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import UploadBox from "./UploadBox";
import { useRef, useEffect } from "react";

function ChatWindow({
  chats,
  setChats,
  messages,
  setMessages,
  currentChatId,
  fetchChats
}) {

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const currentChat = chats.find(
    (chat) => chat.chatId === currentChatId
  );

  return (
    <div className="chat-window">

      <div className="messages">

        {!currentChat ? (

          <div className="welcome-message">
            Create a new chat to begin Or <br></br>select an existing one.
          </div>

        ) : (

          <>
              {messages.length === 0 && !currentChat.summary && (
              <div className="welcome-message">
                Upload a document and start chatting.
              </div>
            )}

            {/* Show upload only if no PDF uploaded */}
            {!currentChat.pdfName && (
              <UploadBox
                currentChatId={currentChatId}
                fetchChats={fetchChats}
              />
            )}

            {/* Show summary after upload */}
            {currentChat.summary && (
              <div className="summary-box">
                <h3>Document Summary</h3>
                <p>{currentChat.summary}</p>
              </div>
            )}

            {/* Chat messages */}
            {messages.map((msg, index) => (
              <MessageBubble
                key={index}
                sender={msg.sender}
                text={msg.text}
              />
            ))}
          </>
        )}

        <div ref={bottomRef}></div>

      </div>

      {currentChat && (
        <ChatInput
          currentChatId={currentChatId}
          messages={messages}
          setMessages={setMessages}
        />
      )}

    </div>
  );
}

export default ChatWindow;