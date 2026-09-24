import "../stylesheets/Sidebar.css";

import { useNavigate, useLocation } from "react-router-dom";

export default function Sidebar({ menuBtnRef }) {
  const navigate = useNavigate();
  const location = useLocation();
  let page = location.pathname.slice(1);

  return (
    <>
      <div className="sidebar font-bold" ref={menuBtnRef}>
        <div
          onClick={() => {
            navigate("/dashboard");
          }}
          style={
            page === "dashboard" || page === ""
              ? { color: "#4FD8FF" }
              : undefined
          }
        >
          <span className="sidebar-icons">
            <i className="ti ti-layout-dashboard"></i>
          </span>
          Dashboard
        </div>
        <div
          onClick={() => {
            navigate("/memory");
          }}
          style={page === "memory" ? { color: "#4FD8FF" } : undefined}
        >
          <span className="sidebar-icons">
            <i className="ti ti-brain"></i>
          </span>
          Memory
        </div>
        <div
          onClick={() => {
            navigate("/settings");
          }}
          style={page === "settings" ? { color: "#4FD8FF" } : undefined}
        >
          <span className="sidebar-icons">
            <i className="ti ti-settings"></i>
          </span>
          Settings
        </div>
      </div>
    </>
  );
}
