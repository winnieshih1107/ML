"use client";

// 每個演算法對應一個簡單的 SVG 示意圖,color 為主色 hex。
export default function AlgoIcon({ type, color, size = 64 }) {
  const s = { stroke: color, fill: "none", strokeWidth: 1.6 };
  const f = { fill: color };
  const shapes = {
    line: (
      <>
        <circle cx="14" cy="40" r="2.5" {...f} />
        <circle cx="22" cy="34" r="2.5" {...f} />
        <circle cx="32" cy="30" r="2.5" {...f} />
        <circle cx="42" cy="22" r="2.5" {...f} />
        <circle cx="50" cy="16" r="2.5" {...f} />
        <line x1="10" y1="44" x2="56" y2="12" {...s} />
      </>
    ),
    sig: (
      <>
        <path d="M10 44 C28 44 30 16 54 14" {...s} />
        <circle cx="20" cy="40" r="2" {...f} />
        <circle cx="44" cy="18" r="2" {...f} />
      </>
    ),
    tree: (
      <>
        <circle cx="32" cy="12" r="4" {...f} />
        <circle cx="18" cy="34" r="4" {...f} />
        <circle cx="46" cy="34" r="4" {...f} />
        <circle cx="40" cy="50" r="4" {...f} />
        <circle cx="54" cy="50" r="4" {...f} />
        <line x1="32" y1="16" x2="18" y2="30" {...s} />
        <line x1="32" y1="16" x2="46" y2="30" {...s} />
        <line x1="46" y1="38" x2="40" y2="46" {...s} />
        <line x1="46" y1="38" x2="54" y2="46" {...s} />
      </>
    ),
    forest: (
      <>
        <circle cx="20" cy="14" r="3.5" {...f} />
        <circle cx="12" cy="32" r="3.5" {...f} />
        <circle cx="28" cy="32" r="3.5" {...f} />
        <circle cx="46" cy="14" r="3.5" {...f} />
        <circle cx="40" cy="34" r="3.5" {...f} />
        <circle cx="54" cy="34" r="3.5" {...f} />
        <line x1="20" y1="18" x2="12" y2="28" {...s} />
        <line x1="20" y1="18" x2="28" y2="28" {...s} />
        <line x1="46" y1="18" x2="40" y2="30" {...s} />
        <line x1="46" y1="18" x2="54" y2="30" {...s} />
      </>
    ),
    svm: (
      <>
        <line x1="12" y1="48" x2="52" y2="12" {...s} />
        <circle cx="18" cy="20" r="2.5" {...f} />
        <circle cx="26" cy="16" r="2.5" {...f} />
        <circle cx="22" cy="28" r="2.5" {...f} />
        <circle cx="40" cy="44" r="2.5" {...f} />
        <circle cx="48" cy="40" r="2.5" {...f} />
        <circle cx="44" cy="34" r="2.5" {...f} />
      </>
    ),
    knn: (
      <>
        <circle cx="32" cy="30" r="14" stroke={color} fill="none" strokeWidth="1.2" strokeDasharray="3 3" />
        <circle cx="32" cy="30" r="2.5" {...f} />
        <circle cx="24" cy="24" r="2.5" {...f} />
        <circle cx="40" cy="24" r="2.5" {...f} />
        <circle cx="28" cy="38" r="2.5" {...f} />
        <circle cx="48" cy="44" r="2.5" {...f} />
        <circle cx="14" cy="16" r="2.5" {...f} />
      </>
    ),
    bayes: (
      <>
        <path d="M10 44 C18 44 18 22 26 22 C34 22 34 44 42 44" {...s} />
        <path d="M24 44 C32 44 32 18 40 18 C48 18 48 44 56 44" stroke={color} fill="none" strokeWidth="1.2" opacity="0.5" />
      </>
    ),
    kmeans: (
      <>
        <circle cx="20" cy="22" r="2.5" {...f} />
        <circle cx="26" cy="16" r="2.5" {...f} />
        <circle cx="16" cy="28" r="2.5" {...f} />
        <circle cx="44" cy="38" r="2.5" {...f} />
        <circle cx="50" cy="32" r="2.5" {...f} />
        <circle cx="46" cy="46" r="2.5" {...f} />
        <rect x="19" y="20" width="5" height="5" {...f} />
        <rect x="44" y="38" width="5" height="5" {...f} />
      </>
    ),
    pca: (
      <>
        <line x1="12" y1="46" x2="52" y2="14" {...s} />
        <circle cx="20" cy="40" r="2" {...f} />
        <circle cx="28" cy="36" r="2" {...f} />
        <circle cx="30" cy="28" r="2" {...f} />
        <circle cx="40" cy="26" r="2" {...f} />
        <circle cx="42" cy="20" r="2" {...f} />
      </>
    ),
    nn: (
      <>
        <circle cx="14" cy="20" r="3" {...f} />
        <circle cx="14" cy="40" r="3" {...f} />
        <circle cx="32" cy="14" r="3" {...f} />
        <circle cx="32" cy="30" r="3" {...f} />
        <circle cx="32" cy="46" r="3" {...f} />
        <circle cx="50" cy="24" r="3" {...f} />
        <circle cx="50" cy="40" r="3" {...f} />
        <g stroke={color} strokeWidth="0.8" opacity="0.6">
          <line x1="14" y1="20" x2="32" y2="14" />
          <line x1="14" y1="20" x2="32" y2="30" />
          <line x1="14" y1="40" x2="32" y2="30" />
          <line x1="14" y1="40" x2="32" y2="46" />
          <line x1="32" y1="14" x2="50" y2="24" />
          <line x1="32" y1="30" x2="50" y2="24" />
          <line x1="32" y1="46" x2="50" y2="40" />
        </g>
      </>
    ),
  };
  return (
    <svg width={size} height={(size * 56) / 64} viewBox="0 0 64 56">
      {shapes[type] || null}
    </svg>
  );
}
