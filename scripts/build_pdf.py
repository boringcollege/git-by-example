#!/usr/bin/env python3
"""
Build a designed PDF of "Git By Example" from the markdown source files.

Usage: python scripts/build_pdf.py [output_filename.pdf]
"""

import sys
import os
import re
import markdown
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Flowable, KeepTogether, Frame, PageTemplate, BaseDocTemplate,
    NextPageTemplate, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents
import datetime

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
CLR_BG_DARK    = HexColor("#1a1b26")    # Tokyo Night dark bg
CLR_BG_CODE    = HexColor("#24283b")    # Code block bg
CLR_ACCENT     = HexColor("#7aa2f7")    # Bright blue
CLR_ACCENT2    = HexColor("#bb9af7")    # Purple
CLR_ACCENT3    = HexColor("#9ece6a")    # Green
CLR_ORANGE     = HexColor("#ff9e64")    # Orange
CLR_RED        = HexColor("#f7768e")    # Red / warning
CLR_TEXT       = HexColor("#2e3440")    # Dark text
CLR_TEXT_LIGHT = HexColor("#565e6c")    # Secondary text
CLR_BORDER     = HexColor("#d0d7e3")    # Light border
CLR_BG_TIP     = HexColor("#e8f4f8")    # Tip box bg
CLR_BG_WARN    = HexColor("#fef3e2")    # Warning box bg
CLR_BG_PAGE    = HexColor("#fafbfc")    # Page background hint
CLR_WHITE      = white

PAGE_W, PAGE_H = A4
MARGIN_LEFT   = 2.2 * cm
MARGIN_RIGHT  = 2.2 * cm
MARGIN_TOP    = 2.5 * cm
MARGIN_BOTTOM = 2.5 * cm

# ---------------------------------------------------------------------------
# Ordered list of source files
# ---------------------------------------------------------------------------
CHAPTERS = [
    ("chapters/01-getting-started.md",      "Part I — Foundations"),
    ("chapters/02-the-basics.md",           None),
    ("chapters/03-viewing-history.md",      None),
    ("chapters/04-undoing-things.md",       None),
    ("chapters/05-branches.md",             "Part II — Branching & Collaboration"),
    ("chapters/06-merging.md",              None),
    ("chapters/07-rebasing.md",             None),
    ("chapters/08-remotes.md",              None),
    ("chapters/09-stashing.md",             "Part III — Intermediate Techniques"),
    ("chapters/10-tagging.md",              None),
    ("chapters/11-cherry-picking.md",       None),
    ("chapters/12-interactive-rebase.md",   None),
    ("chapters/13-git-internals.md",        "Part IV — Advanced Topics"),
    ("chapters/14-reflog.md",              None),
    ("chapters/15-bisect.md",              None),
    ("chapters/16-worktrees.md",           None),
    ("chapters/17-submodules.md",          None),
    ("chapters/18-branching-strategies.md", "Part V — Real-World Workflows"),
    ("chapters/19-commit-messages.md",      None),
    ("chapters/20-git-hooks.md",            None),
    ("chapters/21-tips-and-tricks.md",      None),
    ("appendices/config-cheatsheet.md",     "Appendices"),
    ("appendices/gitignore-patterns.md",    None),
    ("appendices/aliases.md",               None),
]


# ---------------------------------------------------------------------------
# Custom Flowables
# ---------------------------------------------------------------------------

