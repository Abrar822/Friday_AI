export function settingConnect(data) {
  return fetch("http://127.0.0.1:8000/settings", {
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
    console.log('response: ', response)
    return response;
  });
}

export function fetchSetting() {
  return fetch("http://127.0.0.1:8000/settings_get").then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail);
    }
    console.log('fetched: ', data)
    return data;
  });
}
