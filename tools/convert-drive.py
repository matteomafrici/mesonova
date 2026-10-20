#!/usr/bin/env python3
"""Convert the colleague drive snapshot into Markdown under sources/.

What gets converted, and why:
  .docx  -> docling (structure, headings, tables, figures)
  .xlsx  -> openpyxl (table fidelity; docling is weaker on spec sheets)
  everything else (.pdf .png .csv .py .md .txt) is LEFT ALONE and only recorded
  in the manifest: PDFs already render in Obsidian and on GitHub, so converting
  them would only add megabytes of text nobody needs.

Output layout:
  sources/<drive-name>/<topical>/<slug>.md     one file per converted document
  sources/<drive-name>/<topical>/figures/      figures, referenced relatively
  sources/<drive-name>/manifest.md             every drive file: author, date, fate
  sources/<drive-name>/README.md               one sentence

Converted files are GENERATED: never edit them by hand, re-run this script.

Usage:
    python tools/convert-drive.py [drive-dir]
Defaults to onedrive/2026-10-20 and writes to sources/drive-2026-10-20.
Idempotent: a file is re-converted only if the source is newer than the output.
"""

import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import zipfile

from openpyxl import load_workbook

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCX_EXT = ".docx"
XLSX_EXT = ".xlsx"
FIG_RE = re.compile(r"!\[([^\]]*)\]\(file:///([^)]+)\)")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def slug(text):
    s = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", s) or "document"


def topical_dir(relpath):
    """Top-level folder of the drive, slugified; drive root files go to '.'."""
    parts = relpath.replace("\\", "/").split("/")
    if len(parts) == 1:
        return "."
    return slug(parts[0])


def office_metadata(path):
    """Author and date from a .docx/.xlsx core.xml. Returns (author, date)."""
    try:
        with zipfile.ZipFile(path) as z:
            core = [n for n in z.namelist() if n.endswith("docProps/core.xml")]
            if not core:
                return "", ""
            x = z.read(core[0]).decode("utf-8", "replace")
    except Exception:
        return "", ""
    creator = (re.search(r"<dc:creator>(.*?)</dc:creator>", x) or [None, ""])[1]
    lastmod = (re.search(r"<cp:lastModifiedBy>(.*?)</cp:lastModifiedBy>", x) or [None, ""])[1]
    created = (re.search(r"<dcterms:created[^>]*>(.*?)</dcterms:created>", x) or [None, ""])[1]
    modified = (re.search(r"<dcterms:modified[^>]*>(.*?)</dcterms:modified>", x) or [None, ""])[1]
    author = creator or lastmod
    if lastmod and creator and lastmod != creator:
        author = "%s (mod. %s)" % (creator, lastmod)
    date = modified or created
    return author, date[:19].replace("T", " ")


def pdf_metadata(path):
    try:
        with open(path, "rb") as fh:
            head = fh.read(400000)
    except Exception:
        return "", ""
    author = re.search(rb"/Author\s*\(([^)]{0,200})\)", head)
    title = re.search(rb"/Title\s*\(([^)]{0,200})\)", head)
    def dec(m):
        return m.group(1).decode("latin-1", "replace").strip() if m else ""
    return dec(author), dec(title)


def banner(source_rel, author, date, tool, snapshot):
    bits = ["**Source:** %s, `%s`" % (snapshot, source_rel)]
    bits.append("**Author:** %s" % (author or "n/d"))
    if date:
        bits.append("**Date:** %s" % date)
    bits.append("*converted with %s - generated, do not edit*" % tool)
    return "> " + " | ".join(bits) + "\n\n"


# --------------------------------------------------------------------------
# converters
# --------------------------------------------------------------------------

