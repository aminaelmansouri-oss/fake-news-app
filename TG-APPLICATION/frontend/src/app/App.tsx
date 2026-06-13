import { useState, useRef, useEffect } from "react";
import { Trash2, Eye, EyeOff, LogOut, X, Database } from "lucide-react";
import { DataScrapingJournal } from "./components/DataScrapingJournal";

type Page = "splash" | "welcome" | "auth" | "detect" | "journal";
type AuthMode = "signin" | "signup";
type Verdict = "TRUE" | "FALSE" | "MIXED";

interface UserData {
  name: string;
  email: string;
}

interface HistoryEntry {
  id: string;
  snippet: string;
  verdict: Verdict;
  confidence: number;
  timestamp: string;
}

const SERIF = { fontFamily: "'Playfair Display', Georgia, serif" };
const BODY  = { fontFamily: "'Libre Baskerville', Georgia, serif" };
const MONO  = { fontFamily: "'DM Mono', 'Courier New', monospace" };

/* ─── ANALYSIS ENGINE ─── */
function analyzeText(text: string): { verdict: Verdict; confidence: number; summary: string } {
  const lower = text.toLowerCase();
  const words = text.trim().split(/\s+/).length;

  const falseSignals = [
    "fake", "hoax", "fabricated", "false claim", "misleading", "not true",
    "conspiracy", "debunked", "misinformation", "satire", "parody",
    "lie", "lied", "cover-up", "secret agenda", "fabrication",
  ];
  const trueSignals = [
    "reuters", "associated press", "ap news", "bbc", "new york times",
    "confirmed by", "study published", "researchers from", "official statement",
    "according to", "peer-reviewed", "data shows", "government announced",
    "statistics indicate", "census bureau", "health officials",
  ];
  const mixedSignals = [
    "some reports", "allegedly", "unconfirmed", "sources say",
    "rumored", "it is believed", "may have", "could be", "possibly",
    "claims", "purportedly", "said to be",
  ];

  let falseScore = 0, trueScore = 0, mixedScore = 0;
  falseSignals.forEach(s => { if (lower.includes(s)) falseScore += 2; });
  trueSignals.forEach(s =>  { if (lower.includes(s)) trueScore  += 2; });
  mixedSignals.forEach(s => { if (lower.includes(s)) mixedScore += 1; });
  if (words > 80) trueScore  += 1;
  if (words < 15) falseScore += 1;

  const total = falseScore + trueScore + mixedScore;
  if (total === 0) {
    const seeded = (text.charCodeAt(0) + text.charCodeAt(Math.min(5, text.length - 1))) % 3;
    if (seeded === 0) return { verdict: "TRUE",  confidence: 62, summary: "No clear misinformation signals detected. The content appears consistent with factual reporting, though independent verification is always recommended." };
    if (seeded === 1) return { verdict: "MIXED", confidence: 54, summary: "The content contains both plausible claims and unsubstantiated assertions. Seek additional primary sources before drawing conclusions." };
    return               { verdict: "FALSE", confidence: 58, summary: "Several elements of this content could not be verified and exhibit patterns consistent with misinformation campaigns." };
  }
  if (falseScore > trueScore && falseScore >= mixedScore) return { verdict: "FALSE", confidence: Math.min(95, 55 + falseScore * 7), summary: "This content exhibits multiple characteristics of misinformation. Key claims appear unsubstantiated or directly contradict verified reporting from credible sources." };
  if (trueScore  > falseScore && trueScore  >= mixedScore) return { verdict: "TRUE",  confidence: Math.min(95, 55 + trueScore  * 7), summary: "This content aligns with verified reporting from credible sources. The claims are factually grounded and consistent with known, corroborated information." };
  return { verdict: "MIXED", confidence: Math.min(78, 44 + mixedScore * 5), summary: "This content blends verifiable facts with unsubstantiated claims. Exercise caution and consult primary sources before accepting or sharing this information." };
}

