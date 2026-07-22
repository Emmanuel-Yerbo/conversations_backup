# Spatial Validation & Transferability: Technical Output & Interpretation Manual

This manual describes the execution flow, input requirements, output artifacts, and academic interpretation of the two Colab notebooks:
1. `spatial_validation_pipeline.ipynb` (Theme 1)
2. `spatial_transferability_aoa_pipeline.ipynb` (Theme 2)

All dummy/mock data generators have been completely removed. The pipelines now run strictly on real-world datasets exported from Google Earth Engine (GEE).

---

## 📂 1. Input Specifications (No Dummy Data)

To execute the pipelines successfully in Google Colab, you must export the following datasets from Google Earth Engine (GEE) to your Google Drive folder `/content/drive/MyDrive/GEE_EXPORTS/`:

### A. Theme 1: Spatial Validation Pipeline Inputs
* **File Name:** `LULC_Training_Samples_Spatial_Val.csv`
* **Structure:** A comma-separated table containing point extractions across your study region.
* **Required Columns:**
  * `lon`, `lat`: Geographical coordinates in decimal degrees (WGS84).
  * `lulc_class`: Integer target labels (`0` = Built-up, `1` = Agriculture, `2` = Forest, `3` = Water, `4` = Bare).
  * `B2`, `B3`, `B4`, `B5`, `B6`, `B7`, `B8`, `B8A`, `B11`, `B12`: Sentinel-2 raw surface reflectance bands.
  * `NDRE`, `NDWI`, `EVI`, `BSI`: Derived spectral indices.
  *(Note: Raw NDVI is excluded to prevent model shortcutting and data leakage).*

### B. Theme 2: Spatial Transferability Pipeline Inputs
* **Source Domain Training Data:** `Source_LULC_Training_Samples.csv` (CSV file extracted from City A/Source region using the same 14-feature stack).
* **Target Domain Raster Image:** `Target_S2_Composite_Kumasi.tif` (Multi-band GeoTIFF file exported from GEE for the target domain, e.g., Kumasi. It must contain the 14 bands/features in the exact same sequence).

---

## 📊 2. Outputs Produced by Theme 1: Spatial Validation

When you run `spatial_validation_pipeline.ipynb` in Colab, the following analytical outputs are generated:

### Output 1: Empirical Semivariogram Range Plot
* **How it is produced:** The pipeline uses `skgstat.Variogram` to compute spatial variance on the `NDRE` index as a function of distance between points.
* **The Graphic:** A fitted semivariogram curve showing the distance lag on the x-axis (degrees) and semivariance on the y-axis.
* **The Output Metric:** A calculated block size (e.g., `0.002700` degrees, which corresponds to ~300 meters in tropical landscapes). This is the distance beyond which spatial autocorrelation ceases.

### Output 2: Validation Performance Decay vs. Spatial Block Size Curve
* **How it is produced:** A grid search runs GroupKFold validation over several block sizes (from 11m to 5.5km).
* **The Graphic:** A line chart showing **Validation Accuracy** and **Cohen's Kappa** decaying as block size increases.
* **Interpretation:** At small block sizes (e.g., 10m–50m), data leakage is severe, showing artificial accuracies of >95%. As block sizes exceed the spatial autocorrelation range (~300m), accuracy stabilizes at a lower, mathematically rigorous value (e.g., 78%–82%). This is the "honest" accuracy of the model on unseen geographic space.

```
       Performance (%)
       100 |   *---* (Optimistic / Leaked: 10m - 50m)
           |        \
        80 |         *-------* (calibrated range ~300m)
           |                  \
        60 |                   *---* (Rigorous / Independent: >1km)
           +----------------------------------
             10m      300m    1km    5km    (Block Size)
```

