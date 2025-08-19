#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List, Optional

import click
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import FoldedScalarString

# Desired key order for the top-level mapping (anything not listed is appended alphabetically)
TOP_LEVEL_ORDER = [
    "information_resources",
]

# Desired key order for each item in `information_resources`
INFORES_ORDER = [
    "id",
    "status",
    "name",
    "xref",
    "description",
    "knowledge_level",
    "agent_type",
]


def reorder_mapping(m: CommentedMap, priority_order: List[str]) -> CommentedMap:
    """
    Reorder a ruamel CommentedMap: first keys in priority_order (if present),
    then any remaining keys in alphabetical order (stable). Preserve comments.
    """
    if not isinstance(m, CommentedMap):
        return m

    present = list(m.keys())
    ordered_keys = [k for k in priority_order if k in m]
    remaining = sorted(k for k in present if k not in priority_order)

    new = CommentedMap()
    for k in ordered_keys + remaining:
        new[k] = m[k]
        # carry over per-key comments
        if getattr(m, "ca", None) and m.ca.items.get(k):
            new.ca.items[k] = m.ca.items[k]

    # copy map-level comments (NOTE: .ca is read-only; copy fields instead)
    if getattr(m, "ca", None):
        if m.ca.comment is not None:
            new.ca.comment = m.ca.comment
        if m.ca.end is not None:
            new.ca.end = m.ca.end

    return new


def normalize_description_scalar(v):
    """
    Ensure description is a folded block scalar (>-like), preserving text.
    """
    if isinstance(v, str) and not isinstance(v, FoldedScalarString):
        return FoldedScalarString(v)
    return v


def process_information_resources(node: CommentedSeq, sort_xrefs: bool, dedupe_xrefs: bool):
    """
    Reorder keys for each information resource and optionally sort/dedupe xref lists.
    Preserve sequence-level comments where feasible.
    """
    if not isinstance(node, CommentedSeq):
        return

    for i, item in enumerate(node):
        if not isinstance(item, CommentedMap):
            continue

        # Normalize xref list
        if "xref" in item and isinstance(item["xref"], (list, CommentedSeq)):
            old_seq = item["xref"]
            xrefs = list(old_seq)
            if dedupe_xrefs:
                # preserve order while deduping
                seen = set()
                xrefs = [x for x in xrefs if not (x in seen or seen.add(x))]
            if sort_xrefs:
                xrefs = sorted(xrefs)
            new_seq = CommentedSeq(xrefs)

            # carry over sequence-level comments (can't bulk-assign .ca)
            if isinstance(old_seq, CommentedSeq) and getattr(old_seq, "ca", None):
                if old_seq.ca.comment is not None:
                    new_seq.ca.comment = old_seq.ca.comment
                if old_seq.ca.end is not None:
                    new_seq.ca.end = old_seq.ca.end
                # per-element inline comments are not preserved if order changed

            item["xref"] = new_seq

        # Normalize description to folded block scalar
        if "description" in item:
            item["description"] = normalize_description_scalar(item["description"])

        # Reorder keys
        new_item = reorder_mapping(item, INFORES_ORDER)
        node[i] = new_item


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("input_path", type=click.Path(path_type=Path, exists=True, dir_okay=False))
@click.option(
    "-o", "--output", "output_path",
    type=click.Path(path_type=Path, dir_okay=False),
    default=None,
    help="Write to this file. If omitted and not --in-place, prints to stdout.",
)
@click.option(
    "-i", "--in-place",
    is_flag=True,
    help="Overwrite the input file with standardized YAML."
)
@click.option(
    "--sort-xrefs/--no-sort-xrefs",
    default=True,
    show_default=True,
    help="Sort entries under 'xref' lists."
)
@click.option(
    "--dedupe-xrefs/--no-dedupe-xrefs",
    default=True,
    show_default=True,
    help="De-duplicate entries under 'xref' lists (preserves the first occurrence)."
)
@click.option(
    "--width",
    default=88,
    show_default=True,
    help="Preferred line width for scalars."
)
def main(input_path: Path, output_path: Optional[Path], in_place: bool,
         sort_xrefs: bool, dedupe_xrefs: bool, width: int):
    """
    Read a YAML file and standardize indentation, key ordering, and some scalar styles.
    """
    if in_place and output_path:
        raise click.UsageError("Use either --in-place or --output, not both.")

    yaml = YAML(typ="rt")  # round-trip to preserve comments/anchors
    yaml.preserve_quotes = True
    yaml.width = width
    # Standardize indentation: 2 spaces for maps & sequences, 2 offset for sequence dashes
    yaml.indent(mapping=2, sequence=2, offset=2)

    with Path(input_path).open("r", encoding="utf-8") as f:
        data = yaml.load(f)

    # Ensure we have a mapping at top-level
    if isinstance(data, CommentedMap):
        # Reorder top-level keys
        data = reorder_mapping(data, TOP_LEVEL_ORDER)

        # Process information_resources list
        ir = data.get("information_resources")
        if isinstance(ir, CommentedSeq):
            process_information_resources(ir, sort_xrefs=sort_xrefs, dedupe_xrefs=dedupe_xrefs)

    # Decide output target
    if in_place:
        target = Path(input_path)
    elif output_path:
        target = Path(output_path)
    else:
        target = None

    if target:
        with target.open("w", encoding="utf-8") as f:
            yaml.dump(data, f)
    else:
        yaml.dump(data, sys.stdout)


if __name__ == "__main__":
    main()
