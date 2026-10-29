import json, sys, re
src, out = sys.argv[1], sys.argv[2]
cells, cur, kind = [], [], None
def flush():
    if kind is None: return
    body = "\n".join(cur).strip("\n")
    if not body.strip(): return
    lines = [l + "\n" for l in body.split("\n")]
    if lines: lines[-1] = lines[-1].rstrip("\n")
    if kind == "MD":
        cells.append({"cell_type":"markdown","metadata":{},"source":lines})
    else:
        cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":lines})
for line in open(src, encoding="utf-8").read().split("\n"):
    m = re.match(r"^#@@ (MD|CODE)\s*$", line)
    if m:
        flush(); cur, kind = [], m.group(1)
    else:
        cur.append(line)
flush()
nb = {"cells":cells,"metadata":{"colab":{"provenance":[],"toc_visible":True},
      "kernelspec":{"display_name":"Python 3","name":"python3"},
      "language_info":{"name":"python"},"accelerator":"GPU"},
      "nbformat":4,"nbformat_minor":0}
json.dump(nb, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {out}: {len(cells)} cells ({sum(1 for c in cells if c['cell_type']=='code')} code, {sum(1 for c in cells if c['cell_type']=='markdown')} md)")
