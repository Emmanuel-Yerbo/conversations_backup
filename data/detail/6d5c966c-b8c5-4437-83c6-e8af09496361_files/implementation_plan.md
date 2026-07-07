# Night-Time Light Visualization of Accra (VIIRS)

This document outlines the proposed strategy to brainstorm and implement a night-time light visualization of the Accra Metropolis using NASA's VIIRS data in R. 

## Overview

Visualizing night-time lights involves spatial data manipulation: acquiring a raster dataset of the lights, acquiring a vector dataset of the city boundary, cropping the raster to the boundary, and rendering it beautifully.

NASA's VIIRS (Visible Infrared Imaging Radiometer Suite) provides excellent high-resolution night-time light data, commonly known as the "Black Marble" product.

## Implementation Approaches

We have a few different technical paths we can take in R to achieve this. Please review these and let me know your preference:

### Option 1: The `blackmarbler` R Package (Recommended for pure R workflow)
We can use the `blackmarbler` R package, which is specifically designed to interact with NASA's Earthdata API to download Black Marble products (like VNP46A1 - daily radiance, or VNP46A4 - annual).
* **Pros**: Native R workflow, automated downloading.
* **Cons**: You will need to create a free NASA Earthdata account and generate a Bearer Token to authenticate the API requests.

### Option 2: Google Earth Engine via `rgee`
We can use the `rgee` package to run Google Earth Engine (GEE) commands from within R. GEE hosts vast amounts of VIIRS data.
* **Pros**: Extremely fast processing, no need to download massive global datasets locally.
* **Cons**: Requires a Google Earth Engine account, Python installed on your system, and setting up the `rgee` environment, which can sometimes be tricky to configure initially.

### Option 3: Manual Download & Local Processing
You can manually download a Geotiff of the VIIRS data for West Africa (or globally) from the Earth Observation Group (EOG) or NASA Earthdata portal, save it in your workspace, and we write R code to load and process it.
* **Pros**: No need for API keys or complex environment setups in R.
* **Cons**: Requires you to manually find and download a potentially large file.

---

## Step-by-Step Plan (Assuming Option 1 or 3)

### 1. Setup & Area of Interest (AOI) Definition
* Install/Load required spatial packages: `sf`, `terra`, `tidyterra`, `ggplot2`, `geodata`.
* Fetch the administrative boundary for Accra Metropolis using the `geodata` or `rnaturalearth` package.

### 2. Data Acquisition
* Fetch the VIIRS night-time light raster data (either via API or loading a local file). 
* We will likely aim for a composite image (e.g., monthly or annual average) to reduce cloud cover noise.

### 3. Data Processing
* Load the raster using the `terra` package.
* **Crop** the global/regional VIIRS raster to the bounding box of Accra.
* **Mask** the raster so that areas outside the exact Accra boundary are set to NA (transparent).
* Log-transform the radiance values (night lights have a very high dynamic range; log transformation helps visualize dim and bright lights simultaneously).

### 4. Visualization
* Use `ggplot2` combined with `tidyterra` to render the spatial raster.
* Apply a dark theme and a striking color palette (like `viridis::inferno` or a custom black-to-yellow/white gradient).
* Add contextual elements: title, scale bar, north arrow, and maybe basic street maps as a dim background context using `maptiles`.
* Alternatively, create an interactive web map using `leaflet`.

## Open Questions

> [!IMPORTANT]
> 1. **Which data acquisition approach do you prefer?** (Option 1: `blackmarbler` API, Option 2: `rgee`, or Option 3: Manual Geotiff download).
> 2. **What time frame are you interested in?** Do you want a single recent night, a monthly average, or an annual average (e.g., for the year 2023)?
> 3. **What type of visualization do you prefer?** A high-quality static image (good for reports/presentations) or an interactive map (good for exploring)?
