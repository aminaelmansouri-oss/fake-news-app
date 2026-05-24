// ═══════════════════════════════════════
//  TruthGuard — Dashboard
// ═══════════════════════════════════════

async function checkApiStatus() {
  const dot = document.getElementById("apiStatus");
  const label = document.getElementById("statusLabel");
  const online = await API.checkHealth();
  if (dot) dot.className = "status-dot " + (online ? "online" : "offline");
  if (label) label.textContent = online ? "API Online" : "API Offline";
}
checkApiStatus();

async function loadDashboard() {
  try {
    const [stats, history] = await Promise.all([API.getStats(), API.getHistory(10)]);
    renderKPIs(stats);
    renderDonut(stats);
    renderBarChart(stats.daily || []);
    renderRecentTable(history);
  } catch (e) {
    console.error("Dashboard error:", e);
    showDashboardError();
  }
}

function renderKPIs(stats) {
  animateNumber("kpiTotal", stats.total);
  animateNumber("kpiFake", stats.fake_count);
  animateNumber("kpiReal", stats.real_count);
  const el = document.getElementById("kpiConf");
  if (el) el.textContent = stats.avg_confidence.toFixed(1);
  const fr = document.getElementById("kpiFakeRatio");
  const rr = document.getElementById("kpiRealRatio");
  if (fr) fr.textContent = stats.fake_ratio + "%";
  if (rr) rr.textContent = stats.real_ratio + "%";
}

function animateNumber(id, target) {
  const el = document.getElementById(id);
  if (!el) return;
  const start = 0;
  const duration = 800;
  const t0 = performance.now();
  function step(now) {
    const pct = Math.min((now - t0) / duration, 1);
    const ease = 1 - Math.pow(1 - pct, 3);
    el.textContent = Math.round(start + (target - start) * ease).toLocaleString();
    if (pct < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function renderDonut(stats) {
  const circumference = 2 * Math.PI * 70; // ~440
  const total = stats.total || 1;
  const fakePct = stats.fake_count / total;
  const realPct = stats.real_count / total;

  const fakeLen = fakePct * circumference;
  const realLen = realPct * circumference;

  const donutFake = document.getElementById("donutFake");
  const donutReal = document.getElementById("donutReal");
  const donutTotal = document.getElementById("donutTotal");

  if (donutTotal) donutTotal.textContent = stats.total.toLocaleString();

  // Fake arc starts at top (offset = circumference/4 from 0)
  if (donutFake) {
    donutFake.style.transition = "stroke-dasharray 0.8s ease";
    setTimeout(() => {
      donutFake.setAttribute("stroke-dasharray", `${fakeLen} ${circumference - fakeLen}`);
      donutFake.setAttribute("stroke-dashoffset", circumference / 4);
    }, 100);
  }

  // Real arc starts after fake
  if (donutReal) {
    donutReal.style.transition = "stroke-dasharray 0.8s ease 0.3s";
    setTimeout(() => {
      donutReal.setAttribute("stroke-dasharray", `${realLen} ${circumference - realLen}`);
      donutReal.setAttribute("stroke-dashoffset", circumference / 4 - fakeLen);
    }, 200);
  }

  const lf = document.getElementById("legendFake");
  const lr = document.getElementById("legendReal");
  if (lf) lf.textContent = `Fake: ${stats.fake_count} (${stats.fake_ratio}%)`;
  if (lr) lr.textContent = `Real: ${stats.real_count} (${stats.real_ratio}%)`;
}

function renderBarChart(daily) {
  const container = document.getElementById("barChart");
  if (!container) return;
  if (!daily.length) {
    container.innerHTML = '<div class="bar-empty">Aucune donnée sur 7 jours</div>';
    return;
  }

  // Group by day
  const byDay = {};
  daily.forEach(r => {
    if (!byDay[r.day]) byDay[r.day] = { fake: 0, real: 0 };
    if (r.prediction === "FAKE") byDay[r.day].fake = r.cnt;
    else byDay[r.day].real = r.cnt;
  });

  const days = Object.keys(byDay).sort();
  const maxVal = Math.max(...days.map(d => byDay[d].fake + byDay[d].real), 1);
  const MAX_H = 130;

  container.innerHTML = days.map(day => {
    const { fake, real } = byDay[day];
    const fakeH = Math.round((fake / maxVal) * MAX_H);
    const realH = Math.round((real / maxVal) * MAX_H);
    const label = day.slice(5); // MM-DD
    return `
      <div class="bar-group">
        <div class="bars-inner">
          ${fake > 0 ? `<div class="bar-segment fake" style="height:${fakeH}px" title="Fake: ${fake}"></div>` : ''}
          ${real > 0 ? `<div class="bar-segment real" style="height:${realH}px" title="Real: ${real}"></div>` : ''}
        </div>
        <div class="bar-day-label">${label}</div>
      </div>
    `;
  }).join("");
}

function renderRecentTable(history) {
  const tbody = document.getElementById("recentTbody");
  if (!tbody) return;
  if (!history.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-row">Aucune analyse pour l\'instant</td></tr>';
    return;
  }

  tbody.innerHTML = history.slice(0, 8).map((row, i) => {
    const isFake = row.prediction === "FAKE";
    const date = new Date(row.created_at).toLocaleString("fr-FR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
    const preview = (row.text_preview || "—").substring(0, 60) + "...";
    const confPct = Math.round(row.confidence * 100);
    const typeIcon = row.input_type === "url" ? "🔗" : "✎";
    return `
      <tr>
        <td style="font-family:var(--font-mono);color:var(--text-dim)">#${row.id}</td>
        <td style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted)">${date}</td>
        <td>${typeIcon} ${row.input_type === "url" ? "URL" : "Texte"}</td>
        <td style="max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--text-muted)">${preview}</td>
        <td><span class="verdict-pill ${isFake ? "pill-fake" : "pill-real"}">${row.prediction}</span></td>
        <td>
          <div class="conf-bar-mini">
            <div class="conf-track-mini"><div class="conf-fill-mini" style="width:${confPct}%"></div></div>
            <span class="conf-num">${confPct}%</span>
          </div>
        </td>
      </tr>
    `;
  }).join("");
}

function showDashboardError() {
  const kpiGrid = document.getElementById("kpiGrid");
  if (kpiGrid) {
    kpiGrid.innerHTML = `
      <div class="kpi-card" style="grid-column:1/-1;text-align:center;color:var(--text-muted);font-family:var(--font-mono);font-size:0.85rem;padding:2rem">
        ⚠ Impossible de charger les données. Vérifiez que l'API Flask est démarrée sur le port 5000.
      </div>
    `;
  }
}

loadDashboard();
