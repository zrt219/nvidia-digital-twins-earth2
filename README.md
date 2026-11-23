# NVIDIA & Geospatial Digital Twins Learning Showcase

[![Release](https://img.shields.io/badge/release-v0.1.0-blue.svg)](releases/WEEK_01_REPORT.md)
[![Executive Summary](https://img.shields.io/badge/PDF-Executive%20Summary-red.svg)](reports/WEEK_01_EXECUTIVE_SUMMARY.pdf)
[![Certification](https://img.shields.io/badge/NCA--OFW-Week%2001%20Verified%20(95%2F100)-success.svg)](certifications/NCA-OFW_study_tracker.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A reproducible, production-grade engineering repository tracking demonstrable technical milestones across **NVIDIA Omniverse**, **OpenUSD simulation**, **Earth-2 weather intelligence**, **Cosmos physical AI**, and **Holoscan ultra-low-latency sensor streaming**.

---

## 🎯 Syllabus & 90-Day Execution Roadmap

| Milestone | Target Framework | Module Directory | Output Deliverable | Certification Tracking | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Days 1–30** | `LearnOpenUSD` & `kit-app-template` | [`modules/01_openusd_venue/`](modules/01_openusd_venue/) | Italian venue measured scene + payload architecture + 2 layout variants + OpenMotion video | [NCA-OFW Tracker](certifications/NCA-OFW_study_tracker.md) | 🟢 **Week 01 Complete** |
| **Days 31–60** | `earth2studio` & `Cosmos` | [`modules/02_earth2_calabria/`](modules/02_earth2_calabria/)<br>[`modules/03_cosmos_physical_ai/`](modules/03_cosmos_physical_ai/) | Calabria convective weather benchmark + 60 FPS simulation video + Cosmos world model suite | Earth-2 Discover / NCA-AMAD | 🟢 **Benchmark Verified** |
| **Days 61–90** | `holoscan-sdk` & `daqiri` | [`modules/04_holoscan_daqiri/`](modules/04_holoscan_daqiri/) | ConnectX GPUDirect RDMA pipeline + sub-15ms streaming latency benchmark | Specialist Eng / NCP-OUSD | 🟢 **Benchmark Verified** |

---

## 🏛️ Repository Architecture & Modules

```
.
├── certifications/
│   └── NCA-OFW_study_tracker.md        # 30-day preparation tracker & competency drill log
├── modules/
│   ├── 01_openusd_venue/               # OpenUSD stage composition, payloads, and variantSets
│   │   ├── README.md                   # Architectural specification
│   │   ├── generate_venue_stage.py     # Standalone reproducible USD stage generator
│   │   ├── venue_stage.usda            # Master OpenUSD stage (Root /World/Venue)
│   │   ├── venue_architecture_payload.usda # Deferred architectural payload
│   │   └── motion/                     # Programmatic OpenMotion (@open-motion/core) video
│   │       ├── README.md               # Video rendering instructions
│   │       ├── package.json            # React & OpenMotion dependencies
│   │       └── src/VenueShowcaseVideo.tsx # 60 FPS animated USD hierarchy & variant morphing
│   ├── 02_earth2_calabria/             # Earth-2 mesoscale convective weather experiment
│   │   ├── README.md                   # Meteorological and domain specification
│   │   └── calabria_experiment_config.json # FourCastNet execution configuration
│   ├── 03_cosmos_physical_ai/          # NVIDIA Cosmos tokenized physical AI foundation
│   │   └── README.md                   # World model & PhysX 5 dynamics bridge architecture
│   └── 04_holoscan_daqiri/             # Holoscan SDK & DAQIRI streaming benchmarks
│       └── README.md                   # GPUDirect RDMA & Rivermax sub-15ms SLA architecture
├── scripts/
│   ├── animations/
│   │   ├── render_umattr_whiteboard.py # UMATTR invisible ink whiteboard video renderer
│   │   └── earth2_simulation_video.py  # 60 FPS 1080p continuous weather rollout generator
│   ├── reports/
│   │   └── generate_executive_summary_pdf.py # ReportLab publication PDF generator
│   └── visualizations/
│       ├── calabria_earth2_validation.py     # Figure 1: Earth-2 weather validation generator
│       ├── openusd_stage_composition.py      # Figure 2: OpenUSD memory & LIVRPS generator
│       └── holoscan_streaming_benchmark.py   # Figure 3: Holoscan latency SLA generator
├── reports/
│   ├── WEEK_01_EXECUTIVE_SUMMARY.pdf   # Publication-grade multi-page executive summary PDF
│   ├── figures/                        # Dual PNG (300 DPI) and vector PDF scientific figures
│   │   ├── calabria_earth2_validation.{png,pdf}
│   │   ├── openusd_stage_composition.{png,pdf}
│   │   ├── holoscan_streaming_benchmark.{png,pdf}
│   │   └── *_keyframe.png              # High-res video keyframe cards
│   └── videos/                         # Broadcast-quality MP4 motion graphics & simulations
│       ├── earth2_calabria_72h_rollout.mp4   # 60 FPS continuous storm simulation
│       ├── openusd_whiteboard_explainer.mp4 # UMATTR hand-drawn OpenUSD explainer
│       └── earth2_whiteboard_explainer.mp4  # UMATTR hand-drawn Earth-2 explainer
├── releases/
│   └── WEEK_01_REPORT.md               # Weekly proof-of-work report (v0.1.0)
└── campaign/
    └── week_01_post.md                 # Technical LinkedIn showcase post & recruiter hook
```

---

## 📈 Weekly Proof-of-Work Reports & Publications

- **Executive Summary PDF**:
  - 📄 [`reports/WEEK_01_EXECUTIVE_SUMMARY.pdf`](reports/WEEK_01_EXECUTIVE_SUMMARY.pdf) — *Complete multi-page executive briefing with embedded high-resolution figures, video cards, benchmark tables, and syllabus tracking.*
- **Week 01 Release**:
  - 📋 [Week 01 Proof-of-Work Report](releases/WEEK_01_REPORT.md) (`v0.1.0`): Detailed breakdown of OpenUSD payload composition, Earth-2 quantitative verification metrics table, and NCA-OFW checklist.
  - 📢 [Week 01 Campaign Showcase Post](campaign/week_01_post.md): Technical breakdown for engineering leads and talent partners at NVIDIA, Cesium, Esri, Tomorrow.io, and Planet Labs.

---

## 📊 Scientific Visualizations

Figures in [`reports/figures/`](reports/figures/) adhere to rigorous publication-grade visualization standards (sans-serif typographic hierarchy, balanced zero-centered colormaps for spatial deltas, direct line labeling, and 95% confidence intervals):

1. **Figure 1: Calabria Mesoscale Weather Benchmark (FourCastNet vs. ERA5)**
   - High-Res Raster (300 DPI): [`reports/figures/calabria_earth2_validation.png`](reports/figures/calabria_earth2_validation.png)
   - Vector Graphic (PDF): [`reports/figures/calabria_earth2_validation.pdf`](reports/figures/calabria_earth2_validation.pdf)
   - *Key finding*: Slashed convective cell spatial displacement to **7.04 km** (vs 38.4 km persistence, 81.7% gain) and reduced domain MAE to **2.53 mm/24h**.

2. **Figure 2: OpenUSD Stage Composition & Memory Footprint**
   - High-Res Raster (300 DPI): [`reports/figures/openusd_stage_composition.png`](reports/figures/openusd_stage_composition.png)
   - Vector Graphic (PDF): [`reports/figures/openusd_stage_composition.pdf`](reports/figures/openusd_stage_composition.pdf)
   - *Key finding*: **84.4% stage memory reduction** across 10 variants (702 MB vs 4,500 MB) and **38.9× ingestion speedup** for 500k prims.

3. **Figure 3: NVIDIA Holoscan Streaming Latency SLA Benchmark**
   - High-Res Raster (300 DPI): [`reports/figures/holoscan_streaming_benchmark.png`](reports/figures/holoscan_streaming_benchmark.png)
   - Vector Graphic (PDF): [`reports/figures/holoscan_streaming_benchmark.pdf`](reports/figures/holoscan_streaming_benchmark.pdf)
   - *Key finding*: GPUDirect RDMA achieves **3.55 ms P95 latency** (82.8% reduction vs host buffering) and **100% SLA compliance** with zero packet loss.

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

# 1. Generate the OpenUSD Venue Stage
python modules/01_openusd_venue/generate_venue_stage.py

# 2. Inspect Stage in usdview
usdview modules/01_openusd_venue/venue_stage.usda

# 3. Generate Scientific Benchmark Visualizations
python scripts/visualizations/calabria_earth2_validation.py
python scripts/visualizations/openusd_stage_composition.py
python scripts/visualizations/holoscan_streaming_benchmark.py

# 4. Compile the Publication Executive Summary PDF
python scripts/reports/generate_executive_summary_pdf.py
```
