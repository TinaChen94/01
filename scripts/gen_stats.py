#!/usr/bin/env python3
"""產出統計總表生成器 — regenerate the auto block in docs/STATS.md.

Scans every `origin/claude/*` branch (+ `main`) for asset-case records,
workflow files and produced images, then computes per file:
  - 產生時間 (first commit touching the path on that branch)
  - 異動次數 (number of commits touching it; 含建立)
  - 最後修改時間 (latest commit)
plus a per-branch tally and a produced-image count.

It rewrites only the text between the AUTO:START / AUTO:END markers in
docs/STATS.md, so the hand-curated context (status / 分類 / notes) is kept.

Usage:
    python3 scripts/gen_stats.py            # update docs/STATS.md in place
    python3 scripts/gen_stats.py --stdout   # print the block, don't write
    python3 scripts/gen_stats.py --no-fetch # skip `git fetch` (offline)

Pure git + Python stdlib; no third-party deps.
"""
import fnmatch
import os
import re
import subprocess
import sys
from collections import defaultdict

START = "<!-- AUTO:START -->"
END = "<!-- AUTO:END -->"

# 要追蹤的檔案 glob(對 git ls-tree 的完整路徑做 fnmatch)。
# 新增的案例 / 工作流檔只要落在這些 pattern 下,就會自動被統計到。
TRACK = [
    "docs/asset-cases/*.md",
    ".claude/skills/ai-media-generator/examples/*.md",
    "asset-cutout-jobs/*/RECORD.md",
    ".claude/skills/ai-media-generator/templates/concept-to-3d-pipeline.md",
    ".claude/skills/ai-media-generator/references/concept-to-3d.md",
    ".claude/skills/asset-cutout/SKILL.md",
]
EXCLUDE = {"docs/asset-cases/README.md", "docs/asset-cases/images/README.md"}
IMG_RE = re.compile(r"\.(png|jpe?g|webp|tga|exr)$", re.IGNORECASE)
SESSION_RE = re.compile(r"session_([A-Za-z0-9]+)")


def git(*args):
    """Run a git command at the repo root and return stdout (text)."""
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True
    ).stdout


def list_branches():
    out = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin")
    bs = [b for b in out.split() if b == "origin/main" or b.startswith("origin/claude/")]
    # main first, then the rest alphabetically
    bs.sort(key=lambda b: (b != "origin/main", b))
    return bs


def is_tracked(path):
    if path in EXCLUDE:
        return False
    return any(fnmatch.fnmatch(path, pat) for pat in TRACK)


def commits_for(branch, path):
    """Newest-first list of commit hashes touching `path` on `branch`."""
    return git("log", "--format=%H", branch, "--", path).split()


def short_dt(commit):
    raw = git("show", "-s", "--format=%ci", commit).strip()  # 2026-06-23 08:33:40 +0000
    return raw[:16] if raw else "?"


def session_of(commit):
    body = git("show", "-s", "--format=%B", commit)
    m = SESSION_RE.search(body)
    return m.group(1)[:9] if m else "—"


def collect_files(branches):
    """basename -> best record (the branch with the richest history)."""
    best = {}
    for branch in branches:
        tree = git("ls-tree", "-r", branch)
        for line in tree.splitlines():
            # "<mode> <type> <sha>\t<path>"
            try:
                meta, path = line.split("\t", 1)
            except ValueError:
                continue
            if not is_tracked(path):
                continue
            hashes = commits_for(branch, path)
            if not hashes:
                continue
            rec = {
                "name": os.path.basename(path),
                "path": path,
                "branch": branch.replace("origin/", ""),
                "created": short_dt(hashes[-1]),
                "last": short_dt(hashes[0]),
                "count": len(hashes),
                "session_new": session_of(hashes[0]),
            }
            key = rec["path"]  # 用完整路徑當鍵:同路徑跨分支會收斂成一列,
            if key not in best or rec["count"] > best[key]["count"]:  # 不同檔(即使同名)各自一列
                best[key] = rec
    return sorted(best.values(), key=lambda r: (r["created"], r["name"]))


