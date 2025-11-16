import React, { useState } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [jsonData, setJsonData] = useState("");
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleRegister = async () => {
    const res = await fetch("http://127.0.0.1:8000/user/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    setResponse(data);
  };

  const handleUploadJson = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/upload/json", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, data: JSON.parse(jsonData) }),
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: "Invalid JSON" });
    }
  };

  const handleUploadFile = async () => {
    const formData = new FormData();
    formData.append("email", email);
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload/media", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setResponse(data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>SmartStore Frontend</h1>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleRegister}>Register User</button>

      <hr />

      <textarea
        placeholder='Enter JSON data here'
        value={jsonData}
        onChange={(e) => setJsonData(e.target.value)}
        rows={6}
        cols={50}
      />
      <button onClick={handleUploadJson}>Upload JSON</button>

      <hr />

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUploadFile}>Upload File</button>

      <hr />

      <pre>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}

export default App;
