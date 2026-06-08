"use client";

import Link from "next/link";
import { COLORS } from "@/lib/api";

export function ComparisonTable({ data }) {
  if (!data) return null;
  const short = (zh) =>
    zh.replace(/\s*\(.*\)/, "").replace(" Clustering", "").replace(" / 深度學習", "");
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-[11px]">
        <thead>
          <tr>
            <th className="bg-navy text-[#cfe0f2] px-2 py-1.5 text-left font-medium whitespace-nowrap">
              項目
            </th>
            {data.columns.map((col) => (
              <th
                key={col.id}
                className="bg-navy text-[#cfe0f2] px-2 py-1.5 text-center font-medium whitespace-nowrap"
              >
                {short(col.zh)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, i) => (
            <tr key={row.label} className={i % 2 ? "bg-gray-50" : ""}>
              <td className="px-2 py-1.5 text-left text-gray-900 border-b border-[var(--border)]">
                {row.label}
              </td>
              {row.values.map((v, j) => (
                <td
                  key={j}
                  className="px-2 py-1.5 text-center text-gray-600 border-b border-[var(--border)] whitespace-nowrap"
                >
                  {v}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function LearningPath({ path }) {
  if (!path) return null;
  return (
    <div className="flex flex-wrap items-start justify-center gap-1">
      {path.map((p, i) => {
        const c = COLORS[p.color] || COLORS.blue;
        return (
          <div key={p.step} className="flex items-center">
            <Link
              href={`/algorithm/${p.id}`}
              className="flex flex-col items-center w-[58px] group"
            >
              <span
                className="w-8 h-8 rounded-full text-white text-[13px] font-medium flex items-center justify-center group-hover:scale-110 transition-transform"
                style={{ background: c[1] }}
              >
                {p.step}
              </span>
              <span className="text-[10px] text-gray-600 text-center mt-1 leading-tight">
                {p.zh.replace(/\s*\(.*\)/, "")}
              </span>
            </Link>
            {i < path.length - 1 && (
              <span className="text-gray-300 text-sm self-start mt-2">›</span>
            )}
          </div>
        );
      })}
    </div>
  );
}
