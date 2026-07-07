# Detailed Implementation Guide — Part 1 of 2
## Cape Coast Urban Expansion × Geomorphic Features Analysis

> [!IMPORTANT]
> This guide follows a strict **sequential pipeline**. Each module feeds into the next. Do NOT skip ahead.

---

# MODULE 1: Data Acquisition & Pre-Processing (Foundation)

**Duration:** ~3 weeks | **Prerequisite:** None — this is the starting point

## Step 1.1: Define Study Area Boundary

1. Open ArcGIS Pro → New Project → Set CRS to **UTM Zone 30N (EPSG:32630)**
2. Download Cape Coast Metropolitan boundary from:
   - Ghana Statistical Service shapefiles, OR
   - GADM (gadm.org) Level 2 administrative boundaries
   - HDX (Humanitarian Data Exchange) Ghana admin boundaries
3. If boundary unavailable as shapefile:
   - Open Google Earth Pro → digitize boundary manually using official gazetted extent
   - Export as KML → convert to shapefile in ArcGIS (Conversion Tools → KML to Layer)
4. Add a **5 km buffer** around the metro boundary to capture peri-urban expansion zones
5. Save as `study_area_boundary.shp` — this clips ALL subsequent datasets

**Output:** `study_area_boundary.shp` + `study_area_buffered.shp`

## Step 1.2: Satellite Imagery Acquisition

### Landsat Imagery (1990, 2000, 2010)

1. Go to **USGS EarthExplorer** (earthexplorer.usgs.gov)
2. Search Criteria → enter coordinates: **5.1°N, 1.25°W**
3. Set date ranges (target **dry season Dec–Feb** for minimal cloud):
   - Epoch 1: `1988-12-01` to `1992-02-28`
   - Epoch 2: `1999-12-01` to `2002-02-28`
   - Epoch 3: `2009-12-01` to `2012-02-28`
4. Data Sets:
   - Epoch 1: Landsat → Landsat 4-5 TM → Collection 2 Level-2 (Surface Reflectance)
   - Epoch 2: Landsat → Landsat 7 ETM+ → Collection 2 Level-2 (**avoid post-May 2003 SLC-off**)
   - Epoch 3: Landsat → Landsat 4-5 TM → Collection 2 Level-2
5. Filter: Cloud cover < 10%
6. Select best scene per epoch → Download **Surface Reflectance** product
7. Scene ID format: `LT05_L2SP_194056_YYYYMMDD` (Path 194, Row 056 covers Cape Coast)

### Sentinel-2 / Landsat 8-9 (2020, 2025)

1. Go to **Copernicus Open Access Hub** (scihub.copernicus.eu) or **Google Earth Engine**
2. Search tile **T30NWN** or nearby tiles covering Cape Coast
3. Date ranges:
   - Epoch 4: `2019-12-01` to `2021-02-28`
   - Epoch 5: `2024-12-01` to `2025-02-28`
4. Download **Level-2A** (already atmospherically corrected)
5. Bands needed: B2(Blue), B3(Green), B4(Red), B8(NIR), B11(SWIR1), B12(SWIR2)

### Alternative: Google Earth Engine (Recommended for Efficiency)

```javascript
// GEE Script — Landsat 5 Composite for 1990 epoch
var aoi = ee.Geometry.Point([-1.25, 5.1]).buffer(15000);
var l5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
  .filterBounds(aoi)
  .filterDate('1989-12-01', '1991-02-28')
  .filter(ee.Filter.lt('CLOUD_COVER', 10))
  .median()
  .clip(aoi);

// Apply scaling factors
var scaled = l5.select(['SR_B1','SR_B2','SR_B3','SR_B4','SR_B5','SR_B7'])
  .multiply(0.0000275).add(-0.2);

Export.image.toDrive({image: scaled, description: 'CC_1990', region: aoi, scale: 30, crs: 'EPSG:32630'});
```

> Repeat with modified collection IDs and dates for each epoch.

## Step 1.3: DEM Acquisition

