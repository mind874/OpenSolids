from __future__ import annotations

from pathlib import Path

from opensolids.providers.base import LocalDataPackProvider


class MilHdbk5Provider(LocalDataPackProvider):
    def __init__(self):
        repo_root = Path(__file__).resolve().parents[4]
        fallback = (
            repo_root
            / "packages"
            / "opensolids_data_mil_hdbk_5"
            / "src"
            / "opensolids_data_mil_hdbk_5"
        )
        super().__init__(
            name="mil-hdbk-5",
            version="0.3.0",
            package_name="opensolids_data_mil_hdbk_5",
            fallback_path=fallback,
        )
