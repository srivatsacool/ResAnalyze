# ResAnalyze Website Plan

## Project Overview
Interactive NLP-powered resume analysis platform showcasing the full pipeline from text parsing to ATS scoring, with cinematic visualizations — all built with glassmorphic UI and interactive 3D elements.

---

## Tech Stack

| Layer | Choice |
|---|---|
| **Framework** | Astro |
| **3D** | react-three-fiber (real-time WebGL, not prerendered video) |
| **UI** | React islands + Tailwind CSS |
| **Styling** | Tailwind + custom glassmorphism utilities |
| **Fonts** | Space Grotesk (display) + Inter (body) |
| **Deploy** | Vercel |

---

## Design System (Global)

### Color Palette
| Role | Value |
|---|---|
| Background | `#0a0a0f` → radial gradient (center lighter) |
| Glass Panel | `rgba(255,255,255,0.08)` with `backdrop-blur-3xl` |
| Accent Gradient | `violet (#7c3aed) → cyan (#22d3ee) → gold (#f59e0b)` |
| NEO accent | Cyan-blue — `#06b6d4` |
| Text | `#f8fafc` (primary), `#ffffff90` (secondary) |
| Borders | `rgba(255,255,255,0.08)` |

### Glassmorphism Utilities (Tailwind plugin)
```ts
// tailwind.config.ts — custom glass utilities
export default {
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.glass': {
          'background': 'rgba(255,255,255,0.06)',
          'backdrop-filter': 'blur(20px)',
          'border': '1px solid rgba(255,255,255,0.08)',
          'box-shadow': 'inset 0 1px 0 rgba(255,255,255,0.1), 0 1px 2px rgba(0,0,0,0.3)',
        },
        '.glass-card': {
          '@apply glass rounded-3xl p-8': {},
        },
      })
    }),
  ]
}
```

### Typography
- Display/Headings: `Space Grotesk` (variable font)
- Body: `Inter`
- Code: `JetBrains Mono`

---

## Pages & Structure

### 1. Landing Page (`/`)

#### Hero Section — Interactive 3D NLP Pipeline
**Live interactive WebGL scene** (react-three-fiber), not a video:

- **3D Resume Document** floats in center (glassmorphic plane with real text). Users can:
  - Grab & rotate (orbit controls)
  - Hover over words → they highlight
  - Click a word → fly-to and show details (POS, lemma, embedding)

- **5 Pipeline Stages** (clickable tabs on the side):
  1. **Tokenization**: Words peel off document on hover, floating as interactive 3D tags
  2. **NER**: Entities auto-color + group → person=BLUE, org=GREEN, skill=ORANGE, date=PURPLE
  3. **BoW**: Bar chart rises from document (interactive — hover bars for frequency)
  4. **Embeddings**: Semantic constellation (points with connecting lines — hover for similarity score)
  5. **Scoring**: Ring expands + fills; click for detailed breakdown

- **Mouse Parallax**: Scene responds subtly to cursor position
- **CTA Button**: "Analyze Your Resume →" with hover pulse animation

#### Features Section
- 3-column card grid (glass-morphic panels, hover lift)
- **Live Demo Ticker** at bottom — marquee of anonymized score animations

### 2. Analyze Page (`/analyze`)

#### Upload Flow
- Drag & drop zone with **scanning laser-line animation** (CSS gradient sweep)
- Progress stages: `Parsing → Extracting → Scoring` (animated step indicator)
- File type support badges: PDF, DOCX, TXT, Image (OCR)

#### Results Dashboard
Dashboard has these **interactive glass panels** arranged in a responsive grid:

1. **Score Reveal Central Panel**
   - 3D gradient torus ring fills from 0 → score (60fps animation)
   - Count-up number with elastic ease
   - Confetti burst on reveal (canvas-confetti)
   - Sub-score: Interview Readiness Score (STAR compliance — shown as a smaller ring inside)

2. **Resume DNA Helix** *(react-three-fiber)*
   - Interactive double helix (user skills = teal strands, JD requirements = gold strands)
   - Missing links = broken red pulse animation
   - Mouse drag to rotate helix

3. **Resume X-Ray Toggle**
   - Split view: formatted resume ↔ raw ATS-parsed tokens
   - ATS view highlights keyword hits in **glowing green**, misses in **pulsing red**
   - Toggle button with smooth transition

4. **Skill Matrix**
   - Chip cloud with hover tooltips showing confidence (0.0–1.0)
   - Chips light up green (matched), amber (partial), red (missing)

5. **Emotion & Confidence Heatmap**
   - Each bullet bar is color-coded: gold (confident), blue (passive), red (arrogant)
   - Hover any bullet → see detailed sentiment breakdown

6. **NLP Explorer Tab Panel** ← Tabs: Tokens / Word Cloud / Embeddings
   - **Tokens tab**: Syntax-highlighted document, clickable for POS/NER details
   - **Word Cloud tab**: 3D spinning word cloud (react-three-fiber) — size = frequency
   - **Embeddings tab**: 2D t-SNE scatter plot + hover for similarity neighbors

7. **Bullet Quality Scoring**
   - Table: each bullet with star_score, has_metric, has_action_verb, weakness_flags
   - Click a bullet → "Power Verb Forge" recommendation modal pops up

### 3. Suggestions & Live Matching (`/suggest`)

