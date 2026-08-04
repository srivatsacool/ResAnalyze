import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function FloatingChatBubble() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hello! I am the ResAnalyze AI. Upload your resume on the Analyze page, or paste a job description on the Suggestions page, and I can give you live feedback!' }
  ]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      let aiText = "I can help you review your resume. Try going to the Analyze page to scan it first, and then I'll be able to tell you exactly how to improve your score!";
      if (userMessage.toLowerCase().includes('score') || userMessage.toLowerCase().includes('ats')) {
        aiText = "Your ATS score is computed using semantic alignment (embeddings) and entity extraction (NER) matched against industry standards. A STAR compliance check is also run on your bullet points.";
      } else if (userMessage.toLowerCase().includes('job') || userMessage.toLowerCase().includes('match')) {
        aiText = "On the Suggestions page, you can paste any job description. I'll highlight matched skills in green and missing gaps in pulsing red, drawing live connection lines!";
      } else if (userMessage.toLowerCase().includes('notebook') || userMessage.toLowerCase().includes('docs')) {
        aiText = "Our Docs page outlines the notebook structure (00-54) explaining exactly how we tokenized the text, computed TF-IDF weights, and calculated cosine similarity vectors.";
      }
      setMessages((prev) => [...prev, { role: 'assistant', text: aiText }]);
    }, 1000);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 50 }}
            transition={{ type: 'spring', damping: 20 }}
            className="glass mb-4 flex h-[450px] w-[350px] flex-col overflow-hidden rounded-3xl border border-white/10 shadow-2xl shadow-black/50"
          >
            {/* Header */}
            <div className="flex items-center justify-between bg-gradient-to-r from-violet-900/40 to-cyan-900/40 px-5 py-4 border-b border-white/5">
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
                <span className="font-semibold text-sm text-white">ResAnalyze AI Assistant</span>
              </div>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="text-white/60 hover:text-white transition-colors cursor-pointer"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M15 3L3 15M3 3l12 12"/></svg>
              </button>
            </div>

            {/* Message Area */}
            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-xs leading-relaxed ${
                      msg.role === 'user'
                        ? 'bg-violet-600 text-white rounded-br-none'
                        : 'bg-white/5 text-white/90 border border-white/5 rounded-bl-none'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>

            {/* Input Form */}
            <form onSubmit={handleSend} className="p-3 border-t border-white/5 bg-black/20 flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask something..."
                className="flex-1 rounded-xl bg-white/5 px-4 py-2 text-xs text-white placeholder-white/30 border border-white/10 focus:outline-none focus:border-cyan-500/50"
              />
              <button
                type="submit"
                className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-r from-violet-600 to-cyan-500 text-white hover:scale-105 transition-transform cursor-pointer"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M1 8h14M9 2l6 6-6 6"/></svg>
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Button */}
      <motion.button
        whileHover={{ scale: 1.08 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-tr from-violet-600 to-cyan-500 text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/30 cursor-pointer border border-white/15"
      >
        {isOpen ? (
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6"><path d="M18 6 6 18M6 6l12 12"/></svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        )}
      </motion.button>
    </div>
  );
}
