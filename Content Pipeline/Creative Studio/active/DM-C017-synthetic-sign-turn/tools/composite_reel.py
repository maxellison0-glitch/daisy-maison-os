#!/usr/bin/env python3
"""RETIRED failure-evidence tool for the rejected synthetic sign overlay."""

from __future__ import annotations

raise RuntimeError(
    "RETIRED: product-surface overlays, planar tracks and moving sign-face "
    "replacements are forbidden because humans see the material mismatch."
)

import argparse
import hashlib
import json
import math
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


WIDTH = 1080
HEIGHT = 1920
FPS = 24
DURATION = 8.0
FRAME_COUNT = int(FPS * DURATION)
SIGN_WIDTH = 1026
SIGN_HEIGHT = 225
SIGN_CX = 540.0
SIGN_CY = 1010.0
TURN_START = 0.70
TURN_END = 3.80
HOLD_QC_START = 4.00
CAMERA_DISTANCE = 2600.0
HOOK = "WAIT FOR THE NAME…"
CTA = "PERSONALISE YOURS  →"


@dataclass
class Geometry:
    frame: int
    time_seconds: float
    angle_degrees: float
    quad: list[list[float]]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def smootherstep(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value**3 * (value * (value * 6.0 - 15.0) + 10.0)


def turn_angle(time_seconds: float) -> float:
    if time_seconds <= TURN_START:
        return math.pi
    if time_seconds >= TURN_END:
        return 0.0
    progress = (time_seconds - TURN_START) / (TURN_END - TURN_START)
    return math.pi * (1.0 - smootherstep(progress))


def sign_quad(angle: float) -> np.ndarray:
    points = []
    for x, y in (
        (-SIGN_WIDTH / 2, -SIGN_HEIGHT / 2),
        (SIGN_WIDTH / 2, -SIGN_HEIGHT / 2),
        (SIGN_WIDTH / 2, SIGN_HEIGHT / 2),
        (-SIGN_WIDTH / 2, SIGN_HEIGHT / 2),
    ):
        rotated_y = y * math.cos(angle)
        depth = y * math.sin(angle)
        perspective = CAMERA_DISTANCE / (CAMERA_DISTANCE + depth)
        points.append(
            (
                SIGN_CX + x * perspective,
                SIGN_CY + rotated_y * perspective,
            )
        )
    return np.float32(points)


def alpha_over(background: np.ndarray, foreground: np.ndarray) -> np.ndarray:
    alpha = foreground[:, :, 3:4].astype(np.float32) / 255.0
    blended = (
        foreground[:, :, :3].astype(np.float32) * alpha
        + background.astype(np.float32) * (1.0 - alpha)
    )
    return np.clip(blended, 0, 255).astype(np.uint8)


def load_scene(base_path: Path) -> np.ndarray:
    image = cv2.imread(str(base_path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(base_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return cv2.resize(image, (WIDTH, HEIGHT), interpolation=cv2.INTER_LANCZOS4)


def load_face(face_path: Path) -> tuple[np.ndarray, np.ndarray]:
    image = cv2.imread(str(face_path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(face_path)
    if image.shape[2] != 4:
        raise ValueError("The sign face must be an RGBA PNG")
    face = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    back = np.zeros_like(face)
    rng = np.random.default_rng(17017)
    texture = rng.normal(0, 1.3, face.shape[:2]).astype(np.float32)
    for channel, base_value in enumerate((35, 35, 35)):
        back[:, :, channel] = np.clip(base_value + texture, 0, 255)
    back[:, :, 3] = face[:, :, 3]
    # Physical mounting holes on the rear, based on the canonical millimetres.
    for x_mm, y_mm in ((23.306, 63.735), (546.0, 61.5)):
        centre = (
            int(round(x_mm / 570.0 * face.shape[1])),
            int(round(y_mm / 125.0 * face.shape[0])),
        )
        cv2.circle(back, centre, 8, (104, 78, 66, 255), thickness=-1)
        cv2.circle(back, centre, 9, (18, 18, 18, 255), thickness=2)
    return face, back


def make_hand_mask(scene: np.ndarray) -> np.ndarray:
    """Select only the fingertips that should sit above the sign end caps."""
    ycrcb = cv2.cvtColor(scene, cv2.COLOR_RGB2YCrCb)
    skin = cv2.inRange(
        ycrcb,
        np.array([45, 128, 72], dtype=np.uint8),
        np.array([255, 188, 145], dtype=np.uint8),
    )
    allowed = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    left = np.array(
        [[18, 945], [92, 940], [99, 1000], [98, 1135], [62, 1165], [18, 1095]],
        dtype=np.int32,
    )
    right = np.array(
        [[982, 948], [1060, 930], [1079, 1098], [1018, 1162], [982, 1128]],
        dtype=np.int32,
    )
    cv2.fillPoly(allowed, [left, right], 255)
    mask = cv2.bitwise_and(skin, allowed)
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)),
        iterations=2,
    )
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
    return cv2.GaussianBlur(mask, (0, 0), 2.0)


def render_surface(
    texture: np.ndarray,
    angle: float,
    add_shadow: bool = True,
) -> np.ndarray:
    layer = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    quad = sign_quad(angle)
    cosine = abs(math.cos(angle))

    if cosine > 0.018:
        source = np.float32(
            [
                [0, 0],
                [texture.shape[1] - 1, 0],
                [texture.shape[1] - 1, texture.shape[0] - 1],
                [0, texture.shape[0] - 1],
            ]
        )
        transform = cv2.getPerspectiveTransform(source, quad)
        warped = cv2.warpPerspective(
            texture,
            transform,
            (WIDTH, HEIGHT),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0),
        )
        layer = warped

    # The real plaque is thin but not infinitely thin. This keeps the midpoint
    # readable as a continuous physical turn instead of a disappearing cut.
    if cosine < 0.22:
        centre_width = float(
            (
                np.linalg.norm(quad[1] - quad[0])
                + np.linalg.norm(quad[2] - quad[3])
            )
            / 2
        )
        thickness = max(2, int(round(7.0 * abs(math.sin(angle)))))
        x0 = int(round(SIGN_CX - centre_width / 2))
        x1 = int(round(SIGN_CX + centre_width / 2))
        y0 = int(round(SIGN_CY - thickness / 2))
        y1 = int(round(SIGN_CY + thickness / 2))
        cv2.rectangle(layer, (x0, y0), (x1, y1), (31, 31, 31, 255), -1)
        cv2.line(layer, (x0, y0), (x1, y0), (102, 102, 102, 230), 1)

    if add_shadow and np.any(layer[:, :, 3]):
        shadow_alpha = cv2.GaussianBlur(layer[:, :, 3], (0, 0), 12.0)
        shadow = np.zeros_like(layer)
        shadow[:, :, 3] = (shadow_alpha.astype(np.float32) * 0.34).astype(np.uint8)
        shift = np.float32([[1, 0, 0], [0, 1, 11]])
        shadow = cv2.warpAffine(
            shadow,
            shift,
            (WIDTH, HEIGHT),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
        )
        shadowed = np.zeros_like(layer)
        shadowed = alpha_rgba_over(shadowed, shadow)
        layer = alpha_rgba_over(shadowed, layer)
    return layer


def alpha_rgba_over(background: np.ndarray, foreground: np.ndarray) -> np.ndarray:
    front_alpha = foreground[:, :, 3:4].astype(np.float32) / 255.0
    back_alpha = background[:, :, 3:4].astype(np.float32) / 255.0
    out_alpha = front_alpha + back_alpha * (1.0 - front_alpha)
    out_rgb_premult = (
        foreground[:, :, :3].astype(np.float32) * front_alpha
        + background[:, :, :3].astype(np.float32)
        * back_alpha
        * (1.0 - front_alpha)
    )
    output = np.zeros_like(background)
    valid = out_alpha[:, :, 0] > 1e-6
    output[:, :, 3] = np.clip(out_alpha[:, :, 0] * 255.0, 0, 255)
    output[valid, :3] = np.clip(
        out_rgb_premult[valid] / out_alpha[valid],
        0,
        255,
    )
    return output


def render_sign_motion(
    time_seconds: float,
    face: np.ndarray,
    back: np.ndarray,
) -> tuple[np.ndarray, float]:
    angle = turn_angle(time_seconds)
    turning = TURN_START < time_seconds < TURN_END
    sample_count = 3 if turning else 1
    offsets = np.linspace(-0.42, 0.42, sample_count) / FPS
    premultiplied = np.zeros((HEIGHT, WIDTH, 4), dtype=np.float32)
    accumulated_alpha = np.zeros((HEIGHT, WIDTH, 1), dtype=np.float32)
    for offset in offsets:
        sample_time = min(DURATION, max(0.0, time_seconds + float(offset)))
        sample_angle = turn_angle(sample_time)
        texture = face if math.cos(sample_angle) >= 0 else back
        rendered = render_surface(texture, sample_angle)
        alpha = rendered[:, :, 3:4].astype(np.float32) / 255.0
        premultiplied[:, :, :3] += rendered[:, :, :3].astype(np.float32) * alpha
        accumulated_alpha += alpha
    accumulated_alpha /= sample_count
    premultiplied[:, :, :3] /= sample_count
    result = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    visible = accumulated_alpha[:, :, 0] > 1e-6
    result[:, :, 3] = np.clip(accumulated_alpha[:, :, 0] * 255.0, 0, 255)
    result[visible, :3] = np.clip(
        premultiplied[visible, :3] / accumulated_alpha[visible],
        0,
        255,
    )
    return result, angle


def camera_transform(time_seconds: float) -> np.ndarray:
    fade = 1.0 - smootherstep(
        (time_seconds - (TURN_END - 0.55)) / 0.55
    )
    dx = fade * 1.8 * math.sin(time_seconds * 2.1)
    dy = fade * 2.2 * math.sin(time_seconds * 1.65 + 0.7)
    scale = 1.0 + fade * 0.0012 * math.sin(time_seconds * 1.25)
    return cv2.getRotationMatrix2D((WIDTH / 2, HEIGHT / 2), 0.0, scale) + np.array(
        [[0.0, 0.0, dx], [0.0, 0.0, dy]],
        dtype=np.float64,
    )


def transformed_quad(quad: np.ndarray, affine: np.ndarray) -> np.ndarray:
    homogeneous = np.hstack([quad, np.ones((4, 1), dtype=np.float32)])
    return np.float32(homogeneous @ affine.T)


def fade_window(
    time_seconds: float,
    fade_in_start: float,
    full_start: float,
    full_end: float,
    fade_out_end: float,
) -> float:
    if time_seconds < fade_in_start or time_seconds > fade_out_end:
        return 0.0
    if time_seconds < full_start:
        return smootherstep((time_seconds - fade_in_start) / (full_start - fade_in_start))
    if time_seconds <= full_end:
        return 1.0
    return 1.0 - smootherstep((time_seconds - full_end) / (fade_out_end - full_end))


def draw_pill(
    frame: np.ndarray,
    text: str,
    centre_y: int,
    font: ImageFont.FreeTypeFont,
    opacity: float,
    horizontal_padding: int,
    vertical_padding: int,
    background_alpha: int,
) -> np.ndarray:
    if opacity <= 0.0:
        return frame
    image = Image.fromarray(frame).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x0 = int((WIDTH - text_width) / 2 - horizontal_padding)
    x1 = int((WIDTH + text_width) / 2 + horizontal_padding)
    y0 = int(centre_y - text_height / 2 - vertical_padding)
    y1 = int(centre_y + text_height / 2 + vertical_padding)
    draw.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=(y1 - y0) // 2,
        fill=(1, 1, 1, background_alpha),
    )
    draw.text(
        ((WIDTH - text_width) / 2, centre_y - text_height / 2 - bbox[1]),
        text,
        font=font,
        fill=(255, 255, 255, 255),
    )
    alpha = overlay.getchannel("A").point(lambda value: int(value * opacity))
    overlay.putalpha(alpha)
    return np.asarray(Image.alpha_composite(image, overlay).convert("RGB"))


def add_typography(
    frame: np.ndarray,
    time_seconds: float,
    hook_font: ImageFont.FreeTypeFont,
    cta_font: ImageFont.FreeTypeFont,
) -> np.ndarray:
    hook_alpha = fade_window(time_seconds, 0.05, 0.25, 2.75, 3.35)
    result = draw_pill(
        frame,
        HOOK,
        188,
        hook_font,
        hook_alpha,
        horizontal_padding=35,
        vertical_padding=21,
        background_alpha=154,
    )
    cta_alpha = fade_window(time_seconds, 4.35, 4.65, 7.45, 7.90)
    return draw_pill(
        result,
        CTA,
        1535,
        cta_font,
        cta_alpha,
        horizontal_padding=42,
        vertical_padding=24,
        background_alpha=205,
    )


def synthesize_audio(output_path: Path) -> None:
    sample_rate = 48_000
    count = int(DURATION * sample_rate)
    time = np.arange(count, dtype=np.float64) / sample_rate
    rng = np.random.default_rng(17017)
    white = rng.normal(0.0, 1.0, count)
    room = np.convolve(white, np.ones(37) / 37.0, mode="same") * 0.020

    whoosh_env = np.zeros(count)
    start = int(0.66 * sample_rate)
    end = int(3.92 * sample_rate)
    phase = np.linspace(0.0, math.pi, end - start)
    whoosh_env[start:end] = np.sin(phase) ** 1.7
    whoosh_noise = np.convolve(
        rng.normal(0.0, 1.0, count),
        np.ones(13) / 13.0,
        mode="same",
    )
    whoosh = whoosh_noise * whoosh_env * 0.085

    settle_time = np.maximum(0.0, time - 3.80)
    settle = (
        np.sin(2 * math.pi * 185 * settle_time)
        + 0.55 * np.sin(2 * math.pi * 325 * settle_time)
    )
    settle *= np.exp(-settle_time * 14.0) * (time >= 3.80) * 0.12
    click = rng.normal(0.0, 1.0, count)
    click_env = np.exp(-np.maximum(0.0, time - 3.80) * 55.0) * (time >= 3.80)
    click *= click_env * 0.028

    chime_time = np.maximum(0.0, time - 4.05)
    chime = np.sin(2 * math.pi * 880 * chime_time)
    chime += 0.45 * np.sin(2 * math.pi * 1320 * chime_time)
    chime *= np.exp(-chime_time * 7.5) * (time >= 4.05) * 0.027

    mono = room + whoosh + settle + click + chime
    pan = np.clip((time - TURN_START) / (TURN_END - TURN_START), 0.0, 1.0)
    left = mono * (0.92 - 0.12 * pan)
    right = mono * (0.80 + 0.12 * pan)
    stereo = np.column_stack([left, right])
    peak = float(np.max(np.abs(stereo)))
    if peak > 0:
        stereo *= 0.69 / peak
    pcm = np.int16(np.clip(stereo, -1.0, 1.0) * 32767)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())


