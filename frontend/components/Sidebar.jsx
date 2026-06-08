'use client';
import Link from 'next/link';
import { COLORS } from '@/lib/api';
import { useTheme } from './ThemeProvider';
import AlgoIcon from './AlgoIcon';

export default function Sidebar({ algorithms, activeId }) {
  const { theme, toggle } = useTheme();

  return (
    <aside
      className="w-52 flex-shrink-0 hidden md:flex flex-col border-r"
      style={{ background: 'var(--sidebar-bg)', borderColor: 'var(--border)' }}
    >
      {/* Logo */}
      <div className="px-4 py-4 border-b" style={{ borderColor: 'var(--border)' }}>
        <div className="text-sm font-bold" style={{ color: 'var(--text)' }}>ML Platform</div>
        <div className="text-[10px] mt-0.5" style={{ color: 'var(--sidebar-muted)' }}>十大機器學習演算法</div>
      </div>

      {/* Algorithm list */}
      <nav className="flex-1 overflow-y-auto px-2 pt-2 pb-2 space-y-0.5">
        {algorithms.map((a) => {
          const c = COLORS[a.color] || COLORS.blue;
          const on = activeId === a.id;
          return (
            <Link
              key={a.id}
              href={`/algorithm/${a.id}`}
              className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs transition-colors"
              style={{
                background: on ? c[1] : 'transparent',
                color: on ? '#ffffff' : 'var(--sidebar-text)',
              }}
            >
              <span className="flex-shrink-0 opacity-90">
                <AlgoIcon type={a.icon} color={on ? '#ffffff' : c[1]} size={20} />
              </span>
              <span className="leading-tight min-w-0">
                <span className="block truncate font-medium text-[11px]">
                  {a.zh.replace(/\s*\(.*\)/, '')}
                </span>
                <span className="text-[9px]" style={{ color: on ? 'rgba(255,255,255,0.7)' : 'var(--sidebar-muted)' }}>
                  {a.en}
                </span>
              </span>
            </Link>
          );
        })}
      </nav>

      {/* Theme toggle */}
      <div className="px-3 py-3 border-t" style={{ borderColor: 'var(--border)' }}>
        <button
          onClick={toggle}
          className="w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-xs transition-colors"
          style={{ color: 'var(--sidebar-muted)', background: 'var(--sidebar-hover)' }}
        >
          <span>{theme === 'dark' ? '☀' : '🌙'}</span>
          切換主題
        </button>
      </div>
    </aside>
  );
}