class CodeBlock(Flowable):
    """A syntax-highlighted code block with rounded corners."""

    def __init__(self, code, language="", width=None):
        super().__init__()
        self.code = code.rstrip("\n")
        self.language = language
        self._width = width or (PAGE_W - MARGIN_LEFT - MARGIN_RIGHT)
        self.padding = 10 * mm
        self.line_height = 12
        self.lines = self.code.split("\n")
        self.height = self.padding * 2 + len(self.lines) * self.line_height + 4

    def wrap(self, availWidth, availHeight):
        self._width = availWidth
        self.height = self.padding + 8 + len(self.lines) * self.line_height + self.padding
        return (self._width, self.height)

    def draw(self):
        c = self.canv
        w, h = self._width, self.height
        r = 4 * mm

        # Background
        c.setFillColor(CLR_BG_DARK)
        c.roundRect(0, 0, w, h, r, fill=1, stroke=0)

        # Language badge
        if self.language:
            c.setFont("Helvetica", 7)
            c.setFillColor(CLR_TEXT_LIGHT)
            tw = c.stringWidth(self.language.upper(), "Helvetica", 7)
            c.roundRect(w - tw - 16, h - 18, tw + 12, 14, 3, fill=0, stroke=0)
            c.setFillColor(HexColor("#565e6c"))
            c.drawString(w - tw - 10, h - 14.5, self.language.upper())

        # Code lines
        c.setFont("Courier", 8.5)
        y = h - self.padding - 4
        for line in self.lines:
            # Simple syntax coloring
            display_line = line
            color = HexColor("#a9b1d6")  # default text

            stripped = line.lstrip()
            if stripped.startswith("#") and not stripped.startswith("#!"):
                color = HexColor("#565a6e")  # comment
            elif stripped.startswith(("$", "git ", "npm ", "echo ", "mkdir ", "cd ", "ls ", "cat ", "rm ", "find ", "chmod ")):
                color = CLR_ACCENT3
            elif stripped.startswith(("+++", "---", "diff ")):
                color = CLR_ACCENT
            elif stripped.startswith("+"):
                color = CLR_ACCENT3
            elif stripped.startswith("-"):
                color = CLR_RED
            elif stripped.startswith(("*", "error:", "fatal:", "CONFLICT")):
                color = CLR_ORANGE
            elif any(stripped.startswith(k) for k in ("pick ", "reword ", "edit ", "squash ", "fixup ", "drop ")):
                color = CLR_ACCENT2

            c.setFillColor(color)
            # Truncate long lines
            max_chars = int((w - self.padding * 2) / 4.5)
            if len(display_line) > max_chars:
                display_line = display_line[:max_chars - 1] + "…"
            c.drawString(self.padding, y, display_line)
            y -= self.line_height


class TipBox(Flowable):
    """A callout box for tips (🧠) or warnings (⚠️)."""

    def __init__(self, text, kind="tip", width=None):
        super().__init__()
        self.text = text
        self.kind = kind  # "tip" or "warning"
        self._width = width or (PAGE_W - MARGIN_LEFT - MARGIN_RIGHT)
        self._calculated = False

    def _calc(self, availWidth):
        self._width = availWidth
        style = ParagraphStyle(
            "tiptext", fontName="Helvetica", fontSize=8.5,
            leading=13, textColor=CLR_TEXT
        )
        self._para = Paragraph(self.text, style)
        pw, ph = self._para.wrap(availWidth - 18 * mm, 1000)
        self.height = max(ph + 10 * mm, 14 * mm)
        self._calculated = True

    def wrap(self, availWidth, availHeight):
        self._calc(availWidth)
        return (self._width, self.height)

    def draw(self):
        c = self.canv
        w, h = self._width, self.height
        r = 3 * mm

        bg = CLR_BG_TIP if self.kind == "tip" else CLR_BG_WARN
        accent = CLR_ACCENT if self.kind == "tip" else CLR_ORANGE

        # Background
        c.setFillColor(bg)
        c.roundRect(0, 0, w, h, r, fill=1, stroke=0)

        # Left accent bar
        c.setFillColor(accent)
        c.roundRect(0, 0, 3, h, 1, fill=1, stroke=0)

        # Icon
        icon = "🧠" if self.kind == "tip" else "⚠"
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(accent)
        c.drawString(5 * mm, h - 9 * mm, icon)

        # Text
        self._para.drawOn(c, 12 * mm, 4 * mm)


