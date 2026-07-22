# Shoreline Change Data Analysis Report
*Cape Coast Coastline Dynamics (2000 – 2023) — Digital Earth Africa Specifications*

This report analyzes the shoreline change data for Cape Coast, Ghana, using the official specifications of the **Digital Earth Africa (DE Africa) Coastlines** monitoring service.

---

## 1. Technical Framework & Dataset Specifications

The datasets (`SHORE.shp` and `CHANTE_STATS.shp`) are derived from the continental DE Africa Coastlines program.

### A. Core Methodology
* **Source Imagery:** Landsat Collection 2 Surface Reflectance (30-meter spatial resolution).
* **Water Delineation Index:** Modified Normalized Difference Water Index (MNDWI):
  $$\text{MNDWI} = \frac{\text{Green} - \text{SWIR}}{\text{Green} + \text{SWIR}}$$
  Values $> 0$ are classified as water.
* **Tidal Correction:** To isolate true geomorphic change from tidal fluctuations, the method integrates **tidal modeling** to map the shoreline position at Mean Sea Level (MSL) (**0 m Above Mean Sea Level**).
* **Sub-Pixel Delineation:** Sub-pixel waterline extraction algorithms are applied, allowing horizontal accuracy far finer than the raw 30m cell size.

### B. Validation & Accuracy in Ghana
* The dataset has been rigorously validated in West Africa by the **Centre de Suivi Ecologique (CSE), Dakar** in collaboration with the **WACA/ORLOA** (West Africa Coastal Areas Management Program) network.
* Validation using sub-meter **WorldView satellite imagery** in Ghana (acquired October 31, 2018) confirms an average **Root Mean Square Error (RMSE) of ~5 to 9 meters** (sub-pixel accuracy), making the dataset highly reliable for academic research.

---

## 2. Statistical Definitions & Cape Coast Results

The 187 transect points (`CHANTE_STATS.shp`) spaced every 30 meters along the Cape Coast littoral zone provide the following metrics:

### A. Linear Regression Rate (`rate_time` / LRR)
* **Definition:** The annual rate of change (meters/year) calculated by fitting a least-squares linear regression through all cloud-free, tide-corrected annual shoreline positions (excluding outliers identified via Median Absolute Deviation).
* **Cape Coast Results:**
  * **Mean Rate of Change:** **`+0.03 m/yr`** (Indicates overall dynamic equilibrium, but hides significant spatial variations).
  * **Eroding Transects (Rate < 0):** **98 transects (52.4%)** — maximum erosion rate of **`-1.26 m/yr`**.
  * **Accreting Transects (Rate > 0):** **89 transects (47.6%)** — maximum accretion rate of **`+1.53 m/yr`**.

### B. Net Shoreline Movement (`nsm` / NSM)
* **Definition:** The net horizontal distance (meters) between the oldest shoreline (2000) and the most recent shoreline (2023). It represents the net shoreline shift but does not capture intermediate fluctuations.
* **Cape Coast Results:**
  * **Average Net Movement:** **`+2.19 meters`** (Seaward).
  * **Maximum Landward Shift (Erosion):** **`-23.55 meters`** (Net land lost).
  * **Maximum Seaward Shift (Accretion):** **`+84.33 meters`** (Net land gained).

### C. Shoreline Change Envelope (`sce` / SCE)
* **Definition:** The maximum horizontal distance (meters) between any two annual shorelines, regardless of year. It measures the total width of the shoreline migration corridor (envelope of variability) over the 24-year period.
* **Cape Coast Results:**
  * **Mean SCE:** **`23.07 meters`** (Average lateral movement band).
  * **Maximum SCE:** **`44.74 meters`** (Maximum localized shoreline stability swing).

---

## 3. Visualizations

### Annual Shorelines (`SHORE.shp`)
Shows the annual vector shorelines at 0 m MSL.
![SHORE Plot](file:///C:/Users/LENOVO/.gemini/antigravity/brain/d3011edc-0e68-4460-85c5-8e57da2c2d6e/shore_plot.png)

### Transect Rates (`CHANTE_STATS.shp`)
Displays the 187 points along the Cape Coast sector where the rates were calculated.
![CHANTE_STATS Plot](file:///C:/Users/LENOVO/.gemini/antigravity/brain/d3011edc-0e68-4460-85c5-8e57da2c2d6e/chante_stats_plot.png)

---

## 4. Academic Interpretation for Cape Coast
The data shows a highly active coastline. With **52.4% of the transects undergoing erosion**, coastal retreat is the dominant geomorphic threat. The localized hotspots reaching **$-1.26\text{ m/yr}$** of erosion represent significant threats to coastal infrastructure, particularly where built-up areas (from your LULC maps) encroach directly onto the beach. The accretion hot spots (up to $+1.53\text{ m/yr}$) likely correspond to areas of coastal defense structures (groynes, revetments) or natural deposition zones.
