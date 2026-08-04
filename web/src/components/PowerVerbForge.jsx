import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const VERB_MAP = {
  managed: 'orchestrated',
  helped: 'catalyzed',
  built: 'engineered',
  created: 'spearheaded',
  led: 'championed',
  improved: 'optimized',
  used: 'leveraged',
  made: 'formulated'
};

export default function PowerVerbForge() {
  const [inputText, setInputText] = useState('');
  const [forgedText, setForgedText] = useState('');
  const [isForging, setIsForging] = useState(false);
  const [showSparks, setShowSparks] = useState(false);

  const handleForge = (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setIsForging(true);
    
    // Trigger spark animation after 0.5s (simulate hammer blow)
    setTimeout(() => {
      setShowSparks(true);
      
      // Perform replacement of weak verbs
      let text = inputText.toLowerCase();
      let hasReplacements = false;
      const replacements = [];

      Object.entries(VERB_MAP).forEach(([weak, strong]) => {
        if (text.includes(weak)) {
          hasReplacements = true;
          replacements.push({ weak, strong });
        }
      });

      let resultText = inputText;
      if (hasReplacements) {
        replacements.forEach(({ weak, strong }) => {
          const regex = new RegExp(`\\b${weak}\\b`, 'gi');
          resultText = resultText.replace(regex, `<span class="text-amber-400 font-bold underline decoration-wavy decoration-amber-400/50">${strong.toUpperCase()}</span>`);
        });
      } else {
        // Fallback upgrade
        resultText = resultText.replace(/\b(wrote|did|worked)\b/gi, '<span class="text-amber-400 font-bold underline">SPEARHEADED</span>');
      }

      setForgedText(resultText);
    }, 800);

    // Stop forging state after 2.2s
    setTimeout(() => {
      setIsForging(false);
      setShowSparks(false);
    }, 2200);
  };

  return (
    <div className="glass-card border border-white/5 relative overflow-hidden text-left">
      <h2 className="text-xl font-bold font-display mb-2 text-white">Power Verb Forge</h2>
      <p className="text-xs text-white/50 mb-8 font-light">Forge weak passive verbs into high-impact action power verbs with active heat-mapping.</p>

      <div className="grid md:grid-cols-2 gap-12 items-center">
        {/* Left Form */}
        <form onSubmit={handleForge} className="space-y-4">
          <label className="block text-xs font-mono font-bold text-white/50 uppercase">Input Weak Bullet Point</label>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type or paste a bullet point (e.g. 'I managed a team of developers and helped build the database structure.')"
            className="w-full h-[120px] rounded-2xl bg-white/5 p-4 text-sm text-white placeholder-white/30 border border-white/10 focus:outline-none focus:border-amber-500/50 resize-none font-light leading-relaxed"
          />
          <button
            type="submit"
            disabled={isForging}
            className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-600 to-orange-500 hover:from-amber-500 hover:to-orange-400 px-6 py-3.5 text-xs font-bold text-white shadow-xl shadow-amber-500/10 transition-all hover:scale-[1.01] duration-200 cursor-pointer disabled:opacity-50"
          >
            {isForging ? 'Forging Actions...' : 'Forge Upgrade'}
          </button>
        </form>

        {/* Right Forge Animation & Output */}
        <div className="flex flex-col items-center justify-center min-h-[220px] p-6 bg-black/40 border border-white/5 rounded-2xl relative overflow-hidden">
          {isForging ? (
            <div className="relative flex flex-col items-center">
              {/* Anvil SVG */}
              <motion.div
                animate={{ y: [0, -15, 0] }}
                transition={{ duration: 0.8, repeat: 2 }}
                className="text-amber-500 z-10"
              >
                <svg className="w-20 h-20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 2H5v2h2v4H3v2h2v10h14v-2h2v-8h-2V8h2V4h-2V2h-4v2h2v4H9V4h2V2z" />
                </svg>
              </motion.div>

              {/* Sparks particles */}
              {showSparks && (
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  {[...Array(12)].map((_, i) => (
                    <span 
                      key={i} 
                      className="absolute h-1.5 w-1.5 rounded-full bg-amber-400 spark-particle"
                      style={{
                        transform: `rotate(${i * 30}deg) translateX(40px)`,
                        animation: 'spark 0.6s ease-out forwards'
                      }}
                    />
                  ))}
                </div>
              )}
              
              <span className="text-xs font-mono text-amber-400 animate-pulse mt-4 uppercase tracking-widest">Applying heat compression...</span>
            </div>
          ) : forgedText ? (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }}
              className="text-left w-full h-full flex flex-col justify-between"
            >
              <div>
                <h4 className="text-xs font-mono font-bold text-amber-400 uppercase tracking-widest mb-3">Forged Bullet Result</h4>
                <p 
                  className="text-sm text-white/90 leading-relaxed font-light"
                  dangerouslySetInnerHTML={{ __html: forgedText }}
                />
              </div>
              
              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => {
                    setInputText('');
                    setForgedText('');
                  }}
                  className="text-[10px] font-mono text-white/40 hover:text-white/60 transition-colors cursor-pointer"
                >
                  Clear Output
                </button>
              </div>
            </motion.div>
          ) : (
            <div className="text-center text-white/30 max-w-[200px]">
              <svg className="w-12 h-12 mx-auto mb-3 opacity-30" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z" />
              </svg>
              <p className="text-xs font-light">Weak verbs will be upgraded to strong action terms.</p>
            </div>
          )}
        </div>
      </div>

      <style>{`
        .spark-particle {
          opacity: 0;
        }
        @keyframes spark {
          0% {
            transform: rotate(var(--rot)) translateX(0px);
            opacity: 1;
          }
          100% {
            transform: rotate(var(--rot)) translateX(80px);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