def encode_master(
    output_path: Path,
    audio_path: Path,
    frames: Iterable[np.ndarray],
) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s:v",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "pipe:0",
        "-i",
        str(audio_path),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
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
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    for frame in frames:
        process.stdin.write(np.ascontiguousarray(frame).tobytes())
    process.stdin.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace")
    code = process.wait()
    if code != 0:
        raise RuntimeError(f"ffmpeg master encode failed ({code}):\n{stderr[-5000:]}")


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
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-5000:])


def probe_video(path: Path) -> dict:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    text = result.stderr
    return {
        "has_1080x1920": "1080x1920" in text,
        "has_h264": "Video: h264" in text,
        "has_aac": "Audio: aac" in text,
        "has_24_fps": "24 fps" in text,
        "probe_excerpt": "\n".join(
            line.strip()
            for line in text.splitlines()
            if "Duration:" in line or "Video:" in line or "Audio:" in line
        ),
    }


def rectify_face(frame: np.ndarray, quad: np.ndarray) -> np.ndarray:
    destination = np.float32(
        [
            [0, 0],
            [SIGN_WIDTH - 1, 0],
            [SIGN_WIDTH - 1, SIGN_HEIGHT - 1],
            [0, SIGN_HEIGHT - 1],
        ]
    )
    transform = cv2.getPerspectiveTransform(quad, destination)
    return cv2.warpPerspective(
        frame,
        transform,
        (SIGN_WIDTH, SIGN_HEIGHT),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
    )