def collect_images(branches):
    """Return (per_branch_counts, distinct_blob_count, per_prefix_distinct)."""
    per_branch = {}
    blobs = set()
    prefix_blobs = defaultdict(set)
    prefixes = {
        "mausoleum-": "A1 哥德陵墓",
        "buddhist-relief-wall-": "A2 佛教浮雕牆",
        "mossy-ground-": "A10 苔蘚草地",
        "cobblestone-path-": "A11 石板路",
    }
    for branch in branches:
        n = 0
        for line in git("ls-tree", "-r", branch).splitlines():
            try:
                meta, path = line.split("\t", 1)
            except ValueError:
                continue
            if "/images/" not in path and "/assets/" not in path:
                continue
            if not IMG_RE.search(path):
                continue
            sha = meta.split()[2]
            n += 1
            blobs.add(sha)
            base = os.path.basename(path)
            for pre, label in prefixes.items():
                if base.startswith(pre):
                    prefix_blobs[label].add(sha)
        if n:
            per_branch[branch.replace("origin/", "")] = n
    return per_branch, len(blobs), {k: len(v) for k, v in prefix_blobs.items()}


def branch_commit_counts(branches):
    """Commits unique to each branch vs main (rough 'contribution')."""
    rows = []
    for branch in branches:
        if branch == "origin/main":
            total = int(git("rev-list", "--count", branch).strip() or 0)
            rows.append((branch.replace("origin/", ""), total, "全部 merge 線"))
            continue
        uniq = git("rev-list", "--count", branch, "^origin/main").strip() or "0"
        rng = git("log", "--format=%ci", branch, "^origin/main")
        dates = [l[:10] for l in rng.splitlines()]
        span = f"{dates[-1]} → {dates[0]}" if dates else "—"
        rows.append((branch.replace("origin/", ""), int(uniq), span))
    return rows


CASE_PAT = ["docs/asset-cases/A*.md", "*/examples/B*.md", "asset-cutout-jobs/*/RECORD.md"]
REF_RE = re.compile(r"[\w./\-]+\.(?:png|jpe?g|webp|tga|exr)", re.IGNORECASE)
EMBED_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")  # 只認真正的 ![alt](path) 內嵌


def is_case(path):
    return any(fnmatch.fnmatch(path, p) for p in CASE_PAT)


def md_embeds(branch, path):
    """Resolved image paths actually embedded via ![...](...) in the file."""
    content = git("show", f"{branch}:{path}")
    base = os.path.dirname(path)
    return [os.path.normpath(os.path.join(base, m)) for m in EMBED_RE.findall(content)
            if IMG_RE.search(m)]


def ls_tree(branch):
    """[(sha, path)] for every blob on the branch."""
    out = []
    for line in git("ls-tree", "-r", branch).splitlines():
        try:
            meta, path = line.split("\t", 1)
        except ValueError:
            continue
        parts = meta.split()
        if len(parts) >= 3:
            out.append((parts[2], path))
    return out


def md_refs(branch, path):
    """Image basenames referenced inside a markdown file."""
    content = git("show", f"{branch}:{path}")
    return {os.path.basename(m) for m in REF_RE.findall(content)}


def in_asset_dir(path):
    return "/images/" in path or "/assets/" in path


def lint(branches):
    """Detection only — flag likely 遺漏/重複/垃圾. Returns issue dict."""
    trees = {b: ls_tree(b) for b in branches}
    paths_on = {b: {p for _, p in trees[b]} for b in branches}

    referenced = set()                 # 任何 md 引用過的圖檔 basename
    blob_paths = defaultdict(set)      # sha -> {distinct paths}(跨分支)
    seen_case = {}                     # 去重後的案例 md:path -> branch
    for b in branches:
        for sha, p in trees[b]:
            if IMG_RE.search(p):
                blob_paths[sha].add(p)
        for p in paths_on[b]:
            if is_tracked(p) and p.endswith(".md"):
                referenced.update(md_refs(b, p))
            if is_case(p):
                seen_case.setdefault(p, b)

    issues = {}

    # A. 0 圖案例 + E. 斷掉的內嵌(只看真正的 ![](…))
    zero, broken = [], []
    for p, b in sorted(seen_case.items()):
        embeds = md_embeds(b, p)
        existing = [e for e in embeds if e in paths_on[b]]
        missing = sorted(set(embeds) - set(existing))
        if not existing:
            zero.append(f"{p}  @{b.replace('origin/','')}")
        elif missing:
            broken.append(f"{p} @{b.replace('origin/','')} → 缺 {', '.join(os.path.basename(m) for m in missing)}")
    issues["0 圖案例(未完成 / 無成品圖)"] = zero
    issues["斷掉的圖片內嵌(![](…) 指向不存在的圖)"] = broken

    # B. 孤兒圖(圖檔 basename 沒有任何 md 引用)
    orphan = sorted({
        p for b in branches for _, p in trees[b]
        if IMG_RE.search(p) and os.path.basename(p) not in referenced
    })
    issues["孤兒圖(沒被任何案例 .md 引用)"] = orphan

    # C. 非標準位置的圖(不在 */images/ 或 */assets/)— 例如散在 repo 根目錄
    stray = sorted({
        f"{p}  @{b.replace('origin/','')}"
        for b in branches for _, p in trees[b]
        if IMG_RE.search(p) and not in_asset_dir(p)
    })
    issues["散落圖(不在 images/ 或 assets/,如 repo 根目錄)"] = stray

    # D. 同內容、多路徑(真重複 → dedupe 候選)
    dup = [f"{sha[:9]} → " + " | ".join(sorted(ps))
           for sha, ps in sorted(blob_paths.items()) if len(ps) > 1]
    issues["同內容存在於多個路徑(重複檔)"] = dup

    return issues


