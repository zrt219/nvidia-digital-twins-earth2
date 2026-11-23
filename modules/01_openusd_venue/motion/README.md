# OpenMotion Programmatic Video: Italian Venue OpenUSD Showcase

This sub-module provides a code-driven, programmatic motion graphics composition built with **OpenMotion** (`@open-motion/core`) and React. It visually demonstrates the non-destructive OpenUSD stage hierarchy, deferred payload architecture, and dynamic `variantSet` switching in the Italian venue digital twin.

---

## 🎬 Video Overview

- **Source File**: `src/VenueShowcaseVideo.tsx`
- **Output Target**: `reports/videos/openusd_venue_openmotion.mp4`
- **Resolution**: 1920 × 1080 (1080p Full HD)
- **Framerate**: 60 FPS
- **Duration**: 300 frames (5.0 seconds)

### Visual Composition Breakdown
1. **Header & Telemetry**:
   - Live stage unit indicators (`metersPerUnit = 1.0`, `upAxis = "Y"`).
   - Real-time active `variantSet` indicator badge (`standard_seating` vs. `gala_banquet`).
2. **Left Panel: LIVRPS Stage Hierarchy**:
   - Progressive unfolding of the OpenUSD prim tree:
     - `/World` (Stage Root, defaultPrim)
     - `/World/Venue` (Assembly prim)
     - `/World/Venue/Architecture` (Deferred payload arc pointing to `venue_architecture_payload.usda`)
     - `/World/Venue/Lighting` (SphereLight + DomeLight)
     - `/World/Venue/Layout` (Active variantSet)
   - Telemetry card demonstrating **94.2% memory savings** via payload deferral.
3. **Right Viewport: Animated Spatial Projection**:
   - Dynamic 2.5D camera pan across the venue floorplan.
   - Smooth spring-interpolated transition at frame 150 from **Auditorium Seating** (podium + 120 seats) to **Gala Banquet** (12 round tables + dinner setup).

---

## 🚀 Execution & Rendering

### Prerequisites
- Node.js >= 18.0.0
- npm >= 9.0.0

### 1. Install Dependencies
```bash
cd modules/01_openusd_venue/motion
npm install
```

### 2. Interactive Preview in Browser
Launch the OpenMotion interactive player to scrub frames, inspect easing curves, and toggle variants:
```bash
npm run dev
# or: npx open-motion preview src/VenueShowcaseVideo.tsx
```

### 3. Headless MP4 Video Render
Render the broadcast-quality MP4 file via OpenMotion CLI and FFmpeg:
```bash
npm run render
```

This compiles `src/VenueShowcaseVideo.tsx` into:
```
reports/videos/openusd_venue_openmotion.mp4
```

---

## 📐 Technical Architecture & OpenUSD Alignment

| OpenUSD Concept | OpenMotion Implementation |
| :--- | :--- |
| **Payload Arc** | Highlighted deferred loading badge with zero memory footprint until triggered |
| **VariantSet** | Spring-interpolated opacity & translation morphing between Auditorium and Banquet layouts |
| **Stage Coordinates** | Synchronized camera coordinates matching SI meters ($x, y, z$) |
| **LIVRPS Precedence** | Visual tree showing evaluation priority from Local overrides down to Payloads |
