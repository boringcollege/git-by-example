#!/usr/bin/env python3
"""
Build designed PDFs of "Git By Example" from the markdown source files.

Produces two variants:
  - Light mode (default)
  - Dark mode

Usage:
  python scripts/build_pdf.py <output.pdf>              # light mode
  python scripts/build_pdf.py <output.pdf> --dark        # dark mode
  python scripts/build_pdf.py <basename>   --both        # both variants
"""

import sys, os, re, datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, Table, TableStyle,
    Flowable, Frame, PageTemplate, BaseDocTemplate, NextPageTemplate,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.token import Token

# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 2.2*cm, 2.2*cm, 2.5*cm, 2.5*cm
CW = PAGE_W - ML - MR

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

LEXER_MAP = {
    "bash":"bash","sh":"bash","shell":"bash","zsh":"bash",
    "python":"python","py":"python","javascript":"javascript","js":"javascript",
    "json":"json","yaml":"yaml","yml":"yaml","ini":"ini","toml":"toml",
    "diff":"diff","patch":"diff","gitignore":"ini","powershell":"powershell",
    "go":"go","rust":"rust","java":"java","html":"html","css":"css",
}


# ═══════════════════════════════════════════════════════════════════════════
# Fonts
# ═══════════════════════════════════════════════════════════════════════════

