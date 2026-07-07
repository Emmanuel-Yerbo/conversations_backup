# BASED.ipynb — Notebook Audit & Upgrade Plan

## Current Notebook Structure (75 cells)

| Cell | What It Does | Status |
|:---|:---|:---|
| 0–1 | Coordinate extraction from `.geo` JSON | ✅ Fine |
| 2–7 | Markdown overview docs | ✅ Fine |
| 8–9 | Install torch, rasterio, geopandas | ✅ Fine |
| 10 | Import libraries | ⚠️ Missing `GroupKFold` |
| 11 | Check PyTorch/CUDA | ✅ Fine |
| 12 | Mount Google Drive | ✅ Fine |
| 13–20 | Load CSV, inspect, drop `.geo` | ✅ Fine — **but `.geo` is dropped too early; we need lat/lon from it for spatial blocking** |
| 21–23 | Define features, drop NaN, extract X/y | ✅ Fine |
| 24–26 | Shift labels 1-3 → 0-2, class distribution | ✅ Fine |
| **30** | **`train_test_split` — RANDOM SPLIT** | 🔴 **THIS IS THE PROBLEM** |
| 31–33 | StandardScaler, save scaler | ✅ Fine |
| 34–37 | Dataset, DataLoader | ✅ Fine |
| 38–41 | VegHealthCNN model definition | ✅ Fine |
| 42–44 | Loss/Optimizer/Training loop | ⚠️ Uses Adam not AdamW |
| 45 | Training curves plot | ✅ Fine |
| 46 | Evaluation (confusion matrix) | ✅ Fine |
| 47–59 | AKAA region inference + area calc + plots | ✅ Fine |
| 60–73 | PHMA region inference + area calc + plots | ✅ Fine |
| 74 | Markdown header "VARIABLE RATE FERTILIZER APPLICATION" | 🔴 **Empty — no VRA code** |

---

## What Needs to Change

### Problem 1: Random Split → Spatial Block CV

**Current code (Cell 30):**
```python
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)
```

This is random splitting. Nearby pixels end up in both train and test → spatial data leakage → inflated accuracy (Roberts et al., 2017).

**Fix:** Extract coordinates from `.geo` BEFORE dropping it, assign spatial block IDs, use `GroupKFold`.

### Problem 2: Missing VRA Section

Cell 74 has the markdown header but no code. The VRA logic described in the methodology needs to be implemented.

---

## Exact Code to Add — Copy These into Colab

### STEP 1: Extract Coordinates BEFORE Dropping `.geo`

> **WHERE:** Insert this AFTER Cell 14 (loading CSV) and BEFORE Cell 18 (dropping `.geo`)

```python
# ============================================================
# STEP 1: Extract lat/lon from .geo for Spatial Block CV
# ============================================================
import json

def extract_coords(geo_str):
    """Parse GEE .geo JSON to get lat/lon"""
    geo = json.loads(geo_str)
    lon, lat = geo['coordinates']
    return pd.Series({'lat': lat, 'lon': lon})

coords = df['.geo'].apply(extract_coords)
df['lat'] = coords['lat']
df['lon'] = coords['lon']

print(f"Coordinate range:")
print(f"  Lat: {df['lat'].min():.4f} to {df['lat'].max():.4f}")
print(f"  Lon: {df['lon'].min():.4f} to {df['lon'].max():.4f}")
```

### STEP 2: Assign Spatial Block IDs

> **WHERE:** Insert AFTER Step 1, still before the `.geo` drop

```python
# ============================================================
# STEP 2: Assign Spatial Block IDs (~1.1 km grid)
# ============================================================
BLOCK_SIZE = 0.01  # ~1.1 km at equatorial latitudes

df['block_id'] = (
    (df['lon'] // BLOCK_SIZE).astype(int).astype(str) + '_' +
    (df['lat'] // BLOCK_SIZE).astype(int).astype(str)
)

n_blocks = df['block_id'].nunique()
print(f"Number of spatial blocks: {n_blocks}")
print(f"Block size: {BLOCK_SIZE}° ≈ 1.1 km")
print(f"\nSamples per block:")
print(df['block_id'].value_counts().describe())
```

