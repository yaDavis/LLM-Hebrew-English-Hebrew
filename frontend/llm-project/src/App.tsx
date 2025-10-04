import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [temperature, setTemperature] = useState('0.7');
  const [topP, setTopP] = useState('0.9');
  const [topK, setTopK] = useState('40');
  const [maxTokens, setMaxTokens] = useState('256');
  const [summary, setSummary] = useState("");
  const handleSummarize = async () => {
    setSummary("");
    const response = await fetch("http://localhost:8000/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt, temperature, top_p: topP, top_k: topK, max_tokens: maxTokens }),
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
      <div className="config-container">
        <div>
        <label htmlFor="">Temperature</label>
        <input type="text" value={temperature} onChange={(e) => setTemperature(e.target.value)}/>
        </div>
        <div>
        <label htmlFor="">Top P</label>
        <input type="text" value={topP} onChange={(e) => setTopP(e.target.value)}/>
        </div>
        <div>
        <label htmlFor="">Top K</label>
        <input type="text" value={topK} onChange={(e) => setTopK(e.target.value)}/>
        </div>
        <div><label htmlFor="">Max tokens</label>
        <input type="text" value={maxTokens} onChange={(e) => setMaxTokens(e.target.value)} />
      </div></div>
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
      <div className="summary-output">
        {summary && summary.split("-").map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </div>
    </div>
  );
}

export default App;
