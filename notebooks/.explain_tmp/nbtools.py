"""Safe utilities for expanding markdown cells in .ipynb notebooks.
Loads BOM-tolerant, only touches markdown cell 'source' arrays,
preserves ids/code/outputs/metadata. Writes clean utf-8 nbformat JSON.
"""
import json
import uuid


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def save(nb, path):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")


def to_source_lines(text):
    """Convert a markdown string to nbformat source array (trailing \n on all but last line)."""
    lines = text.split("\n")
    if not lines:
        return [""]
    out = [ln + "\n" for ln in lines[:-1]]
    if lines[-1]:
        out.append(lines[-1])
    return out


def dump(path, max_out=250):
    """Human-readable dump: every cell with index, type, source, and truncated outputs."""
    nb = load(path)
    out = []
    for i, c in enumerate(nb["cells"]):
        out.append(f"--- cell [{i}] {c['cell_type']} (id={c.get('id', '?')})")
        src = "".join(c.get("source", []))
        out.append("SOURCE:\n" + src)
        if c["cell_type"] == "code" and c.get("outputs"):
            for o in c["outputs"]:
                t = ""
                if o.get("output_type") == "stream":
                    t = "".join(o.get("text", []))
                elif "data" in o:
                    d = o["data"]
                    t = d.get("text/plain", d.get("text/html", ""))
                    if isinstance(t, list):
                        t = "".join(t)
                t = str(t)
                out.append("OUTPUT: " + t[:max_out].replace("\n", "\\n"))
    return "\n".join(out)


def apply(path, replace=None, append=None):
    """replace: {cell_index: markdown_text} — cell must be markdown.
    append: [markdown_text, ...] — appended as new md cells at the end.
    Never touches code cells. Returns dict of what changed."""
    nb = load(path)
    cells = nb["cells"]
    changed = {"replaced": {}, "appended": []}
    for idx, text in (replace or {}).items():
        idx = int(idx)
        assert 0 <= idx < len(cells), f"cell {idx} out of range (nb has {len(cells)})"
        assert cells[idx]["cell_type"] == "markdown", f"cell {idx} is {cells[idx]['cell_type']}, not markdown"
        old = "".join(cells[idx].get("source", []))
        cells[idx]["source"] = to_source_lines(text)
        changed["replaced"][idx] = {"old_len": len(old), "new_len": len(text)}
    for text in (append or []):
        cells.append({
            "cell_type": "markdown",
            "id": uuid.uuid4().hex[:8],
            "metadata": {},
            "source": to_source_lines(text),
        })
        changed["appended"].append(len(text))
    save(nb, path)
    return changed


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1]
    if cmd == "dump":
        print(dump(sys.argv[2]))
    elif cmd == "apply":
        # apply <nb> <pyfile>  — pyfile defines REPLACE and APPEND dicts
        nb = sys.argv[2]
        ns = {}
        exec(open(sys.argv[3], encoding="utf-8").read(), ns)
        res = apply(nb, ns.get("REPLACE"), ns.get("APPEND"))
        print(json.dumps(res))
