import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const LOG_LINES = [
  'INITIALIZING RESANALYZE NLP CORE ENGINE...',
  'LOADING PRE-TRAINED SENTENCE TRANSFORMERS (ALL-MINILM-L6-V2)... SUCCESS',
  'LOADING EN_CORE_WEB_SM NLP MODULES... SUCCESS',
  'ESTABLISHING CONNECTION TO ATS SCHEMA v2.1.4...',
  'NLP ENGINE: STANDBY (WAITING FOR DOCUMENT STREAM)',
  '>> PRESS CTRL+~ TO CLOSE TERMINAL CONSOLE',
  '-------------------------------------------------------',
  '[INF] NLP Tokenization pipeline initialized.',
  '[INF] Named Entity Recognition (NER) models cached.',
  '[INF] STAR Compliance logic parsed (Situation, Task, Action, Result).',
  '[INF] Semantic embeddings vectorizer ready.',
  '[INF] TF-IDF dictionary size: 14,802 tokens.',
  '[INF] POS tagger categories loaded: PROPN, VERB, NOUN, ADJ.',
  '[INF] Anvil Power Verb Forge loaded (Active count: 350 verbs).'
];

export default function TerminalEasterEgg() {
  const [isOpen, setIsOpen] = useState(false);
  const [logs, setLogs] = useState(LOG_LINES);
  const terminalRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Listen for Ctrl + ~ (or Ctrl + ` which is code 'Backquote')
      if (e.ctrlKey && (e.key === '~' || e.code === 'Backquote')) {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (!isOpen) return;

    // Simulate real-time background logs
    const interval = setInterval(() => {
      const randomLogs = [
        `[DBG] Heartbeat check: NLP core thread operational. Load: ${(Math.random() * 5).toFixed(2)}%`,
        `[INF] Garbage collector cleared ${Math.floor(Math.random() * 50) + 10} unused token pointers.`,
        `[DBG] Vector dimension check: 384 dimensions matching MiniLM model.`,
        `[INF] Cached embedding query matched with similarity confidence ${0.85 + Math.random() * 0.14}`,
        `[DBG] POS parse count: verified ${Math.floor(Math.random() * 200) + 50} POS tags.`,
        `[INF] STAR analyzer evaluation: STAR structure successfully matched in Bullet ${Math.floor(Math.random() * 5) + 1}`
      ];
      const nextLog = randomLogs[Math.floor(Math.random() * randomLogs.length)];
      setLogs((prev) => [...prev, nextLog]);
    }, 3000);

    return () => clearInterval(interval);
  }, [isOpen]);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs, isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          className="fixed inset-x-0 top-0 z-50 h-[300px] border-b border-green-500/20 bg-black/95 p-6 font-mono text-xs text-green-400 shadow-2xl"
          style={{ textShadow: '0 0 5px rgba(34, 197, 94, 0.5)' }}
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-green-500/20 pb-2 mb-3">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-green-500 animate-pulse"></span>
              <span className="font-bold uppercase tracking-wider text-green-400">ResAnalyze NLP Console (Ctrl+~)</span>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-green-500 hover:text-green-300 transition-colors cursor-pointer"
            >
              [CLOSE X]
            </button>
          </div>

          {/* Console stream */}
          <div
            ref={terminalRef}
            className="h-[210px] overflow-y-auto space-y-1.5 scrollbar-thin scrollbar-thumb-green-500"
          >
            {logs.map((log, idx) => (
              <div key={idx} className="leading-relaxed">
                {log}
              </div>
            ))}
            <div className="flex items-center gap-1">
              <span>$</span>
              <span className="h-4 w-2 bg-green-500 animate-[blink_1s_infinite]"></span>
            </div>
          </div>

          <style>{`
            @keyframes blink {
              0%, 100% { opacity: 1; }
              50% { opacity: 0; }
            }
          `}</style>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