### STEP 3: Replace Random Split with GroupKFold

> **WHERE:** REPLACE Cell 30 entirely

```python
# ============================================================
# STEP 3: Spatial Block Cross-Validation (GroupKFold)
# Replaces random train_test_split to prevent spatial leakage
# ============================================================
from sklearn.model_selection import GroupKFold

# Prepare arrays
feature_cols = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12',
                'NDVI', 'EVI', 'NDMI', 'SAVI', 'NDRE', 'BSI']
label_col = 'health_class'

x = df[feature_cols].values.astype(np.float32)
y = df[label_col].values.astype(np.int64)

# Shift labels from 1-3 to 0-2
y = y - 1

groups = df['block_id'].values

# GroupKFold with k=5
gkf = GroupKFold(n_splits=5)

# Use the first fold for the primary train/test split
for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(x, y, groups)):
    if fold_idx == 0:
        x_train, x_test = x[train_idx], x[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        train_blocks = set(groups[train_idx])
        test_blocks = set(groups[test_idx])
        break

# Verify NO spatial overlap
overlap = train_blocks.intersection(test_blocks)
assert len(overlap) == 0, f"SPATIAL LEAKAGE DETECTED: {overlap}"

print("=" * 60)
print("SPATIAL BLOCK CROSS-VALIDATION SUMMARY")
print("=" * 60)
print(f"Total samples:      {len(x):,}")
print(f"Training samples:   {len(x_train):,} ({len(x_train)/len(x)*100:.1f}%)")
print(f"Testing samples:    {len(x_test):,} ({len(x_test)/len(x)*100:.1f}%)")
print(f"Training blocks:    {len(train_blocks)}")
print(f"Testing blocks:     {len(test_blocks)}")
print(f"Spatial overlap:    {len(overlap)} (MUST be 0)")
print()
print("Test set class distribution:")
for i, name in enumerate(['Healthy', 'Moderate Stress', 'Non-Vegetation']):
    count = np.sum(y_test == i)
    print(f"  {name}: {count:,} ({count/len(y_test)*100:.1f}%)")
```

### STEP 4: VRA Nitrogen Prescription (Final Section)

> **WHERE:** Add as the LAST section after all inference/plotting cells (after Cell 73)

```python
# ============================================================
# VARIABLE-RATE NITROGEN PRESCRIPTION (NDRE-MODULATED)
# ============================================================
# This implements the two-stage VRA pipeline:
#   Stage 1: Health-class base N rate
#   Stage 2: NDRE spectral refinement
# ============================================================

import rasterio
import numpy as np

# ---- Paths ----
HEALTH_MAP_PATH = '/content/drive/MyDrive/NEURAL NETWORK/data/PHMA_VEG_HEALTH.tif'
STACKED_PATH    = '/content/drive/MyDrive/NEURAL NETWORK/data/PHMA_VEG_2024_DL.tif'
VRA_OUTPUT_PATH = '/content/drive/MyDrive/NEURAL NETWORK/data/PHMA_VRA_Prescription.tif'

# ---- Load health classification map ----
with rasterio.open(HEALTH_MAP_PATH) as src:
    health_map = src.read(1)  # Class labels: 0=Healthy, 1=Stress, 2=NonVeg
    meta = src.meta.copy()
    transform = src.transform

# ---- Extract NDRE from the stacked GeoTIFF ----
# Band order in stacked file: B2,B3,B4,B5,B6,B7,B8,B8A,B11,B12,BSI,EVI,NDMI,NDRE,NDVI,SAVI
# NDRE is band 14 (0-indexed: 13)
with rasterio.open(STACKED_PATH) as src:
    ndre = src.read(14).astype(np.float32)  # Band 14 = NDRE (1-indexed)

# Replace NaN/invalid values
ndre = np.nan_to_num(ndre, nan=0.0)

print(f"Health map shape: {health_map.shape}")
print(f"NDRE shape:       {ndre.shape}")
print(f"NDRE range:       [{ndre.min():.4f}, {ndre.max():.4f}]")
```

