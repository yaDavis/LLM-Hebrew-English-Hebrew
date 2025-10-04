import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [summary, setSummary] = useState("");
  const handleSummarize = async () => {
    setSummary("");
    const response = await fetch("http://localhost:8000/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.body) {
      const text = await response.text();
      setSummary(text);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) {
        const chunk = decoder.decode(value, { stream: true });
        setSummary((prev) => prev + chunk);
      }
    }
  };
  return (
    <div className="app-container">
      <h1>Hebrew Text Summarizer</h1>
      <div className="input-container">
        <textarea
          className="prompt-input"
          rows={10}
          cols={50}
          placeholder="Enter your prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button className="summarize-button" onClick={handleSummarize}>
          Summarize
        </button>
      </div>
      <div className="summary-output">{summary}</div>
    </div>
  );
}

export default App;
