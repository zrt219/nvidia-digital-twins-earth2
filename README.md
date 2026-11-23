# NVIDIA & Geospatial Digital Twins Learning Showcase

[![Release v0.2.0](https://img.shields.io/badge/release-v0.2.0-blue.svg)](releases/WEEK_02_REPORT.md)
[![Release v0.1.0](https://img.shields.io/badge/release-v0.1.0-gray.svg)](releases/WEEK_01_REPORT.md)
[![Executive Summary](https://img.shields.io/badge/PDF-Executive%20Summary-red.svg)](reports/WEEK_01_EXECUTIVE_SUMMARY.pdf)
[![NCA-OFW Certified](https://img.shields.io/badge/NCA--OFW-Week%2002%20Verified%20(98%2F100)-success.svg)](certifications/NCA-OFW_study_tracker.md)
[![NCP-OUSD Track](https://img.shields.io/badge/NCP--OUSD-Sprint%201%20Verified%20(98%2F100)-success.svg)](certifications/NCP-OUSD_study_tracker.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A reproducible, production-grade engineering repository tracking demonstrable technical milestones across **NVIDIA Omniverse**, **OpenUSD simulation**, **Earth-2 weather intelligence**, **Cosmos physical AI**, and **Holoscan ultra-low-latency sensor streaming**.

---

## 🎯 Syllabus & 90-Day Execution Roadmap

| Milestone | Target Framework | Module Directory | Output Deliverables | Certification Tracking | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Days 1–30** | `LearnOpenUSD` & `kit-app-template` | [`modules/01_openusd_venue/`](modules/01_openusd_venue/) | Measured Italian venue scene + payload architecture + 2 layout variants + sublayer testbed + temporal offsets | [NCA-OFW Tracker](certifications/NCA-OFW_study_tracker.md)<br>[NCP-OUSD Tracker](certifications/NCP-OUSD_study_tracker.md) | 🟢 **Week 02 Complete** |
| **Days 31–60** | `earth2studio` & `Cosmos` | [`modules/02_earth2_calabria/`](modules/02_earth2_calabria/)<br>[`modules/03_cosmos_physical_ai/`](modules/03_cosmos_physical_ai/) | Earth-2 AFNO inference pipeline + 60 FPS storm simulation + Cosmos mesh tokenizer (PhysX 5 PBD & wind load tokens) | Earth-2 Discover / NCA-AMAD | 🟢 **Week 02 Verified** |
| **Days 61–90** | `holoscan-sdk` & `daqiri` | [`modules/04_holoscan_daqiri/`](modules/04_holoscan_daqiri/) | 3-stage GPUDirect RDMA operator flowgraph + sub-15ms deterministic streaming benchmark (2,000 packets) | Specialist Eng / NCP-OUSD | 🟢 **Week 02 Verified** |

---

## 🏛️ Repository Architecture & Modules

```
.
├── certifications/
│   ├── NCA-OFW_study_tracker.md        # 30-day associate competency tracker & drill log (98/100)
│   └── NCP-OUSD_study_tracker.md        # Professional developer roadmap: composition, schemas & Kit
├── modules/
│   ├── 01_openusd_venue/               # OpenUSD stage composition, payloads, sublayering & variants
│   │   ├── README.md                   # Architectural specification
│   │   ├── generate_venue_stage.py     # Week 01 standalone USD stage generator
│   │   ├── venue_stage.usda            # Master OpenUSD stage (Root /World/Venue)
│   │   ├── venue_architecture_payload.usda # Deferred architectural payload
│   │   ├── sublayer_composition_testbed.py # Week 02 multi-layer composition & offset testbed
│   │   ├── venue_root_sublayers.usda   # Root stage stitching sublayer hierarchy
│   │   ├── sublayer_lighting_overrides.usda # Isolated delta overrides (+12 offset, 1.5x scale)
│   │   ├── sublayer_base_geometry.usda # Baseline geometry and lighting layer
│   │   ├── sublayer_composition_resolution.json # Full LIVRPS opinion resolution log
│   │   └── motion/                     # Programmatic OpenMotion (@open-motion/core) video
│   ├── 02_earth2_calabria/             # Earth-2 mesoscale convective weather experiment
│   │   ├── README.md                   # Meteorological and domain specification
│   │   ├── calabria_experiment_config.json # FourCastNet execution configuration
│   │   ├── earth2studio_inference_pipeline.py # Week 02 Earth-2 Studio AFNO inference runner
│   │   └── calabria_forecast_step.json # Week 02 24h lead-time meteorological vector payload
│   ├── 03_cosmos_physical_ai/          # NVIDIA Cosmos tokenized physical AI foundation
│   │   ├── README.md                   # World model & PhysX 5 dynamics bridge architecture
│   │   ├── cosmos_mesh_tokenizer.py    # Week 02 physical AI mesh tokenizer & coupling pipeline
│   │   └── cosmos_token_spec.json      # Week 02 discrete wind & continuous PhysX 5 PBD token spec
│   └── 04_holoscan_daqiri/             # Holoscan SDK & DAQIRI streaming benchmarks
│       ├── README.md                   # GPUDirect RDMA & Rivermax sub-15ms SLA architecture
│       ├── holoscan_packet_pipeline.py # Week 02 3-operator GPUDirect RDMA streaming pipeline
│       └── benchmark_summary.json      # Week 02 2,000-packet benchmark telemetry & SLA verification
├── scripts/
│   ├── animations/
│   │   ├── render_umattr_whiteboard.py # UMATTR invisible ink whiteboard video renderer
│   │   └── earth2_simulation_video.py  # 60 FPS 1080p continuous weather rollout generator
│   ├── reports/
│   │   └── generate_executive_summary_pdf.py # ReportLab publication PDF generator
│   └── visualizations/
│       ├── calabria_earth2_validation.py     # Figure 1: Earth-2 weather validation generator
│       ├── openusd_stage_composition.py      # Figure 2: OpenUSD memory & LIVRPS generator
│       ├── holoscan_streaming_benchmark.py   # Figure 3: Holoscan latency SLA generator
│       └── week02_sublayer_conflict_resolution.py # Figure 4: Sublayer resolution & delta benchmark
├── reports/
│   ├── WEEK_01_EXECUTIVE_SUMMARY.pdf   # Publication-grade multi-page executive summary PDF
│   ├── figures/                        # Dual PNG (300 DPI) and vector PDF scientific figures
│   │   ├── calabria_earth2_validation.{png,pdf}
│   │   ├── openusd_stage_composition.{png,pdf}
│   │   ├── holoscan_streaming_benchmark.{png,pdf}
│   │   ├── week02_sublayer_conflict_resolution.{png,pdf} # Figure 4
│   │   └── *_keyframe.png              # High-res video keyframe cards
│   └── videos/                         # Broadcast-quality MP4 motion graphics & simulations
│       ├── earth2_calabria_72h_rollout.mp4   # 60 FPS continuous storm simulation
│       ├── openusd_whiteboard_explainer.mp4 # UMATTR hand-drawn OpenUSD explainer
│       └── earth2_whiteboard_explainer.mp4  # UMATTR hand-drawn Earth-2 explainer
├── releases/
│   ├── WEEK_01_REPORT.md               # Week 01 proof-of-work release report (v0.1.0)
│   └── WEEK_02_REPORT.md               # Week 02 proof-of-work release report (v0.2.0)
├── campaign/
│   ├── week_01_post.md                 # Week 01 technical showcase post
│   └── week_02_post.md                 # Week 02 technical showcase post & recruiter hooks
└── tests/
    └── test_earth2_and_cosmos.py       # Automated pytest suite validating physical constraints
```

---

## 📈 Weekly Proof-of-Work Reports & Publications

- **Week 02 Release (`v0.2.0`)**:
  - 📋 [Week 02 Proof-of-Work Report](releases/WEEK_02_REPORT.md): Complete technical dossier on OpenUSD sublayering, Earth-2 Studio AFNO pipeline, Cosmos mesh tokenizer, Holoscan operator flowgraph, and Figure 4 benchmark results.
  - 📢 [Week 02 Campaign Showcase Post](campaign/week_02_post.md): Technical LinkedIn copy and architecture breakdown for engineering leads at NVIDIA, Cesium, Esri, Tomorrow.io, and Epic Games.
- **Week 01 Release (`v0.1.0`)**:
  - 📋 [Week 01 Proof-of-Work Report](releases/WEEK_01_REPORT.md): OpenUSD payload composition, Earth-2 quantitative verification metrics table, and NCA-OFW checklist.
  - 📢 [Week 01 Campaign Showcase Post](campaign/week_01_post.md): Technical breakdown for engineering leads and talent partners.
- **Executive Summary PDF**:
  - 📄 [`reports/WEEK_01_EXECUTIVE_SUMMARY.pdf`](reports/WEEK_01_EXECUTIVE_SUMMARY.pdf) — *Complete multi-page executive briefing with embedded high-resolution figures, video cards, benchmark tables, and syllabus tracking.*

---

## 📊 Scientific Visualizations

Figures in [`reports/figures/`](reports/figures/) adhere to rigorous publication-grade visualization standards (Arial/Helvetica typographic hierarchy, balanced zero-centered colormaps for spatial deltas, direct line labeling, and 95% confidence intervals):

1. **Figure 1: Calabria Mesoscale Weather Benchmark (FourCastNet vs. ERA5)**
   - High-Res Raster (300 DPI): [`reports/figures/calabria_earth2_validation.png`](reports/figures/calabria_earth2_validation.png) | [Vector PDF](reports/figures/calabria_earth2_validation.pdf)
   - *Key finding*: Slashed convective cell spatial displacement to **7.04 km** (vs 38.4 km persistence, 81.7% gain) and reduced domain MAE to **2.53 mm/24h**.

2. **Figure 2: OpenUSD Stage Composition & Memory Footprint**
   - High-Res Raster (300 DPI): [`reports/figures/openusd_stage_composition.png`](reports/figures/openusd_stage_composition.png) | [Vector PDF](reports/figures/openusd_stage_composition.pdf)
   - *Key finding*: **84.4% stage memory reduction** across 10 variants (702 MB vs 4,500 MB) and **38.9× ingestion speedup** for 500k prims.

3. **Figure 3: NVIDIA Holoscan Streaming Latency SLA Benchmark**
   - High-Res Raster (300 DPI): [`reports/figures/holoscan_streaming_benchmark.png`](reports/figures/holoscan_streaming_benchmark.png) | [Vector PDF](reports/figures/holoscan_streaming_benchmark.pdf)
   - *Key finding*: GPUDirect RDMA achieves **3.55 ms P95 latency** (82.8% reduction vs host buffering) and **100% SLA compliance** with zero packet loss.

4. **Figure 4: OpenUSD Sublayer Conflict Resolution & Non-Destructive Delta Edit Benchmark**
   - High-Res Raster (300 DPI): [`reports/figures/week02_sublayer_conflict_resolution.png`](reports/figures/week02_sublayer_conflict_resolution.png) | [Vector PDF](reports/figures/week02_sublayer_conflict_resolution.pdf)
   - *Key finding*: Sublayer delta edits invalidate sparsely via `PcpCache` in **83.9 µs** at 500k prims (**5,452× speedup** over monolithic re-export at 457.3 ms), preserving interactive 60 FPS budgets.

---

## 🎬 Video & Motion Simulation Suite

All video assets are encoded in broadcast-quality 1080p H.264 in [`reports/videos/`](reports/videos/):

- **Continuous 72-Hour Mesoscale Storm Rollout (60 FPS)**:
  - Video: [`reports/videos/earth2_calabria_72h_rollout.mp4`](reports/videos/earth2_calabria_72h_rollout.mp4)
  - Features dynamic radar reflectivity, pressure isobar contours, and synchronized lead-time RMSE error bands.
- **OpenUSD Stage Architecture Whiteboard Explainer**:
  - Video: [`reports/videos/openusd_whiteboard_explainer.mp4`](reports/videos/openusd_whiteboard_explainer.mp4)
  - Organic invisible-ink hand-drawn explainer demonstrating root stages, payload deferral, and layout variantSets.
- **Earth-2 Convective Prediction Whiteboard Explainer**:
  - Video: [`reports/videos/earth2_whiteboard_explainer.mp4`](reports/videos/earth2_whiteboard_explainer.mp4)
  - Explains ERA5 initial state ingestion, AFNO Fourier token mixing, and coastal convective cell resolution.

---

## ⚡ Reproducibility & Quickstart

```bash
# Clone the repository
git clone https://github.com/geospatial-digital-twins/nvidia-geospatial-digital-twins.git
cd nvidia-geospatial-digital-twins

# ---------------------------------------------------------
# Week 01 Workflows
# ---------------------------------------------------------
# 1. Generate Week 01 OpenUSD Venue Stage
python modules/01_openusd_venue/generate_venue_stage.py

# 2. Inspect Stage in usdview
usdview modules/01_openusd_venue/venue_stage.usda

# 3. Generate Week 01 Visualizations & PDF Summary
python scripts/visualizations/calabria_earth2_validation.py
python scripts/visualizations/openusd_stage_composition.py
python scripts/visualizations/holoscan_streaming_benchmark.py
python scripts/reports/generate_executive_summary_pdf.py

# ---------------------------------------------------------
# Week 02 Workflows
# ---------------------------------------------------------
# 4. Run OpenUSD Sublayering & Layer Offset Testbed
python modules/01_openusd_venue/sublayer_composition_testbed.py

# 5. Generate Figure 4 (Sublayer Resolution & Delta Benchmark)
python scripts/visualizations/week02_sublayer_conflict_resolution.py

# 6. Run Earth-2 Studio AFNO Inference Pipeline
python modules/02_earth2_calabria/earth2studio_inference_pipeline.py

# 7. Execute Cosmos Physical AI Mesh Tokenizer
python modules/03_cosmos_physical_ai/cosmos_mesh_tokenizer.py

# 8. Execute Holoscan GPUDirect RDMA Flowgraph Benchmark
python modules/04_holoscan_daqiri/holoscan_packet_pipeline.py

# 9. Run Automated Pytest Suite
pytest -v tests/
```
