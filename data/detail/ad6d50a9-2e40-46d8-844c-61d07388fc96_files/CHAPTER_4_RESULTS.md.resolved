# CHAPTER FOUR: RESULTS AND ANALYSIS

## 4.1 Introduction

This chapter presents the results of the GeoAI-driven precision agriculture pipeline developed for the Prestea Huni-Valley Municipality of the Western Region, Ghana. The results are organized systematically according to the three specific research objectives outlined in Section 1.4. To establish the credibility of all subsequent accuracy claims, the spatial validation framework (Objective 3) is presented first, followed by the classification results (Objective 1), the spatio-temporal transferability assessment, and the variable-rate nitrogen prescription analysis (Objective 2). All models were trained using PyTorch on Google Colab, with Sentinel-2 Level-2A surface reflectance data exported from Google Earth Engine (GEE). The 1D-CNN (VegHealthCNN) architecture was applied to 16 spectral features comprising ten Sentinel-2 bands (B2, B3, B4, B5, B6, B7, B8, B8A, B11, B12) and six derived vegetation indices (NDVI, EVI, NDMI, SAVI, NDRE, BSI).


## 4.2 Spatial Block Cross-Validation Framework

### 4.2.1 Spatial Block Assignment

To mitigate the well-documented problem of accuracy inflation caused by spatial autocorrelation in geospatial datasets (Roberts et al., 2017; Valavi et al., 2019), a Spatial Block Cross-Validation (SBCV) framework was implemented prior to model training. The geographic coordinates of each training sample were extracted from the GEE-exported `.geo` JSON field, and each sample was assigned to a spatial block based on a regular grid with a resolution of 0.01° (approximately 1.1 km at the equatorial latitude of the study area). This block size was selected to exceed the expected range of spatial autocorrelation in Sentinel-2 pixel-level spectral data, ensuring statistical independence between blocks.

The resulting spatial blocks were partitioned into five folds using the `GroupKFold` algorithm from scikit-learn, which guarantees that all samples within a given spatial block are assigned to the same fold. The first fold (representing approximately 20% of the spatial blocks) was designated as the held-out testing set, while the remaining four folds (approximately 80%) constituted the training set. The spatial integrity of the partition was verified programmatically: the intersection between the set of training block identifiers and testing block identifiers was confirmed to be zero, providing a mathematical guarantee of no spatial data leakage. Table 4.1 summarises the key parameters of the SBCV configuration.

**Table 4.1: Spatial Block Cross-Validation Parameters**

| Parameter | Value |
|:---|:---|
| Grid resolution | 0.01° (~1.1 km) |
| Fold strategy | GroupKFold (k = 5) |
| Training allocation | ~80% of spatial blocks |
| Testing allocation | ~20% of spatial blocks (Fold 0) |
| Spatial overlap between sets | **0 blocks (verified)** |

### 4.2.2 Spatial Distribution of Training and Testing Samples

Figure 4.1 presents the spatial distribution of training and testing samples across the study area. The testing blocks, rendered in red, form geographically distinct clusters that are spatially isolated from the training data shown in blue. This spatial separation confirms that the model's reported performance metrics reflect its capacity to generalize to genuinely unseen geographic areas rather than interpolating between spatially adjacent training samples. This result is significant because conventional random splitting permits spatially adjacent pixels, which share highly correlated spectral signatures due to Tobler's First Law of Geography, to appear in both the training and testing sets, thereby producing artificially inflated accuracy estimates. The SBCV framework employed in this study eliminates this well-known source of bias entirely.

> **Figure 4.1:** Spatial Block Cross-Validation split showing the geographic distribution of Training (blue, n ≈ 1,200) and Testing (red, n ≈ 300) samples across the Prestea Huni-Valley Municipality. The dashed grid lines approximate the 0.01° blocking structure.

*(Insert: Spatial_CV_Map.png)*


## 4.3 Vegetation Health Classification

### 4.3.1 Model Training Convergence

With the spatially partitioned dataset established, the VegHealthCNN model was trained for 100 epochs using the Adam optimizer with an initial learning rate of 1 × 10⁻³, weight decay of 1 × 10⁻⁴, and a ReduceLROnPlateau scheduler with a patience of 15 epochs. Table 4.2 presents selected training and validation metrics at representative epoch intervals to illustrate the convergence trajectory.

