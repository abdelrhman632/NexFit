import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // =========================================================
  // STATE
  // =========================================================

  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showBack, setShowBack] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // =========================================================
  // SPEECH RECOGNITION REFS
  // IMPORTANT: ONLY ONE COPY OF THESE
  // =========================================================

  const recognitionRef = useRef(null);
  const finalTranscriptRef = useRef("");
  const listeningRef = useRef(false);
  const manuallyStoppedRef = useRef(false);
  const restartTimeoutRef = useRef(null);

  // =========================================================
  // SPEECH RECOGNITION
  // =========================================================

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(
        "Speech recognition is not supported in this browser."
      );

      return;
    }

    const recognition = new SpeechRecognition();

    // Arabic/Egyptian speech
    recognition.lang = "ar-EG";

    /*
     * IMPORTANT
     *
     * continuous = true means we want a long
     * conversation instead of a single phrase.
     *
     * Chrome can still terminate recognition
     * after silence, so onend() below restarts it.
     */
    recognition.continuous = true;

    recognition.interimResults = true;

    recognition.maxAlternatives = 1;

    // =======================================================
    // START
    // =======================================================

    recognition.onstart = () => {
      console.log(
        "Speech recognition started"
      );

      setIsListening(true);

      listeningRef.current = true;

      setError("");
    };

    // =======================================================
    // RESULT
    // =======================================================

    recognition.onresult = (event) => {
      let interimText = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        const text =
          event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          /*
           * Keep previous final speech.
           *
           * Example:
           *
           * "عايز جزمة"
           *
           * then:
           *
           * "مشي"
           *
           * becomes:
           *
           * "عايز جزمة مشي"
           */

          finalTranscriptRef.current +=
            text + " ";
        } else {
          interimText += text;
        }
      }

      const combined =
        finalTranscriptRef.current +
        interimText;

      setTranscript(
        combined.trim()
      );

      console.log(
        "TRANSCRIPT:",
        combined.trim()
      );
    };

    // =======================================================
    // ERROR
    // =======================================================

    recognition.onerror = (event) => {
      console.error(
        "Speech recognition error:",
        event.error
      );

      /*
       * These are not fatal.
       *
       * Chrome can generate these while we are
       * trying to maintain continuous recognition.
       */

      if (
        event.error === "no-speech" ||
        event.error === "aborted"
      ) {
        return;
      }

      if (
        event.error === "not-allowed"
      ) {
        listeningRef.current = false;

        setIsListening(false);

        setError(
          "Microphone permission was denied."
        );

        return;
      }

      setError(
        `Speech recognition error: ${event.error}`
      );
    };

    // =======================================================
    // END
    // =======================================================

    recognition.onend = () => {
      console.log(
        "Speech recognition ended"
      );

      /*
       * CASE 1:
       *
       * The USER pressed the microphone button
       * to stop.
       *
       * In this case we send the transcript
       * to the backend.
       */

      if (
        manuallyStoppedRef.current
      ) {
        console.log(
          "Recognition stopped manually."
        );

        listeningRef.current = false;

        setIsListening(false);

        const finalText =
          finalTranscriptRef.current.trim();

        if (finalText) {
          searchProducts(finalText);
        }

        return;
      }

      /*
       * CASE 2:
       *
       * Chrome stopped recognition automatically
       * because of silence.
       *
       * DO NOT search.
       *
       * Restart recognition instead.
       */

      if (listeningRef.current) {
        console.log(
          "Browser ended recognition. Restarting..."
        );

        clearTimeout(
          restartTimeoutRef.current
        );

        restartTimeoutRef.current =
          setTimeout(() => {
            try {
              recognition.start();

              console.log(
                "Speech recognition restarted."
              );
            } catch (restartError) {
              /*
               * Chrome sometimes says recognition
               * is already running.
               *
               * This is safe to ignore.
               */

              console.log(
                "Recognition restart ignored:",
                restartError
              );
            }
          }, 300);
      }
    };

    // =======================================================
    // SAVE RECOGNITION INSTANCE
    // =======================================================

    recognitionRef.current =
      recognition;

    // =======================================================
    // CLEANUP
    // =======================================================

    return () => {
      clearTimeout(
        restartTimeoutRef.current
      );

      listeningRef.current = false;

      manuallyStoppedRef.current = true;

      try {
        recognition.stop();
      } catch {
        // Ignore cleanup errors.
      }

      recognitionRef.current = null;
    };
  }, []);

  // =========================================================
  // MICROPHONE
  // =========================================================

  const toggleListening = () => {
    const recognition =
      recognitionRef.current;

    if (!recognition) {
      setError(
        "Speech recognition is not available."
      );

      return;
    }

    // =======================================================
    // STOP
    // =======================================================

    if (listeningRef.current) {
      console.log(
        "User stopped listening."
      );

      /*
       * Tell onend() that this was intentional.
       */

      manuallyStoppedRef.current =
        true;

      listeningRef.current = false;

      clearTimeout(
        restartTimeoutRef.current
      );

      try {
        recognition.stop();
      } catch {
        // Recognition may already have stopped.
      }

      return;
    }

    // =======================================================
    // START
    // =======================================================

    console.log(
      "Starting voice search..."
    );

    setError("");

    setProducts([]);

    setTranscript("");

    finalTranscriptRef.current = "";

    manuallyStoppedRef.current =
      false;

    listeningRef.current = true;

    try {
      recognition.start();
    } catch (error) {
      console.error(
        "Could not start speech recognition:",
        error
      );
    }
  };

  // =========================================================
  // SEARCH BACKEND
  // =========================================================

  const searchProducts = async (query) => {
    if (!query?.trim()) {
      return;
    }

    console.log(
      "Sending query to backend:",
      query
    );

    setLoading(true);

    setError("");

    try {
      /*
       * IMPORTANT:
       *
       * Backend endpoint:
       *
       * POST /api/search
       */

      const response = await fetch(
        `${API_URL}/api/search`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            query: query.trim(),
          }),
        }
      );

      console.log(
        "Backend status:",
        response.status
      );

      if (!response.ok) {
        throw new Error(
          `Backend returned ${response.status}`
        );
      }

      const data =
        await response.json();

      console.log(
        "API RESPONSE:",
        data
      );

      setProducts(
        Array.isArray(data.products)
          ? data.products
          : []
      );
    } catch (err) {
      console.error(
        "Search error:",
        err
      );

      setProducts([]);

      setError(
        "Could not connect to the NexFit AI service."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // PRODUCT MODAL
  // =========================================================

  const openProduct = (product) => {
    setSelectedProduct(product);

    setShowBack(false);
  };

  const closeProduct = () => {
    setSelectedProduct(null);

    setShowBack(false);
  };

  // =========================================================
  // ESCAPE KEY
  // =========================================================

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        closeProduct();
      }
    };

    window.addEventListener(
      "keydown",
      handleKeyDown
    );

    return () => {
      window.removeEventListener(
        "keydown",
        handleKeyDown
      );
    };
  }, []);

  // =========================================================
  // HELPERS
  // =========================================================

  const getImage = (product) => {
    if (!product?.sku) {
      return null;
    }

    return `/products/${product.sku}.jpg`;
  };

  const getBackImage = (product) => {
    if (!product?.sku) {
      return null;
    }

    return `/products/${product.sku}-back.jpg`;
  };

  const formatPrice = (price) => {
    if (
      price === null ||
      price === undefined ||
      price === ""
    ) {
      return "-";
    }

    return `${Number(
      price
    ).toLocaleString()} EGP`;
  };

  const displayValue = (
    value,
    fallback = "-"
  ) => {
    if (
      value === null ||
      value === undefined ||
      value === ""
    ) {
      return fallback;
    }

    return value;
  };

  const getTotalQuantity = (
    product
  ) => {
    if (
      !Array.isArray(
        product?.branches
      )
    ) {
      return 0;
    }

    return product.branches.reduce(
      (total, branch) =>
        total +
        Number(
          branch.quantity || 0
        ),
      0
    );
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="app">

      {/* ===================================================
          HEADER
          =================================================== */}

      <header className="header">

        <div className="brand">

          <h1>
            NexFit
          </h1>

          <p>
            AI Product Search
          </p>

        </div>

      </header>

      {/* ===================================================
          MAIN
          =================================================== */}

      <main className="main">

        {/* =================================================
            HERO
            ================================================= */}

        <section className="hero">

          <div className="hero-badge">

            <span className="status-dot" />

            AI-powered shopping

          </div>

          <h2>

            Tell us what

            <span>
              you're looking for.
            </span>

          </h2>

          <p className="hero-description">

            Tell NexFit what you need.
            We'll search the available
            products for you.

          </p>

          {/* ===============================================
              MICROPHONE
              =============================================== */}

          <button
            className={`mic-button ${
              isListening
                ? "listening"
                : ""
            }`}
            onClick={
              toggleListening
            }
            aria-label={
              isListening
                ? "Stop listening"
                : "Start voice search"
            }
          >

            <div className="mic-glow" />

            <div className="mic-icon">

              {isListening ? (
                <span className="stop-icon">
                  ■
                </span>
              ) : (
                <span className="microphone-icon">
                  🎙
                </span>
              )}

            </div>

          </button>

          <p
            className={`mic-status ${
              isListening
                ? "active"
                : ""
            }`}
          >

            {isListening
              ? "Listening... Take your time. Press the microphone when you're finished."
              : "Tap the microphone and tell us what you need"}

          </p>

          {/* ===============================================
              TRANSCRIPT DEBUG
              =============================================== */}

          {transcript && (
            <div className="transcript-box">

              <span className="transcript-label">
                TRANSCRIPT
              </span>

              <p>
                {transcript}
              </p>

            </div>
          )}

          {/* ===============================================
              ERROR
              =============================================== */}

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

        </section>

        {/* =================================================
            LOADING
            ================================================= */}

        {loading && (
          <section className="loading-section">

            <div className="spinner" />

            <p>
              Searching available products...
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

                  <span className="section-label">
                    SEARCH RESULTS
                  </span>

                  <h3>
                    {products.length}{" "}
                    products found
                  </h3>

                </div>

              </div>

              <div className="products-grid">

                {products.map(
                  (product) => {

                    const image =
                      getImage(
                        product
                      );

                    return (
                      <article
                        className="product-card"
                        key={
                          product.productid ??
                          product.sku
                        }
                        onClick={() =>
                          openProduct(
                            product
                          )
                        }
                      >

                        {/* IMAGE */}

                        <div className="card-image">

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

                                event.currentTarget.parentElement.classList.add(
                                  "image-missing"
                                );
                              }}
                            />
                          ) : (
                            <div className="image-placeholder">

                              <span>
                                {
                                  product.productbrand
                                }
                              </span>

                              <small>
                                No image
                              </small>

                            </div>
                          )}

                          <div className="card-view">
                            View details →
                          </div>

                        </div>

                        {/* CONTENT */}

                        <div className="card-content">

                          <span className="card-brand">
                            {
                              product.productbrand
                            }
                          </span>

                          <h4>
                            {
                              product.productname
                            }
                          </h4>

                          <p className="card-model">
                            {
                              product.productmodel
                            }
                          </p>

                          <div className="card-price">
                            {formatPrice(
                              product.productprice
                            )}
                          </div>

                          <div className="card-tags">

                            <span>
                              Size{" "}
                              {displayValue(
                                product.productsize
                              )}
                            </span>

                            <span>
                              {displayValue(
                                product.productcategory
                              )}
                            </span>

                          </div>

                          <div className="card-footer">

                            <span>
                              {displayValue(
                                product.productusage
                              )}
                            </span>

                            <span className="availability">
                              ●{" "}
                              {
                                getTotalQuantity(
                                  product
                                )
                              }{" "}
                              available
                            </span>

                          </div>

                        </div>

                      </article>
                    );
                  }
                )}

              </div>

            </section>
          )}

        {/* =================================================
            NO RESULTS
            ================================================= */}

        {!loading &&
          transcript &&
          products.length === 0 &&
          !error && (
            <section className="no-results">

              <div className="no-results-icon">
                🔎
              </div>

              <h3>
                No products found
              </h3>

              <p>
                Try describing what you need differently.
              </p>

            </section>
          )}

      </main>

      {/* =====================================================
          PRODUCT MODAL
          ===================================================== */}

      {selectedProduct && (
        <div
          className="modal-overlay"
          onClick={
            closeProduct
          }
        >

          <div
            className="product-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            {/* CLOSE */}

            <button
              className="modal-close"
              onClick={
                closeProduct
              }
              aria-label="Close"
            >
              ×
            </button>

            <div className="modal-layout">

              {/* =============================================
                  IMAGE
                  ============================================= */}

              <div className="modal-image-section">

                <div
                  className={`product-image-viewer ${
                    showBack
                      ? "show-back"
                      : ""
                  }`}
                >

                  {/* FRONT */}

                  <div className="image-face front">

                    <img
                      src={getImage(
                        selectedProduct
                      )}
                      alt={
                        selectedProduct.productname
                      }
                      onError={(
                        event
                      ) => {
                        event.currentTarget.style.display =
                          "none";
                      }}
                    />

                  </div>

                  {/* BACK */}

                  <div className="image-face back">

                    <img
                      src={getBackImage(
                        selectedProduct
                      )}
                      alt={`${selectedProduct.productname} back`}
                      onError={(
                        event
                      ) => {
                        event.currentTarget.style.display =
                          "none";
                      }}
                    />

                  </div>

                </div>

                <button
                  className="flip-button"
                  onClick={() =>
                    setShowBack(
                      !showBack
                    )
                  }
                >
                  {showBack
                    ? "Show Front"
                    : "Show Back"}
                </button>

              </div>

              {/* =============================================
                  DETAILS
                  ============================================= */}

              <div className="modal-details">

                <div className="product-detail-header">

                  <span className="product-detail-brand">
                    {
                      selectedProduct.productbrand
                    }
                  </span>

                  <h2>
                    {
                      selectedProduct.productname
                    }
                  </h2>

                  <p className="product-detail-model">
                    {
                      selectedProduct.productmodel
                    }
                  </p>

                  <div className="product-detail-price">
                    {formatPrice(
                      selectedProduct.productprice
                    )}
                  </div>

                </div>

                {/* =========================================
                    SPECIFICATIONS
                    ========================================= */}

                <div className="spec-section">

                  <h3>
                    Specifications
                  </h3>

                  <div className="product-specs">

                    <Spec
                      label="Size"
                      value={displayValue(
                        selectedProduct.productsize
                      )}
                    />

                    <Spec
                      label="Weight"
                      value={
                        selectedProduct.weight !==
                          null &&
                        selectedProduct.weight !==
                          undefined
                          ? `${selectedProduct.weight} g`
                          : "-"
                      }
                    />

                    <Spec
                      label="Material"
                      value={displayValue(
                        selectedProduct.material
                      )}
                    />

                    <Spec
                      label="Cushioning"
                      value={displayValue(
                        selectedProduct.cushioning
                      )}
                    />

                    <Spec
                      label="Support"
                      value={displayValue(
                        selectedProduct.supporttype
                      )}
                    />

                    <Spec
                      label="Breathability"
                      value={displayValue(
                        selectedProduct.breathability
                      )}
                    />

                    <Spec
                      label="Surface"
                      value={displayValue(
                        selectedProduct.surface
                      )}
                    />

                    <Spec
                      label="Terrain"
                      value={displayValue(
                        selectedProduct.terrain
                      )}
                    />

                    <Spec
                      label="Foot Strike"
                      value={displayValue(
                        selectedProduct.footstrike
                      )}
                    />

                    <Spec
                      label="Energy Return"
                      value={displayValue(
                        selectedProduct.energyreturn
                      )}
                    />

                    <Spec
                      label="Heel Drop"
                      value={
                        selectedProduct.heeldropmm !==
                          null &&
                        selectedProduct.heeldropmm !==
                          undefined
                          ? `${selectedProduct.heeldropmm} mm`
                          : "-"
                      }
                    />

                    <Spec
                      label="Distance"
                      value={displayValue(
                        selectedProduct.recommendeddistance
                      )}
                    />

                    <Spec
                      label="Arch Type"
                      value={displayValue(
                        selectedProduct.archtype
                      )}
                    />

                    <Spec
                      label="Waterproof"
                      value={
                        selectedProduct.waterproof ===
                          null ||
                        selectedProduct.waterproof ===
                          undefined
                          ? "-"
                          : selectedProduct.waterproof
                            ? "Yes"
                            : "No"
                      }
                    />

                    <Spec
                      label="Release Year"
                      value={displayValue(
                        selectedProduct.releaseyear
                      )}
                    />

                  </div>

                </div>

                {/* =========================================
                    DESCRIPTION
                    ========================================= */}

                {selectedProduct.description && (
                  <div className="product-description">

                    <h3>
                      Description
                    </h3>

                    <p>
                      {
                        selectedProduct.description
                      }
                    </p>

                  </div>
                )}

                {/* =========================================
                    BRANCHES
                    ========================================= */}

                <div className="branches-section">

                  <h3>
                    Available at
                  </h3>

                  <div className="branches-list">

                    {Array.isArray(
                      selectedProduct.branches
                    ) &&
                      selectedProduct.branches
                        .filter(
                          (
                            branch,
                            index,
                            array
                          ) =>
                            index ===
                            array.findIndex(
                              (
                                item
                              ) =>
                                item.branchname ===
                                  branch.branchname &&
                                item.city ===
                                  branch.city
                            )
                        )
                        .map(
                          (
                            branch,
                            index
                          ) => (
                            <div
                              className="branch-item"
                              key={`${branch.branchname}-${branch.city}-${index}`}
                            >

                              <div>

                                <strong>
                                  {
                                    branch.branchname
                                  }
                                </strong>

                                <span>
                                  {
                                    branch.city
                                  }
                                </span>

                              </div>

                              <span className="branch-quantity">

                                {
                                  branch.quantity
                                }{" "}
                                available

                              </span>

                            </div>
                          )
                        )}

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

// =========================================================
// SPECIFICATION COMPONENT
// =========================================================

function Spec({
  label,
  value,
}) {
  return (
    <div className="spec-item">

      <span className="spec-label">
        {label}
      </span>

      <span className="spec-value">
        {value}
      </span>

    </div>
  );
}

export default App;