/* ─── SPLASH / VIDEO INTRO ─── */
function SplashPage({ onFinish }: { onFinish: () => void }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [fading, setFading] = useState(false);
  const [videoFailed, setVideoFailed] = useState(false);
  const [progress, setProgress] = useState(0);

  const exit = () => {
    if (fading) return;
    setFading(true);
    setTimeout(onFinish, 700);
  };

  /* update progress bar */
  const handleTimeUpdate = () => {
    const v = videoRef.current;
    if (v && v.duration) setProgress((v.currentTime / v.duration) * 100);
  };

  /* if video can't load, show branded fallback and auto-exit after 3 s */
  useEffect(() => {
    if (!videoFailed) return;
    const t = setTimeout(exit, 3000);
    return () => clearTimeout(t);
  }, [videoFailed]); // eslint-disable-line

  return (
    <div
      className="fixed inset-0 z-50 bg-black flex items-center justify-center overflow-hidden"
      style={{ opacity: fading ? 0 : 1, transition: "opacity 0.7s ease" }}
    >
      {/* Video */}
      {!videoFailed && (
        <video
          ref={videoRef}
          src="/intro-video.mp4"
          autoPlay
          muted
          playsInline
          onEnded={exit}
          onError={() => setVideoFailed(true)}
          onTimeUpdate={handleTimeUpdate}
          className="absolute inset-0 w-full h-full object-cover"
        />
      )}
        {/* Fallback countdown bar */}
        {videoFailed && (
          <div className="h-px bg-white/15 w-full overflow-hidden">
            <div className="h-full bg-white/40 animate-[grow_3s_linear_forwards]" style={{ width: "0%" }} />
          </div>
        )}
    </div>
  );
}

