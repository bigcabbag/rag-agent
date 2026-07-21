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
        <p className="eyebrow">DevKit · M3 全栈 RAG</p>
        <h1>研发团队文档助手</h1>
        <p className="subtitle">上传 PDF → 向量统计 → 流式问答 + 引用来源</p>
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
        <h2>验收（M3.5）</h2>
        <ol className="tips-list">
          <li>左侧上传 PDF，确认 vector_count &gt; 0</li>
          <li>右侧开「流式输出」，提问后看逐字生成 + 引用来源</li>
          <li>关流式开关，确认仍可用非流式 /chat</li>
          <li>全程浏览器完成，无需 Swagger</li>
        </ol>
      </section>
    </main>
  );
}

export default App;
