# Detailed Implementation Guide — Part 2 of 2
## Cape Coast Urban Expansion × Geomorphic Features Analysis

> [!IMPORTANT]
> This guide covers the final analytical stages of your project: **Module 5** (Relationship Overlay & Spatial Statistics), **Module 6** (Hazard Vulnerability Mapping), and **Module 7** (Policy Integration & Map Production).

---

# MODULE 5: Spatiotemporal Relationship Analysis (RO3)

**Duration:** ~3 weeks | **Prerequisite:** Modules 2 (LULC) and 4 (Terrain) complete

The goal of this module is to mathematically and spatially prove **how** urban expansion has encroached onto and altered the geomorphic landscape (slopes and drainage systems).

## Step 5.1: Spatial Overlay Analysis (ArcGIS Pro)

### 5.1.1 Built-up Encroachment on Slopes (Slope Encroachment)
You will calculate how much built-up area has moved onto steep, unstable slopes over the years (1990, 2000, 2010, 2020, 2025).

1. In ArcGIS Pro, open **Tabulate Area** (*Spatial Analyst Tools → Zonal → Tabulate Area*).
2. Set the following parameters:
   - **Input raster or feature zone data:** Your reclassified Slope raster (`slope_classes.tif`).
   - **Zone field:** `Value` (representing Slope Classes 1 to 5).
   - **Input raster class data:** LULC map for Year 1 (`lulc_1990.tif`).
   - **Class field:** `Value` (representing Class 1: Built-up, Class 2: Veg, etc.).
   - **Output table:** `encroachment_1990.dbf`.
3. Repeat this tool for all 5 epochs (1990, 2000, 2010, 2020, 2025).
4. Combine the tables in Excel to show the increase in built-up area (in $km^2$) on slopes $>15^\circ$ (Slope classes 4 and 5) over time.

### 5.1.2 Built-up Encroachment on Flood-Prone Areas (TWI Encroachment)
Identify if urbanization is expanding into wet, low-lying zones (valleys and floodplains).

1. Reclassify your TWI raster into 3 classes:
   - *Low TWI (1–5):* Dry slopes (low flood risk)
   - *Moderate TWI (5–9):* Transitional slopes
   - *High TWI (> 9):* Valleys / accumulation zones (high flood risk)
2. Run **Tabulate Area** using the reclassified TWI as the zone layer and your LULC rasters as the class data.
3. Record the total built-up area ($km^2$) inside the **High TWI** class across all epochs.

---

## Step 5.2: Grid-Based Statistical Correlation (Python / R / Excel)

To perform statistical correlation (RO3), you must divide the study area into a grid to extract localized values.

```
┌───────┬───────┬───────┐
│ Cell 1│ Cell 2│ Cell 3│  ← 500m Grid Cells
├───────┼───────┼───────┤
│ Cell 4│ Cell 5│ Cell 6│  ← For each cell, extract:
│       │       │       │    1. % Built-up Increase
└───────┴───────┴───────┘    2. Mean Slope / Mean TWI
```

### 5.2.1 Create Analysis Grid
1. Run **Create Fishnet** (*Data Management Tools → Sampling → Create Fishnet*).
   - **Output Feature Class:** `analysis_grid.shp`
   - **Template Extent:** Same as `study_area_boundary.shp`
   - **Cell Size Width / Height:** `500` (meters)
   - **Geometry Type:** `Polygon`
2. Clip the resulting grid to your study area boundary (`study_area_boundary.shp`).

### 5.2.2 Extract Spatial Variables per Grid Cell
For each grid cell polygon, you will extract the average terrain characteristics and the change in built-up area:

1. **Calculate Slope per Cell:** 
   - Run **Zonal Statistics as Table** (*Spatial Analyst → Zonal*).
   - Input Zone: `analysis_grid.shp` (Zone field: `FID` / `OBJECTID`).
   - Input Value Raster: `slope_degrees.tif` (or `twi.tif`).
   - Statistics Type: `Mean`.
   - Join the output table back to `analysis_grid.shp` based on the ID field.
2. **Calculate Built-up Change per Cell:**
   - For 1990 LULC, run **Zonal Histogram** to count the number of Built-up pixels in each grid cell. Repeat for 2025 LULC.
   - Calculate the change: $\Delta \text{Built-up} = \text{Built-up}_{2025} - \text{Built-up}_{1990}$.
   - Add this change value to the grid attribute table.

### 5.2.3 Run Correlation (Python Script)
Export the attribute table of your `analysis_grid.shp` as a CSV file (`grid_data.csv`). Use this Python code (which you can run locally or in Jupyter/ArcGIS Pro Notebooks) to calculate correlation coefficients:

```python
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('grid_data.csv')

# Variables:
# 'built_change' = Built-up increase (%)
# 'mean_slope' = Mean slope in degrees
# 'mean_twi' = Mean Topographic Wetness Index
# 'elev_range' = Elevation relief (max - min)

# 1. Pearson Correlation
pearson_slope, p_slope = stats.pearsonr(df['built_change'], df['mean_slope'])
pearson_twi, p_twi = stats.pearsonr(df['built_change'], df['mean_twi'])

print(f"Built-up Change vs Slope: r = {pearson_slope:.3f} (p-value = {p_slope:.3e})")
print(f"Built-up Change vs TWI: r = {pearson_twi:.3f} (p-value = {p_twi:.3e})")

# 2. Plot Relationship
plt.figure(figsize=(10, 5))
sns.regplot(data=df, x='mean_slope', y='built_change', scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
plt.title('Urban Expansion vs. Slope Gradient in Cape Coast')
plt.xlabel('Mean Slope (Degrees)')
plt.ylabel('Built-up Area Increase (%)')
plt.savefig('slope_urban_correlation.png', dpi=300)
plt.show()
```