def setup_fonts():
    sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    pdfmetrics.registerFont(TTFont("Inter",    os.path.join(sd, "Inter-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-B",  os.path.join(sd, "Inter-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-I",  os.path.join(sd, "Inter-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-BI", os.path.join(sd, "Inter-BoldItalic.ttf")))
    registerFontFamily("Inter", normal="Inter", bold="Inter-B",
                       italic="Inter-I", boldItalic="Inter-BI")

    pdfmetrics.registerFont(TTFont("Plex",    os.path.join(sd, "IBMPlexMono-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Plex-B",  os.path.join(sd, "IBMPlexMono-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Plex-I",  os.path.join(sd, "IBMPlexMono-Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Plex-BI", os.path.join(sd, "IBMPlexMono-BoldItalic.ttf")))
    registerFontFamily("Plex", normal="Plex", bold="Plex-B",
                       italic="Plex-I", boldItalic="Plex-BI")


# ═══════════════════════════════════════════════════════════════════════════
# Themes — Claude.ai branding colors
# ═══════════════════════════════════════════════════════════════════════════

def _hx(s):
    return HexColor(s)

def theme(dark=False):
    if dark:
        return dict(
            page_bg      = _hx("#1B1B1F"),
            text         = _hx("#E8E4DD"),
            text2        = _hx("#9B9590"),
            accent       = _hx("#DA7756"),
            accent2      = _hx("#E8A87C"),
            heading      = _hx("#F4F3EE"),
            h3           = _hx("#DA7756"),
            code_bg      = _hx("#131316"),
            border       = _hx("#3A3A40"),
            tip_bg       = _hx("#2A2520"),
            warn_bg      = _hx("#2E2518"),
            tbl_hdr      = _hx("#2A2A30"),
            tbl_brd      = _hx("#3A3A40"),
            ic_fg        = _hx("#E8A87C"),
            ic_bg        = _hx("#2A2A30"),
            badge_fg     = _hx("#131316"),
            # syntax
            tk_kw=_hx("#DA7756"), tk_str=_hx("#A3BE8C"), tk_cmt=_hx("#6B6560"),
            tk_num=_hx("#D08770"), tk_fn=_hx("#E8A87C"), tk_op=_hx("#D4D0C8"),
            tk_bi=_hx("#EBCB8B"), tk_var=_hx("#E8E4DD"), tk_add=_hx("#A3BE8C"),
            tk_del=_hx("#BF616A"), tk_hd=_hx("#DA7756"), tk_def=_hx("#D4D0C8"),
        )
    else:
        return dict(
            page_bg      = _hx("#FFFFFF"),
            text         = _hx("#1A1915"),
            text2        = _hx("#6B6560"),
            accent       = _hx("#DA7756"),
            accent2      = _hx("#C4623E"),
            heading      = _hx("#1A1915"),
            h3           = _hx("#DA7756"),
            code_bg      = _hx("#1A1915"),
            border       = _hx("#E8E4DD"),
            tip_bg       = _hx("#FBF8F4"),
            warn_bg      = _hx("#FEF6EE"),
            tbl_hdr      = _hx("#F4F3EE"),
            tbl_brd      = _hx("#E8E4DD"),
            ic_fg        = _hx("#C4623E"),
            ic_bg        = _hx("#F4F3EE"),
            badge_fg     = _hx("#FFFFFF"),
            # syntax
            tk_kw=_hx("#B7472A"), tk_str=_hx("#4D7A3C"), tk_cmt=_hx("#9B9590"),
            tk_num=_hx("#B7472A"), tk_fn=_hx("#8B5E3C"), tk_op=_hx("#1A1915"),
            tk_bi=_hx("#8B6914"), tk_var=_hx("#1A1915"), tk_add=_hx("#4D7A3C"),
            tk_del=_hx("#B7472A"), tk_hd=_hx("#DA7756"), tk_def=_hx("#D4D0C8"),
        )


# ═══════════════════════════════════════════════════════════════════════════
# Syntax Highlighting
# ═══════════════════════════════════════════════════════════════════════════

def tok_color(tt, T):
    """Map Pygments token type → theme color."""
    if tt in Token.Keyword:            return T["tk_kw"]
    if tt in Token.Name.Function:      return T["tk_fn"]
    if tt in Token.Name.Builtin:       return T["tk_bi"]
    if tt in Token.Name.Variable:      return T["tk_var"]
    if tt in Token.Literal.String:     return T["tk_str"]
    if tt in Token.Literal.Number:     return T["tk_num"]
    if tt in Token.Comment:            return T["tk_cmt"]
    if tt in Token.Operator:           return T["tk_op"]
    if tt in Token.Generic.Inserted:   return T["tk_add"]
    if tt in Token.Generic.Deleted:    return T["tk_del"]
    if tt in Token.Generic.Heading:    return T["tk_hd"]
    if tt in Token.Generic.Strong:     return T["tk_fn"]
    if tt in Token.Name.Decorator:     return T["tk_fn"]
    if tt in Token.Name.Class:         return T["tk_fn"]
    return T["tk_def"]

def tokenize(code, lang):
    lk = LEXER_MAP.get(lang.lower(), lang.lower()) if lang else ""
    try:
        lex = get_lexer_by_name(lk, stripall=False)
    except Exception:
        lex = TextLexer()
    toks = list(lex.get_tokens(code))
    lines = [[]]
    for tt, tv in toks:
        parts = tv.split("\n")
        for j, p in enumerate(parts):
            if j > 0:
                lines.append([])
            if p:
                lines[-1].append((p, tt))
    if lines and not lines[-1]:
        lines.pop()
    return lines


# ═══════════════════════════════════════════════════════════════════════════
# Flowables
# ═══════════════════════════════════════════════════════════════════════════

class CodeBlock(Flowable):
    FS = 7.8; LH = 12; PAD = 8*mm
    MAX_LINES = 45  # max lines per block before splitting

    def __init__(self, code, lang="", T=None):
        super().__init__()
        self.code = code.rstrip("\n")
        self.lang = lang
        self.T = T or theme()
        self.tlines = tokenize(self.code, self.lang)

    def wrap(self, aw, ah):
        self._w = aw
        self.height = self.PAD + 6 + len(self.tlines)*self.LH + self.PAD
        return (self._w, self.height)

    def draw(self):
        c = self.canv; w = self._w; h = self.height; T = self.T
        c.setFillColor(T["code_bg"])
        c.roundRect(0, 0, w, h, 3.5*mm, fill=1, stroke=0)
        if self.lang:
            c.setFont("Plex", 6); c.setFillColor(T["tk_cmt"])
            lb = self.lang.upper()
            c.drawString(w - c.stringWidth(lb,"Plex",6) - 10, h - 13, lb)
        y = h - self.PAD - 4
        mx = int((w - self.PAD*2) / 4.2)
        for tl in self.tlines:
            x = self.PAD; cc = 0
            for txt, tt in tl:
                c.setFillColor(tok_color(tt, T))
                c.setFont("Plex", self.FS)
                rem = mx - cc
                if len(txt) > rem:
                    txt = txt[:rem-1] + "…"
                c.drawString(x, y, txt)
                x += c.stringWidth(txt, "Plex", self.FS)
                cc += len(txt)
                if cc >= mx: break
            y -= self.LH


def make_code_blocks(code, lang, T):
    """Split a code string into one or more CodeBlock flowables that fit on a page."""
    lines = code.rstrip("\n").split("\n")
    limit = CodeBlock.MAX_LINES
    if len(lines) <= limit:
        return [CodeBlock(code, lang, T)]
    blocks = []
    for i in range(0, len(lines), limit):
        chunk = "\n".join(lines[i:i+limit])
        # Only show language badge on the first chunk
        blocks.append(CodeBlock(chunk, lang if i == 0 else "", T))
    return blocks


class TipBox(Flowable):
    LABEL_H = 6*mm   # space for the label line
    PAD_TOP = 5*mm
    PAD_BOT = 5*mm
    PAD_LR  = 5*mm

    def __init__(self, text, kind="tip", T=None):
        super().__init__()
        self.text = text; self.kind = kind; self.T = T or theme()

    def wrap(self, aw, ah):
        self._w = aw; T = self.T
        self._style = ParagraphStyle("t", fontName="Inter", fontSize=8.5,
                                     leading=13, textColor=T["text"])
        self._p = Paragraph(self.text, self._style)
        text_w = aw - self.PAD_LR * 2
        _, ph = self._p.wrap(text_w, 10000)
        self._ph = ph
        self.height = self.PAD_TOP + self.LABEL_H + ph + self.PAD_BOT
        return (self._w, self.height)

    def draw(self):
        c = self.canv; w = self._w; h = self.height; T = self.T
        bg = T["tip_bg"] if self.kind == "tip" else T["warn_bg"]
        ac = T["accent"] if self.kind == "tip" else T["accent2"]

        # Background
        c.setFillColor(bg)
        c.roundRect(0, 0, w, h, 3*mm, fill=1, stroke=0)

        # Left accent bar
        c.setFillColor(ac)
        c.rect(0, 0, 3, h, fill=1, stroke=0)

        # Label at top
        label = "What happened?" if self.kind == "tip" else "Warning"
        c.setFont("Inter-B", 8.5)
        c.setFillColor(ac)
        label_y = h - self.PAD_TOP - 3*mm
        c.drawString(self.PAD_LR, label_y, label)

        # Body text below label
        text_y = h - self.PAD_TOP - self.LABEL_H - self._ph
        self._p.drawOn(c, self.PAD_LR, text_y)


class PartDivider(Flowable):
    def __init__(self, title, T=None):
        super().__init__()
        self.title = title; self.T = T or theme()
        self.height = 200*mm

    def wrap(self, aw, ah):
        self._w = aw; self.height = min(self.height, ah - 2)
        return (self._w, self.height)

    def draw(self):
        c = self.canv; w = self._w; h = self.height; T = self.T
        c.setFillColor(T["accent"])
        c.circle(w/2, h*0.55, 18*mm, fill=1, stroke=0)
        pl = self.title.split("—")[0].strip() if "—" in self.title else self.title
        c.setFillColor(T["badge_fg"]); c.setFont("Inter-B", 14)
        c.drawCentredString(w/2, h*0.55 - 4, pl)
        if "—" in self.title:
            sub = self.title.split("—",1)[1].strip()
            c.setFillColor(T["heading"]); c.setFont("Inter", 20)
            c.drawCentredString(w/2, h*0.55 - 40*mm, sub)
        c.setStrokeColor(T["border"]); c.setLineWidth(0.5)
        c.line(w/2-30*mm, h*0.55-52*mm, w/2+30*mm, h*0.55-52*mm)


class ChapterHeader(Flowable):
    def __init__(self, num, title, T=None):
        super().__init__()
        self.num = num; self.title = title; self.T = T or theme()
        self.height = 28*mm

    def wrap(self, aw, ah):
        self._w = aw; return (aw, self.height)

    def draw(self):
        c = self.canv; T = self.T
        c.setFillColor(T["accent"]); c.setFont("Inter", 11)
        c.drawString(0, self.height - 8*mm, self.num)
        c.setStrokeColor(T["accent"]); c.setLineWidth(2)
        c.line(0, self.height - 11*mm, 30*mm, self.height - 11*mm)
        c.setFillColor(T["heading"])
        fs = 22 if len(self.title) <= 40 else 18
        c.setFont("Inter-B", fs)
        c.drawString(0, self.height - 24*mm, self.title)


class CoverImage(Flowable):
    """Placeholder flowable that triggers a page — the actual image is drawn by the page template."""
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.height = 1  # minimal height, actual drawing is in onPage

    def wrap(self, aw, ah):
        return (aw, 1)

    def draw(self):
        pass  # drawn by _pg_cover_with_image instead


class AccentBar(Flowable):
    def __init__(self, color):
        super().__init__()
        self.color = color; self.height = 4
    def wrap(self, aw, ah): return (50*mm, 4)
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0,0,50*mm,3,fill=1,stroke=0)


# ═══════════════════════════════════════════════════════════════════════════
# Page decorations
# ═══════════════════════════════════════════════════════════════════════════

def _pg_normal(T):
    def fn(cv, doc):
        cv.saveState()
        if str(T["page_bg"]) != str(_hx("#FFFFFF")):
            cv.setFillColor(T["page_bg"]); cv.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
        cv.setStrokeColor(T["border"]); cv.setLineWidth(0.4)
        cv.line(ML, PAGE_H-MT+5*mm, PAGE_W-MR, PAGE_H-MT+5*mm)
        cv.setFont("Inter", 7); cv.setFillColor(T["text2"])
        cv.drawString(ML, PAGE_H-MT+7*mm, "Git By Example")
        cv.drawRightString(PAGE_W-MR, PAGE_H-MT+7*mm, "Dariush Abbasi")
        cv.line(ML, MB-5*mm, PAGE_W-MR, MB-5*mm)
        cv.setFont("Inter", 8); cv.setFillColor(T["text2"])
        cv.drawCentredString(PAGE_W/2, MB-10*mm, str(doc.page))
        cv.restoreState()
    return fn

def _pg_blank(T):
    def fn(cv, doc):
        cv.saveState()
        if str(T["page_bg"]) != str(_hx("#FFFFFF")):
            cv.setFillColor(T["page_bg"]); cv.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
        cv.restoreState()
    return fn

def _pg_cover(T, image_path=None):
    def fn(cv, doc):
        if image_path and os.path.exists(image_path):
            cv.drawImage(image_path, 0, 0, width=PAGE_W, height=PAGE_H,
                         preserveAspectRatio=False, mask="auto")
    return fn


# ═══════════════════════════════════════════════════════════════════════════
# Markdown → Flowables
# ═══════════════════════════════════════════════════════════════════════════

def _hex_s(c):
    """Convert a reportlab Color to a hex string."""
    try:
        r, g, b = int(c.red*255), int(c.green*255), int(c.blue*255)
        return "#%02x%02x%02x" % (r, g, b)
    except Exception:
        return str(c)

def ifmt(text, T):
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    fg = _hex_s(T["ic_fg"])
    text = re.sub(r'`([^`]+)`',
                  rf'<font face="Plex" size="8" color="{fg}">\1</font>', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'<u>\1</u>', text)
    return text

def _styles(T):
    return dict(
        body = ParagraphStyle("body", fontName="Inter", fontSize=9.5,
                              leading=15, textColor=T["text"], spaceAfter=6, spaceBefore=2),
        h2   = ParagraphStyle("h2", fontName="Inter-B", fontSize=14,
                              leading=20, textColor=T["heading"], spaceAfter=6, spaceBefore=14),
        h3   = ParagraphStyle("h3", fontName="Inter-B", fontSize=11,
                              leading=16, textColor=T["h3"], spaceAfter=4, spaceBefore=10),
        h4   = ParagraphStyle("h4", fontName="Inter-B", fontSize=10,
                              leading=14, textColor=T["heading"], spaceAfter=4, spaceBefore=8),
        bq   = ParagraphStyle("bq", fontName="Inter-I", fontSize=10,
                              leading=15, textColor=T["text2"], leftIndent=12*mm,
                              spaceAfter=8, spaceBefore=8),
        li   = ParagraphStyle("li", fontName="Inter", fontSize=9.5,
                              leading=14, textColor=T["text"], leftIndent=8*mm,
                              bulletIndent=3*mm, spaceAfter=3),
    )

def md2fl(md, S, T, chnum=None):
    fl = []; lines = md.split("\n"); i = 0; first_h1 = True
    while i < len(lines):
        ln = lines[i]; st = ln.strip()
        if st.startswith("[←") or st.startswith("[Next:"):
            i+=1; continue
        if st in ("---","***","___"):
            fl.append(Spacer(1,6*mm)); i+=1; continue
        if not st:
            i+=1; continue
        # Headings
        if st.startswith("#"):
            lv = len(st.split()[0]); title = st.lstrip("#").strip()
            if lv == 1 and first_h1:
                first_h1 = False
                nl = f"Chapter {chnum}" if chnum else ""
                dt = title.split("—",1)[-1].strip() if "—" in title else title
                fl.append(ChapterHeader(nl, dt, T)); fl.append(Spacer(1,4*mm))
                i+=1; continue
            sk = {2:"h2",3:"h3"}.get(lv,"h4")
            fl.append(Paragraph(ifmt(title,T), S[sk])); i+=1; continue
        # Code
        if st.startswith("```"):
            lang = st[3:].strip(); cl = []; i+=1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                cl.append(lines[i]); i+=1
            i+=1
            fl.append(Spacer(1,2*mm))
            for cb in make_code_blocks("\n".join(cl), lang, T):
                fl.append(cb)
            fl.append(Spacer(1,3*mm)); continue
        # Blockquote
        if st.startswith(">"):
            ql = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                ql.append(lines[i].strip().lstrip(">").strip()); i+=1
            fl.append(Spacer(1,2*mm))
            fl.append(Paragraph(ifmt(" ".join(ql),T), S["bq"]))
            fl.append(Spacer(1,2*mm)); continue
        # Tips
        if "🧠" in st:
            t = st.replace("🧠","").replace("**What happened?**","").strip()
            fl.append(TipBox(ifmt(t,T), "tip", T)); fl.append(Spacer(1,3*mm))
            i+=1; continue
        # Warnings
        if st.startswith("⚠️") or st.startswith("⚠"):
            t = st.replace("⚠️","").replace("⚠","").strip()
            t = t.replace("**Warning**:","").replace("**Warning:**","").strip()
            fl.append(TipBox(ifmt(t,T), "warning", T)); fl.append(Spacer(1,3*mm))
            i+=1; continue
        # Lists
        if st.startswith("- ") or st.startswith("* "):
            fl.append(Paragraph("• "+ifmt(st[2:],T), S["li"])); i+=1; continue
        m = re.match(r'^(\d+)\.\s+(.*)', st)
        if m:
            fl.append(Paragraph(f"{m.group(1)}. "+ifmt(m.group(2),T), S["li"]))
            i+=1; continue
        # Tables
        if "|" in st and st.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                r = lines[i].strip()
                if re.match(r'^\|[\s\-:|]+\|$', r): i+=1; continue
                rows.append([c.strip() for c in r.split("|")[1:-1]]); i+=1
            if rows:
                nc = max(len(r) for r in rows)
                for r in rows:
                    while len(r)<nc: r.append("")
                cs = ParagraphStyle("c",fontName="Inter",fontSize=8,leading=11,textColor=T["text"])
                ch = ParagraphStyle("ch",fontName="Inter-B",fontSize=8,leading=11,textColor=T["text"])
                data = [[Paragraph(ifmt(c,T), ch if ri==0 else cs) for c in row]
                        for ri,row in enumerate(rows)]
                cw = CW/nc
                tb = Table(data, colWidths=[cw]*nc)
                tb.setStyle(TableStyle([
                    ("BACKGROUND",(0,0),(-1,0),T["tbl_hdr"]),
                    ("GRID",(0,0),(-1,-1),0.4,T["tbl_brd"]),
                    ("VALIGN",(0,0),(-1,-1),"TOP"),
                    ("LEFTPADDING",(0,0),(-1,-1),4*mm),
                    ("RIGHTPADDING",(0,0),(-1,-1),4*mm),
                    ("TOPPADDING",(0,0),(-1,-1),2*mm),
                    ("BOTTOMPADDING",(0,0),(-1,-1),2*mm),
                ]))
                fl.append(Spacer(1,2*mm)); fl.append(tb); fl.append(Spacer(1,3*mm))
            continue
        # Paragraph
        pl = []
        while i < len(lines):
            l = lines[i].strip()
            if (not l or l.startswith("#") or l.startswith("```")
                or l.startswith(">") or l.startswith("- ") or l.startswith("* ")
                or l.startswith("|") or "🧠" in l or l.startswith("⚠")
                or l in ("---","***","___") or re.match(r'^\d+\.\s+',l)
                or l.startswith("[←") or l.startswith("[Next:")): break
            pl.append(l); i+=1
        if pl:
            fl.append(Paragraph(ifmt(" ".join(pl),T), S["body"]))
    return fl


# ═══════════════════════════════════════════════════════════════════════════
# TOC
# ═══════════════════════════════════════════════════════════════════════════

def build_toc(T):
    fl = [Spacer(1,10*mm)]
    fl.append(Paragraph("Table of Contents",
        ParagraphStyle("tt",fontName="Inter-B",fontSize=20,leading=26,
                       textColor=T["heading"],spaceAfter=8*mm)))
    ps = ParagraphStyle("tp",fontName="Inter-B",fontSize=10,leading=16,
                        textColor=T["accent"],spaceBefore=6*mm,spaceAfter=2*mm)
    cs = ParagraphStyle("tc",fontName="Inter",fontSize=9.5,leading=16,
                        textColor=T["text"],leftIndent=5*mm)
    cn = 0
    for fp, part in CHAPTERS:
        if part: fl.append(Paragraph(part, ps))
        fn = os.path.basename(fp)
        if fn[0].isdigit():
            cn += 1
            t = fn.replace(".md","").split("-",1)[1].replace("-"," ").title()
            fl.append(Paragraph(f"{cn}. &nbsp; {t}", cs))
        else:
            t = fn.replace(".md","").replace("-"," ").title()
            fl.append(Paragraph(f"&nbsp;&nbsp;&nbsp; {t}", cs))
    fl.append(PageBreak())
    return fl


# ═══════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════

def build_pdf(output, dark=False):
    setup_fonts()
    T = theme(dark)
    mode = "dark" if dark else "light"
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cover = os.path.join(root, "cover.png")

    doc = BaseDocTemplate(output, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title="Git By Example", author="Dariush Abbasi",
        subject="A practical guide to Git")

    fr = Frame(ML, MB, CW, PAGE_H-MT-MB, id="main")
    fr_cover = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover",  frames=fr_cover, onPage=_pg_cover(T, cover if os.path.exists(cover) else None)),
        PageTemplate(id="blank",  frames=fr,       onPage=_pg_blank(T)),
        PageTemplate(id="normal", frames=fr,       onPage=_pg_normal(T)),
    ])

    S = _styles(T); story = []

    # Cover page — just the image, nothing else
    if os.path.exists(cover):
        story.append(NextPageTemplate("cover"))
        story.append(CoverImage(cover))
        story.append(NextPageTemplate("normal"))
        story.append(PageBreak())
    else:
        # No cover image — use a text title page instead
        print(f"  ⚠  cover.png not found, using text title page")
        story.append(NextPageTemplate("blank"))
        story.append(Spacer(1,50*mm))
        story.append(Paragraph("Git By Example",
            ParagraphStyle("t",fontName="Inter-B",fontSize=32,leading=38,textColor=T["heading"])))
        story.append(Spacer(1,5*mm))
        story.append(AccentBar(T["accent"]))
        story.append(Spacer(1,8*mm))
        story.append(Paragraph("A practical guide to Git — learn by doing,<br/>not by reading manuals.",
            ParagraphStyle("s",fontName="Inter",fontSize=12,leading=18,textColor=T["text2"])))
        story.append(Spacer(1,35*mm))
        story.append(Paragraph("Dariush Abbasi",
            ParagraphStyle("a",fontName="Inter-B",fontSize=12,leading=16,textColor=T["text"])))
        story.append(Spacer(1,3*mm))
        story.append(Paragraph(datetime.datetime.now().strftime("%B %Y"),
            ParagraphStyle("d",fontName="Inter",fontSize=9,leading=13,textColor=T["text2"])))
        story.append(Spacer(1,5*mm))
        story.append(Paragraph("github.com/boringcollege/git-by-example",
            ParagraphStyle("u",fontName="Plex",fontSize=8,leading=12,textColor=T["accent"])))
        story.append(Spacer(1,4*mm))
        story.append(Paragraph(f"{mode.capitalize()} Edition",
            ParagraphStyle("m",fontName="Inter",fontSize=8,leading=12,textColor=T["text2"])))
        story.append(NextPageTemplate("normal"))
        story.append(PageBreak())

    # TOC
    story.append(NextPageTemplate("normal"))
    story.extend(build_toc(T))

    # Chapters
    cn = 0
    for fp, pn in CHAPTERS:
        full = os.path.join(root, fp)
        if not os.path.exists(full):
            print(f"  ⚠  {fp} not found"); continue
        if pn:
            story.append(NextPageTemplate("blank"))
            story.append(PageBreak())
            story.append(PartDivider(pn, T))
            story.append(NextPageTemplate("normal"))
            story.append(PageBreak())
        fn = os.path.basename(fp)
        is_ch = fn[0].isdigit()
        if is_ch: cn += 1
        with open(full, "r", encoding="utf-8") as f:
            md = f.read()
        try:
            chapter_fl = md2fl(md, S, T, chnum=cn if is_ch else None)
            story.extend(chapter_fl)
            print(f"  ✓ {fp} ({len(chapter_fl)} flowables)")
        except Exception as e:
            print(f"  ✗ {fp} FAILED: {e}")
        story.append(PageBreak())

    print(f"  Building {output} ({mode}), {len(story)} total flowables ...")
    try:
        doc.build(story)
    except Exception as e:
        print(f"  ✗ doc.build FAILED: {e}")
        raise
    print(f"  ✅  {output}  ({os.path.getsize(output)/1024:.0f} KB)")


if __name__ == "__main__":
    args = sys.argv[1:]
    both = "--both" in args
    dk = "--dark" in args
    name = next((a for a in args if not a.startswith("--")), "gitbyexample")

    if both:
        b = name.replace(".pdf","")
        build_pdf(f"{b}-light.pdf", dark=False)
        build_pdf(f"{b}-dark.pdf",  dark=True)
    elif dk:
        out = name if name.endswith(".pdf") else f"{name}.pdf"
        build_pdf(out, dark=True)
    else:
        out = name if name.endswith(".pdf") else f"{name}.pdf"
        build_pdf(out, dark=False)