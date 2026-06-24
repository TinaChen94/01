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
        subprocess.run(
            ["git", "fetch", "--quiet", "origin", "+refs/heads/*:refs/remotes/origin/*"],
            cwd=REPO,
        )
    branches = list_branches()
    if not branches:
        sys.exit("找不到 origin/claude/* 或 origin/main 分支;先 git fetch。")
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
