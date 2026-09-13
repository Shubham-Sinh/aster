import { useState } from "react";

function FarmerGuidelines() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askGuideline = async (customQuestion = null) => {
    const q = customQuestion || question;

    if (!q.trim()) {
      setError("Please enter a question.");
      return;
    }

    setQuestion(q);
    setAnswer("");
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        `https://aster-4.onrender.com/weather-ai?question=${encodeURIComponent(q)}`
      );

      if (!response.ok) {
        throw new Error("Unable to get guideline information.");
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

  const guidelineCategories = [
    {
      icon: "🌧️",
      title: "Crop Damage",
      description: "Guidance for crops damaged by rainfall and extreme weather.",
      question:
        "What government guidelines are available for crop damage due to extreme weather?"
    },
    {
      icon: "🛡️",
      title: "Crop Insurance",
      description: "Understand government-supported crop insurance guidelines.",
      question:
        "What are the government guidelines for crop insurance?"
    },
    {
      icon: "💰",
      title: "Compensation & Claims",
      description: "Learn about crop-loss claims and compensation procedures.",
      question:
        "What guidelines are available for crop damage compensation and claims?"
    },
    {
      icon: "📋",
      title: "Government Schemes",
      description: "Explore agricultural schemes and farmer-related guidelines.",
      question:
        "What government schemes and guidelines are available for farmers?"
    }
  ];

  const guidelineQuestions = [
    "What government guidelines are available for crop damage?",
    "What should farmers do after heavy rainfall damages crops?",
    "What are the guidelines for crop insurance?",
    "What should farmers do when crops are damaged by extreme weather?"
  ];

  return (
    <div className="weather-page guidelines-page">

      {/* PAGE HEADER */}
      <div className="page-heading">
        <h1>👨‍🌾 Farmer Guidelines</h1>

        <p>
          Government-supported agricultural information for crop damage,
          insurance, compensation and weather-related risks.
        </p>
      </div>

      <div className="guidelines-container">

        {/* INTRO */}
        <div className="guidelines-intro">

          <div className="guidelines-icon">
            📋
          </div>

          <div>
            <h2>Government & Farmer Guidance</h2>

            <p>
              WeatherGPT uses a knowledge base built from government
              agricultural documents to help farmers find relevant
              information quickly.
            </p>
          </div>

        </div>

        {/* CATEGORY CARDS */}
        <div className="guideline-categories">

          <div className="guideline-section-title">
            <h2>📚 Explore Guidelines</h2>

            <p>
              Select a topic or ask your own question.
            </p>
          </div>

          <div className="guideline-category-grid">

            {guidelineCategories.map((category, index) => (

              <button
                className="guideline-category-card"
                key={index}
                onClick={() => askGuideline(category.question)}
              >

                <div className="category-icon">
                  {category.icon}
                </div>

                <div className="category-content">

                  <h3>{category.title}</h3>

                  <p>{category.description}</p>

                  <span>
                    Ask about this →
                  </span>

                </div>

              </button>

            ))}

          </div>

        </div>

        {/* SEARCH */}
        <div className="guideline-search">

          <div className="search-heading">
            <div>🤖</div>

            <div>
              <h2>Ask WeatherGPT</h2>

              <p>
                Ask a question about government guidelines or crop-related
                agricultural support.
              </p>
            </div>
          </div>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: What should I do if heavy rainfall damages my crop?"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                askGuideline();
              }
            }}
          />

          <button
            className="guideline-submit-button"
            onClick={() => askGuideline()}
            disabled={loading}
          >
            {loading ? "🔍 Searching..." : "📚 Get Guidelines"}
          </button>

        </div>

        {/* COMMON QUESTIONS */}
        <div className="guideline-topics">

          <h3>💡 Common Questions</h3>

          <div className="guideline-question-grid">

            {guidelineQuestions.map((q, index) => (

              <button
                key={index}
                onClick={() => askGuideline(q)}
              >
                <span>💬</span>
                {q}
              </button>

            ))}

          </div>

        </div>

        {/* ERROR */}
        {error && (
          <div className="guideline-error">
            ❌ {error}
          </div>
        )}

        {/* LOADING */}
        {loading && (
          <div className="guideline-loading">

            <div className="loading-book">
              📚
            </div>

            <h3>Searching Government Documents</h3>

            <p>
              WeatherGPT is finding relevant information from the
              agricultural knowledge base...
            </p>

          </div>
        )}

        {/* ANSWER */}
        {answer && !loading && (

          <div className="guideline-answer">

            <div className="guideline-answer-header">

              <div className="answer-icon">
                📖
              </div>

              <div>
                <h3>Guideline Information</h3>

                <p>
                  Answer generated from WeatherGPT's knowledge base
                </p>
              </div>

            </div>

            <div className="guideline-answer-content">
              {answer}
            </div>

            <div className="guideline-note">
              📚 This answer is based on the government-document
              knowledge base available to WeatherGPT.
            </div>

          </div>

        )}

        {/* RAG FLOW */}
        <div className="rag-info">

          <div className="rag-info-header">
            <span>🧠</span>

            <div>
              <h3>How WeatherGPT Helps</h3>

              <p>
                Your question is searched against the available
                government-document knowledge base.
              </p>
            </div>
          </div>

          <div className="rag-flow">

            <div className="rag-step">
              <span>💬</span>
              <strong>Your Question</strong>
            </div>

            <div className="rag-arrow">→</div>

            <div className="rag-step">
              <span>🔎</span>
              <strong>Document Search</strong>
            </div>

            <div className="rag-arrow">→</div>

            <div className="rag-step">
              <span>📚</span>
              <strong>Government PDFs</strong>
            </div>

            <div className="rag-arrow">→</div>

            <div className="rag-step">
              <span>🤖</span>
              <strong>AI Answer</strong>
            </div>

          </div>

        </div>

        {/* DISCLAIMER */}
        <div className="guideline-disclaimer">

          ⚠️ <strong>Important:</strong> For actual crop-loss claims,
          insurance claims, compensation and official applications,
          farmers should verify the latest requirements with the
          relevant government department or authorized official.

        </div>

      </div>

    </div>
  );
}

export default FarmerGuidelines;