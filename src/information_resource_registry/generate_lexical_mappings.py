# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "curies",
#     "fairsharing-client",
#     "ruamel.yaml",
#     "ssslm[gilda-slim]",
# ]
# ///

"""Add xrefs to the YAML file where the catalog is curated.

Run from the root with ``uv run src/information_resource_registry/generate_lexical_mappings.py``,
which automates creating the right environment.
"""

import csv
from pathlib import Path

import ssslm
from curies import NamableReference
from fairsharing_client import load_fairsharing
from ruamel.yaml import YAML

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.parent.resolve()
INFORES_CATALOG_PATH = ROOT.joinpath("infores_catalog.yaml")


def main(write_sssom: bool = False) -> None:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 96  # line wrap
    yaml.indent(mapping=2, sequence=4, offset=2)

    with INFORES_CATALOG_PATH.open() as file:
        records = yaml.load(file)

    fairsharing_grounder = ssslm.make_grounder(
        ssslm.LiteralMapping(
            reference=NamableReference(
                prefix="fairsharing",
                identifier=fairsharing_id,
                name=fairsharing_data["name"],
            ),
            text=fairsharing_data["name"],
        )
        for fairsharing_id, fairsharing_data in load_fairsharing().items()
    )

    rows = []
    for record in records["information_resources"]:
        name = record.get("name")
        if name is None:
            print(f"missing name for {record['id']}")
            continue
        match = fairsharing_grounder.get_best_match(name)
        if match is not None:
            xrefs = record.setdefault("xref", [])
            if match.curie not in xrefs:
                xrefs.append(match.curie)
            rows.append(
                (
                    record["id"],
                    name,
                    match.curie,
                    match.name,
                    "skos:exactMatch",
                    "semapv:LexicalMatching",
                )
            )

    if write_sssom:
        with HERE.joinpath("infores.sssom.tsv").open("w") as file:
            writer = csv.writer(file, delimiter="\t")
            writer.writerow(
                (
                    "subject_id",
                    "subject_label",
                    "object_id",
                    "object_label",
                    "predicate_id",
                    "mapping_justification",
                )
            )
            writer.writerows(rows)

    with INFORES_CATALOG_PATH.open("w") as file:
        file.write("---\n")
        yaml.dump(records, file)


if __name__ == "__main__":
    main()
