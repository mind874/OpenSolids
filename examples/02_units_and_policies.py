"""Unit conversion and out-of-range policy examples."""

import opensolids as osl


def main() -> None:
    strength_mat = osl.material("in718-am")
    thermal_mat = osl.material("cucrzr-am")

    t = 293.15
    sy_pa = strength_mat.sigma_y(t)
    sy_mpa = strength_mat.sigma_y(t, units="MPa")

    print(f"in718-am sigma_y({t} K) = {sy_pa:.1f} Pa")
    print(f"in718-am sigma_y({t} K) = {sy_mpa:.2f} MPa")
    print(f"cucrzr-am diffusivity({t} K) = {thermal_mat.diffusivity(t, units='mm^2/s'):.3f} mm^2/s")
    print()

    t_out = 1500.0
    print("Out-of-range policies at T=1500 K (for CuCrZr k):")
    print(f"clamp      -> {thermal_mat.k(t_out, policy='clamp'):.3f}")
    print(f"extrapolate-> {thermal_mat.k(t_out, policy='extrapolate'):.3f}")

    try:
        thermal_mat.k(t_out, policy="raise")
    except ValueError as exc:
        print(f"raise      -> {exc}")


if __name__ == "__main__":
    main()
