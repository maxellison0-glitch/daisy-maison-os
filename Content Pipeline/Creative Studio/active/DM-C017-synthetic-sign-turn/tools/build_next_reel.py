#!/usr/bin/env python3
"""Build exact Daisy Maison street-sign SVG/PNG/PDF assets.

This script deliberately stops before image or video generation. It cannot
reuse motion, track a sign or overlay artwork. A human-approved coherent sign
image and real front/edge/back references are required before a separate
native video workflow may begin.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
CANONICAL_BUILD = WORKSPACE / "projects" / "daisy-street-sign" / "artwork" / "build.py"
NODE = (
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "node"
    / "bin"
    / "node.exe"
)
NODE_MODULES = NODE.parents[1] / "node_modules"
PNPM_NODE_MODULES = NODE_MODULES / ".pnpm" / "node_modules"


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-")
    if not slug:
        raise ValueError("The slug must contain at least one letter or number")
    return slug[:80]


def checked_text(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{label} cannot be blank")
    if "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be one line")
    if len(value) > 160:
        raise ValueError(f"{label} is unexpectedly long; review it manually")
    return value


def command_text(command: list[str | Path]) -> str:
    return subprocess.list2cmdline([str(item) for item in command])


def run(command: list[str | Path], *, env: dict[str, str] | None = None) -> None:
    print(f"+ {command_text(command)}", flush=True)
    subprocess.run([str(item) for item in command], check=True, env=env)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description=(
            "Build exact sign assets only. Product-surface overlays and "
            "motion-template reuse are retired."
        )
    )
    parser.add_argument("--line1", required=True, help='For example: "MR & MRS EVERLY"')
    parser.add_argument(
        "--line2",
        required=True,
        help='For example: "FROM THIS DAY FORWARD... 14TH JUNE 2026"',
    )
    parser.add_argument(
        "--slug",
        help="Output stem; defaults to a safe version of line 1",
    )
    parser.add_argument(
        "--order-ref",
        default="SYNTHETIC-CONTENT",
        help="Non-customer provenance label embedded in the SVG",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the intended commands without writing",
    )
    args = parser.parse_args()

    line1 = checked_text(args.line1, "line1")
    line2 = checked_text(args.line2, "line2")
    slug = safe_slug(args.slug or line1)
    order_ref = checked_text(args.order_ref, "order-ref")

    required = [
        CANONICAL_BUILD,
        Path(__file__).with_name("rasterize_sign.cjs"),
        Path(__file__).with_name("make_exact_visual_pdf.py"),
    ]
    missing = [str(path) for path in required if not path.exists()]
    if not NODE.exists():
        missing.append(str(NODE))
    if not NODE_MODULES.exists():
        missing.append(str(NODE_MODULES))
    if not PNPM_NODE_MODULES.exists():
        missing.append(str(PNPM_NODE_MODULES))
    if missing:
        raise FileNotFoundError("Missing workflow dependency:\n" + "\n".join(missing))

    assets = LANE / "assets"
    svg = assets / f"{slug}-sign-face.svg"
    png = assets / f"{slug}-sign-face.png"
    pdf = assets / f"{slug}-sign-face.pdf"

    commands: list[tuple[list[str | Path], dict[str, str] | None]] = []
    commands.append(
        (
            [
                sys.executable,
                CANONICAL_BUILD,
                order_ref,
                line1,
                line2,
                "486",
                svg,
            ],
            None,
        )
    )
    node_env = os.environ.copy()
    node_env["NODE_PATH"] = os.pathsep.join(
        (str(NODE_MODULES), str(PNPM_NODE_MODULES))
    )
    commands.append(
        (
            [NODE, Path(__file__).with_name("rasterize_sign.cjs"), svg, png],
            node_env,
        )
    )
    commands.append(
        (
            [
                sys.executable,
                Path(__file__).with_name("make_exact_visual_pdf.py"),
                png,
                pdf,
                "--width-mm",
                "570",
                "--height-mm",
                "125",
            ],
            None,
        )
    )
    print(f"Lane: {LANE}")
    print(f"Output slug: {slug}")
    for command, _ in commands:
        print(f"+ {command_text(command)}")
    if args.dry_run:
        print("Dry run complete; no files written.")
        return

    assets.mkdir(parents=True, exist_ok=True)
    for command, environment in commands:
        run(command, env=environment)
    print(f"Complete: {pdf}")


if __name__ == "__main__":
    main()
