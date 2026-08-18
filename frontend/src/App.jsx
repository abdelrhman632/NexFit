import { useRef, useState } from "react";
import "./App.css";

/* =========================================================
   PRODUCT MODAL
   ========================================================= */

function ProductModal({ product, onClose }) {
  const [showBack, setShowBack] = useState(false);

  const frontImage = `/products/${product.sku}.jpg`;
  const backImage = `/products/${product.sku}-back.jpg`;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="product-modal"
        onClick={(event) => event.stopPropagation()}
      >
        {/* CLOSE */}

        <button
          className="modal-close"
          onClick={onClose}
        >
          ×
        </button>

        {/* =================================================
            IMAGE
            ================================================= */}

        <div className="modal-image-container">
          <div
            className={`shoe-flipper ${
              showBack ? "flipped" : ""
            }`}
          >
            {/* FRONT */}

            <div className="shoe-face">
              <img
                src={frontImage}
                alt={product.productname}
                onError={(event) => {
                  event.currentTarget.style.display =
                    "none";
                }}
              />
            </div>

            {/* BACK */}

            <div className="shoe-back">
              <img
                src={backImage}
                alt={`${product.productname} back`}
                onError={(event) => {
                  event.currentTarget.style.display =
                    "none";
                }}
              />
            </div>
          </div>
        </div>

        {/* FLIP */}

        <button
          className="flip-button"
          onClick={() =>
            setShowBack((current) => !current)
          }
        >
          {showBack ? "Show Front" : "Show Back"}
        </button>

        {/* =================================================
            PRODUCT INFORMATION
            ================================================= */}

        <div className="modal-content">
          <p className="modal-brand">
            {product.productbrand}
          </p>

          <h2>{product.productname}</h2>

          <p className="modal-model">
            {product.productmodel}
          </p>

          <div className="modal-price">
            {Number(
              product.productprice
            ).toLocaleString()}

            <span> EGP</span>
          </div>

          {/* =================================================
              SPECIFICATIONS
              ================================================= */}

          <div className="spec-grid">
            <Spec
              label="Size"
              value={product.productsize}
            />

            <Spec
              label="Weight"
              value={
                product.weight != null
                  ? `${product.weight} g`
                  : "-"
              }
            />

            <Spec
              label="Material"
              value={product.material}
            />

            <Spec
              label="Cushioning"
              value={product.cushioning}
            />

            <Spec
              label="Support"
              value={product.supporttype}
            />

            <Spec
              label="Breathability"
              value={product.breathability}
            />

            <Spec
              label="Surface"
              value={product.surface}
            />

            <Spec
              label="Terrain"
              value={product.terrain}
            />

            <Spec
              label="Foot Strike"
              value={product.footstrike}
            />

            <Spec
              label="Energy Return"
              value={product.energyreturn}
            />

            <Spec
              label="Heel Drop"
              value={
                product.heeldropmm != null
                  ? `${product.heeldropmm} mm`
                  : "-"
              }
            />

            <Spec
              label="Distance"
              value={
                product.recommendeddistance
              }
            />

            <Spec
              label="Arch Type"
              value={product.archtype}
            />

            <Spec
              label="Waterproof"
              value={
                product.waterproof === true
                  ? "Yes"
                  : product.waterproof === false
                    ? "No"
                    : "-"
              }
            />

            <Spec
              label="Release Year"
              value={product.releaseyear}
            />
          </div>

          {/* =================================================
              DESCRIPTION
              ================================================= */}

          {product.description && (
            <div className="modal-description">
              <h3>Description</h3>

              <p>
                {product.description}
              </p>
            </div>
          )}

          {/* =================================================
              BRANCHES
              ================================================= */}

          {product.branches?.length > 0 && (
            <div className="modal-branches">
              <h3>Available at</h3>

              {product.branches.map(
                (branch, index) => (
                  <div
                    className="modal-branch"
                    key={index}
                  >
                    <span>
                      {branch.branchname}
                    </span>

                    <strong>
                      {branch.quantity} available
                    </strong>
                  </div>
                )
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


/* =========================================================
   SPECIFICATION COMPONENT
   ========================================================= */

function Spec({ label, value }) {
  return (
    <div className="spec">
      <span>{label}</span>

      <strong>
        {value ?? "-"}
      </strong>
    </div>
  );
}


/* =========================================================
   MAIN APP
   ========================================================= */

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState("");
  const [selectedProduct, setSelectedProduct] =
    useState(null);

  const recognitionRef = useRef(null);
  const transcriptRef = useRef("");


  /* =======================================================
     START STT
     ======================================================= */

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(
        "Speech recognition is not supported in this browser."
      );

      return;
    }

    setError("");
    setProducts([]);
    setSelectedProduct(null);

    const recognition =
      new SpeechRecognition();

    recognition.lang = "ar-EG";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognitionRef.current = recognition;
    transcriptRef.current = "";

    recognition.onstart = () => {
      console.log("STT started");

      setListening(true);
    };

    recognition.onresult = (event) => {
      let finalTranscript = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        const transcript =
          event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        }
      }

      if (finalTranscript) {
        transcriptRef.current +=
          " " + finalTranscript;

        console.log(
          "Transcript:",
          transcriptRef.current
        );
      }
    };

    recognition.onerror = (event) => {
      console.error(
        "STT error:",
        event.error
      );

      if (event.error !== "no-speech") {
        setError(
          `Speech recognition error: ${event.error}`
        );
      }
    };

    recognition.onend = () => {
      console.log("STT ended");

      setListening(false);

      const transcript =
        transcriptRef.current.trim();

      console.log(
        "FINAL TRANSCRIPT:",
        transcript
      );

      recognitionRef.current = null;

      if (transcript) {
        searchProducts(transcript);
      }
    };

    recognition.start();
  };


  /* =======================================================
     STOP STT
     ======================================================= */

  const stopListening = () => {
    if (!recognitionRef.current) {
      return;
    }

    console.log("Stopping STT...");

    recognitionRef.current.stop();
  };


  /* =======================================================
     MICROPHONE
     ======================================================= */

  const toggleListening = () => {
    if (listening) {
      stopListening();
    } else {
      startListening();
    }
  };


  /* =======================================================
     SEARCH BACKEND
     ======================================================= */

  const searchProducts = async (voiceQuery) => {
    if (!voiceQuery?.trim()) {
      return;
    }

    console.log(
      "Sending query to backend:",
      voiceQuery
    );

    setLoading(true);
    setError("");
    setProducts([]);
    setSelectedProduct(null);

    try {
      const response = await fetch(
        "http://localhost:8000/api/search",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            query: voiceQuery,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Search request failed: ${response.status}`
        );
      }

      const data =
        await response.json();

      console.log(
        "API RESPONSE:",
        data
      );

      setProducts(
        data.products || []
      );

    } catch (err) {
      console.error(err);

      setError(
        err.message ||
        "Something went wrong while searching."
      );

    } finally {
      setLoading(false);
    }
  };


  /* =======================================================
     PRODUCT IMAGE
     ======================================================= */

  const getProductImage = (product) => {
    if (!product?.sku) {
      return null;
    }

    return `/products/${product.sku}.jpg`;
  };


  /* =======================================================
     RENDER
     ======================================================= */

  return (
    <div className="app">

      {/* =================================================
          HEADER
          ================================================= */}

      <header className="header">
        <div className="brand-container">
          <h1>NexFit</h1>

          <p>
            AI Product Search
          </p>
        </div>
      </header>


      {/* =================================================
          MAIN
          ================================================= */}

      <main className="main">

        {/* =================================================
            VOICE SEARCH
            ================================================= */}

        <section className="voice-section">

          <div className="hero-glow"></div>

          <p className="eyebrow">
            AI-POWERED SHOPPING
          </p>

          <h2>
            What are you looking for?
          </h2>

          <p className="voice-description">
            Tell NexFit what you need and
            we'll find the available
            products for you.
          </p>

          <button
            className={`voice-button ${
              listening
                ? "listening"
                : ""
            }`}
            onClick={toggleListening}
            disabled={loading}
            aria-label={
              listening
                ? "Stop listening"
                : "Start voice search"
            }
          >
            <span className="mic-icon">
              {listening
                ? "■"
                : "🎙️"}
            </span>
          </button>

          <p className="voice-status">
            {listening
              ? "Listening..."
              : loading
                ? "Finding products..."
                : "Tap the microphone and tell us what you need."}
          </p>

        </section>


        {/* =================================================
            ERROR
            ================================================= */}

        {error && (
          <div className="error">
            {error}
          </div>
        )}


        {/* =================================================
            LOADING
            ================================================= */}

        {loading && (
          <section className="loading-container">

            <div className="loading-spinner"></div>

            <p>
              Searching NexFit...
            </p>

          </section>
        )}


        {/* =================================================
            RESULTS
            ================================================= */}

        {!loading &&
          products.length > 0 && (

            <section className="results-section">

              <div className="results-header">

                <div>

                  <p className="results-eyebrow">
                    MATCHES FOUND
                  </p>

                  <h2>
                    Search Results
                  </h2>

                </div>

                <span className="result-count">
                  {products.length} products
                </span>

              </div>


              <div className="product-grid">

                {products.map(
                  (product) => {

                    const image =
                      getProductImage(
                        product
                      );

                    return (
                      <article
                        className="product-card"
                        key={
                          product.productid
                        }
                        onClick={() =>
                          setSelectedProduct(
                            product
                          )
                        }
                      >

                        {/* IMAGE */}

                        <div className="product-image">

                          {image ? (

                            <img
                              src={image}
                              alt={
                                product.productname
                              }
                              onError={(
                                event
                              ) => {
                                event.currentTarget.style.display =
                                  "none";
                              }}
                            />

                          ) : (

                            <div className="image-placeholder">
                              {product.productbrand}
                            </div>

                          )}

                        </div>


                        {/* INFORMATION */}

                        <div className="product-info">

                          <p className="product-brand">
                            {product.productbrand}
                          </p>

                          <h3>
                            {product.productname}
                          </h3>

                          <p className="product-model">
                            {product.productmodel}
                          </p>

                          <div className="price">

                            {Number(
                              product.productprice
                            ).toLocaleString()}

                            <span>
                              EGP
                            </span>

                          </div>

                          <div className="product-details">

                            <div>
                              <span>
                                Size
                              </span>

                              <strong>
                                {
                                  product.productsize
                                }
                              </strong>
                            </div>

                            <div>
                              <span>
                                Category
                              </span>

                              <strong>
                                {
                                  product.productcategory
                                }
                              </strong>
                            </div>

                            <div>
                              <span>
                                Usage
                              </span>

                              <strong>
                                {
                                  product.productusage
                                }
                              </strong>
                            </div>

                          </div>


                          {/* BRANCHES */}

                          {product.branches?.length >
                            0 && (

                              <div className="branches">

                                <div className="availability-title">

                                  <span className="availability-dot"></span>

                                  Available at

                                </div>

                                {product.branches.map(
                                  (
                                    branch,
                                    index
                                  ) => (

                                    <div
                                      className="branch"
                                      key={
                                        index
                                      }
                                    >

                                      <span>
                                        {
                                          branch.branchname
                                        }
                                      </span>

                                      <span>
                                        {
                                          branch.quantity
                                        }{" "}
                                        available
                                      </span>

                                    </div>

                                  )
                                )}

                              </div>

                            )}

                        </div>

                      </article>
                    );
                  }
                )}

              </div>

            </section>
          )}


        {/* =================================================
            EMPTY STATE
            ================================================= */}

        {!loading &&
          !error &&
          products.length === 0 && (

            <section className="empty-state">

              <div className="empty-icon">
                🎙️
              </div>

              <h3>
                Start your search
              </h3>

              <p>
                Tell NexFit what you're
                looking for.
              </p>

            </section>
          )}

      </main>


      {/* =================================================
          PRODUCT MODAL
          ================================================= */}

      {selectedProduct && (
        <ProductModal
          product={selectedProduct}
          onClose={() =>
            setSelectedProduct(null)
          }
        />
      )}

    </div>
  );
}

export default App;