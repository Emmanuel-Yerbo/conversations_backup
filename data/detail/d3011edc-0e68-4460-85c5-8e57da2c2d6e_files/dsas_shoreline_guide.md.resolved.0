# Module 3: Shoreline Change Analysis (DSAS) — Complete Step-by-Step Guide
## Cape Coast Metropolis, Ghana

> [!IMPORTANT]
> This guide walks you through **every single step** from extracting shorelines in GEE to producing your final erosion/accretion map. Follow it in order.

---

## What Is DSAS and Why Do We Use It?

**DSAS** (Digital Shoreline Analysis System) is a free tool made by the USGS that measures how much a shoreline has moved over time.

**How it works (simple analogy):**
Imagine you stand on a fixed point on the beach and measure the distance to the water's edge every year. After 5 years, you can tell if the beach is shrinking (erosion) or growing (accretion), and how fast. DSAS does exactly this — but at hundreds of points along the entire coastline simultaneously.

**Key terms you need to know:**

| Term | What It Means (Simple) |
|---|---|
| **Baseline** | A fixed reference line you draw offshore (in the sea). All measurements start from here. |
| **Shoreline** | The land-water boundary extracted from your satellite image for a specific year. |
| **Transect** | A straight line drawn perpendicular from the baseline toward land. DSAS measures where each shoreline crosses each transect. |
| **EPR** (End Point Rate) | How fast the shoreline moved (m/yr) between the oldest and newest shoreline only. |
| **LRR** (Linear Regression Rate) | A best-fit line through ALL shoreline positions — more statistically robust than EPR. |
| **NSM** (Net Shoreline Movement) | Total distance (in meters) the shoreline moved between the oldest and newest position. |
| **SCE** (Shoreline Change Envelope) | The total range of movement across ALL shoreline positions. |

```
        OCEAN (seaward)
  ═══════════════════════════  ← Baseline (fixed reference)
        |     |     |     |   ← Transects (perpendicular lines)
  ------+-----+-----+-----+--  ← Shoreline 1990
    ----+---+-+-----+---+-----  ← Shoreline 2000
      --+--+--+---+-+--+------  ← Shoreline 2010
        +-+---+--+--+-+-------  ← Shoreline 2020
        LAND (landward)

  Where each transect crosses each shoreline = a measurement point.
  DSAS calculates how far apart these crossing points are over time.
```

---

## The Big Picture: 3-Phase Workflow

```
PHASE A: Extract shorelines from satellite imagery (GEE)
    ↓
PHASE B: Prepare data for DSAS (ArcGIS Pro)
    ↓
PHASE C: Run DSAS analysis & map results
```

---

# PHASE A: Shoreline Extraction in Google Earth Engine

## Why GEE?
You already have your composites in GEE. We will use a water index called **MNDWI** (Modified Normalized Difference Water Index) to automatically detect where the ocean meets the land.

**MNDWI Formula:**
```
MNDWI = (Green - SWIR1) / (Green + SWIR1)
```
- Water has **positive** MNDWI values (water reflects green, absorbs SWIR)
- Land has **negative** MNDWI values

By setting a threshold (usually MNDWI > 0), we separate water from land. The boundary between them = the shoreline.

---

## Step A1: Shoreline Extraction Script (Landsat 7 — for 2000 epoch)

> [!NOTE]
> You need to repeat this for **each epoch**. I provide the Landsat 7 version below. The only things that change between epochs are the collection ID, band names, and dates.