| DEM | Download From | Action |
|---|---|---|
| SRTM 30m | earthexplorer.usgs.gov → Digital Elevation → SRTM 1 Arc-Second | Download tile N05W002 |
| ALOS PALSAR 12.5m | search.asf.alaska.edu → ALOS PALSAR → RTC DEM | Search by coordinates |
| Copernicus DEM 30m | panda.copernicus.eu/panda → COP-DEM_GLO-30 | Download tile |

**Post-download for ALL DEMs:**
1. Load into ArcGIS Pro
2. Project Raster → UTM Zone 30N (EPSG:32630)
3. Clip to `study_area_buffered.shp` (use Extract by Mask)
4. Fill sinks (Spatial Analyst → Hydrology → Fill)
5. Save as `dem_srtm_30m.tif`, `dem_alos_12m.tif`, `dem_copernicus_30m.tif`

## Step 1.4: Pre-Processing Satellite Imagery

For **Landsat Collection 2 Level-2** (already surface reflectance):
1. Load bands into ArcGIS Pro
2. Composite Bands tool → create multi-band raster stack
3. Project to UTM Zone 30N
4. Clip to `study_area_buffered.shp`

For **Sentinel-2 Level-2A**:
1. Resample B11, B12 (20m) to 10m using bilinear interpolation
2. Composite Bands → stack B2, B3, B4, B8, B11, B12
3. Project and clip as above

**Quality Check:** Visually inspect all 5 epoch composites. Ensure no cloud contamination, geometric alignment (overlay on same reference — roads should align).

**Output:** 5 analysis-ready composite rasters, 3 processed DEMs

---

# MODULE 2: LULC Classification & Urban Expansion Mapping (RO1)

**Duration:** ~4 weeks | **Prerequisite:** Module 1 complete

## Step 2.1: Classification Scheme Design

Use a **consistent 5-class scheme** across ALL epochs:

| Class ID | Class Name | Spectral Characteristics |
|---|---|---|
| 1 | **Built-up/Urban** | High reflectance in SWIR, low NDVI |
| 2 | **Dense Vegetation** | High NIR, high NDVI (>0.4) |
| 3 | **Sparse Vegetation/Agriculture** | Moderate NDVI (0.2–0.4) |
| 4 | **Bare Soil/Exposed** | High visible, low NIR |
| 5 | **Water** | High absorption in NIR/SWIR, high NDWI |

## Step 2.2: Spectral Index Computation

For EACH epoch composite, compute and add as bands:

```
NDVI = (NIR - Red) / (NIR + Red)
NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)
NDWI = (Green - NIR) / (Green + NIR)
MNDWI = (Green - SWIR1) / (Green + SWIR1)
```

In ArcGIS: Raster Calculator or Image Analysis → Band Arithmetic.

## Step 2.3: Training Sample Collection

**For EACH of the 5 epochs independently:**

1. Create a new polygon feature class: `training_samples_YYYY.shp`
2. Add field: `ClassID` (Short Integer), `ClassName` (Text)
3. Collect **minimum 30 polygons per class** (150+ total per epoch):
   - Use the epoch's own imagery as reference
   - Use Google Earth Pro historical imagery for validation
   - Ensure spatial distribution across the entire study area
   - Avoid mixed pixels at class boundaries
4. For historical epochs (1990, 2000): use Google Earth Pro time slider to verify land cover

> [!WARNING]
> Training samples for 1990 are the hardest. Use Google Earth's earliest available imagery (~2004) cautiously, combined with historical maps and local knowledge.

## Step 2.4: Run Classification (Random Forest Recommended)

**In ArcGIS Pro:**
1. Analysis → Image Classification → Classification Tools → Train Random Trees Classifier
   - Input: epoch composite (with spectral indices as added bands)
   - Training Samples: `training_samples_YYYY.shp`
   - Max Trees: 100–500
   - Max Depth: 30
2. Classification Tools → Classify Raster
   - Input: same composite
   - Classifier: the .ecd file from training
3. Output: `lulc_YYYY_raw.tif`

**Post-classification cleaning:**
1. Spatial Analyst → Generalization → Majority Filter (3×3 window)
2. Reclassify any obvious misclassifications
3. Save as `lulc_YYYY_final.tif`

**Repeat for all 5 epochs.**

## Step 2.5: Accuracy Assessment

