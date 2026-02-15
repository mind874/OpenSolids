from __future__ import annotations

from pathlib import Path

from opensolids.providers.base import LocalDataPackProvider


class NISTCryoProvider(LocalDataPackProvider):
    def __init__(self):
        repo_root = Path(__file__).resolve().parents[4]
        fallback = (
            repo_root
            / "packages"
            / "opensolids_data_nist_cryo"
            / "src"
            / "opensolids_data_nist_cryo"
        )
        super().__init__(
            name="nist-cryo",
            version="0.3.1",
            package_name="opensolids_data_nist_cryo",
            fallback_path=fallback,
        )
