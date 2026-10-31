#!/usr/bin/env python3
"""Check that every CJK character the scenes render is actually preloaded.

Fonts are loaded from npm and gated behind `delayRender`, with an explicit
character list passed to `document.fonts.load`. A character rendered but left
out of that list can come back as tofu in the render, and nothing fails loudly
when it does — so this runs before rendering.

    python3 check_glyphs.py src                       # report
    python3 check_glyphs.py src --write src/fonts.ts  # update the list in place

With --font-dir it also verifies the characters exist in the font itself,
which is what catches using a Japanese face for Traditional Chinese: DotGothic16
has no 每 內 腳 踢 擊 錄, because Japanese writes those 毎 内 脚 撃 録.
Needs `fonttools` and `brotli`; skipped silently if either is missing.

    python3 check_glyphs.py src \
        --font-dir node_modules/@fontsource/unifont/files
"""

import argparse
import glob
import os
import re
import sys

CJK = re.compile(r"[぀-ヿ㐀-鿿！-｠]")
# the preload list lives in a `const <NAME> =` string literal
DECL = re.compile(r"(const\s+\w*GLYPHS\w*\s*=\s*\n?\s*\")([^\"]*)(\")")


def used_in(src_dir, skip):
    found = set()
    for path in sorted(glob.glob(os.path.join(src_dir, "**", "*.ts*"), recursive=True)):
        if os.path.basename(path) in skip:
            continue
        with open(path, encoding="utf-8") as fh:
            found |= set(CJK.findall(fh.read()))
    return found


def declared_in(fonts_file):
    with open(fonts_file, encoding="utf-8") as fh:
        text = fh.read()
    m = DECL.search(text)
    if not m:
        return None, text
    return set(m.group(2)), text


def font_coverage(font_dir):
    """Union of the cmaps of every font file in the directory.

    .woff and .ttf are read directly; .woff2 needs the brotli extension, which
    often is not installed, so those are only a fallback.
    """
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None, "fontTools is not installed"
    plain = glob.glob(os.path.join(font_dir, "*.woff")) + \
        glob.glob(os.path.join(font_dir, "*.ttf")) + \
        glob.glob(os.path.join(font_dir, "*.otf"))
    files = plain or glob.glob(os.path.join(font_dir, "*.woff2"))
    if not files:
        return None, f"no font files in {font_dir}"
    cov, failed = set(), 0
    for f in files:
        try:
            cov |= set(TTFont(f).getBestCmap())
        except Exception:
            failed += 1
    if not cov:
        return None, (f"could not decode any of {len(files)} file(s); "
                      "woff2 needs the brotli extension")
    return cov, f"{len(files) - failed}/{len(files)} file(s) read"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?", default="src")
    ap.add_argument("--fonts-file", default=None,
                    help="defaults to <src>/fonts.ts")
    ap.add_argument("--font-dir", default=None,
                    help="an @fontsource files/ directory to check coverage against")
    ap.add_argument("--write", nargs="?", const=True, default=False,
                    help="rewrite the preload list to exactly what is used")
    args = ap.parse_args()

    fonts_file = args.fonts_file or os.path.join(args.src, "fonts.ts")
    if not os.path.exists(fonts_file):
        sys.exit(f"no font loader at {fonts_file}")

    used = used_in(args.src, skip={os.path.basename(fonts_file)})
    declared, text = declared_in(fonts_file)
    if declared is None:
        sys.exit(f"no `const ...GLYPHS = \"...\"` declaration found in {fonts_file}")

    missing = sorted(used - declared)
    unused = sorted(declared - used)

    print(f"rendered in {args.src}: {len(used)} CJK characters")
    print(f"preloaded in {os.path.basename(fonts_file)}: {len(declared)}")
    print()
    print("missing from the preload list: " + ("".join(missing) if missing else "none"))
    if unused:
        print(f"preloaded but unused ({len(unused)}): {''.join(unused)}")
        print("  (harmless — extra characters only cost a slightly larger subset)")

    status = 1 if missing else 0
    font_problem = False

    if args.font_dir:
        cov, note = font_coverage(args.font_dir)
        if cov is None:
            print(f"\nfont coverage: skipped — {note}")
        else:
            absent = sorted(c for c in used if ord(c) not in cov)
            print(f"\nfont coverage ({os.path.basename(args.font_dir)}): "
                  f"{len(cov)} glyphs, {note}")
            if absent:
                print("NOT IN THE FONT: " + "".join(absent))
                print("  This face cannot render those. A Japanese font cannot do "
                      "Traditional Chinese — use a face that covers them.")
                status = 1
                font_problem = True
            else:
                print("every rendered character exists in the font")

    if args.write and missing:
        target = fonts_file if args.write is True else args.write
        new_list = "".join(sorted(used))
        with open(fonts_file, encoding="utf-8") as fh:
            original = fh.read()
        updated = DECL.sub(lambda m: m.group(1) + new_list + m.group(3), original, count=1)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(updated)
        print(f"\nrewrote the preload list in {target} ({len(new_list)} characters)")
        status = 0

    print()
    if status == 0:
        print("Preload list is complete and the font covers it.")
    elif font_problem and not missing:
        print("The preload list is complete, but the FONT cannot render every "
              "character — switch to a face that covers them.")
    else:
        print("Preload list is incomplete — fix before rendering.")
    return status


if __name__ == "__main__":
    sys.exit(main())
