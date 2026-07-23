from __future__ import annotations

import json
import math
from pathlib import Path

import cv2
import numpy as np


BATCH_DIR = Path(__file__).resolve().parent
LANE_DIR = BATCH_DIR.parents[3]
FRAMES_DIR = BATCH_DIR / "qc" / "frames"
OUTPUT_DIR = BATCH_DIR / "qc" / "lettering-compare-pages"
APPROVED_END = (
    LANE_DIR
    / "working"
    / "batches"
    / "hero-still"
    / "v05-approved-product-lock"
    / "outputs"
    / "take-01.jpg"
)

FIRST_READABLE_FRAME = 112
LAST_FRAME = 192

# Fixed crops contain the full plaque across the stable readable hold.
SOURCE_CROP = (35, 630, 735, 825)  # x1, y1, x2, y2
VIDEO_CROP = (20, 820, 1060, 1225)


def crop(image: np.ndarray, bounds: tuple[int, int, int, int]) -> np.ndarray:
    x1, y1, x2, y2 = bounds
    return image[y1:y2, x1:x2]


def fit(image: np.ndarray, width: int, height: int) -> np.ndarray:
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(
        image,
        (
            max(1, round(image.shape[1] * scale)),
            max(1, round(image.shape[0] * scale)),
        ),
        interpolation=cv2.INTER_AREA,
    )
    canvas = np.full((height, width, 3), 248, dtype=np.uint8)
    x = (width - resized.shape[1]) // 2
    y = (height - resized.shape[0]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def label(image: np.ndarray, text: str) -> np.ndarray:
    band = np.full((40, image.shape[1], 3), 255, dtype=np.uint8)
    cv2.putText(
        band,
        text,
        (10, 27),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (20, 20, 20),
        1,
        cv2.LINE_AA,
    )
    return np.concatenate([band, image], axis=0)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source = cv2.imread(str(APPROVED_END), cv2.IMREAD_COLOR)
    if source is None:
        raise RuntimeError(f"Could not open approved endpoint: {APPROVED_END}")
    source_face = crop(source, SOURCE_CROP)
    cv2.imwrite(
        str(OUTPUT_DIR / "approved-source-face.jpg"),
        source_face,
        [cv2.IMWRITE_JPEG_QUALITY, 98],
    )

    indices = list(range(FIRST_READABLE_FRAME, LAST_FRAME + 1))
    per_page = 9
    pages = math.ceil(len(indices) / per_page)
    source_header = label(
        fit(source_face, 1800, 430),
        "APPROVED SOURCE — MR & MRS JANNAWAY / WHEN TWO NAMES BECOME ONE 15TH AUGUST 2026",
    )

    for page_index in range(pages):
        page = np.full((470 + 3 * 285, 1800, 3), 255, dtype=np.uint8)
        page[:470] = source_header
        page_indices = indices[page_index * per_page : (page_index + 1) * per_page]
        for offset, frame_index in enumerate(page_indices):
            frame_path = FRAMES_DIR / f"frame-{frame_index:03d}.jpg"
            frame = cv2.imread(str(frame_path), cv2.IMREAD_COLOR)
            if frame is None:
                raise RuntimeError(f"Could not open frame: {frame_path}")
            face = crop(frame, VIDEO_CROP)
            cell = label(
                fit(face, 600, 245),
                f"NATIVE f{frame_index:03d} — {frame_index / 24:0.3f}s",
            )
            row, col = divmod(offset, 3)
            y, x = 470 + row * 285, col * 600
            page[y : y + 285, x : x + 600] = cell
        cv2.imwrite(
            str(OUTPUT_DIR / f"lettering-compare-{page_index + 1:02d}.jpg"),
            page,
            [cv2.IMWRITE_JPEG_QUALITY, 97],
        )

    manifest = {
        "approved_source": str(APPROVED_END.relative_to(LANE_DIR)).replace("\\", "/"),
        "source_crop": SOURCE_CROP,
        "video_crop": VIDEO_CROP,
        "first_readable_frame": FIRST_READABLE_FRAME,
        "last_frame": LAST_FRAME,
        "compared_frame_count": len(indices),
        "fps": 24,
        "readable_hold_seconds": (LAST_FRAME - FIRST_READABLE_FRAME + 1) / 24,
        "page_count": pages,
        "every_readable_hold_frame_included": True,
        "product_surface_modified": False,
    }
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
