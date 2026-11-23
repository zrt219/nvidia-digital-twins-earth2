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

### Generated Artifacts (Week 01)
- `venue_stage.usda`: Master OpenUSD ASCII stage with root prim `/World/Venue`, default prim metadata, payload arcs, and `layoutVariant` variantSet.
- `venue_architecture_payload.usda`: Dedicated architectural payload containing structural geometry definitions (bounding bounds, walls, columns, vaulted ceiling).

---

## 🔬 Week 02 Sublayer Composition & Opinion Resolution Testbed

Week 02 demonstrates advanced multi-layer composition, department-level non-destructive workflows, and temporal animation offsets:

```bash
# Run programmatic sublayer generator & LIVRPS verifier
python sublayer_composition_testbed.py

# Generate publication Figure 4 (PDF & PNG)
python ../../scripts/visualizations/week02_sublayer_conflict_resolution.py
```

### Sublayer Architecture & LIVRPS Precedence Order
1. **Root Layer (`venue_root_sublayers.usda`)**:
   - Holds stage metadata, time ranges (`0.0` to `100.0`), and assembles the sublayer stack.
   - Authors root-level opinions (`/World/Venue/Lighting/Ambient_Sky.exposure = 2.5 EV`), demonstrating that root stage opinions have **Rank 1 (Highest Precedence)** over all sublayers.
2. **Sublayer 1 — Delta Overrides (`sublayer_lighting_overrides.usda`)**:
   - Declared as `subLayers[0]` with `SdfLayerOffset(offset = 12.0, scale = 1.5)`.
   - Uses non-destructive `over` prims to override lighting intensity (`85,000 lm`), cool cyan color palette `(0.35, 0.75, 1.0)`, and introduces department-level prims (`Stage_Fill`).
   - Demonstrates **Rank 2 (Stronger Sublayer)** precedence over base geometry.
   - Demonstrates **Time Dilation**: Animation keyframes are shifted by +12 frames and scaled by 1.5x ($t_{\text{root}} = t_{\text{sub}} \times 1.5 + 12.0$).
3. **Sublayer 2 — Base Geometry (`sublayer_base_geometry.usda`)**:
   - Declared as `subLayers[1]`.
   - Defines structural perimeter walls, colonnades, terrazzo floor, and baseline warm lighting (`45,000 lm`).
   - Serves as **Rank 3 (Weaker / Fallback Layer)**.

### Performance Benchmark Highlights
- **Sparse Delta Recomposition**: Evaluating delta edits via `PcpCache` sparse invalidation requires only **14.0 μs to 83.9 μs** (0.084 ms) across 1k to 500k prim scenes.
- **Speedup vs. Monolithic Re-export**: Up to **5,452× faster** than reloading a monolithic scene (457.6 ms at 500k prims), ensuring zero frame drops well within 60 FPS interactive budgets (16.67 ms).
- **Figure 4 Output**: `reports/figures/week02_sublayer_conflict_resolution.pdf` and `.png`.

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
