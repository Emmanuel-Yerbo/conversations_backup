# 🌍 WebGIS Mastery Course: Intermediate → Advanced

> A self-paced, project-driven curriculum to take you from competent GIS user to full-stack WebGIS engineer.

---

## Course Philosophy

> [!IMPORTANT]
> **Focus on fundamentals over frameworks.** Technologies change rapidly, but core principles — how spatial data is indexed, how web requests work, how to optimize memory and rendering — remain constant. Every module pairs theory with a hands-on project.

---

## Technology Landscape Overview

Before diving in, understand the ecosystem you'll be navigating:

### Frontend Mapping Libraries

| Library | Rendering | Best For | Learning Curve |
|:---|:---|:---|:---|
| **Leaflet** | DOM/SVG | Simple 2D maps, prototypes, mobile-first | ⭐ Low |
| **OpenLayers** | Canvas/WebGL | Enterprise GIS, OGC compliance, complex projections | ⭐⭐⭐ High |
| **MapLibre GL JS** | WebGL | High-perf vector tiles, custom-styled maps, 3D extrusions | ⭐⭐ Medium |
| **CesiumJS** | WebGL/WebGPU | True 3D globes, digital twins, photorealistic terrain | ⭐⭐⭐ High |
| **deck.gl** | WebGL | Massive dataset visualization, GPU-accelerated layers | ⭐⭐ Medium |

### Cloud-Native Geospatial Formats

| Format | Type | Use Case |
|:---|:---|:---|
| **COG** (Cloud Optimized GeoTIFF) | Raster | Streaming raster imagery from cloud storage |
| **PMTiles** | Tiles (raster/vector) | Single-file tile pyramids, serverless map hosting |
| **FlatGeobuf** | Vector | Streamable vectors with built-in spatial index |
| **GeoParquet** | Vector/Analytics | Columnar analytics, DuckDB/Spark integration |
| **Zarr** | Raster/N-D Arrays | Multi-dimensional scientific data (climate, weather) |

### OGC Standards Evolution

| Legacy Standard | Modern Replacement | Protocol |
|:---|:---|:---|
| WMS (Web Map Service) | OGC API – Maps | REST/JSON |
| WFS (Web Feature Service) | OGC API – Features | REST/GeoJSON |
| WMTS (Web Map Tile Service) | OGC API – Tiles | REST/JSON |
| CSW (Catalogue Service) | OGC API – Records | REST/JSON |
| SWE (Sensor Web) | OGC API – Connected Systems | REST/JSON |

---

## 📚 MODULE 1: Web Mapping Foundations (Weeks 1–3)

### 1.1 — How Web Maps Work (Theory)
- The client-server model for geospatial data
- Tile pyramids: XYZ, TMS, and quadkey schemes
- Map projections on the web (EPSG:3857 vs EPSG:4326)
- Coordinate reference systems and on-the-fly reprojection
- The HTTP request lifecycle for map tiles

### 1.2 — Leaflet Deep Dive
- Setting up a dev environment (VS Code, Live Server, npm)
- Tile layers: OpenStreetMap, Stadia, Thunderforest, custom
- GeoJSON: loading, styling, filtering, interactivity
- Marker clustering with `Leaflet.markercluster`
- Custom controls, popups, tooltips
- Layer groups and overlay management
- Responsive mobile-first map design
- Plugin ecosystem: Draw, MeasurePath, Heatmap, MiniMap

### 1.3 — OpenLayers for GIS Professionals
- Architecture: Map → View → Layer → Source → Style
- Loading WMS/WFS/WMTS from GeoServer
- Vector layers with complex styling (rules, expressions)
- Custom projections with `proj4js`
- Feature selection, modification, and snapping
- Overlay popups and coordinate display
- Print/export map views

### 🔨 Project 1: Multi-Layer Thematic Map Viewer
Build an interactive map of Ghana showing administrative boundaries, health facilities, and road networks using Leaflet. Include layer toggle, search, legend, and responsive sidebar.

**Skills practiced:** GeoJSON handling, layer management, UI/UX design, event handling.

---

## 📚 MODULE 2: Spatial Databases & Backend Engineering (Weeks 4–6)

### 2.1 — PostgreSQL + PostGIS Mastery
- Installation and spatial database setup
- `CREATE EXTENSION postgis;` and spatial reference tables
- Importing data: `shp2pgsql`, `ogr2ogr`, QGIS DB Manager
- Geometry types: Point, LineString, Polygon, Multi*, GeometryCollection
- Spatial indexing: GiST indexes and query planning (`EXPLAIN ANALYZE`)
- Core spatial functions:
  - `ST_Intersects`, `ST_Contains`, `ST_Within`, `ST_DWithin`
  - `ST_Buffer`, `ST_Union`, `ST_Difference`
  - `ST_Area`, `ST_Length`, `ST_Distance`
  - `ST_Transform` (CRS conversion)
  - `ST_Simplify`, `ST_SimplifyPreserveTopology`
