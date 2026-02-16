# Material Sources

This table shows where each canonical property curve comes from, including units,
valid temperature range, and whether data is modeled/computed or experimentally derived.

| canonical_id | property | units | valid_T_range_K | source_id / derivation | data_origin | citation_or_url |
|---|---|---|---|---|---|---|
| `al-6061-am` | `E` | `Pa` | `[2, 295]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-am` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-am` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:aluminum-6061-t6 | cp:nist-cryo-src:aluminum-6061-t6 | rho:density_ref=2700.0 kg/m^3` | `fit-parse | assumed-constant` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-am` | `eps_th` | `1` | `[4, 300]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-am` | `k` | `W/(m*K)` | `[1, 300]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-am` | `sigma_uts` | `Pa` | `[294, 533]` | `mil-hdbk-5-src:H:al-6061-t6` | `manual` | MIL-HDBK-5H |
| `al-6061-am` | `sigma_y` | `Pa` | `[294, 533]` | `mil-hdbk-5-src:H:al-6061-t6` | `manual` | MIL-HDBK-5H |
| `al-6061-t6` | `E` | `Pa` | `[2, 295]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-t6` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-t6` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:aluminum-6061-t6 | cp:nist-cryo-src:aluminum-6061-t6 | rho:density_ref=2700.0 kg/m^3` | `fit-parse | assumed-constant` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-t6` | `eps_th` | `1` | `[4, 300]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-t6` | `k` | `W/(m*K)` | `[1, 300]` | `nist-cryo-src:aluminum-6061-t6` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm |
| `al-6061-t6` | `sigma_uts` | `Pa` | `[294, 533]` | `mil-hdbk-5-src:H:al-6061-t6` | `manual` | MIL-HDBK-5H |
| `al-6061-t6` | `sigma_y` | `Pa` | `[294, 533]` | `mil-hdbk-5-src:H:al-6061-t6` | `manual` | MIL-HDBK-5H |
| `alsi10mg-am` | `E` | `Pa` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `alpha` | `1/K` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `cp` | `J/(kg*K)` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `diffusivity` | `m^2/s` | `[293.15, 793.15]` | `k:curated-public-src:alsi10mg:mdpi-ma2023 | cp:curated-public-src:alsi10mg:mdpi-ma2023 | rho:curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `k` | `W/(m*K)` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `nu` | `1` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `rho` | `kg/m^3` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `alsi10mg-am` | `sigma_uts` | `Pa` | `[293.15, 293.15]` | `curated-public-src:alsi10mg:nasa-20205003675` | `manual` | https://ntrs.nasa.gov/citations/20205003675 |
| `alsi10mg-am` | `sigma_y` | `Pa` | `[293.15, 793.15]` | `curated-public-src:alsi10mg:mdpi-ma2023` | `computed` | https://www.mdpi.com/2076-3417/13/6/3460 |
| `c101` | `E` | `Pa` | `[293.15, 293.15]` | `curated-public-src:c101:copper-org` | `manual` | https://alloys.copper.org/alloy/C10100 |
| `c101` | `alpha` | `1/K` | `[4, 300]` | `nist-cryo-src:oxygen-free-copper` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm |
| `c101` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:oxygen-free-copper` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm |
| `c101` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:oxygen-free-copper-rrr100 | cp:nist-cryo-src:oxygen-free-copper | rho:curated-public-src:c101:copper-org` | `fit-sampled-tabular | fit-parse | manual` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm<br>https://alloys.copper.org/alloy/C10100 |
| `c101` | `k` | `W/(m*K)` | `[4, 300]` | `nist-cryo-src:oxygen-free-copper-rrr100` | `fit-sampled-tabular` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm |
| `c101` | `rho` | `kg/m^3` | `[4, 300]` | `curated-public-src:c101:copper-org` | `manual` | https://alloys.copper.org/alloy/C10100 |
| `c101` | `sigma_uts` | `Pa` | `[293.15, 293.15]` | `curated-public-src:c101:copper-org` | `manual` | https://alloys.copper.org/alloy/C10100 |
| `c101` | `sigma_y` | `Pa` | `[293.15, 293.15]` | `curated-public-src:c101:copper-org` | `manual` | https://alloys.copper.org/alloy/C10100 |
| `c110` | `E` | `Pa` | `[293.15, 293.15]` | `curated-public-src:c110:copper-org` | `manual` | https://alloys.copper.org/alloy/C11000 |
| `c110` | `alpha` | `1/K` | `[4, 300]` | `nist-cryo-src:oxygen-free-copper` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm |
| `c110` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:oxygen-free-copper` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm |
| `c110` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:oxygen-free-copper-rrr50 | cp:nist-cryo-src:oxygen-free-copper | rho:curated-public-src:c110:copper-org` | `fit-sampled-tabular | fit-parse | manual` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm<br>https://alloys.copper.org/alloy/C11000 |
| `c110` | `k` | `W/(m*K)` | `[4, 300]` | `nist-cryo-src:oxygen-free-copper-rrr50` | `fit-sampled-tabular` | https://trc.nist.gov/cryogenics/materials/OFHC%20Copper/OFHC_Copper_rev1.htm |
| `c110` | `rho` | `kg/m^3` | `[4, 300]` | `curated-public-src:c110:copper-org` | `manual` | https://alloys.copper.org/alloy/C11000 |
| `c110` | `sigma_uts` | `Pa` | `[293.15, 293.15]` | `curated-public-src:c110:copper-org` | `manual` | https://alloys.copper.org/alloy/C11000 |
| `c110` | `sigma_y` | `Pa` | `[293.15, 293.15]` | `curated-public-src:c110:copper-org` | `manual` | https://alloys.copper.org/alloy/C11000 |
| `cucrzr-am` | `cp` | `J/(kg*K)` | `[293.15, 900]` | `ntrs-src:20210010991` | `experimental` | https://ntrs.nasa.gov/citations/20210010991 |
| `cucrzr-am` | `diffusivity` | `m^2/s` | `[293.15, 900]` | `k:ntrs-src:20210010991 | cp:ntrs-src:20210010991 | rho:density_ref=8900.0 kg/m^3` | `experimental | assumed-constant` | https://ntrs.nasa.gov/citations/20210010991 |
| `cucrzr-am` | `k` | `W/(m*K)` | `[293.15, 900]` | `ntrs-src:20210010991` | `experimental` | https://ntrs.nasa.gov/citations/20210010991 |
| `grcop-84-am` | `k` | `W/(m*K)` | `[293.15, 1000]` | `ntrs-src:20070017311` | `tabular-digitized` | 20070017311 |
| `grcop-84-am` | `sigma_uts` | `Pa` | `[293.15, 1000]` | `ntrs-src:20070017311` | `tabular-digitized` | 20070017311 |
| `grcop-84-am` | `sigma_y` | `Pa` | `[293.15, 1000]` | `ntrs-src:20070017311` | `tabular-digitized` | 20070017311 |
| `in718-am` | `eps_th` | `1` | `[4, 300]` | `nist-cryo-src:inconel-718` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/Iconel%20718/Inconel718_rev.htm |
| `in718-am` | `k` | `W/(m*K)` | `[4, 300]` | `nist-cryo-src:inconel-718` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/Iconel%20718/Inconel718_rev.htm |
| `in718-am` | `sigma_uts` | `Pa` | `[294, 1000]` | `mil-hdbk-5-src:H:inconel-718` | `manual` | MIL-HDBK-5H |
| `in718-am` | `sigma_y` | `Pa` | `[294, 1000]` | `mil-hdbk-5-src:H:inconel-718` | `manual` | MIL-HDBK-5H |
| `ss304` | `E` | `Pa` | `[57, 293]` | `nist-cryo-src:stainless-steel-304` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/304Stainless/304Stainless_rev.htm |
| `ss304` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:stainless-steel-304` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/304Stainless/304Stainless_rev.htm |
| `ss304` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:stainless-steel-304 | cp:nist-cryo-src:stainless-steel-304 | rho:density_ref=8030.0 kg/m^3` | `fit-parse | assumed-constant` | https://trc.nist.gov/cryogenics/materials/304Stainless/304Stainless_rev.htm |
| `ss304` | `eps_th` | `1` | `[4, 300]` | `nist-cryo-src:stainless-steel-304` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/304Stainless/304Stainless_rev.htm |
| `ss304` | `k` | `W/(m*K)` | `[1, 300]` | `nist-cryo-src:stainless-steel-304` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/304Stainless/304Stainless_rev.htm |
| `ss316` | `E` | `Pa` | `[50, 294]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:stainless-steel-316 | cp:nist-cryo-src:stainless-steel-316 | rho:density_ref=8000.0 kg/m^3` | `fit-parse | assumed-constant` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316` | `eps_th` | `1` | `[4, 300]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316` | `k` | `W/(m*K)` | `[1, 300]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316-am` | `E` | `Pa` | `[50, 294]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316-am` | `cp` | `J/(kg*K)` | `[4, 300]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316-am` | `diffusivity` | `m^2/s` | `[4, 300]` | `k:nist-cryo-src:stainless-steel-316 | cp:nist-cryo-src:stainless-steel-316 | rho:density_ref=8000.0 kg/m^3` | `fit-parse | assumed-constant` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316-am` | `eps_th` | `1` | `[4, 300]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
| `ss316-am` | `k` | `W/(m*K)` | `[1, 300]` | `nist-cryo-src:stainless-steel-316` | `fit-parse` | https://trc.nist.gov/cryogenics/materials/316Stainless/316Stainless_rev.htm |
