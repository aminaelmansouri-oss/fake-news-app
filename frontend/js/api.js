// ═══════════════════════════════════════
//  TruthGuard — API Client
// ═══════════════════════════════════════

const API_BASE = "http://localhost:5000/api";

const API = {
  async predictText(text) {
    const res = await fetch(`${API_BASE}/predict/text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: "Server error" }));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    return res.json();
  },

  async predictUrl(url) {
    const res = await fetch(`${API_BASE}/predict/url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: "Server error" }));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    return res.json();
  },

  async getHistory(limit = 50) {
    const res = await fetch(`${API_BASE}/history?limit=${limit}`);
    if (!res.ok) throw new Error("Could not load history");
    return res.json();
  },

  async getStats() {
    const res = await fetch(`${API_BASE}/stats`);
    if (!res.ok) throw new Error("Could not load stats");
    return res.json();
  },

  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
      return res.ok;
    } catch {
      return false;
    }
  }
};
