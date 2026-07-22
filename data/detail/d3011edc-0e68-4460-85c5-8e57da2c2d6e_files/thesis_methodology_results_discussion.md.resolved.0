# CHAPTER THREE: METHODOLOGY

## 3.1 Introduction

This chapter describes the geospatial techniques, data sources, and analytical procedures employed to investigate the spatiotemporal relationship between urban expansion and geomorphic landscape change in the Cape Coast Metropolis of Ghana. The study integrates remote sensing, Geographic Information Systems (GIS), and coastal monitoring datasets within a multi-temporal framework spanning from 2000 to 2023.

## 3.2 Study Area

The Cape Coast Metropolitan Area is located in the Central Region of Ghana, lying between latitudes 5°06'N and 5°08'N, and longitudes 1°12'W and 1°19'W. The metropolis occupies a total land area of approximately 122 km², bounded to the south by the Gulf of Guinea. The terrain is characterised by undulating coastal lowlands, interspersed with moderate hills and dissected by small river valleys draining into the Atlantic Ocean. The coastline extends for approximately 13 km, consisting predominantly of sandy and mixed sand-gravel beaches that are subject to wave action, longshore drift, and periodic storm surges.

The climate is semi-equatorial, with mean annual rainfall of approximately 750–1,000 mm, concentrated in two wet seasons (May–July and September–November). The warm, humid conditions, combined with the moderate relief and proximity to the coast, render the area susceptible to flooding, slope instability, and coastal erosion—all of which are exacerbated by rapid, unplanned urbanisation.

## 3.3 Research Design

A quantitative, spatially explicit research design was adopted, structured around four interlinked analytical modules corresponding to the research objectives:

1. **Land Use/Land Cover (LULC) Classification and Change Detection** — to quantify the spatial extent and rate of urban expansion (RO1).
2. **Geomorphic Terrain Analysis** — to characterise slope instability zones and flood-susceptible lowlands (RO2).
3. **Spatial Overlay and Encroachment Analysis** — to determine the extent to which urbanisation has encroached onto geomorphically sensitive terrain (RO3).
4. **Shoreline Change Analysis** — to assess the dynamics of coastal erosion and accretion along the Cape Coast littoral zone (RO2/RO3).

## 3.4 Data Sources

Table 3.1 summarises the primary and secondary datasets used in the study.

| Dataset | Source | Resolution / Scale | Temporal Coverage | Purpose |
|---|---|---|---|---|
| Landsat Collection 2 Surface Reflectance | USGS Earth Explorer | 30 m | 2000, 2010, 2020 | LULC classification |
| ASTER Global DEM (GDEM v3) | NASA/METI | 30 m | Static | Terrain analysis (slope, TWI, flow) |
| DE Africa Coastlines v0.4.2 | Digital Earth Africa | 30 m (sub-pixel) | 2000–2023 (annual) | Shoreline change rates |
| Administrative Boundaries | Ghana Statistical Service | 1:50,000 | 2021 | Study area delineation |
| WorldView VHR Imagery | Maxar Technologies | < 1 m | 2018 | Coastlines validation reference |

## 3.5 Land Use/Land Cover Classification

### 3.5.1 Image Pre-processing

Landsat imagery (Landsat 5 TM for 2000; Landsat 7 ETM+ for 2010; and Landsat 8 OLI for 2020) was acquired from the USGS Earth Explorer platform. All images were atmospherically corrected Level-2 Surface Reflectance products processed using the USGS EROS Science Processing Architecture (ESPA). Scenes were selected based on minimum cloud cover (< 10%) and temporal proximity to the dry season (December–February) to maximise land surface visibility and reduce atmospheric interference.

### 3.5.2 Supervised Classification

A supervised Maximum Likelihood Classification (MLC) was performed in ArcGIS Pro using training samples collected for four land cover classes:

1. **Built-Up:** Residential, commercial, and institutional structures, roads, and impervious surfaces.
2. **Vegetation:** Natural forest, secondary regrowth, shrubland, and agricultural cropland.
3. **Water:** Rivers, lagoons, reservoirs, and the ocean.
4. **Bare Soil:** Exposed earth, quarries, construction sites, and fallow agricultural land.

