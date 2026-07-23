#!/usr/bin/env python3
"""Scaffold the validated native white wedding-sign Reel workflow.

This tool prepares exact artwork, stage prompts, reference slots and human
approval gates. It never submits paid generation, edits a moving sign surface,
reads Shopify itself or publishes. It is deliberately blocked for coloured or
non-wedding sign families.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


LANE = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
PROMPT_CASE = (
    WORKSPACE
    / "Content Pipeline"
    / "Creative Studio"
    / "prompts"
    / "wedding-signs"
    / "cases"
    / "DM-C017-JANNAWAY"
)
ASSET_BUILDER = Path(__file__).with_name("build_next_reel.py")
RUNS_DIR = LANE / "working" / "runs"

VALIDATED_PROMPTS = {
    "01-product-print-edit.txt": PROMPT_CASE / "01-validated-product-print-edit.txt",
    "02-synthetic-max-hero.txt": PROMPT_CASE / "02-validated-synthetic-max-hero.txt",
    "03-white-back-start.txt": PROMPT_CASE / "03-validated-white-back-start.txt",
    "04-native-video.txt": PROMPT_CASE / "04-validated-native-video.txt",
}


def checked_text(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{label} cannot be blank")
    if "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be one line")
    if len(value) > 160:
        raise ValueError(f"{label} is unexpectedly long")
    return value


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-")
    if not slug:
        raise ValueError("slug must contain a letter or number")
    return slug[:80]


def adapt_prompt(source: str, line1: str, line2: str, slug: str) -> str:
    # Replace exact phrases before the mixed-case case name.
    adapted = source.replace("MR & MRS JANNAWAY", line1)
    adapted = adapted.replace(
        "WHEN TWO NAMES BECOME ONE 15TH AUGUST 2026",
        line2,
    )
    adapted = adapted.replace("Jannaway", slug)
    return adapted


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare a new no-overlay white wedding-sign Reel run."
    )
    parser.add_argument("--line1", required=True)
    parser.add_argument("--line2", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument(
        "--demand-source",
        default="shopify-read-only-demand",
        help="Display-safe provenance label; never include address/contact/payment data.",
    )
    parser.add_argument(
        "--real-master",
        help="Real Daisy Maison front photo to use as manufactured-object authority.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate dependencies and print the plan without writing.",
    )
    parser.add_argument(
        "--confirm-white-wedding-sign",
        action="store_true",
        help=(
            "Required scope gate: confirms this is the validated white wedding-sign "
            "family, not a coloured or non-wedding product."
        ),
    )
    args = parser.parse_args()

    line1 = checked_text(args.line1, "line1")
    line2 = checked_text(args.line2, "line2")
    slug = safe_slug(args.slug)
    demand_source = checked_text(args.demand_source, "demand-source")
    if not args.confirm_white_wedding_sign:
        parser.error(
            "--confirm-white-wedding-sign is required. Coloured and non-wedding "
            "signs are not validated by this workflow."
        )

    missing = [
        str(path)
        for path in [ASSET_BUILDER, *VALIDATED_PROMPTS.values()]
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError("Missing validated dependency:\n" + "\n".join(missing))

    asset_command = [
        sys.executable,
        str(ASSET_BUILDER),
        "--line1",
        line1,
        "--line2",
        line2,
        "--slug",
        slug,
        "--order-ref",
        demand_source,
    ]
    if args.dry_run:
        asset_command.append("--dry-run")
        print(
            json.dumps(
                {
                    "slug": slug,
                    "line1": line1,
                    "line2": line2,
                    "demand_source": demand_source,
                    "real_master": args.real_master,
                    "validated_cost_baseline_credits": 90,
                    "validated_product_family": "white-wedding-sign",
                    "human_gates": [
                        "product image",
                        "synthetic-Max hero",
                        "plain-white reverse",
                        "untouched native video",
                        "publishing",
                    ],
                    "paid_submission": False,
                    "product_surface_overlay": False,
                },
                indent=2,
            )
        )
        subprocess.run(asset_command, check=True)
        print("Dry run complete; no files written and no paid job submitted.")
        return

    run_dir = RUNS_DIR / slug
    if run_dir.exists():
        raise FileExistsError(
            f"Run already exists: {run_dir}. Choose a new slug; nothing was overwritten."
        )

    subprocess.run(asset_command, check=True)
    prompts_dir = run_dir / "prompts"
    prompts_dir.mkdir(parents=True)
    for output_name, source_path in VALIDATED_PROMPTS.items():
        source = source_path.read_text(encoding="utf-8")
        adapted = adapt_prompt(source, line1, line2, slug)
        (prompts_dir / output_name).write_text(adapted, encoding="utf-8")

    manifest = {
        "method": "wedding-sign-engineering-prompt-workflow-v1",
        "validated_product_family": "white-wedding-sign",
        "excluded_unvalidated_families": [
            "coloured-sign-black-text",
            "coloured-sign-coloured-text",
            "non-wedding-sign",
        ],
        "source_case": "DM-C017-JANNAWAY-v03",
        "slug": slug,
        "line1": line1,
        "line2": line2,
        "demand_source": demand_source,
        "artwork": {
            "svg": f"assets/{slug}-sign-face.svg",
            "png": f"assets/{slug}-sign-face.png",
            "pdf": f"assets/{slug}-sign-face.pdf",
        },
        "reference_slots": {
            "real_front_master": args.real_master,
            "approved_product_image": None,
            "synthetic_max_identity": None,
            "approved_hero_end": None,
            "approved_white_back_start": None,
            "real_front_to_edge": None,
            "real_back_to_edge": None,
            "real_white_back": None,
            "privacy_cropped_real_turn": None,
        },
        "human_gates": {
            "product_image": False,
            "synthetic_max_hero": False,
            "plain_white_reverse": False,
            "untouched_native_video": False,
            "publishing": False,
        },
        "generation_baseline": {
            "product_candidates": 4,
            "hero_candidates": 4,
            "white_back_candidates": 4,
            "video_candidates": 1,
            "image_model": "nano_banana_flash",
            "video_model": "seedance_2_0",
            "video_mode": "std",
            "video_resolution": "1080p",
            "video_bitrate": "high",
            "video_duration_seconds": 8,
            "video_aspect_ratio": "9:16",
            "generated_audio": False,
            "validated_cost_baseline_credits": 90,
        },
        "paid_video_submit_allowed": False,
        "product_surface_overlay_allowed": False,
        "publishes": False,
    }
    (run_dir / "run-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (run_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {slug} native white wedding-sign Reel",
                "",
                "Status: awaiting human-approved product image.",
                "",
                "Follow `Content Pipeline/Creative Studio/WEDDING_SIGN_ENGINEERING_PROMPT_WORKFLOW.md`.",
                "Fill reference slots and record hashes after each human approval.",
                "Do not submit video until the first three human gates pass.",
                "Do not overlay or repair the moving product surface.",
                "Do not publish without Max's explicit publishing approval.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Prepared: {run_dir}")
    print("Paid submission: disabled")
    print("Product-surface overlay: disabled")


if __name__ == "__main__":
    main()
