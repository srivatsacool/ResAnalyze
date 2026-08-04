import React, { useState, useEffect } from 'react';
import UploadFlow from './UploadFlow.jsx';
import ResultsDashboard from './ResultsDashboard.jsx';

const PRESETS = [
  {
    name: "Srivatsa Gorti",
    role: "Data Scientist",
    score: 87,
    summary: "Senior Data Scientist with 5+ years of experience specializing in NLP pipeline design, large language models, and scalable machine learning APIs.",
    skills: ["Python", "NLP", "TensorFlow", "PyTorch", "Transformers", "SQL", "Docker", "FastAPI"],
    matchedSkills: ["Python", "NLP", "TensorFlow", "SQL", "FastAPI"],
    missingSkills: ["PyTorch", "Transformers", "Docker"],
    readiness: 85,
    radar: { skills: 90, experience: 85, education: 95, formatting: 80, impact: 85 },
    bullets: [
      {
        text: "Built a distributed NLP tokenization pipeline in Python that processed 10M+ documents daily, reducing average latency by 35% and saving $40k/yr in compute costs.",
        star: { s: true, t: true, a: true, r: true },
        score: 95,
        type: "confident"
      },
      {
        text: "Designed and implemented target schema mapping SQL architectures across 4 legacy databases, resolving entity relations.",
        star: { s: true, t: true, a: true, r: false },
        score: 65,
        type: "passive"
      },
      {
        text: "Pioneered team initiatives on advanced deep learning and neural network training frameworks.",
        star: { s: false, t: false, a: true, r: false },
        score: 40,
        type: "arrogant"
      }
    ],
    tokens: [
      { word: "Srivatsa", tag: "PERSON" },
      { word: "Gorti", tag: "PERSON" },
      { word: "Senior", tag: "O" },
      { word: "Data", tag: "O" },
      { word: "Scientist", tag: "O" },
      { word: "at", tag: "O" },
      { word: "Google", tag: "ORG" },
      { word: "since", tag: "O" },
      { word: "2024", tag: "DATE" },
      { word: "specializing", tag: "O" },
      { word: "in", tag: "O" },
      { word: "Python", tag: "SKILL" },
      { word: "NLP", tag: "SKILL" },
      { word: "and", tag: "O" },
      { word: "TensorFlow", tag: "SKILL" }
    ]
  },
  {
    name: "Priya Sharma",
    role: "DevOps Engineer",
    score: 78,
    summary: "Cloud and Infrastructure Engineer with expertise in infrastructure-as-code, container orchestration, and automating multi-stage CI/CD pipelines.",
    skills: ["AWS", "Terraform", "Kubernetes", "Docker", "Jenkins", "Ansible", "Bash", "Python"],
    matchedSkills: ["AWS", "Terraform", "Docker", "Jenkins"],
    missingSkills: ["Kubernetes", "Ansible", "Bash"],
    readiness: 72,
    radar: { skills: 80, experience: 75, education: 80, formatting: 90, impact: 65 },
    bullets: [
      {
        text: "Migrated 40+ microservices to Kubernetes using Terraform IaC, resulting in 99.99% system availability and cutting infrastructure overhead by 22%.",
        star: { s: true, t: true, a: true, r: true },
        score: 92,
        type: "confident"
      },
      {
        text: "Configured Jenkins CI/CD automation templates to run tests automatically on git push events.",
        star: { s: true, t: false, a: true, r: false },
        score: 60,
        type: "passive"
      }
    ],
    tokens: [
      { word: "Priya", tag: "PERSON" },
      { word: "Sharma", tag: "PERSON" },
      { word: "Cloud", tag: "O" },
      { word: "Architect", tag: "O" },
      { word: "deployed", tag: "O" },
      { word: "infrastructure", tag: "O" },
      { word: "on", tag: "O" },
      { word: "AWS", tag: "ORG" },
      { word: "using", tag: "O" },
      { word: "Terraform", tag: "SKILL" },
      { word: "and", tag: "O" },
      { word: "Docker", tag: "SKILL" }
    ]
  },
  {
    name: "Arjun Patel",
    role: "Frontend Architect",
    score: 92,
    summary: "Principal Frontend Developer focused on crafting performant, visually spectacular user interfaces with high-end animations and interactive 3D WebGL scenes.",
    skills: ["React", "Next.js", "TypeScript", "TailwindCSS", "Three.js", "WebGL", "GSAP", "Framer Motion"],
    matchedSkills: ["React", "TypeScript", "TailwindCSS", "Three.js", "Framer Motion"],
    missingSkills: ["Next.js", "WebGL", "GSAP"],
    readiness: 90,
    radar: { skills: 95, experience: 90, education: 85, formatting: 95, impact: 95 },
    bullets: [
      {
        text: "Architected the core product dashboards using Next.js and Three.js, achieving 60fps animations and reducing First Contentful Paint by 40% on mid-range devices.",
        star: { s: true, t: true, a: true, r: true },
        score: 98,
        type: "confident"
      },
      {
        text: "Helped write React code components using standard design tokens and simple Tailwind CSS configs.",
        star: { s: false, t: true, a: true, r: false },
        score: 55,
        type: "passive"
      }
    ],
    tokens: [
      { word: "Arjun", tag: "PERSON" },
      { word: "Patel", tag: "PERSON" },
      { word: "engineered", tag: "O" },
      { word: "UI", tag: "O" },
      { word: "with", tag: "O" },
      { word: "React", tag: "SKILL" },
      { word: "and", tag: "O" },
      { word: "Three.js", tag: "SKILL" }
    ]
  }
];

