# ResAnalyze Website Plan

## Project Overview
Interactive NLP-powered resume analysis platform showcasing the full pipeline from text parsing to ATS scoring, with cinematic visualizations.

## Tech Stack
- **Frontend**: Astro + React islands (lightweight)
- **3D/Animation**:
  - Interactive WebGL/Three.js scene for Hero (or optimized pre-rendered scroll-scrubbed video, pending decision)
  - react-three-fiber for interactive Analyze page
- **Styling**: Tailwind CSS + custom glassmorphism utilities
- **Fonts**: Space Grotesk (display) + Inter (body)
- **Deployment**: Vercel (optimal for Astro)

---

## Pages & Structure

### 1. Landing Page (`/` — "Inside the NLP Engine")

#### Hero Section
- 3D resume document floating in space (react-three-fiber or scroll-scrubbed animation)
- Auto-playing or scroll-reactive animation showing the NLP pipeline:
  1. Text → Tokenization (words peel off)
  2. NER → Color-coded entity clusters
  3. BoW → 3D bar chart rising
  4. Embeddings → Semantic constellation
  5. Scoring → Animated score ring
- Scroll scrubbing/interactive controls for frame-by-frame control
- CTA: "Analyze Your Resume" → `/analyze`

#### Features Section
- Animated feature cards (glassmorphic)
- Highlight of key notebook blocks (A-I) and advanced features
- Hover reveals detailed descriptions

#### Live Demo Ticker
- Bottom of page: real-time scoring of sample resumes
- Marquee-style display with score badges

---

### 2. Analyze Page (`/analyze`)

#### Upload Flow
- Drag & drop zone with file scanning laser-line animation
- Progress indicators (parsing -> extracting -> scoring)
- Support: PDF, DOCX, TXT, image (OCR)

#### Results Dashboard
- **Score Reveal**: Count-up animation + gradient torus ring + confetti
- **Interview Readiness Score**: Additional score analyzing STAR framework compliance
- **Radar Chart**: Skills | Experience | Education | Format | Impact
- **Resume DNA Helix**: 3D double helix matching your skills (teal glow) vs target job requirements (missing links = broken red pulse)
- **Resume X-Ray Toggle**: See exactly what the ATS machine parser sees (raw tokens with keyword hits in glowing green, misses in red)
- **Emotion & Confidence Heatmap**: sentiment per bullet (gold = confident, blue = passive, red = arrogant)
- **Skill Matrix**: Interactive chips (hover -> confidence tooltips)
- **NLP Explorer Tab**:
  - Tokenized view with POS/NER highlighting
  - 3D Word Cloud (frequency = size)
  - Embedding visualization (PCA/t-SNE projection constellation)
- **Bullet Quality Scoring**: Detailed STAR breakdown

---

### 3. Suggestions & Live Matching (`/suggest`)
- **Live Job Match Engine**: Paste target job description URL -> split-screen view showing glowing connecting lines from resume bullets to matching job requirements.
- **Before/After Rewrite Slider**: Real-time slider showing bullet transformations.
- **Power Verb Forge**: Workshop tool where users paste a bullet to see an anvil/fire forging animation that upgrades weak verbs.
- **Ghost Mode (Industry Benchmarking)**: Translucent overlays of top-performing resumes in target roles to benchmark formatting and content density.
- **Role Pivot Calculator**: Shows transferrable skills and missing gaps when switching from one target role to another.
- **Gap Analysis**: Severity meters and ranked action cards.

---

### 4. Documentation & Developer Space (`/docs`)
- **Notebook Reference (00-54)**: Notebook blocks with interactive previews.
- **Architecture Diagrams**: Shared package and backend/MCP structure.
- **API Reference**: FastAPI backend endpoints.
- **Terminal Mode Easter Egg**: Keyboard shortcut (`Ctrl+~`) toggles retro-green terminal stream showing raw NLP parsing outputs.

---

### 5. Chat & Sharing (`/chat`)
- **Floating Chat Bubble**: Present on every page, MCP-backed AI assistant.
- **Resume Fingerprint Card**: Generative art graphic based on your unique resume stats (skills vector, experience density), ready for sharing on LinkedIn/Twitter.

---

## Design System

### Visual Language
- **Base**: Deep dark (`#07070f`) with reactive aurora particle background gradients (particles flow toward cursor and shift color on scroll)
- **Glass**: `backdrop-blur-xl` panels, 1px white/10 borders, soft inner glows
- **Animations**: framer-motion for UI, GSAP for scroll reveals

### Color Palette
| Role | Value / Description |
|---|---|
| Primary | Gradient: violet -> cyan -> pink |
| Secondary | Skill category colors (blue=person, green=org, orange=skill, purple=date) |
| Accent | Neon gold for highlights and CTA buttons |

### Typography
| Use | Font |
|---|---|
| Display / Headings | Space Grotesk |
| Body / Labels | Inter |
| Code / Technical | JetBrains Mono |

---

## 3D Components

### Hero (Video vs Interactive WebGL)
- Pending decision (see comparison brief).
- Either: Pre-rendered scroll-scrubbed 20-second WebM/MP4 animation.
- Or: Interactive real-time three.js / react-three-fiber scene with interactive mouse parallax.

### Analyze & Results Page (Real-time 3D)
- react-three-fiber scene.
- Interactive glassmorphic resume document.
- Floating 3D word tags and semantic point clouds.
- 3D Torus Score Ring with breathing scale animation.
- Resume DNA Helix interactive model.

---

## Performance Strategy
- Astro islands architecture (minimal JS on landing)
- Video lazy loading with low-quality placeholder (if video is used)
- 3D canvas deferred loading (only initializes when in viewport)
- Asset optimization (WebP/WebM, GLTF/GLB compression)
- Vercel Edge caching

---

## Success Metrics
- First Contentful Paint < 1.5s
- Lighthouse Performance score > 90
- Smooth 60fps on mid-range devices for 3D interactions
- Zero blocking main-thread JS during user uploads
