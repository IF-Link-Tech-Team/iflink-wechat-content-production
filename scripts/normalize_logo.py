#!/usr/bin/env python3
"""Create a trimmed, transparent, near-black raster Logo for light layouts."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageColor, ImageOps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize a raster Logo to transparent near-black PNG."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--mode",
        required=True,
        choices=("preserve-alpha", "dark-on-light", "light-on-dark"),
    )
    parser.add_argument(
        "--low",
        type=int,
        default=20,
        help="Luminance mapped to one end of alpha range (0-255).",
    )
    parser.add_argument(
        "--high",
        type=int,
        default=240,
        help="Luminance mapped to the other end of alpha range (0-255).",
    )
    parser.add_argument("--padding", type=int, default=12)
    parser.add_argument("--black", default="#080808")
    return parser.parse_args()


def luminance_alpha(gray: Image.Image, mode: str, low: int, high: int) -> Image.Image:
    if not 0 <= low < high <= 255:
        raise ValueError("Require 0 <= --low < --high <= 255")

    if mode == "light-on-dark":
        lut = [
            0 if value <= low else 255 if value >= high else round((value - low) * 255 / (high - low))
            for value in range(256)
        ]
    else:
        lut = [
            255 if value <= low else 0 if value >= high else round((high - value) * 255 / (high - low))
            for value in range(256)
        ]
    return gray.point(lut)


def main() -> None:
    args = parse_args()
    if args.input.suffix.lower() == ".svg":
        raise ValueError("Keep SVG vector; correct its viewBox or use an HTML clip container")
    if not args.input.is_file():
        raise FileNotFoundError(args.input)
    if args.padding < 0:
        raise ValueError("--padding must be non-negative")

    with Image.open(args.input) as source:
        source = ImageOps.exif_transpose(source).convert("RGBA")
        original_alpha = source.getchannel("A")

        if args.mode == "preserve-alpha":
            if original_alpha.getextrema() == (255, 255):
                raise ValueError(
                    "Input has no transparency; use dark-on-light or light-on-dark"
                )
            alpha = original_alpha
        else:
            gray = ImageOps.grayscale(source.convert("RGB"))
            alpha = luminance_alpha(gray, args.mode, args.low, args.high)
            if original_alpha.getextrema() != (255, 255):
                alpha = ImageChops.multiply(alpha, original_alpha)

    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError("No foreground detected; adjust --mode, --low, or --high")

    rgb = Image.new("RGB", alpha.size, ImageColor.getrgb(args.black))
    result = Image.merge("RGBA", (*rgb.split(), alpha)).crop(bbox)
    if args.padding:
        result = ImageOps.expand(result, border=args.padding, fill=(0, 0, 0, 0))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output, format="PNG", optimize=True)
    print(f"output={args.output} size={result.width}x{result.height}")


if __name__ == "__main__":
    main()