- Window functions for spatial analytics
- Raster support: `raster2pgsql`, `ST_Value`, `ST_MapAlgebra`

### 2.2 — Building Geospatial APIs
- **Python/FastAPI** for RESTful geospatial endpoints
- **Node.js/Express** alternative path
- Connecting to PostGIS with `asyncpg` / `pg` drivers
- Returning GeoJSON from SQL queries
- Spatial query endpoints: bounding box, radius search, point-in-polygon
- Pagination, filtering, and error handling
- API documentation with OpenAPI/Swagger
- Authentication with JWT tokens and API keys

### 2.3 — Data Pipelines & ETL
- Python geospatial stack: `GeoPandas`, `Shapely`, `Fiona`, `Rasterio`
- Automated data ingestion scripts
- Data validation and cleaning workflows
- Coordinate transformation pipelines
- Scheduling with cron / Windows Task Scheduler

### 🔨 Project 2: Geospatial REST API
Build a FastAPI backend connected to PostGIS that serves Ghana district boundaries, performs spatial queries (find nearest facility, point-in-polygon lookup), and returns GeoJSON. Deploy with Docker.

**Skills practiced:** SQL, PostGIS, REST API design, Python, Docker basics.

---

## 📚 MODULE 3: Map Servers & OGC Standards (Weeks 7–9)

### 3.1 — GeoServer Administration
- Installation (standalone + Docker)
- Workspace, Store, and Layer concepts
- Connecting PostGIS stores
- Publishing vector and raster layers
- SQL Views for dynamic, parameterized layers
- SLD (Styled Layer Descriptor) styling
- GeoWebCache: tile caching and seeding
- REST API for programmatic administration
- CORS configuration for frontend integration

### 3.2 — OGC Web Services In-Depth
- **WMS**: GetCapabilities, GetMap, GetFeatureInfo
- **WFS**: GetFeature, Transaction (insert/update/delete)
- **WMTS**: RESTful and KVP tile access
- **WCS**: Web Coverage Service for raster data
- **WPS**: Web Processing Service for server-side analysis
- CQL/ECQL filters for server-side data filtering
- SLD styling rules, classifications, and label placement

### 3.3 — Modern OGC API Standards
- OGC API – Features (successor to WFS)
- OGC API – Tiles (successor to WMTS)
- OGC API – Maps (successor to WMS)
- OGC API – Records (metadata catalog)
- Building blocks philosophy: modular, RESTful, JSON-first
- STAC (SpatioTemporal Asset Catalog) for imagery discovery
- Implementing with `pygeoapi` (Python OGC API server)

### 🔨 Project 3: Full-Stack OGC Map Portal
Deploy GeoServer with Docker, connect to PostGIS, publish layers via WMS/WFS, and build an OpenLayers frontend that consumes these services. Add GetFeatureInfo popups, CQL filtering, and a print layout.

**Skills practiced:** GeoServer admin, OGC standards, OpenLayers integration, Docker.

---

## 📚 MODULE 4: High-Performance Frontend & Modern Frameworks (Weeks 10–12)

### 4.1 — MapLibre GL JS
- Vector tile specification (Mapbox Vector Tile / MVT)
- Style specification: layers, sources, expressions
- Data-driven styling with `match`, `interpolate`, `step`
- 3D building extrusions and terrain
- Custom map styles with Maputnik editor
- Adding GeoJSON, image, and video sources
- Camera animations and fly-to transitions
- Events, popups, and custom controls

### 4.2 — Integrating with Modern JS Frameworks
- **React + MapLibre** (using `react-map-gl` or refs)
- **Vue + Leaflet/MapLibre** (component patterns)
- State management for map applications
- Component architecture: MapContainer, LayerPanel, Legend, Sidebar
- Routing and multi-page map applications

### 4.3 — Advanced Visualization
- **deck.gl**: ScatterplotLayer, HexagonLayer, ArcLayer, TripsLayer
- Kepler.gl for rapid geospatial exploration
- Heatmaps, hexbins, and flow maps
- Time-series animation on maps
- Custom WebGL shaders for unique visualizations

### 4.4 — Client-Side Spatial Analysis
- **Turf.js**: buffer, union, intersect, dissolve, voronoi
- Isochrone generation and service area analysis
- Distance matrices and nearest-neighbor
- Client-side raster analysis with `geotiff.js`
- DuckDB-WASM for in-browser SQL on GeoParquet