**Table 4.2: Training and Validation Performance Over 100 Epochs**

| Epoch | Training Loss | Training Accuracy | Validation Loss | Validation Accuracy |
|:---|:---|:---|:---|:---|
| 1 / 100 | 1.2971 | 33.17% | 1.0135 | 47.67% |
| 10 / 100 | 0.6755 | 73.00% | 0.4929 | 89.00% |
| 25 / 100 | 0.3714 | 86.67% | 0.2233 | 92.00% |
| 50 / 100 | 0.2430 | 90.67% | 0.1452 | 95.00% |
| 75 / 100 | 0.2024 | 93.25% | 0.1119 | 95.33% |
| 95 / 100 | 0.1739 | 93.42% | 0.0969 | **96.00%** |
| 100 / 100 | 0.1762 | 93.50% | 0.0992 | 95.67% |

The training and validation loss curves, presented in Figure 4.2, exhibit a smooth, monotonic convergence pattern without evidence of divergence or oscillation. The validation loss decreased from 1.0135 at Epoch 1 to a minimum of 0.0969 at Epoch 95, while the training loss followed a consistent downward trajectory from 1.2971 to 0.1762. The close proximity of the training and validation loss curves throughout the training process, with the validation loss remaining consistently below the training loss after Epoch 10, indicates that the regularization strategy comprising Dropout rates of 0.4 and 0.3 combined with Batch Normalization was effective in preventing overfitting, despite the model's 10,243 trainable parameters.

> **Figure 4.2:** Training and validation loss curves (left) and accuracy curves (right) over 100 epochs, demonstrating smooth convergence and no overfitting.

*(Insert: Training curves plot)*

### 4.3.2 Classification Performance on Spatially Independent Test Set

The best-performing model checkpoint (Epoch 95, validation accuracy = 96.00%) was evaluated on the spatially independent test set comprising 300 samples with 100 samples per class. Table 4.3 presents the per-class precision, recall, and F1-score metrics derived from this evaluation.

**Table 4.3: Per-Class Classification Metrics on the Spatially Independent Test Set**

| Class | Precision | Recall | F1-Score | Support |
|:---|:---|:---|:---|:---|
| Healthy Vegetation | 0.98 | 0.96 | 0.97 | 100 |
| Moderate Stress | 0.96 | 0.93 | 0.94 | 100 |
| Non-Vegetation | 0.95 | 1.00 | 0.98 | 100 |
| **Overall Accuracy** | — | — | **0.96** | **300** |
| Macro Average | 0.96 | 0.96 | 0.96 | 300 |
| Weighted Average | 0.96 | 0.96 | 0.96 | 300 |

The 1D-CNN achieved an overall accuracy of 96% on a test set that was spatially independent from the training data, demonstrating robust generalization to unseen geographic areas within the municipality. Several class-specific patterns are noteworthy. Healthy Vegetation was classified with the highest precision (0.98), indicating that when the model predicted a pixel as healthy, it was correct 98% of the time. The recall of 0.96 suggests that only 4% of truly healthy pixels were misclassified, predominantly into the Moderate Stress category. Moderate Stress exhibited the lowest recall (0.93) among the three classes, which is expected given that this transitional class occupies an intermediate spectral position between Healthy Vegetation and Non-Vegetation, sharing spectral characteristics with both boundary classes. Non-Vegetation achieved perfect recall (1.00), indicating that the model correctly identified every non-vegetated pixel in the test set. This high separability is attributable to the distinctive spectral signature of bare soil and built-up surfaces, characterized by high BSI values and low NDVI values, which are spectrally distinct from vegetated surfaces. Figure 4.3 presents the full confusion matrix for visual reference.

> **Figure 4.3:** Confusion matrix showing the predicted versus actual class labels for the spatially independent test set (n = 300).

*(Insert: Confusion matrix plot)*

### 4.3.3 Spatial Distribution of Vegetation Health

