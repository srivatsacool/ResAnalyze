import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function Header() {
  const [currentPath, setCurrentPath] = useState('');
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    setCurrentPath(window.location.pathname);
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'Analyze', href: '/analyze' },
    { name: 'Suggestions', href: '/suggest' },
    { name: 'Docs', href: '/docs' },
    { name: 'Chat', href: '/chat' },
  ];

  return (
    <nav className="nav-in fixed top-4 inset-x-0 z-50 flex justify-center px-4" aria-label="Main navigation">
      <div
        className={`glass flex w-[min(94vw,680px)] items-center justify-between gap-2 rounded-full py-2 pl-3 pr-2 transition-all duration-300 ${
          scrolled ? 'bg-white/[0.07] shadow-[0_8px_40px_rgba(0,0,0,0.5)]' : ''
        }`}
      >
        <a href="/" className="flex items-center gap-2.5 pl-1" aria-label="ResAnalyze home">
          <span className="relative grid h-7 w-7 place-items-center rounded-lg bg-gradient-to-br from-[#8B5CF6] to-[#22D3EE] shadow-[0_0_18px_rgba(139,92,246,0.45)]">
            <span className="h-[10px] w-[2px] rounded-full bg-white/95" />
            <span className="absolute inset-x-[5px] top-1/2 h-[1.5px] -translate-y-1/2 bg-white/40" />
          </span>
          <span className="font-display text-[15px] font-bold tracking-tight text-ink">
            Res<span className="grad-text">Analyze</span>
          </span>
        </a>

        <div className="hidden items-center gap-1 md:flex">
          {navLinks.map((link) => {
            const isActive =
              currentPath === link.href || (link.href !== '/' && currentPath.startsWith(link.href));
            return (
              <a
                key={link.name}
                href={link.href}
                aria-current={isActive ? 'page' : undefined}
                className={`relative rounded-full px-3.5 py-1.5 text-[13px] font-medium transition-colors ${
                  isActive ? 'text-ink' : 'text-mute hover:text-ink'
                }`}
              >
                {isActive && (
                  <motion.span
                    layoutId="nav-lamp"
                    className="absolute inset-0 -z-10 rounded-full bg-white/10 shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]"
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  >
                    <span className="absolute -top-1 left-1/2 h-[2px] w-6 -translate-x-1/2 rounded-full bg-gradient-to-r from-[#8B5CF6] to-[#22D3EE]" />
                  </motion.span>
                )}
                <span className="relative z-10">{link.name}</span>
              </a>
            );
          })}
        </div>

        <a
          href="/analyze"
          className="btn-primary rounded-full px-4 py-2 text-[13px] font-semibold text-white"
        >
          Analyze resume
        </a>
      </div>
    </nav>
  );
}
