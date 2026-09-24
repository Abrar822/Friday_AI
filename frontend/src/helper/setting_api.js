export function settingConnect(data) {
  return fetch("http://127.0.0.1:8000/settings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: data.name,
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
  return fetch("http://127.0.0.1:8000/settings_get").then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail);
    }
    return data;
  });
}