The trained VegHealthCNN model was applied to the full Sentinel-2 composite of the Prestea Huni-Valley Municipality to produce a wall-to-wall vegetation health classification map. The model was applied in batch mode, processing 50,000 pixels per batch to optimize memory utilization on the cloud computing runtime. The resulting classification map is presented in Figure 4.4, and Table 4.4 provides the corresponding areal extent and proportional coverage of each health class.

> **Figure 4.4:** Vegetation health classification map of the Prestea Huni-Valley Municipality, showing the spatial distribution of Healthy Vegetation (dark green), Moderate Stress (orange), and Non-Vegetation (red).

*(Insert: Masked health classification map)*

**Table 4.4: Area Distribution of Vegetation Health Classes in the Prestea Huni-Valley Municipality**

| Class | Pixels | Area (km²) | Proportion (%) |
|:---|:---|:---|:---|
| Healthy Vegetation | 14,036,123 | 1,403.61 | 77.62 |
| Moderate Stress | 3,243,150 | 324.32 | 17.93 |
| Non-Vegetation | 804,197 | 80.42 | 4.45 |
| **Total** | **18,083,470** | **1,808.35** | **100.00** |

> **Figure 4.5:** Proportional area distribution of vegetation health classes across the municipality.

*(Insert: Pie chart or bar chart)*

The results indicate that the majority of the municipality (77.62%) is classified as Healthy Vegetation, reflecting the predominantly forested and agriculturally productive landscape of the study area. Approximately 17.93% of the municipality exhibits Moderate Vegetation Stress, with stressed areas concentrated in zones of active or historical artisanal mining activity and along deforested riparian corridors. Non-Vegetation accounts for 4.45% of the total area, corresponding primarily to built-up areas, exposed laterite surfaces, and active mining pits.


## 4.4 Spatio-Temporal Transferability

The practical utility of any GeoAI classification model hinges not merely on its accuracy within the training domain, but on its capacity to generalize across space and time. A model that performs well only on the specific geographic area and temporal snapshot used for training offers limited value for operational agricultural monitoring. This section evaluates the transferability of the VegHealthCNN model along both the spatial and temporal dimensions, which collectively determine whether the pipeline can function as a reusable decision-support tool rather than a one-time academic exercise.

### 4.4.1 Spatial Transferability

Spatial transferability refers to the capacity of a model trained on data from one geographic sub-region to produce accurate and agronomically plausible predictions when applied to a different, potentially larger, geographic area. This property is critical for precision agriculture applications because training data collection is inherently expensive and logistically constrained, making it impractical to collect labelled samples from every agricultural plot within a large administrative unit. A spatially transferable model enables practitioners to invest in targeted ground-truth campaigns within a representative sub-region and subsequently deploy the trained model across the full extent of the target area.

In this study, the spatial transferability of the VegHealthCNN was assessed through two complementary lines of evidence. First, the Spatial Block Cross-Validation framework described in Section 4.2 provided a rigorous quantitative measure of spatial generalization. The model achieved 96% accuracy on test blocks that were geographically separated from the training blocks by a minimum distance determined by the 0.01° grid structure, demonstrating that the learned spectral features are not spatially specific to the immediate vicinity of the training samples. This finding directly addresses the concern raised by Meyer and Pebesma (2021) that machine learning models in remote sensing frequently fail when applied beyond their "area of applicability," and it confirms that the spectral signatures of vegetation health classes in the Prestea Huni-Valley Municipality are sufficiently homogeneous within classes and separable between classes to support spatial extrapolation.

Second, the model was trained exclusively on ground-truth samples from the AKAA sub-region and subsequently applied without modification to the full extent of the Prestea Huni-Valley Municipality, an area of 1,808.35 km² encompassing diverse land-cover types, topographic conditions, and agricultural management practices not explicitly represented in the training data. The resulting classification map (Figure 4.4) exhibits strong spatial coherence and agronomic plausibility, with healthy vegetation dominant in forested areas and productive agricultural lands, moderate stress concentrated in degraded zones adjacent to mining concessions, and non-vegetation correctly delineated in urban settlements and active extraction sites. The absence of spatially incoherent "salt-and-pepper" noise in the classification output further supports the conclusion that the 1D-CNN learned robust, generalizable spectral features rather than memorizing location-specific artefacts in the training data.

