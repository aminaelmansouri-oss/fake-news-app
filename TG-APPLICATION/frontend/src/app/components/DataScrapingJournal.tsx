import { Database, TrendingUp, AlertTriangle, CheckCircle, Clock, Globe } from "lucide-react";

const SERIF = { fontFamily: "'Playfair Display', Georgia, serif" };
const BODY = { fontFamily: "'Libre Baskerville', Georgia, serif" };
const MONO = { fontFamily: "'DM Mono', 'Courier New', monospace" };

interface ScrapedArticle {
  id: string;
  headline: string;
  source: string;
  domain: string;
  verdict: "TRUE" | "FALSE" | "MIXED";
  scrapedAt: string;
  shares: number;
  engagement: number;
}

interface SourceStats {
  domain: string;
  articles: number;
  reliability: number;
  lastScrape: string;
}

const mockScrapedData: ScrapedArticle[] = [
  {
    id: "1",
    headline: "Climate scientists warn of unprecedented Arctic ice melt",
    source: "Reuters Science Desk",
    domain: "reuters.com",
    verdict: "TRUE",
    scrapedAt: "2 hours ago",
    shares: 12400,
    engagement: 89,
  },
  {
    id: "2",
    headline: "Government to replace all currency with microchips by 2027",
    source: "Anonymous Blog",
    domain: "conspiracynews.net",
    verdict: "FALSE",
    scrapedAt: "3 hours ago",
    shares: 8900,
    engagement: 34,
  },
  {
    id: "3",
    headline: "New vaccine shows promise in early trials, experts cautious",
    source: "Medical Journal Abstract",
    domain: "sciencedirect.com",
    verdict: "MIXED",
    scrapedAt: "5 hours ago",
    shares: 5600,
    engagement: 67,
  },
  {
    id: "4",
    headline: "Tech giant announces major data breach affecting millions",
    source: "TechCrunch",
    domain: "techcrunch.com",
    verdict: "TRUE",
    scrapedAt: "7 hours ago",
    shares: 18200,
    engagement: 92,
  },
  {
    id: "5",
    headline: "Celebrity death hoax spreads rapidly on social media",
    source: "Viral Tweet Thread",
    domain: "twitter.com",
    verdict: "FALSE",
    scrapedAt: "9 hours ago",
    shares: 24100,
    engagement: 41,
  },
  {
    id: "6",
    headline: "Economic indicators suggest potential market correction",
    source: "Financial Times",
    domain: "ft.com",
    verdict: "MIXED",
    scrapedAt: "12 hours ago",
    shares: 4200,
    engagement: 78,
  },
];

const sourceStats: SourceStats[] = [
  { domain: "reuters.com", articles: 847, reliability: 94, lastScrape: "12 min ago" },
  { domain: "nytimes.com", articles: 623, reliability: 91, lastScrape: "18 min ago" },
  { domain: "bbc.com", articles: 701, reliability: 93, lastScrape: "25 min ago" },
  { domain: "conspiracynews.net", articles: 234, reliability: 12, lastScrape: "31 min ago" },
  { domain: "twitter.com", articles: 1523, reliability: 48, lastScrape: "8 min ago" },
  { domain: "facebook.com", articles: 1102, reliability: 52, lastScrape: "14 min ago" },
];

