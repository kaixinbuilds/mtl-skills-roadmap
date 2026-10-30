#!/usr/bin/env python3
"""Embed tools/stocktake.json into sow-stocktake.html (between the INV markers). Idempotent.
Regenerate tools/stocktake.json from the department drive with tools/stocktake_gen.py <drive root> tools/stocktake.json."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
inv = json.loads((ROOT / "tools" / "stocktake.json").read_text(encoding="utf-8"))
p = ROOT / "sow-stocktake.html"; h = p.read_text(encoding="utf-8")
new = "/*INV*/" + json.dumps(inv, ensure_ascii=False) + "/*INV_END*/"
h2, n = re.subn(r"/\*INV\*/.*?/\*INV_END\*/", lambda m: new, h, flags=re.S)
assert n == 1, "INV markers not found"
p.write_text(h2, encoding="utf-8"); print("embedded", len(inv), "documents;", len(h2), "bytes")
