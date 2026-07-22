import { useEffect, useState } from "react";
import { fetchHealth, type HealthResponse } from "./api/health";
import ChatPanel from "./components/ChatPanel";
import UploadPanel from "./components/UploadPanel";
import { API_BASE_URL } from "./config";
import "./App.css";

type LoadState = "loading" | "ok" | "error";

function App() {
  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetchHealth()
      .then((data) => {
        if (!cancelled) {
          setHealth(data);
          setLoadState("ok");
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "未知错误");
          setLoadState("error");
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const backendReady = loadState === "ok";

  return (
    <main className="page">
      <header className="header">
        <p className="eyebrow">DevKit · M4 真实文档 RAG</p>
        <h1>研发团队文档助手</h1>
        <p className="subtitle">
          索引本项目 docs（PLAN、分步指南、qa 卡）→ 流式问答 + 引用来源（DevKit 场景）
        </p>
      </header>

      <section className="card card--compact">
        <div className="status-row">
          <span className="status-row__label">后端</span>
          {loadState === "loading" && <span className="status loading">检测中…</span>}
          {loadState === "ok" && health && (
            <span className="status ok-inline">✅ {health.message}</span>
          )}
          {loadState === "error" && (
            <span className="status error-inline">❌ {error}</span>
          )}
          <code className="status-row__api">{API_BASE_URL}</code>
        </div>
        {loadState === "error" && (
          <p className="hint">请先运行：.\scripts\dev.ps1</p>
        )}
      </section>

      <div className="layout">
        <aside className="layout__sidebar">
          <UploadPanel disabled={!backendReady} />
        </aside>
        <div className="layout__main">
          <ChatPanel disabled={!backendReady} />
        </div>
      </div>

      <section className="card muted">
        <h2>验收（M4.0）</h2>
        <ol className="tips-list">
          <li>终端运行 <code>uv run python scripts/import_docs.py</code></li>
          <li>确认 vector_count &gt; 0</li>
          <li>问「M3 分几步？」→ 回答应引用 M3-steps.md 内容</li>
          <li>无需外部简历 PDF 也能演示 DevKit 场景</li>
        </ol>
      </section>
    </main>
  );
}

export default App;