#### Live Job Match Engine
- Textarea: "Paste job description" → auto-parses on blur
- Split screen: Resume (left) | Job JD (right)
- **Animated connecting lines** appear between matched pairs (green = strong, yellow = weak, red = missing)
- Real-time match % at the top

#### Before/After Rewrite Slider
- Horizontal slider (noUiSlider) splits a bullet
- Left = original, Right = AI-enhanced STAR-formatted version
- Live score delta indicator ("+0.3 STAR score")

#### Power Verb Forge
- Workshop text input at the bottom
- **Forging animation** (CSS anvil + hammer + sparks) on submit
- Output: upgraded bullet + explanation of changes

#### Ghost Mode Toggle
- Switch enables "benchmark mode"
- Top 5 anonymized resumes from same industry fade in as translucent overlays on your document

#### Role Pivot Calculator
- Dropdown: "Current target role" vs "Alternative role"
- Radar chart animates showing transferable skills vs new gaps

#### Gap Analysis
- Severity meters (low/med/high) for each skill category
- Ranked action cards (glass panels, click to expand details)

### 4. Documentation & Developer Space (`/docs`)

#### Notebook Reference (00–54)
- Filterable grid of notebook cards (search, block filter, tags)
- Each card: title, 1-line description, "Run in Colab" + "View on GitHub" buttons

#### Architecture Diagrams
- SVG diagrams: shared/ package → FastAPI + MCP — interactive (click nodes for contract details)

#### API Reference
- Auto-generated OpenAPI spec, collapsible endpoints

#### Terminal Mode Easter Egg
- `Ctrl + ~` toggles a `<pre>` terminal-style overlay
- Shows raw parsing logs (regex hits, NER entities, embedding dims) in green-on-black ASCII

### 5. Chat & Sharing (`/chat`)

#### Floating Chat Bubble
- Fixed bottom-right (glass-morphic, subtle pulse on load)
- MCP-backed assistant: "Why did my resume score 72?" → returns grounded answer
- Chat window slides up (framer-motion)

#### Resume Fingerprint Card
- Button "Generate Share Card" → creates a generative-art SVG based on your score vector
- Preview modal + PNG download + "Share to LinkedIn" (opens share dialog)

---

## 3D / Interactive Elements Guide

| Element | Location | Interaction Type |
|---|---|---|
| Floating Resume Document | Hero | Grab/rotate, word hover/click |
| Pipeline stage previews | Hero tabs | Click to activate stage animation |
| Resume-DNA-Helix | Analyze | Mouse-drag rotate, missing-link pulse |
| X-Ray split-view | Analyze | Toggle switch, hover keyword highlights |
| Word Cloud | Analyzer tab | Click to spin, hover for frequency |
| Embedding constellation | Analyzer tab | Hover for nearest-neighbor lines |
| Job Match connecting lines | Suggest | Auto-draw on JD paste |
| Before/After slider | Suggest | Drag for comparison |
| Anvil forging animation | Power Verb Forge | Trigger on submit |

---

## Performance Strategy

- **Astro islands**: 3D scenes only mount when scrolled into view (`IntersectionObserver`)
- **Lazy 3D**: heavy components (`react-three/fiber` scenes) load on interaction
- **Code splitting**: each Analyze tab panel is its own lazy chunk
- **Asset optimization**: GLB models compressed, Web Workers for heavy parsing
- **`loading="lazy"` + blur-up placeholders** for all images
- **Minimal global JS**: glassmorphism effects purely via Tailwind/CSS

---

## Development Roadmap (MVP → Polished)

| Milestone | Focus |
|---|---|
| **v1** | Hero scene, analyze upload, score ring, basic dashboard |
| **v2** | DNA helix, X-ray toggle, NLP explorer tabs |
| **v3** | Live Job Match, Power Verb Forge, Ghost Mode |
| **v4** | Chat bubble, Terminal easter egg, Share card export |

---

## File Structure (Scaffold)

```
src/
├── pages/
│   ├── index.astro              # Landing — Hero + Features + Ticker
│   ├── analyze.astro            # Upload + Results Dashboard
│   ├── suggest.astro            # Live Match + Recommendations
│   ├── docs.astro               # Notebook grid, architecture, API, Easter egg
│   └── chat.astro               # Share card preview + chat history
├── components/
│   ├── Hero.jsx                 # Interactive 3D pipeline (R3F)
│   ├── ScoreRing.jsx            # 3D torus + count-up + confetti
│   ├── DNAStructure.jsx         # Helix visualization
│   ├── XRayView.jsx              # Parsed vs formatted toggle
│   ├── NLPExplorer.jsx           # Tabs: tokens, wordcloud, embeddings
│   ├── LiveMatch.jsx            # JD paste + connecting lines
│   ├── VerbForge.jsx            # Anvil animation + rewrite
│   ├── GhostMode.jsx           # Benchmarking overlay
│   ├── ChatBubble.jsx          # MCP assistant floating
│   └── TerminalMode.jsx        # Retro ASCII log overlay
├── lib/
│   ├── api.ts                  # API client stubs (FastAPI later)
│   ├── three-utils.ts          # R3F helpers
│   └── animations.ts           # Shared framer-motion variants
└── styles/
    └── glass.css               # Custom glass utility overrides
```

---

## Success Metrics
- First Contentful Paint < 1.5s
- Lighthouse Performance score > 90
- 3D interactions stay at **60fps** on mid-range devices
- Zero blocking during resume uploads