### Output 3: Comparative Classification Reports & Heatmaps
* **The Table:** Side-by-side standard classification metrics (Precision, Recall, F1-score, Cohen's Kappa, and Mean IoU) for:
  1. **Random K-Fold Cross-Validation** (shows high, biased values due to spatial autocorrelation).
  2. **Spatial Block Cross-Validation** (shows true out-of-sample capability).
* **The Graphic:** Two confusion matrix heatmaps (Blue for Random CV, Orange for Spatial Block CV) displaying the distribution of misclassifications.

---

## 🗺️ 3. Outputs Produced by Theme 2: Spatial Transferability & AOA

When you run `spatial_transferability_aoa_pipeline.ipynb` in Colab, the following outputs are generated:

### Output 1: Random Forest Feature Importance Weights
* **How it is produced:** A Random Forest classifier evaluates the source training set to assign weights to the 14 features based on Gini impurity.
* **The Text Output:** A printout of the features and their normalized weights (e.g., `B8: 0.184`, `NDRE: 0.152`). These weights scale the multi-dimensional distance calculation for the Dissimilarity Index (DI).

### Output 2: The IJGIS Deployment Panel (3-Pane Visual Plot)
The notebook generates a publication-ready figure containing three side-by-side spatial panels:

```
+--------------------------+--------------------------+--------------------------+
|  Panel 1: Transferred    |   Panel 2: Continuous    |   Panel 3: Binary AOA     |
|   LULC Map (Kumasi)      |      DI Map (Kumasi)     |      Mask (Kumasi)       |
|                          |                          |                          |
|  - Predicted crop/LULC   |  - Pixel-wise distance   |  - Green: Trustworthy    |
|    classes (Built, Agri, |    to source training    |    predictions (DI<=Th)  |
|    Forest, Water, Bare). |    data in feature space.|  - Red: OOD / Flagged    |
|                          |                          |    predictions (DI > Th) |
+--------------------------+--------------------------+--------------------------+
```

1. **Panel 1: Transferred LULC Map**
   * Shows the pixel-wise model classification over the unseen target domain (Kumasi).
2. **Panel 2: Dissimilarity Index (DI) Map**
   * A continuous map showing feature-space distance. High DI (bright yellow) indicates pixels that look very different from anything the model was trained on.
3. **Panel 3: Area of Applicability (AOA) Mask**
   * A binary map showing **Trustworthy (Green)** and **OOD/Flagged (Red)** zones. 
   * **Calculated AOA Threshold:** A printed threshold value (representing the 95th percentile of training data DI).
   * **Percentage of Target Domain inside AOA:** (e.g., `72.45%`). Tells you exactly what portion of your map can be trusted.

### Output 3: Guided Active Sampling Output
* **How it is produced:** The algorithm extracts the geographic coordinates of pixels flagged as Out-of-Distribution (AOA == 0).
* **The Text & File Output:** Prints the number of detected OOD pixels and generates a target coordinate list (CSV format) of the 100 most representative OOD points.
* **Purpose:** These coordinates are exported so a field crew or GIS analyst can collect targeted ground-truth labels, which are appended to the training set to retrain and expand the model's AOA.

---

## ✍️ 4. Thesis & Journal Interpretation Guide

When writing your dissertation or submitting to journals like *IJGIS*, *Remote Sensing of Environment*, or *IEEE TGRS*, use these outputs to structure your discussion:

| Technical Output | Scientific Argument | Academic Reference |
| :--- | :--- | :--- |
| **Random vs. Spatial CV Gap** | Demonstrates that standard random validation suffers from spatial autocorrelation leakage. Spatial CV provides an unbiased estimation of model transferability. | *Valavi et al. (2019)*; *Wadoux et al. (2021)* |
| **Sensitivity Decay Curve** | Mathematically justifies the spatial block size chosen for validation, showing that a block size too small inflates accuracy, while too large may introduce a pessimistic bias. | *Meyer & Pebesma (2021)* |
| **AOA Mask (Red Zones)** | Proves that machine learning models cannot extrapolate reliably. Visualizes exactly where the transferred map is subject to domain shift (e.g., due to soil, urban density, or atmospheric differences). | *Meyer & Pebesma (2021)* |
| **Active Learning Coordinates** | Demonstrates a cost-effective sampling strategy: instead of randomly sampling the target domain, only collect labels in the red AOA-flagged zones to maximize model improvement. | *Tuia et al. (2011)* |
