import ReactMarkdown from "react-markdown";

function MessageBubble({ sender, text }) {
  return (
    <div className={`message ${sender}`}>
      <ReactMarkdown>
        {text}
      </ReactMarkdown>
    </div>
  );
}

export default MessageBubble;