Training samples were digitised from high-resolution Google Earth imagery and verified against field knowledge. A minimum of 50 training pixels per class were collected for each epoch to ensure statistical representativeness.

### 3.5.3 Change Detection

Post-classification change detection was performed by cross-tabulating the classified rasters for consecutive epochs (2000–2010 and 2010–2020) using the *Tabulate Area* tool in ArcGIS Pro. This generated a transition matrix quantifying the area (in km²) that transitioned from one LULC class to another between each pair of epochs.

## 3.6 Geomorphic Terrain Analysis

### 3.6.1 Slope Analysis

A slope raster (in degrees) was derived from the ASTER GDEM using the *Slope* tool in ArcGIS Pro's Spatial Analyst extension. The slope raster was subsequently reclassified into five classes:

| Slope Class | Range (°) | Terrain Description |
|---|---|---|
| 1 | 0–3 | Flat / Nearly flat |
| 2 | 3–8 | Gentle slopes |
| 3 | 8–15 | Moderate slopes |
| 4 | 15–25 | Steep slopes |
| 5 | > 25 | Very steep slopes |

Slopes exceeding 8° were designated as **geomorphically unstable** for the purpose of the slope instability encroachment analysis, based on established thresholds in tropical geomorphology literature (Selby, 1993; Crozier, 2010).

### 3.6.2 Hydrological Terrain Analysis

The Topographic Wetness Index (TWI) was computed to identify areas with a high propensity for water accumulation and surface flooding. TWI is defined as:

$$\text{TWI} = \ln\left(\frac{A}{\tan(\beta)}\right)$$

where *A* is the specific catchment area (derived from flow accumulation) and *β* is the local slope angle in radians. High TWI values indicate flat, low-lying terrain where surface water is likely to accumulate—areas inherently susceptible to flooding.

Flow Direction and Flow Accumulation rasters were computed from the filled DEM using D8 single-flow algorithms in ArcGIS Pro.

### 3.6.3 Flood Hazard Mapping

A multi-criteria flood hazard assessment was constructed by combining four geomorphic input factors using a Weighted Overlay approach:

| Factor | Weight (%) | Justification |
|---|---|---|
| Topographic Wetness Index (TWI) | 35% | Primary indicator of water accumulation potential |
| Flow Accumulation | 25% | Identifies concentrated surface runoff pathways |
| Flow Direction | 20% | Determines drainage routing and convergence zones |
| LULC | 20% | Impervious surfaces increase runoff generation |

The resulting hazard map was classified into four zones: Low, Moderate, High, and Very High flood risk.

### 3.6.4 Slope Instability Encroachment Analysis

To quantify the extent of urban encroachment onto geomorphically unstable terrain, the LULC Built-Up class for each epoch was spatially intersected with the reclassified slope raster. Specifically, the total number of Built-Up pixels located on slopes exceeding 8° was extracted for each year (2000, 2010, 2020) and converted to area (km²) using the spatial resolution factor (30 m × 30 m = 900 m² = 0.0009 km² per pixel).

## 3.7 Shoreline Change Analysis

### 3.7.1 Data Source and Extraction Method

Shoreline positions were obtained from the **Digital Earth Africa (DE Africa) Coastlines** monitoring service (version 0.4.2), a continental-scale dataset that maps annual shoreline positions along the entire African coast from 2000 onwards (Bishop-Taylor et al., 2021).

Annual shorelines are delineated by applying the Modified Normalised Difference Water Index (MNDWI) to Landsat Collection 2 Surface Reflectance imagery:

$$\text{MNDWI} = \frac{\text{Green} - \text{SWIR}}{\text{Green} + \text{SWIR}}$$

where values greater than zero are classified as water. Sub-pixel waterline extraction algorithms are applied to achieve horizontal accuracy finer than the native 30 m pixel resolution. Tidal modelling is integrated to standardise all shoreline positions to Mean Sea Level (0 m AMSL), thereby isolating true geomorphic change from daily tidal fluctuations.

### 3.7.2 Accuracy and Validation

The DE Africa Coastlines dataset has been validated across 12 West African countries by the Centre de Suivi Ecologique (CSE), Dakar, in collaboration with the WACA/ORLOA network. In Ghana, validation was conducted against sub-metre WorldView satellite imagery (acquired October 31, 2018), yielding a Root Mean Square Error (RMSE) of approximately 5–9 metres—well within sub-pixel accuracy for Landsat-derived products (CSE/WACA, 2022).