export function DataScrapingJournal({ onClose }: { onClose: () => void }) {
  const dateStr = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const stats = {
    totalScraped: 6847,
    last24h: 1423,
    falseDetected: 342,
    accuracy: 91,
  };

  // Read selected category from localStorage (set by App.tsx buttons)
  const selectedCategory = (typeof window !== 'undefined' && localStorage.getItem('selectedCategory')) || '';

  // Simple keyword mapping to simulate filtering per category for demo
  const categoryKeywords: Record<string, string[]> = {
    Politics: ['government', 'election', 'policy', 'congress', 'senate', 'president'],
    Technology: ['tech', 'data breach', 'AI', 'machine', 'software', 'startup'],
    World: ['global', 'united', 'world', 'international', 'u.s.', 'china', 'russia'],
    Science: ['study', 'research', 'scientists', 'vaccine', 'trial'],
    Health: ['health', 'vaccine', 'hospital', 'covid', 'disease'],
    'Fact Check': [],
  };

  const filteredData = selectedCategory && categoryKeywords[selectedCategory]
    ? mockScrapedData.filter(a => categoryKeywords[selectedCategory].some(k => a.headline.toLowerCase().includes(k)))
    : mockScrapedData;

  return (
    <div className="min-h-screen bg-background">
      {/* Masthead */}
      <header className="border-b-4 border-foreground px-6 md:px-12 pt-6 pb-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center text-xs tracking-widest uppercase text-muted-foreground border-b border-border pb-2 mb-5" style={MONO}>
            <span>{dateStr}</span>
            <span className="hidden md:block">Data Intelligence Report</span>
            <button
              onClick={onClose}
              className="hover:text-foreground transition-colors"
            >
              ← Back
            </button>
          </div>
          <div className="text-center">
            <p className="text-xs tracking-[0.45em] uppercase text-muted-foreground mb-3" style={MONO}>
              TruthGuard Intelligence Division
            </p>
            <h1 className="text-6xl md:text-8xl font-black tracking-tight leading-none text-foreground" style={SERIF}>
              Scraping Journal
            </h1>
            <p className="text-sm text-muted-foreground mt-3 tracking-wide" style={MONO}>
              Real-time monitoring of digital information streams
            </p>
            <div className="h-1 bg-foreground mt-5 mb-1" />
            <div className="h-px bg-foreground" />
          </div>
        </div>
      </header>

      {/* Stats bar */}
      <div className="border-b-2 border-foreground bg-card">
        <div className="max-w-7xl mx-auto px-6 md:px-12 py-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center border-r border-border last:border-r-0">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Database size={16} className="text-muted-foreground" />
                <span className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>
                  Total Scraped
                </span>
              </div>
              <div className="text-3xl font-black" style={SERIF}>
                {stats.totalScraped.toLocaleString()}
              </div>
            </div>
            <div className="text-center border-r border-border md:border-r">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Clock size={16} className="text-muted-foreground" />
                <span className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>
                  Last 24 Hours
                </span>
              </div>
              <div className="text-3xl font-black" style={SERIF}>
                {stats.last24h.toLocaleString()}
              </div>
            </div>
            <div className="text-center border-r border-border last:border-r-0">
              <div className="flex items-center justify-center gap-2 mb-2">
                <AlertTriangle size={16} className="text-accent" />
                <span className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>
                  False Detected
                </span>
              </div>
              <div className="text-3xl font-black text-accent" style={SERIF}>
                {stats.falseDetected}
              </div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                <CheckCircle size={16} className="text-emerald-700" />
                <span className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>
                  Accuracy
                </span>
              </div>
              <div className="text-3xl font-black text-emerald-700" style={SERIF}>
                {stats.accuracy}%
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-6 md:px-12 py-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10">

          {/* Left: recent scrapes */}
          <div className="md:col-span-7">
            <div className="border-b-2 border-foreground pb-3 mb-6">
              <div className="flex items-center gap-2 mb-1">
                <TrendingUp size={18} className="text-foreground" />
                <p className="text-xs tracking-widest uppercase text-muted-foreground" style={MONO}>
                  Live Feed
                </p>
              </div>
              <h2 className="text-3xl font-bold" style={SERIF}>
                Recently Scraped Articles
              </h2>
            </div>

            <div className="space-y-5">
              {filteredData.map((article) => (
                <article
                  key={article.id}
                  className="border-2 border-border hover:border-foreground transition-all p-5"
                >
                  <div className="flex items-start justify-between mb-3">
                    <span
                      className={`text-xs font-bold px-2 py-1 tracking-widest ${
                        article.verdict === "TRUE"
                          ? "bg-emerald-700 text-white"
                          : article.verdict === "FALSE"
                          ? "bg-accent text-accent-foreground"
                          : "bg-amber-600 text-white"
                      }`}
                      style={MONO}
                    >
                      {article.verdict}
                    </span>
                    <span className="text-xs text-muted-foreground" style={MONO}>
                      {article.scrapedAt}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold leading-tight mb-2" style={SERIF}>
                    {article.headline}
                  </h3>

                  <div className="flex items-center gap-4 text-xs text-muted-foreground mb-3" style={MONO}>
                    <span className="flex items-center gap-1">
                      <Globe size={12} />
                      {article.domain}
                    </span>
                    <span>•</span>
                    <span>{article.source}</span>
                  </div>

                  <div className="flex items-center justify-between border-t border-border pt-3">
                    <div className="flex items-center gap-4 text-xs" style={MONO}>
                      <span className="text-muted-foreground">
                        {article.shares.toLocaleString()} shares
                      </span>
                      <span className="text-muted-foreground">•</span>
                      <span className="text-muted-foreground">
                        {article.engagement}% engagement
                      </span>
                    </div>
                    <div className="h-1 w-16 bg-muted">
                      <div
                        className={`h-full ${
                          article.engagement > 70
                            ? "bg-emerald-700"
                            : article.engagement > 40
                            ? "bg-amber-600"
                            : "bg-accent"
                        }`}
                        style={{ width: `${article.engagement}%` }}
                      />
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>

          {/* Right: source monitoring */}
          <div className="md:col-span-5 md:border-l md:border-border md:pl-10">
            <div className="border-b-2 border-foreground pb-3 mb-6">
              <p className="text-xs tracking-widest uppercase text-muted-foreground mb-1" style={MONO}>
                Source Intelligence
              </p>
              <h2 className="text-2xl font-bold" style={SERIF}>
                Monitored Sources
              </h2>
            </div>

            <div className="space-y-4">
              {sourceStats.map((source) => (
                <div
                  key={source.domain}
                  className="border border-border p-4 hover:border-foreground transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="text-sm font-bold mb-1" style={SERIF}>
                        {source.domain}
                      </h3>
                      <p className="text-xs text-muted-foreground" style={MONO}>
                        {source.articles.toLocaleString()} articles scraped
                      </p>
                    </div>
                    <span
                      className={`text-xs font-bold px-2 py-1 ${
                        source.reliability > 80
                          ? "bg-emerald-700 text-white"
                          : source.reliability > 50
                          ? "bg-amber-600 text-white"
                          : "bg-accent text-accent-foreground"
                      }`}
                      style={MONO}
                    >
                      {source.reliability}%
                    </span>
                  </div>

                  <div className="mb-2">
                    <div className="h-1.5 bg-muted">
                      <div
                        className={`h-full transition-all ${
                          source.reliability > 80
                            ? "bg-emerald-700"
                            : source.reliability > 50
                            ? "bg-amber-600"
                            : "bg-accent"
                        }`}
                        style={{ width: `${source.reliability}%` }}
                      />
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-muted-foreground" style={MONO}>
                    <span>Reliability Score</span>
                    <span>Last: {source.lastScrape}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Info box */}
            <div className="mt-8 border-2 border-foreground p-5 bg-card">
              <div className="text-xs tracking-widest uppercase text-center text-muted-foreground mb-3" style={MONO}>
                System Status
              </div>
              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm" style={BODY}>
                  <span className="text-muted-foreground">Scraper Engine</span>
                  <span className="flex items-center gap-1.5 text-emerald-700 font-bold">
                    <div className="w-2 h-2 bg-emerald-700 rounded-full animate-pulse" />
                    ACTIVE
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm" style={BODY}>
                  <span className="text-muted-foreground">Sources Monitored</span>
                  <span className="font-bold">247</span>
                </div>
                <div className="flex justify-between items-center text-sm" style={BODY}>
                  <span className="text-muted-foreground">Avg. Response Time</span>
                  <span className="font-bold">1.2s</span>
                </div>
                <div className="flex justify-between items-center text-sm" style={BODY}>
                  <span className="text-muted-foreground">Uptime</span>
                  <span className="font-bold">99.8%</span>
                </div>
              </div>
            </div>

            {/* Image */}
            <div className="mt-6 relative overflow-hidden bg-muted h-48 hidden md:block">
              <img
                src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop&auto=format"
                alt="Data analytics dashboard on computer screen"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-foreground/40" />
              <div className="absolute inset-0 flex items-center justify-center">
                <p className="text-white text-xs tracking-widest uppercase text-center px-4" style={MONO}>
                  Powered by AI &middot; Updated in Real-Time
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 border-t-4 border-foreground pt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-muted-foreground text-center" style={MONO}>
            <div className="tracking-widest uppercase">
              Automated web scraping engine
            </div>
            <div className="tracking-widest uppercase md:border-x md:border-border">
              Cross-platform source monitoring
            </div>
            <div className="tracking-widest uppercase">
              Real-time misinformation detection
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
