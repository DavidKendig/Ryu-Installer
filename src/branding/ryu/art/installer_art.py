#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 David Kendig
# SPDX-License-Identifier: GPL-3.0-or-later
"""Pictures for the Ryū OS installer (Calamares branding), drawn on the same generated
aurora as the boot menu so the installer looks like the GRUB screen that started it.

    installer_art.py RYUGLASS OUT_DIR VERSION

RYUGLASS is the built compositor (it renders the aurora with --render-wallpaper).
Writes welcome.png, slide1.png .. slide3.png and arrow-down.png into OUT_DIR.
"""
import glob
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def font(weight, size):
    """Inter (the desktop's typeface) at a weight, else DejaVu Sans."""
    names = {700: ["Inter-Bold", "InterDisplay-Bold"], 600: ["Inter-SemiBold", "Inter-Bold"],
             400: ["Inter-Regular", "Inter"]}[weight]
    for n in names:
        for pat in (f"/usr/share/fonts/**/{n}.ttf", f"/usr/share/fonts/**/{n}.otf"):
            hits = glob.glob(pat, recursive=True)
            if hits:
                return ImageFont.truetype(hits[0], size)
    for var in glob.glob("/usr/share/fonts/**/Inter*Variable*.ttf", recursive=True):
        f = ImageFont.truetype(var, size)
        try:
            f.set_variation_by_name({700: "Bold", 600: "SemiBold", 400: "Regular"}[weight])
        except Exception:
            pass
        return f
    dv = "DejaVuSans-Bold.ttf" if weight >= 600 else "DejaVuSans.ttf"
    hits = glob.glob(f"/usr/share/fonts/**/{dv}", recursive=True)
    return ImageFont.truetype(hits[0], size) if hits else ImageFont.load_default()


def aurora(ryuglass, w, h):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "a.png")
        subprocess.run([ryuglass, "--render-wallpaper", p, f"{w}x{h}"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return Image.open(p).convert("RGBA")


def shadow_text(img, xy, text, f, fill=(255, 255, 255, 255), anchor="la"):
    """Text with a soft shadow, as on the lock screen."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((xy[0], xy[1] + 2), text, font=f, fill=(0, 0, 0, 150), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    img.alpha_composite(layer)
    ImageDraw.Draw(img).text(xy, text, font=f, fill=fill, anchor=anchor)


def dim(img, alpha):
    img.alpha_composite(Image.new("RGBA", img.size, (6, 8, 30, alpha)))


def welcome(ryuglass, out, version):
    w, h = 880, 360
    img = aurora(ryuglass, w, h)
    dim(img, 40)
    shadow_text(img, (w // 2, h // 2 - 20), "Ryū OS", font(700, 78), anchor="mm")
    shadow_text(img, (w // 2, h // 2 + 42), f"Version {version}", font(400, 22),
                fill=(225, 230, 255, 235), anchor="mm")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=255)
    img.putalpha(mask)
    img.save(os.path.join(out, "welcome.png"))


SLIDES = [
    ("Welcome to Ryū OS",
     ["A light, fast desktop with frosted glass", "The full system is being copied to your disk",
      "This takes a few minutes"]),
    ("Everything for making things",
     ["Verso for code, notes, Markdown and git", "C++, Rust, Python, Java and Haxe, ready to use",
      "The Craft Apps for art, film, sound and more"]),
    ("Get more software",
     ["Ryū Software installs apps in one click", "Flatpak, AppImage and Windows apps (Wine)",
      "Brave for the web, RustDesk for remote help"]),
]


def slides(ryuglass, out):
    w, h = 800, 440
    base = aurora(ryuglass, w, h)
    for i, (title, lines) in enumerate(SLIDES, 1):
        img = base.copy()
        dim(img, 70)
        shadow_text(img, (56, 96), title, font(700, 40))
        y = 176
        for line in lines:
            d = ImageDraw.Draw(img)
            d.ellipse((60, y + 9, 72, y + 21), fill=(142, 200, 240, 255))
            shadow_text(img, (92, y), line, font(400, 24), fill=(232, 236, 255, 240))
            y += 54
        img.convert("RGB").save(os.path.join(out, f"slide{i}.png"))


def arrow(out):
    s = 4  # draw large, scale down for smooth edges
    img = Image.new("RGBA", (12 * s, 8 * s), (0, 0, 0, 0))
    ImageDraw.Draw(img).line([(2 * s, 2 * s), (6 * s, 6 * s), (10 * s, 2 * s)],
                             fill=(220, 226, 255, 255), width=2 * s, joint="curve")
    img.resize((12, 8), Image.LANCZOS).save(os.path.join(out, "arrow-down.png"))


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    ryuglass, out, version = sys.argv[1:]
    os.makedirs(out, exist_ok=True)
    welcome(ryuglass, out, version)
    slides(ryuglass, out)
    arrow(out)


if __name__ == "__main__":
    main()
