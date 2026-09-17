import Orb from "../components/Orb";
import "../stylesheets/Dashboard.css";

export default function Dashboard({ state }) {
  return (
    <>
      <div className="dashboard">
        <div className="dashboard-content">
          <div className="wish">
            <h2>
              Hello, <span className="username">Abrar</span>
            </h2>
            <h2>How can I help you today?</h2>
          </div>
          {/* <Orb /> */}
          <div className="state">{state}...</div>
          <div className="quick-actions">
            <button className="quick-action">
              <span className="quick-action-icon">
                <i className="ti ti-apps"></i>
              </span>
              <span>Open App</span>
            </button>

            <button className="quick-action">
              <span className="quick-action-icon">
                <i className="ti ti-world-search"></i>
              </span>
              <span>Search Web</span>
            </button>

            <button className="quick-action">
              <span className="quick-action-icon">
                <i className="ti ti-folder-cog"></i>
              </span>
              <span>Manage Files</span>
            </button>

            <button className="quick-action">
              <span className="quick-action-icon">
                <i className="ti ti-mail-ai"></i>
              </span>
              <span>Generate Email</span>
            </button>

            <button className="quick-action">
              <span className="quick-action-icon">
                <i className="ti ti-file-type-pdf"></i>
              </span>
              <span>Chat with PDF</span>
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
