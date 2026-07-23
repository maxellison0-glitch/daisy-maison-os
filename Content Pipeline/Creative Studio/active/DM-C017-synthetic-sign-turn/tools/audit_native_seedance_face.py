#!/usr/bin/env python3
"""Create a frame-by-frame audit of Seedance's untouched sign face.

This diagnostic deliberately does not composite or alter the raw video. It
uses the saved physical-panel track only to rectify each native Seedance frame
next to the canonical LightBurn-derived source.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def order_quad(points: np.ndarray) -> np.ndarray:
    sums = points.sum(axis=1)
    differences = np.diff(points, axis=1).reshape(-1)
    return np.array(
        [
            points[np.argmin(sums)],
            points[np.argmin(differences)],
            points[np.argmax(sums)],
            points[np.argmax(differences)],
        ],
        dtype=np.float32,
    )


def rectify(
    frame: np.ndarray, quad: np.ndarray, output_size: tuple[int, int]
) -> np.ndarray:
    width, height = output_size
    destination = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(order_quad(quad), destination)
    return cv2.warpPerspective(
        frame,
        transform,
        (width, height),
        flags=cv2.INTER_LANCZOS4,
    )


def ink_iou(source: np.ndarray, observed: np.ndarray) -> float:
    source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    observed_gray = cv2.cvtColor(observed, cv2.COLOR_BGR2GRAY)
    observed_gray = cv2.normalize(observed_gray, None, 0, 255, cv2.NORM_MINMAX)
    source_ink = source_gray < 165
    observed_ink = observed_gray < 112
    margin_x = max(8, source.shape[1] // 100)
    margin_y = max(5, source.shape[0] // 24)
    mask = np.zeros(source_ink.shape, dtype=bool)
    mask[margin_y:-margin_y, margin_x:-margin_x] = True
    source_ink &= mask
    observed_ink &= mask
    intersection = np.logical_and(source_ink, observed_ink).sum()
    union = np.logical_or(source_ink, observed_ink).sum()
    return float(intersection / union) if union else 1.0


def label_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/segoeuib.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def make_pages(
    source: np.ndarray,
    observations: list[tuple[int, np.ndarray, float]],
    output_dir: Path,
    fps: float,
) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cell_width = source.shape[1] // 2
    cell_height = source.shape[0] // 2
    label_height = 38
    header_height = cell_height + 58
    rows_per_page = 8
    columns = 2
    per_page = rows_per_page * columns
    page_width = cell_width * columns
    page_height = header_height + rows_per_page * (cell_height + label_height)
    font = label_font(24)
    title_font = label_font(28)

    source_rgb = cv2.cvtColor(
        cv2.resize(source, (cell_width, cell_height), interpolation=cv2.INTER_AREA),
        cv2.COLOR_BGR2RGB,
    )
    pages: list[str] = []
    for page_index, start in enumerate(range(0, len(observations), per_page), 1):
        canvas = Image.new("RGB", (page_width, page_height), (18, 18, 18))
        draw = ImageDraw.Draw(canvas)
        draw.text(
            (18, 10),
            "EXACT LIGHTBURN-DERIVED SOURCE",
            font=title_font,
            fill=(255, 255, 255),
        )
        canvas.paste(Image.fromarray(source_rgb), (0, 54))
        for local_index, (frame_index, observed, score) in enumerate(
            observations[start : start + per_page]
        ):
            column = local_index % columns
            row = local_index // columns
            x = column * cell_width
            y = header_height + row * (cell_height + label_height)
            observed_rgb = cv2.cvtColor(
                cv2.resize(
                    observed,
                    (cell_width, cell_height),
                    interpolation=cv2.INTER_AREA,
                ),
                cv2.COLOR_BGR2RGB,
            )
            canvas.paste(Image.fromarray(observed_rgb), (x, y))
            draw.text(
                (x + 10, y + cell_height + 5),
                (
                    f"RAW F{frame_index:03d}  {frame_index / fps:0.3f}s"
                    f"  threshold IoU {score:0.4f}"
                ),
                font=font,
                fill=(255, 255, 255),
            )
        output = output_dir / f"native-face-page-{page_index:02d}.jpg"
        canvas.save(output, quality=94, subsampling=0)
        pages.append(str(output))
    return pages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--track", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    track_payload = json.loads(args.track.read_text(encoding="utf-8"))
    panel_x, panel_y, panel_width, panel_height = track_payload["source_face"][
        "panel_bbox"
    ]
    source_rgba = cv2.imread(str(args.source), cv2.IMREAD_UNCHANGED)
    if source_rgba is None:
        raise RuntimeError(f"Could not read {args.source}")
    source = source_rgba[
        panel_y : panel_y + panel_height,
        panel_x : panel_x + panel_width,
        :3,
    ]
    quads = {
        int(item["frame"]): np.array(item["smoothed_quad"], dtype=np.float32)
        for item in track_payload["frames"]
    }

    capture = cv2.VideoCapture(str(args.raw))
    if not capture.isOpened():
        raise RuntimeError(f"Could not decode {args.raw}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    observations: list[tuple[int, np.ndarray, float]] = []
    frame_index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if frame_index in quads:
            observed = rectify(
                frame,
                quads[frame_index],
                (panel_width, panel_height),
            )
            observations.append(
                (frame_index, observed, ink_iou(source, observed))
            )
        frame_index += 1
    capture.release()

    pages = make_pages(source, observations, args.output_dir, fps)
    metrics = {
        "raw": str(args.raw),
        "track": str(args.track),
        "source": str(args.source),
        "fps": fps,
        "first_frame": observations[0][0],
        "last_frame": observations[-1][0],
        "frame_count": len(observations),
        "threshold_metric_warning": (
            "Threshold IoU is diagnostic only. It is affected by raw lighting, "
            "motion blur, foreshortening and track error and cannot approve "
            "letter identity without visual review."
        ),
        "ink_iou_min": min(item[2] for item in observations),
        "ink_iou_mean": float(np.mean([item[2] for item in observations])),
        "pages": pages,
    }
    report_path = args.output_dir / "native-face-audit.json"
    report_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