class PartDivider(Flowable):
    """Full-width part divider page."""

    def __init__(self, title):
        super().__init__()
        self.title = title
        self.height = 200 * mm  # fixed safe height

    def wrap(self, availWidth, availHeight):
        self.height = min(self.height, availHeight - 2)
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        w = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
        h = self.height

        # Large accent circle
        c.setFillColor(CLR_ACCENT)
        c.setStrokeColor(CLR_ACCENT)
        c.setLineWidth(0)
        c.circle(w / 2, h * 0.55, 18 * mm, fill=1, stroke=0)

        # Part number/title
        c.setFillColor(CLR_WHITE)
        c.setFont("Helvetica-Bold", 14)
        tw = c.stringWidth(self.title.split("—")[0].strip(), "Helvetica-Bold", 14)
        c.drawCentredString(w / 2, h * 0.55 + 2, self.title.split("—")[0].strip())

        # Subtitle
        if "—" in self.title:
            subtitle = self.title.split("—", 1)[1].strip()
            c.setFillColor(CLR_TEXT)
            c.setFont("Helvetica", 20)
            c.drawCentredString(w / 2, h * 0.55 - 40 * mm, subtitle)

        # Decorative line
        c.setStrokeColor(CLR_BORDER)
        c.setLineWidth(0.5)
        lw = 60 * mm
        c.line(w / 2 - lw / 2, h * 0.55 - 52 * mm, w / 2 + lw / 2, h * 0.55 - 52 * mm)


class ChapterHeader(Flowable):
    """Styled chapter header."""

    def __init__(self, number, title):
        super().__init__()
        self.number = number
        self.title = title
        self.height = 28 * mm

    def wrap(self, availWidth, availHeight):
        self._width = availWidth
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        w = self._width

        # Chapter number
        c.setFillColor(CLR_ACCENT)
        c.setFont("Helvetica", 11)
        c.drawString(0, self.height - 8 * mm, self.number)

        # Accent line
        c.setStrokeColor(CLR_ACCENT)
        c.setLineWidth(2)
        c.line(0, self.height - 11 * mm, 30 * mm, self.height - 11 * mm)

        # Title
        c.setFillColor(CLR_TEXT)
        c.setFont("Helvetica-Bold", 22)
        # Handle long titles
        title = self.title
        if len(title) > 40:
            c.setFont("Helvetica-Bold", 18)
        c.drawString(0, self.height - 24 * mm, title)


# ---------------------------------------------------------------------------
# Page templates
# ---------------------------------------------------------------------------

def page_background_normal(canvas_obj, doc):
    """Draw header/footer on normal pages."""
    c = canvas_obj
    c.saveState()

    # Top line
    c.setStrokeColor(CLR_BORDER)
    c.setLineWidth(0.4)
    c.line(MARGIN_LEFT, PAGE_H - MARGIN_TOP + 5 * mm,
           PAGE_W - MARGIN_RIGHT, PAGE_H - MARGIN_TOP + 5 * mm)

    # Header text
    c.setFont("Helvetica", 7)
    c.setFillColor(CLR_TEXT_LIGHT)
    c.drawString(MARGIN_LEFT, PAGE_H - MARGIN_TOP + 7 * mm, "Git By Example")
    c.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - MARGIN_TOP + 7 * mm,
                      "Dariush Abbasi")

    # Bottom line
    c.line(MARGIN_LEFT, MARGIN_BOTTOM - 5 * mm,
           PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM - 5 * mm)

    # Page number
    c.setFont("Helvetica", 8)
    c.setFillColor(CLR_TEXT_LIGHT)
    c.drawCentredString(PAGE_W / 2, MARGIN_BOTTOM - 10 * mm, str(doc.page))

    c.restoreState()


def page_background_blank(canvas_obj, doc):
    """No header/footer (for title page, part dividers)."""
    pass


# ---------------------------------------------------------------------------
# Markdown → Flowables converter
# ---------------------------------------------------------------------------

