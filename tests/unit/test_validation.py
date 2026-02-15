import json
from pathlib import Path

from opensolids.validation import validate_material_record



def test_sample_data_records_validate():
    base_dirs = [
        Path("packages/opensolids_data_nist_cryo/src/opensolids_data_nist_cryo/materials"),
        Path("packages/opensolids_data_ntrs_public/src/opensolids_data_ntrs_public/materials"),
        Path("packages/opensolids_data_mil_hdbk_5/src/opensolids_data_mil_hdbk_5/materials"),
    ]

    for base in base_dirs:
        for fp in base.glob("*.json"):
            validate_material_record(json.loads(fp.read_text()))