export default function AnalyzeManager() {
  const [phase, setPhase] = useState('upload'); // upload | scanning | dashboard
  const [activeProfile, setActiveProfile] = useState(null);
  const [scanProgress, setScanProgress] = useState(0);
  const [scanMessage, setScanMessage] = useState('');

  const messages = [
    { threshold: 10, text: 'Opening file stream...' },
    { threshold: 30, text: 'Running spaCy sentence tokenization...' },
    { threshold: 55, text: 'Parsing Named Entities (NER model)...' },
    { threshold: 75, text: 'Vectorizing text into semantic embedding space...' },
    { threshold: 90, text: 'Computing STAR compliance metrics...' },
    { threshold: 100, text: 'Finalizing report...' }
  ];

  const handleStartAnalysis = (filename, profile) => {
    setActiveProfile(profile);
    setPhase('scanning');
    setScanProgress(0);
  };

  useEffect(() => {
    if (phase !== 'scanning') return;

    const interval = setInterval(() => {
      setScanProgress((prev) => {
        const next = prev + 4;
        if (next >= 100) {
          clearInterval(interval);
          setTimeout(() => setPhase('dashboard'), 600);
          return 100;
        }
        
        // Find matching status message
        const matched = messages.find(m => next <= m.threshold);
        if (matched) {
          setScanMessage(matched.text);
        }

        return next;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [phase]);

  if (phase === 'upload') {
    return <UploadFlow onStartAnalysis={handleStartAnalysis} presets={PRESETS} />;
  }

  if (phase === 'scanning') {
    return (
      <div className="mx-auto max-w-xl text-center py-20">
        <div className="glass-card relative border border-white/10 overflow-hidden">
          <div className="laser-sweep absolute inset-0 pointer-events-none"></div>
          
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2.0" stroke="currentColor" className="w-6 h-6 animate-spin">
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
          </div>

          <h2 className="text-xl font-bold font-display text-white mb-2">Analyzing Resume DNA</h2>
          <p className="text-xs text-white/50 mb-8 font-mono">{scanMessage}</p>

          {/* Progress bar */}
          <div className="w-full bg-white/5 border border-white/5 h-2.5 rounded-full overflow-hidden mb-3">
            <div 
              className="h-full bg-gradient-to-r from-violet-600 to-cyan-500 rounded-full transition-all duration-100 ease-out" 
              style={{ width: `${scanProgress}%` }}
            ></div>
          </div>
          <div className="flex justify-between items-center text-[10px] text-white/40 font-mono">
            <span>Progress</span>
            <span>{scanProgress}%</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ResultsDashboard 
      profile={activeProfile} 
      onReset={() => setPhase('upload')} 
    />
  );
}
