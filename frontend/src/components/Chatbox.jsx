import "../stylesheets/Chatbox.css";
import { fastapiConnect } from "../helper/FastapiConnect";
import {
  pdfUpload,
  deletePdf,
  queryRequest,
  getData,
} from "../helper/pdf_assistant_api";

import { useEffect, useRef, useState } from "react";

export default function Chatbox({
  setState,
  setAlert,
  setTableUpdate,
  recording,
  startRecorder,
  stopRecorder,
  prompt,
  setPrompt,
  sendBtnRef,
  recordBtnRef
}) {
  const draggerRef = useRef(null);
  const modeBox = useRef(null);
  const chatboxRef = useRef(null);
  const textareaRef = useRef(null);
  const chatInputRef = useRef(null);
  const chatSectionRef = useRef(null);
  const [uploader, setUploader] = useState(false);
  const [mode, setMode] = useState({ mode: "Automation", state: false });

  const [messages, setMessages] = useState([
    {
      type: "bot-message",
      message: "Hi, Friday here. How can I help you?",
    },
  ]);
  const [loading, setLoading] = useState(false);

  const uploadFileRef = useRef(null);
  const [pdfs, setPdfs] = useState([]);
  const [storedFiles, setStoredFiles] = useState([]);
  const [isUploaded, setIsUploaded] = useState(false);
  const [copied, setCopied] = useState(null);

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
  }, []); // dragger

  // chatcontainer scrolls down each time a msg inserted
  useEffect(() => {
    if (chatSectionRef.current) {
      chatSectionRef.current.scrollTop = chatSectionRef.current.scrollHeight;
    }
  }, [messages]);

  // Clicking upload button
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

  // Clicking the delete button => clearing the whole db
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

  // Stuff to copy system response in chat container
  const copy = async (text) => {
    await navigator.clipboard.writeText(text);
  };
  useEffect(() => {
    const id = setTimeout(() => {
      setCopied(null);
    }, 1000);
    return () => {
      clearTimeout(id);
    };
  }, [copied]); // stuff to copy system response in chat container

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
      if (data.length > 0) {
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

  // hide the mode box
  useEffect(() => {
    const execute = (e) => {
      if (!mode.state) return;
      if (modeBox.current && !modeBox.current.contains(e.target)) {
        setMode((prev) => ({ ...prev, state: false }));
      }
    };
    document.addEventListener("mousedown", execute);
    return () => {
      document.removeEventListener("mousedown", execute);
    };
  }, [mode.state]);

  return (
    <>
      <div
        className="chat-box shadow-[-4px_0_8px_rgba(0,0,0,0.25)]"
        ref={chatboxRef}
      >
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
            <span className="chat-title font-bold relative">Chat</span>
            <div
              className={`${!loading ? "cursor-pointer" : "cursor-not-allowed"} mode-changer bg-(--message) text-(--text-primary) py-1 px-3 mx-6 rounded-4xl border-[1px] border-[white]/20 border-solid flex justify-center items-center gap-1 text-[14px] w-[135px]`}
              ref={modeBox}
              onClick={() => {
                if (loading) return;
                setMode((prev) => ({ ...prev, state: !prev.state }));
              }}
            >
              {mode.mode}{" "}
              <i
                className={`${mode.state && !loading ? "ti ti-chevron-up" : "ti ti-chevron-down"} inline-block h-full transition-all ease-in duration-750`}
              ></i>
              {mode.state && !loading && (
                <div className="select absolute flex flex-col top-[45px] z-2 bg-(--message) text-(--text-primary) shadow-[14px_14px_14px_rgba(0,0,0,0.25)]">
                  <span
                    className="px-2 py-1 w-full inline-block border-[1px] border-[white]/20 border-solid"
                    onClick={(e) => {
                      setMode({ mode: "Automation", state: false });
                      e.stopPropagation();
                    }}
                  >
                    Automation
                  </span>
                  <span
                    className="px-2 py-1 w-full inline-block border-[1px] border-[white]/20 border-solid cursor-pointer"
                    onClick={(e) => {
                      setMode({ mode: "Pdf Retrieval", state: false });
                      e.stopPropagation();
                    }}
                  >
                    Pdf Retrieval
                  </span>
                </div>
              )}
            </div>
            <div
              className="stt-btn text-(--text-primary) bg-transparent p-1 rounded-full border-[1px] border-solid w-[35px] h-[35px] border-[white]/20 flex justify-center items-center cursor-pointer transition-all duration-250 ease-in active:scale-95"
              onClick={recording ? stopRecorder : startRecorder}
              ref={recordBtnRef}
            >
              {recording ? (
                <i className="ti ti-microphone"></i>
              ) : (
                <i className="ti ti-microphone-off"></i>
              )}
            </div>
          </div>
          <div
            className="chat-section"
            style={{
              height: isUploaded ? "calc(100% - 170px)" : "calc(100% - 120px)",
            }}
            ref={chatSectionRef}
          >
            {messages.map((msg, idx) => (
              <div
                className={`${msg.type === "user-message" ? "justify-end" : "justify-start"} flex items-end gap-1 w-full relative`}
              >
                <pre className={msg.type} key={idx}>
                  {msg.message}
                </pre>
                {msg.type == "bot-message" && (
                  <i
                    className={`${copied === idx ? "ti ti-check text-(--text-secondary) text-[14px]" : "ti ti-copy text-(--text-secondary) cursor-pointer text-[14px]"} mb-[10px]`}
                    onClick={() => {
                      setCopied(idx);
                      copy(msg.message);
                    }}
                  ></i>
                )}
              </div>
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
                    if (prompt.trim().length <= 0 || loading || !/[a-zA-Z]/.test(prompt.trim())) return;
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
                      if (mode.mode === "Automation") {
                        response = await fastapiConnect(prompt);
                        // To update in memory ui table after folder state update
                        response.response.forEach((msg) => {
                          if (msg.includes("folder")) {
                            setTableUpdate(true);
                          }
                        });

                        newMessages = response.response.map((msg) => ({
                          type: "bot-message",
                          message: msg,
                        }));
                        setMessages((prev) => [...prev, ...newMessages]);
                      } else if (mode.mode === "Pdf Retrieval") {
                        if (!isUploaded) {
                          setMessages((prev) => [
                            ...prev,
                            {
                              type: "bot-message",
                              message: "Please upload a pdf.",
                            },
                          ]);
                          return;
                        }
                        response = await queryRequest(prompt);
                        setMessages((prev) => [
                          ...prev,
                          {
                            type: "bot-message",
                            message: response,
                          },
                        ]);
                      }
                    } catch (err) {
                      setMessages((prev) => [
                        ...prev,
                        {
                          type: "bot-message",
                          message:
                            "Sorry I could not process the request." +
                            str(err.message),
                        },
                      ]);
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
                ref={sendBtnRef}
                className="send-btn"
                title="Send Prompt"
                onClick={async () => {
                  if (prompt.trim().length <= 0 || loading || !/[a-zA-Z]/.test(prompt.trim())) return;
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
                    if (mode.mode === "Automation") {
                      response = await fastapiConnect(prompt);
                      // To update in memory ui table after folder state update
                      response.response.forEach((msg) => {
                        if (msg.includes("folder")) {
                          setTableUpdate(true);
                        }
                      });
                      newMessages = response.response.map((msg) => ({
                        type: "bot-message",
                        message: msg,
                      }));
                      setMessages((prev) => [...prev, ...newMessages]);
                    } else if (mode.mode === "Pdf Retrieval") {
                      if (!isUploaded) {
                        setMessages((prev) => [
                          ...prev,
                          {
                            type: "bot-message",
                            message: "Please upload a pdf.",
                          },
                        ]);
                        return;
                      }
                      response = await queryRequest(prompt);
                      setMessages((prev) => [
                        ...prev,
                        {
                          type: "bot-message",
                          message: response,
                        },
                      ]);
                    }
                  } catch (err) {
                    setMessages((prev) => [
                      ...prev,
                      {
                        type: "bot-message",
                        message:
                          "Sorry I could not process the request." +
                          str(err.message),
                      },
                    ]);
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