def build_block(branches):
    files = collect_files(branches)
    per_branch_img, distinct_img, prefix_img = collect_images(branches)
    bcounts = branch_commit_counts(branches)

    lines = [START]
    lines.append(f"> ⏱️ 自動產生於 `scripts/gen_stats.py`,掃描 {len(branches)} 個分支。"
                 f"異動次數 = 觸及該檔的 commit 數(含建立);時間為 UTC。")
    lines.append("")

    # 檔案層級統計
    lines.append("### 檔案統計(產生 / 異動 / 最後修改)")
    lines.append("")
    lines.append("| 檔案 | 所在分支 | 產生時間 | 異動次數 | 最後修改 | 最近 session |")
    lines.append("|---|---|---|---:|---|---|")
    for r in files:
        lines.append(
            f"| `{r['name']}` | {r['branch']} | {r['created']} | {r['count']} | {r['last']} | `{r['session_new']}` |"
        )
    lines.append("")

    # 成品圖
    lines.append("### 成品圖")
    lines.append("")
    lines.append(f"- **不重複圖檔(blob)**:{distinct_img} 張")
    if prefix_img:
        per_case = " · ".join(f"{label} {n}" for label, n in sorted(prefix_img.items()))
        lines.append(f"- **依案例**:{per_case}")
    if per_branch_img:
        per_b = " · ".join(f"{b} {n}" for b, n in sorted(per_branch_img.items()))
        lines.append(f"- **各分支圖檔數(含複本)**:{per_b}")
    lines.append("")

    # 分支貢獻
    lines.append("### 各分支貢獻(相對 main 的獨有 commit)")
    lines.append("")
    lines.append("| 分支 | 獨有 commit | 期間 |")
    lines.append("|---|---:|---|")
    for name, n, span in bcounts:
        lines.append(f"| {name} | {n} | {span} |")
    lines.append("")
    lines.append(END)
    return "\n".join(lines)


def main():
    if "--no-fetch" not in sys.argv:
        # --prune:遠端已刪除的分支,連帶清掉本地 refs/remotes/origin/* 殭屍參照,
        # 否則已刪分支會被繼續算進統計。
        subprocess.run(
            ["git", "fetch", "--quiet", "--prune", "origin", "+refs/heads/*:refs/remotes/origin/*"],
            cwd=REPO,
        )
    branches = list_branches()
    if not branches:
        sys.exit("找不到 origin/claude/* 或 origin/main 分支;先 git fetch。")

    if "--lint" in sys.argv:
        report = lint(branches)
        total = sum(len(v) for v in report.values())
        print(f"# 🔎 倉庫健檢(偵測,未改任何檔)— 掃 {len(branches)} 分支,共 {total} 項待看\n")
        for title, items in report.items():
            print(f"## {'✅' if not items else '⚠️'} {title} — {len(items)}")
            for it in items:
                print(f"  - {it}")
            print()
        return

    block = build_block(branches)

    if "--stdout" in sys.argv:
        print(block)
        return

    if not os.path.exists(STATS):
        sys.exit(f"{STATS} 不存在;請先建立含 {START}/{END} 標記的頁面。")
    text = open(STATS, encoding="utf-8").read()
    if START in text and END in text:
        new = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            block,
            text,
            flags=re.DOTALL,
        )
    else:
        new = text.rstrip() + "\n\n" + block + "\n"
    open(STATS, "w", encoding="utf-8").write(new)
    print(f"已更新 {STATS}")


if __name__ == "__main__":
    REPO = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    ).stdout.strip()
    STATS = os.path.join(REPO, "docs", "STATS.md")
    main()