```python
# ============================================================
# STAGE 1: Health-Class Base Nitrogen Rate
# ============================================================

base_rate = np.zeros_like(health_map, dtype=np.float32)

# Assign base rates per class
base_rate[health_map == 0] = 80.0    # Healthy: maintenance dose
base_rate[health_map == 1] = 120.0   # Moderate Stress: remedial dose
base_rate[health_map == 2] = 0.0     # Non-Vegetation: no application

print("Stage 1 — Base Rate Assignment:")
print(f"  Healthy pixels (80 kg/ha):  {np.sum(health_map == 0):,}")
print(f"  Stressed pixels (120 kg/ha): {np.sum(health_map == 1):,}")
print(f"  Non-Veg pixels (0 kg/ha):    {np.sum(health_map == 2):,}")
```

```python
# ============================================================
# STAGE 2: NDRE Spectral Refinement
# ============================================================
# Formula: P_refined = P_base × clip((1.0 - NDRE) / 1.0, 0.5, 1.5)
#
# Low NDRE (chlorophyll deficiency) → factor up to 1.5×
# High NDRE (healthy chlorophyll)   → factor down to 0.5×
# ============================================================

ndre_factor = np.clip((1.0 - ndre) / 1.0, 0.5, 1.5)

# Apply NDRE refinement
prescription = base_rate * ndre_factor

# Cap at 220 kg N/ha to prevent over-fertilisation
prescription = np.clip(prescription, 0, 220)

# Force non-vegetation to 0
prescription[health_map == 2] = 0.0

print("\nStage 2 — NDRE-Refined Prescription:")
veg_mask = health_map != 2
print(f"  Mean prescription (vegetated): {prescription[veg_mask].mean():.1f} kg N/ha")
print(f"  Min prescription (vegetated):  {prescription[veg_mask & (prescription > 0)].min():.1f} kg N/ha")
print(f"  Max prescription:              {prescription.max():.1f} kg N/ha")
```

```python
# ============================================================
# SAVINGS CALCULATION: VRA vs Uniform 120 kg/ha
# ============================================================

pixel_area_ha = 0.01  # 10m × 10m = 100 m² = 0.01 ha

n_veg_pixels = np.sum(veg_mask)
total_veg_area_ha = n_veg_pixels * pixel_area_ha

# Uniform application total
uniform_total_kg = 120.0 * total_veg_area_ha

# VRA total
vra_total_kg = prescription[veg_mask].sum() * pixel_area_ha

# Savings
savings_kg = uniform_total_kg - vra_total_kg
savings_pct = (savings_kg / uniform_total_kg) * 100

print("=" * 60)
print("NITROGEN SAVINGS REPORT")
print("=" * 60)
print(f"  Vegetated area:       {total_veg_area_ha:,.1f} ha ({total_veg_area_ha/100:.1f} km²)")
print(f"  Uniform total (120):  {uniform_total_kg:,.0f} kg N")
print(f"  VRA total:            {vra_total_kg:,.0f} kg N")
print(f"  SAVINGS:              {savings_kg:,.0f} kg N ({savings_pct:.1f}%)")
```

```python
# ============================================================
# SAVE VRA PRESCRIPTION MAP AS GEOTIFF
# ============================================================

meta.update({
    'driver': 'GTiff',
    'dtype': 'float32',
    'count': 1,
    'nodata': 0
})

with rasterio.open(VRA_OUTPUT_PATH, 'w', **meta) as dst:
    dst.write(prescription.astype(np.float32), 1)

print(f"\nVRA prescription map saved: {VRA_OUTPUT_PATH}")
```