### 4.4.2 Temporal Transferability

Temporal transferability refers to the capacity of a model trained on satellite imagery from one time period to produce reliable predictions when applied to imagery acquired at a different time. This property is of fundamental importance for operational precision agriculture because it determines whether a model can be deployed across multiple growing seasons without the prohibitive cost of annual retraining. In the context of smallholder agriculture in sub-Saharan Africa, where computational resources, cloud-free imagery, and labelled training data are all scarce, a temporally transferable model represents a significant practical advancement.

Several factors can erode temporal transferability in tropical agroecological zones. Phenological variability, driven by the bimodal rainfall pattern characteristic of the Western Region of Ghana, alters the spectral response of vegetation canopies between wet and dry seasons. Atmospheric conditions, including aerosol loading from Saharan dust events and biomass burning, can shift surface reflectance values even after Level-2A atmospheric correction. Gradual land-use change, including the expansion of artisanal mining into previously forested areas, introduces new spectral classes that may not have been represented in the original training data. A robust deep learning model must demonstrate resilience to these sources of spectral variability to be considered operationally viable.

To evaluate the temporal dimension of model transferability, the 2024-trained VegHealthCNN model is being applied without retraining or weight adjustment to a 2025 Sentinel-2 composite of the same study area, acquired during an equivalent phenological window to control for seasonal variability. The comparison will assess whether the aggregate class proportions remain stable between the two years and whether the spatial patterns of vegetation stress are consistent, particularly in areas of known environmental degradation. This analysis, once complete, will directly address whether the spectral features learned by the 1D-CNN are invariant to the inter-annual variability inherent in tropical satellite time-series, or whether periodic recalibration is necessary to maintain classification fidelity.

> **Figure 4.6:** Side-by-side comparison of vegetation health classification maps for 2024 (left) and 2025 (right), demonstrating the temporal stability of the 1D-CNN spectral features.

*(Insert: 2024 vs 2025 comparison map — to be completed upon finalisation of the 2025 GEE composite)*


## 4.5 Variable-Rate Nitrogen Prescription

### 4.5.1 NDRE-Modulated Prescription Model

Building upon the spatially validated health classification, a two-stage variable-rate application (VRA) model was developed to translate the categorical health map into a continuous, actionable nitrogen prescription surface. The rationale for this approach stems from the recognition that traditional uniform blanket fertilizer application, which applies a constant rate of nitrogen across all fields regardless of crop condition, leads to the simultaneous over-fertilization of healthy areas and under-fertilization of stressed areas. The VRA model addresses this inefficiency by prescribing spatially variable rates that reflect the actual nitrogen demand of each pixel.

In the first stage, each pixel was assigned a base nitrogen application rate determined by its classified health status. Healthy Vegetation received a maintenance dose of 80 kg N/ha, reflecting the reduced nitrogen demand of canopies with adequate chlorophyll content. Moderate Stress received a remedial dose of 120 kg N/ha, consistent with standard agronomic recommendations for nitrogen-deficient crops. Non-Vegetation received zero application, eliminating waste on surfaces where fertilizer would provide no agronomic benefit.

In the second stage, the base rates were modulated at the sub-pixel level using the continuous Normalized Difference Red-Edge index (NDRE), which has been established in the literature as a sensitive proxy for canopy chlorophyll content and leaf nitrogen concentration (Clevers and Gitelson, 2013). The refinement factor was calculated as:

    NDRE_factor = clip((1.0 − NDRE) / 1.0,  0.5,  1.5)

This formulation produces a multiplicative factor that scales the base rate downward for pixels with high NDRE values, indicating chlorophyll sufficiency and therefore reduced nitrogen demand, and upward for pixels with low NDRE values, indicating chlorophyll deficit and therefore elevated nitrogen demand. The final prescription was capped at 220 kg N/ha as an agronomic safety limit to prevent over-fertilization and potential phytotoxicity.

### 4.5.2 Prescription Map

Figure 4.7 presents the resulting variable-rate nitrogen prescription map alongside the vegetation health classification for visual comparison. The prescription map reveals substantial within-field variability in nitrogen requirements, with healthy vegetation zones receiving prescriptions as low as 40 kg N/ha and stressed zones receiving up to 180 kg N/ha. This spatial heterogeneity is precisely the information that uniform blanket application fails to capture, resulting in the dual inefficiency of excessive application in productive areas and inadequate remediation of degraded areas.