def make_styles():
    """Create the paragraph styles used throughout the book."""
    return {
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9.5,
            leading=15, textColor=CLR_TEXT, spaceAfter=6,
            spaceBefore=2
        ),
        "h1": ParagraphStyle(
            "h1", fontName="Helvetica-Bold", fontSize=22,
            leading=28, textColor=CLR_TEXT, spaceAfter=8,
            spaceBefore=16
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold", fontSize=14,
            leading=20, textColor=CLR_TEXT, spaceAfter=6,
            spaceBefore=14
        ),
        "h3": ParagraphStyle(
            "h3", fontName="Helvetica-Bold", fontSize=11,
            leading=16, textColor=CLR_ACCENT, spaceAfter=4,
            spaceBefore=10
        ),
        "h4": ParagraphStyle(
            "h4", fontName="Helvetica-Bold", fontSize=10,
            leading=14, textColor=CLR_TEXT, spaceAfter=4,
            spaceBefore=8
        ),
        "inline_code": ParagraphStyle(
            "inline_code", fontName="Courier", fontSize=8.5,
            leading=13, textColor=CLR_TEXT, backColor=HexColor("#eef0f5"),
        ),
        "blockquote": ParagraphStyle(
            "blockquote", fontName="Helvetica-Oblique", fontSize=10,
            leading=15, textColor=CLR_TEXT_LIGHT, leftIndent=12 * mm,
            borderPadding=4, spaceAfter=8, spaceBefore=8
        ),
        "li": ParagraphStyle(
            "li", fontName="Helvetica", fontSize=9.5,
            leading=14, textColor=CLR_TEXT, leftIndent=8 * mm,
            bulletIndent=3 * mm, spaceAfter=3,
        ),
    }


def inline_format(text):
    """Convert markdown inline formatting to ReportLab XML."""
    # Bold + italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`',
                  r'<font face="Courier" size="8" color="#5b21b6">\1</font>', text)
    # Links — just show text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'<u>\1</u>', text)
    # Escape XML-sensitive characters that aren't already tags
    # (We can't blindly escape because we've added XML tags above)
    return text


def md_to_flowables(md_text, styles, chapter_num=None):
    """Convert a markdown string into a list of ReportLab flowables."""
    flowables = []
    lines = md_text.split("\n")
    i = 0
    first_h1 = True

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip navigation links at bottom of chapters
        if stripped.startswith("[←") or stripped.startswith("[Next:"):
            i += 1
            continue

        # Horizontal rule
        if stripped in ("---", "***", "___"):
            flowables.append(Spacer(1, 6 * mm))
            i += 1
            continue

        # Empty line
        if not stripped:
            i += 1
            continue

        # Headings
        if stripped.startswith("#"):
            level = len(stripped.split()[0])  # count #'s
            title = stripped.lstrip("#").strip()

            if level == 1 and first_h1:
                # Chapter title — use custom header
                first_h1 = False
                num_label = f"Chapter {chapter_num}" if chapter_num else ""
                flowables.append(ChapterHeader(num_label, title.split("—", 1)[-1].strip() if "—" in title else title))
                flowables.append(Spacer(1, 4 * mm))
                i += 1
                continue

            style_key = f"h{min(level, 4)}"
            flowables.append(Paragraph(inline_format(title), styles[style_key]))
            i += 1
            continue

        # Code blocks
        if stripped.startswith("```"):
            language = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code_text = "\n".join(code_lines)
            flowables.append(Spacer(1, 2 * mm))
            flowables.append(CodeBlock(code_text, language))
            flowables.append(Spacer(1, 3 * mm))
            continue

        # Blockquotes
        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            quote_text = " ".join(quote_lines)
            flowables.append(Spacer(1, 2 * mm))
            flowables.append(Paragraph(inline_format(quote_text), styles["blockquote"]))
            flowables.append(Spacer(1, 2 * mm))
            continue

        # Tip boxes (🧠 What happened?)
        if "🧠" in stripped or stripped.startswith("🧠"):
            tip_text = stripped.replace("🧠", "").strip()
            # Remove bold markers from "What happened?"
            tip_text = tip_text.replace("**What happened?**", "<b>What happened?</b>")
            tip_text = inline_format(tip_text)
            flowables.append(TipBox(tip_text, kind="tip"))
            flowables.append(Spacer(1, 3 * mm))
            i += 1
            continue

        # Warning boxes
        if stripped.startswith("⚠️") or stripped.startswith("⚠"):
            warn_text = stripped.replace("⚠️", "").replace("⚠", "").strip()
            warn_text = warn_text.replace("**Warning**:", "<b>Warning</b>:")
            warn_text = warn_text.replace("**Warning:**", "<b>Warning:</b>")
            warn_text = inline_format(warn_text)
            flowables.append(TipBox(warn_text, kind="warning"))
            flowables.append(Spacer(1, 3 * mm))
            i += 1
            continue

        # Unordered list items
        if stripped.startswith("- ") or stripped.startswith("* "):
            text = stripped[2:]
            flowables.append(
                Paragraph("• " + inline_format(text), styles["li"])
            )
            i += 1
            continue

        # Ordered list items
        m = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if m:
            num = m.group(1)
            text = m.group(2)
            flowables.append(
                Paragraph(f"{num}. " + inline_format(text), styles["li"])
            )
            i += 1
            continue

        # Tables (simple rendering)
        if "|" in stripped and stripped.startswith("|"):
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                # Skip separator rows
                if re.match(r'^\|[\s\-:|]+\|$', row):
                    i += 1
                    continue
                cells = [c.strip() for c in row.split("|")[1:-1]]
                table_rows.append(cells)
                i += 1

            if table_rows:
                # Build reportlab table
                col_count = max(len(r) for r in table_rows)
                # Pad rows to same length
                for r in table_rows:
                    while len(r) < col_count:
                        r.append("")

                cell_style = ParagraphStyle("cell", fontName="Helvetica", fontSize=8,
                                             leading=11, textColor=CLR_TEXT)
                cell_style_h = ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8,
                                               leading=11, textColor=CLR_TEXT)

                data = []
                for ri, row in enumerate(table_rows):
                    st = cell_style_h if ri == 0 else cell_style
                    data.append([Paragraph(inline_format(c), st) for c in row])

                avail_w = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
                col_w = avail_w / col_count
                t = Table(data, colWidths=[col_w] * col_count)
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#e8ecf2")),
                    ("GRID", (0, 0), (-1, -1), 0.4, CLR_BORDER),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
                ]))
                flowables.append(Spacer(1, 2 * mm))
                flowables.append(t)
                flowables.append(Spacer(1, 3 * mm))
            continue

        # Normal paragraph — collect consecutive non-empty, non-special lines
        para_lines = []
        while i < len(lines):
            l = lines[i].strip()
            if (not l or l.startswith("#") or l.startswith("```")
                    or l.startswith(">") or l.startswith("- ") or l.startswith("* ")
                    or l.startswith("|") or "🧠" in l or l.startswith("⚠")
                    or l in ("---", "***", "___")
                    or re.match(r'^\d+\.\s+', l)
                    or l.startswith("[←") or l.startswith("[Next:")):
                break
            para_lines.append(l)
            i += 1
        if para_lines:
            text = " ".join(para_lines)
            flowables.append(Paragraph(inline_format(text), styles["body"]))

    return flowables


