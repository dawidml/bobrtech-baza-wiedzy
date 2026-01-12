"""Kopiuje skille z .agents/skills (Codex, Cursor, Copilot, Gemini CLI) do .claude/skills (Claude Code).
Na Linuksie i macOS można zamiast tego użyć dowiązań symbolicznych; na Windowsie kopia jest prostsza."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src, dst = root / ".agents" / "skills", root / ".claude" / "skills"
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)
print("Skopiowano", len(list(dst.iterdir())), "skilli do .claude/skills")
