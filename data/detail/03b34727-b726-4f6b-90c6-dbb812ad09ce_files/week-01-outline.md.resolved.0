# Week 01 — How Web Maps Work: From Pixels to Planet

## Module: 01 — Web Mapping Foundations
## Duration: ~10–12 hours (Theory: 5–6 hrs | Practice: 5–6 hrs)

---

## 🎯 Learning Objectives

By the end of this week, you will be able to:

1. Explain the full architecture of a WebGIS application (client → server → database)
2. Describe how tile pyramids work and calculate tile counts at any zoom level
3. Distinguish between EPSG:4326 and EPSG:3857 and explain why web maps use Mercator
4. Trace the complete HTTP request lifecycle when a map tile loads
5. Read, write, and manipulate GeoJSON by hand
6. Build a multi-layer interactive web map using Leaflet.js
7. Add markers, popups, GeoJSON overlays, and basemap switching

---

## PART 1: THEORY NOTEBOOK

### Section 1 — What is WebGIS?
- **1.1** Definition: GIS delivered through web browsers
- **1.2** Evolution: Desktop GIS → Server GIS → Cloud GIS → WebGIS
  - ArcInfo (1982) → MapServer (1997) → Google Maps (2005) → Modern era
- **1.3** Why WebGIS matters: accessibility, collaboration, real-time data, no installation
- **1.4** WebGIS vs Desktop GIS: a comparison table
  - Data storage, processing location, user access, update cycle, cost model
- **1.5** Real-world WebGIS examples
  - Google Maps, OpenStreetMap, USGS National Map, Ghana CERSGIS portals
  - Humanitarian: HDX, MapAction disaster maps
  - Agriculture: CropMonitor, FEWS NET
- **📝 Knowledge Check 1**: Multiple-choice quiz (5 questions)

### Section 2 — The Client-Server Architecture
- **2.1** The three-tier model:
  - **Client (Frontend)**: Browser renders maps, handles user interaction
  - **Server (Middleware)**: Processes requests, serves data (GeoServer, MapServer, Tile servers)
  - **Database (Backend)**: Stores spatial data (PostGIS, file-based, cloud storage)
- **2.2** How a web map request flows (step-by-step):
  1. User opens browser → loads HTML/CSS/JS
  2. JavaScript map library initializes (Leaflet, OpenLayers)
  3. Library calculates which tiles are visible
  4. HTTP GET requests sent to tile server
  5. Server returns 256×256 PNG/JPEG tiles (or vector PBF tiles)
  6. Browser composites tiles into seamless map
  7. User interaction triggers new tile requests
- **2.3** Thin client vs thick client architectures
  - Thin: server does processing, client just displays (WMS approach)
  - Thick: client does processing with raw data (WFS + client-side rendering)
- **2.4** REST APIs in WebGIS: request/response patterns
- **2.5** Diagram: Complete data flow from database to user's screen
- **📝 Knowledge Check 2**: Label-the-diagram exercise + 4 questions

### Section 3 — Tile Pyramids & Slippy Maps
- **3.1** Why not one giant image? (bandwidth, rendering, caching)
- **3.2** The tile pyramid concept:
  - Zoom level 0: entire world = 1 tile (256×256 px)
  - Zoom level 1: 4 tiles (2×2)
  - Zoom level z: 2^z × 2^z = 4^z tiles
  - Zoom level 18: ~68 billion tiles
- **3.3** The XYZ tile addressing scheme:
  - URL pattern: `https://tile.server.com/{z}/{x}/{y}.png`
  - z = zoom level, x = column (west→east), y = row (north→south)
- **3.4** TMS vs XYZ vs Quadkey:
  - TMS: y-axis flipped (south→north)
  - Quadkey: Bing Maps' single-string addressing
- **3.5** Raster tiles vs Vector tiles:
  - Raster: pre-rendered images (PNG/JPEG), simple but inflexible
  - Vector: raw geometry data (PBF/MVT), styled client-side, interactive
- **3.6** Tile caching and CDNs: why maps load fast
- **3.7** Interactive element: Tile calculator
  - Input a zoom level → see tile count, total pixels, and storage estimate
- **📝 Knowledge Check 3**: Calculate tiles at zoom levels + 5 questions

### Section 4 — Map Projections on the Web
- **4.1** The fundamental problem: Earth is 3D, screens are 2D
- **4.2** What is a map projection? (mathematical transformation)
- **4.3** Projection families: Cylindrical, Conic, Azimuthal
- **4.4** EPSG:4326 (WGS 84 Geographic):
  - Latitude/Longitude in degrees
  - Used for storing data, GPS coordinates, GeoJSON
  - Range: Lat [-90, 90], Lng [-180, 180]
- **4.5** EPSG:3857 (Web Mercator):
  - Meters as unit, used by ALL major web tile providers
  - Why Mercator? Conformal (preserves shapes), tiles align to square grid
  - The distortion problem: Greenland vs Africa, area exaggeration at poles
  - Latitude cutoff at ±85.06° (tiles would be infinite)
- **4.6** Why Leaflet uses 4326 but tiles use 3857:
  - You write code in lat/lng → Leaflet reprojects internally
  - Tile URLs use 3857 grid coordinates
- **4.7** Other projections you'll encounter:
  - UTM zones (e.g., Ghana = UTM Zone 30N, EPSG:32630)
  - National grids
- **4.8** Interactive element: Projection distortion visualizer
  - Tissot's indicatrix on Web Mercator
- **📝 Knowledge Check 4**: Identify CRS codes + projection properties

