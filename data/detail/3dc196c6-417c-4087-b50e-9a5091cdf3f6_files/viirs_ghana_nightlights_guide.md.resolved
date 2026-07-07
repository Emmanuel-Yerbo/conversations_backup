# 🌌 VIIRS Nighttime Lights Mapping for Ghana: Implementation Guide

This guide details the complete technical workflow, data requirements, and code needed to produce a high-contrast, premium "nightlights" map of Ghana similar to NASA's global visualizations. It covers programmatic data acquisition, preprocessing (specifically tackling raw skewness), and cartographic styling in R.

```
       GHANA NIGHTLIGHTS CONCEPTUAL VISUALIZATION
       
                 ^  [Upper West]   [Upper East]
                / \      *              *
               |   |        [Northern]
               |   |            * (Tamale)
               |   |
               |   |        [Ashanti]
               |   |       * (Kumasi)
               \   /
                \ /        * (Accra)  [Greater Accra]
                 v  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    Gulf of Guinea (Dark Ocean Backdrop)
```

---

## 🛠️ Prerequisites & Package Setup

To run this pipeline, you will need standard R spatial libraries. Install them in your R console before running the script:

```R
# Install required libraries from CRAN
install.packages(c("tidyverse", "sf", "terra", "tidyterra", "geodata", "blackmarbler"))
```

### Key Libraries Explained
*   **`sf`**: Handles vector data (administrative borders).
*   **`terra`**: Handles large, high-performance raster operations (clipping, masking, transformations).
*   **`tidyterra`**: Provides `geom_spatraster()` to directly map raster objects inside `ggplot2`.
*   **`geodata`**: Automates downloading administrative boundaries from GADM.
*   **`blackmarbler`**: Connects directly to the NASA Earthdata API to download, mosaic, and crop Black Marble nighttime lights rasters programmatically.

---

## 📡 Programmatic Data Acquisition via NASA Earthdata

Rather than downloading massive global files manually and cropping them, the R package **`blackmarbler`** (maintained by the World Bank Group) allows you to download and crop VIIRS data programmatically. 

### How to Get Your NASA Token
To pull the data programmatically, NASA requires registration (to prevent abuse of their servers). This process is free and takes less than a minute:
1.  **Register:** Create a free account at [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov/users/new).
2.  **Generate a Bearer Token:** Once logged in, navigate to your **Profile** and click **Generate Token**. Copy this string.
3.  **Run the Script:** Run the script in RStudio. R will prompt you in the console to paste your token, then download the exact tiles needed for Ghana, mosaic them, and clip them to the country boundaries automatically.

---

## 🎨 Visual Design System for "Glow" Aesthetics

To match the premium look of NASA's visualizations, we must design the map with care:

### 1. The Logarithmic Transformation (Critical)
Nightlight intensity values are heavily skewed. The difference between Accra's bright center and a small rural village is orders of magnitude. 
*   **Without log-scaling**: Accra/Kumasi will appear as tiny white dots, and 95% of Ghana will appear pitch black.
*   **With log-scaling (`log1p(x)`)**: It compresses the dynamic range, revealing infrastructure corridors, road networks, and smaller towns.

### 2. High-Contrast Dark Color Palette
The colors transition smoothly from empty space to fiery energy:
*   `#06060c` (Base Space/Ocean)
*   `#140e2d` (Faint Violet Halo for low lights)
*   `#391b6f` (Deep Purple for rural settlements)
*   `#a84200` (Copper Orange for peri-urban areas)
*   `#d87e00` (Warm Amber for town centers)
*   `#f1c40f` (Golden Yellow for city cores)
*   `#ffffff` (Electric White for maximum intensity)

### 3. Anchoring the Landmass
Plotting the country boundary with a very dark fill (`#0d0d18`) behind the transparent parts of the raster anchors the map. This makes the shape of Ghana visible even in areas without any nighttime lights.

---

## 💻 Implementation Script (R)