**For EACH epoch:**
1. Generate **50 stratified random points per class** (250 total) using Create Accuracy Assessment Points
2. Verify each point against:
   - Google Earth Pro historical imagery
   - Original satellite composite (visual interpretation)
3. Compute Accuracy Assessment tool → Confusion Matrix
4. Record: **Overall Accuracy, Kappa, Producer's/User's Accuracy per class**
5. Target: OA ≥ 85%, Kappa ≥ 0.80

**Output per epoch:** Confusion matrix table, accuracy statistics

## Step 2.6: Urban Expansion Quantification

### 2.6.1 Area Statistics
For each `lulc_YYYY_final.tif`:
- Raster to Polygon → Dissolve by ClassID
- Calculate Geometry → Area (km²)
- Record built-up area per epoch in table

### 2.6.2 Change Detection Matrices
For consecutive epoch pairs (1990→2000, 2000→2010, 2010→2020, 2020→2025):
1. Combine tool (Spatial Analyst → Local → Combine)
2. Input: `lulc_YYYY_final.tif` + `lulc_YYYY+1_final.tif`
3. Export attribute table → cross-tabulation (from-to matrix)
4. Calculate area converted from each class TO Built-up

### 2.6.3 Annual Expansion Rate

```
Annual Growth Rate (%) = [(Area_t2 / Area_t1)^(1/(t2-t1)) - 1] × 100
```

### 2.6.4 Expansion Direction Analysis
1. For each epoch's built-up class → calculate centroid (Mean Center tool)
2. Plot centroid shift across epochs → shows dominant expansion direction
3. Directional Distribution (Standard Deviational Ellipse) for each epoch's built-up patches

### 2.6.5 Urban Sprawl Index (Shannon's Entropy)
```
H = -Σ(Pi × ln(Pi)) / ln(n)
```
Where Pi = proportion of built-up in zone i, n = number of zones. H closer to 1 = dispersed sprawl; closer to 0 = compact growth.

**Module 2 Outputs:**
- 5 classified LULC maps
- 5 accuracy assessment reports
- Urban area statistics table (km² per epoch)
- 4 change detection matrices
- Growth rate chart
- Centroid shift map
- Shannon's Entropy values

---

# MODULE 3: Shoreline Change Analysis — DSAS (RO2-A)

**Duration:** ~2 weeks | **Prerequisite:** Module 1 imagery ready

## Step 3.1: Shoreline Extraction

**For EACH epoch:**

1. Compute MNDWI from the epoch composite:
   ```
   MNDWI = (Green - SWIR1) / (Green + SWIR1)
   ```
2. Apply threshold: MNDWI > 0 = Water; MNDWI ≤ 0 = Land
3. Reclassify → binary raster (Land=1, Water=0)
4. Raster to Polygon → select the land-water boundary
5. Convert to polyline → this is the raw shoreline
6. Manually edit to remove inland water edges (lagoons, rivers) — keep ONLY the ocean-facing coastline
7. Smooth Line tool (PAEK algorithm, 50m tolerance) for cleaner geometry
8. Save as `shoreline_YYYY.shp`

**Validation:** Overlay each extracted shoreline on its source imagery + Google Earth Pro historical imagery. Manually adjust where automated extraction is inaccurate (shadows, wet sand confusion).

## Step 3.2: DSAS Setup (ArcGIS Pro)

1. Install **DSAS v5.1** add-in for ArcGIS Pro (from USGS website)
2. Create DSAS geodatabase: `shoreline_analysis.gdb`
3. Create required feature classes following DSAS schema:
   - **Baseline:** Digitize a baseline OFFSHORE (seaward of all shorelines), parallel to coast, ~200m offshore
   - **Shorelines:** Merge all epoch shorelines into single feature class with `Date` field (format: MM/DD/YYYY)
   - Add required fields: `Date_`, `Uncertainty` (set to 15m for Landsat, 5m for Sentinel-2)

## Step 3.3: Generate Transects

1. DSAS toolbar → Cast Transects
2. Parameters:
   - Transect spacing: **50 meters**
   - Transect length: **500 meters** (landward + seaward)
   - Smoothing distance: 250m
