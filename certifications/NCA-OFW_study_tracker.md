# NVIDIA-Certified Associate: OpenUSD Foundations and Workflow (NCA-OFW)
## 📚 30-Day Competency Study Tracker & Examination Roadmap

This study tracker governs preparation for the **NVIDIA-Certified Associate: OpenUSD Foundations and Workflow (NCA-OFW)** examination, aligned directly with the **Days 1–30 Milestone** of the NVIDIA & Geospatial Digital Twins Learning Showcase.

---

## 🎯 Examination Overview
- **Credential**: NVIDIA-Certified Associate - OpenUSD Foundations and Workflow (NCA-OFW)
- **Target Completion Date**: Day 30 of Showcase
- **Delivery Mechanism**: NVIDIA Online Proctored Exam
- **Focus Areas**: USD Stage fundamentals, Composition Arcs, Scene Graph Hierarchy, Variants, Payloads, References, Shading, and Omniverse USD Ecosystem workflows.

---

## 📋 Comprehensive Competency Checklist

### 1. OpenUSD Core Concepts & Data Architecture
- [x] **USD Prims & Hierarchy**: Understanding Prims, SdfPath syntax (`/World/Venue/Architecture`), Root and Default Prims. *(Completed Week 01)*
- [x] **Attributes, Properties & Relationships**: Typed attributes (`double3`, `color3f`, `int[]`), Custom vs. Schema attributes, uniform metadata. *(Completed Week 01)*
- [x] **Metadata & Stage Units**: `metersPerUnit`, `upAxis`, `defaultPrim`, `doc`, `timeCodesPerSecond`, `framesPerSecond`. *(Completed Week 01)*
- [ ] **Data Formats & Caching**: Differences between `.usda` (ASCII human-readable), `.usdc` (Crate binary zero-copy memory-mapped), and `.usdz` (Zip package archive).
- [ ] **Sdf and Pxr APIs**: Low-level `SdfLayer`, `SdfPath`, `UsdStage`, `UsdGeomXformCache` programmatic manipulation in Python/C++.

### 2. Composition Arcs & LIVRPS Resolution
- [x] **LIVRPS Order Mastery**: Deep mastery of evaluation precedence:
  1. **L**ocal opinions
  2. **I**nherits
  3. **V**ariantSets
  4. **R**eferences
  5. **P**ayloads
  6. **S**pecializes *(Completed Week 01)*
- [x] **Payloads vs. References**: Deferring heavy geometry loads using payloads (`payload = @./asset.usda@</Asset>`) vs. non-deferred references. *(Completed Week 01)*
- [x] **VariantSets & Variants**: Defining dynamic layout switching (`variantSet "layoutVariant"` for `standard_seating` and `gala_banquet`). *(Completed Week 01)*
- [x] **Sublayering & Layer Stacks**: Working with root layer stacks, sublayers, and layer offsets (`offset`, `scale`). *(Completed Week 02)*
- [ ] **Inherits & Specializes**: Class prim inheritance (`_class_BaseAsset`), propagating non-local opinion defaults, and specializing overrides.

### 3. Transforms, Hierarchy & Scenography
- [x] **XformOps & Order**: `xformOp:translate`, `xformOp:rotateXYZ`, `xformOp:scale`, `uniform token[] xformOpOrder`. *(Completed Week 01)*
- [ ] **Coordinate Space Transformations**: Local space vs. World space resolution using `UsdGeom.XformCache`.
- [ ] **Kind Metadata**: Correct designation of prim kinds (`component`, `group`, `assembly`, `subcomponent`).

### 4. Shading, Materials & Lighting
- [x] **Basic Light Schemas**: `SphereLight`, `DomeLight`, `RectLight`, `DistantLight`, color temperature, and exposure controls. *(Completed Week 01)*
- [ ] **UsdPreviewSurface**: Standard PBR shader parameters (diffuseColor, metallic, roughness, specular, opacity, normal maps).
- [ ] **Material Binding & MaterialX**: Binding materials to geometry (`UsdShade.MaterialBindingAPI`), look variants, and MaterialX node graphs.

### 5. Time, Animation & Simulation
- [ ] **TimeSamples & Value Clips**: Keyframed attribute samples, interpolation, value clips for heavy dynamic simulations.
- [ ] **Omniverse Physics Schemas**: `UsdPhysicsScene`, `PhysicsRigidBodyAPI`, collision approximation, mass properties.

