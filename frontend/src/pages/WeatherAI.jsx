import { useState } from "react";

function WeatherAI() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askAI = async (customQuestion = null) => {
    const q = customQuestion || question;

    if (!q.trim()) {
      setError("Please enter a question.");
      return;
    }

    setQuestion(q);
    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/weather-ai?question=${encodeURIComponent(q)}`
      );

      if (!response.ok) {
        throw new Error("AI server could not process the question.");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What government guidelines are available for crop damage?",
    "What should farmers do during heavy rainfall?",
    "What are the guidelines for crop insurance?",
    "How can farmers protect crops from extreme weather?"
  ];

  return (
    <div className="weather-page ai-page">

      <div className="page-heading">
        <h1>🤖 WeatherGPT AI</h1>
        <p>
          Ask questions about weather, farming, government guidelines and
          agricultural risks.
        </p>
      </div>

      <div className="ai-container">

        <div className="ai-intro">
          <div className="ai-big-icon">🤖</div>

          <div>
            <h2>Ask WeatherGPT</h2>
            <p>
              Your AI assistant for weather and farmer-related information.
            </p>
          </div>
        </div>

        <div className="ai-search">

          <textarea
            placeholder="Ask something like: What should I do if my crop is damaged by heavy rain?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                askAI();
              }
            }}
          />

          <button onClick={() => askAI()} disabled={loading}>
            {loading ? "🤔 Thinking..." : "🚀 Ask AI"}
          </button>

        </div>

        <div className="suggested-section">
          <h3>💡 Suggested Questions</h3>

          <div className="suggested-grid">
            {suggestedQuestions.map((q, index) => (
              <button
                key={index}
                onClick={() => askAI(q)}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="ai-error">
            ❌ {error}
          </div>
        )}

        {loading && (
          <div className="ai-loading">
            <div className="loading-icon">🤖</div>
            <p>WeatherGPT is analyzing your question...</p>
          </div>
        )}

        {answer && !loading && (
          <div className="ai-answer">

            <div className="answer-header">
              <span>🤖</span>
              <h3>WeatherGPT Answer</h3>
            </div>

            <div className="answer-content">
              {answer}
            </div>

            <div className="answer-note">
              📚 Answer generated using WeatherGPT's available weather
              tools and government-document knowledge base.
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default WeatherAI;