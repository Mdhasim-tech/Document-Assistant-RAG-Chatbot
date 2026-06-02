import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import UploadBox from "./UploadBox";
import { useRef,useEffect } from "react";

function ChatWindow({

  chats,
  setChats,
  currentChatId

}) {
    const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [chats]);

  // active chat
  const currentChat = chats.find(
    (chat) => chat.chatId === currentChatId
  );

  return (

    <div className="chat-window">

      <div className="messages">

        {
          !currentChat && (

            <div className="welcome-message">

              Create a new chat to begin.

            </div>
          )
        }

        {
          currentChat &&
          currentChat.messages.length === 0 && (

            <div className="welcome-message">

              Upload a document and start chatting.

            </div>
          )
        }

        {
          currentChat && (

            <UploadBox

              chats={chats}

              setChats={setChats}

              currentChatId={currentChatId}

            />
          )
        }

        {
          currentChat?.messages.map((msg, index) => (

            <MessageBubble
              key={index}
              sender={msg.sender}
              text={msg.text}
            />

          ))
        }
        <div ref={bottomRef}></div>

      </div>

      {
        currentChat && (

          <ChatInput

            chats={chats}

            setChats={setChats}

            currentChatId={currentChatId}

          />
        )
      }


    </div>
  );
}

export default ChatWindow;