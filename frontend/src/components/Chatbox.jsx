import "../stylesheets/Chatbox.css";
import { fastapiConnect } from "../helper/FastapiConnect";

import { useEffect, useRef, useState } from "react";

export default function Chatbox({ setState }) {
  const draggerRef = useRef(null);
  const chatboxRef = useRef(null);
  const textareaRef = useRef(null);
  const chatInputRef = useRef(null);
  const chatSectionRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      type: "bot-message",
      message: "Hi, I am Friday. How can I help you?",
    },
  ]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let draggable = false;
    const dragger = draggerRef.current;
    if (!dragger) return;

    let rect;

    const pointerDown = () => {
      if (!chatboxRef.current) return;

      draggable = true;
      rect = chatboxRef.current.getBoundingClientRect();
      document.body.style.userSelect = "none";
    };
    const pointerMove = (e) => {
      if (draggable && chatboxRef.current) {
        let delta = rect.left - e.clientX;
        let newWidth = Math.max(400, Math.min(900, rect.width + delta));

        chatboxRef.current.style.width = `${newWidth}px`;
      }
    };
    const pointerUp = () => {
      draggable = false;
      document.body.style.userSelect = "";
    };
    dragger.addEventListener("pointerdown", pointerDown);
    document.addEventListener("pointermove", pointerMove);
    document.addEventListener("pointerup", pointerUp);

    return () => {
      dragger.removeEventListener("pointerdown", pointerDown);
      document.removeEventListener("pointermove", pointerMove);
      document.removeEventListener("pointerup", pointerUp);
    };
  }, []);

  useEffect(() => {
    if (chatSectionRef.current) {
      chatSectionRef.current.scrollTop = chatSectionRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <>
      <div className="chat-box" ref={chatboxRef}>
        <div className="dragger" ref={draggerRef}></div>
        <div className="chat-container">
          <div className="cross-btn-container">
            <span
              className="cross-btn"
              onClick={() => {
                chatboxRef.current.style.width = "0px";
              }}
            >
              <i className="ti ti-x"></i>
            </span>
            <span className="chat-title font-bold">Chat</span>
          </div>
          <div className="chat-section" ref={chatSectionRef}>
            {messages.map((msg, idx) => (
              <pre className={msg.type} key={idx}>
                {msg.message}
              </pre>
            ))}
            {loading && (
              <div className="loading bot-message" key={12345}>
                <div className="typing-loader">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div className="chat-input" ref={chatInputRef}>
              <button className="add-btn" title="Add Pdf">
                <i className="ti ti-plus"></i>
              </button>
              <textarea
                className="input-bar"
                placeholder="Ask Friday.."
                ref={textareaRef}
                rows={1}
                onKeyDown={async (e) => {
                  if (e.key == "Enter" && !e.shiftKey) {
                    if (prompt.trim().length <= 0 || loading) return;
                    e.preventDefault();
                    setMessages((prev) => [
                      ...prev,
                      { type: "user-message", message: prompt.trim() },
                    ]);
                    setPrompt("");
                    chatInputRef.current.style.height = `auto`;
                    setLoading(true);
                    setState("Working on it");
                    try {
                      let response = await fastapiConnect(prompt);
                      let newMessages = response.response.map((msg) => ({
                        type: "bot-message",
                        message: msg,
                      }));
                      setMessages((prev) => [...prev, ...newMessages]);
                    } finally {
                      setLoading(false);
                      setState("Listening");
                    }
                  }
                }}
                onChange={(e) => {
                  setPrompt(e.target.value);
                }}
                value={prompt}
                onInput={() => {
                  chatInputRef.current.style.height = `auto`;
                  let styles = getComputedStyle(chatInputRef.current);
                  // Added vertical padding as scrollheight of textarea doesnt include padding of chatinput
                  let height =
                    Math.min(textareaRef.current.scrollHeight, 250) +
                    parseFloat(styles.paddingTop) +
                    parseFloat(styles.paddingBottom);
                  chatInputRef.current.style.height = `${height}px`;
                }}
              />
              <button
                className="send-btn"
                title="Send Prompt"
                onClick={async () => {
                  if (prompt.trim().length <= 0 || loading) return;
                  setMessages((prev) => [
                    ...prev,
                    { type: "user-message", message: prompt.trim() },
                  ]);
                  setPrompt("");

                  chatInputRef.current.style.height = `auto`;
                  setLoading(true);
                  setState("Working on it");
                  try {
                    let response = await fastapiConnect(prompt);
                    let newMessages = response.response.map((msg) => ({
                      type: "bot-message",
                      message: msg,
                    }));
                    setMessages((prev) => [...prev, ...newMessages]);
                  } finally {
                    setLoading(false);
                    setState("Listening");
                  }
                }}
              >
                <i className="ti ti-arrow-up"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        className="chat-btn"
        title="Chats"
        onClick={() => {
          chatboxRef.current.style.width = "400px";
        }}
      >
        <i className="ti ti-messages"></i>
      </div>
    </>
  );
}
