#!/usr/bin/env python3
"""Append equal-width page images and optionally build a mobile contact sheet."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageColor


Image.MAX_IMAGE_PIXELS = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compose ordered WeChat page images into one long PNG."
    )
    parser.add_argument("--pages", nargs="+", required=True, type=Path)
    parser.add_argument("--banner", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--thumb-width", type=int, default=216)
    parser.add_argument("--contact-width", type=int, default=1200)
    parser.add_argument("--contact-height", type=int, default=469)
    parser.add_argument("--background", default="#ded8d0")
    return parser.parse_args()


def open_rgb(path: Path, background: tuple[int, int, int]) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as source:
        source.load()
        if source.mode in {"RGBA", "LA"} or "transparency" in source.info:
            rgba = source.convert("RGBA")
            canvas = Image.new("RGBA", rgba.size, (*background, 255))
            canvas.alpha_composite(rgba)
            return canvas.convert("RGB")
        return source.convert("RGB")


def save_long_image(
    page_paths: list[Path], banner_path: Path | None, output: Path
) -> tuple[int, int]:
    white = (255, 255, 255)
    images = [open_rgb(path, white) for path in page_paths]
    if banner_path:
        images.append(open_rgb(banner_path, white))

    width = images[0].width
    mismatches = [
        f"{path}: {image.width}px"
        for path, image in zip(
            page_paths + ([banner_path] if banner_path else []), images
        )
        if image.width != width
    ]
    if mismatches:
        raise ValueError(
            f"All inputs must share width {width}px; mismatches: "
            + ", ".join(mismatches)
        )

    total_height = sum(image.height for image in images)
    result = Image.new("RGB", (width, total_height), white)
    y = 0
    for image in images:
        result.paste(image, (0, y))
        y += image.height

    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output, format="PNG", optimize=True)
    return result.size


def save_contact_sheet(
    page_paths: list[Path],
    output: Path,
    thumb_width: int,
    canvas_width: int,
    canvas_height: int,
    background: str,
) -> tuple[int, int]:
    color = ImageColor.getrgb(background)
    thumbs: list[Image.Image] = []
    for path in page_paths:
        image = open_rgb(path, color)
        height = round(image.height * thumb_width / image.width)
        thumbs.append(image.resize((thumb_width, height), Image.Resampling.LANCZOS))

    row_width = sum(image.width for image in thumbs)
    row_height = max(image.height for image in thumbs)
    final_width = max(canvas_width, row_width)
    final_height = max(canvas_height, row_height)
    sheet = Image.new("RGB", (final_width, final_height), color)
    x = (final_width - row_width) // 2
    for image in thumbs:
        y = (final_height - image.height) // 2
        sheet.paste(image, (x, y))
        x += image.width

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG", optimize=True)
    return sheet.size


def main() -> None:
    args = parse_args()
    if args.thumb_width <= 0:
        raise ValueError("--thumb-width must be positive")

    long_size = save_long_image(args.pages, args.banner, args.output)
    print(f"long_image={args.output} size={long_size[0]}x{long_size[1]}")

    if args.contact_sheet:
        sheet_size = save_contact_sheet(
            args.pages,
            args.contact_sheet,
            args.thumb_width,
            args.contact_width,
            args.contact_height,
            args.background,
        )
        print(
            f"contact_sheet={args.contact_sheet} "
            f"size={sheet_size[0]}x{sheet_size[1]}"
        )


if __name__ == "__main__":
    main()
