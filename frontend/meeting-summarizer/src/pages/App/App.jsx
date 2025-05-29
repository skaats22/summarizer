import { useState, useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router";
import "./App.css";

const BASE_URL = "http://localhost:8000/api";

function App() {
  const [notes, setNotes] = useState("");
  const [summary, setSummary] = useState("");
  const [email, setEmail] = useState("");

  async function handleSummarize() {
    const response = await fetch(`${BASE_URL}/summarize/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ notes }),
    });
    const data = await response.json();
    setSummary(data.summary);
  }

  async function handleEmail() {
    const response = await fetch(`${BASE_URL}/email/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ summary }),
    });
    const data = await response.json();
    setEmail(data.email);
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Sales Meeting Summarizer</h1>
      <textarea
        rows={10}
        cols={50}
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Paste your meeting notes here..."
      />
      <br />
      <button onClick={handleSummarize}>Generate Summary</button>

      {summary && (
        <div>
          <h2>Summary</h2>
          <p>{summary}</p>
          <button onClick={handleEmail}>Generate Follow-up Email</button>
        </div>
      )}

      {email && (
        <div>
          <h2>Email</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{email}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
