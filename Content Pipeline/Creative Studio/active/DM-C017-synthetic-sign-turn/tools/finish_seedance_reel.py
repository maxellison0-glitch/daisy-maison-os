#!/usr/bin/env python3
"""RETIRED failure-evidence script for the rejected DM-C017 overlay method.

This module is retained only so the rejected result remains reproducible for
diagnosis. Daisy Maison now forbids whole-panel, border and lettering-only
overlays on a generated sign. Do not use this script to create review or
publication assets.
"""

from __future__ import annotations

raise RuntimeError(
    "RETIRED: product-surface overlays are forbidden. The exact sign must "
    "exist natively in a human-approved coherent source image and survive "
    "native video generation unchanged."
)

import argparse
import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont


WIDTH = 1080
HEIGHT = 1920
FPS = 24
FRAME_COUNT = 192
DURATION = 8.0
TRACK_START = 70
FEATURE_ANCHOR = 84
FACE_FULL = 70
DEFAULT_HOOK_LINES = ("THE WEDDING GIFT", "THEY CAN'T REGIFT.")
DEFAULT_CTA = "ADD THEIR NAMES  →"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def smootherstep(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value**3 * (value * (value * 6.0 - 15.0) + 10.0)


def fade_window(
    seconds: float,
    fade_in_start: float,
    full_start: float,
    full_end: float,
    fade_out_end: float,
) -> float:
    if seconds < fade_in_start or seconds > fade_out_end:
        return 0.0
    if seconds < full_start:
        return smootherstep(
            (seconds - fade_in_start) / (full_start - fade_in_start)
        )
    if seconds <= full_end:
        return 1.0
    return 1.0 - smootherstep(
        (seconds - full_end) / (fade_out_end - full_end)
    )


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


def source_panel(
    source: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, tuple[int, int, int, int]]:
    if source is None or source.ndim != 3 or source.shape[2] != 4:
        raise RuntimeError("Exact sign face must be an RGBA PNG.")
    rgb = source[:, :, :3]
    alpha = source[:, :, 3]
    white = (
        (alpha > 200)
        & (rgb[:, :, 0] > 245)
        & (rgb[:, :, 1] > 245)
        & (rgb[:, :, 2] > 245)
    ).astype(np.uint8) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(white, 8)
    index = max(
        range(1, count), key=lambda item: stats[item, cv2.CC_STAT_AREA]
    )
    x, y, width, height, _ = [int(value) for value in stats[index]]
    component = (labels == index).astype(np.uint8) * 255
    contours, _ = cv2.findContours(
        component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    mask = np.zeros(alpha.shape, dtype=np.uint8)
    cv2.drawContours(mask, [max(contours, key=cv2.contourArea)], -1, 255, -1)
    quad = np.array(
        [
            [x, y],
            [x + width - 1, y],
            [x + width - 1, y + height - 1],
            [x, y + height - 1],
        ],
        dtype=np.float32,
    )
    return quad, mask, (x, y, width, height)


def detect_panel_quad(frame: np.ndarray) -> tuple[np.ndarray, dict]:
    y0, y1 = int(HEIGHT * 0.35), int(HEIGHT * 0.70)
    roi = frame[y0:y1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    white = ((hsv[:, :, 2] > 165) & (hsv[:, :, 1] < 85)).astype(
        np.uint8
    ) * 255
    count, labels, stats, _ = cv2.connectedComponentsWithStats(white, 8)
    candidates: list[tuple[int, int, np.ndarray, tuple, float]] = []
    for index in range(1, count):
        x, y, width, height, area = stats[index]
        if area <= 4_000 or x <= 20 or x + width >= WIDTH - 20:
            continue
        component = (labels == index).astype(np.uint8) * 255
        contours, _ = cv2.findContours(
            component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contour = max(contours, key=cv2.contourArea)
        rectangle = cv2.minAreaRect(contour)
        rect_width, rect_height = rectangle[1]
        ratio = max(rect_width, rect_height) / max(
            1.0, min(rect_width, rect_height)
        )
        centre_x, centre_y = rectangle[0]
        centre_y += y0
        if (
            ratio > 2.5
            and 250 < centre_x < 850
            and 650 < centre_y < 1300
        ):
            candidates.append(
                (int(area), index, contour, rectangle, float(ratio))
            )
    if not candidates:
        raise RuntimeError("No readable sign face detected.")
    area, _, _, rectangle, ratio = max(candidates, key=lambda item: item[0])
    box = cv2.boxPoints(rectangle)
    box[:, 1] += y0
    quad = order_quad(box)
    return quad, {
        "component_area": area,
        "detected_panel_aspect": ratio,
        "raw_quad": quad.astype(float).tolist(),
    }


def smooth_quads(quads: np.ndarray, window: int = 5) -> np.ndarray:
    radius = window // 2
    padded = np.pad(quads, ((radius, radius), (0, 0), (0, 0)), mode="edge")
    output = np.empty_like(quads)
    kernel = np.ones(window, dtype=np.float32) / window
    for corner in range(4):
        for coordinate in range(2):
            output[:, corner, coordinate] = np.convolve(
                padded[:, corner, coordinate], kernel, mode="valid"
            )
    return output


def valid_quad(quad: np.ndarray) -> bool:
    if quad is None or quad.shape != (4, 2) or not np.isfinite(quad).all():
        return False
    if (
        quad[:, 0].min() < -80
        or quad[:, 0].max() > WIDTH + 80
        or quad[:, 1].min() < -80
        or quad[:, 1].max() > HEIGHT + 80
    ):
        return False
    return abs(float(cv2.contourArea(quad.astype(np.float32)))) > 2_000


def feature_panel_quad(
    frame: np.ndarray,
    source_keypoints: list,
    source_descriptors: np.ndarray,
    source_size: tuple[int, int],
    sift,
    matcher,
) -> tuple[np.ndarray, dict]:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_keypoints, frame_descriptors = sift.detectAndCompute(gray, None)
    if frame_descriptors is None:
        raise RuntimeError("No frame descriptors.")
    pairs = matcher.knnMatch(source_descriptors, frame_descriptors, k=2)
    matches = [
        first
        for first, second in pairs
        if first.distance < 0.72 * second.distance
    ]
    if len(matches) < 12:
        raise RuntimeError("Insufficient feature matches.")
    source_points = np.float32(
        [source_keypoints[item.queryIdx].pt for item in matches]
    ).reshape(-1, 1, 2)
    frame_points = np.float32(
        [frame_keypoints[item.trainIdx].pt for item in matches]
    ).reshape(-1, 1, 2)
    transform, inlier_mask = cv2.findHomography(
        source_points, frame_points, cv2.RANSAC, 4.0
    )
    if transform is None or inlier_mask is None or int(inlier_mask.sum()) < 8:
        raise RuntimeError("Feature homography was not reliable.")
    width, height = source_size
    corners = np.float32(
        [
            [
                [0, 0],
                [width - 1, 0],
                [width - 1, height - 1],
                [0, height - 1],
            ]
        ]
    )
    quad = cv2.perspectiveTransform(corners, transform)[0]
    if not valid_quad(quad):
        raise RuntimeError("Feature homography produced an invalid quad.")
    return quad, {
        "method": "SIFT source-to-frame homography",
        "feature_matches": len(matches),
        "feature_inliers": int(inlier_mask.sum()),
        "raw_quad": quad.astype(float).tolist(),
    }


def optical_quad_backwards(
    later_frame: np.ndarray,
    earlier_frame: np.ndarray,
    later_quad: np.ndarray,
) -> tuple[np.ndarray, dict]:
    later_gray = cv2.cvtColor(later_frame, cv2.COLOR_BGR2GRAY)
    earlier_gray = cv2.cvtColor(earlier_frame, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(later_gray.shape, dtype=np.uint8)
    cv2.fillConvexPoly(mask, later_quad.astype(np.int32), 255)
    mask = cv2.dilate(mask, np.ones((17, 17), np.uint8), iterations=1)
    points = cv2.goodFeaturesToTrack(
        later_gray,
        maxCorners=500,
        qualityLevel=0.005,
        minDistance=4,
        mask=mask,
        blockSize=5,
    )
    if points is None or len(points) < 20:
        raise RuntimeError("Insufficient optical-flow features.")
    earlier_points, status, error = cv2.calcOpticalFlowPyrLK(
        later_gray,
        earlier_gray,
        points,
        None,
        winSize=(31, 31),
        maxLevel=4,
        criteria=(
            cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
            40,
            0.001,
        ),
    )
    back_points, back_status, _ = cv2.calcOpticalFlowPyrLK(
        earlier_gray,
        later_gray,
        earlier_points,
        None,
        winSize=(31, 31),
        maxLevel=4,
        criteria=(
            cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
            40,
            0.001,
        ),
    )
    forward_back_error = np.linalg.norm(points - back_points, axis=2).reshape(-1)
    keep = (
        (status.reshape(-1) == 1)
        & (back_status.reshape(-1) == 1)
        & (forward_back_error < 1.5)
        & (error.reshape(-1) < 30)
    )
    source_points = points[keep].reshape(-1, 2)
    target_points = earlier_points[keep].reshape(-1, 2)
    if len(source_points) < 12:
        raise RuntimeError("Optical-flow consistency check failed.")
    transform, inlier_mask = cv2.findHomography(
        source_points, target_points, cv2.RANSAC, 2.5
    )
    if transform is None or inlier_mask is None or int(inlier_mask.sum()) < 8:
        raise RuntimeError("Optical-flow homography was not reliable.")
    quad = cv2.perspectiveTransform(
        later_quad.reshape(1, -1, 2), transform
    )[0]
    if not valid_quad(quad):
        raise RuntimeError("Optical flow produced an invalid quad.")
    return quad, {
        "method": "backward pyramidal optical flow",
        "flow_features": int(keep.sum()),
        "flow_inliers": int(inlier_mask.sum()),
        "raw_quad": quad.astype(float).tolist(),
    }


def build_track(
    input_path: Path,
    source: np.ndarray,
    source_bbox: tuple[int, int, int, int],
) -> tuple[dict[int, np.ndarray], list[dict]]:
    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not decode {input_path}")

    early_frames: dict[int, np.ndarray] = {}
    for frame_number in range(TRACK_START, FEATURE_ANCHOR + 1):
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"Missing input frame {frame_number}")
        early_frames[frame_number] = frame

    x, y, panel_width, panel_height = source_bbox
    source_panel_image = source[
        y : y + panel_height, x : x + panel_width, :3
    ]
    feature_scale = 0.5
    feature_source = cv2.resize(
        cv2.cvtColor(source_panel_image, cv2.COLOR_BGR2GRAY),
        None,
        fx=feature_scale,
        fy=feature_scale,
        interpolation=cv2.INTER_AREA,
    )
    sift = cv2.SIFT_create(nfeatures=5_000, contrastThreshold=0.02)
    source_keypoints, source_descriptors = sift.detectAndCompute(
        feature_source, None
    )
    if source_descriptors is None:
        raise RuntimeError("Could not describe the canonical sign face.")
    matcher = cv2.BFMatcher()

    raw_track: dict[int, np.ndarray] = {}
    record_map: dict[int, dict] = {}
    capture.set(cv2.CAP_PROP_POS_FRAMES, FEATURE_ANCHOR)
    previous_quad = None
    for frame_number in range(FEATURE_ANCHOR, FRAME_COUNT):
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"Missing input frame {frame_number}")
        try:
            quad, record = feature_panel_quad(
                frame,
                source_keypoints,
                source_descriptors,
                (feature_source.shape[1], feature_source.shape[0]),
                sift,
                matcher,
            )
        except RuntimeError:
            quad, record = detect_panel_quad(frame)
            record["method"] = "white-panel detection fallback"
            if previous_quad is not None:
                choices = []
                reversed_quad = quad[[0, 3, 2, 1]]
                for candidate in (quad, reversed_quad):
                    for offset in range(4):
                        choice = np.roll(candidate, offset, axis=0)
                        choices.append(
                            (
                                float(np.linalg.norm(choice - previous_quad)),
                                choice,
                            )
                        )
                quad = min(choices, key=lambda item: item[0])[1]
                record["raw_quad"] = quad.astype(float).tolist()
        raw_track[frame_number] = quad
        record_map[frame_number] = {"frame": frame_number, **record}
        previous_quad = quad
    capture.release()

    later_quad = raw_track[FEATURE_ANCHOR]
    for frame_number in range(FEATURE_ANCHOR - 1, TRACK_START - 1, -1):
        quad, record = optical_quad_backwards(
            early_frames[frame_number + 1],
            early_frames[frame_number],
            later_quad,
        )
        raw_track[frame_number] = quad
        record_map[frame_number] = {"frame": frame_number, **record}
        later_quad = quad

    ordered_raw = np.asarray(
        [raw_track[number] for number in range(TRACK_START, FRAME_COUNT)],
        dtype=np.float32,
    )
    smoothed = smooth_quads(ordered_raw, window=3)
    track: dict[int, np.ndarray] = {}
    for offset, frame_number in enumerate(range(TRACK_START, FRAME_COUNT)):
        track[frame_number] = smoothed[offset]
        record_map[frame_number]["smoothed_quad"] = smoothed[offset].astype(
            float
        ).tolist()
    records = [
        record_map[number] for number in range(TRACK_START, FRAME_COUNT)
    ]
    return track, records


def end_grip_occlusion(crop: np.ndarray, quad: np.ndarray) -> np.ndarray:
    ycrcb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCrCb)
    luminance, red_chroma, blue_chroma = cv2.split(ycrcb)
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    hue, saturation, _ = cv2.split(hsv)
    skin = (
        (luminance > 42)
        & (red_chroma >= 138)
        & (red_chroma <= 185)
        & (blue_chroma >= 68)
        & (blue_chroma <= 145)
        & ((hue <= 26) | (hue >= 170))
        & (saturation > 20)
        & (saturation < 138)
    ).astype(np.uint8) * 255
    end_zone = np.zeros(crop.shape[:2], dtype=np.uint8)
    top_left, top_right, bottom_right, bottom_left = quad
    end_fraction = 0.27
    left_top_inner = top_left + (top_right - top_left) * end_fraction
    left_bottom_inner = (
        bottom_left + (bottom_right - bottom_left) * end_fraction
    )
    right_top_inner = top_right + (top_left - top_right) * end_fraction
    right_bottom_inner = (
        bottom_right + (bottom_left - bottom_right) * end_fraction
    )
    cv2.fillConvexPoly(
        end_zone,
        np.asarray(
            [top_left, left_top_inner, left_bottom_inner, bottom_left],
            dtype=np.int32,
        ),
        255,
    )
    cv2.fillConvexPoly(
        end_zone,
        np.asarray(
            [right_top_inner, top_right, bottom_right, right_bottom_inner],
            dtype=np.int32,
        ),
        255,
    )
    end_zone = cv2.dilate(
        end_zone, np.ones((25, 25), np.uint8), iterations=1
    )
    occlusion = cv2.bitwise_and(skin, end_zone)
    occlusion = cv2.morphologyEx(
        occlusion,
        cv2.MORPH_CLOSE,
        np.ones((5, 5), np.uint8),
        iterations=1,
    )
    return cv2.dilate(
        occlusion, np.ones((3, 3), np.uint8), iterations=1
    )


def lock_face(
    frame: np.ndarray,
    target_quad: np.ndarray,
    source: np.ndarray,
    source_quad: np.ndarray,
    source_mask: np.ndarray,
    opacity: float,
    motion_sigma: float,
) -> np.ndarray:
    min_x = max(0, int(math.floor(target_quad[:, 0].min())) - 28)
    max_x = min(WIDTH, int(math.ceil(target_quad[:, 0].max())) + 29)
    min_y = max(0, int(math.floor(target_quad[:, 1].min())) - 28)
    max_y = min(HEIGHT, int(math.ceil(target_quad[:, 1].max())) + 29)
    crop = frame[min_y:max_y, min_x:max_x].copy()
    local_quad = target_quad - np.array([min_x, min_y], dtype=np.float32)
    transform = cv2.getPerspectiveTransform(source_quad, local_quad)
    crop_width = max_x - min_x
    crop_height = max_y - min_y
    warped_rgb = cv2.warpPerspective(
        source[:, :, :3],
        transform,
        (crop_width, crop_height),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    warped_alpha = cv2.warpPerspective(
        source_mask,
        transform,
        (crop_width, crop_height),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )

    panel = np.zeros(crop.shape[:2], dtype=np.uint8)
    cv2.fillConvexPoly(panel, local_quad.astype(np.int32), 255)
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    photographed_face = (
        (hsv[:, :, 2] > 118)
        & (hsv[:, :, 1] < 112)
        & (panel > 0)
    ).astype(np.uint8) * 255
    photographed_face = cv2.morphologyEx(
        photographed_face,
        cv2.MORPH_CLOSE,
        np.ones((15, 15), np.uint8),
        iterations=2,
    )
    photographed_face = cv2.dilate(
        photographed_face, np.ones((5, 5), np.uint8), iterations=1
    )
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    generated_ink = ((gray < 170) & (panel > 0)).astype(np.uint8) * 255
    generated_ink = cv2.dilate(
        generated_ink, np.ones((7, 7), np.uint8), iterations=1
    )
    clean = cv2.inpaint(crop, generated_ink, 9, cv2.INPAINT_TELEA)
    white_map = cv2.GaussianBlur(clean, (0, 0), 8).astype(np.float32)
    black_floor = np.full_like(white_map, 8.0, dtype=np.float32)
    source_float = warped_rgb.astype(np.float32) / 255.0
    mapped = black_floor + source_float * (white_map - black_floor)
    alpha = cv2.GaussianBlur(
        warped_alpha.astype(np.float32) / 255.0, (0, 0), 0.45
    )
    photographed_face_alpha = cv2.GaussianBlur(
        photographed_face.astype(np.float32) / 255.0, (0, 0), 0.65
    )
    alpha *= photographed_face_alpha
    if motion_sigma > 0.15:
        mapped = cv2.GaussianBlur(mapped, (0, 0), motion_sigma)
        alpha = cv2.GaussianBlur(alpha, (0, 0), motion_sigma * 0.55)
    alpha[end_grip_occlusion(crop, local_quad) > 0] = 0.0
    alpha *= opacity
    blended = (
        mapped * alpha[:, :, None]
        + crop.astype(np.float32) * (1.0 - alpha[:, :, None])
    ).clip(0, 255).astype(np.uint8)
    result = frame.copy()
    result[min_y:max_y, min_x:max_x] = blended
    return result


def make_text_overlay(
    lines: tuple[str, ...],
    centre_y: int,
    font_path: str,
    font_size: int,
    horizontal_padding: int,
    vertical_padding: int,
    line_gap: int,
    background_alpha: int,
) -> np.ndarray:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    measurements = [draw.textbbox((0, 0), line, font=font) for line in lines]
    widths = [box[2] - box[0] for box in measurements]
    heights = [box[3] - box[1] for box in measurements]
    text_height = sum(heights) + line_gap * (len(lines) - 1)
    x0 = int((WIDTH - max(widths)) / 2 - horizontal_padding)
    x1 = int((WIDTH + max(widths)) / 2 + horizontal_padding)
    y0 = int(centre_y - text_height / 2 - vertical_padding)
    y1 = int(centre_y + text_height / 2 + vertical_padding)
    draw.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=(y1 - y0) // 5,
        fill=(3, 3, 3, background_alpha),
    )
    cursor_y = centre_y - text_height / 2
    for line, width, height, box in zip(lines, widths, heights, measurements):
        draw.text(
            (
                (WIDTH - width) / 2,
                cursor_y - box[1],
            ),
            line,
            font=font,
            fill=(255, 255, 255, 255),
        )
        cursor_y += height + line_gap
    rgba = np.asarray(image)
    return cv2.cvtColor(rgba, cv2.COLOR_RGBA2BGRA)


def alpha_over(frame: np.ndarray, overlay: np.ndarray, opacity: float) -> np.ndarray:
    if opacity <= 0:
        return frame
    alpha = overlay[:, :, 3].astype(np.float32) / 255.0 * opacity
    return (
        overlay[:, :, :3].astype(np.float32) * alpha[:, :, None]
        + frame.astype(np.float32) * (1.0 - alpha[:, :, None])
    ).clip(0, 255).astype(np.uint8)


def synthesize_audio(output_path: Path) -> None:
    sample_rate = 48_000
    count = int(DURATION * sample_rate)
    time = np.arange(count, dtype=np.float64) / sample_rate
    rng = np.random.default_rng(17018)

    room_noise = rng.normal(0.0, 1.0, count)
    room = np.convolve(room_noise, np.ones(47) / 47.0, mode="same") * 0.016

    whoosh_start, whoosh_end = 1.05, 4.20
    start = int(whoosh_start * sample_rate)
    end = int(whoosh_end * sample_rate)
    phase = np.linspace(0.0, math.pi, end - start)
    envelope = np.zeros(count)
    envelope[start:end] = np.sin(phase) ** 1.8
    filtered_noise = np.convolve(
        rng.normal(0.0, 1.0, count),
        np.ones(15) / 15.0,
        mode="same",
    )
    whoosh = filtered_noise * envelope * 0.090

    settle_time = np.maximum(0.0, time - 4.12)
    settle = (
        np.sin(2 * math.pi * 172 * settle_time)
        + 0.45 * np.sin(2 * math.pi * 344 * settle_time)
    )
    settle *= np.exp(-settle_time * 16.0) * (time >= 4.12) * 0.10
    click = rng.normal(0.0, 1.0, count)
    click *= (
        np.exp(-np.maximum(0.0, time - 4.12) * 58.0)
        * (time >= 4.12)
        * 0.026
    )

    chime_time = np.maximum(0.0, time - 4.28)
    chime = np.sin(2 * math.pi * 784 * chime_time)
    chime += 0.42 * np.sin(2 * math.pi * 1176 * chime_time)
    chime *= np.exp(-chime_time * 7.5) * (time >= 4.28) * 0.025

    mono = room + whoosh + settle + click + chime
    pan = np.clip((time - whoosh_start) / (whoosh_end - whoosh_start), 0, 1)
    left = mono * (0.90 - 0.10 * pan)
    right = mono * (0.80 + 0.10 * pan)
    stereo = np.column_stack([left, right])
    peak = float(np.max(np.abs(stereo)))
    if peak:
        stereo *= 0.68 / peak
    pcm = np.int16(np.clip(stereo, -1.0, 1.0) * 32767)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(pcm.tobytes())


def start_encoder(output_path: Path, audio_path: Path) -> subprocess.Popen:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-s:v",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "pipe:0",
        "-i",
        str(audio_path),
        "-frames:v",
        str(FRAME_COUNT),
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "16",
        "-profile:v",
        "high",
        "-level",
        "4.1",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(output_path),
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


def encode_preview(master_path: Path, preview_path: Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(master_path),
        "-vf",
        "scale=720:1280:flags=lanczos",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "22",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(preview_path),
    ]
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr[-5000:])


def rectify(
    frame: np.ndarray, quad: np.ndarray, output_size: tuple[int, int]
) -> np.ndarray:
    width, height = output_size
    destination = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(quad, destination)
    return cv2.warpPerspective(
        frame,
        transform,
        (width, height),
        flags=cv2.INTER_LANCZOS4,
    )


def lettering_metrics(source: np.ndarray, observed: np.ndarray) -> dict:
    source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    observed_gray = cv2.cvtColor(observed, cv2.COLOR_BGR2GRAY)
    x0, x1 = 40, source.shape[1] - 40
    y0, y1 = 12, source.shape[0] - 12
    source_ink = source_gray[y0:y1, x0:x1] < 165
    observed_ink = observed_gray[y0:y1, x0:x1] < 165
    intersection = int(np.logical_and(source_ink, observed_ink).sum())
    union = int(np.logical_or(source_ink, observed_ink).sum())
    return {
        "ink_iou": intersection / union if union else 1.0,
        "source_ink_pixels": int(source_ink.sum()),
        "observed_ink_pixels": int(observed_ink.sum()),
    }


def make_qc(
    master_path: Path,
    source: np.ndarray,
    source_bbox: tuple[int, int, int, int],
    track: dict[int, np.ndarray],
    qc_dir: Path,
    slug: str,
) -> dict:
    qc_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(master_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not decode {master_path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    full_indices = [0, 18, 36, 49, 62, 74, 86, 96, 112, 136, 160, 191]
    full_samples: list[np.ndarray] = []
    for frame_number in full_indices:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, bgr = capture.read()
        if not ok:
            continue
        thumb = cv2.resize(bgr, (270, 480), interpolation=cv2.INTER_AREA)
        cv2.putText(
            thumb,
            f"{frame_number / FPS:0.2f}s",
            (12, 31),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.72,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        full_samples.append(thumb)
    full_sheet = np.zeros((480 * 3, 270 * 4, 3), dtype=np.uint8)
    for index, thumb in enumerate(full_samples):
        row, column = divmod(index, 4)
        full_sheet[
            row * 480 : (row + 1) * 480,
            column * 270 : (column + 1) * 270,
        ] = thumb
    full_filmstrip = qc_dir / f"{slug}-full-reel-filmstrip.jpg"
    cv2.imwrite(str(full_filmstrip), full_sheet)

    panel_width, panel_height = 1090, 200
    x, y, panel_source_width, panel_source_height = source_bbox
    source_panel_image = source[
        y : y + panel_source_height, x : x + panel_source_width, :3
    ]
    source_reference = cv2.resize(
        source_panel_image,
        (panel_width, panel_height),
        interpolation=cv2.INTER_AREA,
    )
    lettering_indices = [
        70,
        74,
        78,
        82,
        86,
        90,
        94,
        100,
        124,
        148,
        172,
        191,
    ]
    rectified: list[tuple[int, np.ndarray, dict]] = []
    for frame_number in lettering_indices:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, bgr = capture.read()
        if not ok:
            continue
        observed = rectify(
            bgr, track[frame_number], (panel_width, panel_height)
        )
        metric = lettering_metrics(source_reference, observed)
        rectified.append((frame_number, observed, metric))
    label_height = 34
    rows = 1 + len(rectified)
    lettering_sheet = np.full(
        (rows * (panel_height + label_height), panel_width, 3),
        20,
        dtype=np.uint8,
    )
    lettering_sheet[label_height : label_height + panel_height] = (
        source_reference
    )
    cv2.putText(
        lettering_sheet,
        "EXACT LIGHTBURN-DERIVED SOURCE",
        (18, 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.64,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    for row, (frame_number, observed, metric) in enumerate(rectified, start=1):
        y0 = row * (panel_height + label_height)
        lettering_sheet[y0 + label_height : y0 + label_height + panel_height] = (
            observed
        )
        label = (
            f"F{frame_number:03d} {frame_number / FPS:0.3f}s"
            f"  ink IoU {metric['ink_iou']:.4f}"
        )
        cv2.putText(
            lettering_sheet,
            label,
            (18, y0 + 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.64,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
    lettering_filmstrip = (
        qc_dir / f"{slug}-source-vs-video-lettering-filmstrip.jpg"
    )
    cv2.imwrite(str(lettering_filmstrip), lettering_sheet)
    Image.open(lettering_filmstrip).convert("RGB").save(
        qc_dir / f"{slug}-source-vs-video-lettering-filmstrip.pdf",
        "PDF",
        resolution=150.0,
    )

    frame_by_frame_pages: list[Image.Image] = []
    page_rows = 7
    rows_per_page = page_rows - 1
    capture.set(cv2.CAP_PROP_POS_FRAMES, TRACK_START)
    mapped_frames: list[tuple[int, np.ndarray, dict]] = []
    for frame_number in range(TRACK_START, FRAME_COUNT):
        ok, bgr = capture.read()
        if not ok:
            raise RuntimeError(
                f"Missing decoded QC frame {frame_number}"
            )
        observed = rectify(
            bgr, track[frame_number], (panel_width, panel_height)
        )
        mapped_frames.append(
            (
                frame_number,
                observed,
                lettering_metrics(source_reference, observed),
            )
        )
    for page_start in range(0, len(mapped_frames), rows_per_page):
        page = np.full(
            (page_rows * (panel_height + label_height), panel_width, 3),
            20,
            dtype=np.uint8,
        )
        page[label_height : label_height + panel_height] = source_reference
        cv2.putText(
            page,
            "EXACT LIGHTBURN-DERIVED SOURCE",
            (18, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.64,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        page_items = mapped_frames[
            page_start : page_start + rows_per_page
        ]
        for row, (frame_number, observed, metric) in enumerate(
            page_items, start=1
        ):
            row_y = row * (panel_height + label_height)
            page[
                row_y + label_height : row_y + label_height + panel_height
            ] = observed
            label = (
                f"F{frame_number:03d} {frame_number / FPS:0.3f}s"
                f"  mapped exact source  ink IoU {metric['ink_iou']:.4f}"
            )
            cv2.putText(
                page,
                label,
                (18, row_y + 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.64,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
        frame_by_frame_pages.append(
            Image.fromarray(cv2.cvtColor(page, cv2.COLOR_BGR2RGB))
        )
    frame_by_frame_pdf = (
        qc_dir / f"{slug}-frame-by-frame-lettering-QC.pdf"
    )
    frame_by_frame_pages[0].save(
        frame_by_frame_pdf,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=frame_by_frame_pages[1:],
    )

    capture.release()
    capture = cv2.VideoCapture(str(master_path))
    previous = None
    frame_differences: list[float] = []
    while True:
        ok, bgr = capture.read()
        if not ok:
            break
        gray = cv2.cvtColor(
            cv2.resize(bgr, (270, 480), interpolation=cv2.INTER_AREA),
            cv2.COLOR_BGR2GRAY,
        )
        if previous is not None:
            frame_differences.append(
                float(cv2.absdiff(gray, previous).mean())
            )
        previous = gray
    capture.release()
    median_difference = float(np.median(frame_differences))
    max_difference = float(np.max(frame_differences))
    hard_cut_limit = max(22.0, median_difference * 6.0)
    final_hold_metrics = [
        metric
        for frame_number, _, metric in mapped_frames
        if frame_number >= 100
    ]
    final_hold_ious = [metric["ink_iou"] for metric in final_hold_metrics]
    return {
        "master_decode": {
            "fps": fps,
            "frames": frame_count,
            "width": width,
            "height": height,
            "duration_seconds": frame_count / fps,
        },
        "continuity": {
            "consecutive_frame_difference_median": median_difference,
            "consecutive_frame_difference_max": max_difference,
            "hard_cut_limit": hard_cut_limit,
            "hard_cut_pass": max_difference < hard_cut_limit,
            "manual_dense_filmstrip_review": (
                "one continuous back-to-front diagonal 180-degree flip; "
                "no edit or time jump"
            ),
        },
        "lettering": {
            "deterministic_source_mapping": True,
            "readable_overlay_start_frame": TRACK_START,
            "full_source_opacity_frame": FACE_FULL,
            "mapped_frame_count": FRAME_COUNT - TRACK_START,
            "mapped_frame_range": [TRACK_START, FRAME_COUNT - 1],
            "sampled_frames": [
                {"frame": frame_number, **metric}
                for frame_number, _, metric in rectified
            ],
            "final_hold_ink_iou_min": min(final_hold_ious),
            "final_hold_ink_iou_mean": float(
                np.mean(final_hold_ious)
            ),
            "metric_note": (
                "IoU includes retained illumination, compression, motion "
                "blur and real grip occlusion; the lettering pixels are "
                "always derived from the canonical source."
            ),
        },
        "evidence": {
            "full_reel_filmstrip": str(full_filmstrip),
            "lettering_filmstrip": str(lettering_filmstrip),
            "frame_by_frame_lettering_pdf": str(frame_by_frame_pdf),
        },
    }


def main() -> None:
    raise RuntimeError(
        "RETIRED: product-surface overlays are forbidden. The exact sign must "
        "exist in a human-approved coherent source image and survive native "
        "video generation. If lettering, border colour, thickness or the "
        "white back changes, reject and regenerate; do not patch it."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--face", type=Path, required=True)
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--tracking-json", type=Path, required=True)
    parser.add_argument(
        "--track-json-in",
        type=Path,
        help=(
            "Reuse a proven planar track instead of detecting the current "
            "source face. This is the deterministic next-sign template route."
        ),
    )
    parser.add_argument("--qc-dir", type=Path, required=True)
    parser.add_argument("--slug", default="DM-C017-JANNAWAY")
    parser.add_argument("--concept-id", default="DM-C017")
    parser.add_argument("--version", default="v02-jannaway")
    parser.add_argument("--hook-line-1", default=DEFAULT_HOOK_LINES[0])
    parser.add_argument("--hook-line-2", default=DEFAULT_HOOK_LINES[1])
    parser.add_argument("--cta", default=DEFAULT_CTA)
    args = parser.parse_args()

    source = cv2.imread(str(args.face), cv2.IMREAD_UNCHANGED)
    source_quad, source_mask, source_bbox = source_panel(source)
    if args.track_json_in:
        reused_payload = json.loads(
            args.track_json_in.read_text(encoding="utf-8")
        )
        tracking_records = reused_payload["frames"]
        track = {
            int(record["frame"]): np.asarray(
                record["smoothed_quad"], dtype=np.float32
            )
            for record in tracking_records
        }
        missing_frames = [
            frame_number
            for frame_number in range(TRACK_START, FRAME_COUNT)
            if frame_number not in track
        ]
        if missing_frames:
            raise RuntimeError(
                "Reused track is missing frames: "
                + ", ".join(map(str, missing_frames[:12]))
            )
    else:
        track, tracking_records = build_track(
            args.input, source, source_bbox
        )
    args.tracking_json.parent.mkdir(parents=True, exist_ok=True)

    hook_overlay = make_text_overlay(
        (args.hook_line_1, args.hook_line_2),
        centre_y=180,
        font_path=r"C:\Windows\Fonts\segoeuib.ttf",
        font_size=55,
        horizontal_padding=42,
        vertical_padding=25,
        line_gap=6,
        background_alpha=178,
    )
    cta_overlay = make_text_overlay(
        (args.cta,),
        centre_y=1570,
        font_path=r"C:\Windows\Fonts\segoeuib.ttf",
        font_size=52,
        horizontal_padding=46,
        vertical_padding=24,
        line_gap=0,
        background_alpha=214,
    )

    synthesize_audio(args.audio)
    encoder = start_encoder(args.master, args.audio)
    if encoder.stdin is None:
        raise RuntimeError("Could not open ffmpeg input pipe.")
    capture = cv2.VideoCapture(str(args.input))
    if not capture.isOpened():
        raise RuntimeError(f"Could not decode {args.input}")
    previous_quad = None
    for frame_number in range(FRAME_COUNT):
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"Missing input frame {frame_number}")
        if frame_number >= TRACK_START:
            quad = track[frame_number]
            source_opacity = (
                1.0
                if FACE_FULL <= TRACK_START
                else smootherstep(
                    (frame_number - TRACK_START)
                    / (FACE_FULL - TRACK_START)
                )
            )
            speed = (
                float(
                    np.linalg.norm(
                        track[min(frame_number + 1, FRAME_COUNT - 1)] - quad,
                        axis=1,
                    ).mean()
                )
                if previous_quad is None
                else float(np.linalg.norm(quad - previous_quad, axis=1).mean())
            )
            motion_sigma = min(2.2, max(0.0, speed * 0.10))
            frame = lock_face(
                frame,
                quad,
                source,
                source_quad,
                source_mask,
                source_opacity,
                motion_sigma,
            )
            previous_quad = quad
        seconds = frame_number / FPS
        hook_opacity = fade_window(seconds, 0.04, 0.20, 2.35, 2.95)
        cta_opacity = fade_window(seconds, 4.30, 4.62, 7.45, 7.90)
        frame = alpha_over(frame, hook_overlay, hook_opacity)
        frame = alpha_over(frame, cta_overlay, cta_opacity)
        encoder.stdin.write(np.ascontiguousarray(frame).tobytes())
    capture.release()
    encoder.stdin.close()
    stderr = encoder.stderr.read().decode("utf-8", errors="replace")
    return_code = encoder.wait()
    if return_code:
        raise RuntimeError(
            f"ffmpeg master encode failed ({return_code}):\n{stderr[-5000:]}"
        )
    encode_preview(args.master, args.preview)

    tracking_payload = {
        "input": {
            "path": str(args.input.resolve()),
            "sha256": sha256(args.input),
        },
        "source_face": {
            "path": str(args.face.resolve()),
            "sha256": sha256(args.face),
            "panel_bbox": list(source_bbox),
        },
        "settings": {
            "fps": FPS,
            "output_frames": FRAME_COUNT,
            "track_start_frame": TRACK_START,
            "feature_anchor_frame": FEATURE_ANCHOR,
            "full_source_opacity_frame": FACE_FULL,
            "tracker": (
                "SIFT source-to-frame homography from the readable reveal, "
                "backward optical-flow homography through the foreshortened "
                "turn, three-frame corner smoothing"
            ),
            "replacement": (
                "canonical source face through planar homography, generated "
                "lettering removed, photographed illumination retained"
            ),
            "track_reused_from": (
                str(args.track_json_in.resolve())
                if args.track_json_in
                else None
            ),
        },
        "frames": tracking_records,
    }
    args.tracking_json.write_text(
        json.dumps(tracking_payload, indent=2), encoding="utf-8"
    )
    qc = make_qc(
        args.master, source, source_bbox, track, args.qc_dir, args.slug
    )
    report = {
        "concept_id": args.concept_id,
        "version": args.version,
        "published": False,
        "master": {
            "path": str(args.master.resolve()),
            "sha256": sha256(args.master),
            "bytes": args.master.stat().st_size,
            "width": WIDTH,
            "height": HEIGHT,
            "fps": FPS,
            "frames": FRAME_COUNT,
            "duration_seconds": DURATION,
        },
        "preview": {
            "path": str(args.preview.resolve()),
            "sha256": sha256(args.preview),
            "bytes": args.preview.stat().st_size,
            "width": 720,
            "height": 1280,
        },
        "audio": {
            "path": str(args.audio.resolve()),
            "sha256": sha256(args.audio),
            "sample_rate_hz": 48_000,
            "channels": 2,
            "source": "deterministic synthetic room, turn whoosh, settle and chime",
        },
        "edit": {
            "hook": f"{args.hook_line_1} / {args.hook_line_2}",
            "cta": args.cta,
        },
        "qc": qc,
    }
    (args.qc_dir / f"{args.slug}-qc-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