def convert_docx(src, out_md, out_fig_dir, slug_name):
    """docling -> markdown, then move figures and rewrite their references."""
    tmp = tempfile.mkdtemp(prefix="docling-")
    try:
        proc = subprocess.run(
            ["docling", "convert", src, "--to", "md", "--output", tmp,
             "--image-export-mode", "referenced"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        stamp = re.search(r"docling v?([\d.]+)", proc.stdout + proc.stderr)
        tool = "docling %s" % (stamp.group(1) if stamp else "")
        if proc.returncode != 0:
            return None, tool, "docling failed: %s" % (proc.stderr or "")[-300:]

        stem = os.path.splitext(os.path.basename(src))[0]
        produced = None
        for root, _dirs, files in os.walk(tmp):
            for f in files:
                if f == stem + ".md":
                    produced = os.path.join(root, f)
        if not produced:
            return None, tool, "docling produced no markdown"

        text = open(produced, encoding="utf-8").read()

        # move artefacts -> figures/<slug>-fig-NN.png and rewrite references
        figs = []
        for root, _dirs, files in os.walk(tmp):
            if root.endswith("_artifacts"):
                figs = sorted(os.path.join(root, f) for f in files)
        fig_map = {}
        counter = 0
        for old in figs:
            counter += 1
            ext = os.path.splitext(old)[1].lower() or ".png"
            new_name = "%s-fig-%02d%s" % (slug_name, counter, ext)
            fig_map[os.path.basename(old)] = new_name
            os.makedirs(out_fig_dir, exist_ok=True)
            shutil.copy2(old, os.path.join(out_fig_dir, new_name))

        def rewrite(match):
            raw = urllib.parse.unquote(match.group(2)).replace("\\", "/")
            new = fig_map.get(os.path.basename(raw))
            if not new:
                return match.group(0)
            return "![%s](figures/%s)" % (match.group(1), new)

        text = FIG_RE.sub(rewrite, text)
        text = text.replace("file:///", "")
        return text, tool, None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def convert_xlsx(src):
    """openpyxl -> markdown tables, one section per sheet."""
    wb = load_workbook(src, data_only=True)
    out = []
    for ws in wb.worksheets:
        rows = []
        for row in ws.iter_rows(values_only=True):
            cells = ["" if v is None else str(v).replace("\n", " ").strip() for v in row]
            while cells and cells[-1] == "":
                cells.pop()
            if cells:
                rows.append(cells)
        if not rows:
            continue
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        out.append("## Sheet: %s" % ws.title)
        out.append("")
        out.append("| " + " | ".join(rows[0]) + " |")
        out.append("|" + "---|" * width)
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
        out.append("")
    return "\n".join(out), "openpyxl", None


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main(argv):
    drive = argv[1] if len(argv) > 1 else os.path.join(REPO, "onedrive", "2026-10-20")
    if not os.path.isdir(drive):
        print("drive not found: %s" % drive)
        return 1
    drive_name = "drive-" + os.path.basename(drive.rstrip("\\/"))
    out_root = os.path.join(REPO, "sources", drive_name)
    os.makedirs(out_root, exist_ok=True)

    manifest = []
    converted = 0
    skipped = 0

    for root, dirs, files in os.walk(drive):
        dirs.sort()
        for name in sorted(files):
            src = os.path.join(root, name)
            rel = os.path.relpath(src, drive)
            ext = os.path.splitext(name)[1].lower()
            topical = topical_dir(rel)
            dest_dir = out_root if topical == "." else os.path.join(out_root, topical)

            if ext in (DOCX_EXT, XLSX_EXT):
                slug_name = slug(os.path.splitext(name)[0])
                out_md = os.path.join(dest_dir, slug_name + ".md")
                author, date = office_metadata(src)
                if os.path.exists(out_md) and os.path.getmtime(out_md) > os.path.getmtime(src):
                    manifest.append((rel, author, date, "`%s` (up to date)" % os.path.relpath(out_md, out_root).replace("\\", "/")))
                    skipped += 1
                    continue
                os.makedirs(dest_dir, exist_ok=True)
                if ext == DOCX_EXT:
                    body, tool, err = convert_docx(src, out_md, os.path.join(dest_dir, "figures"), slug_name)
                else:
                    body, tool, err = convert_xlsx(src)
                if err:
                    manifest.append((rel, author, date, "**CONVERSION FAILED** - %s" % err))
                    print("  FAIL %s: %s" % (rel, err))
                    continue
                with open(out_md, "w", encoding="utf-8") as fh:
                    fh.write(banner(rel.replace("\\", "/"), author, date, tool, drive_name))
                    fh.write(body.rstrip() + "\n")
                manifest.append((rel, author, date, "`%s`" % os.path.relpath(out_md, out_root).replace("\\", "/")))
                converted += 1
                print("  ok   %s -> %s" % (rel, os.path.relpath(out_md, REPO)))
            else:
                if ext == ".pdf":
                    author, title = pdf_metadata(src)
                    note = "left as PDF (renders in Obsidian and on GitHub)"
                    if title:
                        note += " - title: %s" % title
                else:
                    author, note = "", "left as-is (already text, %s)" % (ext or "no extension")
                    if ext in (".png", ".jpg", ".jpeg", ".gif"):
                        note = "left as-is (image, %s)" % ext
                manifest.append((rel, author, "", note))

    # ---- manifest.md
    lines = ["# Drive manifest - %s" % os.path.basename(drive.rstrip("\\/")), "",
             "Every file in the drive snapshot, where it went, and who wrote it (from the",
             "document metadata - the field is empty when the file carries none).", "",
             "| File in drive | Author (metadata) | Date | Fate |", "|---|---|---|---|"]
    for rel, author, date, note in sorted(manifest):
        lines.append("| `%s` | %s | %s | %s |" % (rel.replace("\\", "/"), author or "n/d", date or "-", note))
    lines += ["", "Regenerate with `python tools/convert-drive.py`."]
    with open(os.path.join(out_root, "manifest.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("converted %d, skipped %d, manifest rows %d" % (converted, skipped, len(manifest)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