### Section 5 — Geospatial Data Formats for the Web
- **5.1** Vector vs Raster data (review):
  - Vector: Points, Lines, Polygons (discrete features)
  - Raster: Grid of pixels/cells (continuous surfaces)
- **5.2** GeoJSON — The web mapping standard:
  - JSON-based, human-readable, natively supported by all libraries
  - Structure: FeatureCollection → Feature → Geometry + Properties
  - Geometry types: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon
  - CRS: always EPSG:4326 (by specification)
  - Limitations: no topology, verbose, large file sizes
  - Hands-on: write GeoJSON by hand for Ghana cities
- **5.3** TopoJSON:
  - Topology-aware: shared boundaries stored once
  - 50-80% smaller than equivalent GeoJSON
  - Requires conversion step
- **5.4** Shapefile (legacy but ubiquitous):
  - Multi-file format (.shp, .shx, .dbf, .prj)
  - Not web-native — must convert to GeoJSON/GeoPackage
- **5.5** Other formats you'll meet later:
  - GeoPackage (.gpkg): SQLite-based, single file, modern replacement for Shapefile
  - FlatGeobuf (.fgb): Binary, streamable, cloud-native
  - PMTiles: Single-file tile archive
  - GeoParquet: Columnar analytics format
  - CSV with coordinates: Simple but limited
- **5.6** Format selection guide (decision tree)
- **📝 Knowledge Check 5**: Write GeoJSON by hand + format matching

### Section 6 — Introduction to Leaflet.js
- **6.1** What is Leaflet? History and philosophy
  - Created by Volodymyr Agafonkin (2011)
  - Design principle: simplicity, performance, usability
  - ~42KB gzipped — lightweight by design
- **6.2** Core architecture:
  - `L.map()` — the map container
  - `L.tileLayer()` — basemap tiles
  - `L.marker()` — point features
  - `L.popup()` — information windows
  - `L.geoJSON()` — vector data layers
  - `L.control` — UI controls (zoom, layers, scale, attribution)
- **6.3** The Leaflet initialization pattern:
  ```javascript
  const map = L.map('map').setView([lat, lng], zoom);
  L.tileLayer(url, options).addTo(map);
  ```
- **6.4** Event system overview:
  - Map events: click, mousemove, zoomend, moveend
  - Layer events: click, mouseover, mouseout
  - Event object: `e.latlng`, `e.target`, `e.layer`
- **6.5** Plugin ecosystem:
  - Leaflet.markercluster, Leaflet.draw, Leaflet.heat
  - How plugins extend core functionality
- **6.6** Leaflet vs OpenLayers vs MapLibre (when to use what)
- **📝 Knowledge Check 6**: Match Leaflet classes to their purpose

### Section 7 — Bringing It All Together
- **7.1** The complete mental model:
  - Data (PostGIS/files) → Server (GeoServer/tiles) → Network (HTTP) → Client (Leaflet) → Screen
- **7.2** What you'll build in Part 2 (preview)
- **7.3** Key vocabulary glossary (30+ terms)
- **📝 Final Assessment**: Comprehensive 15-question quiz covering all sections

---

## PART 2: PRACTICE LAB

### Lab 01 — Building Your First Interactive Web Map

**Goal**: Build a multi-layer, interactive map of Ghana with custom styling, popups, and controls.

### Step 1 — Project Setup (30 min)
- Create project folder structure
- Set up `index.html` with Leaflet CDN
- Create `style.css` with dark theme
- Create `app.js` with map initialization
- Verify "Hello Map" loads in browser

### Step 2 — Basemap Layers (45 min)
- Add 4 different tile providers:
  - OpenStreetMap (default)
  - CartoDB Dark Matter
  - Esri World Imagery (satellite)
  - OpenTopoMap (topographic)
- Implement layer control (radio buttons for basemaps)
- Understand tile URL templates and attribution

### Step 3 — GeoJSON Data & Markers (60 min)
- Create GeoJSON for 10 Ghana regional capitals (by hand)
- Custom div markers with color coding
- Rich HTML popups with city information
- Marker clustering preparation concepts

### Step 4 — Polygon Overlays (60 min)
- Load Ghana regional boundaries (GeoJSON)
- Style polygons: fill color, opacity, border
- Choropleth concept: color by population/area
- Hover effects: highlight on mouseover
- Click: show region info in sidebar panel

### Step 5 — Interactive Features (60 min)
- Real-time coordinate display (mousemove event)
- Click-to-place markers with coordinate popups
- Scale control and measurement
- Zoom-to-feature functionality
- Responsive design and mobile considerations

### Step 6 — Polish & Challenge (60 min)
- Add a custom legend
- Add a search/geocoding control
- Implement "fly to" animations between cities
- Dark-themed Leaflet controls
- Code review: what each line does

---

## 📦 Deliverables

By end of Week 1, you should have:
- [ ] Completed all 7 theory sections with knowledge checks
- [ ] A working interactive web map of Ghana
- [ ] Understanding of tile pyramids, CRS, GeoJSON, and Leaflet basics
- [ ] Confidence to read Leaflet documentation independently

---

## 📚 Supplementary Resources

- [Leaflet Quick Start Guide](https://leafletjs.com/examples/quick-start/)
- [GeoJSON Specification (RFC 7946)](https://datatracker.ietf.org/doc/html/rfc7946)
- [MapTiler: How Web Maps Work](https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection/)
- [Tom MacWright: How Web Maps Work](https://macwright.com/2012/05/15/how-web-maps-work.html)
- [Leaflet Providers Preview](https://leaflet-extras.github.io/leaflet-providers/preview/)
