export async function pdfUpload(formData) {
  let response = await fetch("http://127.0.0.1:8000/pdf/upload", {
    method: "POST",
    body: formData,
  });
  let filenames = response.json();
  return filenames;
}

export function deletePdf() {
  return fetch("http://127.0.0.1:8000/pdf/delete", {
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
  return fetch('http://127.0.0.1:8000/pdf/query', {
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
  return fetch('http://127.0.0.1:8000/pdf/get')
  .then(async res => {
    let data = await res.json()
    if(!res.ok) {
      throw new Error(' Failed to Fetch.')
    }
    return data
  })
}