# Verify actual behavior of key code cells from block_e notebooks (venv python)
import sys, os, tempfile

print("=== ch26 cell5: fpdf + pdfplumber ===")
try:
    from fpdf import FPDF
    import pdfplumber
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, text="Srivatsa Gorti", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, text="srivatsa@email.com", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Arial", style="B", size=11)
    pdf.cell(200, 10, text="PROFESSIONAL SUMMARY", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, text="Data scientist with 5+ years of Python, NLP, and ML experience.")
    pdf.set_font("Arial", style="B", size=11)
    pdf.cell(200, 10, text="EXPERIENCE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, text="Google — Senior Data Scientist, 2020-Present", new_x="LMARGIN", new_y="NEXT")
    test_pdf = os.path.join(tempfile.gettempdir(), "test_resume.pdf")
    pdf.output(test_pdf)
    print(f"PDF created: {os.path.getsize(test_pdf)} bytes")
    with pdfplumber.open(test_pdf) as pdfp:
        for i, page in enumerate(pdfp.pages):
            text = page.extract_text() or ""
            print(f"\nPage {i+1}:\n{text[:200]}")
except Exception as e:
    print(f"ch26 FAILED: {type(e).__name__}: {e}")

print("\n=== ch29 cell4: ResumeNormalizer ===")
import re, unicodedata
class ResumeNormalizer:
    def normalize(self, text):
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode()
        text = re.sub(r"[\u2022\u2023\u25cf\u25d8\u25c9\u279c]", ">", text)
        text = re.sub(r"\t|\r", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)
        return text.strip()
n = ResumeNormalizer()
sample = "Srivatsa Gorti\n\u2022 Python specialist\n\u2022 NLP engineer\n\tTensorFlow expert"
print(f"Before: {repr(sample)}")
print(f"After:  {repr(n.normalize(sample))}")
# accent check
print(f"Accent: {n.normalize('Café résumé — Sr.')}")

print("\n=== ch29 cell6: expand ===")
abbrev_map = {
    "sr.": "senior", "jr.": "junior", "dr.": "doctor",
    "engr.": "engineer", "mgr.": "manager", "dir.": "director",
    "w/": "with", "&": "and",
    "exp.": "experience", "yrs": "years", "yr": "year",
}
def expand(text):
    pat = re.compile(r"\b(" + "|".join(re.escape(k) for k in abbrev_map) + r")\b", re.IGNORECASE)
    return pat.sub(lambda m: abbrev_map[m.group(0).lower()], text)
print(expand("Sr. ML Engr. w/ 10+ yrs exp."))
print(expand("B.Tech CSE & M.S. Data Science"))
print(expand("Srivatsa Gorti"))  # false-positive check

print("\n=== ch30 cell2: langdetect ===")
try:
    from langdetect import detect, detect_langs
    texts = [
        ("English", "I have experience in Python and machine learning"),
        ("French", "J'ai de l'experience en Python et machine learning"),
        ("German", "Ich habe Erfahrung mit Python und maschinellem Lernen"),
    ]
    for expected, text in texts:
        lang = detect(text)
        probs = detect_langs(text)
        ok = "OK" if lang == expected[:2].lower() else " "
        print(f"  {ok} {expected:10s} -> {lang} (top: {probs[0]})")
except Exception as e:
    print(f"ch30 FAILED: {type(e).__name__}: {e}")

print("\n=== ch31 cell4: detect_type ===")
def detect_type(filepath):
    sigs = {b'%PDF': 'pdf', b'PK\x03\x04': 'docx', b'\x89PNG': 'png', b'\xff\xd8\xff': 'jpg'}
    with open(filepath, 'rb') as f:
        h = f.read(4)
    for sig, t in sigs.items():
        if h.startswith(sig): return t
    return 'unknown'
with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
    f.write(b'%PDF-1.4 fake')
    fn = f.name
print(f"File: {fn}")
print(f"Detected: {detect_type(fn)} (vs extension: .pdf)")
os.unlink(fn)
# mismatch case: .pdf that is really a zip
with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
    f.write(b'PK\x03\x04 fake')
    fn2 = f.name
print(f"Fake .pdf containing ZIP magic -> {detect_type(fn2)}")
os.unlink(fn2)

print("\n=== ch28 cell4: pytesseract without binary ===")
try:
    import pytesseract
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
    draw.text((20, 20), "Srivatsa Gorti", fill='black', font=font)
    draw.text((20, 60), "Senior Data Scientist", fill='black', font=font)
    draw.text((20, 100), "Python, NLP, TensorFlow", fill='black', font=font)
    img.save(os.path.join(tempfile.gettempdir(), "test_resume.png"))
    text = pytesseract.image_to_string(img)
    print("=== OCR Result ===")
    print(text)
except ImportError:
    print("Install: pip install pytesseract pillow")
except Exception as e:
    print(f"OCR error: {e} (needs Tesseract system install)")

print("\n=== ch30 cell4: select_pipeline ===")
LANG_MODELS = {"en": "en_core_web_sm", "fr": "fr_core_news_sm", "de": "de_core_news_sm", "es": "es_core_news_sm"}
def select_pipeline(text):
    from langdetect import detect
    lang = detect(text) if text.strip() else "en"
    return LANG_MODELS.get(lang, "en_core_web_sm")
for text in ["I love Python", "J'adore Python", "Ich liebe Python"]:
    print(f"  '{text}' -> load {select_pipeline(text)}")
