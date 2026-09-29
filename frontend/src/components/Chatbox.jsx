import "../stylesheets/Chatbox.css";
import { fastapiConnect } from "../helper/FastapiConnect";
import {
  pdfUpload,
  deletePdf,
  queryRequest,
  getData,
} from "../helper/pdf_assistant_api";

import { use, useEffect, useRef, useState } from "react";

export default function Chatbox({ setState, setAlert }) {
  const draggerRef = useRef(null);
  const chatboxRef = useRef(null);
  const textareaRef = useRef(null);
  const chatInputRef = useRef(null);
  const chatSectionRef = useRef(null);
  const [uploader, setUploader] = useState(false);

  const [messages, setMessages] = useState([
    {
      type: "bot-message",
      message: "Hi, Friday here. How can I help you?",
    },
  ]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadFileRef = useRef(null);
  const [pdfs, setPdfs] = useState([]);
  const [storedFiles, setStoredFiles] = useState([]);
  const [isUploaded, setIsUploaded] = useState(false);

  // dragger
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

  // chatcontainer scrolls down each time a msg inserted
  useEffect(() => {
    if (chatSectionRef.current) {
      chatSectionRef.current.scrollTop = chatSectionRef.current.scrollHeight;
    }
  }, [messages]);

  const uploadFile = async () => {
    let formData = new FormData();
    pdfs.forEach((pdfObj) => {
      formData.append("files", pdfObj.file);
      formData.append("doc_ids", pdfObj.doc_id);
    });
    const upload = async () => {
      try {
        setUploader(true);
        let filenames = await pdfUpload(formData);
        pdfs.forEach((pdf) => {
          let exist = false;
          for (let fileObj of filenames) {
            if (fileObj.filename === pdf.file.name) {
              exist = true;
              break;
            }
          }
          if (!exist) {
            throw new Error("Pdf upload failed");
          }
        });
        setAlert({ msg: "Pdfs uploaded successfully.", state: true });
        setIsUploaded(true);
      } catch (err) {
        setAlert({ msg: "PDF upload failed.", state: true });
      } finally {
        setUploader(false);
      }
    };
    upload();
  };

  const deletePdfs = async () => {
    try {
      setUploader(true);
      let message = await deletePdf();
      setAlert({ msg: "All uploaded pdfs removed.", state: true });
      setPdfs([]);
      setIsUploaded(false);
    } catch (err) {
      setAlert({ msg: err.message, state: true });
    } finally {
      setUploader(false);
    }
  };

  // storing the filenames along with their doc_id for display
  useEffect(() => {
    let names = pdfs.map((pdf) => ({
      filename: pdf.file.name,
      doc_id: pdf.doc_id,
    }));
    setStoredFiles(names);
  }, [pdfs]);

  // On refresh get the stored data unless deleted manually
  useEffect(() => {
    const fetchData = async () => {
      let data = await getData();
      if(data.length > 0) {
        setStoredFiles(data);
        setIsUploaded(true); 
      }
    };
    try {
      fetchData();
    } catch (err) {
      setAlert("Failed to Fetch uploaded Pdfs.");
    }
  }, []);

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
          <div
            className="chat-section"
            style={{
              height: isUploaded ? "calc(100% - 170px)" : "calc(100% - 120px)",
            }}
            ref={chatSectionRef}
          >
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
              {storedFiles.length > 0 && (
                <div className="files-show">
                  <button
                    title={
                      !isUploaded ? "Upload Pdfs" : "Delete all uploaded pdfs"
                    }
                    className="upload-btn"
                    onClick={!isUploaded ? uploadFile : deletePdfs}
                  >
                    {uploader && (
                      <div className="w-4 h-4 border-[transparent] border-r-(--text-primary) border-2 border-t-(--text-primary) rounded-full animate-spin"></div>
                    )}
                    {!isUploaded ? "Upload" : "Delete"}
                  </button>
                  {storedFiles.map((file) => (
                    <div className="name-box" key={file.doc_id}>
                      {file.filename}
                      {!isUploaded && (
                        <div
                          className="file-cross-btn"
                          onClick={() => {
                            let updatedPdfs = pdfs.filter(
                              (pdfObj) => pdfObj.doc_id != file.doc_id,
                            );
                            setPdfs(updatedPdfs);
                          }}
                        >
                          <i className="ti ti-x"></i>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
              <input
                type="file"
                multiple
                accept=".pdf"
                style={{ display: "none" }}
                ref={uploadFileRef}
                onChange={(e) => {
                  let files = Array.from(e.target.files);
                  let fileArr = files.map((file) => ({
                    file: file,
                    doc_id: crypto.randomUUID(),
                  }));
                  setPdfs((prev) => [...prev, ...fileArr]);
                }}
              />
              <button
                className={`add-btn${isUploaded ? " block" : ""}`}
                title={!isUploaded ? "Add Pdf" : "Cannot add pdf"}
                onClick={() => {
                  if (isUploaded) return;
                  uploadFileRef.current.click();
                }}
              >
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
                      let response, newMessages;
                      if (!isUploaded) {
                        response = await fastapiConnect(prompt);
                        // need to update in memory ui table after folder state update
                        newMessages = response.response.map((msg) => ({
                          type: "bot-message",
                          message: msg,
                        }));
                        setMessages((prev) => [...prev, ...newMessages]);
                      } else {
                        response = await queryRequest(prompt);
                        setMessages((prev) => [
                          ...prev,
                          {
                            type: "bot-message",
                            message: response,
                          },
                        ]);
                      }
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
                    let response, newMessages;
                    if (!isUploaded) {
                      response = await fastapiConnect(prompt);
                      newMessages = response.response.map((msg) => ({
                        type: "bot-message",
                        message: msg,
                      }));
                      setMessages((prev) => [...prev, ...newMessages]);
                    } else {
                      response = await queryRequest(prompt);
                      setMessages((prev) => [
                        ...prev,
                        {
                          type: "bot-message",
                          message: response,
                        },
                      ]);
                    }
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
