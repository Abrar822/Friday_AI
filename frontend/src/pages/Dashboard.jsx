import "../stylesheets/Dashboard.css";
import FridayLogo from "../components/Friday";

export default function Dashboard({ state, setting }) {
  return (
    <>
      <FridayLogo />
      <div className="dashboard">
        <div className="dashboard-content">
          <div className="wish">
            <h2 className="font-bold">
              Hello, <span className="username">{setting.name}</span>
            </h2>
            <h2>How can I help you today?</h2>
          </div>
          <div className="state font-bold tracking-widest opacity-70 font-[Orbitron]">{state}...</div>
          <div className="quick-actions font-extrabold tracking-wider opacity-70">
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