---

# MODULE 6: Hazard Susceptibility Mapping (RO4)

**Duration:** ~2 weeks | **Prerequisite:** Modules 2, 4, and 5 complete

You will combine your geomorphic change maps (Slope, TWI, and LULC) into a single hazard susceptibility map using a **Weighted Overlay** (Analytical Hierarchy Process - AHP).

## Step 6.1: Prepare Input Rasters
All input rasters must be reclassified into a standardized scale of **1 to 5** (1 = Very Low Susceptibility, 5 = Very High Susceptibility).

### 1. Reclassify Slope (`slope_susceptibility.tif`)
- $0^\circ - 5^\circ$ → Class 1 (Very Low risk of slope failure)
- $5^\circ - 15^\circ$ → Class 2
- $15^\circ - 25^\circ$ → Class 4
- $> 25^\circ$ → Class 5 (Very High landslide risk)

### 2. Reclassify TWI (`flood_susceptibility.tif`)
- TWI $< 4$ → Class 1 (Very Low risk of water accumulation)
- TWI $4 - 7$ → Class 2
- TWI $7 - 10$ → Class 4
- TWI $> 10$ → Class 5 (Very High flooding risk)

### 3. Reclassify LULC (`landuse_susceptibility.tif`)
*Built-up and bare soils increase run-off and erosion.*
- Water / Vegetation → Class 1 (Stable land cover)
- Agriculture / Sparse Veg → Class 2
- Bare Soil → Class 4
- Built-up (Impervious) → Class 5 (High runoff generation)

---

## Step 6.2: Weighted Overlay
You will merge these factors together using the **Weighted Overlay** tool (*Spatial Analyst Tools → Overlay → Weighted Overlay*).

### Weighting Scheme (AHP-derived):
*   **Slope Susceptibility:** **40%**
*   **TWI (Flood Susceptibility):** **40%**
*   **LULC Susceptibility:** **20%**

```
[Slope Class x 0.40] + [TWI Class x 0.40] + [LULC Class x 0.20] = Hazard Score (1 to 5)
```

1. Add your three reclassified rasters to the tool.
2. Set the scale values for each input from **1 to 5**.
3. Assign the percentage weights (40%, 40%, 20%).
4. Set the output to `composite_hazard_map.tif`.
5. Symbolize the output using a green-to-red color ramp:
   - *1 (Green):* Safe / Stable Zone
   - *2 (Light Green):* Low Susceptibility
   - *3 (Yellow):* Moderate Susceptibility
   - *4 (Orange):* High Susceptibility
   - *5 (Red):* Very High Susceptibility (Extreme Risk)

---

## Step 6.3: Risk Exposure Delineation
Identify which settlements and urban expansion vectors are extending directly into these high-risk areas:

1. **Overlay settlements:** Add your 2025 LULC Built-up layer (or local community shapefiles) on top of the `composite_hazard_map.tif`.
2. Extract cells where: **LULC = Built-up AND Hazard Map class = 4 or 5**.
3. Calculate the total built-up area ($km^2$) currently located in high-risk zones.

---

# MODULE 7: Policy & Management Synthesis (RO4)

**Duration:** ~2 weeks | **Prerequisite:** All spatial analysis complete

You will translate your technical maps into planning recommendations to complete your research proposal requirements.

## Step 7.1: Develop the Policy Recommendation Matrix
Include this table in your final thesis chapter to link your spatial findings to physical planning actions:

| Spatial Findings | Identified Risk | Policy / Planning Action | Key SDG |
|---|---|---|---|
| Built-up expansion on slopes $>15^\circ$ | Gully erosion, slope failures, structure collapse | Slope stabilization, tree planting, enforcing slope building codes | **SDG 11** (Sustainable Cities) |
| Rapid built-up expansion in high TWI zones | Localized flooding, waterlogging, disease outbreaks | Sustainable Urban Drainage Systems (SuDS), retention ponds, buffer zones | **SDG 13** (Climate Action) |
| Extensive bare soil creation at urban fringes | High sediment run-off, loss of agricultural land | mandatory vegetation cover during construction, green infrastructure | **SDG 15** (Life on Land) |

## Step 7.2: Final Map Layout Production
Produce three primary high-quality maps for your thesis/publication using ArcGIS Pro layouts:

1. **Map 1: LULC Change (1990–2025):** Showing side-by-side maps of your LULC classes.
2. **Map 2: Geomorphic Factors:** Showing TWI, Slope, Curvature, and Hillshade.
3. **Map 3: Geomorphic Hazard Susceptibility Map:** Showing the final weighted overlay with high-risk zones highlighted.

---

## Deliverables Checklist for Final Thesis Presentation

- [ ] **Encroachment Tables:** Excel sheets showing Built-up expansion on steep slopes and TWI basins.
- [ ] **Correlation Plot:** Scatter plot showing correlation between % urban expansion and slope gradient.
- [ ] **Weighted Hazard Map:** Standardized, A3-format composite hazard layout map.
- [ ] **Exposure Statistics:** Total area ($km^2$) and percentage of built-up elements at risk.
- [ ] **Policy Matrix:** Completed policy/planning recommendation table.