```javascript
// ============================================
// SHORELINE EXTRACTION — EPOCH: 2000
// Sensor: Landsat 7 ETM+ (Collection 2, Level 2)
// ============================================

// Step 1: Cloud masking function (same as your LULC script)
function maskL7sr(image) {
  var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
  var saturationMask = image.select('QA_RADSAT').eq(0);
  var opticalBands = image.select('SR_B.*').multiply(0.0000275).add(-0.2);
  var thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0);
  return image.addBands(opticalBands, null, true)
      .addBands(thermalBands, null, true)
      .updateMask(qaMask)
      .updateMask(saturationMask);
}

// Step 2: Build composite (median is better for shoreline work)
var collection = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
    .filterDate('2000-01-01', '2002-12-31')
    .filterBounds(roi)
    .map(maskL7sr);

var composite = collection.median().clip(roi).unmask(0);

// Step 3: Compute MNDWI
// Landsat 7 bands: Green = SR_B2, SWIR1 = SR_B5
var mndwi = composite.normalizedDifference(['SR_B2', 'SR_B5']).rename('MNDWI');

// Step 4: Create binary water mask (Water = 1, Land = 0)
var waterMask = mndwi.gt(0).selfMask();

// Step 5: Visualize to verify before exporting
Map.centerObject(roi, 12);
Map.addLayer(mndwi, {min: -0.5, max: 0.5, palette: ['brown', 'white', 'blue']}, 'MNDWI 2000');
Map.addLayer(waterMask, {palette: ['cyan']}, 'Water Mask 2000');

// Step 6: Convert the water boundary to a vector (polyline)
// First, detect the edge of the water mask
var edge = waterMask.reduceNeighborhood({
  reducer: ee.Reducer.countDistinctNonNull(),
  kernel: ee.Kernel.square(1)
}).gt(1).selfMask();

// Convert edge pixels to vector
var shorelineVector = edge.reduceToVectors({
  geometry: roi,
  scale: 30,
  geometryType: 'polygon',
  eightConnected: true,
  maxPixels: 1e10,
  tileScale: 4
});

// Step 7: Export as Shapefile to Google Drive
Export.table.toDrive({
  collection: shorelineVector,
  description: 'Shoreline_2000',
  folder: 'DSAS_Shorelines',
  fileFormat: 'SHP'
});

print('Shoreline 2000 — run the export task in the Tasks tab');
```

---

## Step A2: Band Names Reference for Each Epoch

Use this table to adapt the script for each sensor:

| Epoch | Sensor | Collection ID | Green Band | SWIR1 Band |
|---|---|---|---|---|
| ~1990 | Landsat 5 TM | `LANDSAT/LT05/C02/T1_L2` | `SR_B2` | `SR_B5` |
| ~2000 | Landsat 7 ETM+ | `LANDSAT/LE07/C02/T1_L2` | `SR_B2` | `SR_B5` |
| ~2010 | Landsat 5 TM | `LANDSAT/LT05/C02/T1_L2` | `SR_B2` | `SR_B5` |
| ~2020 | Landsat 8 OLI | `LANDSAT/LC08/C02/T1_L2` | `SR_B3` | `SR_B6` |
| ~2025 | Landsat 9 OLI-2 | `LANDSAT/LC09/C02/T1_L2` | `SR_B3` | `SR_B6` |

> [!WARNING]
> For each epoch, change **3 things** in the script:
> 1. The `ImageCollection` ID (from the table above)
> 2. The `.filterDate()` range
> 3. The band names inside `.normalizedDifference()` (Green and SWIR1 from the table)

---

## Step A3: Alternative — Manual Digitization (More Accurate)

If the automated extraction gives messy results (common in lagoon areas), you can **manually digitize** the shoreline in GEE or ArcGIS:

1. Display your **True Color composite** for the epoch
2. Zoom into the coastline
3. Use the **line drawing tool** to trace the water-land boundary
4. Export the drawn line as a shapefile

> [!TIP]
> **Best practice for academic work:** Use automated MNDWI extraction first, then **manually clean** the result in ArcGIS Pro by deleting inland water edges and smoothing the coastline. This gives you the best of both worlds.

---

# PHASE B: Prepare Data for DSAS

## Important Update About DSAS Versions

| Version | Runs Inside | Status |
|---|---|---|
| DSAS v5.1 | ArcMap 10.4–10.7 (old desktop) | Still works if you have ArcMap |
| **DSAS v6.0/6.1** | **Standalone application** (separate program) | **Current recommended version** |

> [!IMPORTANT]
> **DSAS v5.1 does NOT work inside ArcGIS Pro.** If you only have ArcGIS Pro, download **DSAS v6.1** (standalone) from: https://www.usgs.gov/centers/whcmsc/science/digital-shoreline-analysis-system-dsas

---

## Step B1: Download and Install DSAS v6

1. Go to https://www.usgs.gov/centers/whcmsc/science/digital-shoreline-analysis-system-dsas
2. Download `DSAS_v6.1_setup.exe`
3. Install it (standard Windows installer)
4. It runs as its own program — no ArcGIS needed for the analysis itself

---

## Step B2: Download Your Exported Shorelines

1. Go to your **Google Drive** → folder `DSAS_Shorelines`
2. Download all 5 zipped shapefiles:
   - `Shoreline_1990.zip`
   - `Shoreline_2000.zip`
   - `Shoreline_2010.zip`
   - `Shoreline_2020.zip`
   - `Shoreline_2025.zip`
