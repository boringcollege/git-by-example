#!/usr/bin/env python3
"""
Convert Inter OTF fonts (CFF outlines) to TTF (TrueType outlines).

ReportLab cannot read CFF-based OpenType fonts directly. This script
converts the CFF cubic curves to TrueType quadratic curves and fixes
the sfntVersion and maxp table so ReportLab accepts them.

Run once before build_pdf.py — idempotent (skips if already converted).
"""

import os
import sys

def convert_inter_fonts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, "fonts")
    os.makedirs(out_dir, exist_ok=True)

    # Check if already converted
    target = os.path.join(out_dir, "Inter-Regular.ttf")
    if os.path.exists(target) and os.path.getsize(target) > 10000:
        # Quick check: is it actually TrueType?
        with open(target, "rb") as f:
            sig = f.read(4)
        if sig == b'\x00\x01\x00\x00':
            print("Inter TTF fonts already present, skipping conversion.")
            return

    # Find Inter OTF source
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
        # Try installing
        print("Inter fonts not found. Install with: sudo apt install fonts-inter")
        sys.exit(1)

    from fontTools.ttLib import TTFont
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
    from fontTools.ttLib.tables._l_o_c_a import table__l_o_c_a

    variants = [
        "Inter-Regular.otf",
        "Inter-Bold.otf",
        "Inter-Italic.otf",
        "Inter-BoldItalic.otf",
    ]

    for name in variants:
        src = os.path.join(src_dir, name)
        out_name = name.replace(".otf", ".ttf")
        dst = os.path.join(out_dir, out_name)

        if not os.path.exists(src):
            print(f"  ⚠  {src} not found, skipping")
            continue

        print(f"  Converting {name} → {out_name} ...", end=" ", flush=True)

        font = TTFont(src)

        if "CFF " not in font:
            print("(no CFF table, copying as-is)")
            font.save(dst)
            continue

        gs = font.getGlyphSet()
        glyph_order = font.getGlyphOrder()

        # Convert CFF cubic curves → TrueType quadratic curves
        glyphs = {}
        for gname in glyph_order:
            ttpen = TTGlyphPen(None)
            cu2qupen = Cu2QuPen(ttpen, max_err=1.0, reverse_direction=True)
            gs[gname].draw(cu2qupen)
            glyphs[gname] = ttpen.glyph()

        # Replace CFF with glyf + loca
        glyf_table = table__g_l_y_f()
        glyf_table.glyphs = glyphs
        glyf_table.glyphOrder = glyph_order
        font["glyf"] = glyf_table
        font["loca"] = table__l_o_c_a()
        font["head"].glyphDataFormat = 0

        # Remove CFF-specific tables
        for tag in ["CFF ", "VORG"]:
            if tag in font:
                del font[tag]

        # Fix maxp for TrueType (version 1.0 = 0x00010000)
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

        # Set TrueType sfntVersion
        font.sfntVersion = "\x00\x01\x00\x00"

        font.save(dst)
        size_kb = os.path.getsize(dst) / 1024
        print(f"OK ({size_kb:.0f} KB)")

    print("  Done.")


if __name__ == "__main__":
    convert_inter_fonts()