import { API_BASE_URL } from "../config/api";

export async function pdfUpload(formData) {
  let response = await fetch(`${API_BASE_URL}/pdf/upload`, {
    method: "POST",
    body: formData,
  });
  let filenames = response.json();
  return filenames;
}

export function deletePdf() {
  return fetch(`${API_BASE_URL}/pdf/delete`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    }
  }).then(async (res) => {
    let data = await res.json();
    if (!res.ok) {
      throw new Error("Failed to remove the files.");
    }
    return data;
  });
}

export function queryRequest(query) {
  return fetch(`${API_BASE_URL}/pdf/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: query
    })
  })
  .then(async res => {
    let data = await res.json()
    if(!res.ok) {
      throw new Error('Cannot perform query. Please try again.')
    }
    return data
  })
}

export function getData() {
  return fetch(`${API_BASE_URL}/pdf/get`)
  .then(async res => {
    let data = await res.json()
    if(!res.ok) {
      throw new Error(' Failed to Fetch.')
    }
    return data
  })
}