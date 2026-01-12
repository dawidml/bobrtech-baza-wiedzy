"""Podgląd tekstowy plików Office (docx, xlsx, pptx) dla Git i GitHub. Tylko biblioteka standardowa Pythona.

Git widzi .docx/.xlsx/.pptx jako binarne archiwa ZIP, więc `git diff` i GitHub pokazują tylko „Binary file”.
Ten skrypt wyciąga z nich tekst i tabele, żeby zmiany było widać wiersz po wierszu.

  python narzedzia/podglad_tekstowy.py PLIK.xlsx      # tekst na ekran (tak używa go git diff, textconv)
  python narzedzia/podglad_tekstowy.py --wszystkie    # zalaczniki/oryginaly/* -> zalaczniki/podglad/*.md (hook pre-commit)
  python narzedzia/podglad_tekstowy.py --sprawdz      # kod wyjścia 1, gdy podgląd jest nieaktualny (GitHub Actions)

Lokalny diff dokumentów (raz na komputerze, w folderze repozytorium):
  git config diff.dokument.textconv "python narzedzia/podglad_tekstowy.py"
  git config diff.dokument.cachetextconv true
Plik .gitattributes przypisuje docx/xlsx/pptx do sterownika diff=dokument.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
OBSLUGIWANE = (".docx", ".xlsx", ".pptx")
ROOT = Path(__file__).resolve().parent.parent
ORYGINALY = ROOT / "zalaczniki" / "oryginaly"
# Akapity podobne do poleceń dla AI (prompt injection) nie trafiają do podglądu w repozytorium. W textconv (lokalny diff) są widoczne.
UKRYTE_POLECENIA = re.compile(r"instrukcj\w* dla (system|model|asystent|ai)|zignoruj (wszystkie |poprzednie )?(instrukcje|polecenia)|"
                              r"ignore (all |previous )?instructions|system prompt|nie wspominaj o tej instrukcji|"
                              r"(podaj|podanie|prześlij|wyślij)\w* .{0,30}(hasł|login)", re.I)
PODGLAD = ROOT / "zalaczniki" / "podglad"


def komorka_md(t: str) -> str:
    return " ".join(str(t).split()).replace("|", "\\|")


def tabela_md(wiersze: list[list[str]]) -> list[str]:
    if not wiersze:
        return []
    n = max(len(w) for w in wiersze)
    wiersze = [w + [""] * (n - len(w)) for w in wiersze]
    out = ["| " + " | ".join(komorka_md(c) for c in wiersze[0]) + " |", "|" + "---|" * n]
    out += ["| " + " | ".join(komorka_md(c) for c in w) + " |" for w in wiersze[1:]]
    return out


# ---------- Word ----------
def tekst_akapitu(p) -> str:
    czesci = []
    for el in p.iter():
        if el.tag == W + "t":
            czesci.append(el.text or "")
        elif el.tag == W + "tab":
            czesci.append("\t")
        elif el.tag in (W + "br", W + "cr"):
            czesci.append(" ")
    return "".join(czesci).strip()


def docx(z: zipfile.ZipFile) -> list[str]:
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    out = []
    for el in body:
        if el.tag == W + "p":
            t = tekst_akapitu(el)
            if not t:
                continue
            styl = el.find(f"{W}pPr/{W}pStyle")
            styl = styl.get(W + "val", "") if styl is not None else ""
            lista = el.find(f"{W}pPr/{W}numPr") is not None
            m = re.match(r"(?i)(heading|nagwek|nagłówek)\s*(\d)", styl)
            if styl.lower() == "title":
                out += [f"# {t}", ""]
            elif m:
                out += [f"{'#' * (int(m.group(2)) + 1)} {t}", ""]
            elif lista:
                out.append(f"- {t}")
            else:
                out += [t, ""]
        elif el.tag == W + "tbl":
            wiersze = [[tekst_akapitu(c) for c in tr.findall(W + "tc")] for tr in el.findall(W + "tr")]
            out += tabela_md(wiersze) + [""]
    return out


# ---------- Excel ----------
def kolumna(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx(z: zipfile.ZipFile) -> list[str]:
    wspolne = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(S + "si"):
            wspolne.append("".join(t.text or "" for t in si.iter(S + "t")))
    relacje = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall(PR + "Relationship")}
    out = []
    for sh in ET.fromstring(z.read("xl/workbook.xml")).find(S + "sheets"):
        cel = relacje[sh.get(R + "id")].lstrip("/")
        sciezka = cel if cel.startswith("xl/") else "xl/" + cel
        wiersze = []
        for row in ET.fromstring(z.read(sciezka)).iter(S + "row"):
            w = {}
            for c in row.findall(S + "c"):
                typ, v, f = c.get("t"), c.find(S + "v"), c.find(S + "f")
                if typ == "s" and v is not None:
                    tekst = wspolne[int(v.text)]
                elif typ == "inlineStr":
                    tekst = "".join(t.text or "" for t in c.iter(S + "t"))
                elif typ == "b" and v is not None:
                    tekst = "PRAWDA" if v.text == "1" else "FAŁSZ"
                else:
                    tekst = v.text if v is not None and v.text is not None else ""
                    if re.fullmatch(r"-?\d+\.\d+", tekst):
                        tekst = f"{float(tekst):.10g}"
                if f is not None and f.text:
                    tekst = f"={f.text} → {tekst}" if tekst else f"={f.text}"
                w[kolumna(c.get("r"))] = tekst
            if any(str(x).strip() for x in w.values()):
                wiersze.append([w.get(i, "") for i in range(max(w) + 1)])
        out += [f"## Arkusz: {sh.get('name')}", ""] + (tabela_md(wiersze) or ["(pusty)"]) + [""]
    return out


# ---------- PowerPoint ----------
def pptx(z: zipfile.ZipFile) -> list[str]:
    relacje = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("ppt/_rels/presentation.xml.rels")).findall(PR + "Relationship")}
    out = []
    lista = ET.fromstring(z.read("ppt/presentation.xml")).find(P + "sldIdLst")
    for nr, s in enumerate(lista if lista is not None else [], 1):
        cel = relacje[s.get(R + "id")].lstrip("/")
        drzewo = ET.fromstring(z.read(cel if cel.startswith("ppt/") else "ppt/" + cel))
        out += [f"## Slajd {nr}", ""]
        for akapit in drzewo.iter(A + "p"):
            t = "".join(x.text or "" for x in akapit.iter(A + "t")).strip()
            if t:
                out.append(f"- {t}")
        out.append("")
    return out


def podglad(plik: Path) -> str:
    with zipfile.ZipFile(plik) as z:
        linie = {".docx": docx, ".xlsx": xlsx, ".pptx": pptx}[plik.suffix.lower()](z)
    while linie and not linie[-1]:
        linie.pop()
    return "\n".join(linie) + "\n"


def plik_podgladu(oryginal: Path) -> Path:
    return PODGLAD / (oryginal.name + ".md")


def tresc_podgladu(oryginal: Path) -> str:
    linie = [("> [ukryto w podglądzie: tekst wygląda na polecenie dla AI (prompt injection), zobacz kontrolę bazy]"
              if UKRYTE_POLECENIA.search(l) else l) for l in podglad(oryginal).split("\n")]
    return (f"<!-- Podgląd tekstowy pliku {oryginal.name}, generowany skryptem narzedzia/podglad_tekstowy.py. "
            f"Nie edytuj: zmień oryginał. -->\n# Podgląd: `zalaczniki/oryginaly/{oryginal.name}`\n\n" + "\n".join(linie))


def wszystkie(tylko_sprawdz: bool) -> int:
    oczekiwane = {plik_podgladu(o): tresc_podgladu(o) for o in sorted(ORYGINALY.glob("*")) if o.suffix.lower() in OBSLUGIWANE}
    istniejace = set(PODGLAD.glob("*.md")) if PODGLAD.exists() else set()
    rozne = [p for p, t in oczekiwane.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    zbedne = sorted(istniejace - set(oczekiwane))
    if tylko_sprawdz:
        for p in rozne:
            print("NIEAKTUALNY", p.relative_to(ROOT).as_posix())
        for p in zbedne:
            print("ZBĘDNY    ", p.relative_to(ROOT).as_posix())
        print(f"Podgląd: plików {len(oczekiwane)}, do odświeżenia {len(rozne)}, zbędnych {len(zbedne)}.")
        return 1 if rozne or zbedne else 0
    PODGLAD.mkdir(parents=True, exist_ok=True)
    for p in rozne:
        p.write_text(oczekiwane[p], encoding="utf-8", newline="\n")
    for p in zbedne:
        p.unlink()
    print(f"Podgląd: plików {len(oczekiwane)}, zapisano {len(rozne)}, usunięto {len(zbedne)}.")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if len(sys.argv) == 2 and sys.argv[1] in ("--wszystkie", "--sprawdz"):
        sys.exit(wszystkie(sys.argv[1] == "--sprawdz"))
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    plik = Path(sys.argv[1])
    if plik.suffix.lower() not in OBSLUGIWANE:
        sys.stdout.write(plik.read_bytes().decode("utf-8", "replace"))
    else:
        try:
            sys.stdout.write(podglad(plik))
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
            sys.stdout.write(f"(nie udało się odczytać {plik.name}: {e})\n")
