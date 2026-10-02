export async function sttConnect(file) {
  let formData = new FormData();
  formData.append("file", file);
  let response = await fetch("http://127.0.0.1:8000/stt", {
    method: "POST",
    body: formData,
  });
  let data = await response.json();
  if (!response.ok) {
    throw new Error(`${data.detail}`);
  }
  return data;
}