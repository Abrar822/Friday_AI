import { API_BASE_URL } from "../config/api";

export function settingConnect(data) {
  return fetch(`${API_BASE_URL}/settings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: data.name,
      api_key: data.api_key,
      llm_mode: data.llm_mode
    }),
  }).then(async (res) => {
    let response = await res.json();
    if (!res.ok) {
      throw new Error(response.detail);
    }
    return response;
  });
}

export function fetchSetting() {
  return fetch(`${API_BASE_URL}/settings_get`).then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail);
    }
    return data;
  });
}
