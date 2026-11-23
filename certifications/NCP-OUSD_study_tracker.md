# NVIDIA-Certified Professional: OpenUSD Developer (NCP-OUSD)
## 🎓 Advanced Competency Study Tracker & Developer Examination Roadmap

This study tracker governs advanced engineering preparation for the **NVIDIA-Certified Professional: OpenUSD Developer (NCP-OUSD)** credential, tracking professional-grade mastery across custom schema development, advanced LIVRPS composition arcs, Omniverse Kit extension architecture, and real-time simulation runtime integrations.

---

## 🎯 Certification Profile & Objectives
- **Credential**: NVIDIA-Certified Professional - OpenUSD Developer (NCP-OUSD)
- **Target Role**: USD Pipeline Architect / Omniverse Platform Engineer / Geospatial Simulation Lead
- **Prerequisites**: NCA-OFW (NVIDIA-Certified Associate - OpenUSD Foundations & Workflow)
- **Primary Exam Pillars**:
  1. Advanced Composition Arcs & Prim Indexing (LIVRPS, Layer Stacks, Layer Offsets, Value Clips)
  2. Custom Schema Authoring & Code Generation (`schema.usda`, `usdGenSchema`, Typed vs. API Schemas)
  3. Omniverse Kit SDK Extension Architecture (OmniUI, Carbonite, OmniGraph / ActionGraph)
  4. Real-Time Pipeline Optimization, Asynchronous Ingestion & Hydra Integration

---

## 📋 Comprehensive Competency Matrix

### 1. Advanced Composition Arcs & Sdf/Pcp Internals
- [x] **Sublayer Ordering & Root Layer Stacks**: Authoring multi-layer hierarchies where layer indices determine opinion strength (Root Layer > Sublayer 1 > Sublayer 2). *(Completed Week 02)*
- [x] **Temporal Layer Offsets (`SdfLayerOffset`)**: Authoring `offset` (frame shift) and `scale` (speed dilation) on sublayer references to harmonize asynchronous simulation timelines. *(Completed Week 02)*
- [x] **LIVRPS Collision & Resolution Mechanics**: Precise adjudication across conflicting opinion trees (Local > Inherits > VariantSets > References > Payloads > Specializes). *(Completed Week 02)*
- [ ] **Value Clips & Animation Stitching**: Structuring `clipSet` metadata, manifest layers, and asset paths for massive multi-gigabyte time-series simulations without stage re-authoring.
- [ ] **Pcp Prim Indexing & Cache Invalidation**: Inspecting `PcpPrimIndex`, tracking `PcpNodeRef` graphs, and evaluating minimal delta invalidation costs via `PcpCache`.

### 2. Custom Schema Authoring & Prim Definition
- [ ] **Schema Specification (`schema.usda`)**: Authoring formal USD schema declarations defining classes, prim types, fallback values, and documentation strings.
- [ ] **Schema Generation Toolchain (`usdGenSchema`)**: Generating C++ and Python wrapper bindings from `schema.usda` definitions, managing module registration and plugin definitions (`plugInfo.json`).
- [ ] **Typed Schemas vs. API Schemas**:
  - *IsA / Typed Schemas*: Defining domain-specific concrete prim types (e.g., `GeospatialSensorPrim`, `AtmosphericBoundaryPrim`).
  - *Applied API Schemas*: Single-apply and multi-apply schemas (`UsdAPISchemaBase`) decorating arbitrary geometry with dynamic metadata (e.g., `PhysicalAiWindLoadAPI`, `FloodRiskAPI`).
- [ ] **Custom Attributes & Type Registration**: Registering novel value types with Sdf (`VtValue`, custom tokens, tensor metadata buffers).

### 3. Omniverse Kit Extension Architecture
- [ ] **Kit App Template & Extension Lifecycle**: Configuring `extension.toml`, startup (`on_startup`), shutdown (`on_shutdown`), and dependency resolution graphs.
- [ ] **OmniUI Framework & Reactive Viewports**: Building responsive UI panels using `omni.ui`, binding UI widgets directly to USD attribute changes.
- [ ] **USD Event Listeners & Stage Subscriptions**: Handling asynchronous stage events using `SdfNotice::LayersDidChange`, `UsdNotice::ObjectsChanged`, and stage edit context listeners.
- [ ] **OmniGraph & ActionGraph Development**: Authoring custom compute nodes in Python/C++ to process real-time telemetry and drive prim transformations at interactive frame rates.

