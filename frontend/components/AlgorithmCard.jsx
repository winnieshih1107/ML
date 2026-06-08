"use client";

import Link from "next/link";
import AlgoIcon from "./AlgoIcon";
import { COLORS } from "@/lib/api";

export default function AlgorithmCard({ algo }) {
  const c = COLORS[algo.color] || COLORS.blue;
  return (
    <Link
      href={`/algorithm/${algo.id}`}
      className="card-hover block bg-white border border-[var(--border)] rounded-lg p-3"
    >
      <div className="flex items-center gap-2 mb-2">
        <span
          className="flex-shrink-0 w-6 h-6 rounded-md text-white text-[13px] font-medium flex items-center justify-center"
          style={{ background: c[1] }}
        >
          {algo.id}
        </span>
        <span>
          <span className="block text-[13px] font-medium leading-tight text-gray-900">
            {algo.zh}
          </span>
          <span className="text-[9px] text-gray-400">{algo.en}</span>
        </span>
      </div>
      <div className="h-14 flex items-center justify-center mb-2">
        <AlgoIcon type={algo.icon} color={c[1]} />
      </div>
      <p className="text-[11px] text-gray-600 leading-snug">{algo.desc}</p>
    </Link>
  );
}