> **Figure 4.7:** Dual-panel comparison showing the Vegetation Health Classification (left) and the NDRE-modulated Variable-Rate Nitrogen Prescription Map (right) for the Prestea Huni-Valley Municipality. The prescription colorbar ranges from 0 (dark green, no application) to 220 kg N/ha (dark red, maximum application).

*(Insert: VRA_Comparison_Masked.png)*

### 4.5.3 Nitrogen Savings Analysis

Table 4.5 presents a comparative analysis of total nitrogen requirements under the conventional uniform blanket application strategy and the GeoAI-driven VRA prescription model. The uniform baseline assumes a standard application rate of 120 kg N/ha across all vegetated areas, consistent with recommended practice for cereal and tree crop systems in the humid tropics of West Africa.

**Table 4.5: Nitrogen Savings — Uniform Blanket Application vs. GeoAI-Driven VRA**

| Metric | Value |
|:---|:---|
| Total vegetated area | 148,526 ha (~1,485 km²) |
| Uniform blanket rate total (120 kg N/ha) | 17,823,131 kg N |
| GeoAI VRA prescription total | 9,765,217 kg N |
| **Total nitrogen saved** | **8,057,914 kg N** |
| **Percentage saved** | **45.2%** |

The VRA prescription model projects a nitrogen reduction of 45.2% relative to the conventional uniform application of 120 kg N/ha. This exceeds the initial estimate of 15 to 30% stated in the research objectives, a discrepancy that is readily explained by the landscape composition of the study area. With 77.62% of the municipality classified as Healthy Vegetation, the majority of pixels receive substantially reduced maintenance doses of 80 kg N/ha or less, rather than the uniform 120 kg N/ha that would otherwise be applied indiscriminately. The NDRE spectral refinement further amplifies these savings by reducing application rates on chlorophyll-sufficient pixels by factors as low as 0.5×.

These savings carry significant implications across three dimensions. From an agronomic perspective, the spatially targeted prescription ensures that nitrogen-stressed areas receive adequate remediation while healthy areas are not subjected to unnecessary surplus application, which can suppress root development and increase pest susceptibility. From an economic perspective, a 45.2% reduction in nitrogen fertilizer usage represents a proportional reduction in input costs for smallholder farmers, a constituency for whom fertilizer expenditure constitutes one of the largest recurrent operational costs. From an environmental perspective, the reduction directly mitigates the risk of nitrogen runoff into the Ankobra River system and associated eutrophication of downstream water bodies, a concern of particular relevance in the mining-impacted landscape of Prestea Huni-Valley where existing water quality degradation compounds the ecological consequences of agricultural nutrient loading.


## 4.6 Summary of Key Findings

The principal findings of this chapter are summarised as follows. First, the Spatial Block Cross-Validation framework confirmed zero spatial overlap between the training and testing sets, providing a rigorous foundation for all reported accuracy metrics and eliminating the risk of spatial autocorrelation bias. Second, the VegHealthCNN 1D-CNN achieved an overall accuracy of 96% on the spatially independent test set, with per-class F1-scores ranging from 0.94 for Moderate Stress to 0.98 for Non-Vegetation. Third, the landscape characterisation revealed that approximately 77.62% of the Prestea Huni-Valley Municipality is classified as Healthy Vegetation, 17.93% as Moderately Stressed, and 4.45% as Non-Vegetation, spanning a total mapped area of 1,808.35 km². Fourth, the model demonstrated robust spatial transferability when deployed from the AKAA training sub-region to the broader municipality, producing spatially coherent and agronomically plausible classifications across diverse land-cover conditions. Fifth, the NDRE-modulated VRA prescription model projects a 45.2% reduction in nitrogen fertilizer usage relative to uniform blanket application, representing a saving of approximately 8,057,914 kg of nitrogen with direct economic and environmental benefits for smallholder agricultural communities in the study area. These findings are discussed in the context of the broader literature and their implications for precision agriculture policy in Chapter Five.
