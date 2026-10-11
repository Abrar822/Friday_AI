import { API_BASE_URL } from "../config/api";

export function FetchLocations() {
  return fetch(`${API_BASE_URL}/display`).then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error(`Some Error occurred. ${data.detail}`);
    }
    return data;
  });
}

export function SearchLocations(f_name) {
  return fetch(`${API_BASE_URL}/search`, {
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
  return fetch(`${API_BASE_URL}/delete`, {
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
  return fetch(`${API_BASE_URL}/insert`, {
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