3. Review transects — delete any that cross land promontories or intersect incorrectly

## Step 3.4: Compute Change Statistics

1. DSAS → Calculate Change Statistics
2. Select ALL statistics:
   - **NSM** (Net Shoreline Movement): total distance of change (meters)
   - **EPR** (End Point Rate): NSM / time span (m/yr)
   - **LRR** (Linear Regression Rate): best-fit line through all positions (m/yr)
   - **WLR** (Weighted Linear Regression): weights by shoreline uncertainty
   - **SCE** (Shoreline Change Envelope): total movement range
3. Output appended to transect attribute table

## Step 3.5: Interpret & Map Results

1. Symbolize transects by **EPR** value:
   - Red (< -1.0 m/yr) = Severe erosion
   - Orange (-1.0 to -0.5) = Moderate erosion
   - Yellow (-0.5 to 0) = Slight erosion
   - Green (0 to +0.5) = Slight accretion
   - Blue (> +0.5) = Significant accretion
2. Create summary table: mean EPR, max retreat, max accretion, % eroding transects
3. Identify **hotspot erosion zones** for later overlay with urban expansion

**Module 3 Outputs:**
- 5 epoch shoreline vectors
- DSAS transect feature class with EPR, LRR, NSM, SCE
- Shoreline change rate map (symbolized transects)
- Summary statistics table
- Erosion hotspot identification

---

# MODULE 4: Slope & Terrain Analysis (RO2-B)

**Duration:** ~2 weeks | **Prerequisite:** Module 1 DEMs ready

## Step 4.1: Slope Map Generation

1. Input: `dem_srtm_30m.tif` (or ALOS 12.5m for higher detail)
2. Spatial Analyst → Surface → Slope
   - Output measurement: **Degrees**
3. Save as `slope_degrees.tif`
4. Reclassify into geomorphic significance classes:

| Class | Slope Range | Geomorphic Significance |
|---|---|---|
| 1 | 0°–2° | Flat — flood/waterlogging prone |
| 2 | 2°–5° | Gentle — suitable for development |
| 3 | 5°–15° | Moderate — erosion potential if disturbed |
| 4 | 15°–25° | Steep — high erosion risk with urbanization |
| 5 | >25° | Very steep — mass movement/landslide risk |

## Step 4.2: Aspect Map

1. Spatial Analyst → Surface → Aspect
2. Save as `aspect_degrees.tif`
3. Reclassify into 8 cardinal directions + Flat
4. **Use for:** identifying slopes facing prevailing rain direction (SW monsoon) → higher erosion exposure

## Step 4.3: Curvature Analysis

1. Spatial Analyst → Surface → Curvature
   - Generate: Profile Curvature + Plan Curvature
2. Profile curvature: negative = convex (erosion), positive = concave (deposition)
3. Plan curvature: identifies convergent flow paths → gully erosion risk

## Step 4.4: Topographic Wetness Index (TWI)

```
TWI = ln(Contributing Area / tan(Slope))
```

**Steps:**
1. Fill DEM → Flow Direction (D8) → Flow Accumulation
2. Calculate contributing area: `(FlowAcc + 1) × cell_size²`
3. Slope in radians: `slope_rad = slope_degrees × π / 180`
4. Raster Calculator: `Ln(("contrib_area") / Tan("slope_rad"))`
5. High TWI = saturation/flood prone areas

## Step 4.5: Hillshade (Visualization)

1. Spatial Analyst → Surface → Hillshade
2. Azimuth: 315°, Altitude: 45°
3. Use as basemap for all terrain-related map layouts

## Step 4.6: Slope Instability Zone Identification

Combine multiple terrain factors:
1. Select areas where: **Slope > 15° AND Curvature < 0 (convex) AND TWI > threshold**
2. Overlay with LULC: identify steep slopes that were **vegetated in 1990 but urbanized by 2025**
3. These are the **highest-risk geomorphic change zones**
4. Save as `slope_instability_zones.shp`

**Module 4 Outputs:**
- Slope map (degrees + reclassified)
- Aspect map
- Profile & plan curvature rasters
- TWI raster
- Hillshade basemap
- Slope instability zone map
