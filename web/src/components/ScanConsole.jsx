import React, { useEffect, useRef, useCallback } from 'react';

const CIRC = 2 * Math.PI * 34;

const LINES = [
  { text: 'Srivatsa Gorti', entity: 'PERSON', color: '#818CF8' },
  { text: 'Senior Data Engineer — Engine Assembly', entity: null },
  { text: 'Tata Motors Ltd · Jamshedpur', entity: 'ORG', color: '#38BDF8' },
  { text: 'Jun 2024 — Aug 2024', entity: 'DATE', color: '#6B6B80' },
  { text: '▸ Built ETL pipelines · PySpark, Airflow, dbt', entity: 'SKILL', color: '#818CF8' },
  { text: '▸ Cut defect-report latency by 38%', entity: null },
  { text: '▸ Led Databricks migration · 15-node cluster', entity: 'SKILL', color: '#818CF8' },
];

const METRICS = [
  { label: 'ATS MATCH', value: 87, color: '#F0C246' },
  { label: 'KEYWORDS', value: 84, color: '#818CF8' },
  { label: 'READABILITY', value: 91, color: '#38BDF8' },
];

export default function ScanConsole() {
  const cardRef = useRef(null);
  const areaRef = useRef(null);
  const scanLineRef = useRef(null);
  const chipRefs = useRef([]);
  const lineRefs = useRef([]);
  const ringRef = useRef(null);
  const scoreRef = useRef(null);
  const barRefs = useRef([]);
  const rafRef = useRef(null);
  const litSet = useRef(new Set());

  const reduced =
    typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── gauge with score scramble ── */
  useEffect(() => {
    const ring = ringRef.current;
    const score = scoreRef.current;
    if (!ring || !score) return;

    const drawGauge = () => {
      const t0 = performance.now();
      const dur = 1200;
      const scrambleEnd = 300;
      const step = (now) => {
        const elapsed = now - t0;
        const p = Math.min(elapsed / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        ring.style.strokeDashoffset = CIRC * (1 - eased * 0.87);

        if (elapsed < scrambleEnd) {
          score.textContent = String(Math.floor(Math.random() * 100));
          score.style.opacity = '0.7';
        } else {
          score.textContent = String(Math.round(eased * 87));
          score.style.opacity = '1';
        }
        if (p < 1) rafRef.current = requestAnimationFrame(step);
      };
      rafRef.current = requestAnimationFrame(step);
    };

    barRefs.current.forEach((el) => {
      if (el) el.style.width = `${el.dataset.w}%`;
    });

    if (reduced) {
      ring.style.strokeDashoffset = CIRC * (1 - 0.87);
      score.textContent = '87';
      return;
    }
    drawGauge();
    return () => cancelAnimationFrame(rafRef.current);
  }, []);

  /* ── annotation scan with stutter ── */
  const scanRef = useRef({ progress: -12, hold: 0, zones: [] });
  const lastTRef = useRef(0);

  const chipTops = useCallback(() => {
    const area = areaRef.current;
    if (!area) return [];
    const a = area.getBoundingClientRect();
    return chipRefs.current.map((c) => {
      if (!c) return -1;
      const r = c.getBoundingClientRect();
      return ((r.top - a.top + r.height / 2) / a.height) * 100;
    });
  }, []);

  const genZones = () => {
    const n = 4 + Math.floor(Math.random() * 3); // 4-6 zones per pass
    const z = [];
    for (let i = 0; i < n; i++) {
      const pos = Math.random() * 116 - 12; // -12 to 104
      const w = 1.5 + Math.random() * 3;     // zone width 1.5-4.5%
      z.push({ pos, w, slow: 1.5 + Math.random() * 3 });
    }
    return z;
  };

  const tick = (now) => {
    const s = scanRef.current;
    if (!lastTRef.current) lastTRef.current = now;
    const dt = Math.min((now - lastTRef.current) / 1000, 0.05);
    lastTRef.current = now;

    if (s.hold > 0) {
      s.hold -= dt;
      rafRef.current = requestAnimationFrame(tick);
      return;
    }

    // stutter: slow near entity lines + random zones
    const tops = chipTops();
    let speed = 24;
    for (let i = 0; i < tops.length; i++) {
      if (Math.abs(s.progress - tops[i]) < 2.5) {
        speed = Math.min(speed, 3);
        break;
      }
    }
    for (let i = 0; i < s.zones.length; i++) {
      const z = s.zones[i];
      if (Math.abs(s.progress - z.pos) < z.w) {
        speed = Math.min(speed, z.slow);
        break;
      }
    }
    // micro jitter: random brief dips
    if (Math.random() < 0.08) {
      speed *= 0.3 + Math.random() * 0.4;
    }
    s.progress += speed * dt;

    if (s.progress > 104) {
      s.progress = -12;
      s.hold = 1.2;
      s.zones = genZones();
      litSet.current.clear();
      chipRefs.current.forEach((c) => c && c.classList.remove('lit'));
      lineRefs.current.forEach((l) => {
        if (l) {
          l.classList.remove('glitch-active');
          l.style.transform = '';
        }
      });
      rafRef.current = requestAnimationFrame(tick);
      return;
    }

    chipRefs.current.forEach((c, i) => {
      if (!c) return;
      if (s.progress >= tops[i] - 2 && !litSet.current.has(i)) {
        litSet.current.add(i);
        c.classList.add('lit');
        // RGB split flash on the line
        const line = lineRefs.current[i];
        if (line) {
          line.classList.add('glitch-active');
          setTimeout(() => line.classList.remove('glitch-active'), 220);
        }
      }
    });
    if (scanLineRef.current) scanLineRef.current.style.top = `${s.progress}%`;
    rafRef.current = requestAnimationFrame(tick);
  };

  const startScan = useCallback(() => {
    if (reduced) return;
    cancelAnimationFrame(rafRef.current);
    const s = scanRef.current;
    s.progress = -12;
    s.hold = 0;
    s.zones = genZones();
    litSet.current.clear();
    chipRefs.current.forEach((c) => c && c.classList.remove('lit'));
    lineRefs.current.forEach((l) => {
      if (l) {
        l.classList.remove('glitch-active');
        l.style.transform = '';
      }
    });
    lastTRef.current = 0;
    rafRef.current = requestAnimationFrame(tick);
  }, [reduced]);

  useEffect(() => {
    if (reduced) return;
    const t = setTimeout(startScan, 500);
    return () => {
      clearTimeout(t);
      cancelAnimationFrame(rafRef.current);
    };
  }, [startScan]);

  /* ── random micro-glitch on lines ── */
  useEffect(() => {
    if (reduced) return;
    let timeout;
    const glitch = () => {
      const lines = areaRef.current?.children;
      if (lines && lines.length > 0) {
        const i = Math.floor(Math.random() * lines.length);
        const el = lines[i];
        if (el) {
          const dx = (Math.random() > 0.5 ? 1 : -1) * (1 + Math.random());
          el.style.transform = `translateX(${dx}px)`;
          el.style.opacity = '0.82';
          setTimeout(() => {
            el.style.transform = '';
            el.style.opacity = '';
          }, 80 + Math.random() * 60);
        }
      }
      timeout = setTimeout(glitch, 2800 + Math.random() * 3200);
    };
    timeout = setTimeout(glitch, 1500);
    return () => clearTimeout(timeout);
  }, [reduced]);

  /* ── subtle tilt ── */
  const onMouseMove = (e) => {
    const card = cardRef.current;
    if (!card || reduced) return;
    const rect = card.getBoundingClientRect();
    const rx = ((e.clientY - rect.top) / rect.height - 0.5) * -2;
    const ry = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
    card.style.transform = `perspective(1200px) rotateX(${rx}deg) rotateY(${ry}deg)`;
  };
  const onMouseLeave = () => {
    if (cardRef.current) cardRef.current.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg)';
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
      className="analysis-card rounded-2xl border border-white/[0.06] bg-[#0C0C14] transition-transform duration-200 ease-out will-change-transform"
    >
      {/* document area */}
      <div ref={areaRef} className="relative px-6 py-5 font-mono text-[12.5px] leading-[1.9]">
        <div ref={scanLineRef} className="scan-line" aria-hidden="true" />
        {LINES.map((line, i) => (
          <div
            key={i}
            ref={(el) => (lineRefs.current[i] = el)}
            className="scan-line-row flex items-baseline justify-between gap-3 transition-transform duration-75"
          >
            <span className="text-[#C8C8D4]">{line.text}</span>
            {line.entity ? (
              <span
                ref={(el) => (chipRefs.current[i] = el)}
                className="entity-label"
                style={{ color: line.color }}
              >
                {line.entity}
              </span>
            ) : (
              <span />
            )}
          </div>
        ))}
      </div>

      {/* score + metrics */}
      <div className="border-t border-white/[0.06] px-6 py-4">
        <div className="flex items-center gap-6">
          <div className="relative h-16 w-16 shrink-0" role="img" aria-label="ATS match score 87 out of 100">
            <svg className="gauge-ring h-full w-full" viewBox="0 0 80 80">
              <circle cx="40" cy="40" r="34" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="5" />
              <circle
                ref={ringRef}
                cx="40" cy="40" r="34"
                fill="none" stroke="#F0C246" strokeWidth="5"
                strokeLinecap="round"
                strokeDasharray={CIRC}
                strokeDashoffset={CIRC}
                style={{ filter: 'drop-shadow(0 0 4px rgba(240,194,70,0.4))' }}
              />
            </svg>
            <div className="absolute inset-0 grid place-items-center">
              <span ref={scoreRef} className="font-mono text-lg font-bold text-[#F0C246] tabular-nums">0</span>
            </div>
          </div>
          <div className="min-w-0 flex-1 space-y-2">
            {METRICS.map((s) => (
              <div key={s.label}>
                <div className="mb-1 flex justify-between font-mono text-[10px] tracking-wide text-[#6B6B80]">
                  <span>{s.label}</span>
                  <span style={{ color: s.color }}>{s.value}</span>
                </div>
                <div className="h-[2px] overflow-hidden rounded-full bg-white/[0.06]">
                  <div
                    ref={(el) => barRefs.current.push(el)}
                    className="stat-fill h-full rounded-full"
                    style={{ backgroundColor: s.color }}
                    data-w={s.value}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* re-run */}
      <button
        type="button"
        onClick={startScan}
        title="Re-run analysis"
        aria-label="Re-run analysis"
        className="absolute bottom-4 right-4 grid h-7 w-7 place-items-center rounded-full border border-white/[0.08] bg-white/[0.03] text-[#6B6B80] transition-colors hover:border-[#818CF8]/40 hover:text-[#818CF8]"
      >
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 12a9 9 0 1 1-2.64-6.36" />
          <polyline points="21 3 21 9 15 9" />
        </svg>
      </button>
    </div>
  );
}
