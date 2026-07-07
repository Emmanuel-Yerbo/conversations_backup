# Implementation Plan: Explainable GeoAI

This plan outlines the implementation of interpretability frameworks (SHAP, Grad-CAM, and LIME) to explain the decisions of the 1D-CNN Nitrogen Prescription model and the Building Footprint Extraction models.

## User Review Required

> [!IMPORTANT]
> **Priority Model:** Which model should we focus on first? 
> 1. The **1D-CNN** (Spectral data for Nitrogen)?
> 2. The **U-Net/Mask R-CNN** (Spatial imagery for Building Footprints)?

> [!NOTE]
> **Data Availability:** To generate explanations, I will need access to:
> - The trained model files (`.h5`, `.pth`, or `.json`).
> - A small "test" sample of the input data (CSV for 1D-CNN, or Image Tiles for Building Footprints).

## Proposed Changes

### [Component 1] XAI for 1D-CNN (Precision Agriculture)
We will use **SHAP (SHapley Additive exPlanations)** to break down the "black box" of the 1D-CNN.

#### [NEW] [XAI_1D_CNN_Interpretation.ipynb](file:///c:/YERBO/Desktop/CODING/EXPLAINABLE AI/XAI_1D_CNN_Interpretation.ipynb)
- **Feature Importance**: Identify which spectral bands (Red-Edge, NIR, etc.) are the primary drivers for Nitrogen recommendations.
- **Local Explanations**: For a specific field/pixel, show which values increased or decreased the predicted prescription.
- **Global Explanations**: Summary plots showing the distribution of feature impacts across the entire dataset.

---

### [Component 2] XAI for Building Footprint Extraction (Computer Vision)
We will use **Grad-CAM** or **Integrated Gradients** to visualize the "attention" of the U-Net/Mask R-CNN models.

#### [NEW] [XAI_Building_Visualizer.ipynb](file:///c:/YERBO/Desktop/CODING/EXPLAINABLE AI/XAI_Building_Visualizer.ipynb)
- **Heatmap Overlays**: Generate heatmaps on drone/satellite imagery to show which pixels the model "focused" on to identify a building.
- **Error Analysis**: Use XAI to understand why the model might have missed a building or produced a false positive (e.g., mistaking a road for a structure).

---

### [Component 3] Research Documentation
#### [NEW] [XAI_Methodology_Draft.md](file:///c:/YERBO/Desktop/CODING/EXPLAINABLE AI/XAI_Methodology_Draft.md)
- A draft section for your thesis methodology explaining the choice of SHAP/Grad-CAM and how they validate the GeoAI pipeline's reliability for Ghanaian smallholders.

## Open Questions

- **Model Weights**: Do you have the pre-trained weights for the 1D-CNN or Building Footprint models saved locally, or should we train a "dummy" model first to demonstrate the XAI pipeline?
- **Framework**: Are you currently using **PyTorch** or **TensorFlow/Keras** for these models? (This determines which XAI library, e.g., `Captum` vs `tf-explain`, we use).

## Verification Plan

### Automated Tests
- Verify that the SHAP explainer initializes without errors on the model architecture.
- Ensure heatmaps are generated with the correct dimensions (matching input imagery).

### Manual Verification
- Compare the "Feature Importance" plots with known agronomic principles (e.g., check if the Red-Edge band is indeed highly significant for Nitrogen detection).
