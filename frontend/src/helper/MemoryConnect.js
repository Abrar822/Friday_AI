export function FetchLocations() {
  return fetch("http://127.0.0.1:8000/display").then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(`Some Error occurred. ${data.detail}`);
    }
    return data;
  });
}

export function SearchLocations(f_name) {
  return fetch("http://127.0.0.1:8000/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      f_name: f_name,
    }),
  }).then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(`Some Error occurred. ${data.detail}`);
    }
    return data;
  });
}

export function deleteLocations(foldernamesDict) {
  return fetch("http://127.0.0.1:8000/delete", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(foldernamesDict),
  }).then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(`Some Error occurred. ${data.detail}`);
    }
    return data;
  });
}

export function upsertLocations(folderLocations) {
  return fetch("http://127.0.0.1:8000/insert", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      folder_locations: folderLocations
    }),
  }).then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail);
    }
    return data;
  });
}
