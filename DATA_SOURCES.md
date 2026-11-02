# Data sources and processing

The data folder contains processed research inputs, not observed passenger records. No personal home paths, credentials or nationwide source archives are included.

| Source | Data used | License/source terms |
|---|---|---|
| OpenStreetMap contributors / Geofabrik Vietnam extract | Walking network, station entrances, park/grass areas and review links; snapshot 15 August 2026 | [ODbL 1.0 and attribution](https://www.openstreetmap.org/copyright) |
| WorldPop Vietnam 2025, R2025A v1 | Population estimates assigned to walking origins | [WorldPop data](https://www.worldpop.org/); CC BY 4.0 |
| Meta and World Resources Institute, CHM v1 | Predicted existing canopy heights, tile `132230111` | [Dataset and attribution](https://registry.opendata.aws/dataforgood-fb-forests/); CC BY 4.0; source imagery attribution as specified by the provider |
| Kamath et al. (2024), UT-GLOBUS | Building footprints and predicted heights, Ho_Chi_Minh_City_1 | [Dataset DOI 10.5281/zenodo.11156602](https://zenodo.org/records/11156602); CC BY 4.0 in the dataset metadata |
| NOAA Global Monitoring Division | Approximate solar position calculations | [Technical equations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF) |

## Processing summary

1. Existing shortest routes were calculated from WorldPop origin assignments to two accepted OSM entrance nodes. Reachable population is 107,946.0807; unassigned/unreachable population is 687.1339.
2. A simplified geometric model estimated existing shadows on a 2 m grid and proposed-tree shade at three hours. Terrain is flat, foliage opaque and weather unmodeled.
3. Sites were generated on a 6 m grid in mapped park/grass areas near used paths. Planting pits intersecting mapped buildings and certain obstacles, and sites near existing canopy, were excluded. These screens do not verify land rights or underground conditions.
4. Of 1,623 screened sites, 823 had modeled benefits. The top 100 by best individual benefit across the two crown designs were retained.
5. Sunny route samples sharing the same set of covering candidates were grouped. Their benefit weights were summed without changing the maximum-coverage objective: 73 groups for the smaller design and 161 for the larger.

Each `benefit_weight` is population using a segment × represented metres ÷ 80 m/min × time weight. Each time has weight 1/3. The dataset is a derived analysis with design assumptions, not a new field survey. Candidate IDs identify proposed sites, not existing OSM trees.

OSM-derived database content remains subject to ODbL attribution/share-alike requirements where applicable. Other source components retain their original terms. No single blanket license in this repository replaces those source terms. Keep this file with redistributed data, and consult the linked terms for reuse. No software license is selected here; public visibility alone is not a grant of software reuse rights.
