import { api, COLORS } from '@/lib/api';
import Sidebar from '@/components/Sidebar';
import AlgoIcon from '@/components/AlgoIcon';
import TabsClient from '@/components/TabsClient';
import { notFound } from 'next/navigation';

export default async function AlgorithmPage({ params }) {
  const id = parseInt(params.id, 10);
  let algorithms = [], detail = null, paramDefs = [], quiz = null;

  try {
    [algorithms, detail, paramDefs, quiz] = await Promise.all([
      api.algorithms(),
      api.algorithm(id),
      api.params(id).catch(() => []),
      api.quiz(id).catch(() => null),
    ]);
  } catch (e) {
    if (e.message?.includes('404')) notFound();
  }

  if (!detail) notFound();

  const c = COLORS[detail.color] || COLORS.blue;

  return (
    <div className="flex min-h-screen" style={{ background: 'var(--bg)' }}>
      <Sidebar algorithms={algorithms} activeId={id} />

      <main className="flex-1 min-w-0 flex flex-col">
        {/* Header bar */}
        <div className="flex items-center gap-3 px-6 py-3 border-b"
             style={{ background: 'var(--panel-bg)', borderColor: 'var(--border)' }}>
          <span className="w-8 h-8 rounded-lg text-white text-sm font-bold flex items-center justify-center flex-shrink-0"
                style={{ background: c[1] }}>{detail.id}</span>
          <div>
            <span className="font-semibold text-base mr-2" style={{ color: 'var(--text)' }}>{detail.zh}</span>
            <span className="text-sm" style={{ color: 'var(--muted)' }}>{detail.en}</span>
          </div>
          <AlgoIcon type={detail.icon} color={c[1]} size={36} className="ml-auto opacity-60" />
        </div>

        {/* Tab content */}
        <TabsLayout detail={detail} c={c} paramDefs={paramDefs} algoId={id} quiz={quiz} />
      </main>
    </div>
  );
}

function TabsLayout({ detail, c, paramDefs, algoId, quiz }) {
  const guideContent = (
    <div className="space-y-4 max-w-2xl">
      <div className="flex flex-wrap gap-2">
        {[detail.category, detail.task, detail.use].map(t => (
          <span key={t} className="text-[10px] font-medium px-2.5 py-1 rounded-full"
                style={{ background: c[0], color: c[2] }}>{t}</span>
        ))}
      </div>
      <Field label="核心概念">{detail.idea}</Field>
      <Field label="運作原理">{detail.how}</Field>
      <Field label="典型例子">{detail.example}</Field>
      <div className="grid sm:grid-cols-2 gap-4">
        <ListBlock title="優點" items={detail.pros} color="#0F6E56" bg="#E1F5EE" />
        <ListBlock title="缺點" items={detail.cons} color="#993C1D" bg="#FAECE7" />
      </div>
      <Field label="應用場景">{detail.scenarios.join('、')}</Field>
    </div>
  );

  const codeContent = (
    <div className="max-w-xl">
      <div className="text-xs mb-2" style={{ color: 'var(--muted)' }}>程式片段 (scikit-learn / PyTorch)</div>
      <pre className="rounded-lg p-4 text-[12px] overflow-x-auto font-mono whitespace-pre leading-relaxed"
           style={{ background: '#13151f', color: '#e8eef6' }}>
        {detail.code}
      </pre>
    </div>
  );

  return (
    <TabsClient
      algoId={algoId}
      paramDefs={paramDefs}
      guideContent={guideContent}
      codeContent={codeContent}
      quiz={quiz}
      accentColor={c[1]}
    />
  );
}

function Field({ label, children }) {
  return (
    <div className="flex gap-3 text-sm">
      <span className="flex-shrink-0 w-16 text-xs pt-0.5" style={{ color: 'var(--muted)' }}>{label}</span>
      <span className="leading-relaxed" style={{ color: 'var(--text)' }}>{children}</span>
    </div>
  );
}

function ListBlock({ title, items, color, bg }) {
  return (
    <div className="rounded-md p-3" style={{ background: bg }}>
      <div className="text-xs font-medium mb-1.5" style={{ color }}>{title}</div>
      <ul className="space-y-1">
        {items.map((it, i) => (
          <li key={i} className="text-[11px] text-gray-700 flex gap-1.5">
            <span style={{ color }}>•</span>{it}
          </li>
        ))}
      </ul>
    </div>
  );
}
