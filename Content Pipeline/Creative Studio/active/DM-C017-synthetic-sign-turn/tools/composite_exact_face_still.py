#!/usr/bin/env python3
"""RETIRED failure-evidence tool for the invalid exact-face still composite."""

from __future__ import annotations

raise RuntimeError(
    "RETIRED: never create a video reference by compositing the SVG, panel, "
    "border or lettering onto a generated still."
)

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def order_quad(points: np.ndarray) -> np.ndarray:
    """Return TL, TR, BR, BL for four 2D points."""
    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1).reshape(-1)
    return np.array(
        [
            points[np.argmin(sums)],
            points[np.argmin(diffs)],
            points[np.argmax(sums)],
            points[np.argmax(diffs)],
        ],
        dtype=np.float32,
    )


def largest_sign_face(
    target: np.ndarray, roi_top: float, roi_bottom: float
) -> tuple[np.ndarray, np.ndarray]:
    """Detect the long, low-saturation inset face in a vertical still."""
    height = target.shape[0]
    y0 = int(round(height * roi_top))
    y1 = int(round(height * roi_bottom))
    roi = target[y0:y1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = ((hsv[:, :, 2] > 170) & (hsv[:, :, 1] < 70)).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    candidates: list[tuple[int, int]] = []
    for index in range(1, count):
        x, y, width, component_height, area = stats[index]
        aspect = width / max(component_height, 1)
        if aspect > 3.0 and area > 5_000:
            candidates.append((int(area), index))
    if not candidates:
        raise RuntimeError(
            "No long white sign face detected. Adjust --roi-top/--roi-bottom."
        )
    component_index = max(candidates)[1]
    component = (labels == component_index).astype(np.uint8) * 255
    contours, _ = cv2.findContours(
        component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contour = max(contours, key=cv2.contourArea)
    box = cv2.boxPoints(cv2.minAreaRect(contour))
    box[:, 1] += y0
    return order_quad(box), component


def source_panel(
    source: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[int, int, int, int]]:
    """Return the canonical inset panel quad, filled panel mask and bbox."""
    if source.ndim != 3 or source.shape[2] != 4:
        raise RuntimeError("The exact face must be an RGBA PNG.")
    rgb = source[:, :, :3]
    alpha = source[:, :, 3]
    white = (
        (alpha > 200)
        & (rgb[:, :, 0] > 245)
        & (rgb[:, :, 1] > 245)
        & (rgb[:, :, 2] > 245)
    ).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(white, 8)
    if count < 2:
        raise RuntimeError("No opaque white inset panel found in exact face.")
    index = max(
        range(1, count), key=lambda item: stats[item, cv2.CC_STAT_AREA]
    )
    x, y, width, height, _ = [int(value) for value in stats[index]]
    component = (labels == index).astype(np.uint8) * 255
    contours, _ = cv2.findContours(
        component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    panel_mask = np.zeros(alpha.shape, dtype=np.uint8)
    cv2.drawContours(
        panel_mask, [max(contours, key=cv2.contourArea)], -1, 255, -1
    )
    quad = np.array(
        [
            [x, y],
            [x + width - 1, y],
            [x + width - 1, y + height - 1],
            [x, y + height - 1],
        ],
        dtype=np.float32,
    )
    return quad, panel_mask, (x, y, width, height)


def illumination_map(
    target: np.ndarray, target_quad: np.ndarray
) -> np.ndarray:
    """Remove generated ink and retain the photographed surface lighting."""
    panel = np.zeros(target.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(panel, target_quad.astype(np.int32), 255)
    gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    ink = ((gray < 175) & (panel > 0)).astype(np.uint8) * 255
    ink = cv2.dilate(ink, np.ones((7, 7), np.uint8), iterations=1)
    clean = cv2.inpaint(target, ink, 9, cv2.INPAINT_TELEA)
    return cv2.GaussianBlur(clean, (0, 0), 9).astype(np.float32)


def end_grip_occlusion(
    target: np.ndarray, target_quad: np.ndarray
) -> np.ndarray:
    """Protect skin/fingers where they cross the two extreme sign ends."""
    height, width = target.shape[:2]
    ycc = cv2.cvtColor(target, cv2.COLOR_BGR2YCrCb)
    luminance, red_chroma, blue_chroma = cv2.split(ycc)
    skin = (
        (luminance > 45)
        & (red_chroma >= 132)
        & (red_chroma <= 180)
        & (blue_chroma >= 72)
        & (blue_chroma <= 138)
    ).astype(np.uint8) * 255
    min_x, min_y = target_quad.min(axis=0)
    max_x, max_y = target_quad.max(axis=0)
    end_zone = np.zeros((height, width), dtype=np.uint8)
    left_x = int(min_x + (max_x - min_x) * 0.085)
    right_x = int(max_x - (max_x - min_x) * 0.085)
    cv2.rectangle(
        end_zone,
        (max(0, int(min_x) - 40), max(0, int(min_y) - 35)),
        (min(width - 1, left_x), min(height - 1, int(max_y) + 50)),
        255,
        -1,
    )
    cv2.rectangle(
        end_zone,
        (max(0, right_x), max(0, int(min_y) - 35)),
        (
            min(width - 1, int(max_x) + 40),
            min(height - 1, int(max_y) + 50),
        ),
        255,
        -1,
    )
    occlusion = cv2.bitwise_and(skin, end_zone)
    occlusion = cv2.morphologyEx(
        occlusion, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=1
    )
    return cv2.dilate(
        occlusion, np.ones((3, 3), np.uint8), iterations=1
    )


def composite(
    target_path: Path,
    face_path: Path,
    output_path: Path,
    manifest_path: Path,
    mode: str,
    roi_top: float,
    roi_bottom: float,
    debug_path: Path | None,
) -> None:
    target = cv2.imread(str(target_path), cv2.IMREAD_COLOR)
    source = cv2.imread(str(face_path), cv2.IMREAD_UNCHANGED)
    if target is None:
        raise RuntimeError(f"Could not read target: {target_path}")
    if source is None:
        raise RuntimeError(f"Could not read exact face: {face_path}")

    target_quad, _ = largest_sign_face(target, roi_top, roi_bottom)
    source_quad, source_panel_mask, source_bbox = source_panel(source)
    transform = cv2.getPerspectiveTransform(source_quad, target_quad)
    height, width = target.shape[:2]

    warped_rgb = cv2.warpPerspective(
        source[:, :, :3],
        transform,
        (width, height),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    if mode == "panel":
        alpha_source = source_panel_mask
    else:
        alpha_source = source[:, :, 3]
    warped_alpha = cv2.warpPerspective(
        alpha_source,
        transform,
        (width, height),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )

    white_map = illumination_map(target, target_quad)
    source_float = warped_rgb.astype(np.float32) / 255.0
    black_floor = np.full_like(white_map, 8.0, dtype=np.float32)
    mapped = black_floor + source_float * (white_map - black_floor)
    alpha = cv2.GaussianBlur(
        warped_alpha.astype(np.float32) / 255.0, (0, 0), 0.45
    )
    if mode == "full":
        alpha[end_grip_occlusion(target, target_quad) > 0] = 0.0

    output = (
        mapped * alpha[:, :, None]
        + target.astype(np.float32) * (1.0 - alpha[:, :, None])
    ).clip(0, 255).astype(np.uint8)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), output):
        raise RuntimeError(f"Could not write output: {output_path}")

    if debug_path is not None:
        debug = output.copy()
        for point in target_quad.astype(np.int32):
            cv2.circle(debug, tuple(point), 5, (0, 255, 255), -1)
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(debug_path), debug)

    record = {
        "method": "detected planar homography with photographed illumination",
        "mode": mode,
        "target": {
            "path": str(target_path.resolve()),
            "sha256": sha256(target_path),
            "width": width,
            "height": height,
            "detected_panel_quad_tl_tr_br_bl": target_quad.tolist(),
        },
        "source_face": {
            "path": str(face_path.resolve()),
            "sha256": sha256(face_path),
            "width": int(source.shape[1]),
            "height": int(source.shape[0]),
            "detected_panel_bbox": list(source_bbox),
        },
        "homography": transform.tolist(),
        "output": {
            "path": str(output_path.resolve()),
            "sha256": sha256(output_path),
        },
        "settings": {
            "roi_top": roi_top,
            "roi_bottom": roi_bottom,
            "generated_lettering_used": False,
            "source_artwork_is_only_visible_face_source": True,
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    raise RuntimeError(
        "RETIRED: never create a video reference by compositing the SVG onto "
        "a generated sign. Generate one coherent physical sign image from the "
        "SVG plus real product references and obtain human approval."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--source-face", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--mode", choices=("panel", "full"), default="panel")
    parser.add_argument("--roi-top", type=float, default=0.43)
    parser.add_argument("--roi-bottom", type=float, default=0.64)
    parser.add_argument("--debug", type=Path)
    args = parser.parse_args()
    composite(
        target_path=args.target,
        face_path=args.source_face,
        output_path=args.output,
        manifest_path=args.manifest,
        mode=args.mode,
        roi_top=args.roi_top,
        roi_bottom=args.roi_bottom,
        debug_path=args.debug,
    )


if __name__ == "__main__":
    main()
