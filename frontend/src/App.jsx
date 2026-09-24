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

function App() {
  const menuBtnRef = useRef(null);
  const [state, setState] = useState("Listening"); // Listening, Working on it
  const [alert, setAlert] = useState({ msg: "", state: false });
  const [pickedFolder, setPickFolder] = useState([]);
  const [setting, setSetting] = useState({
    name: "",
  });

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

  useEffect(() => {
    const execute = async () => {
      try {
        let data = await fetchSetting();
        setSetting({ name: data.name });
      } catch (err) {
        setAlert({ msg: "Error Fetching the Settings details.", state: true });
      }
    };
    execute()
  }, []);

  return (
    <>
      <div className="friday-ai">
        {alert.state && <Alert msg={alert.msg} />}
        {/* <Navbar menuBtnRef={menuBtnRef} /> */}
        <Sidebar menuBtnRef={menuBtnRef} />
        <Chatbox setState={setState} />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Dashboard state={state} setting={setting} />} />
            <Route path="/dashboard" element={<Dashboard state={state} setting={setting} />} />
            <Route
              path="/memory"
              element={
                <Memory
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
