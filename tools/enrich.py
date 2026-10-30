#!/usr/bin/env python3
"""Enrich the embedded DATA in index.html with:
  - scope domains per unit (ML from CPDD Domain rows; CL/TL inferred from theme keywords)
  - provenance-tagged 21CC / IBL / E21CC-priority tags on every record
  - pedagogical design facts per language
Run: python3 tools/enrich.py   (idempotent: recomputes derived fields from scratch)
Provenance values: cpdd = tagged by CPDD in the guide; derived = mapped from a CPDD tag by a fixed table;
infer = assigned by a content rule (rule id recorded). Rules live in RULES below; keep them auditable.
"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
h = HTML.read_text(encoding="utf-8")
i = h.find("const DATA=") + len("const DATA=")
D, end = json.JSONDecoder().raw_decode(h[i:])

# ---------- 1. Scope domains ----------
DOM = ["self", "family", "school", "community", "nation", "world"]
# ML: Domain row of each Panduan Guru's Gambaran Keseluruhan (CPDD). Key: course, book or sec, unit.
MLD = {}
def ml(course, book, units):
    for n, s in enumerate(units.split(";"), 1 if book in ("1A", "2A", "3", "4") else 5):
        MLD[(course, book, str(n))] = [x.strip() for x in s.split(",") if x.strip()]
ml("G1","1A","school;self;self;self"); ml("G1","1B","family,community;community;self;self,community")
ml("G1","2A","self;self,family;self,family;self"); ml("G1","2B","self,community;self,family,community;self,school,community;self,family,school,community")
ml("G1","3","self,family,community;self,community;family,community;self,community;community,world;self,community,world")
ml("G1","4","self,community;self,community;self,community;self;self;self")
ml("G2","1A","school;self;self;self"); ml("G2","1B","family;self,family;self;self,school,community")
ml("G2","2A","self,school,community;self,school;self,family;self,family,school,community"); ml("G2","2B","self,school,community;self,family,school,community;self,family,community;self,family,community")
ml("G2","3","self,family,community;self,community;family,community;self,community;community,world;self,community,world")
ml("G2","4","self,community;self,community;community,world;self;self;self")
ml("G3","1A","self;self;self;self"); ml("G3","1B","self,community;self,community;self;self,community")
ml("G3","2A","self,school,community;self;self;self,community"); ml("G3","2B","self,school;self,family;self,community,world;self")
ml("G3","3","self,community;self,community;self,community,world;self,community;community;self,community,world")
ml("G3","4","self,world;self,community;self,community,world;self;self;self")
ml("H","1A","self,community,world;self,community;self;self,community"); ml("H","1B","self,community,world;self,community;self,community,world;self,community")
ml("H","2A","self,school,community;self,community;self,community,world;self,community,world"); ml("H","2B","self,community,world;self,family,community,world;self,community,world;self,community")
ml("H","3","self,community,world;self,community,world;self,community,world;self,community;community;self,community,world")
ml("H","4","self,community;self,community;community,world;self;self;self")

KW = [  # inferred from theme wording, widest first
 ("world", r"world|global|earth|planet|international|abroad|overseas|region|foreign|universe|brand-new earth|the world and us|世界|地球|环球|海外|国际"),
 ("nation", r"singapore|lion city|nation|national|red dot|citizen|country|homeland|狮城|新加坡|小红点|国家|家园|society & nation|society and nation"),
 ("community", r"communit|society|social|neighbou|cultur|heritage|tradition|custom|festival|harvest|environment|green|volunteer|public|hawker|dialect|contribution|youth|people|others|way of life|文化|社区|社会|传统|习俗|环保|绿色|贡献|邻"),
 ("school", r"school|class|cca|teacher|study|learn|exam|campus|校园|同学|学校|学习|学无止境|班"),
 ("family", r"famil|parent|reunion|home\b|grandpa|grandma|sibling|团圆|家人|家庭|父母|亲情|爱的"),
]
def infer_dom(t_en, t_m):
    s = (t_en + " " + t_m).lower()
    out = [d for d, rx in KW if re.search(rx, s)]
    return out or ["self"]
for t in D["themes"]:
    if t["lang"] == "ML":
        k = (t["course"], t["book"] or str(t["sec"]), t["unit"])
        t["dom"] = MLD.get(k, ["self"]); t["domSrc"] = "cpdd" if k in MLD else "infer"
    else:
        t["dom"] = infer_dom(t["theme_en"], t["theme_m"]); t["domSrc"] = "infer"
D["domains"] = {"keys": DOM, "en": {"self":"Self","family":"Family","school":"School","community":"Community & culture","nation":"Nation (Singapore)","world":"World & region"},
 "note": "ML domains are the Domain row of each JATi Panduan Guru (CPDD). CL and TL domains are inferred from the unit theme wording by keyword rules in tools/enrich.py; a unit can carry more than one."}

# ---------- 2. Provenance-tagged 21CC / IBL / E21CC priority tags ----------
D["cat"].update({
 "PA_AT": {"lens":"pri","en":"Adaptive Thinking","zh":"适应性思维","ms":"Pemikiran adaptif","ta":"தகவமைப்புச் சிந்தனை","desc":"confident without established answers, resilient in failure, responds nimbly to changing contexts"},
 "PA_IT": {"lens":"pri","en":"Inventive Thinking","zh":"创造性思维","ms":"Pemikiran inventif","ta":"புத்தாக்கச் சிந்தனை","desc":"curious and reflective, driven by purpose, cognitively flexible in problem-solving"},
 "PA_CL": {"lens":"pri","en":"Civic Literacy","zh":"公民素养","ms":"Literasi sivik","ta":"குடிமை அறிவு","desc":"willing to act on social and global issues from the Singapore context; discerning about online information"},
 "PA_CM": {"lens":"pri","en":"Communication","zh":"沟通","ms":"Komunikasi","ta":"தொடர்பு","desc":"courageous and spontaneous in voicing ideas, able to persuade; open-minded and empathetic across cultures"},
})
DERIVE = {"CAIT":["PA_AT","PA_IT"], "CCIS":["PA_CM"], "CGC":["PA_CL"], "SEC":["PA_AT"]}  # CPDD 21CC domain -> BVSS priority area
PURP_VIEW = {"Give a view","Argue","Persuade","Propose","Recommend"}
PURP_INTER = {"Reply","Respond","Give a view","Thank","Share","Apply","Report"}
RULES = [  # (id, test(rec)->bool, cats, priority areas, explanation)
 ("R1 view",  lambda r: r["purpose"] in PURP_VIEW or "arg" in (r["strand"], r["also"]), ["CAIT"], ["PA_CM"], "states and supports a view (critical thinking; courageous in voicing ideas)"),
 ("R2 interact", lambda r: (r["strand"]=="fw" and (r["purpose"] in PURP_INTER or re.search(r"reply|respond|post|comment|e-?mail|message|forum", r["task_en"], re.I))) or (r["strand"]=="oral" and re.search(r"respond|views?|discuss|interact|listener|conversation|audience", r["task_en"]+" "+r["sub_en"], re.I)), ["CCIS"], ["PA_CM"], "responds to a reader or listener (communication; open-minded, empathetic)"),
 ("R3 civic", lambda r: re.search(r"singapore|lion city|nation|citizen|red dot|communit|society|heritage|cultur|tradition|environment|earth|global|world|harmony|dialect|green|volunteer", r["theme_en"]+" "+r["task_en"], re.I), ["CGC"], ["PA_CL"], "unit theme or task is about community, Singapore, culture or the world (civic literacy)"),
 ("R4 discern", lambda r: re.search(r"fact|opinion|author'?s view|critical|evaluat|reliab|fake|media|news|advert|source|evidence|mystery|true\?|discern|inference", r["sub_en"]+" "+r["task_en"], re.I), ["CAIT"], ["PA_CL"], "weighs facts, opinions, sources or media (discerning information)"),
 ("R5 invent", lambda r: r["strand"] in ("lit","nar") or re.search(r"creat|design|imagin|story|poem|comic|scene|meme|slogan|advert|banner|poster|brochure|dream board|product|script|podcast", r["task_en"], re.I), ["CAIT"], ["PA_IT"], "creates or designs something new (inventive thinking)"),
 ("R6 adapt", lambda r: re.search(r"challeng|resilien|change|adapt|problem|solution|failure|new beginning|grow(ing)? up|dream|future|career|habit|cope|setback|discover", r["theme_en"]+" "+r["task_en"]+" "+r["sub_en"], re.I), [], ["PA_AT"], "theme or task is about coping with change, challenge or the future (adaptive thinking)"),
 ("R7 inquiry", lambda r: re.search(r"search|find (out|information)|research|survey|interview|investigat|collect|plan a|design a|project|exhibit|present(ation)? (from|on)|integrated task|综合任务|explore", r["task_en"]+" "+r["sub_en"], re.I), ["INQ"], [], "task needs students to find out, plan, make or present (inquiry-shaped, not tagged by CPDD)"),
]
for r in D["recs"]:
    tags = []
    seen = set()
    def add(k, src, rule):
        if k in seen: return
        seen.add(k); tags.append({"k": k, "src": src, "rule": rule})
    for k in r.get("cats", []): add(k, "cpdd", "tagged in the CPDD guide")
    for k in r.get("cats", []):
        for p in DERIVE.get(k, []): add(p, "derived", f"derived from the CPDD {k} tag")
    for rid, test, cats, pris, why in RULES:
        try: ok = bool(test(r))
        except Exception: ok = False
        if not ok: continue
        for k in cats + pris: add(k, "infer", f"{rid}: {why}")
    r["tags"] = tags
D["prov"] = {"cpdd":"CPDD-tagged","derived":"Derived from a CPDD tag","infer":"Inferred by rule"}
D["rules"] = [{"id": rid, "cats": cats + pris, "why": why} for rid, _, cats, pris, why in RULES] + [{"id":"DERIVE","cats":sum(DERIVE.values(),[]),"why":"CPDD 21CC domain tags mapped to BVSS E21CC priority areas: CAIT → Adaptive + Inventive Thinking; CCIS → Communication; CGC → Civic Literacy; SEC → Adaptive Thinking"}]
D["priNote"] = "BVSS E21CC priority areas (school approach from 2027): Adaptive Thinking, Inventive Thinking, Civic Literacy, Communication. No CPDD guide tags these, so every priority-area tag is either derived from a CPDD 21CC tag or inferred from the task by rule. Treat inferred tags as proposals to confirm in SOW planning."

# ---------- 3. Pedagogical design facts ----------
D["design"] = json.loads((ROOT / "tools" / "design.json").read_text(encoding="utf-8"))

new = json.dumps(D, ensure_ascii=False)
HTML.write_text(h[:i] + new + h[i+end:], encoding="utf-8")
from collections import Counter
c = Counter((t["k"], t["src"]) for r in D["recs"] for t in r["tags"])
print("tags:", sorted(c.items())); print("bytes:", len(new))
