import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

const MOCK_REQUIREMENTS = [
  { id: 'req-1', text: 'Build performant and scalable NLP models or pipelines in Python.', matchId: 'bullet-1', title: 'NLP Pipeline' },
  { id: 'req-2', text: '5+ years of experience with relational databases and SQL optimization.', matchId: 'bullet-2', title: 'SQL Architecture' },
  { id: 'req-3', text: 'Demonstrated leadership or pioneering deep learning frameworks.', matchId: 'bullet-3', title: 'Neural Networks' }
];

const MOCK_BULLETS = [
  { id: 'bullet-1', text: 'Built a distributed NLP tokenization pipeline in Python that processed 10M+ documents daily, reducing average latency by 35% and saving $40k/yr in compute costs.' },
  { id: 'bullet-2', text: 'Designed and implemented target schema mapping SQL architectures across 4 legacy databases, resolving entity relations.' },
  { id: 'bullet-3', text: 'Pioneered team initiatives on advanced deep learning and neural network training frameworks.' }
];

export default function JobMatchEngine() {
  const [jobText, setJobText] = useState('');
  const [isCalculated, setIsCalculated] = useState(false);
  const [activeReq, setActiveReq] = useState(null);
  
  // Refs to measure positions for drawing SVG lines
  const reqRefs = useRef({});
  const bulletRefs = useRef({});
  const containerRef = useRef(null);
  const [lineCoords, setLineCoords] = useState(null);

  const handleCalculate = (e) => {
    e.preventDefault();
    if (!jobText.trim()) return;
    setIsCalculated(true);
  };

  useEffect(() => {
    if (!activeReq || !isCalculated) {
      setLineCoords(null);
      return;
    }

    const reqEl = reqRefs.current[activeReq];
    const targetId = MOCK_REQUIREMENTS.find(r => r.id === activeReq)?.matchId;
    const bulletEl = bulletRefs.current[targetId];
    const containerEl = containerRef.current;

    if (reqEl && bulletEl && containerEl) {
      const containerRect = containerEl.getBoundingClientRect();
      const reqRect = reqEl.getBoundingClientRect();
      const bulletRect = bulletEl.getBoundingClientRect();

      // Find middle-right of requirement card, and middle-left of bullet card
      const x1 = reqRect.right - containerRect.left;
      const y1 = reqRect.top + reqRect.height / 2 - containerRect.top;
      
      const x2 = bulletRect.left - containerRect.left;
      const y2 = bulletRect.top + bulletRect.height / 2 - containerRect.top;

      setLineCoords({ x1, y1, x2, y2 });
    }
  }, [activeReq, isCalculated]);

  return (
    <div className="glass-card border border-white/5 relative overflow-hidden text-left" ref={containerRef}>
      <h2 className="text-xl font-bold font-display mb-2 text-white">Live Job Match Engine</h2>
      <p className="text-xs text-white/50 mb-8 font-light">Paste a target job description to match and trace alignments with your resume bullets.</p>

      {!isCalculated ? (
        <form onSubmit={handleCalculate} className="space-y-5">
          <textarea
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            placeholder="Paste target job description requirements here (e.g. 'Must have experience with Python NLP algorithms and SQL databases...')"
            className="w-full h-[150px] rounded-2xl bg-white/5 p-4 text-sm text-white placeholder-white/30 border border-white/10 focus:outline-none focus:border-cyan-500/50 resize-none font-light"
          />
          <div className="flex justify-end">
            <button
              type="submit"
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-500 hover:to-cyan-400 px-6 py-3.5 text-xs font-bold text-white shadow-xl shadow-cyan-500/10 transition-all hover:scale-105 duration-200 cursor-pointer"
            >
              Analyze Job Match
            </button>
          </div>
        </form>
      ) : (
        <div className="relative">
          {/* Back button */}
          <button 
            onClick={() => setIsCalculated(false)}
            className="absolute -top-12 right-0 flex items-center gap-1.5 text-xs font-mono text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer"
          >
            ← Reset Job Match
          </button>

          {/* SVG Overlay for Connection Lines */}
          {lineCoords && (
            <svg className="absolute inset-0 h-full w-full pointer-events-none z-20">
              <motion.path
                d={`M ${lineCoords.x1} ${lineCoords.y1} C ${(lineCoords.x1 + lineCoords.x2) / 2} ${lineCoords.y1}, ${(lineCoords.x1 + lineCoords.x2) / 2} ${lineCoords.y2}, ${lineCoords.x2} ${lineCoords.y2}`}
                fill="none"
                stroke="#22d3ee"
                strokeWidth="2.5"
                strokeDasharray="6 4"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                className="animate-[dash_1.5s_linear_infinite]"
              />
            </svg>
          )}

          <div className="grid md:grid-cols-2 gap-12 relative z-10 mt-6">
            {/* Left: Job Requirements */}
            <div className="space-y-4">
              <h3 className="text-xs font-bold font-mono uppercase tracking-widest text-cyan-400 mb-4">Job Requirements</h3>
              {MOCK_REQUIREMENTS.map((req) => (
                <div
                  key={req.id}
                  ref={el => reqRefs.current[req.id] = el}
                  onMouseEnter={() => setActiveReq(req.id)}
                  onMouseLeave={() => setActiveReq(null)}
                  className={`p-5 rounded-2xl border transition-all duration-300 cursor-pointer ${
                    activeReq === req.id 
                      ? 'bg-cyan-500/10 border-cyan-400/50 shadow-lg shadow-cyan-500/5' 
                      : 'bg-white/5 border-white/5 hover:border-white/15'
                  }`}
                >
                  <div className="text-[10px] font-mono font-bold text-cyan-300 uppercase mb-2">{req.title}</div>
                  <p className="text-sm text-white/80 leading-relaxed font-light">{req.text}</p>
                </div>
              ))}
            </div>

            {/* Right: Resume Bullets */}
            <div className="space-y-4">
              <h3 className="text-xs font-bold font-mono uppercase tracking-widest text-violet-400 mb-4">Matched Resume Experience</h3>
              {MOCK_BULLETS.map((bullet) => {
                const isMatched = activeReq && MOCK_REQUIREMENTS.find(r => r.id === activeReq)?.matchId === bullet.id;
                return (
                  <div
                    key={bullet.id}
                    ref={el => bulletRefs.current[bullet.id] = el}
                    className={`p-5 rounded-2xl border transition-all duration-300 ${
                      isMatched 
                        ? 'bg-violet-500/10 border-violet-400/50 shadow-lg shadow-violet-500/5' 
                        : 'bg-white/5 border-white/5'
                    }`}
                  >
                    <p className="text-sm text-white/70 leading-relaxed font-light">{bullet.text}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      <style>{`
        @keyframes dash {
          to {
            stroke-dashoffset: -20;
          }
        }
      `}</style>
    </div>
  );
}
