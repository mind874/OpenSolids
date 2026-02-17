from __future__ import annotations

from pathlib import Path

from opensolids.providers.base import LocalDataPackProvider


class CuratedPublicProvider(LocalDataPackProvider):
    def __init__(self):
        repo_root = Path(__file__).resolve().parents[4]
        fallback = (
            repo_root
            / "packages"
            / "opensolids_data_curated_public"
            / "src"
            / "opensolids_data_curated_public"
        )
        super().__init__(
            name="curated-public",
            version="0.3.5",
            package_name="opensolids_data_curated_public",
            fallback_path=fallback,
        )
