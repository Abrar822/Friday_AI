export function FetchLocations() {
  return fetch("http://127.0.0.1:8000/display")
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return res.json();
    })
    .catch((err) => {
      return "Some Error Occurred." + String(err.message);
    });
}

export function SearchLocations(f_name) {
  return fetch("http://127.0.0.1:8000/search", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      f_name: f_name
    })
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return res.json();
    })
    .catch((err) => {
      return "Some Error Occurred. " + String(err.message);
    });
}
