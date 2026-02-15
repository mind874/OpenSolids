"""Simple regen-focused trade comparison at selected temperatures."""

import opensolids as osl


MATERIAL_IDS = [
    "ntrs:20070017311:grcop-84",
    "ntrs:20160001501:cucrzr",
    "ntrs:20190030979:alsi10mg",
    "mil-hdbk-5:H:inconel-718",
]

TEMPERATURES = [293.15, 700.0, 900.0]



def _fmt(value: float | None, width: int = 10, precision: int = 2) -> str:
    if value is None:
        return f"{'-':>{width}}"
    return f"{value:>{width}.{precision}f}"



def main() -> None:
    print("Regen material trade study")
    print("k in W/(m*K), sigma_y in MPa")
    print()

    for t in TEMPERATURES:
        print(f"T = {t:.2f} K")
        print(f"{'material':42} {'k':>10} {'sigma_y':>10}")

        for material_id in MATERIAL_IDS:
            mat = osl.material(material_id)
            props = set(mat.available_properties())

            k_val = mat.k(t, policy="clamp") if "k" in props else None
            sy_val = mat.sigma_y(t, units="MPa", policy="clamp") if "sigma_y" in props else None

            print(f"{material_id:42} {_fmt(k_val)} {_fmt(sy_val)}")

        print()


if __name__ == "__main__":
    main()
