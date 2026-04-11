"""
Fix script for _iteration_9.ipynb — RQ3 Hazard Classification.
1 bug: DataFrame.get() returns string default when column missing,
       causing AttributeError on chained .fillna().
"""
import json, ast

NB = "_iteration_9.ipynb"

with open(NB, "r", encoding="utf-8") as f:
    nb = json.load(f)

changes = 0

def safe_replace(source: str, old: str, new: str, label: str) -> str:
    global changes
    count = source.count(old)
    assert count == 1, f"[{label}] expected 1 occurrence, found {count}"
    changes += 1
    return source.replace(old, new)

# ---------------------------------------------------------------------------
# Cell 23: Fix template_df.get("review_notes", "").fillna("").astype(str)
# When the column is missing, .get() returns "" (a string) and .fillna() fails.
# ---------------------------------------------------------------------------
src23 = "".join(nb["cells"][23]["source"])
assert nb["cells"][23]["cell_type"] == "code"
assert "template_df.get" in src23, "Cell 23 does not contain template_df.get"

OLD = '    template_df["review_notes"] = template_df.get("review_notes", "").fillna("").astype(str)'
NEW = (
    '    if "review_notes" not in template_df.columns:\n'
    '        template_df["review_notes"] = ""\n'
    '    template_df["review_notes"] = template_df["review_notes"].fillna("").astype(str)'
)

src23 = safe_replace(src23, OLD, NEW, "Cell 23: DataFrame.get fix")
nb["cells"][23]["source"] = src23.splitlines(True)
if not nb["cells"][23]["source"][-1].endswith("\n"):
    nb["cells"][23]["source"][-1] += ""  # keep as-is; just ensure list form

# ---------------------------------------------------------------------------
# Verify syntax of all code cells
# ---------------------------------------------------------------------------
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        code = "".join(cell["source"])
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise SyntaxError(f"Cell {i} has syntax error after fix: {e}")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
with open(NB, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")

print(f"Applied {changes} fix(es). All cells pass ast.parse().")
