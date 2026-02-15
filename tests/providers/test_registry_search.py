import opensolids as osl



def test_registry_material_resolution_from_each_provider():
    assert osl.material("nist-cryo:oxygen-free-copper").name == "Oxygen-Free Copper"
    assert osl.material("ntrs:20070017311:grcop-84").name == "GRCop-84"
    assert osl.material("mil-hdbk-5:H:inconel-718").name == "Inconel 718"
