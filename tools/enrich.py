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
 "PA_AT": {"lens":"pri","en":"Adaptive Thinking","zh":"适应性思维","ms":"Pemikiran adaptif","ta":"தகவமைப்புச் சிந்தனை","desc":"MOE LG&M: the ability to apply learnt knowledge and skills strategically and with flexibility in different or new and evolving contexts (CAIT 3 assesses contexts to draw new insights; CAIT 4 manages complexity and ambiguity by adjusting perspective and strategies). BVSS slide: confident without established answers, resilient in failure, responds nimbly to changing contexts."},
 "PA_IT": {"lens":"pri","en":"Inventive Thinking","zh":"创造性思维","ms":"Pemikiran inventif","ta":"புத்தாக்கச் சிந்தனை","desc":"MOE LG&M: the ability to frame, investigate and explore issues, generate innovative ideas, and evaluate them to form novel and useful responses (CAIT 5 explores possibilities and generates novel and useful ideas; CAIT 6 evaluates and refines ideas into solutions). BVSS slide: curious and reflective, driven by purpose, cognitively flexible in problem-solving."},
 "PA_CL": {"lens":"pri","en":"Civic Literacy","zh":"公民素养","ms":"Literasi sivik","ta":"குடிமை அறிவு","desc":"MOE LG&M: the ability to understand the nation's values, governance, context and realities, form one's civic identity, and constructively engage with and contribute to one's community and nation (CGC 1 understands values, ideals and issues of personal, community and national significance; CGC 2 plays active and constructive roles). BVSS slide: willing to act on social and global issues from the Singapore context; discerning about online information."},
 "PA_CM": {"lens":"pri","en":"Communication","zh":"沟通","ms":"Komunikasi","ta":"தொடர்பு","desc":"MOE LG&M: the ability to convey information and exchange ideas clearly and coherently through multimodal ways for specific purposes, audiences and contexts (CCI 1 effectively communicates information and co-constructs meaning; CCI 2 engages empathetically with diverse perspectives). BVSS slide: courageous and spontaneous in voicing ideas, able to persuade; open-minded and empathetic across cultures."},
})
CAT_DESC = {  # one-line meaning of each 21CC / IBL tag, shown in the unit detail panel
 "CAIT": "MOE 21CC domain: weighing evidence and views, generating new ideas, and adjusting thinking to new situations.",
 "CCIS": "MOE 21CC domain: getting a message across to a reader or listener, working with others, and finding and using information.",
 "CGC": "MOE 21CC domain: understanding the community, Singapore and the world, and engaging respectfully with other cultures.",
 "SEC": "MOE 21CC domain: self-awareness, self-management, social awareness, relationship management and responsible decision-making.",
 "DIG": "A teacher note in the guide prompting digital literacy at this point.",
 "UG": "The CL teacher guide's appendix uses this unit as its worked example of building a 21CC unit goal.",
 "INQ": "Students work from a question or problem and find out, plan, make or present something. CPDD-tagged where the ML guide flags the task as inquiry-based (usable as a weighted assessment); otherwise inferred from the task wording.",
 "STAR": "ML syllabus teaching activity in four stages: Scenario Analysis, Team Inquiry, Application and Reflection. Students unpack a situation, investigate it in teams, apply what they found, then reflect.",
 "EPED": "TL guide tag: an e-pedagogy activity planned as an inquiry-based learning experience.",
}
for _k, _d in CAT_DESC.items():
    if _k in D["cat"]: D["cat"][_k]["desc"] = _d
