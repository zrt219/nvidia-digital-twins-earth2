# Module 01: OpenUSD Venue Measured Scene & Composition Architecture

This module implements the architectural foundation for the **Italian Venue Measured Scene**, fulfilling the **Days 1–30 Milestone** of the 90-day NVIDIA & Geospatial Digital Twins roadmap.

---

## 🏛️ Architectural Overview

The scene represents a high-fidelity Italian historic palazzo / exhibition hall measured digital twin, structured according to production OpenUSD best practices. The composition leverages non-destructive composition arcs to allow dynamic reconfiguration between distinct event layouts without duplicating heavy asset geometries.

```
/World (Root Prim)
└── /Venue (Default Prim - Stage Scope)
    ├── /Architecture (Payload Arc -> venue_architecture_payload.usda)
    │   ├── /Perimeter_Walls
    │   ├── /Vaulted_Ceiling
    │   └── /Flooring_Terrazzo
    ├── /Lighting (Stage Light Rig)
    │   ├── /Key_Light
    │   └── /Ambient_Fill
    └── /Layout (VariantSet: layoutVariant)
        ├── [standard_seating] -> /Rows_Auditorium (Lectern + 120 Audience Seats)
        └── [gala_banquet]     -> /Banquet_Tables (12 Round Tables + Centerpieces)
```

---

## ⚡ OpenUSD Composition Principles

1. **Root & Default Prim Configuration**:
   - `defaultPrim = "World"`
   - `metersPerUnit = 1.0` (SI unit compliance for physics and geospatial accuracy)
   - `upAxis = "Y"` (Standard DCC and Omniverse orientation)

2. **Payload Layer Architecture**:
   - Heavy architectural meshes (walls, vaulted arches, stone pillars) are deferred via a `payload` composition arc (`venue_architecture_payload.usda`).
   - Enables lightweight stage opening, selective payload loading, and sub-second stage initialization in collaborative Omniverse sessions.

3. **VariantSets (`layoutVariant`)**:
   - Implements non-destructive switching between event floorplans:
     - `standard_seating`: Auditorium configuration with central stage podium, lectern, and tiered seating rows.
     - `gala_banquet`: Gala banquet configuration with 12 distributed round dining tables, banquet seating, and ambient lighting overrides.

4. **LIVRPS Resolution Order Compliance**:
   - Layer composition adheres strictly to the OpenUSD **LIVRPS** order:
     - **L**ocal opinions
     - **I**nherits
     - **V**ariantSets
     - **R**eferences
     - **P**ayloads
     - **S**pecializes

---

## 🛠️ Usage & Stage Generation

Generate the reproducible OpenUSD stage files:

```bash
python generate_venue_stage.py
```

### Generated Artifacts
- `venue_stage.usda`: Master OpenUSD ASCII stage with root prim `/World/Venue`, default prim metadata, payload arcs, and `layoutVariant` variantSet.
- `venue_architecture_payload.usda`: Dedicated architectural payload containing structural geometry definitions (bounding bounds, walls, columns, vaulted ceiling).

### Inspecting in Omniverse / usdview

```bash
# Open in Pixar usdview
usdview venue_stage.usda

# Open in NVIDIA Omniverse USD Composer
# Navigate to File -> Open -> venue_stage.usda
```

---

## 🔗 Milestone & Certification Alignment
- **Milestone**: Days 1–30 (`LearnOpenUSD` & `kit-app-template`)
- **Target Certification**: [NVIDIA-Certified Associate: OpenUSD Foundations & Workflow (NCA-OFW)](../../certifications/NCA-OFW_study_tracker.md)