```python
# ============================================================
# VISUALIZE THE VRA PRESCRIPTION MAP
# ============================================================
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import matplotlib.patches as mpatches

fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=150)

# --- Left: Health Classification Map ---
health_cmap = plt.cm.colors.ListedColormap(['#2d6a4f', '#f4a261', '#e63946'])
ax1 = axes[0]
im1 = ax1.imshow(health_map, cmap=health_cmap, vmin=0, vmax=2)
ax1.set_title('Vegetation Health Classification', fontsize=13, fontweight='bold')
ax1.axis('off')
legend_patches = [
    mpatches.Patch(color='#2d6a4f', label='Healthy'),
    mpatches.Patch(color='#f4a261', label='Moderate Stress'),
    mpatches.Patch(color='#e63946', label='Non-Vegetation')
]
ax1.legend(handles=legend_patches, loc='lower left', fontsize=9, framealpha=0.9)

# --- Right: VRA Prescription Map ---
ax2 = axes[1]
bounds = [0, 40, 60, 80, 100, 120, 150, 180, 220]
cmap_vra = plt.cm.RdYlGn_r  # Red=high N, Green=low N
norm = BoundaryNorm(bounds, cmap_vra.N)
im2 = ax2.imshow(prescription, cmap=cmap_vra, norm=norm)
ax2.set_title('Variable-Rate N Prescription (kg/ha)', fontsize=13, fontweight='bold')
ax2.axis('off')
cbar = fig.colorbar(im2, ax=ax2, shrink=0.7, label='Nitrogen (kg N/ha)')

plt.suptitle('Prestea Huni-Valley Municipality — GeoAI Nitrogen Prescription',
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/content/drive/MyDrive/NEURAL NETWORK/data/VRA_Comparison.png',
            dpi=200, bbox_inches='tight')
plt.show()

print("VRA comparison figure saved.")
```

---

## Summary: What to Do in Colab

> [!IMPORTANT]
> You CANNOT use `train_test_split` and call it spatially validated. The switch to `GroupKFold` is the single most important change.

| Action | Where in Notebook |
|:---|:---|
| **1. Extract lat/lon** from `.geo` before dropping it | After Cell 14, before Cell 18 |
| **2. Assign block IDs** using 0.01° grid | Right after Step 1 |
| **3. Replace** `train_test_split` **with** `GroupKFold` | Replace Cell 30 entirely |
| **4. Add VRA prescription code** (6 cells) | After Cell 73, as the final section |

> [!WARNING]
> After switching to Spatial Block CV, your reported accuracy **will likely drop** from 96% to approximately 70–85%. This is expected and scientifically honest — the random split was inflated by spatial leakage. The new number is the real performance.

---

## BONUS: Visualizing the Spatial Data Split (Map)

To prove to your reviewers that the data is truly spatially separated, add this cell right after **STEP 3** to generate a map of the training vs. testing blocks.

```python
# ============================================================
# OPTIONAL: Visualize the Spatial Block CV Split
# Run this right after the GroupKFold split (Step 3)
# ============================================================
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Create a GeoDataFrame from the original coordinates
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Assign split labels based on the fold we just created
geo_df['Split'] = 'Unused'
geo_df.loc[train_idx, 'Split'] = 'Training (Fold 0)'
geo_df.loc[test_idx, 'Split']  = 'Testing (Fold 0)'

# Plotting
fig, ax = plt.subplots(figsize=(10, 8), dpi=150)

# Plot training points in blue
geo_df[geo_df['Split'] == 'Training (Fold 0)'].plot(
    ax=ax, color='#1f77b4', markersize=15, alpha=0.7, label='Training Blocks'
)

# Plot testing points in red
geo_df[geo_df['Split'] == 'Testing (Fold 0)'].plot(
    ax=ax, color='#d62728', markersize=15, alpha=0.9, label='Testing Blocks', edgecolor='black', linewidth=0.5
)

# Add gridlines to roughly show the blocks
ax.grid(True, linestyle='--', alpha=0.5, color='gray')

# Formatting
ax.set_title('Spatial Block Cross-Validation (Fold 0)', fontsize=14, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend(loc='upper right', framealpha=0.9)

# Save the figure to Drive
save_path = '/content/drive/MyDrive/NEURAL NETWORK/data/Spatial_CV_Map.png'
plt.savefig(save_path, bbox_inches='tight', dpi=300)
plt.show()

print(f"Spatial CV map saved to: {save_path}")
```
