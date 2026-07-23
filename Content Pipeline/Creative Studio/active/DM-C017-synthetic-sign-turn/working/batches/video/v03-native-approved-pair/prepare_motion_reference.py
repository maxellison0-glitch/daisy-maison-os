from __future__ import annotations

import json
from pathlib import Path

import cv2


BATCH_DIR = Path(__file__).resolve().parent
LANE_DIR = BATCH_DIR.parents[3]
SOURCE = (
    LANE_DIR
    / "source"
    / "real-product-reference-pack"
    / "instagram-DPjdseCDbDR"
    / "daisymaison-reel-DPjdseCDbDR-video.mp4"
)
OUTPUT_DIR = BATCH_DIR / "inputs"
OUTPUT = OUTPUT_DIR / "real-turn-face-excluded.mp4"
META = OUTPUT_DIR / "real-turn-face-excluded.json"

# The original reference is 1080 × 1920. This fixed crop retains the sign,
# hands and torso while removing the source performer's face and all identity
# detail. It is construction/motion evidence only.
CROP_TOP = 760
CROP_BOTTOM = 1500
START_FRAME = 60
END_FRAME_EXCLUSIVE = 181


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(SOURCE))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open source video: {SOURCE}")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if width != 1080 or height != 1920:
        raise RuntimeError(
            f"Unexpected source size {width}x{height}; review the privacy crop."
        )
    if not (0 <= CROP_TOP < CROP_BOTTOM <= height):
        raise RuntimeError("Invalid crop bounds")

    out_height = CROP_BOTTOM - CROP_TOP
    writer = cv2.VideoWriter(
        str(OUTPUT),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, out_height),
    )
    if not writer.isOpened():
        raise RuntimeError(f"Could not create output video: {OUTPUT}")

    output_frame_count = END_FRAME_EXCLUSIVE - START_FRAME
    preview_indices = {
        0: "preview-start.jpg",
        output_frame_count // 2: "preview-mid.jpg",
        output_frame_count - 1: "preview-end.jpg",
    }
    capture.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME)
    written = 0
    while written < output_frame_count:
        ok, frame = capture.read()
        if not ok:
            break
        crop = frame[CROP_TOP:CROP_BOTTOM, 0:width]
        writer.write(crop)
        if written in preview_indices:
            cv2.imwrite(str(OUTPUT_DIR / preview_indices[written]), crop)
        written += 1

    capture.release()
    writer.release()
    if written != output_frame_count:
        raise RuntimeError(f"Decoded {written} of {output_frame_count} frames")

    metadata = {
        "role": "motion_and_product_construction_only",
        "source": str(SOURCE.relative_to(LANE_DIR)).replace("\\", "/"),
        "source_width": width,
        "source_height": height,
        "source_fps": fps,
        "source_frames": frame_count,
        "crop": {
            "x": 0,
            "y": CROP_TOP,
            "width": width,
            "height": out_height,
        },
        "source_frame_range": {
            "start_inclusive": START_FRAME,
            "end_exclusive": END_FRAME_EXCLUSIVE,
            "purpose": "white-back through the real thin edge; excludes the readable source front",
        },
        "output": str(OUTPUT.relative_to(LANE_DIR)).replace("\\", "/"),
        "output_frames": written,
        "face_and_identity_excluded": True,
        "must_not_supply_identity": True,
    }
    META.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