### 3.7.3 Rate of Change Calculation

Three standard shoreline change metrics were computed at 187 transect points spaced at 30 m intervals along the Cape Coast littoral zone:

1. **Linear Regression Rate (LRR):** The annual rate of shoreline change (m/yr) calculated by fitting an ordinary least-squares linear regression through all valid annual shoreline distances against time, with outliers excluded via the Median Absolute Deviation (MAD) algorithm.
2. **Net Shoreline Movement (NSM):** The net horizontal distance (m) between the oldest (2000) and most recent (2023) annual shoreline.
3. **Shoreline Change Envelope (SCE):** The maximum horizontal distance (m) between any two annual shorelines, representing the total width of the shoreline migration corridor.

---

# CHAPTER FOUR: RESULTS

## 4.1 Introduction

This chapter presents the results of the spatial analysis of land use/land cover change, geomorphic terrain characteristics, slope instability encroachment, flood hazard mapping, and shoreline dynamics in the Cape Coast Metropolis over the period 2000–2023.

## 4.2 Land Use/Land Cover Distribution (2000–2020)

The supervised classification of Landsat imagery for the three epochs (2000, 2010, 2020) revealed four dominant land cover classes across the 121.96 km² study area. Table 4.1 summarises the LULC area distribution for each year.

**Table 4.1: LULC Area Distribution in the Cape Coast Metropolis (2000–2020)**

| LULC Class | 2000 Area (km²) | 2000 (%) | 2010 Area (km²) | 2010 (%) | 2020 Area (km²) | 2020 (%) | Net Change (km²) |
|---|---|---|---|---|---|---|---|
| Built-Up | 15.47 | 12.68 | 19.62 | 16.09 | 35.81 | 29.37 | +20.34 |
| Vegetation | 104.27 | 85.50 | 100.01 | 82.00 | 82.20 | 67.40 | −22.07 |
| Water | 0.87 | 0.72 | 1.37 | 1.13 | 1.04 | 0.85 | +0.17 |
| Bare Soil | 1.35 | 1.10 | 0.96 | 0.79 | 2.91 | 2.38 | +1.56 |
| **Total** | **121.96** | **100.00** | **121.96** | **100.00** | **121.96** | **100.00** | — |

In 2000, vegetation was the dominant land cover, occupying 104.27 km² (85.50%) of the study area. Built-up areas were concentrated along the southern coastal strip, accounting for only 15.47 km² (12.68%). By 2020, built-up areas had expanded dramatically to 35.81 km² (29.37%), representing a net increase of 20.34 km² (+131.5%) over the two decades. This expansion occurred primarily at the expense of vegetation, which declined by 22.07 km² to 82.20 km² (67.40%). Bare soil also increased from 1.35 km² to 2.91 km², reflecting active land clearing and construction activity at the peri-urban fringes.

*(See Figure 4.1: LULC Classification Maps for 2000, 2010, and 2020)*

## 4.3 Land Use/Land Cover Change Detection

Post-classification change detection analysis quantified the specific transitions between land cover classes across the two decadal periods.

### 4.3.1 Period I: 2000–2010

During the first decade, 110.94 km² (91.0%) of the study area remained unchanged, while 11.02 km² (9.0%) underwent LULC transitions (Table 4.2).

**Table 4.2: LULC Transition Matrix for 2000–2010**

| Transition | Area (km²) | Contribution (%) |
|---|---|---|
| Vegetation → Built-Up | 6.12 | 55.53 |
| Built-Up → Vegetation | 2.30 | 20.91 |
| Bare Soil → Built-Up | 0.83 | 7.57 |
| Vegetation → Water | 0.77 | 7.01 |
| Built-Up → Bare Soil | 0.49 | 4.43 |
| Other minor transitions | 0.51 | 4.55 |

The dominant transition was Vegetation to Built-Up (6.12 km²), accounting for 55.53% of all land cover changes. This represents the initial phase of urban sprawl, characterised by moderate, incremental expansion along existing road corridors and the coastal strip.

### 4.3.2 Period II: 2010–2020