# CPDD 21CC domain -> BVSS priority area. Tightened 31 Oct 2026 against MOE's Learning Goals and Developmental
# Milestones for Emerging 21CC (20 Oct 2023): a CPDD CAIT tag covers Critical, Adaptive AND Inventive thinking, so it
# is mapped to Adaptive Thinking only where the task shows adaptive moves (CAIT 3-4) and to Inventive Thinking only
# where it shows inventive moves (CAIT 5-6). CCIS -> Communication and CGC -> Civic Literacy stay as fixed mappings.
# SEC (social-emotional) no longer maps to Adaptive Thinking: the LG&M lists SE skills as supports, not as the competency.
INVENT = re.compile(r"\b(design|invent|innovat|improv(e|es|ing|ement)|solution|solve|propos(e|al|es|ing)|recommend|suggest(ion)?s?|plan (a|an|the|for)|planning|campaign|dream board|brainstorm|possibilit|alternative|what if|creat(e|ing) (a |an )?(new|own|original)|new (idea|way|product|version|use)|redesign|rewrite the ending|enterprise|business)\b|创新|设计|发明|改进|建议|方案|策划|构想|reka|cipta|inovasi|cadangan|merancang|rancangan|penyelesaian|புத்தாக்க|வடிவமை|திட்டமிட|தீர்வு|ஆலோசனை", re.I)
ADAPT = re.compile(r"perspective|point of view|viewpoint|换位|角度|立场|dilemma|两难|decide between|choose between|adjust|adapt|unfamiliar|new situation|role-?play|角色扮演|scenario|what would you do|如果你是|假设你是|if you were|as the .{0,30}(head|manager|leader|reporter|officer)|in (his|her|their) shoes|different (context|situation|setting|culture)|compare .*(context|situation|culture)|transfer|strateg|debate|辩论|changes? (your|his|her|my) (mind|view)|改变了.{0,6}看法|perspektif|dilema|main peranan|sekiranya anda|seandainya|bayangkan anda|andaikan|menyesuaikan|situasi baharu|perbahasan|berbahas|பார்வை|தீர்மான|மாற்று|சூழ(ல்|லில்)|பாத்திரமேற்று", re.I)
def _invent(r): return r["purpose"] in {"Propose","Recommend"} or bool(INVENT.search(r["task_en"]+" "+r["sub_en"]+" "+(r.get("task_m") or "")+" "+(r.get("sub_m") or "")))
def _adapt(r): return bool(ADAPT.search(r["task_en"]+" "+r["sub_en"]+" "+(r.get("task_m") or "")+" "+(r.get("sub_m") or "")))
DERIVE = {"CCIS":["PA_CM"], "CGC":["PA_CL"]}  # fixed mappings
DERIVE_COND = {"CAIT":[("PA_IT", _invent, "CAIT tag plus an inventive move in the task (CAIT 5-6: generate, evaluate and refine ideas or solutions)"),
                        ("PA_AT", _adapt, "CAIT tag plus an adaptive move in the task (CAIT 3-4: take another perspective, adjust strategy, apply skills in a new context)")]}