def lettering_metrics(source: np.ndarray, observed: np.ndarray) -> dict:
    x0, x1 = 80, SIGN_WIDTH - 80
    y0, y1 = 16, SIGN_HEIGHT - 12
    src = source[y0:y1, x0:x1]
    obs = observed[y0:y1, x0:x1]
    src_gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    obs_gray = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
    src_ink = src_gray < 170
    obs_ink = obs_gray < 170
    intersection = int(np.logical_and(src_ink, obs_ink).sum())
    union = int(np.logical_or(src_ink, obs_ink).sum())
    iou = intersection / union if union else 1.0
    difference = src.astype(np.float32) - obs.astype(np.float32)
    mse = float(np.mean(difference**2))
    psnr = 99.0 if mse == 0 else 10.0 * math.log10((255.0**2) / mse)
    mae = float(np.mean(np.abs(difference)))
    return {"ink_iou": iou, "psnr_db": psnr, "rgb_mae": mae}


def create_qc(
    master_path: Path,
    face_path: Path,
    qc_dir: Path,
    geometry: list[Geometry],
) -> dict:
    qc_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(master_path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not decode {master_path}")
    face_rgba = cv2.cvtColor(
        cv2.imread(str(face_path), cv2.IMREAD_UNCHANGED),
        cv2.COLOR_BGRA2RGBA,
    )
    source = cv2.resize(
        face_rgba[:, :, :3],
        (SIGN_WIDTH, SIGN_HEIGHT),
        interpolation=cv2.INTER_AREA,
    )
    source_alpha = cv2.resize(
        face_rgba[:, :, 3],
        (SIGN_WIDTH, SIGN_HEIGHT),
        interpolation=cv2.INTER_AREA,
    )
    source[source_alpha < 250] = 0

    start_frame = int(round(HOLD_QC_START * FPS))
    observed_frames: list[tuple[int, np.ndarray, dict]] = []
    metrics = []
    frame_index = 0
    geometry_by_frame = {item.frame: item for item in geometry}
    while True:
        ok, bgr = capture.read()
        if not ok:
            break
        if frame_index >= start_frame:
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            quad = np.float32(geometry_by_frame[frame_index].quad)
            rectified = rectify_face(rgb, quad)
            metric = lettering_metrics(source, rectified)
            metrics.append({"frame": frame_index, **metric})
            observed_frames.append((frame_index, rectified, metric))
        frame_index += 1
    capture.release()

    filmstrip_path = qc_dir / "DM-C017-frame-by-frame-qc-filmstrip.pdf"
    page_width, page_height = landscape(A3)
    document = canvas.Canvas(str(filmstrip_path), pagesize=(page_width, page_height))
    document.setTitle("DM-C017 frame-by-frame lettering QC")
    columns, rows = 4, 4
    margin_x, margin_y = 28, 30
    cell_w = (page_width - margin_x * 2) / columns
    cell_h = (page_height - margin_y * 2) / rows
    for item_index, (frame_no, observed, metric) in enumerate(observed_frames):
        slot = item_index % (columns * rows)
        if slot == 0:
            document.setFont("Helvetica-Bold", 10)
            document.drawString(
                margin_x,
                page_height - 18,
                "DM-C017 exact source (top) vs decoded master (bottom)",
            )
        column = slot % columns
        row = slot // columns
        x = margin_x + column * cell_w
        y_top = page_height - margin_y - row * cell_h
        image_w = cell_w - 14
        image_h = image_w / (SIGN_WIDTH / SIGN_HEIGHT)
        source_pil = Image.fromarray(source)
        observed_pil = Image.fromarray(observed)
        document.drawImage(
            ImageReader(source_pil),
            x + 7,
            y_top - 25 - image_h,
            width=image_w,
            height=image_h,
            preserveAspectRatio=True,
            mask="auto",
        )
        document.drawImage(
            ImageReader(observed_pil),
            x + 7,
            y_top - 31 - image_h * 2,
            width=image_w,
            height=image_h,
            preserveAspectRatio=True,
            mask="auto",
        )
        document.setFont("Helvetica", 7)
        document.drawString(
            x + 7,
            y_top - 12,
            f"f{frame_no:03d}  {frame_no/FPS:0.3f}s  "
            f"ink IoU {metric['ink_iou']:.4f}  "
            f"PSNR {metric['psnr_db']:.1f}dB",
        )
        if slot == columns * rows - 1 or item_index == len(observed_frames) - 1:
            document.showPage()
    document.save()

    # Quick full-frame filmstrip for visual review of the whole turn.
    sample_indices = [0, 18, 36, 54, 66, 78, 90, 102, 126, 150, 174, 191]
    capture = cv2.VideoCapture(str(master_path))
    samples = []
    for index in sample_indices:
        capture.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, bgr = capture.read()
        if ok:
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            thumb = cv2.resize(rgb, (270, 480), interpolation=cv2.INTER_AREA)
            cv2.putText(
                thumb,
                f"{index/FPS:0.2f}s",
                (12, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            samples.append(thumb)
    capture.release()
    contact = np.zeros((480 * 3, 270 * 4, 3), dtype=np.uint8)
    for index, thumb in enumerate(samples):
        row, column = divmod(index, 4)
        contact[row * 480 : (row + 1) * 480, column * 270 : (column + 1) * 270] = thumb
    Image.fromarray(contact).save(
        qc_dir / "DM-C017-full-reel-filmstrip.jpg",
        quality=93,
        subsampling=0,
    )

    ious = [item["ink_iou"] for item in metrics]
    psnrs = [item["psnr_db"] for item in metrics]
    maes = [item["rgb_mae"] for item in metrics]
    ink_iou_floor = 0.92
    psnr_floor_db = 27.0
    rgb_mae_ceiling = 3.5
    lettering_pass = (
        min(ious) >= ink_iou_floor
        and min(psnrs) >= psnr_floor_db
        and max(maes) <= rgb_mae_ceiling
    )
    return {
        "readable_hold_frame_count": len(metrics),
        "readable_hold_seconds": len(metrics) / FPS,
        "ink_iou_min": min(ious),
        "ink_iou_mean": float(np.mean(ious)),
        "psnr_db_min": min(psnrs),
        "psnr_db_mean": float(np.mean(psnrs)),
        "rgb_mae_max": max(maes),
        "rgb_mae_mean": float(np.mean(maes)),
        "thresholds": {
            "ink_iou_min": ink_iou_floor,
            "psnr_db_min": psnr_floor_db,
            "rgb_mae_max": rgb_mae_ceiling,
            "basis": (
                "Central lettering region of every decoded hold frame after "
                "forward and inverse perspective resampling plus H.264 4:2:0; "
                "source/observed pairs remain in the filmstrip for visual audit."
            ),
        },
        "lettering_pass": lettering_pass,
        "filmstrip_pdf": str(filmstrip_path),
    }


def main() -> None:
    raise RuntimeError(
        "RETIRED: a rotating or tracked sign graphic is not a valid Daisy "
        "Maison video. The physical sign must be native, human-approved and "
        "preserved through genuine continuous motion."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--face", type=Path, required=True)
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--preview", type=Path, required=True)
    parser.add_argument("--qc-dir", type=Path, required=True)
    parser.add_argument("--checkpoints-only", action="store_true")
    args = parser.parse_args()

    scene = load_scene(args.base)
    face, back = load_face(args.face)
    hand_mask = make_hand_mask(scene)
    hand_layer = np.dstack([scene, hand_mask])
    hook_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 54)
    cta_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 51)

    geometry: list[Geometry] = []
    args.qc_dir.mkdir(parents=True, exist_ok=True)
    keyframe_dir = args.qc_dir / "render-checkpoints"
    keyframe_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_frames = {0, 36, 54, 72, 91, 114, 156, 191}

    def render_one(frame_number: int) -> tuple[np.ndarray, Geometry]:
        time_seconds = frame_number / FPS
        sign_layer, angle = render_sign_motion(time_seconds, face, back)
        composed = alpha_over(scene.copy(), sign_layer)
        composed = alpha_over(composed, hand_layer)
        affine = camera_transform(time_seconds)
        composed = cv2.warpAffine(
            composed,
            affine,
            (WIDTH, HEIGHT),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101,
        )
        composed = add_typography(composed, time_seconds, hook_font, cta_font)
        quad = transformed_quad(sign_quad(angle), affine)
        return composed, Geometry(
            frame=frame_number,
            time_seconds=time_seconds,
            angle_degrees=math.degrees(angle),
            quad=quad.astype(float).tolist(),
        )

    if args.checkpoints_only:
        for frame_number in sorted(checkpoint_frames):
            composed, _ = render_one(frame_number)
            Image.fromarray(composed).save(
                keyframe_dir / f"frame-{frame_number:03d}.jpg",
                quality=94,
                subsampling=0,
            )
        print(f"Rendered {len(checkpoint_frames)} checkpoints to {keyframe_dir}")
        return

    def frame_iterator() -> Iterable[np.ndarray]:
        for frame_number in range(FRAME_COUNT):
            composed, frame_geometry = render_one(frame_number)
            geometry.append(frame_geometry)
            if frame_number in checkpoint_frames:
                Image.fromarray(composed).save(
                    keyframe_dir / f"frame-{frame_number:03d}.jpg",
                    quality=94,
                    subsampling=0,
                )
            yield composed

    audio_path = args.master.parent / "DM-C017-synthetic-sound.wav"
    synthesize_audio(audio_path)
    encode_master(args.master, audio_path, frame_iterator())
    encode_preview(args.master, args.preview)

    args.qc_dir.mkdir(parents=True, exist_ok=True)
    geometry_path = args.qc_dir / "DM-C017-frame-geometry.json"
    geometry_path.write_text(
        json.dumps([item.__dict__ for item in geometry], indent=2),
        encoding="utf-8",
    )
    qc = create_qc(args.master, args.face, args.qc_dir, geometry)
    probe = probe_video(args.master)
    angles = [item.angle_degrees for item in geometry]
    continuity_pass = all(
        angles[index + 1] <= angles[index] + 1e-9
        for index in range(len(angles) - 1)
    )
    report = {
        "concept": "DM-C017-synthetic-sign-turn",
        "master": {
            "path": str(args.master),
            "sha256": sha256(args.master),
            "width": WIDTH,
            "height": HEIGHT,
            "fps": FPS,
            "duration_seconds": DURATION,
            **probe,
        },
        "preview": {
            "path": str(args.preview),
            "sha256": sha256(args.preview),
            "width": 720,
            "height": 1280,
        },
        "source_face": {
            "path": str(args.face),
            "sha256": sha256(args.face),
            "physical_size_mm": [570, 125],
            "pixel_size": [2280, 500],
        },
        "motion": {
            "method": "deterministic textured 3D plane, temporal supersampling",
            "turn_start_seconds": TURN_START,
            "turn_end_seconds": TURN_END,
            "start_angle_degrees": angles[0],
            "end_angle_degrees": angles[-1],
            "monotonic_continuity_pass": continuity_pass,
            "hard_cuts": 0,
        },
        "lettering_qc": qc,
        "acceptance": {
            "format_pass": all(
                (
                    probe["has_1080x1920"],
                    probe["has_h264"],
                    probe["has_aac"],
                    probe["has_24_fps"],
                )
            ),
            "continuity_pass": continuity_pass,
            "lettering_pass": qc["lettering_pass"],
        },
    }
    (args.qc_dir / "DM-C017-qc-report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