During the second decade, the rate of landscape transformation accelerated significantly. Only 98.29 km² (80.6%) remained unchanged, while 23.67 km² (19.4%) underwent transitions—more than double the area that changed during the first decade (Table 4.3).

**Table 4.3: LULC Transition Matrix for 2010–2020**

| Transition | Area (km²) | Contribution (%) |
|---|---|---|
| Vegetation → Built-Up | 18.24 | 77.05 |
| Built-Up → Bare Soil | 1.28 | 5.40 |
| Built-Up → Vegetation | 1.22 | 5.15 |
| Vegetation → Bare Soil | 1.13 | 4.77 |
| Water → Vegetation | 0.80 | 3.38 |
| Vegetation → Water | 0.48 | 2.03 |
| Bare Soil → Built-Up | 0.45 | 1.90 |
| Other minor transitions | 0.07 | 0.32 |

The Vegetation to Built-Up transition intensified dramatically to 18.24 km²—a 198% increase over the previous decade. This single transition accounted for 77.05% of all land cover change during 2010–2020, indicating a shift from gradual peri-urban expansion to rapid, widespread deforestation-driven urbanisation.

*(See Figure 4.2: LULC Change Detection Maps for 2000–2010 and 2010–2020)*

## 4.4 Geomorphic Terrain Characterisation

### 4.4.1 Slope Instability Zones

The slope analysis revealed that the Cape Coast terrain comprises a mixture of gentle coastal lowlands and moderate inland hills. The slope instability encroachment analysis (Table 4.4) quantified the extent of built-up areas located on slopes exceeding 8° for each epoch.

**Table 4.4: Built-Up Encroachment on Unstable Slopes (> 8°)**

| Year | Built-Up Pixels on Unstable Slopes | Area (km²) | Change from 2000 |
|---|---|---|---|
| 2000 | 666 | 0.60 | — |
| 2010 | 732 | 0.66 | +10.0% |
| 2020 | 1,767 | 1.59 | +165.0% |

In 2000, only 0.60 km² of built-up area was situated on slopes exceeding 8°. By 2010, this had increased modestly to 0.66 km² (+10.0%). However, between 2010 and 2020, encroachment accelerated sharply, with built-up area on unstable slopes nearly tripling to 1.59 km²—a cumulative increase of 165.0% over the entire study period.

*(See Figure 4.3: Instability Zones Map — 2000, 2010, 2020)*

### 4.4.2 Flood Hazard Assessment

The multi-criteria flood hazard assessment integrated TWI, Flow Accumulation, Flow Direction, and LULC to produce yearly flood risk maps for 2000, 2010, and 2020. The results showed that High and Very High flood risk zones are concentrated in the low-elevation southern coastal belt and along river valley corridors. As built-up areas expanded between 2000 and 2020, the extent of impervious surfaces within flood-susceptible lowlands increased, amplifying surface runoff generation and reducing natural infiltration capacity.

*(See Figure 4.4: Flood Hazard Maps — Input Factors and Yearly Risk Assessment)*

## 4.5 Shoreline Change Analysis (2000–2023)

### 4.5.1 Overall Shoreline Dynamics

Analysis of 187 transect points along the Cape Coast shoreline revealed a highly dynamic littoral zone (Table 4.5).

**Table 4.5: Shoreline Change Statistics for Cape Coast (2000–2023)**

| Metric | Value |
|---|---|
| Total transect points analysed | 187 |
| Eroding transects (LRR < 0 m/yr) | 98 (52.4%) |
| Accreting transects (LRR > 0 m/yr) | 89 (47.6%) |
| Stable transects (LRR = 0 m/yr) | 0 (0.0%) |
| Mean Linear Regression Rate (LRR) | +0.03 m/yr |
| Maximum Erosion Rate | −1.26 m/yr |
| Maximum Accretion Rate | +1.53 m/yr |
| Mean Net Shoreline Movement (NSM) | +2.19 m (seaward) |
| Maximum Landward Shift (erosion) | −23.55 m |
| Maximum Seaward Shift (accretion) | +84.33 m |
| Mean Shoreline Change Envelope (SCE) | 23.07 m |
| Maximum SCE | 44.74 m |