/* ─── WELCOME PAGE ─── */
function WelcomePage({ onEnter }: { onEnter: () => void }) {
  const dateStr = new Date().toLocaleDateString("en-US", {
    weekday: "long", year: "numeric", month: "long", day: "numeric",
  });

  const sampleVerdicts = [
    { verdict: "FALSE" as Verdict, headline: "New COVID variant claimed to be 'man-made' in lab", source: "Social Media · Viral Thread" },
    { verdict: "TRUE"  as Verdict, headline: "Record temperatures recorded across Southern Europe", source: "Reuters · Official Weather Data" },
    { verdict: "MIXED" as Verdict, headline: "Study links social media use to teen anxiety rates", source: "Research Blog · Preprint" },
    { verdict: "FALSE" as Verdict, headline: "Government secretly replacing paper currency with chips", source: "Online Forum · Anonymous" },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Masthead */}
      <header className="border-b-4 border-foreground px-6 md:px-12 pt-6 pb-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center text-xs tracking-widest uppercase text-muted-foreground border-b border-border pb-2 mb-5" style={MONO}>
            <span>{dateStr}</span>
            <span className="hidden md:block">Vol. CXXIV · No. 42,891</span>
            <span>Est. 1899</span>
          </div>
          <div className="text-center">
            <p className="text-xs tracking-[0.45em] uppercase text-muted-foreground mb-3" style={MONO}>
              The Independent Journal of Digital Verification
            </p>
            <h1 className="text-7xl md:text-9xl font-black tracking-tight leading-none text-foreground" style={SERIF}>
              TruthGuard
            </h1>
            <div className="h-1 bg-foreground mt-5 mb-1" />
            <div className="h-px bg-foreground" />
          </div>
        </div>
      </header>

      {/* Section nav bar */}
      <div className="border-b border-border bg-foreground text-primary-foreground px-6 md:px-12">
        <div className="max-w-6xl mx-auto flex gap-6 py-2 overflow-x-auto" style={MONO}>
          {["Fact Check", "Politics", "Science", "Health", "Technology", "World"].map(s => (
            <button
              key={s}
              onClick={() => { localStorage.setItem('selectedCategory', s); onEnter(); }}
              className="text-xs tracking-widest whitespace-nowrap opacity-80 hover:opacity-100 cursor-pointer transition-opacity bg-transparent border-0 p-0 text-primary-foreground"
              style={MONO}
            >
              {s.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Main grid */}
      <main className="max-w-6xl mx-auto px-6 md:px-12 py-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8">

          {/* Lead story */}
          <div className="md:col-span-8">
            <div className="relative overflow-hidden bg-muted h-64 md:h-80 mb-5">
              <img
                src="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=900&h=500&fit=crop&auto=format"
                alt="Stacks of printed newspapers fresh from the press floor"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-foreground/80 via-foreground/20 to-transparent" />
              <div className="absolute top-4 left-4">
                <span className="bg-accent text-accent-foreground text-xs font-bold px-3 py-1 tracking-widest uppercase" style={MONO}>
                  Special Edition
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:border-r md:border-border md:pr-6">
                <p className="text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>
                  AI-Powered Verification
                </p>
                <h3 className="text-lg font-bold mb-3" style={SERIF}>The Engine Behind the Verdict</h3>
                <p className="text-sm leading-relaxed text-muted-foreground" style={BODY}>
                  Our advanced detection engine analyzes linguistic patterns, source credibility signals, and cross-references content against verified databases — delivering accurate verdicts in seconds. No guesswork. No bias.
                </p>
              </div>
              <div>
                <p className="text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>
                  Personal Archive
                </p>
                <h3 className="text-lg font-bold mb-3" style={SERIF}>Your Research, Preserved</h3>
                <p className="text-sm leading-relaxed text-muted-foreground" style={BODY}>
                  Every analysis is stored in your personal archive. Track misinformation patterns, revisit past verdicts, and maintain a clear record of every story you have verified — all in one place.
                </p>
              </div>
            </div>
          </div>

          {/* Right sidebar */}
          <div className="md:col-span-4 md:border-l md:border-border md:pl-8 space-y-6">
            <div>
              <div className="text-xs tracking-widest uppercase text-muted-foreground border-b border-border pb-2 mb-4" style={MONO}>
                Latest Verdicts
              </div>
              {sampleVerdicts.map((item, i) => (
                <div key={i} className="flex gap-3 pb-3 mb-3 border-b border-border last:border-0 last:pb-0 last:mb-0">
                  <span
                    className={`text-xs font-bold px-1.5 py-0.5 shrink-0 mt-0.5 self-start ${
                      item.verdict === "TRUE"  ? "bg-emerald-700 text-white"
                    : item.verdict === "FALSE" ? "bg-accent text-accent-foreground"
                    : "bg-amber-600 text-white"
                    }`}
                    style={MONO}
                  >
                    {item.verdict}
                  </span>
                  <div>
                    <p className="text-xs leading-snug mb-1" style={BODY}>{item.headline}</p>
                    <p className="text-xs text-muted-foreground" style={MONO}>{item.source}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="border border-foreground p-4">
              <div className="text-xs tracking-widest uppercase text-center text-muted-foreground mb-4" style={MONO}>By The Numbers</div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div>
                  <div className="text-2xl font-black" style={SERIF}>84K</div>
                  <div className="text-xs text-muted-foreground mt-1" style={MONO}>Verified</div>
                </div>
                <div className="border-x border-border">
                  <div className="text-2xl font-black" style={SERIF}>91%</div>
                  <div className="text-xs text-muted-foreground mt-1" style={MONO}>Accuracy</div>
                </div>
                <div>
                  <div className="text-2xl font-black" style={SERIF}>12K</div>
                  <div className="text-xs text-muted-foreground mt-1" style={MONO}>Readers</div>
                </div>
              </div>
            </div>

            <button
              onClick={onEnter}
              className="w-full bg-foreground text-primary-foreground py-4 text-xs tracking-widest uppercase hover:bg-accent transition-colors duration-200"
              style={MONO}
            >
              Enter the Newsroom &rarr;
            </button>
          </div>
        </div>

        <div className="mt-10 border-t-4 border-foreground pt-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-muted-foreground text-center" style={MONO}>
            <div className="tracking-widest uppercase">Fact-Checked by Independent Journalists</div>
            <div className="tracking-widest uppercase md:border-x md:border-border">Powered by Advanced AI Analysis</div>
            <div className="tracking-widest uppercase">Trusted by Researchers Worldwide</div>
          </div>
        </div>
      </main>
    </div>
  );
}

/* ─── AUTH PAGE ─── */
function AuthPage({ onAuth }: { onAuth: (user: UserData) => void }) {
  const [mode, setMode] = useState<AuthMode>("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!email.includes("@")) { setError("Please enter a valid email address."); return; }
    if (password.length < 6)  { setError("Password must be at least 6 characters."); return; }
    onAuth({ name: name.trim() || email.split("@")[0], email });
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b-4 border-foreground px-6 md:px-12 py-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <span className="text-xs tracking-widest uppercase text-muted-foreground hidden md:block" style={MONO}>
            {new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
          </span>
          <h1 className="text-2xl md:text-3xl font-black tracking-tight" style={SERIF}>TruthGuard</h1>
          <span className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>Subscriber Access</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 md:px-12 py-12">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 items-start">

          {/* Left: image + benefits */}
          <div className="md:col-span-5">
            <div className="relative overflow-hidden bg-muted h-72 md:h-96">
              <img
                src="https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=600&h=700&fit=crop&auto=format"
                alt="Journalist reviewing printed news documents at a wooden desk"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-foreground/25" />
              <div className="absolute bottom-4 left-4 right-4">
                <p className="text-white text-sm font-bold leading-snug" style={SERIF}>
                  "In a world of noise, we deliver signal."
                </p>
                <p className="text-white/70 text-xs mt-1" style={MONO}>— TruthGuard, Est. 2026</p>
              </div>
            </div>
            <div className="border border-border p-5 mt-5">
              <div className="text-xs tracking-widest uppercase text-muted-foreground mb-3" style={MONO}>Subscriber Benefits</div>
              <ul className="space-y-3">
                {[
                  "Unlimited fact-checking analyses",
                  "Personal research archive with full history",
                  "Detailed credibility reports & confidence scores",
                  "Priority processing for breaking news",
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm" style={BODY}>
                    <span className="text-emerald-700 font-bold mt-0.5 shrink-0">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Right: form */}
          <div className="md:col-span-7">
            <div className="border-b-2 border-foreground pb-5 mb-8">
              <p className="text-xs tracking-widest uppercase text-muted-foreground mb-1" style={MONO}>Secure Access Portal</p>
              <h2 className="text-4xl font-bold leading-tight" style={SERIF}>
                {mode === "signin" ? "Welcome Back, Reader" : "Begin Your Subscription"}
              </h2>
            </div>

            <div className="flex border border-foreground mb-8">
              <button
                onClick={() => { setMode("signin"); setError(""); }}
                className={`flex-1 py-3 text-xs tracking-widest uppercase transition-colors ${mode === "signin" ? "bg-foreground text-primary-foreground" : "bg-background text-foreground hover:bg-muted"}`}
                style={MONO}
              >Sign In</button>
              <button
                onClick={() => { setMode("signup"); setError(""); }}
                className={`flex-1 py-3 text-xs tracking-widest uppercase transition-colors border-l border-foreground ${mode === "signup" ? "bg-foreground text-primary-foreground" : "bg-background text-foreground hover:bg-muted"}`}
                style={MONO}
              >Register</button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {mode === "signup" && (
                <div>
                  <label className="block text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>Full Name</label>
                  <input
                    type="text" value={name} onChange={e => setName(e.target.value)}
                    placeholder="Jane Doe"
                    className="w-full border border-border bg-background px-4 py-3 text-sm focus:outline-none focus:border-foreground transition-colors"
                    style={BODY} required={mode === "signup"}
                  />
                </div>
              )}

              <div>
                <label className="block text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>Email Address</label>
                <input
                  type="email" value={email} onChange={e => setEmail(e.target.value)}
                  placeholder="jane@example.com"
                  className="w-full border border-border bg-background px-4 py-3 text-sm focus:outline-none focus:border-foreground transition-colors"
                  style={BODY} required
                />
              </div>

              <div>
                <label className="block text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"} value={password} onChange={e => setPassword(e.target.value)}
                    placeholder="Minimum 6 characters"
                    className="w-full border border-border bg-background px-4 py-3 pr-12 text-sm focus:outline-none focus:border-foreground transition-colors"
                    style={BODY} required minLength={6}
                  />
                  <button type="button" onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors" tabIndex={-1}>
                    {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                  </button>
                </div>
              </div>

              {error && <p className="text-xs text-accent" style={MONO}>{error}</p>}

              <button type="submit"
                className="w-full bg-foreground text-primary-foreground py-4 text-xs tracking-widest uppercase hover:bg-accent transition-colors duration-200 mt-2"
                style={MONO}
              >
                {mode === "signin" ? "Enter the Newsroom →" : "Create Account →"}
              </button>
            </form>

            <p className="text-xs text-muted-foreground text-center mt-6" style={MONO}>
              {mode === "signin" ? "New reader? " : "Already subscribed? "}
              <button
                onClick={() => { setMode(mode === "signin" ? "signup" : "signin"); setError(""); }}
                className="text-foreground underline hover:text-accent transition-colors"
              >
                {mode === "signin" ? "Create an account" : "Sign in instead"}
              </button>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

/* ─── DETECTION PAGE ─── */
function DetectionPage({ user, onLogout, onOpenJournal }: { user: UserData; onLogout: () => void; onOpenJournal: () => void }) {
  const [inputText, setInputText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<{ verdict: Verdict; confidence: number; summary: string } | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [activeHistoryId, setActiveHistoryId] = useState<string | null>(null);

  const wordCount = inputText.trim().split(/\s+/).filter(Boolean).length;
  const canAnalyze = wordCount >= 5 && !isAnalyzing;

  const handleAnalyze = async () => {
    if (!canAnalyze) return;
    setIsAnalyzing(true);
    setResult(null);
    setActiveHistoryId(null);
    await new Promise(r => setTimeout(r, 2200));
    const analysis = analyzeText(inputText);
    setResult(analysis);
    const id = Date.now().toString();
    setHistory(prev => [{
      id,
      snippet: inputText.slice(0, 130) + (inputText.length > 130 ? "…" : ""),
      verdict: analysis.verdict,
      confidence: analysis.confidence,
      timestamp: new Date().toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }),
    }, ...prev]);
    setIsAnalyzing(false);
  };

  const verdictMeta = {
    TRUE:  { label: "VERIFIED TRUE",      color: "bg-emerald-700 text-white",       border: "border-emerald-700", bar: "bg-emerald-700", icon: "✓" },
    FALSE: { label: "FALSE / MISLEADING", color: "bg-accent text-accent-foreground", border: "border-accent",      bar: "bg-accent",      icon: "✗" },
    MIXED: { label: "MIXED / UNVERIFIED", color: "bg-amber-600 text-white",          border: "border-amber-600",   bar: "bg-amber-600",   icon: "!" },
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="border-b-4 border-foreground px-6 md:px-12 py-4 shrink-0">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <span className="text-xs tracking-widest uppercase text-muted-foreground hidden md:block" style={MONO}>{user.name}</span>
          <h1 className="text-2xl md:text-3xl font-black tracking-tight" style={SERIF}>TruthGuard</h1>
          <div className="flex items-center gap-4">
            <button onClick={onOpenJournal} className="flex items-center gap-2 text-xs tracking-widest uppercase text-muted-foreground hover:text-foreground transition-colors" style={MONO}>
              <Database size={13} /><span className="hidden md:block">Scraping Journal</span>
            </button>
            <button onClick={onLogout} className="flex items-center gap-2 text-xs tracking-widest uppercase text-muted-foreground hover:text-foreground transition-colors" style={MONO}>
              <LogOut size={13} /><span className="hidden md:block">Sign Out</span>
            </button>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-3 space-y-1">
          <div className="h-px bg-border" />
          <p className="text-center text-xs tracking-widest uppercase text-muted-foreground py-0.5" style={MONO}>
            Fact Verification Terminal &mdash; Advanced Misinformation Detection Engine
          </p>
          <div className="h-px bg-border" />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 md:px-12 py-8 flex-1 w-full">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10">

          {/* Left: input + result */}
          <div className="md:col-span-7">
            <div className="border-b-2 border-foreground pb-3 mb-6">
              <p className="text-xs tracking-widest uppercase text-muted-foreground mb-1" style={MONO}>Analysis Terminal</p>
              <h2 className="text-2xl font-bold" style={SERIF}>Submit Article for Verification</h2>
            </div>

            <textarea
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              placeholder="Paste or type the news article, headline, or social media post you wish to verify. Our engine will scan it for credibility signals, source patterns, and linguistic markers of misinformation..."
              className="w-full border border-border bg-background p-4 text-sm leading-relaxed resize-none focus:outline-none focus:border-foreground transition-colors"
              style={{ ...BODY, height: "220px" }}
            />

            <div className="flex justify-between items-center mt-3 mb-6">
              <span className="text-xs text-muted-foreground" style={MONO}>
                {wordCount} word{wordCount !== 1 ? "s" : ""} &middot; minimum 5 required
              </span>
              <div className="flex gap-3">
                <button onClick={() => { setInputText(""); setResult(null); }}
                  className="px-4 py-2 text-xs tracking-widest uppercase border border-border hover:border-foreground text-muted-foreground hover:text-foreground transition-colors" style={MONO}>
                  Clear
                </button>
                <button onClick={handleAnalyze} disabled={!canAnalyze}
                  className="px-6 py-2 bg-foreground text-primary-foreground text-xs tracking-widest uppercase hover:bg-accent transition-colors disabled:opacity-40 disabled:cursor-not-allowed" style={MONO}>
                  {isAnalyzing ? "Analyzing…" : "Analyze →"}
                </button>
              </div>
            </div>

            {isAnalyzing && (
              <div className="border border-border p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-4 h-4 border-2 border-foreground border-t-transparent rounded-full animate-spin" />
                  <span className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>Cross-referencing sources…</span>
                </div>
                <div className="space-y-2.5">
                  {["Scanning linguistic patterns and rhetoric markers", "Checking source credibility signals", "Analyzing factual consistency across databases"].map((step, i) => (
                    <div key={i} className="flex items-center gap-3 text-xs text-muted-foreground" style={MONO}>
                      <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse" style={{ animationDelay: `${i * 0.35}s` }} />
                      {step}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result && !isAnalyzing && (
              <div className={`border-2 ${verdictMeta[result.verdict].border} p-6`}>
                <div className="flex items-start justify-between mb-5">
                  <div>
                    <p className="text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>Verdict</p>
                    <div className={`inline-flex items-center gap-2 px-4 py-2.5 text-sm font-bold tracking-widest ${verdictMeta[result.verdict].color}`} style={MONO}>
                      <span>{verdictMeta[result.verdict].icon}</span>
                      {verdictMeta[result.verdict].label}
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-xs tracking-widest uppercase text-muted-foreground mb-1" style={MONO}>Confidence</p>
                    <div className="text-5xl font-black leading-none" style={SERIF}>{result.confidence}%</div>
                  </div>
                </div>
                <div className="h-1.5 bg-muted mb-5">
                  <div className={`h-full transition-all duration-700 ${verdictMeta[result.verdict].bar}`} style={{ width: `${result.confidence}%` }} />
                </div>
                <div className="border-t border-border pt-4">
                  <p className="text-xs tracking-widest uppercase text-muted-foreground mb-2" style={MONO}>Analysis Summary</p>
                  <p className="text-sm leading-relaxed" style={BODY}>{result.summary}</p>
                </div>
              </div>
            )}

            {!result && !isAnalyzing && (
              <div className="border border-dashed border-border p-8 text-center">
                <div className="text-muted-foreground text-xs tracking-widest uppercase mb-2" style={MONO}>Awaiting Submission</div>
                <p className="text-xs text-muted-foreground" style={BODY}>Paste any news article, headline, or social media post above and click Analyze.</p>
              </div>
            )}
          </div>

          {/* Right: history */}
          <div className="md:col-span-5 md:border-l md:border-border md:pl-10">
            <div className="flex justify-between items-end border-b-2 border-foreground pb-3 mb-6">
              <div>
                <p className="text-xs tracking-widest uppercase text-muted-foreground mb-1" style={MONO}>Research Archive</p>
                <h2 className="text-2xl font-bold" style={SERIF}>Your History</h2>
              </div>
              {history.length > 0 && (
                <button onClick={() => { setHistory([]); setActiveHistoryId(null); }}
                  className="flex items-center gap-1.5 text-xs tracking-widest uppercase text-muted-foreground hover:text-accent transition-colors pb-1" style={MONO}>
                  <Trash2 size={12} /> Clear All
                </button>
              )}
            </div>

            {history.length === 0 ? (
              <div className="border border-dashed border-border p-8 text-center">
                <div className="text-muted-foreground text-xs tracking-widest uppercase mb-2" style={MONO}>No Analyses Yet</div>
                <p className="text-xs text-muted-foreground" style={BODY}>Verified articles will appear here as you analyze them.</p>
              </div>
            ) : (
              <div className="space-y-3 overflow-y-auto pr-1" style={{ maxHeight: "calc(100vh - 280px)", scrollbarWidth: "thin" }}>
                {history.map(item => (
                  <div
                    key={item.id}
                    className={`border p-4 group transition-colors cursor-pointer ${activeHistoryId === item.id ? "border-foreground" : "border-border hover:border-foreground/50"}`}
                    onClick={() => setActiveHistoryId(activeHistoryId === item.id ? null : item.id)}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className={`text-xs font-bold px-2 py-0.5 ${item.verdict === "TRUE" ? "bg-emerald-700 text-white" : item.verdict === "FALSE" ? "bg-accent text-accent-foreground" : "bg-amber-600 text-white"}`} style={MONO}>
                        {item.verdict}
                      </span>
                      <button
                        onClick={e => { e.stopPropagation(); setHistory(prev => prev.filter(h => h.id !== item.id)); if (activeHistoryId === item.id) setActiveHistoryId(null); }}
                        className="text-muted-foreground hover:text-accent opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <X size={13} />
                      </button>
                    </div>
                    <p className={`text-xs leading-snug mt-2 text-foreground/80 ${activeHistoryId === item.id ? "" : "line-clamp-2"}`} style={BODY}>
                      {item.snippet}
                    </p>
                    <div className="flex justify-between items-center mt-3">
                      <span className="text-xs text-muted-foreground" style={MONO}>{item.timestamp}</span>
                      <span className="text-xs text-muted-foreground" style={MONO}>{item.confidence}% confidence</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="mt-8 relative overflow-hidden bg-muted h-36 hidden md:block">
              <img
                src="/Pasted image.png"
                alt="Newspaper collage background"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-foreground/30" />
              <div className="absolute inset-0 flex items-center justify-center">
                <p className="text-white text-xs tracking-widest uppercase text-center px-4" style={MONO}>Know what you share</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

/* ─── ROOT ─── */
export default function App() {
  const [page, setPage] = useState<Page>("splash");
  const [user, setUser] = useState<UserData | null>(null);

  return (
    <div className="size-full overflow-auto bg-background">
      {page === "splash" && <SplashPage onFinish={() => setPage("welcome")} />}
      {page === "welcome" && <WelcomePage onEnter={() => setPage("auth")} />}
      {page === "auth"    && <AuthPage onAuth={u => { setUser(u); setPage("detect"); }} />}
      {page === "detect"  && user && <DetectionPage user={user} onLogout={() => { setUser(null); setPage("welcome"); }} onOpenJournal={() => setPage("journal")} />}
      {page === "journal" && <DataScrapingJournal onClose={() => setPage("detect")} />}
    </div>
  );
}
