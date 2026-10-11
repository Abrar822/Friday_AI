
export let API_BASE_URL =
  import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

export function setApiBaseUrl(url) {
  API_BASE_URL = url;
}