The mean Linear Regression Rate (LRR) of +0.03 m/yr suggests an overall dynamic equilibrium at the metropolitan scale. However, this average masks significant spatial variability: 52.4% of the transects are undergoing active erosion (up to −1.26 m/yr), while 47.6% are experiencing accretion (up to +1.53 m/yr). No transect along the entire stretch was found to be perfectly stable (LRR = 0), confirming that the Cape Coast shoreline is universally active.

### 4.5.2 Net Shoreline Movement (NSM)

The mean NSM of +2.19 m indicates a slight net seaward advance of the shoreline over the 24-year period. However, localised erosion hotspots recorded a maximum landward retreat of −23.55 m, while deposition zones registered a maximum seaward advance of +84.33 m. The wide spread of NSM values across the transects indicates that shoreline dynamics are highly localised, influenced by nearshore bathymetry, the presence of coastal defence structures, and riverine sediment inputs.

### 4.5.3 Shoreline Change Envelope (SCE)

The mean SCE of 23.07 m reveals that the average shoreline migration corridor over the study period was approximately 23 metres wide. This means that at any given transect, the shoreline fluctuated within a 23-metre horizontal band between 2000 and 2023. The maximum SCE of 44.74 m indicates zones of extreme instability, where the shoreline oscillated across nearly 45 metres of horizontal space.

*(See Figure 4.5: Annual Shoreline Positions and Inset Maps)*

---

# CHAPTER FIVE: DISCUSSION

## 5.1 Introduction

This chapter interprets the spatial and temporal patterns of land use/land cover change, geomorphic terrain dynamics, and shoreline behaviour observed in the Cape Coast Metropolis. The findings are discussed in relation to the research objectives, existing literature on tropical urbanisation and coastal geomorphology, and their implications for spatial planning and environmental management.

## 5.2 Urban Expansion and the Acceleration of Landscape Transformation

The results reveal that built-up areas in the Cape Coast Metropolis more than doubled (+131.5%) over two decades, expanding from 15.47 km² in 2000 to 35.81 km² in 2020. This growth trajectory is consistent with broader patterns of rapid urbanisation documented in secondary cities across sub-Saharan Africa (UN-Habitat, 2022; Cobbinah & Aboagye, 2017). However, a critical finding is that the rate of expansion was not uniform. The conversion of vegetation to built-up area accelerated by approximately 198% between the first decade (6.12 km² lost) and the second decade (18.24 km² lost).

