export default function Footer() {
  return (
    <footer className="border-t border-white/5">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 px-6 py-10 sm:flex-row">
        <div className="flex items-center gap-2.5">
          <span className="grid h-6 w-6 place-items-center rounded-md bg-gradient-to-br from-[#8B5CF6] to-[#22D3EE]">
            <span className="h-[8px] w-[1.5px] rounded-full bg-white/95" />
          </span>
          <span className="font-display text-sm font-bold text-ink">
            Res<span className="grad-text">Analyze</span>
          </span>
          <span className="ml-2 font-mono text-[10px] text-[#5E5E72]">v0.4 · 70 notebooks</span>
        </div>
        <div className="flex items-center gap-6 font-mono text-[11px] tracking-wide text-mute">
          <a href="/analyze" className="transition-colors hover:text-ink">Analyze</a>
          <a href="/docs" className="transition-colors hover:text-ink">Docs</a>
          <a href="/chat" className="transition-colors hover:text-ink">Chat</a>
          <a href="https://github.com/srivatsacool/ResAnalyze" className="transition-colors hover:text-ink">GitHub</a>
        </div>
        <p className="font-mono text-[10px] text-[#5E5E72]">© 2026 ResAnalyze — NLP Resume Intelligence</p>
      </div>
    </footer>
  );
}