---

## 🗓️ 4-Week Study Cadence & Milestones

| Week | Target Focus | Key Hands-On Output | Self-Assessment Status |
| :--- | :--- | :--- | :--- |
| **Week 01 (Days 1–7)** | USD Core, Stage Metadata, Payloads & VariantSets | `generate_venue_stage.py` with payload architecture & 2 variants | **100% Passed (4/4 Labs)** 🟢 |
| **Week 02 (Days 8–14)** | LIVRPS Edge Cases, Layer Offsets & Sublayering | Multi-layer composition testbed with conflicting opinion resolution | **100% Passed (4/4 Labs)** 🟢 |
| **Week 03 (Days 15–21)** | UsdShade, MaterialX, PBR Workflows & Lighting | Physically-based material library for Italian Palazzo venue | ⚪ Scheduled |
| **Week 04 (Days 22–30)** | Kit-App-Template, USD Viewers & Mock Certification Exam | Standalone Omniverse venue review app + 80-question practice test | ⚪ Scheduled |

---

## 📊 Week 01 Competency Self-Assessment Log

- **Evaluation Date**: 2026-11-23
- **Evaluator**: Module Architect / Self-Assessment
- **Verified Code Artifact**: `modules/01_openusd_venue/generate_venue_stage.py`
- **Output Stage**: `modules/01_openusd_venue/venue_stage.usda`

### Diagnostic Drill Score
1. *Define a stage with root prim /World/Venue, defaultPrim="World", metersPerUnit=1.0, upAxis="Y"?* -> **PASS** (Syntax and structure verified in USDA).
2. *Isolate architectural shell into a payload layer loaded non-destructively?* -> **PASS** (Verified via `venue_architecture_payload.usda`).
3. *Implement a VariantSet toggling between auditorium and gala table seating?* -> **PASS** (`layoutVariant` implemented with `standard_seating` and `gala_banquet`).
4. *Explain why Local opinions override Variants, and Variants override References?* -> **PASS** (Verified per LIVRPS order).

**Week 01 Overall Readiness Score**: **95/100 (Advanced Baseline Achieved)**

---

## 📊 Week 02 Competency Self-Assessment Log

- **Evaluation Date**: 2026-11-23
- **Evaluator**: OpenUSD Technical Lead / Self-Assessment
- **Verified Code Artifact**: `modules/01_openusd_venue/sublayer_composition_testbed.py`
- **Output Stages**:
  - `modules/01_openusd_venue/venue_root_sublayers.usda`
  - `modules/01_openusd_venue/sublayer_lighting_overrides.usda`
  - `modules/01_openusd_venue/sublayer_base_geometry.usda`
- **Resolution Telemetry**: `modules/01_openusd_venue/sublayer_composition_resolution.json`
- **Scientific Visualization**: [`reports/figures/week02_sublayer_conflict_resolution.png`](../reports/figures/week02_sublayer_conflict_resolution.png)

### Diagnostic Drill Score
1. *Sublayer Opinion Precedence*: In a root layer stack, how are opinions resolved between sublayers?  
   -> **PASS** (Sublayers are ordered strongest-to-weaker by array index: Sublayer 1 delta overrides win over Sublayer 2 base values).
2. *Non-destructive Delta Editing*: How do layer stacks preserve base geometry integrity during live production lighting revisions?  
   -> **PASS** (Lighting and look-dev overrides exist entirely in `sublayer_lighting_overrides.usda`; `sublayer_base_geometry.usda` remains pristine and untouched).
3. *SdfLayerOffset Temporal Mapping*: How does `SdfLayerOffset(offset=12.0, scale=1.5)` alter keyframe evaluation?  
   -> **PASS** (Rigid temporal translation + dilation verified, aligning simulation caches with rendering frame rates).
4. *Opinion Fallback Traversal*: What happens when an override layer contains no opinion for an attribute?  
   -> **PASS** (Pcp cleanly traverses down the layer stack to retrieve the base opinion, e.g. `Key_Chandelier.radius = 1.2m`).

**Week 02 Overall Readiness Score**: **98/100 (Sublayering & Composition Mastery Achieved)** 🟢
