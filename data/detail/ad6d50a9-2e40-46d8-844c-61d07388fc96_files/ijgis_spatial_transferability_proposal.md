# IJGIS Research Theme 2: Bounding Spatial Transferability with Area of Applicability

This document outlines the theoretical framing, methodology, and implementation details for a manuscript targeting the **IJGIS Special Issue on Critical Challenges in GeoAI**, focusing on the theme: **Spatialization of AI concepts and spatial transfer learning**.

---

## 1. Title and Executive Summary

* **Proposed Title:** Bounding Spatial Transferability in GeoAI: Area of Applicability Mapping for Land Use/Land Cover Classification in Data-Scarce Environments
* **Executive Summary:** This research tackles the critical challenge of spatial transferability in remote sensing deep learning. In data-scarce regions of the Global South, spatial transfer learning is the primary method used to scale Land Use/Land Cover (LULC) models to unmapped regions without retraining. However, these models are highly sensitive to spatial covariate shifts (variations in soils, atmospheric haze, and building architectures) and make highly confident, invalid predictions in out-of-distribution (OOD) zones. This paper integrates the Area of Applicability (AOA) framework into deep learning LULC pipelines to map the geographic boundaries of model reliability, functioning as both an online OOD detector and a spatial guide for targeted active sampling.

---

## 2. IJGIS Special Issue Alignment

This proposal directly aligns with the following IJGIS special issue theme:
* **Spatialization of AI concepts (spatial transfer learning, spatial inductive bias).**
* **Core Contribution:** It develops a transparent deployment framework for transferred deep learning models. Instead of treating transfer learning as a black box, it utilizes the AOA to bound spatial transferability, providing an empirical guide for where model output is scientifically valid and identifying where new ground-truth samples are required.

---

## 3. Research Questions

1. **RQ1:** How does the performance of a pixel-based 1D-CNN LULC model decay when transferred directly across geographically separate cities/regions in West Africa?
2. **RQ2:** Can the Area of Applicability (AOA) metric accurately detect and mask out-of-distribution (OOD) features (e.g., unrecognized roof types, active mining sites) in the target domain?
3. **RQ3:** Does an active learning sampling strategy guided by AOA masks achieve target-domain accuracy faster (requiring fewer samples) compared to traditional random sampling?

---

## 4. Methodology & Workflow

The proposed methodology consists of five main phases:

```
[Source Training (City A)] ---> [Model Transfer to Target (City B)]
                                      |
                                      v
                             [Compute Dissimilarity Index]
                                      |
                                      v
                             [Delineate AOA Mask]
                                      |
                                      v
                         [Guided Active Sampling & Retraining]
```

### Phase 1: Model Training in the Source Domain (City A)
* **Classifier:** A 1D-CNN (VegHealthCNN or equivalent) trained on Sentinel-2 multispectral bands. 
* **Target Classes:** Built-up, Agriculture, Forest, Water, and Bare Land.
* **Feature Extraction:** The model extracts hierarchical feature representations, culminating in a bottleneck/latent representation of the input pixel.

### Phase 2: Model Transfer to the Target Domain (City B)
* Freeze the model weights optimized on City A's training data.
* Deploy the frozen model directly to perform wall-to-wall LULC classification on City B's Sentinel-2 imagery.

### Phase 3: Dissimilarity Index (DI) Calculation
To measure how far a target pixel lies from the training distribution:
1. Extract the feature vectors of the training samples in the multi-dimensional feature space.
2. For each pixel in the target domain (City B), calculate the Euclidean distance to the nearest training sample in the feature space, weighted by the relative importance of each feature (derived from random forest permutation importance or SHAP analysis):
   
   DI_i = min_j ( d(x_i, t_j) ) / mean_k ( d(t_k, t_nearest) )
   
   Where:
   * d(x_i, t_j) is the weighted distance from target pixel i to training sample j.
   * The denominator represents the average distance between training points in cross-validation folds.

### Phase 4: Area of Applicability (AOA) Delineation
1. Establish the AOA threshold (threshold_DI) as the 95th percentile of the minimum distances between training points across cross-validation folds.
2. Delineate the binary AOA mask for the target domain:
   
   AOA_i = 1 (Applicable) if DI_i <= threshold_DI
   AOA_i = 0 (Outside AOA) if DI_i > threshold_DI
3. Mask out all predictions where AOA = 0. These are flagged as "untrustworthy/unknown" due to out-of-distribution spectral properties.

### Phase 5: Guided Active Sampling & Iterative Retraining
1. Identify geographic clusters of pixels flagged as "Outside AOA" (AOA = 0).
2. Collect target-domain ground-truth samples only in these flagged zones (representing new or modified classes, e.g., distinct soils or roof types).
3. Append these targeted samples to the training dataset, retrain the 1D-CNN, and re-compute the AOA. The AOA should expand, showing the model has successfully integrated the new spatial patterns.

---

## 5. Expected Results and Evaluation Framework

1. **AOA Visualization Panels:**
   * **Panel 1:** Transferred LULC classification map.
   * **Panel 2:** Continuous Dissimilarity Index map (highlighting zones of high feature distance).
   * **Panel 3:** Binary AOA Mask (showing geographic regions flagged for active sampling).

2. **Active Learning Efficiency Curve:**
   A line plot showing target domain classification accuracy (y-axis) against the number of collected samples (x-axis). This chart will compare:
   * **AOA-Guided Sampling:** Sampling only in flagged AOA=0 zones (steeper learning curve, reaches high accuracy with few samples).
   * **Random Sampling:** Sampling randomly across the target domain (slower, redundant sampling of already well-fit classes).

---

## 6. Critical Requirements for IJGIS Acceptance

To meet the high academic standards of IJGIS:
* **Novelty in GeoAI:** Frame the AOA not just as an uncertainty mask, but as an active tool for LULC scaling. This directly addresses the Special Issue's goal of moving beyond incremental technical improvements to propose structural solutions.
* **Feature Importance Calibration:** Distance calculations in multi-dimensional space are highly sensitive to the scale and redundancy of bands. You must document how features were normalized and weighted using feature-importance techniques (e.g., Random Forest importance) before computing DI.
* **Code Availability:** The Python/PyTorch code for computing pixel-level Dissimilarity Indices, AOA thresholds, and executing active learning loops must be shared via a public repository with clear setup instructions.
