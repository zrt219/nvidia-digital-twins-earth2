# NVIDIA & Geospatial Digital Twins Learning Showcase

[![Release](https://img.shields.io/badge/release-v0.1.0-blue.svg)](releases/WEEK_01_REPORT.md)
[![Certification](https://img.shields.io/badge/NCA--OFW-Week%2001%20Verified%20(95%2F100)-success.svg)](certifications/NCA-OFW_study_tracker.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A reproducible, production-grade engineering repository tracking demonstrable technical milestones across **NVIDIA Omniverse**, **OpenUSD simulation**, **Earth-2 weather intelligence**, **Cosmos physical AI**, and **Holoscan ultra-low-latency sensor streaming**.

---

## 🎯 Syllabus & 90-Day Execution Roadmap

| Milestone | Target Framework | Module Directory | Output Deliverable | Certification Tracking | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Days 1–30** | `LearnOpenUSD` & `kit-app-template` | [`modules/01_openusd_venue/`](modules/01_openusd_venue/) | Italian venue measured scene + payload architecture + 2 layout variants | [NCA-OFW Tracker](certifications/NCA-OFW_study_tracker.md) | 🟢 **Week 01 Complete** |
| **Days 31–60** | `earth2studio` & `Cosmos` | [`modules/02_earth2_calabria/`](modules/02_earth2_calabria/)<br>[`modules/03_cosmos_physical_ai/`](modules/03_cosmos_physical_ai/) | Calabria convective weather benchmark + tokenized world model suite | Earth-2 Discover / NCA-AMAD | 🟢 **Benchmark Verified** |
| **Days 61–90** | `holoscan-sdk` & `daqiri` | [`modules/04_holoscan_daqiri/`](modules/04_holoscan_daqiri/) | ConnectX GPUDirect RDMA pipeline + sub-15ms streaming latency demo | Specialist Eng / NCP-OUSD | ⚪ **Architecture Scaffolding** |

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
│   │   └── venue_architecture_payload.usda # Deferred architectural payload
│   ├── 02_earth2_calabria/             # Earth-2 mesoscale convective weather experiment
│   │   ├── README.md                   # Meteorological and domain specification
│   │   └── calabria_experiment_config.json # FourCastNet execution configuration
│   ├── 03_cosmos_physical_ai/          # NVIDIA Cosmos tokenized physical AI foundation
│   │   └── README.md                   # World model & PhysX 5 dynamics bridge architecture
│   └── 04_holoscan_daqiri/             # Holoscan SDK & DAQIRI streaming benchmarks
│       └── README.md                   # GPUDirect RDMA & Rivermax sub-15ms SLA architecture
├── scripts/
│   └── visualizations/
│       └── calabria_earth2_validation.py # Publication-grade matplotlib diagnostic generator
├── reports/
│   └── figures/
│       ├── calabria_earth2_validation.png # 300 DPI 4-panel diagnostic raster
│       └── calabria_earth2_validation.pdf # High-resolution publication vector PDF
├── releases/
│   └── WEEK_01_REPORT.md               # Weekly proof-of-work report (v0.1.0)
└── campaign/
    └── week_01_post.md                 # Technical LinkedIn showcase post & recruiter hook
```

---

## 📈 Weekly Proof-of-Work Reports & Campaign Logs

- **Week 01 Release**:
  - 📋 [Week 01 Proof-of-Work Report](releases/WEEK_01_REPORT.md) (`v0.1.0`): Detailed breakdown of OpenUSD payload composition, Earth-2 quantitative verification metrics table, and NCA-OFW checklist.
  - 📢 [Week 01 Campaign Showcase Post](campaign/week_01_post.md): Technical breakdown for engineering leads and talent partners at NVIDIA, Cesium, Esri, Tomorrow.io, and Planet Labs.

---

## 📊 Scientific Visualizations

Figures in [`reports/figures/`](reports/figures/) adhere to rigorous publication-grade visualization standards (sans-serif typographic hierarchy, balanced zero-centered colormaps for spatial deltas, direct line labeling, and 95% confidence intervals):

- **Calabria Mesoscale Weather Benchmark (FourCastNet vs. ERA5)**:
  - High-Res Raster (300 DPI): [`reports/figures/calabria_earth2_validation.png`](reports/figures/calabria_earth2_validation.png)
  - Vector Graphic (PDF): [`reports/figures/calabria_earth2_validation.pdf`](reports/figures/calabria_earth2_validation.pdf)
  - Python Generator: [`scripts/visualizations/calabria_earth2_validation.py`](scripts/visualizations/calabria_earth2_validation.py)

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

# 3. Re-run Publication-Grade Earth-2 Scientific Benchmark
python scripts/visualizations/calabria_earth2_validation.py
```