This acceleration can be attributed to several interrelated factors. First, the expansion of the University of Cape Coast (UCC) and the growth of student accommodation in the Amamoma–Apewosika–Kwaprow corridor has created intense development pressure in the north-western sector of the metropolis (Owusu-Ansah & O'Connor, 2010). Second, the completion of major road infrastructure (including the Cape Coast–Elmina highway) has improved accessibility and stimulated speculative land development in previously vegetated peri-urban zones (Yeboah & Shaw, 2013). Third, the absence of effective land use zoning and building control enforcement has allowed unregulated construction to encroach onto environmentally sensitive terrain.

The dominance of the Vegetation → Built-Up transition (accounting for 55.53% of all change in 2000–2010 and 77.05% in 2010–2020) has profound geomorphic implications. The removal of vegetation cover eliminates root-binding of soils, increases surface runoff velocity, reduces infiltration, and destabilises slopes—thereby amplifying both flood and erosion hazards simultaneously.

## 5.3 Urban Encroachment onto Geomorphically Unstable Terrain

A particularly alarming finding is the 165% increase in built-up area on slopes exceeding 8° between 2000 (0.60 km²) and 2020 (1.59 km²). This encroachment is not merely an aesthetic concern; it represents a direct increase in the population exposed to slope failure, gully erosion, and structural collapse during heavy rainfall events.

In tropical geomorphic environments, slopes exceeding 8° on weathered regolith are inherently prone to shallow translational landslides when vegetation cover is removed and surface loading from buildings is applied (Selby, 1993; Crozier, 2010). The acceleration of encroachment after 2010 (from 0.66 km² to 1.59 km² in a single decade) suggests that land scarcity on the flat coastal plain is increasingly forcing development onto marginal hillside locations. This is consistent with the "hillside urbanisation" phenomenon observed in other rapidly growing coastal cities in West Africa, including Freetown (Maconachie et al., 2019) and Abidjan (Yapi-Diahou, 2000).

The flood hazard mapping results reinforce this concern. As impervious built-up surfaces have expanded into low-lying zones characterised by high TWI values, the capacity of the natural drainage system to absorb and route surface runoff has been progressively diminished. The combination of increased runoff generation (from impervious surfaces) and reduced infiltration capacity (from vegetation loss) creates a positive feedback loop that amplifies both the frequency and severity of urban flooding episodes.

## 5.4 Shoreline Dynamics and Coastal Erosion

The shoreline change analysis reveals a coastline that is simultaneously eroding and accreting in a spatially fragmented pattern. While the mean LRR of +0.03 m/yr suggests apparent stability, this metric is misleading at the metropolitan scale because it averages out the contrasting dynamics of erosion (52.4% of transects) and accretion (47.6% of transects).

The maximum erosion rate of −1.26 m/yr at specific transects represents a significant threat to coastal infrastructure and settlements. At this rate, a building located 30 metres from the shoreline would be at risk of undermining within 24 years—well within the design life of most residential structures in the metropolis. The maximum landward shift of −23.55 m over the study period demonstrates that this is not a hypothetical projection but an observed reality.

The accretion hotspots (up to +1.53 m/yr, with a maximum seaward advance of +84.33 m) are likely associated with sediment trapping by coastal defence structures (groynes and revetments), natural sediment deposition at river mouths, and longshore drift accumulation at headland lee zones. While accretion is superficially positive, it can create a false sense of security and attract further coastal development in areas that remain vulnerable to storm surges and episodic wave attack.

The mean SCE of 23.07 m has direct planning implications: any development located within 23 metres of the current shoreline is statistically likely to be affected by normal interannual shoreline variability, even in the absence of long-term erosion trends. This finding supports the adoption of a minimum coastal setback distance of at least 30–50 metres, as recommended by the Ghana National Building Regulations (LI 1630).

## 5.5 The Nexus: Urban Expansion, Geomorphic Instability, and Coastal Vulnerability

The most significant contribution of this study lies in demonstrating the interconnected nature of three typically siloed phenomena: urban expansion, terrain instability, and coastal erosion. These three processes are not independent—they are linked through a common mechanism: the progressive conversion of natural land cover to impervious built-up surfaces.

When vegetation is cleared for construction on hillsides (as evidenced by the 165% increase in slope instability encroachment), the resulting increase in surface runoff accelerates gully formation and delivers additional sediment loads to downstream river channels. These channels convey the sediment to the coast, where it is redistributed by longshore drift. Conversely, where coastal erosion removes beach material, the resulting exposure of the hinterland to wave action threatens existing built-up infrastructure and forces development further inland—onto progressively steeper and more unstable terrain.

This cyclical relationship suggests that piecemeal, sector-specific interventions (e.g., addressing flooding alone without considering slope stability, or building seawalls without addressing sediment supply from upstream) are unlikely to be effective. Instead, an integrated spatial planning approach that simultaneously manages urban growth boundaries, protects upland vegetation, and maintains coastal buffer zones is required.

## 5.6 Summary of Key Findings

The following table synthesises the principal quantitative findings of the study:

| Finding | Quantitative Result | Geomorphic Implication |
|---|---|---|
| Built-up expansion | +131.5% (15.47 → 35.81 km²) | Increased impervious surface, reduced infiltration |
| Vegetation loss | −21.2% (104.27 → 82.20 km²) | Loss of root binding, increased runoff and erosion |
| Urban expansion rate acceleration | 198% faster in 2010–2020 vs 2000–2010 | Exponentially increasing environmental pressure |
| Slope encroachment (> 8°) | +165% (0.60 → 1.59 km²) | Direct exposure to slope failure and gully erosion |
| Eroding shoreline transects | 52.4% of 187 transects | More than half the coastline is retreating |
| Maximum coastal erosion rate | −1.26 m/yr | Significant threat to coastal infrastructure |
| Maximum landward retreat | −23.55 m over 24 years | Observed land loss at specific locations |
| Shoreline migration corridor (SCE) | Mean 23.07 m | Minimum setback distance must exceed this value |