PURP_VIEW = {"Give a view","Argue","Persuade","Propose","Recommend"}
PURP_INTER = {"Reply","Respond","Give a view","Thank","Share","Apply","Report"}
RULES = [  # (id, test(rec)->bool, cats, priority areas, explanation)
 ("R1 view",  lambda r: r["purpose"] in PURP_VIEW or "arg" in (r["strand"], r["also"]), ["CAIT"], ["PA_CM"], "states and supports a view (critical thinking; courageous in voicing ideas)"),
 ("R2 interact", lambda r: (r["strand"]=="fw" and (r["purpose"] in PURP_INTER or re.search(r"reply|respond|post|comment|e-?mail|message|forum", r["task_en"], re.I))) or (r["strand"]=="oral" and re.search(r"respond|views?|discuss|interact|listener|conversation|audience", r["task_en"]+" "+r["sub_en"], re.I)), ["CCIS"], ["PA_CM"], "responds to a reader or listener (communication; open-minded, empathetic)"),
 ("R3 civic", lambda r: re.search(r"singapore|lion city|nation|citizen|red dot|communit|society|heritage|cultur|tradition|environment|earth|global|world|harmony|dialect|green|volunteer", r["theme_en"]+" "+r["task_en"], re.I), ["CGC"], ["PA_CL"], "unit theme or task is about community, Singapore, culture or the world (civic literacy: CGC 1, understanding values and issues of community and national significance)"),
 ("R4 discern", lambda r: re.search(r"fact|opinion|author'?s view|critical|evaluat|reliab|fake|media|news|advert|source|evidence|mystery|true\?|discern|inference", r["sub_en"]+" "+r["task_en"], re.I), ["CAIT"], ["PA_CL"], "weighs facts, opinions, sources or media (critical thinking; discerning information, the school's Civic Literacy descriptor)"),
 ("R5 invent", _invent, ["CAIT"], ["PA_IT"], "task asks students to generate, design, propose or refine ideas or solutions to an issue (MOE CAIT 5-6, Inventive Thinking). Writing a story, poem or poster no longer counts on its own"),
 ("R6 adapt", _adapt, [], ["PA_AT"], "task asks students to take another perspective, weigh a dilemma, adjust a strategy or apply skills in a new or unfamiliar context (MOE CAIT 3-4, Adaptive Thinking). A theme about change or challenge no longer counts on its own"),
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
        for p, test, why in DERIVE_COND.get(k, []):
            try: ok = bool(test(r))
            except Exception: ok = False
            if ok: add(p, "derived", f"derived: {why}")
    for rid, test, cats, pris, why in RULES:
        try: ok = bool(test(r))
        except Exception: ok = False
        if not ok: continue
        for k in cats + pris: add(k, "infer", f"{rid}: {why}")
    r["tags"] = tags
D["prov"] = {"cpdd":"CPDD-tagged","derived":"Derived from a CPDD tag","infer":"Inferred by rule"}
D["rules"] = [{"id": rid, "cats": cats + pris, "why": why} for rid, _, cats, pris, why in RULES] + [{"id":"DERIVE","cats":["PA_CM","PA_CL","PA_IT","PA_AT"],"why":"CPDD 21CC domain tags mapped to BVSS E21CC priority areas: CCIS → Communication; CGC → Civic Literacy; CAIT → Inventive Thinking only where the task shows an inventive move (CAIT 5-6) and Adaptive Thinking only where it shows an adaptive move (CAIT 3-4); SEC no longer maps to a priority area (tightened 31 Oct 2026 against MOE's LG&M for E21CC)"}]
D["priNote"] = "BVSS E21CC priority areas (school approach from 2027): Adaptive Thinking, Inventive Thinking, Civic Literacy, Communication. No CPDD guide tags these, so every priority-area tag is either derived from a CPDD 21CC tag or inferred from the task by rule, using the definitions and learning goals in MOE's Learning Goals and Developmental Milestones for Emerging 21CC (20 Oct 2023): Adaptive Thinking = CAIT 3-4, Inventive Thinking = CAIT 5-6, Communication = CCI 1-2, Civic Literacy = CGC 1-2. Tightened 31 Oct 2026: a narrative or creative text no longer counts as Inventive Thinking, and a theme about change no longer counts as Adaptive Thinking; the task must show the move. Treat inferred tags as proposals to confirm in SOW planning."

# ---------- 3. Pedagogical design facts ----------
D["design"] = json.loads((ROOT / "tools" / "design.json").read_text(encoding="utf-8"))

# ---------- 4. Redesigned SOW frame (tools/sow.json) ----------
D["sow"] = json.loads((ROOT / "tools" / "sow.json").read_text(encoding="utf-8"))
D["design"].setdefault("about", {})["sow"] = D["sow"]["about"]
D["ui"].pop("t_stock", None)
D["ui"]["t_write"] = {"en":"Writing task bank","zh":"完整写作题库","ms":"Bank tugasan penulisan","ta":"எழுத்துப் பணித் தொகுப்பு"}
D["design"]["about"]["write"] = D["sow"].get("wbankAbout", {"what":"","points":[],"use":""})
D["ui"]["t_sow"] = {"en":"Scheme of work 2027","zh":"2027教学进度表","ms":"Skema Pengajaran 2027","ta":"2027 பாடத்திட்டம்"}

# ---------- 5. CL inquiry wording (recheck of all 44 CL 教师手册 PDFs, 31 Oct 2026) ----------
D["iblTg"]["CL"] = "《华文伴我行》教师手册 do not tag units for inquiry. Every book's 差异教学 notes name 引导——探究 (guided inquiry) as one of two teaching modes, and every unit ends with 文化探索 (look it up and share) and a 综合任务 (integrated task: 展示、交流、反思). 探究 itself appears once or twice per book; 综合任务 about twenty times."
D["iblTgEn"]["CL"] = "The CL guides don't tag units for inquiry. Every book's differentiated-instruction notes name guided inquiry (引导——探究) as one of two teaching modes, and every unit ends with a culture-exploration extension (look it up online and share) and an integrated task (make, present, reflect). The word inquiry appears once or twice per book; the integrated task about twenty times."

new = json.dumps(D, ensure_ascii=False)
HTML.write_text(h[:i] + new + h[i+end:], encoding="utf-8")
from collections import Counter
c = Counter((t["k"], t["src"]) for r in D["recs"] for t in r["tags"])
print("tags:", sorted(c.items())); print("bytes:", len(new))
