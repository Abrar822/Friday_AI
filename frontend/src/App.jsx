import { useState, useRef, useEffect } from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";
import Memory from "./pages/Memory";
import Sidebar from "./components/Sidebar";
import Chatbox from "./components/Chatbox";
import Alert from "./components/Alert";
import { fetchSetting } from "./helper/setting_api";
import { sttConnect } from "./helper/sttConnect";

function App() {
  const recordBtnRef = useRef(null); // To start mic with f2
  const sendBtnRef = useRef(null); // To simulate send btn
  const [simulateSend, setSimulateSend] = useState(false);
  const [prompt, setPrompt] = useState("");

  const menuBtnRef = useRef(null);
  const [state, setState] = useState("Listening"); // Listening, Working on it
  const [alert, setAlert] = useState({ msg: "", state: false });
  const [pickedFolder, setPickFolder] = useState([]);
  const [setting, setSetting] = useState({
    name: "",
  });
  const [tableUpdate, setTableUpdate] = useState(false);

  // STT STUFF
  useEffect(() => {
    const handle = (e) => {
      if (e.code === "F2") recordBtnRef.current.click();
    };
    window.addEventListener("keydown", handle);
    return () => {
      window.removeEventListener("keydown", handle);
    };
  }, []);

  let mediaRecorder = useRef(null);
  let audioChunks = useRef(null);
  let stream = useRef(null);

  const [recording, setRecording] = useState(false);

  const startRecorder = async () => {
    setRecording(true);
    audioChunks.current = [];

    stream.current = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });
    mediaRecorder.current = new MediaRecorder(stream.current);

    mediaRecorder.current.ondataavailable = (event) => {
      audioChunks.current.push(event.data);
    };

    mediaRecorder.current.onstop = async () => {
      try {
        let audioBlob = new Blob(audioChunks.current, {
          type: "audio/webm",
        });
        let audioFile = new File([audioBlob], "recording.webm", {
          type: "audio/webm",
        });

        let text = await sttConnect(audioFile);
        setPrompt(text.text);
        setSimulateSend(true);
      } catch (err) {
        setAlert({ msg: err.message, state: true });
      }
    };

    mediaRecorder.current.start();
  };
  // Simulating the sending
  useEffect(() => {
    if (simulateSend) {
      sendBtnRef.current.click();
      setSimulateSend(false);
    }
  }, [simulateSend]);

  const stopRecorder = () => {
    if (mediaRecorder.current) mediaRecorder.current.stop();
    if (stream.current)
      stream.current.getTracks().forEach((track) => track.stop());
    setRecording(false);
  }; // STT STUFF

  // Alert Box hide
  useEffect(() => {
    let id;
    if (alert.state) {
      id = setTimeout(() => {
        setAlert({ msg: "", state: false });
      }, 4000);
    }
    return () => {
      clearTimeout(id);
    };
  }, [alert]);

  // Fetching the already stored details of settings on start
  useEffect(() => {
    const execute = async () => {
      try {
        let data = await fetchSetting();
        setSetting({ name: data.name });
      } catch (err) {
        setAlert({ msg: "Error Fetching the Settings details.", state: true });
      }
    };
    execute();
  }, []);

  return (
    <>
      <div className="friday-ai">
        {alert.state && <Alert msg={alert.msg} />}
        {/* <Navbar menuBtnRef={menuBtnRef} /> */}
        <Sidebar menuBtnRef={menuBtnRef} />
        <Chatbox
          setState={setState}
          setAlert={setAlert}
          setTableUpdate={setTableUpdate}
          recording={recording}
          startRecorder={startRecorder}
          stopRecorder={stopRecorder}
          prompt={prompt}
          setPrompt={setPrompt}
          sendBtnRef={sendBtnRef}
          recordBtnRef={recordBtnRef}
        />
        <div className="page-content">
          <Routes>
            <Route
              path="/"
              element={
                <Dashboard
                  state={state}
                  setting={setting}
                  setAlert={setAlert}
                />
              }
            />
            <Route
              path="/dashboard"
              element={
                <Dashboard
                  state={state}
                  setting={setting}
                  setAlert={setAlert}
                />
              }
            />
            <Route
              path="/memory"
              element={
                <Memory
                  setTableUpdate={setTableUpdate}
                  tableUpdate={tableUpdate}
                  setAlert={setAlert}
                  pickedFolder={pickedFolder}
                  setPickFolder={setPickFolder}
                />
              }
            />
            <Route
              path="/settings"
              element={
                <Settings
                  setting={setting}
                  setSetting={setSetting}
                  setAlert={setAlert}
                />
              }
            />
          </Routes>
        </div>
      </div>
    </>
  );
}

export default App;
