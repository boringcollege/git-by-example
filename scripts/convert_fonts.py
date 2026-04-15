#!/usr/bin/env python3
"""
Prepare fonts for the PDF build.

1. Convert Inter OTF (CFF outlines) → TTF (TrueType outlines)
   because ReportLab cannot read CFF-based OpenType fonts.

2. Copy IBM Plex Mono TTF files into scripts/fonts/ so the project
   is self-contained and works both locally and in CI.

Run once before build_pdf.py — idempotent (skips if already done).

System font packages needed (CI installs these):
  sudo apt install fonts-inter fonts-ibm-plex
"""

import os
import sys
import shutil


def ensure_inter(out_dir):
    """Convert Inter OTF → TTF if not already present."""
    target = os.path.join(out_dir, "Inter-Regular.ttf")
    if os.path.exists(target) and os.path.getsize(target) > 10000:
        with open(target, "rb") as f:
            sig = f.read(4)
        if sig == b'\x00\x01\x00\x00':
            print("  Inter TTF fonts already present, skipping conversion.")
            return True

    # Find Inter OTF source (installed via fonts-inter)
    search_dirs = [
        "/usr/share/fonts/opentype/inter",
        "/usr/share/fonts/OTF",
        "/usr/share/fonts/opentype",
    ]
    src_dir = None
    for d in search_dirs:
        if os.path.exists(os.path.join(d, "Inter-Regular.otf")):
            src_dir = d
            break

    if src_dir is None:
        print("  ✗ Inter OTF fonts not found.")
        print("    Install with: sudo apt install fonts-inter")
        print("    Or download from: https://rsms.me/inter/")
        return False

    from fontTools.ttLib import TTFont
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
    from fontTools.ttLib.tables._l_o_c_a import table__l_o_c_a

    for name in ["Inter-Regular.otf", "Inter-Bold.otf",
                 "Inter-Italic.otf", "Inter-BoldItalic.otf"]:
        src = os.path.join(src_dir, name)
        out_name = name.replace(".otf", ".ttf")
        dst = os.path.join(out_dir, out_name)

        if not os.path.exists(src):
            print(f"  ⚠  {src} not found, skipping")
            continue

        print(f"  Converting {name} → {out_name} ...", end=" ", flush=True)

        font = TTFont(src)
        if "CFF " not in font:
            font.save(dst)
            print("(no CFF, copied)")
            continue

        gs = font.getGlyphSet()
        glyph_order = font.getGlyphOrder()

        glyphs = {}
        for gname in glyph_order:
            ttpen = TTGlyphPen(None)
            cu2qupen = Cu2QuPen(ttpen, max_err=1.0, reverse_direction=True)
            gs[gname].draw(cu2qupen)
            glyphs[gname] = ttpen.glyph()

        glyf_table = table__g_l_y_f()
        glyf_table.glyphs = glyphs
        glyf_table.glyphOrder = glyph_order
        font["glyf"] = glyf_table
        font["loca"] = table__l_o_c_a()
        font["head"].glyphDataFormat = 0

        for tag in ["CFF ", "VORG"]:
            if tag in font:
                del font[tag]

        maxp = font["maxp"]
        maxp.tableVersion = 0x00010000
        for attr, default in [
            ("maxZones", 2), ("maxTwilightPoints", 0), ("maxStorage", 0),
            ("maxFunctionDefs", 0), ("maxInstructionDefs", 0),
            ("maxStackElements", 0), ("maxSizeOfInstructions", 0),
            ("maxPoints", 0), ("maxContours", 0),
            ("maxCompositePoints", 0), ("maxCompositeContours", 0),
            ("maxComponentElements", 0), ("maxComponentDepth", 0),
        ]:
            if not hasattr(maxp, attr):
                setattr(maxp, attr, default)
        maxp.recalc(font)

        font.sfntVersion = "\x00\x01\x00\x00"
        font.save(dst)
        print(f"OK ({os.path.getsize(dst)/1024:.0f} KB)")

    return True


def ensure_plex_mono(out_dir):
    """Copy IBM Plex Mono TTFs into fonts dir if not already there."""
    needed = [
        "IBMPlexMono-Regular.ttf",
        "IBMPlexMono-Bold.ttf",
        "IBMPlexMono-Italic.ttf",
        "IBMPlexMono-BoldItalic.ttf",
    ]

    # Check if already present
    if all(os.path.exists(os.path.join(out_dir, n)) for n in needed):
        print("  IBM Plex Mono fonts already present, skipping.")
        return True

    # Find system install (installed via fonts-ibm-plex)
    search_dirs = [
        "/usr/share/fonts/truetype/ibm-plex",
        "/usr/share/fonts/TTF",
        "/usr/share/fonts/truetype",
    ]
    src_dir = None
    for d in search_dirs:
        if os.path.exists(os.path.join(d, "IBMPlexMono-Regular.ttf")):
            src_dir = d
            break

    if src_dir is None:
        print("  ✗ IBM Plex Mono fonts not found.")
        print("    Install with: sudo apt install fonts-ibm-plex")
        print("    Or download from: https://github.com/IBM/plex/releases")
        return False

    for name in needed:
        src = os.path.join(src_dir, name)
        dst = os.path.join(out_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  Copied {name}")
        else:
            print(f"  ⚠  {name} not found in {src_dir}")

    return True


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, "fonts")
    os.makedirs(out_dir, exist_ok=True)

    print("Preparing fonts...")
    ok1 = ensure_inter(out_dir)
    ok2 = ensure_plex_mono(out_dir)

    if ok1 and ok2:
        print("All fonts ready ✅")
    else:
        print("Some fonts missing — PDF build may fail.")
        sys.exit(1)