import { useState } from "react";
 import { useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [provider, setProvider] = useState("ollama");
  const [displayedAnswer,setDisplayedAnswer]=useState("");
  const [summary,setSummary]=useState(null);
  const [relatedQuestions, setRelatedQuestions] = useState([]);
  const [history, setHistory] = useState([]);
useEffect(() => {

    const savedHistory = localStorage.getItem("veritas-history");

    if(savedHistory){

        setHistory(JSON.parse(savedHistory));

    }

}, []);
useEffect(()=>{

if(!answer) return;

setDisplayedAnswer("");

let i=0;

const interval=setInterval(()=>{

setDisplayedAnswer(answer.slice(0,i));

i++;

if(i>answer.length){

clearInterval(interval);

}

},8);

return ()=>clearInterval(interval);

},[answer]);
useEffect(() => {
  axios
    .get("http://127.0.0.1:8000/")
    .then(() => setBackendStatus("Online"))
    .catch(() => setBackendStatus("Offline"));
}, []);
   const getBadge = (domain) => {
  
  domain = domain.toLowerCase();

  if(domain.includes("who.int"))
      return {text:"Official",color:"#22c55e",icon:"🟢"};

  if(domain.includes("nih.gov"))
      return {text:"Government",color:"#3b82f6",icon:"🏛️"};

  if(domain.includes(".gov"))
      return {text:"Government",color:"#3b82f6",icon:"🏛️"};

  if(domain.includes(".edu"))
      return {text:"University",color:"#8b5cf6",icon:"🎓"};

  if(domain.includes("nature"))
      return {text:"Peer Reviewed",color:"#f97316",icon:"📄"};

  if(domain.includes("reuters"))
      return {text:"News Agency",color:"#06b6d4",icon:"📰"};

  if(domain.includes("bbc"))
      return {text:"News Agency",color:"#06b6d4",icon:"📰"};

  return {text:"Web Source",color:"#64748b",icon:"🌐"};
}
  const askAI = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setConfidence(null);
    setSources([]);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        question,
        provider
      });

      setAnswer(res.data.answer);
      setConfidence(res.data.confidence);
      setSources(res.data.sources || []);
      setSummary(res.data.summary);
      setRelatedQuestions(res.data.related_questions || []);
       
      console.log(sources);
    } catch (err) {
      console.error(err);
      setAnswer("Unable to connect to backend.");
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="statusIndicator">
  <span
    className={`statusDot ${
      backendStatus === "Online" ? "online" : "offline"
    }`}
  ></span>

  Backend {backendStatus}
</div>
      {/* Hero */}

      <div className="hero">

        <div className="logo">
          <div className="logoCircle">V</div>
          <div>
            <h1>VERITAS AI</h1>
            <p>Truth. Backed by Evidence.</p>
          </div>
        </div>

        <div className="badges">
          <span>🧠 Local LLM</span>
          <span>📚 RAG</span>
          <span>🌐 Live Search</span>
          <span>⚡ FastAPI</span>
          <span>🔍 ChromaDB</span>
        </div>

      </div>

      {/* Search */}
      <div className="providerContainer">

  <label>Inference Engine</label>

  <select
    value={provider}
    onChange={(e) => setProvider(e.target.value)}
  >
    <option value="ollama">🧠 Ollama (Local)</option>
    <option value="gemini">✨ Gemini API</option>
  </select>

</div>

      <div className="searchContainer">

        <input
          type="text"
          placeholder="Ask any research question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") askAI();
          }}
        />

        <button onClick={askAI}>
          Research
        </button>

      </div>

      {/* Loading */}

      {loading && (

        <div className="pipeline">

          <h3>Research Pipeline</h3>

          <div className="step">🌐 Searching trusted sources...</div>
          <div className="step">📄 Extracting webpages...</div>
          <div className="step">🧩 Chunking documents...</div>
          <div className="step">🧠 Creating embeddings...</div>
          <div className="step">📚 Retrieving relevant knowledge...</div>
          <div className="step">🤖 Generating response...</div>

        </div>

      )}

      {!loading && answer && (

        <>

          <div className="answerCard">

            <div className="cardHeader">

              <h2>Generated Answer</h2>

              <button
                className="copyBtn"
                onClick={() => navigator.clipboard.writeText(answer)}
              >
                Copy
              </button>

            </div>

            <p>{displayedAnswer}</p>

          </div>

          <div className="bottomGrid">

            <div className="confidenceCard">

              <h3>Retrieval Score</h3>

              <div className="progressBar">

                <div
                  className="progressFill"
                  style={{ width: `${confidence || 0}%` }}
                ></div>

              </div>

              <div className="confidenceNumber">
                {confidence ?? 0}%
              </div>
            <div className="historyCard">

    <div className="historyHeader">

        <h3>🕘 Search History</h3>

        {history.length > 0 && (

            <button
                className="clearHistoryBtn"
                onClick={() => {

                    localStorage.removeItem("veritas-history");
                    setHistory([]);

                }}
            >
                Clear
            </button>

        )}

    </div>

    {history.length === 0 ? (

        <p className="emptyHistory">
            No searches yet
        </p>

    ) : (

        history.map((item) => (

            <div
                key={item.id}
                className="historyItem"
            >

                <div
                    className="historyQuestion"
                    onClick={() => {

                        setQuestion(item.question);
                        setAnswer(item.answer);
                        setConfidence(item.confidence);
                        setSources(item.sources);
                        setSummary(item.summary);
                        setRelatedQuestions(item.relatedQuestions);

                    }}
                >

                    {item.question}

                </div>

                <button
                    className="deleteHistoryBtn"
                    onClick={(e) => {

                        e.stopPropagation();

                        const updated = history.filter(
                            h => h.id !== item.id
                        );

                        setHistory(updated);

                        localStorage.setItem(
                            "veritas-history",
                            JSON.stringify(updated)
                        );

                    }}
                >

                    ✕

                </button>

            </div>

        ))

    )}

</div>
            </div>
           <div className="sourcesCard">

  <h3>Trusted Sources</h3>

  {sources.length === 0 ? (

    <p>No sources available.</p>

  ) : (

    sources.map((source, index) => {

      const badge = getBadge(source.domain || "");

      return (

        <div className="sourceItem" key={index}>

          <div>

            

            <h4>{source.title}</h4>

            <p>{source.domain}</p>

          </div>

          <a
            href={source.url}
            target="_blank"
            rel="noreferrer"
          >
            Visit →
          </a>

        </div>

      );

    })

  )}

  {summary && (

<div className="summaryCard">

<h3>Research Summary</h3>

<div className="summaryRow">
<span>🌐 Sources Searched</span>
<span>{summary.sources_searched}</span>
</div>

<div className="summaryRow">
<span>📄 Documents Extracted</span>
<span>{summary.documents_extracted}</span>
</div>

<div className="summaryRow">
<span>🧩 Chunks Retrieved</span>
<span>{summary.chunks_retrieved}</span>
</div>

<div className="summaryRow">
<span>🤖 Inference Engine</span>
<span>{summary.engine}</span>
</div>

<div className="summaryRow">
<span>🛡 Verification</span>
<span>{summary.verification}</span>
</div>

<div className="summaryRow">
<span>⚡ Time Taken</span>
<span>{summary.time_taken}s</span>
</div>

</div>

)}
{relatedQuestions.length > 0 && (

<div className="relatedCard">

<h3>Related Questions</h3>

{relatedQuestions.map((q, index)=>(

<button

key={index}

className="relatedButton"

onClick={()=>{
    setQuestion(q);
}}

>

{q}

</button>

))}

</div>

)}

</div>

          </div>

        </>

      )}

      {!loading && !answer && (

        <div className="welcome">

          <div className="welcomeCard">

            <h2>Ready for Research</h2>

            <p>

              Ask anything related to science, medicine, technology,
              education, law or any research topic.

            </p>

            <div className="examples">

              <button
                onClick={() =>
                  setQuestion("Explain Quantum Computing")
                }
              >
                Quantum Computing
              </button>

              <button
                onClick={() =>
                  setQuestion("Latest AI in Healthcare")
                }
              >
                AI in Healthcare
              </button>

              <button
                onClick={() =>
                  setQuestion("Climate Change Research")
                }
              >
                Climate Change
              </button>

            </div>

          </div>

        </div>

      )}

      <footer>

        Powered by Ollama • ChromaDB • Sentence Transformers • DDGS • FastAPI

      </footer>

    </div>
  );
}

export default App;