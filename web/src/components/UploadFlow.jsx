import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function UploadFlow({ onStartAnalysis, presets }) {
  const [isDragActive, setIsDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      onStartAnalysis(file.name, presets[0]); 
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      onStartAnalysis(file.name, presets[0]);
    }
  };

  return (
    <div className="mx-auto max-w-4xl text-center">
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-3 text-white">
          ATS Resume Parser Studio
        </h1>
        <p className="text-zinc-400 mb-10 max-w-xl mx-auto text-xs md:text-sm font-light">
          Drag and drop your document to trigger our compiler-grade parsers, or instantly test using one of our verified profiles below.
        </p>
      </motion.div>

      {/* Drag & Drop Zone */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className={`relative flex flex-col items-center justify-center p-10 min-h-[260px] border-2 border-dashed rounded-xl transition-all duration-300 ${
          isDragActive 
            ? 'border-blue-500 bg-blue-950/10 shadow-lg shadow-blue-500/5' 
            : 'border-zinc-800 bg-zinc-950/30 hover:border-zinc-700'
        }`}
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
      >
        {/* Fine Scanning line animation */}
        <div className="scanner-line absolute inset-0 rounded-xl pointer-events-none"></div>

        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-zinc-900 border border-zinc-800 mb-5 text-blue-400 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2.0" stroke="currentColor" className="w-6 h-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5h10.5a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0016.5 4.5H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25z" />
          </svg>
        </div>

        <h3 className="text-sm font-bold text-white mb-1.5">Drag and drop your document</h3>
        <p className="text-zinc-500 text-[10px] mb-5">Supports PDF, DOCX, TXT, or Image (OCR scan)</p>
        
        <label className="inline-flex items-center gap-2 rounded-lg bg-blue-600 hover:bg-blue-500 px-5 py-2.5 text-xs font-bold text-white shadow-sm shadow-blue-500/10 transition-all active:scale-[0.98] cursor-pointer">
          <input 
            type="file" 
            className="hidden" 
            accept=".pdf,.docx,.txt,.png,.jpg,.jpeg" 
            onChange={handleFileChange}
          />
          Choose File
        </label>
      </motion.div>

      {/* Preset Profiles */}
      <div className="mt-14 text-left">
        <h3 className="text-[10px] font-mono tracking-widest text-zinc-500 mb-6 uppercase text-center md:text-left">
          Or load a verified preset profile
        </h3>
        <div className="grid md:grid-cols-3 gap-5">
          {presets.map((preset, idx) => (
            <motion.div
              key={preset.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + idx * 0.08 }}
              onClick={() => onStartAnalysis(preset.name, preset)}
              className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-5 hover:border-blue-500/40 hover:shadow-lg hover:shadow-blue-500/5 cursor-pointer flex flex-col justify-between text-left group transition-all"
            >
              <div>
                <div className="flex justify-between items-start mb-3.5">
                  <div className="text-[10px] font-bold font-mono text-blue-400 bg-blue-500/10 border border-blue-500/20 px-2 py-0.5 rounded">
                    {preset.role.toUpperCase()}
                  </div>
                  <span className="text-zinc-500 font-mono text-[10px]">Score: <b className="text-white font-bold">{preset.score}</b></span>
                </div>
                <h4 className="font-bold text-sm text-white group-hover:text-blue-400 transition-colors mb-1">{preset.name}</h4>
                <p className="text-[11px] text-zinc-400 leading-relaxed mb-4 font-light">{preset.summary}</p>
              </div>

              <div className="border-t border-zinc-900 pt-3 flex items-center justify-between">
                <span className="text-[9px] text-zinc-500 font-mono tracking-tight">{preset.skills.slice(0, 3).join(' · ')}</span>
                <span className="text-xs text-blue-400 font-bold group-hover:translate-x-0.5 transition-transform">→</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      <style>{`
        .scanner-line {
          position: absolute;
          left: 0; right: 0; top: 0;
          height: 1px;
          background: linear-gradient(90deg, transparent, #3b82f6, transparent);
          box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
          animation: scanDown 3s ease-in-out infinite;
        }
        @keyframes scanDown {
          0% { top: 0%; opacity: 0; }
          15% { opacity: 1; }
          85% { opacity: 1; }
          100% { top: 100%; opacity: 0; }
        }
      `}</style>
    </div>
  );
}
