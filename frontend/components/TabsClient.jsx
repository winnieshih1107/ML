'use client';
import { useState } from 'react';
import dynamic from 'next/dynamic';
import QuizSection from './QuizSection';
import { COLORS } from '@/lib/api';

const PlaygroundTab = dynamic(() => import('./PlaygroundTab'), { ssr: false });

const TABS = [
  { id: 'playground', label: '▷ 實驗室 Playground' },
  { id: 'guide',      label: '□ 學習指引 Guide' },
  { id: 'code',       label: '>_ 程式實作 Code' },
];

export default function TabsClient({ algoId, paramDefs, guideContent, codeContent, quiz, accentColor }) {
  const [tab, setTab] = useState('playground');

  return (
    <div className="flex flex-col flex-1">
      {/* Tab bar */}
      <div className="flex border-b px-6" style={{ borderColor: 'var(--border)', background: 'var(--panel-bg)' }}>
        {TABS.map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className="px-4 py-3 text-xs font-medium border-b-2 -mb-px transition-colors"
            style={{
              borderColor: tab === t.id ? accentColor : 'transparent',
              color: tab === t.id ? accentColor : 'var(--muted)',
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="flex-1 p-6 overflow-auto">
        {tab === 'playground' && (
          paramDefs.length > 0
            ? <PlaygroundTab algoId={algoId} paramDefs={paramDefs} />
            : <p className="text-sm" style={{ color: 'var(--muted)' }}>此演算法暫無互動 Playground。</p>
        )}

        {tab === 'guide' && (
          <div className="space-y-6">
            {guideContent}
            {quiz && (
              <div className="max-w-lg pt-2">
                <QuizSection questions={quiz} color={[null, accentColor, null]} />
              </div>
            )}
          </div>
        )}

        {tab === 'code' && codeContent}
      </div>
    </div>
  );
}
