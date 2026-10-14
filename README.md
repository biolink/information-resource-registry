# information-resource-registry

The Information Resource Registry is a catalog of the data sources, knowledge providers, and
autonomous reasoning agents that participate in the NCATS Biomedical Data Translator system. Each
entry ("stanza") in [`infores_catalog.yaml`](infores_catalog.yaml) describes one information
resource: its identifier, a human-readable name, and metadata about what kind of knowledge it
provides and where it fits in the Translator data flow.

The identifiers minted here (CURIEs with the `infores:` prefix, e.g. `infores:chembl`) are used
throughout Translator and Biolink Model tooling to record the provenance of knowledge — every edge
in a Translator knowledge graph can say which resource it came from by pointing at an infores CURIE.

## Website

[https://biolink.github.io/information-resource-registry](https://biolink.github.io/information-resource-registry)

## Adding a new information resource

To register a new resource, add a stanza to [`infores_catalog.yaml`](infores_catalog.yaml) and open
a pull request. If you would rather not edit YAML, you can also open an issue describing the
resource and someone will add it for you.

A minimal, complete stanza looks like this:

```yaml
  - status: released
    name: My New Resource
    id: infores:my-new-resource
    description: >-
      A short, plain-language description of what this resource is and what
      kind of knowledge it provides.
    xref:
      - https://w3id.org/my-new-resource
    knowledge_level: knowledge_assertion
    agent_type: manual_agent
```

### Required fields

Every stanza must have:

- **`id`** — the infores CURIE for the resource (see naming conventions below). Once merged, this
  identifier is permanent: it must never be changed or deleted, only deprecated.
- **`name`** — a human-readable display name for the resource.
- **`status`** — one of `released`, `deprecated`, `draft`, or `modified`. In practice almost every
  entry should be `released` (in active use) or `deprecated` (no longer in use, kept for
  provenance).

If the status is `released`, two more fields are required:

- **`knowledge_level`** — a broad categorization of the kind of knowledge the resource provides.
  One of: `knowledge_assertion` (curated assertions made by human experts),
  `statistical_association` (associations computed from clinical or omics data), `prediction`
  (computational predictions made without human review), `observation` (reported observations of
  phenomena), `logical_entailment` (conclusions that follow logically from established facts),
  `mixed` (a combination of the above), `other`, or `not_provided`.
- **`agent_type`** — who or what produces the knowledge. One of: `manual_agent` (a human curator
  or expert), `automated_agent` (software producing knowledge without human involvement, with the
  more specific subtypes `data_analysis_pipeline`, `computational_model`, `text_mining_agent`, and
  `image_processing_agent`), `manual_validation_of_automated_agent` (automated output that a human
  reviews and approves), or `not_provided`.

### Optional fields

- **`description`** — a free-text description of the resource. Strongly encouraged.
- **`xref`** — one or more URLs or CURIEs pointing to the resource itself or to a record about it
  (see the guidance on persistent URLs below). Strongly encouraged.
- **`synonym`** — alternate names the resource is known by.
- **`consumes`** / **`consumed_by`** — lists of infores CURIEs describing data flow: the resources
  this one ingests knowledge from, and the resources that ingest knowledge from this one. If you
  add resource A to B's `consumes`, please also add B to A's `consumed_by` so the two views of the
  relationship stay in sync.

### Naming conventions for identifiers

- Identifiers are CURIEs with the `infores:` prefix, e.g. `infores:my-new-resource`.
- Use short, readable, lowercase strings with words separated by dashes (`-`). These identifiers
  appear in user-facing applications, so favor readability over abbreviation.
- Each SmartAPI-registered Translator API gets its own infores identifier, and so does each
  upstream source it aggregates knowledge from. When in doubt, mint separate identifiers rather
  than overloading one.

A GitHub Action automatically standardizes the formatting, field ordering and entry ordering of
`infores_catalog.yaml` on pull requests from branches in this repository, and the test suite
validates the catalog against the
[LinkML schema](src/information_resource_registry/schema/information_resource_registry.yaml) — so
don't worry about getting the formatting perfect; do make sure the required fields are present.
Pull requests from forks are not auto-standardized (the Action cannot push to a fork), so if you
are working from a fork, run `make standardize-data` yourself before opening the PR. See
[Checking your changes](#checking-your-changes) for how to run the same checks locally.

## Why identifiers must persist (and the deprecation protocol)

Infores CURIEs are provenance identifiers. Once an identifier is minted here, it gets baked into
downstream artifacts that this repository does not control: knowledge graph edges, TRAPI query
responses, archived analyses, publications, and the configuration of other Translator components.
If an identifier were deleted or renamed in place, every one of those existing references would
silently break, and the provenance trail for previously produced knowledge would be lost.

For that reason, **entries in this catalog are never deleted, and an `id` is never edited.**
Instead:

- **A resource that is retired or no longer in use** keeps its stanza, and its `status` is set to
  `deprecated`. Downstream applications stop serving deprecated resources, but historical
  references to the identifier continue to resolve to a record explaining what it was.
- **A resource that needs a new identifier** (for example, a rename to reduce confusion) is
  treated as a brand-new entry: add a new stanza with the new `id` carrying the full metadata, and
  set the old stanza's `status` to `deprecated`. Keep the old stanza's `name`, `knowledge_level`,
  and `agent_type`, and add a `description` pointing readers to the replacement identifier, e.g.
  "Deprecated identifier; this resource is now identified as infores:new-id." Then update every
  `consumes` and `consumed_by` reference in the catalog to point at the new identifier, so the
  deprecated identifier is no longer part of the active data-flow graph.

This two-step protocol (deprecate the old, mint the new) gives downstream applications a window to
migrate their records at their own pace while keeping every identifier ever minted resolvable.

## Choosing xrefs that will keep resolving

The best `xref` is one that will still work years from now. Plain links to a project's current web
host tend to rot: sites get reorganized, hosting moves, and lab pages disappear. To give an xref
the best chance of resolving indefinitely, prefer **persistent URLs (PURLs)** — stable web
addresses maintained by a redirection service, which can be re-pointed when the underlying host
moves without the published link ever changing:

- **[w3id.org](https://w3id.org/)** — the community-run permanent identifier service used by
  Biolink and much of the semantic web community (e.g. `https://w3id.org/biolink/`).
- **[purl.obolibrary.org](https://obofoundry.org/)** — OBO Foundry PURLs, the canonical form for
  ontologies (e.g. `http://purl.obolibrary.org/obo/mondo.owl`).
- **DOIs** (`https://doi.org/...`) — for resources with a published, citable form.
- **[identifiers.org](https://identifiers.org/) / [bioregistry.io](https://bioregistry.io/)** —
  resolver-backed links for databases with registered prefixes.
- **[FAIRsharing](https://fairsharing.org/)** records — curated, stable descriptions of standards
  and databases (e.g. `https://fairsharing.org/FAIRsharing.mewhad` for ClinicalTrials.gov).

If no PURL exists for a resource, use the most canonical, top-level landing page available (the
resource's own home page rather than a deep link into its documentation), and consider registering
a PURL with one of the services above — w3id.org accepts community submissions via a simple pull
request.

## Repository Structure

* [infores_catalog.yaml](infores_catalog.yaml) - the registry itself (edit this)
* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/) - source files (edit these)
  * [information_resource_registry](src/information_resource_registry)
    * [schema](src/information_resource_registry/schema) -- LinkML schema
      (edit this)

## Checking your changes

Before opening a pull request that edits `infores_catalog.yaml`, you can confirm locally that
downstream tools will still be able to read the catalog after your change.

### How downstream tools get the catalog

Downstream tools read the catalog in one of these forms, so a change has to survive all of them:

- **`infores_catalog.yaml`** — read straight from this repository or from the website at
  <https://biolink.github.io/information-resource-registry/infores_catalog.yaml>.
- **GitHub release assets** — every [release](https://github.com/biolink/information-resource-registry/releases)
  attaches `infores_catalog.yaml`, `infores_catalog.json`, `infores_catalog.tsv` and
  `infores_catalog.jsonl` (one JSON object per resource). They are generated from the YAML by
  `make create_release_extras`, which uses `linkml-convert` with the LinkML schema. A stanza that
  doesn't fit the schema can therefore break the JSON, TSV and JSONL files even when the YAML
  itself parses.

### Setting up

The checks run through [uv](https://docs.astral.sh/uv/). Install the dependencies with:

```bash
uv sync --python 3.12
```

Pass `--python` explicitly: uv otherwise uses the newest Python it can find, and on Python 3.14 the
install fails because a dependency (`gilda`) pins `scikit-learn==1.4.2`, which cannot be built
there. CI tests on Python 3.10, 3.11 and 3.12.

### The checks

| Command | What it checks | Run in CI? |
| --- | --- | --- |
| `make test_pr` | The checks CI runs on every pull request: `linkml-validate` against the schema (required fields, allowed enum values such as `status`, `knowledge_level` and `agent_type`), `pytest` (catalog rules not expressible in the schema), `codespell`, and `yamllint` (YAML syntax, indentation, duplicate keys). | Yes, on every PR |
| `make check_standardized` | That the file is already in standard form: entries sorted by `id`, fields in schema order, `xref` lists sorted and de-duplicated, descriptions as folded blocks. It runs the standardizer on a copy and fails if anything would change. Fix it with `make standardize-data`, which rewrites the file in place. | Only via the auto-standardize Action, which skips PRs from forks |
| `make create_release_extras` | That the catalog converts cleanly to the JSON, TSV and JSONL release files. It writes them to `release-output/` (git-ignored). | Only when a release is created |
| `make test` | Everything in `make test_pr`, plus `check_standardized` and `check_urls`. `check_urls` requests every `xref` URL with a pause between requests, so it takes a long time; a weekly Action runs it on `main`. | Weekly, for URLs |

For an ordinary catalog edit, this is enough:

```bash
make test_pr
make check_standardized   # if it fails: make standardize-data, then commit the result
make create_release_extras
jq '.information_resources[] | select(.id == "infores:my-new-resource")' release-output/infores_catalog.json
```

The last command should print your stanza with every field you wrote. If a field is missing or
mangled, a downstream tool reading the JSON release won't see it either.

### What the checks don't catch

- **Dangling data-flow references.** Nothing checks that every CURIE in `consumes` or
  `consumed_by` is an `id` in the catalog, or that the two directions agree with each other.
  Check by hand any reference you add.
- **Duplicate names.** Two stanzas can share a `name`. That is expected for a deprecated entry
  and its replacement, but anywhere else it makes resources hard to tell apart in user-facing tools.

### Other make targets

* `make all`: generate the project artefacts (`project/`) and the documentation site
* `make testdoc`: build the documentation site and serve it locally

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
