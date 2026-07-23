from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import cv2
import numpy as np


BATCH_DIR = Path(__file__).resolve().parent
LANE_DIR = BATCH_DIR.parents[3]
VIDEO = BATCH_DIR / "seedance-raw.mp4"
QC_DIR = BATCH_DIR / "qc"
FRAMES_DIR = QC_DIR / "frames"
SHEETS_DIR = QC_DIR / "all-frame-sheets"

APPROVED_START = (
    LANE_DIR
    / "working"
    / "batches"
    / "start-keyframe"
    / "v01-white-back-match"
    / "outputs"
    / "take-01.png"
)
APPROVED_END = (
    LANE_DIR
    / "working"
    / "batches"
    / "hero-still"
    / "v05-approved-product-lock"
    / "outputs"
    / "take-01.jpg"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    canvas = np.full((height, width, 3), 242, dtype=np.uint8)
    x = (width - resized.shape[1]) // 2
    y = (height - resized.shape[0]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def labelled_cell(image: np.ndarray, label: str, width: int, height: int) -> np.ndarray:
    band = 34
    cell = np.full((height, width, 3), 255, dtype=np.uint8)
    cell[band:] = fit(image, width, height - band)
    cv2.putText(
        cell,
        label,
        (8, 23),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (20, 20, 20),
        1,
        cv2.LINE_AA,
    )
    return cell


def main() -> None:
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    SHEETS_DIR.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(VIDEO))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video: {VIDEO}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    declared_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_paths: list[Path] = []
    frame_diffs: list[float] = []
    dense_thumbs: list[np.ndarray] = []
    previous_small: np.ndarray | None = None
    first_frame: np.ndarray | None = None
    last_frame: np.ndarray | None = None

    index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if first_frame is None:
            first_frame = frame.copy()
        last_frame = frame.copy()

        frame_path = FRAMES_DIR / f"frame-{index:03d}.jpg"
        cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        frame_paths.append(frame_path)

        small = cv2.resize(frame, (108, 192), interpolation=cv2.INTER_AREA)
        dense_thumbs.append(small)
        if previous_small is not None:
            frame_diffs.append(float(cv2.absdiff(small, previous_small).mean()))
        previous_small = small
        index += 1

    capture.release()
    if first_frame is None or last_frame is None:
        raise RuntimeError("No frames decoded")
    if declared_frames and index != declared_frames:
        raise RuntimeError(f"Decoded {index} frames but container reports {declared_frames}")

    # One compact overview contains every decoded frame in order.
    dense_cols = 16
    dense_rows = math.ceil(index / dense_cols)
    dense = np.full((dense_rows * 216, dense_cols * 120, 3), 255, dtype=np.uint8)
    for i, thumb in enumerate(dense_thumbs):
        row, col = divmod(i, dense_cols)
        x, y = col * 120, row * 216
        dense[y : y + 192, x + 6 : x + 114] = thumb
        cv2.putText(
            dense,
            f"{i:03d}",
            (x + 7, y + 208),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.38,
            (20, 20, 20),
            1,
            cv2.LINE_AA,
        )
    cv2.imwrite(
        str(QC_DIR / "all-frames-dense-overview.jpg"),
        dense,
        [cv2.IMWRITE_JPEG_QUALITY, 94],
    )

    # Higher-detail sheets, 24 consecutive frames each.
    per_sheet = 24
    cell_width, cell_height = 270, 514
    sheet_cols, sheet_rows = 4, 6
    for sheet_index, start in enumerate(range(0, index, per_sheet), start=1):
        sheet = np.full(
            (sheet_rows * cell_height, sheet_cols * cell_width, 3),
            255,
            dtype=np.uint8,
        )
        for offset, frame_index in enumerate(
            range(start, min(start + per_sheet, index))
        ):
            frame = cv2.imread(str(frame_paths[frame_index]), cv2.IMREAD_COLOR)
            row, col = divmod(offset, sheet_cols)
            label = f"f{frame_index:03d}  {frame_index / fps:0.3f}s"
            cell = labelled_cell(frame, label, cell_width, cell_height)
            y, x = row * cell_height, col * cell_width
            sheet[y : y + cell_height, x : x + cell_width] = cell
        cv2.imwrite(
            str(SHEETS_DIR / f"sheet-{sheet_index:02d}.jpg"),
            sheet,
            [cv2.IMWRITE_JPEG_QUALITY, 95],
        )

    approved_start = cv2.imread(str(APPROVED_START), cv2.IMREAD_COLOR)
    approved_end = cv2.imread(str(APPROVED_END), cv2.IMREAD_COLOR)
    if approved_start is None or approved_end is None:
        raise RuntimeError("Could not open one or both approved endpoints")

    compare_width, compare_height = 384, 722
    comparisons = [
        labelled_cell(
            approved_start, "APPROVED START — plain white reverse", compare_width, compare_height
        ),
        labelled_cell(
            first_frame, "NATIVE VIDEO — first frame", compare_width, compare_height
        ),
        labelled_cell(
            approved_end, "APPROVED END — exact Jannaway", compare_width, compare_height
        ),
        labelled_cell(
            last_frame, "NATIVE VIDEO — final frame", compare_width, compare_height
        ),
    ]
    endpoint_sheet = np.concatenate(comparisons, axis=1)
    cv2.imwrite(
        str(QC_DIR / "endpoint-comparison.jpg"),
        endpoint_sheet,
        [cv2.IMWRITE_JPEG_QUALITY, 97],
    )

    resized_start = cv2.resize(
        approved_start, (width, height), interpolation=cv2.INTER_AREA
    )
    resized_end = cv2.resize(approved_end, (width, height), interpolation=cv2.INTER_AREA)
    first_mae = float(cv2.absdiff(first_frame, resized_start).mean())
    last_mae = float(cv2.absdiff(last_frame, resized_end).mean())
    first_psnr = float(cv2.PSNR(first_frame, resized_start))
    last_psnr = float(cv2.PSNR(last_frame, resized_end))

    top_diffs = sorted(
        (
            {"between_frames": [i, i + 1], "mean_absdiff": value}
            for i, value in enumerate(frame_diffs)
        ),
        key=lambda item: item["mean_absdiff"],
        reverse=True,
    )[:12]

    metadata = {
        "video": str(VIDEO.relative_to(LANE_DIR)).replace("\\", "/"),
        "bytes": VIDEO.stat().st_size,
        "sha256": sha256(VIDEO),
        "width": width,
        "height": height,
        "fps": fps,
        "frames": index,
        "duration_seconds": index / fps,
        "frame_files": len(frame_paths),
        "all_frames_in_dense_overview": True,
        "all_frames_in_numbered_sheets": True,
        "numbered_sheet_count": math.ceil(index / per_sheet),
        "endpoint_metrics": {
            "approved_start_to_video_first_mae": first_mae,
            "approved_start_to_video_first_psnr": first_psnr,
            "approved_end_to_video_last_mae": last_mae,
            "approved_end_to_video_last_psnr": last_psnr,
            "note": "Compression and model synthesis make pixel identity impossible; these metrics support, but do not replace, visual QC.",
        },
        "largest_frame_to_frame_differences": top_diffs,
        "agent_visual_qc": "pending",
        "product_surface_compositing": False,
    }
    (QC_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
