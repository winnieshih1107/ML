'use client';
import { useState, useCallback, useEffect } from 'react';
import DecisionBoundary from './DecisionBoundary';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

function initParams(defs) {
  const p = {};
  defs.forEach(d => { p[d.key] = d.default; });
  return p;
}

export default function PlaygroundTab({ algoId, paramDefs }) {
  const [params, setParams] = useState(() => initParams(paramDefs));
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const run = useCallback(async (p) => {
    setLoading(true);
    setError(false);
    try {
      const res = await fetch(`${API}/api/algorithms/${algoId}/playground`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ params: p }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      setError(true);
    } finally {
      setLoading(false);
    }
  }, [algoId]);

  // auto-run on mount
  useEffect(() => { run(params); }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  function setParam(key, value) {
    const next = { ...params, [key]: value };
    setParams(next);
  }

  const metrics = result?.metrics;

  return (
    <div className="flex flex-col lg:flex-row gap-4">
      {/* Left: controls */}
      <div className="lg:w-56 flex-shrink-0 space-y-3">
        <div className="rounded-lg border p-3 space-y-3"
             style={{ background: 'var(--panel-bg)', borderColor: 'var(--border)' }}>
          <div className="text-xs font-semibold" style={{ color: 'var(--text)' }}>
            控制面板 (Parameters)
          </div>

          {paramDefs.map(def => (
            <div key={def.key}>
              <label className="block text-[11px] mb-1" style={{ color: 'var(--muted)' }}>
                {def.label}
              </label>

              {def.type === 'select' && (
                <select
                  className="w-full text-xs px-2 py-1.5 rounded border appearance-none"
                  style={{ background: 'var(--input-bg)', borderColor: 'var(--input-border)', color: 'var(--text)' }}
                  value={params[def.key]}
                  onChange={e => {
                    const v = isNaN(e.target.value) ? e.target.value : Number(e.target.value);
                    setParam(def.key, v);
                  }}
                >
                  {def.options.map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              )}

              {def.type === 'slider' && (
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min={def.min} max={def.max} step={def.step}
                    value={params[def.key]}
                    className="flex-1 accent-[#185FA5]"
                    onChange={e => setParam(def.key, Number(e.target.value))}
                  />
                  <span className="text-[11px] w-8 text-right" style={{ color: 'var(--text)' }}>
                    {params[def.key]}
                  </span>
                </div>
              )}
            </div>
          ))}

          <button
            onClick={() => run(params)}
            disabled={loading}
            className="w-full py-2 rounded text-sm font-medium text-white transition-opacity disabled:opacity-60"
            style={{ background: '#185FA5' }}
          >
            {loading ? '執行中…' : '▶ 開始執行模型'}
          </button>
        </div>
      </div>

      {/* Right: viz + metrics */}
      <div className="flex-1 space-y-3">
        <div className="rounded-lg border p-3"
             style={{ background: 'var(--panel-bg)', borderColor: 'var(--border)' }}>
          <div className="text-xs font-semibold mb-2" style={{ color: 'var(--text)' }}>
            擬合結果 / 決策邊界 (2D Visualization)
          </div>
          <DecisionBoundary data={result} loading={loading} />
          {error && !loading && (
            <p className="text-[11px] mt-1" style={{ color: '#e05050' }}>
              無法連接後端（請確認 FastAPI 已啟動），點擊「開始執行模型」重試。
            </p>
          )}
        </div>

        {metrics && (
          <div className="rounded-lg border p-3"
               style={{ background: 'var(--panel-bg)', borderColor: 'var(--border)' }}>
            <div className="text-xs font-semibold mb-2" style={{ color: 'var(--text)' }}>
              模型評估指標 (Performance Metrics)
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {metrics.accuracy != null && <Metric label="ACCURACY" value={metrics.accuracy} />}
              {metrics.precision != null && <Metric label="PRECISION" value={metrics.precision} />}
              {metrics.recall != null && <Metric label="RECALL" value={metrics.recall} />}
              {metrics.f1 != null && <Metric label="F1 SCORE" value={metrics.f1} />}
              {metrics.inertia != null && <Metric label="INERTIA" value={metrics.inertia} raw />}
              {metrics.var1 != null && <Metric label="PC1 解釋變異" value={metrics.var1} unit="%" />}
              {metrics.var2 != null && <Metric label="PC2 解釋變異" value={metrics.var2} unit="%" />}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function Metric({ label, value, raw, unit = '' }) {
  const display = raw ? value : `${(value * 100).toFixed(1)}%`;
  const pct = raw ? null : value;
  const color = pct == null ? '#185FA5' : pct >= 0.8 ? '#0F6E56' : pct >= 0.6 ? '#185FA5' : '#993C1D';
  return (
    <div className="rounded p-2 text-center border" style={{ borderColor: 'var(--border)', background: 'var(--input-bg)' }}>
      <div className="text-[9px] tracking-widest mb-1" style={{ color: 'var(--muted)' }}>{label}</div>
      <div className="text-lg font-bold" style={{ color }}>{display}{unit && !raw ? '' : unit}</div>
    </div>
  );
}
