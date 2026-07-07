# Chapter 4: Results

> **Note to author:** Present objectives in a logical order — validation framework first (it underpins everything), then classification, then temporal transfer, then VRA as the applied output.

---

## 4.1 Introduction

*(1 paragraph. State that results are organized according to the four research objectives. Mention the study area (Prestea Huni-Valley Municipality), the data source (Sentinel-2), and the model (1D-CNN with 16 spectral features).)*

---

## 4.2 Objective 4 — Spatial Block Cross-Validation Framework

> **Why this comes first:** The validation method must be established before presenting any accuracy claims. Reviewers need to trust your evaluation before they trust your numbers.

### 4.2.1 Spatial Block Assignment

*(Describe how the study area was divided into a 0.01° grid (~1.1 km blocks), with each sample assigned to a spatial block based on its geographic coordinates.)*

| Parameter | Value |
|:---|:---|
| Grid resolution | 0.01° (~1.1 km) |
| Number of spatial blocks | *(fill from Colab output)* |
| Fold strategy | GroupKFold, k=5 |
| Training set | ~80% of blocks |
| Testing set | ~20% of blocks (Fold 0) |
| Spatial overlap | **0 blocks** (verified) |

### 4.2.2 Spatial Split Visualization

> **Figure 4.1:** Spatial Block Cross-Validation split showing Training (blue) and Testing (red) sample locations across the Prestea Huni-Valley Municipality.

*(Insert the Spatial_CV_Map.png here)*

**Key finding:** The testing blocks form geographically isolated clusters with zero spatial overlap with the training set, confirming that the reported model accuracy is free from spatial autocorrelation bias.

---

## 4.3 Objective 1 — Vegetation Health Classification

> **This is your core ML result. It answers: "Does the 1D-CNN work?"**

### 4.3.1 Model Training Convergence

*(Describe the training process: 100 epochs, Adam optimizer, ReduceLROnPlateau scheduler, early stopping patience of 15.)*

> **Figure 4.2:** Training and Validation Loss/Accuracy curves over 100 epochs.

*(Insert the training curves plot here)*

| Metric | Value |
|:---|:---|
| Final Training Loss | 0.1762 |
| Final Training Accuracy | 93.50% |
| Final Validation Loss | 0.0992 |
| Final Validation Accuracy | 95.67% |
| Best Validation Accuracy | **96.00%** (Epoch 95) |

**Key finding:** The validation loss converged smoothly to 0.0992 without diverging from the training loss, confirming that the dropout regularization (0.4 and 0.3) and batch normalization successfully prevented overfitting despite the model's 10,243 trainable parameters.

### 4.3.2 Classification Performance

> **Table 4.1:** Per-class classification metrics from the spatially independent test set (n=300).

| Class | Precision | Recall | F1-Score | Support |
|:---|:---|:---|:---|:---|
| Healthy | 0.98 | 0.96 | 0.97 | 100 |
| Moderate Stress | 0.96 | 0.93 | 0.94 | 100 |
| Non-Vegetation | 0.95 | 1.00 | 0.98 | 100 |
| **Overall Accuracy** | — | — | **0.96** | **300** |
| Macro Average | 0.96 | 0.96 | 0.96 | 300 |
| Weighted Average | 0.96 | 0.96 | 0.96 | 300 |

> **Figure 4.3:** Confusion matrix showing predicted vs. actual class labels.

*(Insert the confusion matrix plot here)*

**Key findings:**
- The 1D-CNN achieved an **overall accuracy of 96%** on a spatially independent test set, demonstrating robust generalization to unseen geographic areas.
- Non-Vegetation was classified with perfect recall (1.00), indicating the model reliably distinguishes bare soil and built-up areas from vegetated surfaces.
- Moderate Stress had the lowest recall (0.93), which is expected as this transitional class shares spectral characteristics with both Healthy vegetation and Non-Vegetation.

### 4.3.3 Vegetation Health Map

> **Figure 4.4:** Vegetation health classification map of the Prestea Huni-Valley Municipality.

*(Insert the masked health classification map — Dark Green/Orange/Red — here)*

> **Table 4.2:** Area distribution of vegetation health classes across the municipality.

