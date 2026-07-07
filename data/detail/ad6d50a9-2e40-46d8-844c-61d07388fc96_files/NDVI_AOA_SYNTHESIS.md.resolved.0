# Methodological Critique Synthesis: NDVI Multicollinearity & Area of Applicability

## THE TWO ISSUES

### Issue 1: NDVI Used for Both Label Creation AND as a Training Feature

**What happened:**
- Labels were created in GEE using NDVI thresholds:
  - Healthy: NDVI ≥ 0.6
  - Moderate Stress: 0.3 ≤ NDVI < 0.6
  - Non-Vegetation: NDVI < 0.3
- The 16-feature training vector includes NDVI as one of the input features:
  `features = ['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12','NDVI','EVI','NDMI','SAVI','NDRE','BSI']`

**Why this is problematic:**
This is not simply multicollinearity (where two features are correlated). It is **circular dependency / information leakage**. The label `y` was *deterministically derived from* one of the inputs `X`. The model could achieve near-perfect accuracy by ignoring all 15 other features and learning the threshold function on NDVI alone. The 96% accuracy may therefore reflect the model's ability to reconstruct a simple threshold rule, not genuine spectral health discrimination.

Additionally, SAVI and EVI are highly correlated with NDVI (they use the same B4/B8 bands), so it's not just NDVI — the collinearity propagates.

---

### Issue 2: Area of Applicability (AOA) Was Discussed but Not Computed

**What happened:**
- Meyer & Pebesma (2021) was cited in the Discussion as supporting spatial transferability.
- The actual AOA metric was never computed — no dissimilarity index (DI), no AOA mask.
- The committee wants to see whether the model's predictions fall within or outside the feature space covered by training data.

---

## ROUTE ANALYSIS: Three Options for Issue 1

### Route A: Remove NDVI (and possibly SAVI) from the Feature Vector — RECOMMENDED

**What you do:**
- Retrain the model with 14 features (drop NDVI and SAVI) or 13 features (drop NDVI, SAVI, EVI — all B4/B8 derived ratios).
- Keep the NDVI-based labels as they are.
- The remaining features (B2-B12, NDMI, NDRE, BSI, and optionally EVI) are spectrally independent of the labelling criterion.

**Why this is the strongest route:**
- It **breaks the circular dependency** cleanly. The labels were defined by NDVI, but the model no longer sees NDVI. If it still achieves high accuracy, this proves the model learned genuine spectral patterns from raw bands and non-NDVI indices.
- The accuracy may drop slightly (perhaps to 90–93%), but that number is **far more defensible** than 96% with NDVI included.
- EVI can be kept because although correlated with NDVI, it was not the thresholding variable. But dropping it too would be maximally conservative.
- This is a **one-cell change** in your GEE export or a one-line change in your PyTorch training script.

**Defence language:**
> "To eliminate circular dependency between the label-generating index and the input feature space, NDVI was excluded from the training vector. The model's capacity to maintain [X]% accuracy using only raw spectral bands and non-NDVI indices confirms that the 1D-CNN learned biophysically meaningful spectral signatures rather than reconstructing the labelling threshold."

### Route B: Re-derive Labels Using an Independent Method

**What you do:**
- Keep all 16 features including NDVI.
- But regenerate the labels using a different criterion:
  - Option B1: Use **NDRE thresholds** instead of NDVI for labelling.
  - Option B2: Use **unsupervised clustering** (K-Means on raw bands) to define classes.
  - Option B3: Use **manual visual interpretation** + high-resolution Google imagery.

**Why this is harder:**
- Requires full reprocessing in GEE + retraining + re-running all results.
- Changes every number in Chapters 4, 5, and 6.
- If using NDRE for labels, then NDRE becomes the circular variable instead.

### Route C: Keep Everything, Defend It — WEAKEST

**What you do:**
- Argue that NDVI is only 1 of 16 features.
- Show feature importance / ablation proving other features contribute.
- Acknowledge the limitation explicitly.

**Why this is risky:**
- Any examiner familiar with ML will recognise the circularity.
- "It's only 1 of 16" doesn't hold because that 1 feature *perfectly predicts* the label.

---

## MY RECOMMENDATION: Route A (Remove NDVI from Features)

This is the minimum-effort, maximum-credibility fix. Here's the concrete implementation:

### Step 1: In your PyTorch training script
```python
# BEFORE (16 features):
features = ['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12',
            'NDVI','EVI','NDMI','SAVI','NDRE','BSI']

# AFTER (14 features — drop NDVI and SAVI):
features = ['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12',
            'EVI','NDMI','NDRE','BSI']
```

### Step 2: Update VegHealthCNN input dimension
```python
# BEFORE:
self.conv1 = nn.Conv1d(1, 64, kernel_size=3, padding=1)  # input_dim=16

# AFTER:
# input_dim=14 — the Conv1d kernel doesn't change, only the sequence length
```

### Step 3: Retrain, re-validate, re-export
- The spatial block CV, VRA, and temporal transfer all rerun with 14 features.
- Update accuracy numbers in Chapters 4–6.

---

## ROUTE ANALYSIS: Area of Applicability

### What the AOA Is

Meyer & Pebesma (2021) define the AOA as the geographic region where the model's predictions can be trusted because the input features at prediction time fall within the feature space covered by the training data. Pixels outside the AOA are extrapolating into unknown spectral territory.

### What Needs to Be Done

The AOA computation involves:
1. Computing a **Dissimilarity Index (DI)** for every pixel in the prediction area, measuring its spectral distance from the nearest training sample in the normalised feature space.
2. Defining a **threshold** based on the DI values of the cross-validation folds — the 95th percentile of DI among training samples is typically used.
3. Pixels with DI > threshold are **outside the AOA** and should be flagged.

### Implementation Options

**Option 1: Use the `CAST` Python package** (recommended)
```python
# pip install CAST
from CAST import AOA
aoa = AOA(model, X_train, X_test)
```
This directly implements Meyer & Pebesma's algorithm.

**Option 2: Manual implementation**
```python
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import numpy as np

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_pred_scaled = scaler.transform(X_prediction_pixels)

# Dissimilarity = min distance to any training sample
distances = cdist(X_pred_scaled, X_train_scaled, metric='euclidean')
DI = distances.min(axis=1)

# Threshold from CV folds
threshold = np.percentile(DI_cv_folds, 95)

# AOA mask
aoa_mask = DI <= threshold
```

### What It Proves

If >95% of your prediction pixels fall within the AOA, it validates your spatial transferability claim. If a significant portion falls outside, you need to acknowledge that those regions are extrapolations.

---

## RECOMMENDED ACTION PLAN

| Priority | Action | Effort | Impact |
|:---|:---|:---|:---|
| **1** | Remove NDVI (+ SAVI) from features, retrain | ~2 hours | Eliminates the circularity critique entirely |
| **2** | Compute AOA on the 14-feature model | ~3 hours | Provides formal spatial transferability evidence |
| **3** | Update Chapters 4–6 with new accuracy numbers | ~1 hour | Keeps thesis internally consistent |
| **4** | Add AOA figure + paragraph to Chapter 4 | ~30 min | Directly addresses committee concern |

> [!IMPORTANT]
> **The NDVI removal is non-negotiable if you want the thesis to withstand scrutiny.** The AOA is a strong addition but secondary. Do Issue 1 first.
