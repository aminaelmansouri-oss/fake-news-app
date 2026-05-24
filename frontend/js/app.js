// ═══════════════════════════════════════
//  TruthGuard — Main App Logic
// ═══════════════════════════════════════

// ── API Health Check ─────────────────────────────
async function checkApiStatus() {
  const dot = document.getElementById("apiStatus");
  const label = document.getElementById("statusLabel");
  if (!dot) return;
  const online = await API.checkHealth();
  dot.className = "status-dot " + (online ? "online" : "offline");
  if (label) label.textContent = online ? "API Online" : "API Offline";
}
checkApiStatus();
setInterval(checkApiStatus, 30000);

// ── Tab Switching ────────────────────────────────
function switchTab(tab) {
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === tab));
  document.querySelectorAll(".tab-panel").forEach(p => {
    p.classList.toggle("hidden", !p.id.endsWith(tab));
  });
}

// ── Character/Word Count ─────────────────────────
const textInput = document.getElementById("textInput");
if (textInput) {
  textInput.addEventListener("input", () => {
    const val = textInput.value;
    const cc = document.getElementById("charCount");
    const wc = document.getElementById("wordCount");
    if (cc) cc.textContent = `${val.length} caractères`;
    if (wc) wc.textContent = `${val.trim() ? val.trim().split(/\s+/).length : 0} mots`;
  });
}

// ── State Management ─────────────────────────────
let lastResult = null;

function setLoading(show, type = "text") {
  const panels = document.querySelectorAll(".tab-panel");
  const loading = document.getElementById("loadingState");
  const error = document.getElementById("errorState");

  panels.forEach(p => p.classList.toggle("hidden", show));
  loading.classList.toggle("hidden", !show);
  error.classList.add("hidden");

  if (show) {
    animateLoadingSteps(type === "url");
  }
}

function animateLoadingSteps(hasUrl = false) {
  const steps = ["step1", "step2", "step3"];
  const delays = hasUrl ? [0, 1200, 2400] : [0, 800, 1600];
  steps.forEach((id, i) => {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove("active");
      setTimeout(() => el.classList.add("active"), delays[i]);
    }
  });
}

function showError(msg) {
  const loading = document.getElementById("loadingState");
  const error = document.getElementById("errorState");
  const errMsg = document.getElementById("errorMsg");
  loading.classList.add("hidden");
  error.classList.remove("hidden");
  if (errMsg) errMsg.textContent = msg;
}

function resetState() {
  const panels = document.querySelectorAll(".tab-panel");
  const loading = document.getElementById("loadingState");
  const error = document.getElementById("errorState");
  const result = document.getElementById("resultSection");

  panels.forEach(p => {
    if (p.id === "panel-text") p.classList.remove("hidden");
    else p.classList.add("hidden");
  });
  loading.classList.add("hidden");
  error.classList.add("hidden");
  if (result) result.classList.add("hidden");

  // Reset active tab
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === "text"));
}

// ── Analyze Functions ────────────────────────────
async function analyzeText() {
  const text = document.getElementById("textInput").value.trim();
  if (!text || text.length < 20) {
    showError("Veuillez entrer au moins 20 caractères de texte.");
    return;
  }
  setLoading(true, "text");
  try {
    const result = await API.predictText(text);
    displayResult(result, "Manuel");
  } catch (e) {
    showError(e.message || "Erreur lors de l'analyse. Vérifiez que l'API est démarrée.");
  }
}

async function analyzeUrl() {
  const url = document.getElementById("urlInput").value.trim();
  if (!url || !url.startsWith("http")) {
    showError("Veuillez entrer une URL valide commençant par http:// ou https://");
    return;
  }
  setLoading(true, "url");
  try {
    const result = await API.predictUrl(url);
    displayResult(result, url);
  } catch (e) {
    showError(e.message || "Impossible de récupérer cet article. Vérifiez l'URL.");
  }
}

// ── Display Result ────────────────────────────────
function displayResult(data, source) {
  lastResult = { ...data, source };

  const loading = document.getElementById("loadingState");
  loading.classList.add("hidden");

  const section = document.getElementById("resultSection");
  section.classList.remove("hidden");
  section.scrollIntoView({ behavior: "smooth", block: "start" });

  const isFake = data.prediction === "FAKE";

  // Verdict banner
  const banner = document.getElementById("verdictBanner");
  banner.className = "verdict-banner " + (isFake ? "fake-verdict" : "real-verdict");
  document.getElementById("verdictIcon").textContent = isFake ? "⚠" : "✓";
  document.getElementById("verdictLabel").textContent = isFake ? "FAKE NEWS Détecté" : "Information Réelle";
  document.getElementById("verdictDesc").textContent = isFake
    ? "Notre modèle IA a identifié ce contenu comme potentiellement trompeur."
    : "Le contenu analysé présente les caractéristiques d'une information fiable.";
  document.getElementById("verdictBadge").textContent = data.confidence_label || "—";

  // Scores (animate bars)
  setTimeout(() => {
    const fakeBar = document.getElementById("fakeBar");
    const realBar = document.getElementById("realBar");
    if (fakeBar) fakeBar.style.width = data.fake_pct + "%";
    if (realBar) realBar.style.width = data.real_pct + "%";
  }, 100);

  document.getElementById("fakePct").textContent = data.fake_pct + "%";
  document.getElementById("realPct").textContent = data.real_pct + "%";

  // Confidence gauge
  setTimeout(() => {
    const fill = document.getElementById("gaugeFill");
    if (fill) fill.style.width = data.confidence_pct + "%";
  }, 200);
  document.getElementById("gaugePct").textContent = data.confidence_pct + "%";

  const confBadge = document.getElementById("confBadge");
  if (confBadge) {
    const lvl = (data.confidence_label || "low").toLowerCase();
    confBadge.textContent = data.confidence_label;
    confBadge.className = "conf-badge " + lvl;
  }

  // Meta
  document.getElementById("metaWords").textContent = data.word_count?.toLocaleString() || "—";
  const src = source.startsWith("http") ? new URL(source).hostname : source;
  document.getElementById("metaSource").textContent = src || "—";
  document.getElementById("metaConf").textContent = data.confidence_label || "—";
}

// ── Copy Result ───────────────────────────────────
function copyResult() {
  if (!lastResult) return;
  const text = [
    `TruthGuard Analyse — ${new Date().toLocaleString()}`,
    `Verdict: ${lastResult.prediction}`,
    `Confiance: ${lastResult.confidence_pct}% (${lastResult.confidence_label})`,
    `Fake: ${lastResult.fake_pct}% | Real: ${lastResult.real_pct}%`,
    `Mots: ${lastResult.word_count}`,
    `Source: ${lastResult.source}`
  ].join("\n");
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector(".action-btn.secondary");
    if (btn) {
      btn.textContent = "✓ Copié!";
      setTimeout(() => { btn.textContent = "Copier le résultat"; }, 2000);
    }
  });
}

// ── Enter key handlers ────────────────────────────
document.addEventListener("keydown", e => {
  if (e.ctrlKey && e.key === "Enter") {
    const activeTab = document.querySelector(".tab.active")?.dataset.tab;
    if (activeTab === "text") analyzeText();
    else if (activeTab === "url") analyzeUrl();
  }
});
