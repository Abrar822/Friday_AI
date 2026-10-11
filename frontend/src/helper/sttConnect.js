import { API_BASE_URL } from "../config/api";

export async function sttConnect(file) {
  let formData = new FormData();
  formData.append("file", file);
  let response = await fetch(`${API_BASE_URL}/stt`, {
    method: "POST",
    body: formData,
  });
  let data = await response.json();
  if (!response.ok) {
    throw new Error(`${data.detail}`);
  }
  return data;
}