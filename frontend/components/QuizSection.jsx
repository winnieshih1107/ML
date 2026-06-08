'use client';
import { useState } from 'react';

export default function QuizSection({ questions, color }) {
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState(null); // index of chosen option
  const [score, setScore] = useState(0);
  const [done, setDone] = useState(false);

  if (!questions?.length) return null;

  const q = questions[idx];
  const total = questions.length;
  const isCorrect = selected === q.ans;

  function choose(i) {
    if (selected !== null) return;
    setSelected(i);
    if (i === q.ans) setScore(s => s + 1);
  }

  function next() {
    if (idx + 1 >= total) {
      setDone(true);
    } else {
      setIdx(i => i + 1);
      setSelected(null);
    }
  }

  function restart() {
    setIdx(0);
    setSelected(null);
    setScore(0);
    setDone(false);
  }

  const accent = color?.[1] || '#185FA5';
  const bg = color?.[0] || '#E6F1FB';

  return (
    <div className="rounded-lg border border-[var(--border)] overflow-hidden bg-white">
      <div
        className="flex items-center justify-between px-4 py-2.5 border-b border-[var(--border)]"
        style={{ background: bg }}
      >
        <span className="text-xs font-semibold" style={{ color: accent }}>📝 小測驗</span>
        {!done && (
          <span className="text-[10px] text-gray-500">{idx + 1} / {total}</span>
        )}
      </div>

      <div className="p-4">
        {done ? (
          <div className="text-center space-y-3 py-2">
            <div className="text-2xl font-bold" style={{ color: accent }}>
              {score} / {total}
            </div>
            <p className="text-sm text-gray-600">
              {score === total ? '全對！掌握得非常好！' : score >= total / 2 ? '不錯！繼續加油！' : '再複習一遍試試看！'}
            </p>
            <button
              onClick={restart}
              className="text-xs px-3 py-1.5 rounded border border-[var(--border)] text-gray-600 hover:bg-gray-50"
            >
              重新作答
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <p className="text-sm text-gray-800 font-medium leading-relaxed">{q.q}</p>

            <div className="space-y-2">
              {q.opts.map((opt, i) => {
                let cls =
                  'w-full text-left text-xs px-3 py-2 rounded border transition-colors ';
                if (selected === null) {
                  cls += 'border-[var(--border)] hover:border-gray-400 text-gray-700';
                } else if (i === q.ans) {
                  cls += 'border-green-400 bg-green-50 text-green-800 font-medium';
                } else if (i === selected) {
                  cls += 'border-red-300 bg-red-50 text-red-700';
                } else {
                  cls += 'border-[var(--border)] text-gray-400';
                }
                return (
                  <button key={i} className={cls} onClick={() => choose(i)}>
                    {String.fromCharCode(65 + i)}. {opt}
                  </button>
                );
              })}
            </div>

            {selected !== null && (
              <div className="flex items-center justify-between pt-1">
                <span className={`text-xs font-medium ${isCorrect ? 'text-green-600' : 'text-red-500'}`}>
                  {isCorrect ? '✓ 正確！' : `✗ 正確答案：${String.fromCharCode(65 + q.ans)}. ${q.opts[q.ans]}`}
                </span>
                <button
                  onClick={next}
                  className="text-xs px-3 py-1 rounded text-white"
                  style={{ background: accent }}
                >
                  {idx + 1 >= total ? '查看成績' : '下一題 →'}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
