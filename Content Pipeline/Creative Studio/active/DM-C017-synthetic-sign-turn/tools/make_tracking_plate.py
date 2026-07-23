#!/usr/bin/env python3
"""RETIRED helper from the forbidden product-surface tracking workflow."""

from __future__ import annotations

raise RuntimeError(
    "RETIRED: tracking plates must not be used to replace a generated Daisy "
    "Maison sign surface."
)

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
DAISY_NS = "https://daisymaison.co.uk/ns/production"

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)
ET.register_namespace("daisy", DAISY_NS)


def remove_element_by_id(root: ET.Element, element_id: str) -> None:
    for parent in root.iter():
        for child in list(parent):
            if child.attrib.get("id") == element_id:
                parent.remove(child)
                return
            for descendant in child.iter():
                if descendant.attrib.get("id") == element_id:
                    parent.remove(child)
                    return
    raise ValueError(f"Could not find element id {element_id!r}")


def main() -> None:
    raise RuntimeError(
        "RETIRED: tracking plates must not be used to replace a generated "
        "street-sign surface. Reject and regenerate the native video."
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("source_svg", type=Path)
    parser.add_argument("output_svg", type=Path)
    args = parser.parse_args()

    tree = ET.parse(args.source_svg)
    root = tree.getroot()
    remove_element_by_id(root, "line-1")
    remove_element_by_id(root, "signature-heart")
    remove_element_by_id(root, "line-2")

    title = root.find(f"{{{SVG_NS}}}title")
    if title is not None:
        title.text = "DM-C017 lettering-free tracking plate"
    description = root.find(f"{{{SVG_NS}}}desc")
    if description is not None:
        description.text = (
            "Exact approved Large sign silhouette with temporary coloured "
            "tracking fiducials. The fiducials are replaced in post."
        )

    markers = ET.SubElement(
        root,
        f"{{{SVG_NS}}}g",
        {
            "id": "tracking-fiducials",
            "stroke": "#010101",
            "stroke-width": "1.2",
        },
    )
    marker_spec = [
        ("top-left", 55, 28, "#00D9FF"),
        ("top-right", 515, 28, "#FF2ED1"),
        ("bottom-right", 515, 97, "#F6E600"),
        ("bottom-left", 55, 97, "#38FF66"),
    ]
    for marker_id, x, y, fill in marker_spec:
        ET.SubElement(
            markers,
            f"{{{SVG_NS}}}circle",
            {
                "id": f"track-{marker_id}",
                "cx": str(x),
                "cy": str(y),
                "r": "5",
                "fill": fill,
                "data-track-corner": marker_id,
            },
        )
        ET.SubElement(
            markers,
            f"{{{SVG_NS}}}circle",
            {
                "cx": str(x),
                "cy": str(y),
                "r": "1.25",
                "fill": "#010101",
                "stroke": "none",
            },
        )

    args.output_svg.parent.mkdir(parents=True, exist_ok=True)
    tree.write(args.output_svg, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
