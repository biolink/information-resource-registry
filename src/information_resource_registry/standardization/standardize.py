#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List, Optional
from collections.abc import Mapping, Sequence

import click
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import FoldedScalarString, ScalarString

# Desired key order for the top-level mapping (anything not listed is appended alphabetically)
TOP_LEVEL_ORDER = [
    "information_resources",
]

def reorder_mapping(m: CommentedMap, priority_order: List[str]) -> CommentedMap:
    """
    Reorder a ruamel CommentedMap: first keys in priority_order (if present),
    then any remaining keys in alphabetical order (stable).
    NOTE: We intentionally do NOT copy m.ca.items[...] (per-key comments), because transplanting
    those associations can turn keys into 'complex keys' and break dumps/parsing.
    """
    if not isinstance(m, CommentedMap):
        return m

    present = list(m.keys())
    ordered_keys = [k for k in priority_order if k in m]
    remaining = sorted(k for k in present if k not in priority_order)

    new = CommentedMap()
    for k in ordered_keys + remaining:
        new[k] = m[k]
        # Do NOT copy: new.ca.items[k] = m.ca.items[k]

    # Copy map-level comments safely
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


def process_information_resources(node: CommentedSeq, sort_xrefs: bool, dedupe_xrefs: bool, ordered_slots: List[str]):
    """
    Reorder keys for each information resource and optionally sort/dedupe xref lists.
    Preserve sequence-level comments where feasible (not per-element).
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
                xrefs = sorted(xrefs, key=lambda s: str(s))
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

        # Reorder keys according to schema-provided slots, then append any extras alphabetically
        # ordered_slots may miss some ad-hoc keys; reorder_mapping handles that.
        new_item = reorder_mapping(item, ordered_slots)
        node[i] = new_item


# ---------- YAML sanitization to avoid RepresenterError ----------

YAML_PRIMITIVES = (str, int, float, bool, type(None), ScalarString)

def _to_plain_key(k):
    # Allow plain scalars; otherwise stringify
    if isinstance(k, (str, ScalarString, int, float, bool)) or k is None:
        return k
    # Convert any other object to string (e.g., SlotDefinitionName from LinkML)
    return str(k)

def _to_plain_value(v):
    # Keep YAML primitives; stringify common oddballs (Path, etc.)
    if isinstance(v, YAML_PRIMITIVES):
        return v
    if isinstance(v, Path):
        return str(v)
    return v

def sanitize_for_yaml(obj):
    """Recursively coerce keys to YAML-friendly scalars and sanitize values.
       Preserves map/seq-level comments and block scalars."""
    if isinstance(obj, CommentedMap):
        new = CommentedMap()
        for old_k in list(obj.keys()):
            v = obj[old_k]
            k = _to_plain_key(old_k)
            # We do NOT copy per-key ca.items[...] (see note above)
            new[k] = sanitize_for_yaml(v)
        if getattr(obj, "ca", None):
            if obj.ca.comment is not None:
                new.ca.comment = obj.ca.comment
            if obj.ca.end is not None:
                new.ca.end = obj.ca.end
        return new

    if isinstance(obj, dict):
        return { _to_plain_key(k): sanitize_for_yaml(v) for k, v in obj.items() }

    if isinstance(obj, CommentedSeq):
        new_seq = CommentedSeq([sanitize_for_yaml(x) for x in list(obj)])
        if getattr(obj, "ca", None):
            if obj.ca.comment is not None:
                new_seq.ca.comment = obj.ca.comment
            if obj.ca.end is not None:
                new_seq.ca.end = obj.ca.end
        return new_seq

    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray)):
        return [sanitize_for_yaml(x) for x in obj]

    return _to_plain_value(obj)


def get_all_slots_from_schema(schema_path: Optional[Path]) -> List[str]:
    """
    Load the schema and return slot names for InformationResource if present;
    otherwise return an empty list (we'll fall back to alphabetical).
    """
    if schema_path is None:
        return []
    try:
        from linkml_runtime.utils.schemaview import SchemaView
        sv = SchemaView(schema_path)
        # Prefer class-specific ordering if the class exists
        if sv.get_class("InformationResource"):
            # Ensure we return plain strings, not SlotDefinitionName objects
            return [str(slot) for slot in sv.class_slots("InformationResource")]
        # Fallback: all slot names (also convert to strings)
        return [str(slot) for slot in sv.all_slots()]
    except Exception:
        # If schema processing fails, return empty list to fall back to existing order
        return []


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("input_path", type=click.Path(path_type=Path, exists=True, dir_okay=False))
@click.option(
    "-o", "--output", "output_path",
    type=click.Path(path_type=Path, dir_okay=False),
    default=None,
    help="Write to this file. If omitted and not --in-place, prints to stdout.",
)
@click.option(
    "-s", "--schema", "schema_path",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    default=None,
    help="Reference to LinkML schema for the registry.",
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
def main(input_path: Path, output_path: Optional[Path], schema_path: Optional[Path], in_place: bool,
         sort_xrefs: bool, dedupe_xrefs: bool, width: int):
    """
    Read a YAML file and standardize indentation, key ordering, and some scalar styles.
    """
    if in_place and output_path:
        raise click.UsageError("Use either --in-place or --output, not both.")

    yaml = YAML(typ="rt")  # round-trip to preserve comments/anchors
    yaml.preserve_quotes = True
    yaml.width = width
    yaml.explicit_start = True  # Add --- at the start of the document
    # Standardize indentation: 2 spaces for maps, 2 for sequences, 0 offset for sequence dashes
    yaml.indent(mapping=2, sequence=2, offset=0)
    # Avoid anchors/aliases in output (safer for catalogs)
    yaml.representer.ignore_aliases = lambda *_: True

    with Path(input_path).open("r", encoding="utf-8") as f:
        data = yaml.load(f)

    # Ensure we have a mapping at top-level
    if isinstance(data, CommentedMap):
        # Reorder top-level keys
        data = reorder_mapping(data, TOP_LEVEL_ORDER)

        # Process information_resources list
        ir = data.get("information_resources")
        if isinstance(ir, CommentedSeq):
            ordered_slots = get_all_slots_from_schema(Path(schema_path) if schema_path else None)
            process_information_resources(ir, sort_xrefs=sort_xrefs, dedupe_xrefs=dedupe_xrefs, ordered_slots=ordered_slots)

            # Sort the information_resources list by id
            sorted_ir = sorted(ir, key=lambda x: x.get('id', '') if isinstance(x, dict) else '')
            # Replace items in the original sequence to preserve CommentedSeq type
            ir.clear()
            ir.extend(sorted_ir)

    # Final safety: sanitize entire structure before dumping
    data = sanitize_for_yaml(data)

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