The code below is available in your workspace as [visualize_ghana_nightlights.R](file:///c:/YERBO/Desktop/CODING/R%20BASICS/visualize_ghana_nightlights.R).

```R
# ==============================================================================
# Programmatic & Styled VIIRS Nighttime Lights Map of Ghana
# ==============================================================================

library(sf)
library(terra)
library(tidyverse)
library(tidyterra)
library(geodata)
library(blackmarbler)

# ------------------------------------------------------------------------------
# 1. Configuration & Folders
# ------------------------------------------------------------------------------
dir.create("data", showWarnings = FALSE)
dir.create("output", showWarnings = FALSE)

# ------------------------------------------------------------------------------
# 2. Get Administrative Boundary for Ghana
# ------------------------------------------------------------------------------
message("1. Fetching Ghana administrative boundary...")
ghana_vector <- gadm(country = "GHA", level = 0, path = "data", version = "latest") %>%
  st_as_sf()

# ------------------------------------------------------------------------------
# 3. Retrieve VIIRS Nightlight Data (Programmatic vs Local)
# ------------------------------------------------------------------------------
# Choose your download method: TRUE = download programmatically, FALSE = load local file
DOWNLOAD_PROGRAMMATICALLY <- TRUE 

if (DOWNLOAD_PROGRAMMATICALLY) {
  message("\n--- PROGRAMMATIC DOWNLOAD VIA NASA EARTHDATA ---")
  message("To download, you need a free NASA Earthdata account.")
  message("Register here if you don't have one: https://urs.earthdata.nasa.gov/")
  message("Get your token here: https://urs.earthdata.nasa.gov/profile -> 'Generate Token'")
  
  # Prompt for token (interactive)
  bearer_token <- readline(prompt = "Enter your NASA Earthdata Bearer Token: ")
  
  if (nchar(bearer_token) == 0) {
    stop("Error: NASA Bearer Token is required for programmatic download.")
  }
  
  message("\nDownloading & processing VIIRS VNP46A4 Annual Composite for 2023...")
  # bm_raster handles tile checking, downloading, mosaicing, and cropping to Ghana
  viirs_raw <- bm_raster(
    roi_sf = ghana_vector,
    product_id = "VNP46A4",
    date = 2023,
    bearer = bearer_token
  )
  
  # Save the downloaded crop locally to avoid redownloading next time
  writeRaster(viirs_raw, "data/ghana_viirs_2023.tif", overwrite = TRUE)
  message("Downloaded raster saved to 'data/ghana_viirs_2023.tif'")
  
} else {
  # Local fallback
  viirs_raster_path <- "data/ghana_viirs_2023.tif"
  if (!file.exists(viirs_raster_path)) {
    stop(paste("File not found at:", viirs_raster_path, "\nPlease set DOWNLOAD_PROGRAMMATICALLY <- TRUE or download the TIFF manually."))
  }
  message("Loading local VIIRS raster...")
  viirs_raw <- rast(viirs_raster_path)
}

# ------------------------------------------------------------------------------
# 4. Processing & Transform
# ------------------------------------------------------------------------------
message("\n2. Processing data...")
# Align Coordinate Reference Systems
ghana_projected <- st_transform(ghana_vector, crs(viirs_raw))

# Mask the cropped raster to the exact boundaries of Ghana
viirs_masked <- mask(viirs_raw, vect(ghana_projected))

# Apply log1p transformation to bring out subtle rural networks and small towns
viirs_log <- log1p(viirs_masked)

# ------------------------------------------------------------------------------
# 5. Styling and Plotting (ggplot2)
# ------------------------------------------------------------------------------
message("3. Generating the map layout...")

# Premium NASA-style night-glow palette
nightlights_palette <- c(
  "#06060c", # Dark space background (no light)
  "#140e2d", # Faint purple-blue halo (very low light)
  "#391b6f", # Deep violet (low-medium light)
  "#a84200", # Copper orange (medium light)
  "#d87e00", # Warm amber (medium-high light)
  "#f1c40f", # Golden yellow (high light)
  "#ffffff"  # Electric white (intense urban centers)
)

p <- ggplot() +
  # Draw a subtle background for the entire landmass of Ghana to anchor the map
  geom_sf(
    data = ghana_projected,
    fill = "#0d0d18",
    color = "#1d1d2f",
    linewidth = 0.25
  ) +
  
  # Plot the VIIRS raster using tidyterra
  geom_spatraster(data = viirs_log) +
  
  # Apply gradient scale
  scale_fill_gradientn(
    colors = nightlights_palette,
    na.value = "transparent",
    name = "Luminosity Index (Log Scale)"
  ) +
  
  coord_sf(expand = FALSE) +
  
  # Theme Overrides for dark background styling
  theme_void() +
  theme(
    panel.background = element_rect(fill = "#06060c", color = NA),
    plot.background = element_rect(fill = "#06060c", color = NA),
    legend.position = "bottom",
    legend.title = element_text(color = "gray80", size = 8.5, face = "bold"),
    legend.text = element_text(color = "gray60", size = 7.5),
    legend.key.width = unit(1.8, "cm"),
    legend.key.height = unit(0.25, "cm"),
    plot.title = element_text(
      color = "#ffffff", 
      size = 18, 
      face = "bold", 
      hjust = 0.5, 
      margin = margin(t = 25, b = 5)
    ),
    plot.subtitle = element_text(
      color = "gray75", 
      size = 10, 
      hjust = 0.5, 
      margin = margin(b = 20)
    ),
    plot.caption = element_text(
      color = "gray45", 
      size = 7, 
      hjust = 0.5, 
      margin = margin(t = 15, b = 20)
    )
  ) +
  
  # Titles & Captions
  labs(
    title = "GHANA AT NIGHT",
    subtitle = "Infrastructure corridors & urban settlement patterns observed via VIIRS satellite sensors",
    caption = "Data: NASA Black Marble VIIRS DNB (2023) | Cartography: R + ggplot2 + terra + blackmarbler"
  )

# ------------------------------------------------------------------------------
# 6. Save Visualization (High Resolution)
# ------------------------------------------------------------------------------
output_file <- "output/ghana_nightlights_map.png"
message(paste("\n4. Saving final map to", output_file))

ggsave(
  filename = output_file,
  plot = p,
  width = 8.5,
  height = 11,
  dpi = 400,
  bg = "#06060c"
)

message("Success! Your visualization is ready.")
```

---

> [!TIP]
> **Caching the Data**
> Once the program downloads the dataset for the first time, it automatically saves the cropped region as `data/ghana_viirs_2023.tif`. On subsequent runs, you can set `DOWNLOAD_PROGRAMMATICALLY <- FALSE` in the script to load it instantaneously offline.

> [!WARNING]
> **Outlier Noise**
> Standard VIIRS annual composites may occasionally contain extreme pixel values from persistent gas flares or atmospheric noise. The log transformation (`log1p`) handles high values well, but if you notice bright artifacts outside city limits, filter them out using: `viirs_raw[viirs_raw < 0] <- 0` or clamp the upper limit prior to plotting.
