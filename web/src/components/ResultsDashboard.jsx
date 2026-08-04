import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import DnaHelix from './DnaHelix.jsx';

export default function ResultsDashboard({ profile, onReset }) {
  const [activeTab, setActiveTab] = useState('summary'); // summary | nlp | xray
  const [hoveredSkill, setHoveredSkill] = useState(null);

  // SVG Radar Chart coordinates calculation
  const getRadarCoordinates = (data) => {
    const keys = ['skills', 'experience', 'education', 'formatting', 'impact'];
    const center = 100;
    const r = 70;
    return keys.map((key, idx) => {
      const angle = (idx / 5) * Math.PI * 2 - Math.PI / 2;
      const val = data[key] / 100;
      const x = center + r * val * Math.cos(angle);
      const y = center + r * val * Math.sin(angle);
      return `${x},${y}`;
    }).join(' ');
  };

  const radarPoints = getRadarCoordinates(profile.radar);

  return (
    <div className="mx-auto max-w-6xl">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 border-b border-zinc-900 pb-6 mb-8 text-left">
        <div>
          <button 
            onClick={onReset}
            className="flex items-center gap-1.5 text-[10px] font-mono text-blue-500 hover:text-blue-400 transition-colors mb-3 cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M11 6H1M5 10L1 6l4-4"/></svg>
            Upload Another Resume
          </button>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">{profile.name}</h1>
            <span className="text-[10px] font-mono font-bold text-blue-400 bg-blue-500/10 border border-blue-500/20 px-2 py-0.5 rounded uppercase">
              {profile.role}
            </span>
          </div>
          <p className="text-zinc-400 text-xs mt-2.5 max-w-2xl font-light leading-relaxed">{profile.summary}</p>
        </div>

        {/* Big Score Ring */}
        <div className="flex items-center justify-center">
          <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-zinc-950 border border-zinc-900 shadow-md">
            <svg className="absolute inset-0 h-full w-full -rotate-90">
              <circle 
                cx="48" cy="48" r="40" 
                stroke="#18181b" 
                strokeWidth="6" 
                fill="none" 
              />
              <circle 
                cx="48" cy="48" r="40" 
                stroke="url(#scoreGradient)" 
                strokeWidth="6" 
                fill="none" 
                strokeDasharray="251" 
                strokeDashoffset={251 - (251 * profile.score) / 100}
                strokeLinecap="round"
                className="transition-all duration-1000 ease-out"
              />
              <defs>
                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#3b82f6" />
                  <stop offset="100%" stopColor="#10b981" />
                </linearGradient>
              </defs>
            </svg>
            <div className="text-center">
              <span className="text-2xl font-bold font-display text-white">{profile.score}</span>
              <span className="block text-[8px] font-mono tracking-widest text-zinc-500 uppercase mt-0.5">ATS Match</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1.5 border-b border-zinc-900 pb-3 mb-6">
        {['summary', 'nlp', 'xray'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`cursor-pointer rounded-lg px-4 py-2 text-[10px] font-semibold uppercase tracking-wider transition-all duration-200 ${
              activeTab === tab 
                ? 'bg-zinc-900 text-blue-400 border border-zinc-800' 
                : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-900/30'
            }`}
          >
            {tab === 'summary' ? 'Dashboard Overview' : tab === 'nlp' ? 'NLP Parser Matrix' : 'ATS Machine Tokens'}
          </button>
        ))}
      </div>

      {/* Tab Contents */}
      <AnimatePresence mode="wait">
        {activeTab === 'summary' && (
          <motion.div
            key="summary"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="grid lg:grid-cols-3 gap-6 text-left"
          >
            {/* Left Column: DNA Helix + Radar */}
            <div className="space-y-6 lg:col-span-1">
              {/* DNA Helix */}
              <div className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-5 overflow-hidden">
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-400 mb-2">Resume DNA Helix</h3>
                <p className="text-[11px] text-zinc-500 mb-4 font-light">Trace skill alignments and gaps in a 3D structural model.</p>
                <DnaHelix matchedCount={profile.matchedSkills.length} missingCount={profile.missingSkills.length} />
              </div>

              {/* Radar Chart */}
              <div className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-5 flex flex-col items-center">
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-400 mb-5 w-full text-left">Vector Coordinates alignment</h3>
                <svg className="h-[180px] w-[180px]" viewBox="0 0 200 200">
                  <polygon points="100,30 166.5,78.3 141.1,156.7 58.9,156.7 33.5,78.3" fill="none" stroke="#27272a" strokeWidth="1" />
                  <polygon points="100,65 133,90 120,128 80,128 67,90" fill="none" stroke="#18181b" strokeWidth="1" />
                  
                  {/* Values Polygon */}
                  <polygon points={radarPoints} fill="rgba(59, 130, 246, 0.1)" stroke="#3b82f6" strokeWidth="1.5" strokeLinejoin="round" />
                  
                  {/* Labels */}
                  <text x="100" y="22" textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="8" fontFamily="monospace">SKILLS</text>
                  <text x="175" y="78" textAnchor="start" fill="rgba(255,255,255,0.4)" fontSize="8" fontFamily="monospace">EXP</text>
                  <text x="145" y="166" textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="8" fontFamily="monospace">EDU</text>
                  <text x="55" y="166" textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="8" fontFamily="monospace">FORM</text>
                  <text x="25" y="78" textAnchor="end" fill="rgba(255,255,255,0.4)" fontSize="8" fontFamily="monospace">IMPACT</text>
                </svg>
              </div>
            </div>

            {/* Right Column: Bullet scoring + Skill Matrix */}
            <div className="space-y-6 lg:col-span-2">
              {/* STAR compliance checklist */}
              <div className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-5">
                <div className="flex justify-between items-center mb-5">
                  <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-400">Bullet Quality Scoring (STAR)</h3>
                  <div className="text-[10px] text-zinc-500 font-mono">Readiness: <b className="text-blue-400 font-bold">{profile.readiness}%</b></div>
                </div>

                <div className="space-y-4">
                  {profile.bullets.map((bullet, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-zinc-950/50 border border-zinc-900 flex flex-col gap-2.5">
                      <div className="flex items-center justify-between">
                        <span className={`text-[9px] font-mono px-2 py-0.5 rounded font-bold uppercase tracking-wider ${
                          bullet.type === 'confident' 
                            ? 'bg-blue-500/10 text-blue-300 border border-blue-500/20' 
                            : bullet.type === 'passive' 
                              ? 'bg-zinc-800 text-zinc-300 border border-zinc-700' 
                              : 'bg-rose-500/10 text-rose-300 border border-rose-500/20'
                        }`}>
                          {bullet.type} style
                        </span>
                        <span className="font-mono text-[11px] font-bold text-zinc-400">{bullet.score} pts</span>
                      </div>
                      <p className="text-xs text-zinc-300 leading-relaxed font-light">{bullet.text}</p>
                      
                      {/* STAR tags */}
                      <div className="flex gap-1.5 mt-1.5">
                        {Object.entries(bullet.star).map(([key, val]) => (
                          <span 
                            key={key} 
                            className={`h-5 w-12 rounded flex items-center justify-center text-[9px] font-bold tracking-widest font-mono border ${
                              val 
                                ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' 
                                : 'bg-rose-500/10 text-rose-400 border-rose-500/20 opacity-40'
                            }`}
                          >
                            {key.toUpperCase()}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Skills Matrix */}
              <div className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-5">
                <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-400 mb-5">Semantic Skill Matrix</h3>
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill) => {
                    const isMatched = profile.matchedSkills.includes(skill);
                    return (
                      <span
                        key={skill}
                        onMouseEnter={() => setHoveredSkill(skill)}
                        onMouseLeave={() => setHoveredSkill(null)}
                        className={`cursor-pointer px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all duration-200 ${
                          isMatched 
                            ? 'bg-emerald-950/20 text-emerald-300 border-emerald-900/30 shadow-sm' 
                            : 'bg-rose-950/15 text-rose-300 border-rose-900/30'
                        } ${hoveredSkill === skill ? 'scale-102 border-zinc-600' : ''}`}
                      >
                        {skill}
                      </span>
                    );
                  })}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* NLP Parser Matrix */}
        {activeTab === 'nlp' && (
          <motion.div
            key="nlp"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-5 text-left"
          >
            <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-400 mb-2">POS & NER Entity Extraction</h3>
            <p className="text-[11px] text-zinc-500 mb-6 font-light">Natural Language Processing tags parsed from layout document stream.</p>
            
            <div className="flex flex-wrap gap-2 text-xs leading-relaxed p-5 bg-zinc-950/60 rounded-xl border border-zinc-900 max-w-3xl font-light">
              {profile.tokens.map((tok, idx) => {
                if (tok.tag === 'O') {
                  return <span key={idx} className="text-zinc-400 py-0.5">{tok.word}</span>;
                }
                const tagClass = 
                  tok.tag === 'PERSON' ? 'tag-person' : 
                  tok.tag === 'ORG' ? 'tag-org' : 
                  tok.tag === 'SKILL' ? 'tag-skill' : 'tag-date';
                return (
                  <span key={idx} className={tagClass}>
                    {tok.word} <b className="opacity-50 text-[9px] ml-1 font-bold">{tok.tag}</b>
                  </span>
                );
              })}
            </div>

            <div className="mt-8">
              <h4 className="text-xs font-bold font-mono uppercase tracking-widest text-blue-400 mb-3">Semantic Dimension Constellation</h4>
              <div className="h-[230px] w-full rounded-xl bg-zinc-950 border border-zinc-900 relative flex items-center justify-center overflow-hidden">
                {/* 3D scattered point constellation simulated in SVG */}
                <svg className="absolute inset-0 h-full w-full">
                  <line x1="40" y1="40" x2="180" y2="190" stroke="#18181b" strokeWidth="1" />
                  <line x1="180" y1="190" x2="350" y2="100" stroke="#18181b" strokeWidth="1" />
                  <line x1="350" y1="100" x2="520" y2="210" stroke="#18181b" strokeWidth="1" />
                  <line x1="520" y1="210" x2="700" y2="80" stroke="#18181b" strokeWidth="1" />
                  
                  {/* points */}
                  {profile.skills.map((s, idx) => {
                    const cx = 80 + idx * 80 + Math.sin(idx) * 20;
                    const cy = 60 + (idx % 2 === 0 ? 90 : 30) + Math.cos(idx) * 20;
                    return (
                      <g key={s}>
                        <circle cx={cx} cy={cy} r="3.5" fill="#3b82f6" />
                        <text x={cx} y={cy - 8} textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="8" fontFamily="monospace">{s}</text>
                      </g>
                    );
                  })}
                </svg>
                <div className="relative z-10 text-[9px] font-mono text-zinc-500 bg-zinc-900 border border-zinc-800 px-3 py-1 rounded-md">
                  PCA Reduction Projection Matrix
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* ATS Machine Tokens */}
        {activeTab === 'xray' && (
          <motion.div
            key="xray"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="rounded-xl border border-zinc-900 bg-zinc-950/30 p-5 text-left"
          >
            <h3 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-400 mb-2">ATS Compiler Tokens</h3>
            <p className="text-[11px] text-zinc-500 mb-6 font-light">Trace highlighted machine parser hits versus semantic gaps.</p>
            
            <div className="space-y-4 max-w-3xl">
              <div className="p-5 bg-zinc-950 border border-zinc-900 rounded-xl leading-relaxed text-[11px] font-mono text-zinc-400">
                <span className="text-zinc-500 font-bold">&lt;doc_profile&gt;</span><br />
                &nbsp;&nbsp;<span className="text-emerald-400 font-bold">&lt;name&gt;{profile.name}&lt;/name&gt;</span><br />
                &nbsp;&nbsp;<span className="text-blue-400">&lt;role_tag&gt;{profile.role}&lt;/role_tag&gt;</span><br />
                &nbsp;&nbsp;<span className="text-zinc-600">&lt;summary&gt;{profile.summary}&lt;/summary&gt;</span><br />
                &nbsp;&nbsp;<span className="text-zinc-500 font-bold">&lt;skills_vector&gt;</span><br />
                &nbsp;&nbsp;&nbsp;&nbsp;{profile.skills.map((s, idx) => (
                  <span key={s} className={profile.matchedSkills.includes(s) ? "text-emerald-400 font-bold" : "text-rose-400/80"}>
                    &quot;{s}&quot;{idx < profile.skills.length - 1 ? ", " : "" }
                  </span>
                ))}<br />
                &nbsp;&nbsp;<span className="text-zinc-500 font-bold">&lt;/skills_vector&gt;</span><br />
                <span className="text-zinc-500 font-bold">&lt;/doc_profile&gt;</span>
              </div>
              <div className="flex gap-3.5 text-[9px] font-mono text-zinc-500 justify-end px-2">
                <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded bg-emerald-400"></span>Compiler Hit</span>
                <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded bg-rose-400/80"></span>Profile Gap</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
