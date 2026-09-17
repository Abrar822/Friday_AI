import { useState, useRef, use } from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import Dashboard from "./pages/Dashboard";
import Settings from "./pages/Settings";
import Memory from "./pages/Memory";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Chatbox from "./components/Chatbox";

function App() {
  const menuBtnRef = useRef(null);
  const [state, setState] = useState("Listening"); // Listening, Working on it

  return (
    <>
      <div className="friday-ai">
        <Navbar menuBtnRef={menuBtnRef} />
        <Sidebar menuBtnRef={menuBtnRef} />
        <Chatbox setState={setState} />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Dashboard state={state} />} />
            <Route path="/dashboard" element={<Dashboard state={state} />} />
            <Route path="/memory" element={<Memory />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </div>
    </>
  );
}

export default App;
