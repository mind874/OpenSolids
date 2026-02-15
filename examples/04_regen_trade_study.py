"""Simple regen-focused trade comparison at selected temperatures."""

import opensolids as osl


MATERIAL_IDS = [
    "grcop-84-am",
    "cucrzr-am",
    "alsi10mg-am",
    "in718-am",
]

TEMPERATURES = [293.15, 700.0, 900.0]



def _fmt(value: float | None, width: int = 10, precision: int = 2) -> str:
    if value is None:
        return f"{'-':>{width}}"
    return f"{value:>{width}.{precision}f}"



def main() -> None:
    print("Regen material trade study")
    print("k in W/(m*K), diffusivity in mm^2/s, sigma_y in MPa")
    print()

    for t in TEMPERATURES:
        print(f"T = {t:.2f} K")
        print(f"{'material':24} {'k':>10} {'a_th':>10} {'sigma_y':>10}")

        for material_id in MATERIAL_IDS:
            mat = osl.material(material_id)
            props = set(mat.available_properties())

            k_val = mat.k(t, policy="clamp") if "k" in props else None
            a_val = (
                mat.diffusivity(t, units="mm^2/s", policy="clamp")
                if "diffusivity" in props
                else None
            )
            sy_val = mat.sigma_y(t, units="MPa", policy="clamp") if "sigma_y" in props else None

            print(f"{material_id:24} {_fmt(k_val)} {_fmt(a_val)} {_fmt(sy_val)}")

        print()


if __name__ == "__main__":
    main()