# ---------------------------------------------------------------------------
# Title Page
# ---------------------------------------------------------------------------

def build_title_page():
    """Return flowables for the title page."""
    flowables = []

    flowables.append(Spacer(1, 60 * mm))

    # Title
    title_style = ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=36,
        leading=42, textColor=CLR_TEXT, alignment=TA_LEFT
    )
    flowables.append(Paragraph("Git By<br/>Example", title_style))

    flowables.append(Spacer(1, 6 * mm))

    # Accent bar
    class AccentBar(Flowable):
        def __init__(self):
            super().__init__()
            self.height = 4
        def wrap(self, aw, ah):
            return (60 * mm, 4)
        def draw(self):
            self.canv.setFillColor(CLR_ACCENT)
            self.canv.rect(0, 0, 60 * mm, 3, fill=1, stroke=0)

    flowables.append(AccentBar())
    flowables.append(Spacer(1, 8 * mm))

    # Subtitle
    sub_style = ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=13,
        leading=19, textColor=CLR_TEXT_LIGHT
    )
    flowables.append(Paragraph(
        "A practical guide to Git — learn by doing,<br/>not by reading manuals.",
        sub_style
    ))

    flowables.append(Spacer(1, 40 * mm))

    # Author
    author_style = ParagraphStyle(
        "author", fontName="Helvetica", fontSize=12,
        leading=16, textColor=CLR_TEXT
    )
    flowables.append(Paragraph("<b>Dariush Abbasi</b>", author_style))

    flowables.append(Spacer(1, 4 * mm))

    # Date
    date_style = ParagraphStyle(
        "date", fontName="Helvetica", fontSize=9,
        leading=13, textColor=CLR_TEXT_LIGHT
    )
    date_str = datetime.datetime.now().strftime("%B %Y")
    flowables.append(Paragraph(date_str, date_style))

    flowables.append(Spacer(1, 6 * mm))

    # URL
    url_style = ParagraphStyle(
        "url", fontName="Courier", fontSize=8,
        leading=12, textColor=CLR_ACCENT
    )
    flowables.append(Paragraph("github.com/boringcollege/git-by-example", url_style))

    flowables.append(PageBreak())
    return flowables


