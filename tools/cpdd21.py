#!/usr/bin/env python3
"""Build tools/cpdd21.json: every 21CC tag the CPDD guides themselves give, unit by unit (31 Oct 2026).
TL: the MOE-initiatives column (கல்வியமைச்சின் முயற்சிகள்) of each activity row in the 23 unit overviews (கண்ணோட்டம், Word).
CL: the 教师手册 appendix (附录三 21世纪技能在教材中的落实) works one unit per Sec 1 and Sec 3 guide; Sec 2 and 4 guides print the goals table only.
ML: the only 21CC notes in any Panduan Guru are "Penerapan Kemahiran Abad ke-21" boxes in the G1 Sec 4 guide (Units 1-3).
Run on the department Mac with the drive mounted: python3 tools/cpdd21.py
"""
import zipfile, re, glob, os, unicodedata, json, pathlib
import xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent
DRIVE = "/Volumes/Expansion/Kai Xin Work/BVSS MTL T&L/2026/CPDD resources (2021 Syllabus)/"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
N = lambda s: unicodedata.normalize("NFC", s)
MARK = re.compile(r"21\s*-?\s*ஆம்\s*நூ|21CC|நூற்றாண்டு|மனவுணர்வு")
ICT = re.compile(r"தகவல்\s*தொடர்புத்\s*தொழில்நுட்ப[^–\-|]*(–\s*[^|]*)?")
# Tamil wording -> MOE 21CC domain, and the BVSS E21CC area when the guide names the specific competency
def classify_tl(text):
    t = ICT.sub(" ", text)
    out = {}
    if re.search(r"நுண்ணாய்வு|திறனாய்வுச்\s*சிந்தனை|புத்தாக்க|படைப்பாக்கச்\s*சிந்தனை|தகவமை|சிக்கலுக்குத்\s*தீர்வு|பிரச்சினைகளுக்குத்\s*தீர்வு|பரந்த\s*மனப்பான்மை", t): out["CAIT"] = []
    # "நுண்ணாய்வுச் சிந்தனையும் புத்தாக்கச் சிந்தனையும்" is the older MOE name of the whole CAIT domain (Critical and Inventive
    # Thinking), so it does not by itself point to Inventive Thinking; that needs the competency named alone, or problem solving.
    critical = re.search(r"நுண்ணாய்வு|திறனாய்வுச்\s*சிந்தனை", t)
    if re.search(r"தீர்வு\s*காணும்|பிரச்சினைகளுக்குத்\s*தீர்வு", t) or (re.search(r"புத்தாக்க|படைப்பாக்கச்\s*சிந்தனை", t) and not critical): out["CAIT"].append("PA_IT")
    if re.search(r"தகவமை", t): out["CAIT"].append("PA_AT")
    if re.search(r"கருத்துப்பரிமாற்ற|தகவல்\s*(அறிவு|திறன்|சார்|மற்றும்)|உடனிணைந்து|தொடர்பிணைப்பு|கூடிக்கற்றல்", t):
        out["CCIS"] = ["PA_CM"] if re.search(r"கருத்துப்பரிமாற்ற|பரிமாற்றத்\s*திறன்", t) else []
    if re.search(r"குடியிய|உலகளாவிய|பல்லின|அக்கறைகொண்ட\s*குடிமகன்", t):
        out["CGC"] = ["PA_CL"] if re.search(r"குடியிய|அக்கறைகொண்ட\s*குடிமகன்", t) else []
    if re.search(r"சுய\s*விழிப்புணர்வு|சமூக\s*விழிப்புணர்வு|மனவுணர்வு|உறவுநிலை|பொறுப்பான\s*முறையில்\s*முடிவெடு|சுய\s*மேலாண்மை|பரிவு", t): out["SEC"] = []
    if ICT.search(text): out["DIG"] = []
    return out
units = {}
def put(L, c, s, b, u, k, pas, src):
    e = units.setdefault(f"{L}|{c}|{s}|{b}|{u}", {})
    x = e.setdefault(k, {"pa": [], "src": [], "pasrc": {}})
    for p in pas:
        if p not in x["pa"]: x["pa"].append(p)
        x["pasrc"].setdefault(p, src)
    if src not in x["src"]: x["src"].append(src)
# ---- TL ----
for f in sorted(glob.glob(DRIVE + "TL Teachers Guide/*/*.docx")):
    if os.path.basename(f).startswith("._"): continue
    fol = os.path.basename(os.path.dirname(f)); sec = int(fol[0]); crs = {"G1":"G1","G2":"G2","G3":"G3","HT":"H"}[fol[1:3]]
    m = re.search(r"\b([12][AB])\b", N(os.path.basename(f))); book = m.group(1) if (m and sec <= 2) else ""
    root = ET.fromstring(zipfile.ZipFile(f).read("word/document.xml")); act = None
    for tr in root.iter(W + "tr"):
        cells = [N("".join(t.text or "" for t in tc.iter(W + "t")).strip()) for tc in tr.findall(W + "tc")]
        a = next((c for c in cells if re.fullmatch(r"\d{1,2}\.\d{1,2}", c)), None)
        if a: act = a
        if not act: continue
        for c in cells:
            if not MARK.search(c): continue
            for k, pas in classify_tl(c).items():
                put("TL", crs, sec, book, act.split(".")[0], k, pas, "activity " + act + ": " + " ".join(c.split())[:160])
# ---- CL: appendix worked examples (codes printed in the guide) ----
for c, b1 in (("G1","1上"),("G2","1上"),("G3","1A"),("H","1A")):
    for k, pas, code in (("CCIS",["PA_CM"],"CCI 1.3"),("CCIS",[],"CCI 5.3"),("CGC",["PA_CL"],"CGC 1.3")):
        put("CL", c, 1, b1, "3", k, pas, f"教师手册 附录三 worked example 《相约狮城》: {code}")
    for k, pas, code in (("CAIT",["PA_AT"],"CAIT 3.4"),("CAIT",["PA_IT"],"CAIT 5.4"),("CCIS",["PA_CM"],"CCI 2.4")):
        put("CL", c, 3, "", "6", k, pas, f"教师手册 附录三 worked example 《发现真善美》: {code}")
# ---- ML: G1 Sec 4 Panduan Guru notes ----
put("ML","G1",4,"","1","DIG",[],"Panduan Guru: Penerapan Kemahiran Abad ke-21 (Literasi Digital), two notes")
put("ML","G1",4,"","2","CGC",["PA_CL"],"Panduan Guru: Penerapan Kemahiran Abad ke-21 (Literasi Sivik), two notes")
put("ML","G1",4,"","3","CGC",[],"Panduan Guru: Penerapan Kemahiran Abad ke-21 (Literasi Silang Budaya)")
(ROOT / "tools" / "cpdd21.json").write_text(json.dumps({"_readme": __doc__.strip(), "units": units}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(units), "units with CPDD 21CC tags")