3. Unzip each into a folder on your computer (e.g., `C:\DSAS_Project\shorelines\`)

---

## Step B3: Clean Shorelines in ArcGIS Pro

This is the most important preparation step. Raw extracted shorelines are messy — they include lagoon edges, river banks, and noise. You need **only the ocean-facing coastline**.

### For each shoreline shapefile:

1. **Open ArcGIS Pro** → Add the shoreline shapefile to a new map
2. **Set CRS** to **UTM Zone 30N (EPSG:32630)** — this is critical; DSAS needs meters
3. **If the CRS is wrong:** Use the Project tool (Data Management → Projections → Project) to reproject
4. **Start Editing** (Edit tab → Create)
5. **Delete** all features that are NOT the ocean coastline:
   - Delete inland water boundaries (lagoons, rivers, ponds)
   - Delete features outside your coastal study area
6. **Keep only** the single continuous line along the ocean coast
7. **Smooth the line** (optional but recommended):
   - Cartography → Generalization → Smooth Line
   - Algorithm: PAEK, Tolerance: 50m
8. **Save edits** and export as a new shapefile: `shoreline_2000_clean.shp`

```
BEFORE CLEANING:                    AFTER CLEANING:
┌──────────────────┐                ┌──────────────────┐
│  ~~~ lagoon ~~~  │                │                  │
│  ///             │                │                  │
│ /// river ///    │                │                  │
│                  │                │                  │
│==================│ ← coastline   │==================│ ← KEEP ONLY THIS
│   OCEAN          │                │   OCEAN          │
└──────────────────┘                └──────────────────┘
```

---

## Step B4: Add Required Date and Uncertainty Fields

DSAS needs to know **when** each shoreline was captured and **how accurate** it is.

### In ArcGIS Pro, for each cleaned shoreline:

1. Open the **Attribute Table**
2. **Add Field** → `Date_` (Type: **Date**)
3. **Add Field** → `Uncertainty` (Type: **Double**)
4. **Populate the fields:**

| Shoreline File | Date_ Value | Uncertainty Value |
|---|---|---|
| `shoreline_1990_clean.shp` | `01/01/1990` | `15` |
| `shoreline_2000_clean.shp` | `01/01/2000` | `15` |
| `shoreline_2010_clean.shp` | `01/01/2010` | `15` |
| `shoreline_2020_clean.shp` | `01/01/2020` | `15` |
| `shoreline_2025_clean.shp` | `01/01/2025` | `10` |

> [!NOTE]
> **Why 15m uncertainty for Landsat?** Landsat has 30m pixels, so the shoreline position could be off by up to half a pixel (15m). Sentinel-2 has 10m pixels → 5m uncertainty. If you used Landsat for 2025, use 15m.

---

## Step B5: Merge All Shorelines Into One File

DSAS expects **all shorelines in a single feature class/shapefile**.

### In ArcGIS Pro:
1. **Geoprocessing** → Search for **Merge**
2. Input: all 5 cleaned shoreline shapefiles
3. Output: `all_shorelines_merged.shp`
4. Verify: Open the attribute table — you should see features with different `Date_` values

---

## Step B6: Create the Baseline

The baseline is a **fixed reference line** from which DSAS measures distances to each shoreline. Think of it as your "measuring tape starting point."

### Rules for creating a baseline:
- It must be **offshore** (seaward of ALL your shorelines, including the oldest one)
- It must be **roughly parallel** to the general coastline direction
- It should be about **200–500m offshore**

### In ArcGIS Pro:
1. **Create** → New Feature Class → Type: **Polyline** → Name: `baseline.shp`
2. Set CRS to **UTM Zone 30N (EPSG:32630)**
3. **Start Editing**
4. Zoom to the coast and draw a single smooth line **offshore**, parallel to the coast
5. The line should extend slightly beyond the study area on both ends
6. **Save edits**

```
     N
     ↑
     │
─────┼─── baseline (200-500m offshore) ──────
     │
~~~~~│~~~~~ shoreline 2025 ~~~~~
     │
- - -│- - - shoreline 1990 - - -
     │
█████│█████ LAND ███████████████
```

---

# PHASE C: Run DSAS Analysis

## Step C1: Open DSAS v6 and Load Data

1. **Launch DSAS v6** application
2. **Create New Project**
3. **Import Baseline:** Browse to `baseline.shp`
4. **Import Shorelines:** Browse to `all_shorelines_merged.shp`
5. Set the **date field** to `Date_`
6. Set the **uncertainty field** to `Uncertainty`

---

## Step C2: Generate Transects

1. In DSAS, go to **Cast Transects**
2. Set parameters:

| Parameter | Value | Why |
|---|---|---|
| Transect Spacing | **50 meters** | One measurement every 50m along the coast |
| Transect Length | **500 meters** | Long enough to cross all shorelines |
| Smoothing Distance | **250 meters** | Smooths the baseline to avoid jagged transects |
| Cast Direction | **Onshore** (landward from baseline) | Because your baseline is offshore |

3. Click **Generate** — DSAS creates hundreds of perpendicular lines from the baseline toward land

---

## Step C3: Calculate Rate-of-Change Statistics

1. Go to **Calculate Statistics**
2. Select **ALL** statistics:
   - ☑ **NSM** — Net Shoreline Movement (meters)
   - ☑ **EPR** — End Point Rate (m/yr)
   - ☑ **LRR** — Linear Regression Rate (m/yr)
   - ☑ **WLR** — Weighted Linear Regression Rate (m/yr)
   - ☑ **SCE** — Shoreline Change Envelope (meters)
3. Click **Calculate**

### What each statistic tells you:

| Statistic | What It Measures | Interpretation |
|---|---|---|
| **NSM** | Total distance moved (m) | Positive = accretion, Negative = erosion |
| **EPR** | Rate using only oldest & newest shoreline (m/yr) | Quick snapshot of overall trend |
| **LRR** | Rate using ALL shorelines via regression (m/yr) | Most statistically robust — **use this in your thesis** |
| **WLR** | Same as LRR but weights by uncertainty | Even better if uncertainties vary between epochs |
| **SCE** | Total range of all movement (m) | Shows overall variability |

---

## Step C4: Export Results

1. DSAS v6 saves results as a **GeoPackage** (`.gpkg`) or shapefile
2. Export the transect results
3. Open in **ArcGIS Pro** for mapping

---

## Step C5: Map and Interpret Results in ArcGIS Pro

### Symbolize transects by EPR:

1. Add the transect output to ArcGIS Pro
2. Right-click → **Symbology** → Graduated Colors
3. Field: `EPR` (or `LRR`)
4. Use this classification:

| Color | EPR Range (m/yr) | Meaning |
|---|---|---|
| 🔴 Dark Red | < -1.5 | Severe erosion |
| 🟠 Orange | -1.5 to -0.5 | Moderate erosion |
| 🟡 Yellow | -0.5 to 0.0 | Slight erosion |
| 🟢 Green | 0.0 to +0.5 | Slight accretion |
| 🔵 Blue | > +0.5 | Significant accretion |

### Create Summary Statistics Table:

Calculate these for your thesis:

| Metric | How to Calculate |
|---|---|
| Mean EPR | Average of all transect EPR values |
| Max erosion rate | Minimum EPR value (most negative) |
| Max accretion rate | Maximum EPR value (most positive) |
| % of transects eroding | Count(EPR < 0) / Total transects × 100 |
| % of transects accreting | Count(EPR > 0) / Total transects × 100 |
| Total shoreline length analyzed | Number of transects × spacing (50m) |

---

# PHASE D: Connect DSAS Results to Urban Expansion (for Module 5 later)

After completing the DSAS analysis, you will overlay the erosion/accretion results with your LULC change maps. This comes in Module 5, but here's a preview of the questions you'll answer:

- Did areas with **high urban growth** near the coast experience **more erosion**?
- Are **eroding zones** expanding into areas that are now **built-up**?
- Which settlements are most at risk from continued shoreline retreat?

---

# Troubleshooting Common Problems

| Problem | Cause | Solution |
|---|---|---|
| MNDWI shoreline is jagged | 30m Landsat pixels create staircase effect | Smooth the line in ArcGIS (PAEK, 50m tolerance) |
| Lagoons detected as shoreline | MNDWI picks up all water bodies | Manually delete inland water edges in editing |
| DSAS won't generate transects | Baseline not in projected CRS (meters) | Reproject baseline to UTM Zone 30N |
| Transects cross each other | Baseline too curvy or too close to coast | Smooth baseline or move it further offshore |
| No shoreline intersection found | Transect too short or shoreline has gap | Increase transect length or fill shoreline gaps |
| EPR values seem extreme | One shoreline is misaligned | Check all shorelines overlay correctly on imagery |

---

# Checklist: Module 3 Deliverables

- [ ] 5 cleaned shoreline shapefiles (one per epoch)
- [ ] 1 merged shoreline file with Date_ and Uncertainty fields
- [ ] 1 baseline shapefile
- [ ] DSAS transect output with EPR, LRR, NSM, SCE statistics
- [ ] Shoreline change rate map (transects colored by EPR/LRR)
- [ ] Summary statistics table (mean EPR, % eroding, max rates)
- [ ] Erosion hotspot zones identified for Module 5 overlay
