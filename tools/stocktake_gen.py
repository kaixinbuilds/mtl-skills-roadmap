#!/usr/bin/env python3
"""Scan SOW-like documents on the dept drive and emit tools/stocktake.json (inventory + samples)."""
import sys, json, zipfile, re, html, os, datetime
BASE=sys.argv[1]; OUT=sys.argv[2]
def tables(p):
    z=zipfile.ZipFile(p); x=z.read('word/document.xml').decode('utf8','ignore')
    def ptext(frag):
        frag=re.sub(r'<w:tab/>','\t',frag); frag=re.sub(r'<w:br[^>]*/>','\n',frag)
        return html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',frag)))
    out=[]
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>',x,flags=re.S):
        rows=[]
        for tr in re.findall(r'<w:tr[ >].*?</w:tr>',m.group(0),flags=re.S):
            cells=[]
            for tc in re.findall(r'<w:tc>.*?</w:tc>',tr,flags=re.S):
                cells.append('\n'.join(t for t in (ptext(pp) for pp in re.findall(r'<w:p[ >].*?</w:p>',tc,flags=re.S)) if t.strip()))
            rows.append(cells)
        out.append(rows)
    paras=[ptext(p) for p in re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S)]
    return out,[p for p in paras if p.strip()]
DOCS=[
 # path, lang, level, course, year, family
 ("02 Curriculum and Instruction Materials/CL/G2/S1/SOW - 2026 1G2 CL.docx","CL","S1","G2",2026,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G3/S1/SOW/2026 SOW - 1G3 CL.docx","CL","S1","G3",2026,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G3/S1/单元一/SOW for sec 1 term 1.docx","CL","S1","G3",2025,"unitpack"),
 ("02 Curriculum and Instruction Materials/CL/G3/S1/Sec 1 2025 - Copy/2025年 中一G3华文_教学总览.docx","CL","S1","G3",2025,"termgrid"),
 ("02 Curriculum and Instruction Materials/CL/G2/S2/SOW/2026 SOW - 2G2 CL.docx","CL","S2","G2",2026,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G3/S2/S2G3 SOW 2026.docx","CL","S2","G3",2026,"termgrid"),
 ("02 Curriculum and Instruction Materials/CL/G2/S3/SOW - 2025 S3G2 CL (Term 2-4).docx","CL","S3","G2",2025,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G2/S3/SOW - 2025 S3G2 CL (Term 2).docx","CL","S3","G2",2025,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G3/S3/SOW - 2026 S3G3 CL (working document).docx","CL","S3","G3",2026,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G2/S4/SOW - 2026 S4NA CL （working document).docx","CL","S4","G2",2026,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G3/S4/SOW - 2026 S4EXP CL 1.docx","CL","S4","G3",2026,"weekly"),
 ("02 Curriculum and Instruction Materials/CL/G3 HCL/S4/SOW - 2026 S4 HCL (working document).docx","CL","S4","H",2026,"weekly"),
 ("CPDD resources (2021 Syllabus)/ML/Teachers Guidebook/G3/M1_SOW Sampel Ekspres 1A_261220.docx","ML","S1","G3",2020,"cpdd_ml"),
 ("CPDD resources (2021 Syllabus)/ML/Teachers Guidebook/G1/M1_SOW Sampel NT 1B_250621.docx","ML","S1","G1",2021,"cpdd_ml"),
 ("CPDD resources (2021 Syllabus)/ML/Teachers Guidebook/G2/M1_SOW Sampel NA 1A_261220.docx","ML","S1","G2",2020,"cpdd_ml"),
 ("CPDD resources (2021 Syllabus)/ML/Teachers Guidebook/HML/M1_SOW Sampel HML 1A_261220.docx","ML","S1","H",2020,"cpdd_ml"),
 ("CPDD resources (2021 Syllabus)/TL Teachers Guide/1G1 TG/அடிப்படைத் தமிழ் 1A - தொகுதி 1 - 4 - கண்ணோட்டம் (Word).docx","TL","S1","G1",2021,"cpdd_tl"),
 ("CPDD resources (2021 Syllabus)/TL Teachers Guide/3G3 TG/உயர்நிலை 3 - தமிழ் (விரைவுநிலை) - தொகுதி 1 - 7 - கண்ணோட்டம் (Word).docx","TL","S3","G3",2021,"cpdd_tl"),
]
inv=[]
for rel,lang,lvl,crs,yr,fam in DOCS:
    p=os.path.join(BASE,rel)
    if not os.path.exists(p): print("MISSING",rel); continue
    tb,paras=tables(p)
    st=os.stat(p); mod=datetime.date.fromtimestamp(st.st_mtime).isoformat()
    rec={"file":os.path.basename(rel),"folder":os.path.dirname(rel),"lang":lang,"level":lvl,"course":crs,"year":yr,"family":fam,"modified":mod,"kb":round(st.st_size/1024),"tables":len(tb),"paras":len(paras)}
    # weekly: count W rows and filled rows
    if fam=="weekly":
        wk=0;filled=0;terms=0;hdr=None;samples=[]
        for t in tb:
            for r in t:
                if r and re.match(r'^W\d\d',r[0].strip()):
                    wk+=1
                    if len(r)>1 and (r[1].strip() or (len(r)>2 and r[2].strip())): 
                        filled+=1
                        if len(samples)<3: samples.append([c[:220] for c in r])
                elif r and r[0].strip().startswith('周次'): hdr=r; terms+=1
        rec.update({"weeks":wk,"weeks_filled":filled,"terms":terms,"columns":hdr,"samples":samples})
        rec["titles"]=[r[0][:60] for t in tb for r in t if len(r)==1 and r[0].strip()][:6]
        rec["titles"]+= [x[:60] for x in paras if re.search(r'学段教学进度表',x)][:6]
    elif fam=="termgrid":
        t=max(tb,key=lambda t:len(t)); rec["columns"]=[c[:40] for c in t[0]]; rec["rows"]=[r[0][:40] for r in t[1:]]
        rec["samples"]=[[c[:300] for c in r] for r in t[1:4]]
    elif fam=="unitpack":
        rec["columns"]=[x for x in paras if x.strip() in ('周次/日期','读-听-说-写','知识','会考话题','通用能力','练习（1A 作业本，活动纸，写作）','评鉴（WA，考试）')]
        rec["intro"]=paras[:6]; rec["samples"]=[]
    elif fam=="cpdd_ml":
        t=tb[0]; rec["columns"]=[c.replace('\n',' ')[:40] for c in t[0]]; rows=[r for r in t[1:] if r and not r[0].startswith('Minggu')]
        rec["rows_n"]=sum(len([r for r in tt[1:] if r and not r[0].startswith('Minggu')]) for tt in tb); rec["samples"]=[[c[:260] for c in r] for r in rows[:2]]
        rec["units"]=sorted(set(re.sub(r'\s+',' ',x).strip()[:40] for x in paras if re.match(r'^\s*Unit \d',x)))
    elif fam=="cpdd_tl":
        t=tb[0]; hdr=[r for r in t if any('நடவடிக்கை' in c for c in r)][0]; rec["columns"]=[c.replace('\n',' ')[:40] for c in hdr if c.strip()]
        rows=[r for r in t if r and re.match(r'^\d\.\d',r[0].strip())]; rec["rows_n"]=len(rows); rec["samples"]=[[c[:220] for c in r if c.strip()] for r in rows[:2]]
        rec["units"]=len([x for x in paras if x.strip().startswith('தொகுதி') and 'கண்ணோட்டம்' not in x])
    inv.append(rec)
json.dump(inv,open(OUT,'w'),ensure_ascii=False,indent=1)
for r in inv: print(r["lang"],r["level"],r["course"],r["family"],r["file"][:40],"| weeks",r.get("weeks"),"filled",r.get("weeks_filled"),"| cols",r.get("columns"),"| titles",r.get("titles"))
