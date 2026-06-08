'use client';
import { useEffect, useRef } from 'react';

const C0 = { fill: 'rgba(239,68,68,0.55)', dot: '#ef4444', bg: 'rgba(239,68,68,0.3)' };
const C1 = { fill: 'rgba(96,165,250,0.55)', dot: '#60a5fa', bg: 'rgba(96,165,250,0.3)' };
const CENTER_COLOR = '#facc15';

const PAD_LEFT = 34;
const PAD_BOTTOM = 22;

export default function DecisionBoundary({ data, loading }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    if (!data) return;

    const { grid, points, centers } = data;
    const [xMin, xMax] = grid.xRange;
    const [yMin, yMax] = grid.yRange;

    const DW = W - PAD_LEFT;
    const DH = H - PAD_BOTTOM;

    const toX = v => PAD_LEFT + ((v - xMin) / (xMax - xMin)) * DW;
    const toY = v => DH - ((v - yMin) / (yMax - yMin)) * DH;

    // Grid cells
    if (grid.data.length) {
      const cellW = DW / grid.w;
      const cellH = DH / grid.h;
      grid.data.forEach((label, i) => {
        const col = i % grid.w;
        const row = Math.floor(i / grid.w);
        ctx.fillStyle = label === 0 ? C0.fill : C1.fill;
        ctx.fillRect(
          PAD_LEFT + col * cellW,
          (grid.h - 1 - row) * cellH,
          cellW + 1,
          cellH + 1,
        );
      });
    }

    // Axis lines
    ctx.strokeStyle = 'rgba(128,128,128,0.25)';
    ctx.lineWidth = 1;
    const cx = toX(0), cy = toY(0);
    ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, DH); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(PAD_LEFT, cy); ctx.lineTo(W, cy); ctx.stroke();

    // Axis labels
    ctx.font = '10px system-ui, sans-serif';
    ctx.fillStyle = 'rgba(150,155,170,0.85)';

    // X labels
    ctx.textAlign = 'center';
    const xTicks = [-4, -2, 0, 2, 4].filter(v => v >= xMin && v <= xMax);
    xTicks.forEach(v => {
      const x = toX(v);
      ctx.fillText(v.toString(), x, H - 5);
      ctx.beginPath();
      ctx.moveTo(x, DH); ctx.lineTo(x, DH + 3);
      ctx.strokeStyle = 'rgba(128,128,128,0.3)';
      ctx.lineWidth = 0.8;
      ctx.stroke();
    });

    // Y labels
    ctx.textAlign = 'right';
    const yStep = (yMax - yMin) / 4;
    const yTicks = [0, 1, 2, 3, 4].map(i => +(yMin + i * yStep).toFixed(2));
    yTicks.forEach(v => {
      const y = toY(v);
      ctx.fillText(v % 1 === 0 ? v.toFixed(0) : v.toFixed(1), PAD_LEFT - 4, y + 3.5);
    });

    // K-Means centers
    if (centers) {
      centers.forEach(c => {
        const x = toX(c.x), y = toY(c.y);
        ctx.beginPath();
        ctx.arc(x, y, 7, 0, Math.PI * 2);
        ctx.fillStyle = CENTER_COLOR;
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
      });
    }

    // Data points
    points.forEach(p => {
      const x = toX(p.x), y = toY(p.y);
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = p.label === 0 ? C0.dot : C1.dot;
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.7)';
      ctx.lineWidth = 1;
      ctx.stroke();
    });
  }, [data]);

  const hasBoundary = data?.grid?.data?.length > 0;

  return (
    <div className="relative rounded-lg overflow-hidden" style={{ background: 'var(--viz-bg)', aspectRatio: '3/2' }}>
      <canvas ref={canvasRef} width={600} height={400} className="w-full h-full" />

      {loading && (
        <div className="absolute inset-0 flex items-center justify-center"
             style={{ background: 'rgba(0,0,0,0.45)' }}>
          <span className="text-xs text-white">執行中…</span>
        </div>
      )}

      {!data && !loading && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xs" style={{ color: 'var(--muted)' }}>點擊「開始執行模型」查看視覺化結果</span>
        </div>
      )}

      {/* Legend */}
      {data && (
        <div className="absolute bottom-2 left-10 flex flex-wrap gap-x-3 gap-y-1 text-[10px]"
             style={{ color: 'var(--text)' }}>
          {hasBoundary && <>
            <LegendItem color={C0.bg} label="預測類別 0 (背景)" square />
            <LegendItem color={C1.bg} label="預測類別 1 (背景)" square />
          </>}
          <LegendItem color={C0.dot} label="類別 0 資料點" />
          <LegendItem color={C1.dot} label="類別 1 資料點" />
          {data.centers && <LegendItem color={CENTER_COLOR} label="群心" />}
        </div>
      )}
    </div>
  );
}

function LegendItem({ color, label, square }) {
  return (
    <span className="flex items-center gap-1">
      <span
        className="inline-block flex-shrink-0"
        style={{
          background: color,
          width: square ? 10 : 8,
          height: square ? 10 : 8,
          borderRadius: square ? 2 : '50%',
        }}
      />
      {label}
    </span>
  );
}
