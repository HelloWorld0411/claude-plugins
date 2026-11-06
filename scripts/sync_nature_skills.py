#!/usr/bin/env python3
"""Copy selected skills from a local clone of Yuan1z0825/nature-skills into
plugins/nature-skills/skills/ and put a short Chinese label at the start of
each skill's description, so the label shows in Claude's skill menu.

Usage: python3 scripts/sync_nature_skills.py /path/to/upstream-clone

Edit LABELS to add or remove skills. Each listed skill folder is replaced by
the upstream copy on every run; skills not listed are not copied.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

LABELS = {
    "nature-shared": "共享资料包（供其他技能读取，勿单独调用）",
    "nature-figure": "科研绘图",
    "nature-polishing": "Nature风格润色与翻译",
    "nature-reader": "中英对照阅读",
    "nature-paper-trans": "论文PDF整页译成中文",
    "nature-paper-card": "论文精读卡",
    "nature-paper-xray": "深度拆解论文思路",
    "nature-paper2ppt": "论文转组会PPT",
    "nature-paper2word": "稿件排版成Word",
    "nature-image2ppt": "图片转可编辑PPT",
    "nature-paper-to-patent": "论文转专利草稿",
    "nature-statistics": "统计报告审查",
    "nature-data": "数据可用性声明",
}
SEP = "｜"

REPO = Path(__file__).resolve().parent.parent
DEST = REPO / "plugins" / "nature-skills"


def label_description(text: str, label: str) -> str:
    """Insert `label｜` at the start of the frontmatter description."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter")
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    prefix = label + SEP
    for i in range(1, end):
        m = re.match(r"^description:\s*(.*)$", lines[i])
        if not m:
            continue
        value = m.group(1)
        if value[:1] in ('"', "'"):
            q = value[0]
            if value[1:].startswith(prefix):
                return text
            lines[i] = f"description: {q}{prefix}{value[1:]}"
        elif re.match(r"^[|>][-+]?\s*$", value):
            j = i + 1
            while j < end and not lines[j].strip():
                j += 1
            content = lines[j].lstrip()
            if content.startswith(prefix):
                return text
            indent = lines[j][: len(lines[j]) - len(content)]
            lines[j] = f"{indent}{prefix}{content}"
        else:
            if value.startswith(prefix):
                return text
            lines[i] = f"description: {prefix}{value}"
        return "\n".join(lines)
    raise ValueError("no description field")


def main() -> int:
    upstream = Path(sys.argv[1]).resolve()
    (DEST / "skills").mkdir(parents=True, exist_ok=True)
    for name, label in LABELS.items():
        src = upstream / "skills" / name
        if not (src / "SKILL.md").is_file():
            print(f"::warning::{name} is missing upstream; keeping the last copy")
            continue
        dst = DEST / "skills" / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        skill = dst / "SKILL.md"
        skill.write_text(label_description(skill.read_text(encoding="utf-8"), label), encoding="utf-8")
        print(f"copied {name}")
    shutil.copy2(upstream / "LICENSE", DEST / "LICENSE")
    commit = subprocess.run(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    (DEST / "UPSTREAM_COMMIT").write_text(commit + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
