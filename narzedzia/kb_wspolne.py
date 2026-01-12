"""Wspólne funkcje skryptów bazy wiedzy: odnalezienie bazy, odczyt nagłówków YAML i schematu.

Ta sama kopia leży w każdym skillu (scripts/) i w narzedzia/ bazy wzorcowej.
Baza wiedzy to folder z szablony/SCHEMAT.md albo z plikami AGENTS.md i INDEX.md.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Brak biblioteki PyYAML. Zainstaluj: pip install pyyaml")

TU = Path(__file__).resolve().parent
POMIJAJ_FOLDERY = {"szablony", "testy", "narzedzia", ".agents", ".claude", ".codex", ".githooks", "zalaczniki", ".git"}
POMIJAJ_PLIKI = {"INDEX.md", "AGENTS.md", "CLAUDE.md", "README.md"}


def jest_baza(p: Path) -> bool:
    return (p / "szablony" / "SCHEMAT.md").exists() or ((p / "AGENTS.md").exists() and (p / "INDEX.md").exists())


def parser(opis: str) -> argparse.ArgumentParser:
    """Parser z opcją --baza i (dla zgodności) ścieżką bazy jako pierwszym argumentem."""
    p = argparse.ArgumentParser(description=opis)
    p.add_argument("sciezka", nargs="?", help="folder bazy wiedzy (to samo co --baza)")
    p.add_argument("--baza", help="folder bazy wiedzy; domyślnie bieżący folder albo najbliższy folder nadrzędny z bazą")
    return p


def znajdz_baze(wskazana: str | None = None) -> Path:
    """Wskazany folder, a bez wskazania: bieżący folder i foldery nadrzędne, na końcu folder nad narzedzia/."""
    if wskazana:
        p = Path(wskazana).expanduser().resolve()
        if not p.is_dir():
            sys.exit(f"Nie ma folderu {p}")
        return p
    start = Path.cwd().resolve()
    for p in [start, *start.parents]:
        if jest_baza(p):
            return p
    if jest_baza(TU.parent):
        return TU.parent
    sys.exit("Nie znalazłem bazy wiedzy (folder z szablony/SCHEMAT.md albo z AGENTS.md i INDEX.md). Podaj ją: --baza ŚCIEŻKA")


def czytaj(path: Path) -> tuple[dict | None, str]:
    """Nagłówek YAML i treść pliku. Brak nagłówka: (None, treść)."""
    t = path.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return None, t
    end = t.find("\n---", 3)
    if end == -1:
        return None, t
    try:
        meta = yaml.safe_load(t[3:end]) or {}
    except yaml.YAMLError as e:
        return {"_blad_yaml": str(e).splitlines()[0]}, t
    for k, v in list(meta.items()):
        if isinstance(v, date):
            meta[k] = v.isoformat()
    return meta, t[end + 4:].lstrip("\n")


def schemat(root: Path) -> dict:
    """Zamknięte listy i pola wymagane z bloku ```yaml w SCHEMAT.md.
    Kolejność: szablony/SCHEMAT.md bazy, schemat obok skryptu (references/ skilla albo szablony/ bazy wzorcowej)."""
    for p in (root / "szablony" / "SCHEMAT.md", TU.parent / "references" / "SCHEMAT.md", TU.parent / "szablony" / "SCHEMAT.md"):
        if p.exists():
            m = re.search(r"```yaml\n(.*?)```", p.read_text(encoding="utf-8"), re.S)
            if m:
                return yaml.safe_load(m.group(1))
    sys.exit("Brak SCHEMAT.md z blokiem ```yaml (szablony/SCHEMAT.md w bazie albo references/SCHEMAT.md w skillu).")


def pliki_wiedzy(root: Path):
    """Pliki .md z wiedzą: bez indeksów, instrukcji, szablonów, narzędzi i załączników."""
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if p.name in POMIJAJ_PLIKI or set(rel.parts[:-1]) & POMIJAJ_FOLDERY:
            continue
        yield p
