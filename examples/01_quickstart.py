"""Basic OpenSolids usage."""

import opensolids as osl


def main() -> None:
    mat = osl.material("nist-cryo:aluminum-6061-t6")

    print(f"Material: {mat.id}")
    print(f"Name: {mat.name}")
    print(f"Available properties: {', '.join(mat.available_properties())}")
    print()

    k_300 = mat.k(300.0)
    E_vals = mat.E([77.0, 150.0, 293.15], units="GPa")
    eps_120 = mat.eps_th(120.0, T_ref=293.15)

    print(f"k(300 K) = {k_300:.3f} W/(m*K)")
    print(f"E([77,150,293.15] K) = {E_vals} GPa")
    print(f"eps_th(120 K, T_ref=293.15 K) = {eps_120:.6e}")


if __name__ == "__main__":
    main()