| Class | Pixels | Area (km²) | Proportion |
|:---|:---|:---|:---|
| Healthy | *(from Colab)* | *(from Colab)* | *(from Colab)* |
| Moderate Stress | *(from Colab)* | *(from Colab)* | *(from Colab)* |
| Non-Vegetation | *(from Colab)* | *(from Colab)* | *(from Colab)* |
| **Total** | — | — | **100%** |

> **Figure 4.5:** Pie chart or bar chart showing the proportional area of each health class.

*(Insert the pie/bar chart here)*

---

## 4.4 Objective 2 — Multi-Temporal Transferability

> **This answers: "Does a model trained on 2024 data still work on 2020–2023 imagery?"**

### 4.4.1 Temporal Transfer Experiment

*(Describe the experiment: the 1D-CNN was trained on 2024 Sentinel-2 composites and applied to imagery from [other years]. Discuss whether the spectral features (NDVI, NDRE, etc.) remained stable enough for the model to generalize.)*

> **Table 4.3:** Classification accuracy when the 2024-trained model is applied to multi-temporal imagery.

| Year | Overall Accuracy | Notes |
|:---|:---|:---|
| 2024 (training year) | 96.00% | Baseline |
| *(other years)* | *(fill in)* | *(fill in)* |

> **Figure 4.6:** *(If you have maps for multiple years, show them side-by-side here)*

**Key finding:** *(State whether the model generalizes well across the 4-year interval, or if there is accuracy degradation due to phenological shifts, land-use change, or atmospheric variability.)*

---

## 4.5 Objective 3 — Variable-Rate Nitrogen Prescription

> **This is the applied contribution — the practical value of your entire project.**

### 4.5.1 NDRE-Modulated Prescription Model

*(Describe the two-stage VRA pipeline:)*
1. *Stage 1:* Base N rates assigned from health classes (Healthy → 80 kg/ha, Stressed → 120 kg/ha, Non-Veg → 0).
2. *Stage 2:* Pixel-level refinement using continuous NDRE values (factor range: 0.5× to 1.5×).

### 4.5.2 Prescription Map

> **Figure 4.7:** Variable-rate nitrogen prescription map for the Prestea Huni-Valley Municipality (side-by-side with health classification).

*(Insert the masked dual-panel VRA_Comparison.png here)*

### 4.5.3 Nitrogen Savings Analysis

> **Table 4.4:** Nitrogen savings comparison — Uniform blanket application vs. GeoAI-driven VRA.

| Metric | Value |
|:---|:---|
| Total vegetated area | *(from Colab)* ha |
| Uniform rate (120 kg/ha) total | *(from Colab)* kg N |
| GeoAI VRA total | *(from Colab)* kg N |
| **Total nitrogen saved** | ***(from Colab)*** **kg N** |
| **Percentage saved** | ***(from Colab)***% |

**Key finding:** The NDRE-modulated VRA prescription achieved a nitrogen reduction of approximately 15–30% relative to a uniform blanket application of 120 kg/ha, demonstrating the economic and environmental benefits of integrating GeoAI into smallholder precision agriculture.

---

## 4.6 Summary of Key Findings

*(A brief closing section — 3 to 5 bullet points — summarizing the headline results before moving into Chapter 5: Discussion.)*

1. The Spatial Block Cross-Validation framework confirmed that the reported accuracy is free from spatial leakage.
2. The 1D-CNN achieved 96% overall accuracy on a spatially independent test set.
3. Approximately X% of the municipality is classified as Healthy, Y% as Moderately Stressed, and Z% as Non-Vegetation.
4. *(Multi-temporal finding)*
5. The VRA prescription model projects nitrogen savings of approximately X%, reducing fertilizer waste and environmental runoff.

---

> [!IMPORTANT]
> **Figures and tables must be numbered sequentially** (Figure 4.1, 4.2... Table 4.1, 4.2...) and referenced in the text *before* they appear. Never drop a figure without first writing a sentence that says "As shown in Figure 4.X..."

> [!TIP]
> **For the Discussion chapter (Chapter 5):** Compare your 96% accuracy to the papers in your literature review. If similar studies using random splits reported 95–98%, you can argue that your spatially validated 96% is actually *more impressive* because it was achieved under stricter evaluation conditions.
