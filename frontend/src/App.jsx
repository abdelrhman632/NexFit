import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

if (!API_URL) {
  console.warn(
    "VITE_API_URL is not configured. Set it in .env.local or Vercel Environment Variables."
  );
}
function App() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showBack, setShowBack] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const recognitionRef = useRef(null);
  const orbVideoRef = useRef(null);
  const finalTranscriptRef = useRef("");
  const listeningRef = useRef(false);
  const manuallyStoppedRef = useRef(false);
  const restartTimeoutRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError("Speech recognition is not supported in this browser.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "ar-EG";
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      listeningRef.current = true;
      setError("");
    };

    recognition.onresult = (event) => {
      let interimText = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const text = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalTranscriptRef.current += text + " ";
        else interimText += text;
      }
      setTranscript(`${finalTranscriptRef.current}${interimText}`.trim());
    };

    recognition.onerror = (event) => {
      if (event.error === "no-speech" || event.error === "aborted") return;
      if (event.error === "not-allowed") {
        listeningRef.current = false;
        setIsListening(false);
        setError("Microphone permission was denied.");
        return;
      }
      setError(`Speech recognition error: ${event.error}`);
    };

    recognition.onend = () => {
      if (manuallyStoppedRef.current) {
        listeningRef.current = false;
        setIsListening(false);
        const finalText = finalTranscriptRef.current.trim();
        if (finalText) searchProducts(finalText);
        return;
      }
      if (listeningRef.current) {
        clearTimeout(restartTimeoutRef.current);
        restartTimeoutRef.current = setTimeout(() => {
          try {
            recognition.start();
          } catch (restartError) {
            console.log("Recognition restart ignored:", restartError);
          }
        }, 300);
      }
    };

    recognitionRef.current = recognition;
    return () => {
      clearTimeout(restartTimeoutRef.current);
      listeningRef.current = false;
      manuallyStoppedRef.current = true;
      try { recognition.stop(); } catch {}
      recognitionRef.current = null;
    };
  }, []);

  useEffect(() => {
    const video = orbVideoRef.current;
    if (!video) return;

    if (isListening || loading) {
      video.play().catch(() => {});
    } else {
      video.pause();
    }
  }, [isListening, loading]);

  const toggleListening = () => {
    const recognition = recognitionRef.current;
    if (!recognition) {
      setError("Speech recognition is not available.");
      return;
    }
    if (listeningRef.current) {
      manuallyStoppedRef.current = true;
      listeningRef.current = false;
      clearTimeout(restartTimeoutRef.current);
      try { recognition.stop(); } catch {}
      return;
    }
    setError("");
    setProducts([]);
    setTranscript("");
    finalTranscriptRef.current = "";
    manuallyStoppedRef.current = false;
    listeningRef.current = true;
    try { recognition.start(); } catch (startError) {
      console.error("Could not start speech recognition:", startError);
    }
  };

  const searchProducts = async (query) => {
    if (!query?.trim()) return;
    setLoading(true);
    setError("");
    try {
      if (!API_URL) throw new Error("VITE_API_URL is not configured.");
      const response = await fetch(`${API_URL}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query.trim() }),
      });
      if (!response.ok) throw new Error(`Backend returned ${response.status}`);
      const data = await response.json();
      setProducts(Array.isArray(data.products) ? data.products : []);
    } catch (err) {
      console.error("Search error:", err);
      setProducts([]);
      setError("Could not connect to the NexFit AI service.");
    } finally {
      setLoading(false);
    }
  };

  const openProduct = (product) => {
    setSelectedProduct(product);
    setShowBack(false);
  };
  const closeProduct = () => {
    setSelectedProduct(null);
    setShowBack(false);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape") closeProduct();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const getImage = (product) => product?.sku ? `/products/${product.sku}.jpg` : null;
  const getBackImage = (product) => product?.sku ? `/products/${product.sku}-back.jpg` : null;
  const formatPrice = (price) => {
    if (price === null || price === undefined || price === "") return "-";
    return `${Number(price).toLocaleString()} EGP`;
  };
  const displayValue = (value, fallback = "-") =>
    value === null || value === undefined || value === "" ? fallback : value;

  // Card summary: never invent a quantity. Show exact quantity only when there
  // is one stock location; otherwise show how many branches have stock.
  const getAvailabilitySummary = (product) => {
    const branches = Array.isArray(product?.branches)
      ? product.branches.filter((branch) => Number(branch.quantity || 0) > 0)
      : [];
    if (!branches.length) return "Out of stock";
    if (branches.length === 1) return `${branches[0].quantity} available`;
    return `${branches.length} branches in stock`;
  };

  return (
    <div className="app">
      <header className="header">
        <div className="brand"><h1>NexFit</h1><p>AI Product Search</p></div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="hero-badge"><span className="status-dot" />AI-powered shopping</div>
          <h2>Tell us what<span>you're looking for.</span></h2>
          <p className="hero-description">Tell NexFit what you need. We'll search the available products for you.</p>

          <div
            className={`orb-container ${isListening || loading ? "active" : ""}`}
            style={{
              position: "relative",
              width: "155px",
              height: "155px",
              marginTop: "30px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <video
              ref={orbVideoRef}
              className="nexfit-orb"
              src="/nexfit-orb.webm"
              muted
              playsInline
              preload="auto"
              style={{
                position: "absolute",
                inset: "0",
                width: "155px",
                height: "155px",
                objectFit: "contain",
                pointerEvents: "none",
                zIndex: 1,
              }}
            />

            <button
              className={`mic-button ${isListening ? "listening" : ""}`}
              onClick={toggleListening}
              aria-label={isListening ? "Stop listening" : "Start voice search"}
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                width: "68px",
                height: "68px",
                margin: 0,
                transform: "translate(-50%, -50%)",
                zIndex: 2,
              }}
            >
              <div className="mic-glow" />
              <div className="mic-icon">{isListening ? <span className="stop-icon">■</span> : <span className="microphone-icon">🎙</span>}</div>
            </button>
          </div>

          <p className={`mic-status ${isListening ? "active" : ""}`}>
            {isListening ? "Listening... Take your time. Press the microphone when you're finished." : "Tap the microphone and tell us what you need"}
          </p>

          {transcript && <div className="transcript-box"><span className="transcript-label">TRANSCRIPT</span><p>{transcript}</p></div>}
          {error && <div className="error-box">{error}</div>}
        </section>

        {loading && <section className="loading-section"><div className="spinner" /><p>Searching available products...</p></section>}

        {!loading && products.length > 0 && (
          <section className="results-section">
            <div className="results-header"><div><span className="section-label">SEARCH RESULTS</span><h3>{products.length} products found</h3></div></div>
            <div className="products-grid">
              {products.map((product) => {
                const image = getImage(product);
                return (
                  <article className="product-card" key={product.productid ?? product.sku} onClick={() => openProduct(product)}>
                    <div className="card-image">
                      {image ? <img src={image} alt={product.productname} onError={(event) => {
                        event.currentTarget.style.display = "none";
                        event.currentTarget.parentElement.classList.add("image-missing");
                      }} /> : <div className="image-placeholder"><span>{product.productbrand}</span><small>No image</small></div>}
                      <div className="card-view">View details →</div>
                    </div>
                    <div className="card-content">
                      <span className="card-brand">{product.productbrand}</span>
                      <h4>{product.productname}</h4>
                      <p className="card-model">{product.productmodel}</p>
                      <div className="card-price">{formatPrice(product.productprice)}</div>
                      <div className="card-tags"><span>Size {displayValue(product.productsize)}</span><span>{displayValue(product.productcategory)}</span></div>
                      <div className="card-footer"><span>{displayValue(product.productusage)}</span><span className="availability">● {getAvailabilitySummary(product)}</span></div>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        )}

        {!loading && transcript && products.length === 0 && !error && (
          <section className="no-results"><div className="no-results-icon">🔎</div><h3>No products found</h3><p>Try describing what you need differently.</p></section>
        )}
      </main>

      {selectedProduct && (
        <div className="modal-overlay" onClick={closeProduct}>
          <div className="product-modal" onClick={(event) => event.stopPropagation()}>
            <button className="modal-close" onClick={closeProduct} aria-label="Close">×</button>
            <div className="modal-layout">
              <div className="modal-image-section">
                <div className={`product-image-viewer ${showBack ? "show-back" : ""}`}>
                  <div className="image-face front"><img src={getImage(selectedProduct)} alt={selectedProduct.productname} onError={(event) => { event.currentTarget.style.display = "none"; }} /></div>
                  <div className="image-face back"><img src={getBackImage(selectedProduct)} alt={`${selectedProduct.productname} back`} onError={(event) => { event.currentTarget.style.display = "none"; }} /></div>
                </div>
                <button className="flip-button" onClick={() => setShowBack(!showBack)}>{showBack ? "Show Front" : "Show Back"}</button>
              </div>

              <div className="modal-details">
                <div className="product-detail-header">
                  <span className="product-detail-brand">{selectedProduct.productbrand}</span>
                  <h2>{selectedProduct.productname}</h2>
                  <p className="product-detail-model">{selectedProduct.productmodel}</p>
                  <div className="product-detail-price">{formatPrice(selectedProduct.productprice)}</div>
                </div>

                <div className="spec-section">
                  <h3>Specifications</h3>
                  <div className="product-specs">
                    <Spec label="Size" value={displayValue(selectedProduct.productsize)} />
                    <Spec label="Weight" value={selectedProduct.weight != null ? `${selectedProduct.weight} g` : "-"} />
                    <Spec label="Material" value={displayValue(selectedProduct.material)} />
                    <Spec label="Cushioning" value={displayValue(selectedProduct.cushioning)} />
                    <Spec label="Support" value={displayValue(selectedProduct.supporttype)} />
                    <Spec label="Breathability" value={displayValue(selectedProduct.breathability)} />
                    <Spec label="Surface" value={displayValue(selectedProduct.surface)} />
                    <Spec label="Terrain" value={displayValue(selectedProduct.terrain)} />
                    <Spec label="Foot Strike" value={displayValue(selectedProduct.footstrike)} />
                    <Spec label="Energy Return" value={displayValue(selectedProduct.energyreturn)} />
                    <Spec label="Heel Drop" value={selectedProduct.heeldropmm != null ? `${selectedProduct.heeldropmm} mm` : "-"} />
                    <Spec label="Distance" value={displayValue(selectedProduct.recommendeddistance)} />
                    <Spec label="Arch Type" value={displayValue(selectedProduct.archtype)} />
                    <Spec label="Waterproof" value={selectedProduct.waterproof == null ? "-" : selectedProduct.waterproof ? "Yes" : "No"} />
                    <Spec label="Release Year" value={displayValue(selectedProduct.releaseyear)} />
                  </div>
                </div>

                {selectedProduct.description && <div className="product-description"><h3>Description</h3><p>{selectedProduct.description}</p></div>}

                <div className="branches-section">
                  <h3>Available at</h3>
                  <div className="branches-list">
                    {Array.isArray(selectedProduct.branches) && selectedProduct.branches.filter((branch) => Number(branch.quantity || 0) > 0).map((branch, index) => (
                      <div className="branch-item" key={`${branch.branchname}-${branch.city}-${index}`}>
                        <div><strong>{branch.branchname}</strong><span>{branch.city}</span></div>
                        <span className="branch-quantity">{branch.quantity} available</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Spec({ label, value }) {
  return <div className="spec-item"><span className="spec-label">{label}</span><span className="spec-value">{value}</span></div>;
}

export default App;