### 🔨 Project 4: Urban Analytics Dashboard
Build a React + MapLibre application showing urban indicators (population density, land use, accessibility). Include deck.gl layers for large-scale point visualization, Turf.js for on-the-fly buffer analysis, and a responsive dashboard with charts (Chart.js/Recharts).

**Skills practiced:** React, MapLibre, deck.gl, Turf.js, data visualization, responsive design.

---

## 📚 MODULE 5: Cloud-Native Geospatial & Serverless Architecture (Weeks 13–15)

### 5.1 — Cloud-Optimized Formats
- **COG** (Cloud Optimized GeoTIFF): creation with `gdal_translate`, serving via Titiler
- **PMTiles**: creating with `tippecanoe`, hosting on S3/static CDN
- **FlatGeobuf**: conversion, HTTP range request streaming
- **GeoParquet**: creation with GeoPandas, querying with DuckDB
- **Zarr**: multi-dimensional array storage for climate data

### 5.2 — Serverless WebGIS Architecture
- Static hosting of PMTiles on GitHub Pages / Cloudflare
- AWS Lambda / Vercel Functions for on-demand spatial processing
- Titiler for dynamic COG visualization without a tile server
- STAC API for asset catalog and discovery
- Browser-based processing with WebAssembly (GDAL-WASM, DuckDB-WASM)

### 5.3 — Data Discovery with STAC
- STAC specification: Items, Collections, Catalogs
- Searching satellite imagery catalogs (Element84, Microsoft Planetary Computer)
- Building a custom STAC catalog for your data
- `pystac` and `pystac-client` for Python workflows

### 🔨 Project 5: Serverless Satellite Imagery Explorer
Build a zero-server-cost web app that uses STAC API to search Sentinel-2 imagery, displays COGs via Titiler, and overlays vector data from PMTiles. Host everything on static infrastructure (GitHub Pages + Cloudflare R2).

**Skills practiced:** Cloud-native formats, STAC, serverless architecture, cost optimization.

---

## 📚 MODULE 6: 3D, Real-Time & Emerging Technologies (Weeks 16–18)

### 6.1 — 3D WebGIS with CesiumJS
- Cesium ion and 3D Tiles
- Terrain providers and elevation data
- KML, CZML, and GeoJSON on a 3D globe
- Point cloud visualization (LiDAR)
- Building models and BIM integration
- Time-dynamic data and animation

### 6.2 — Real-Time Geospatial Streaming
- WebSocket fundamentals for spatial data
- MQTT protocol for IoT sensor streams
- Building a real-time vehicle/asset tracker
- Server-Sent Events (SSE) for push updates
- Handling high-frequency location updates at scale

### 6.3 — GeoAI Integration
- Serving ML models via FastAPI endpoints
- Object detection on satellite imagery (YOLO, Segment Anything)
- Integration with Google Earth Engine JavaScript API
- Client-side inference with TensorFlow.js / ONNX Runtime Web
- Spatial prediction visualization (heatmaps, uncertainty maps)
- LLM-powered natural language spatial queries

### 6.4 — Progressive Web Apps (PWA) & Offline Mapping
- Service workers for offline tile caching
- IndexedDB for offline feature storage
- Mobile-first field data collection apps
- GPS/geolocation integration
- Sync strategies for intermittent connectivity

### 🔨 Project 6: IoT Environmental Monitoring Dashboard
Build a real-time dashboard that ingests simulated sensor data (air quality, temperature) via WebSockets, displays live readings on a MapLibre map with deck.gl heatmaps, stores historical data in PostGIS, and includes time-series charts and threshold alerts.

**Skills practiced:** Real-time streaming, WebSockets, deck.gl, time-series, full-stack.

---

## 📚 MODULE 7: Security, DevOps & Production Deployment (Weeks 19–20)

### 7.1 — WebGIS Security
- Authentication: OAuth 2.0, OpenID Connect, JWT
- Authorization: RBAC and attribute-based access control
- HTTPS enforcement and CORS configuration
- API key management and rate limiting
- Securing GeoServer: role-based layer access
- Input validation for spatial queries (SQL injection prevention)
- Data governance and metadata standards (ISO 19115)

### 7.2 — Containerization & DevOps
- Docker fundamentals for GIS stack
- `docker-compose` for PostGIS + GeoServer + Nginx + App
- Kubernetes basics for scalable deployments
- CI/CD pipelines (GitHub Actions)
- Infrastructure as Code with Terraform
- Monitoring with Prometheus + Grafana
- Centralized logging (ELK / Loki)

