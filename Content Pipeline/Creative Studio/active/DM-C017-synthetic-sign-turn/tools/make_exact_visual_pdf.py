#!/usr/bin/env python3
"""Embed an exact lossless sign-face PNG on a physical-size PDF page.

This creates the visual-source PDF used by the Reel workflow. It deliberately
does not claim to be a LightBurn/RIP-ready production file.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_png", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument("--width-mm", type=float, required=True)
    parser.add_argument("--height-mm", type=float, required=True)
    args = parser.parse_args()

    with Image.open(args.input_png) as image:
        if image.format != "PNG":
            raise ValueError(f"Expected PNG input, received {image.format!r}")
        pixel_width, pixel_height = image.size
        expected_aspect = args.width_mm / args.height_mm
        pixel_aspect = pixel_width / pixel_height
        if abs(pixel_aspect - expected_aspect) > 1e-9:
            raise ValueError(
                "PNG and requested page proportions differ: "
                f"{pixel_width}x{pixel_height} vs "
                f"{args.width_mm}x{args.height_mm} mm"
            )

    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    page_size = (args.width_mm * mm, args.height_mm * mm)
    document = canvas.Canvas(
        str(args.output_pdf),
        pagesize=page_size,
        pageCompression=1,
        invariant=1,
    )
    document.setTitle(f"{args.input_png.stem} exact visual sign face")
    document.setSubject(
        "Lossless exact visual source for deterministic Reel compositing; "
        "not a laser/RIP production file."
    )
    document.drawImage(
        str(args.input_png),
        0,
        0,
        width=page_size[0],
        height=page_size[1],
        preserveAspectRatio=False,
        mask=None,
    )
    document.showPage()
    document.save()


if __name__ == "__main__":
    main()