# ---------------------------------------------------------------------------
# Table of Contents page
# ---------------------------------------------------------------------------

def build_toc_page(styles):
    """Build a manual table of contents."""
    flowables = []

    flowables.append(Spacer(1, 10 * mm))

    toc_title = ParagraphStyle(
        "toc_title", fontName="Helvetica-Bold", fontSize=20,
        leading=26, textColor=CLR_TEXT, spaceAfter=8 * mm
    )
    flowables.append(Paragraph("Table of Contents", toc_title))

    part_style = ParagraphStyle(
        "toc_part", fontName="Helvetica-Bold", fontSize=10,
        leading=16, textColor=CLR_ACCENT, spaceBefore=6 * mm, spaceAfter=2 * mm
    )
    chapter_style = ParagraphStyle(
        "toc_chapter", fontName="Helvetica", fontSize=9.5,
        leading=16, textColor=CLR_TEXT, leftIndent=5 * mm
    )

    chapter_num = 0
    for filepath, part_name in CHAPTERS:
        if part_name:
            flowables.append(Paragraph(part_name, part_style))

        fname = os.path.basename(filepath)
        if fname.startswith(("0", "1", "2")):
            chapter_num += 1
            # Extract title from filename
            title = fname.replace(".md", "").split("-", 1)[1].replace("-", " ").title()
            flowables.append(
                Paragraph(f"{chapter_num}. &nbsp; {title}", chapter_style)
            )
        else:
            title = fname.replace(".md", "").replace("-", " ").title()
            flowables.append(
                Paragraph(f"&nbsp;&nbsp;&nbsp; {title}", chapter_style)
            )

    flowables.append(PageBreak())
    return flowables


# ---------------------------------------------------------------------------
# Main build function
# ---------------------------------------------------------------------------

def build_pdf(output_path):
    """Build the complete PDF."""
    # Find repo root (script is in scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    # Create document
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Git By Example",
        author="Dariush Abbasi",
        subject="A practical guide to Git",
    )

    # Page templates
    frame_normal = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM,
        PAGE_W - MARGIN_LEFT - MARGIN_RIGHT,
        PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        id="normal"
    )
    frame_title = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM,
        PAGE_W - MARGIN_LEFT - MARGIN_RIGHT,
        PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        id="title"
    )

    doc.addPageTemplates([
        PageTemplate(id="blank", frames=frame_title, onPage=page_background_blank),
        PageTemplate(id="normal", frames=frame_normal, onPage=page_background_normal),
    ])

    styles = make_styles()
    story = []

    # Title page (uses blank template)
    story.append(NextPageTemplate("blank"))
    story.extend(build_title_page())

    # TOC (switch to normal template)
    story.append(NextPageTemplate("normal"))
    story.extend(build_toc_page(styles))

    # Chapters
    chapter_num = 0
    for filepath, part_name in CHAPTERS:
        full_path = os.path.join(repo_root, filepath)
        if not os.path.exists(full_path):
            print(f"  ⚠ Skipping {filepath} (not found)")
            continue

        # Part divider
        if part_name:
            story.append(NextPageTemplate("blank"))
            story.append(PageBreak())
            story.append(PartDivider(part_name))
            story.append(NextPageTemplate("normal"))
            story.append(PageBreak())

        fname = os.path.basename(filepath)
        is_chapter = fname[0].isdigit()
        if is_chapter:
            chapter_num += 1

        with open(full_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        ch_num = chapter_num if is_chapter else None
        flowables = md_to_flowables(md_text, styles, chapter_num=ch_num)
        story.extend(flowables)
        story.append(PageBreak())

    # Build
    print(f"  Building {output_path} ...")
    doc.build(story)
    print(f"  ✅ Done! {os.path.getsize(output_path) / 1024:.0f} KB")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "gitbyexample.pdf"
    build_pdf(output)