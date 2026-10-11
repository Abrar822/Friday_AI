import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import App from "./App.jsx";
import "@tabler/icons-webfont/dist/tabler-icons.min.css";
import { invoke } from "@tauri-apps/api/core";
import { setApiBaseUrl } from "./config/api";

async function bootstrap() {
  if (window.__TAURI_INTERNALS__) {
    const backendUrl = await invoke("get_backend_url");
    console.log("Tauri backend URL:", backendUrl);
    setApiBaseUrl(backendUrl);
  }

  createRoot(document.getElementById("root")).render(
    <BrowserRouter>
      <App />
    </BrowserRouter>,
  );
}

bootstrap().catch((error) => {
  console.error("Failed to initialize Friday:", error);
});
