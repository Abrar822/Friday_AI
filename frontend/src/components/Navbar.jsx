import "../stylesheets/Navbar.css";

export default function Navbar({ menuBtnRef }) {
  return (
    <>
      <div className="navbar-container">
        <nav className="navbar">
          <div
            className="menu-btn"
            onClick={() => {
              menuBtnRef.current.classList.toggle("collapsed");
            }}
          >
            <i className="ti ti-menu-2"></i>
          </div>

          <div className="logo">
            <span style={{'fontWeight': '600'}} className="tracking-wide">Friday</span> <span style={{'color': '#4FD8FF', 'fontWeight': '600'}}>AI</span>
          </div>
        </nav>
      </div>
    </>
  );
}