### 7.3 — Performance at Scale
- Vector tile optimization (geometry simplification, attribute pruning)
- Multi-tiered caching (DB → server → CDN → browser)
- Lazy loading and viewport-based data fetching
- WebGL rendering optimization and clustering
- Database query tuning with `EXPLAIN ANALYZE`
- Load testing with k6 or Locust

---

## 📚 MODULE 8: Capstone & Portfolio (Weeks 21–24)

### Choose One Major Capstone Project

#### Option A: Precision Agriculture WebGIS Platform
Full-stack platform for farm management: upload field boundaries, visualize NDVI time-series from Sentinel-2 (via STAC/COG), overlay soil data, and generate variable-rate prescription maps. Uses PostGIS, FastAPI, MapLibre, and deck.gl.

#### Option B: Urban Digital Twin
3D city model viewer using CesiumJS with building footprints, terrain, real-time transit overlay, and indoor floor plans. Integrates 3D Tiles, GTFS feeds, and GeoServer WFS.

#### Option C: Disaster Response Coordination Portal
Multi-user WebGIS for flood/earthquake response: real-time field reports, affected area polygons, resource allocation dashboard, offline-capable PWA mode for field workers. Uses WebSockets, PostGIS, MapLibre.

#### Option D: National SDI Portal
Build a spatial data infrastructure portal with metadata catalog (OGC API – Records), map services (OGC API – Maps/Tiles), data download, and user management. Demonstrates enterprise-grade WebGIS architecture.

### Portfolio Strategy

> [!TIP]
> **Quality over quantity.** One well-documented, deployed full-stack project beats five tutorial clones. Every project should answer: *"What real-world problem does this solve?"*

- Write detailed `README.md` files explaining **Why → How → Results**
- Include live demo links (Vercel, GitHub Pages, Railway)
- Record 2-minute video walkthroughs
- Blog about your technical decisions on Medium/Dev.to
- Contribute to open-source GIS projects (MapLibre, GeoServer, Turf.js)

---

## 🛠 Recommended Tool Stack

```
Frontend:    MapLibre GL JS + React/Vue + deck.gl + Turf.js
Backend:     Python (FastAPI) or Node.js (Express)
Database:    PostgreSQL + PostGIS
Map Server:  GeoServer (Docker) + pygeoapi
Formats:     GeoJSON, PMTiles, COG, GeoParquet, FlatGeobuf
DevOps:      Docker, GitHub Actions, Nginx
Cloud:       AWS S3 / Cloudflare R2 for static hosting
Design:      Figma for UI mockups
```

---

## 📖 Recommended Learning Resources

### Documentation (Primary Sources)
- [Leaflet Docs](https://leafletjs.com/reference.html)
- [OpenLayers Docs](https://openlayers.org/en/latest/apidoc/)
- [MapLibre GL JS Docs](https://maplibre.org/maplibre-gl-js/docs/)
- [CesiumJS Docs](https://cesium.com/learn/)
- [deck.gl Docs](https://deck.gl/docs)
- [Turf.js Docs](https://turfjs.org/)
- [PostGIS Reference](https://postgis.net/docs/)
- [GeoServer User Manual](https://docs.geoserver.org/)
- [OGC API Standards](https://ogcapi.ogc.org/)
- [STAC Spec](https://stacspec.org/)
- [Cloud-Native Geo](https://cloudnativegeo.org/)

### Courses & Tutorials
- Penn State GEOG 585: Open Web Mapping (free)
- Boundless/GeoServer workshops
- PostGIS tutorial by Boundless
- MapLibre Academy
- deck.gl examples gallery

### Community
- [GIS Stack Exchange](https://gis.stackexchange.com/)
- [OSGeo Mailing Lists](https://www.osgeo.org/)
- FOSS4G Conference talks (YouTube)
- r/gis and r/geospatial on Reddit

---

## ⏱ Suggested Weekly Time Commitment

| Phase | Weeks | Hours/Week | Focus |
|:---|:---|:---|:---|
| Modules 1–3 (Intermediate) | 1–9 | 10–12 | Foundations, databases, standards |
| Modules 4–5 (Advanced) | 10–15 | 12–15 | Modern frontend, cloud-native |
| Modules 6–7 (Specialist) | 16–20 | 12–15 | 3D, real-time, AI, DevOps |
| Module 8 (Capstone) | 21–24 | 15–20 | Portfolio project |

**Total: ~24 weeks (6 months) at 10–20 hrs/week**

---

> [!NOTE]
> This curriculum is tailored for someone with GIS fundamentals and basic programming skills. Given your GeoAI and remote sensing background, you may accelerate through Modules 1–2 and spend more time on Modules 5–6 where cloud-native and AI integration intersect with your research interests.
