# IJGIS Research Theme 1: Spatial Validation and Autocorrelation Bias

This document outlines the theoretical framing, methodology, and implementation details for a manuscript targeting the **IJGIS Special Issue on Critical Challenges in GeoAI**, focusing on the theme: **Traditional and spatial uncertainty quantification, model robustness, and validation bias**.

---

## 1. Title and Executive Summary

* **Proposed Title:** Optimistic vs. Pessimistic Bias in GeoAI: Evaluating Spatial Block Cross-Validation for Land Use/Land Cover Deep Learning Models
* **Executive Summary:** This research addresses the critical challenge of validation bias in remote sensing deep learning models. In Land Use/Land Cover (LULC) classification, conventional random point-splitting (k-fold cross-validation) violates the assumption of independent and identically distributed (i.i.d.) observations due to spatial autocorrelation. This leads to spatial data leakage and highly inflated accuracy metrics (optimistic bias). However, applying strict spatial block cross-validation (Spatial CV) can introduce a "pessimistic bias" by turning an interpolation task into an extrapolation task. This paper presents a systematic protocol to parameterize and evaluate spatial validation blocks for pixel-based deep learning classifiers (1D-CNNs), providing a scientifically defensible method to estimate LULC classification generalizability.

---

## 2. IJGIS Special Issue Alignment

This proposal directly aligns with the following IJGIS special issue theme:
* **Traditional and spatial uncertainty quantification, model robustness, and misuse risks in GeoAI applications.**
* **Core Contribution:** It critiques the current standard of validation in remote sensing deep learning, exposes the magnitude of the "accuracy bubble" created by random splits, and proposes a calibrated, variogram-based protocol for spatial block partitioning.

---

## 3. Research Questions

1. **RQ1:** To what degree does random cross-validation inflate the performance metrics (accuracy, F1-score, Kappa) of pixel-based 1D-CNN models in complex, fragmented West African landscapes?
2. **RQ2:** How does the selection of spatial block size (from sub-pixel scale to multi-kilometer scale) affect the trade-off between optimistic validation bias and pessimistic extrapolation bias?
3. **RQ3:** Can empirical semi-variogram modeling of Sentinel-2 spectral indices provide an optimal, reproducible threshold for sizing spatial validation blocks?

---

## 4. Methodology & Workflow

The proposed methodology consists of five main phases:

```
[Phase 1: Feature Stack] ---> [Phase 2: Autocorrelation Range] ---> [Phase 3: Grid Partitioning] 
                                                                              |
[Phase 5: Bias Analysis] <--- [Phase 4: Multi-Fold GroupKFold] <--------------+
```

### Phase 1: Data Preparation & Feature Stack
* **Sensor:** Sentinel-2 Level-2A Bottom-of-Atmosphere (BOA) Surface Reflectance.
* **Spectral Feature Stack (14 bands):** 
  * Core Bands: B2 (Blue), B3 (Green), B4 (Red), B8 (NIR).
  * Red-Edge Bands: B5, B6, B7, B8a.
  * Shortwave Infrared (SWIR): B11, B12.
  * Derived Indices: NDRE (Normalized Difference Red Edge), NDWI (Normalized Difference Water Index), and soil-adjusted indices (excluding highly collinear variables that cause temporal instability).
* **LULC Classes:** Built-up, Agriculture, Forest, Water, and Bare Soil.

### Phase 2: Empirical Autocorrelation Range Estimation
To prevent arbitrary block sizing, the spatial range of autocorrelation must be determined:
1. Extract the primary spectral indices (e.g., NDRE, NDVI) from all training sample locations.
2. Calculate the empirical semi-variogram for each index using the equation:
   
   gamma(h) = (1 / 2N(h)) * sum_{i=1}^{N(h)} [ Z(x_i) - Z(x_i + h) ]^2
   
   Where:
   * gamma(h) is the semi-variance at lag distance h.
   * N(h) is the number of paired sample points separated by distance h.
   * Z(x_i) is the value of the spectral index at location x_i.
3. Fit a spherical or exponential variogram model to find the **range (a)**—the distance at which spatial autocorrelation decays to statistical independence.

### Phase 3: Spatial Grid Partitioning
1. Divide the study area into a regular grid of rectangular blocks.
2. The block dimension (D) is parameterized to equal or exceed the range of autocorrelation:
   
   D >= range (a)
   
   At equatorial latitudes, a 0.01-degree grid corresponds to approximately 1.1 km, which typically exceeds the empirical variogram range of 50–300 meters observed in fragmented smallholder agricultural landscapes.
3. Assign each training pixel to a unique block ID based on its coordinates:
   
   block_id = floor(longitude / D) + "_" + floor(latitude / D)

### Phase 4: Model Training and GroupKFold Validation
1. **Model Architecture:** A 1D-CNN (VegHealthCNN) implemented in PyTorch, comprising 1D convolutional layers, batch normalization, dropout, and a fully connected output layer.
2. **Validation Setup:** 
   * **Random CV:** Standard 5-fold cross-validation where pixels are randomly assigned to folds.
   * **Spatial CV:** 5-fold GroupKFold cross-validation where the grouping variable is the `block_id`. This guarantees that no pixels belonging to the same geographic block appear in both the training and testing sets.
3. Run both validation setups under identical training parameters (AdamW optimizer, Cosine Annealing learning rate schedule).

### Phase 5: Bias and Error Analysis
Quantify the validation discrepancy:
* **Optimistic Bias:** Difference between Random CV accuracy and Spatial CV accuracy.
* **Pessimistic Bias Analysis:** Evaluate whether the low accuracy in certain spatial folds is due to poor model learning or because those folds contain unique environmental conditions not represented in the training folds (extrapolation error).

---

## 5. Expected Results and Evaluation Framework

1. **The Accuracy Discrepancy Table:**
   A comparative table showing classification metrics across validation strategies.
   
   | Metric | Random CV (i.i.d. assumption) | Spatial Block CV (1.1 km) | Delta (Optimistic Bias) |
   |:---|:---|:---|:---|
   | Overall Accuracy | 99.1% | 89.5% | -9.6% |
   | Macro F1-Score | 0.98 | 0.88 | -0.10 |
   | Kappa | 0.97 | 0.84 | -0.13 |

2. **Block-Size Sensitivity Curve:**
   A line chart plotting validation accuracy against block size (from 10m to 5km). As block size increases, validation accuracy typically drops and stabilizes, indicating the point where spatial autocorrelation leakage is completely mitigated.

---

## 6. Critical Requirements for IJGIS Acceptance

To meet the high academic standards of IJGIS:
* **Mathematical Rigor:** The choice of block size must not be arbitrary. You must present the semi-variogram analysis and the resulting range (a) as the scientific justification for the 1.1 km grid size.
* **Code and Data Availability:** IJGIS enforces a strict data and code sharing policy. The PyTorch training code, block partitioning scripts, and anonymized training samples must be uploaded to a public repository (e.g., Zenodo or GitHub) with a DOI.
* **Double-Anonymous Review Compliance:** Ensure that the manuscript and the uploaded code do not contain references to the author's names, affiliations, or specific project grants.
* **Reproducibility:** Include exact package versions in a `requirements.txt` or Dockerfile. Specify random seeds for PyTorch and Scikit-Learn to ensure identical fold splits and weight initialization.
