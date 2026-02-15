from __future__ import annotations

from pathlib import Path

from opensolids.providers.base import LocalDataPackProvider

from .client import NTRSOpenAPIClient


class NTRSOpenAPIProvider(LocalDataPackProvider):
    def __init__(self, client: NTRSOpenAPIClient | None = None):
        repo_root = Path(__file__).resolve().parents[4]
        fallback = (
            repo_root
            / "packages"
            / "opensolids_data_ntrs_public"
            / "src"
            / "opensolids_data_ntrs_public"
        )
        super().__init__(
            name="ntrs",
            version="0.2.2",
            package_name="opensolids_data_ntrs_public",
            fallback_path=fallback,
        )
        self.client = client or NTRSOpenAPIClient()

    def check_redistributions(self, since_date: str) -> dict:
        return self.client.get_redistributions(since_date)