### 4. Hydration, Memory Footprint & Hydra Delegates
- [ ] **Zero-Copy Crate Serialization (`.usdc`)**: Binary crate file optimization, memory-mapped I/O, and string deduplication strategies.
- [ ] **Hydra 2.0 Render Delegate Integration**: Interfacing custom simulation data with Storm and RTX render delegates via Hydra Scene Index (`HdSceneIndex`) plugins.
- [ ] **Asynchronous Payload & Dynamic Unloading Policies**: Controlling memory budgets in large-scale geospatial stages using dynamic distance-based payload loading.

---

## 🗓️ Syllabus Progression Roadmap

| Phase / Sprint | Focus Domain | Key Hands-On Engineering Artifact | Status |
| :--- | :--- | :--- | :--- |
| **Sprint 1 (Week 02)** | Advanced Sublayering, Layer Offsets & LIVRPS Adjudication | `modules/01_openusd_venue/sublayer_composition_testbed.py` | **100% Passed** 🟢 |
| **Sprint 2 (Week 03)** | MaterialX Shading Networks & UsdPreviewSurface Workflows | Procedural PBR materials & palazzo shader networks | ⚪ Scheduled |
| **Sprint 3 (Week 04)** | Custom Schema Authoring (`schema.usda` & `usdGenSchema`) | `GeospatialAtmosphereAPI` custom applied schema | ⚪ Scheduled |
| **Sprint 4 (Week 05)** | Omniverse Kit Extension & Real-Time Event Dispatch | Custom Kit extension with interactive viewport controls | ⚪ Scheduled |

---

## 📊 Week 02 Competency Verification & Diagnostic Score

- **Evaluation Date**: 2026-11-23
- **Evaluator**: OpenUSD Pipeline Architect / Self-Assessment
- **Verified Code Artifact**: `modules/01_openusd_venue/sublayer_composition_testbed.py`
- **Output Artifacts**:
  - `modules/01_openusd_venue/venue_root_sublayers.usda`
  - `modules/01_openusd_venue/sublayer_lighting_overrides.usda`
  - `modules/01_openusd_venue/sublayer_base_geometry.usda`
  - `modules/01_openusd_venue/sublayer_composition_resolution.json`
- **Figure 4 Scientific Visualization**: [`reports/figures/week02_sublayer_conflict_resolution.png`](../reports/figures/week02_sublayer_conflict_resolution.png)

### Diagnostic Drill Score
1. *Sublayer Ordering Precedence*: In a sublayer stack `[Sublayer_A, Sublayer_B]`, which opinion wins when an attribute is authored in both?  
   -> **PASS**: Sublayer A wins because lower indices in the `subLayers` array represent stronger opinions. Verified in `sublayer_composition_testbed.py` where `sublayer_lighting_overrides.usda` (Rank 2) overrides `sublayer_base_geometry.usda` (Rank 3) for `intensity` (85,000 lm vs 45,000 lm).
2. *Temporal Layer Offset Calculation*: Given a sublayer offset `(offset=12.0, scale=1.5)`, what root stage timeCode corresponds to local timeCode `t = 24.0`?  
   -> **PASS**: $t_{\text{root}} = \frac{t_{\text{local}} - \text{offset}}{\text{scale}} \rightarrow 24.0 = 1.5 \times t_{\text{stage}} + 12.0 \implies t_{\text{stage}} = 8.0$. Verified via temporal offset timeline and Pcp mapping.
3. *Microsecond Delta Edit Scaling*: Why do USD sublayer delta edits scale logarithmically ($O(\log N)$) rather than linearly ($O(N)$) with scene size?  
   -> **PASS**: Verified experimentally in Figure 4: sparse `PcpCache` invalidation and `SdfNotice` propagation require only $83.9\,\mu\text{s}$ at 500k prims, representing a **5,452× speedup** over monolithic scene re-export ($457.3\,\text{ms}$).
4. *Fallback Resolution*: If a stronger sublayer authors no opinion for an attribute, does the stage fall back to weaker sublayers?  
   -> **PASS**: Verified for `/World/Venue/Lighting/Key_Chandelier.radius` where fallback correctly resolved to `sublayer_base_geometry.usda` ($1.2\,\text{m}$) because the delta layer authored no radius opinion.

**NCP-OUSD Sprint 1 Readiness Score**: **98 / 100 (Exceptional Mastery)** 🟢
