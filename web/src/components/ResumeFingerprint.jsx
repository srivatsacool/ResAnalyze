import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function ResumeFingerprint() {
  const [vectorSeed, setVectorSeed] = useState(0.85);

  const handleRegenerate = () => {
    setVectorSeed(0.5 + Math.random() * 0.5);
  };

  return (
    <div className="glass-card border border-white/5 space-y-6 relative overflow-hidden">
      {/* Glow highlight */}
      <div className="absolute -left-12 -bottom-12 h-44 w-44 rounded-full bg-cyan-600/10 blur-[60px] pointer-events-none"></div>

      <div className="flex justify-between items-center">
        <h3 className="text-sm font-bold font-mono uppercase tracking-wider text-white/80">Resume Fingerprint</h3>
        <button 
          onClick={handleRegenerate}
          className="text-[10px] font-mono text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer"
        >
          Regenerate Vector
        </button>
      </div>

      {/* Vector Graphic Canvas */}
      <div className="h-[220px] w-full rounded-2xl bg-black/45 border border-white/5 relative flex items-center justify-center overflow-hidden">
        <svg className="absolute inset-0 h-full w-full opacity-80" viewBox="0 0 200 200">
          <defs>
            <radialGradient id="fingerGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#07070f" stopOpacity="0" />
            </radialGradient>
          </defs>
          
          {/* Glowing central radar rings */}
          <circle cx="100" cy="100" r="80" fill="none" stroke="rgba(255,255,255,0.02)" strokeWidth="0.5" />
          <circle cx="100" cy="100" r="60" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="0.5" />
          <circle cx="100" cy="100" r="40" fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth="0.5" />
          <circle cx="100" cy="100" r="20" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="0.5" />
          
          {/* Radial grid lines */}
          <line x1="100" y1="20" x2="100" y2="180" stroke="rgba(255,255,255,0.03)" strokeWidth="0.5" />
          <line x1="20" y1="100" x2="180" y2="100" stroke="rgba(255,255,255,0.03)" strokeWidth="0.5" />
          <line x1="43" y1="43" x2="157" y2="157" stroke="rgba(255,255,255,0.02)" strokeWidth="0.5" />
          <line x1="43" y1="157" x2="157" y2="43" stroke="rgba(255,255,255,0.02)" strokeWidth="0.5" />

          {/* Generative Vector Shape */}
          <polygon
            points={`
              100,${100 - 80 * vectorSeed} 
              ${100 + 70 * (vectorSeed * 0.9)},${100 - 45 * vectorSeed} 
              ${100 + 60 * vectorSeed},${100 + 40 * (vectorSeed * 1.1)} 
              100,${100 + 55 * vectorSeed} 
              ${100 - 75 * (vectorSeed * 0.85)},${100 + 35 * vectorSeed} 
              ${100 - 65 * vectorSeed},${100 - 50 * (vectorSeed * 0.95)}
            `}
            fill="rgba(124, 58, 237, 0.15)"
            stroke="#c084fc"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />

          {/* Additional secondary glowing polygon */}
          <polygon
            points={`
              100,${100 - 40 * vectorSeed} 
              ${100 + 30 * vectorSeed},${100 - 20 * vectorSeed} 
              ${100 + 35 * vectorSeed},${100 + 25 * vectorSeed} 
              100,${100 + 30 * vectorSeed} 
              ${100 - 40 * vectorSeed},${100 + 15 * vectorSeed} 
              ${100 - 30 * vectorSeed},${100 - 25 * vectorSeed}
            `}
            fill="rgba(34, 211, 238, 0.1)"
            stroke="#22d3ee"
            strokeWidth="1"
            strokeLinejoin="round"
          />

          {/* Constellation dots */}
          <circle cx="100" cy={100 - 80 * vectorSeed} r="3" fill="#ffffff" />
          <circle cx={100 + 70 * (vectorSeed * 0.9)} cy={100 - 45 * vectorSeed} r="3" fill="#22d3ee" />
          <circle cx={100 - 75 * (vectorSeed * 0.85)} cy={100 + 35 * vectorSeed} r="3" fill="#c084fc" />
        </svg>

        <div className="absolute bottom-3 right-3 text-[9px] font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-500/20 px-2.5 py-0.5 rounded">
          VECTOR ID: {(vectorSeed * 100000).toFixed(0)}
        </div>
      </div>

      <div className="text-xs text-white/50 leading-relaxed font-light">
        Your Resume Fingerprint is a unique generative vector generated based on your semantic skills cluster and experience density coefficients.
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-4">
        <button className="inline-flex items-center justify-center gap-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 px-4 py-3 text-xs font-semibold text-white transition-all cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 9v3a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9M4 5l4 4 4-4M8 1v8"/></svg>
          Export PNG
        </button>
        <button className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-cyan-500 hover:from-violet-500 hover:to-cyan-400 px-4 py-3 text-xs font-semibold text-white shadow-xl shadow-cyan-500/10 transition-all cursor-pointer">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M14 1.5h-3.5a1.5 1.5 0 0 0-1.5 1.5v3.5M10.5 1.5L5.5 6.5M1.5 8h3.5a1.5 1.5 0 0 1 1.5 1.5V13M5.5 9.5l-4 4"/></svg>
          Share Vector
        </button>
      </div>
    </div>
  );
}
