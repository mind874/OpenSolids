from __future__ import annotations

import argparse
import json
from pathlib import Path

from opensolids.providers.mil_hdbk_5.import_local import import_mil_hdbk_5_pdf
from opensolids.providers.nist_cryo.sync import sync_nist_cryo
from opensolids.providers.ntrs_openapi.sync import sync_ntrs



def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]



def _default_pack_dir(name: str) -> Path:
    return _repo_root() / "packages" / name / "src" / name



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opensolids")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="Sync provider datasets")
    sync_sub = sync_parser.add_subparsers(dest="provider", required=True)

    nist = sync_sub.add_parser("nist-cryo", help="Sync NIST cryogenic materials")
    nist.add_argument("--output", type=Path, default=_default_pack_dir("opensolids_data_nist_cryo"))
    nist.add_argument("--max-materials", type=int, default=None)

    ntrs = sync_sub.add_parser("ntrs", help="Sync NTRS metadata and redistributions")
    ntrs.add_argument("--since", required=True, help="YYYY-MM-DD")
    ntrs.add_argument("--output", type=Path, default=_default_pack_dir("opensolids_data_ntrs_public"))
    ntrs.add_argument(
        "--citation-id",
        dest="citation_ids",
        action="append",
        default=[],
        help="Curated citation id to ingest as source metadata (repeatable)",
    )

    import_parser = subparsers.add_parser("import", help="Import local data into packs")
    import_sub = import_parser.add_subparsers(dest="provider", required=True)

    mil = import_sub.add_parser("mil-hdbk-5", help="Import MIL-HDBK-5 data from local PDF")
    mil.add_argument("--pdf", required=True, type=Path)
    mil.add_argument("--output", type=Path, default=_default_pack_dir("opensolids_data_mil_hdbk_5"))
    mil.add_argument("--revision", default="H")
    mil.add_argument("--material-slug", default="al-6061-t6")
    mil.add_argument("--material-name", default="Aluminum 6061-T6")
    mil.add_argument("--condition", default="T6")
    mil.add_argument("--property-key", default="sigma_y")
    mil.add_argument("--units", default="Pa")
    mil.add_argument("--basis", default="B-basis")
    mil.add_argument("--product-form", default=None)
    mil.add_argument("--direction", default=None)

    return parser



def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "sync" and args.provider == "nist-cryo":
        manifest = sync_nist_cryo(args.output, max_materials=args.max_materials)
        print(json.dumps(manifest, indent=2))
        return 0

    if args.command == "sync" and args.provider == "ntrs":
        manifest = sync_ntrs(
            args.output,
            since=args.since,
            curated_citation_ids=args.citation_ids,
        )
        print(json.dumps(manifest, indent=2))
        return 0

    if args.command == "import" and args.provider == "mil-hdbk-5":
        manifest = import_mil_hdbk_5_pdf(
            args.pdf,
            args.output,
            revision=args.revision,
            material_slug=args.material_slug,
            material_name=args.material_name,
            condition=args.condition,
            property_key=args.property_key,
            units=args.units,
            basis=args.basis,
            product_form=args.product_form,
            direction=args.direction,
        )
        print(json.dumps(manifest, indent=2))
        return 0

    parser.error("Unhandled command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
