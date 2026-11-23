# Module 02: Earth-2 Calabria Extreme Weather & Decision Intelligence

This module implements the **Calabria Extreme Convective Precipitation Experiment**, supporting the **Days 31–60 Milestone** of the 90-day NVIDIA & Geospatial Digital Twins roadmap.

---

## 🌪️ Scientific Problem & Experiment Rationale

The Calabria peninsula in Southern Italy is prone to rapid mesoscale convective systems (MCS) and Mediterranean cyclogenesis ("medicanes"), driven by steep orographic gradients (Aspromonte, Sila, and Serre massifs) bounded by the warm Tyrrhenian and Ionian Seas.

Numerical Weather Prediction (NWP) models (e.g., IFS, GFS) frequently suffer from spatial displacement errors and precipitation underestimation in complex coastal terrain due to computational constraints on grid resolution and convection parameterization.

This experiment evaluates **NVIDIA Earth-2** AI weather forecasting models—specifically **FourCastNet (AFNO)**—against standard NWP baselines and ECMWF ERA5 reanalysis ground truth over a 72-hour forecast horizon.

---

## 🗺️ Geospatial Domain & Bounding Box

```
North Latitude: 40.2° N  (Northern Pollino Massif / Basilicata border)
South Latitude: 38.0° N  (Strait of Messina / Southern Aspromonte)
West Longitude: 15.5° E  (Tyrrhenian Sea coastal approach)
East Longitude: 17.5° E  (Ionian Sea maritime boundary)
```

The domain encompasses critical civil protection monitoring nodes:
- Lamezia Terme atmospheric sounding station
- Catanzaro coastal isthmus
- Crotone maritime convective convergence zone

---

## 🧠 Model Configuration & Earth-2 Pipeline

- **AI Model**: FourCastNet v2 (`FourCastNet_AFNO`)
- **Neural Backbone**: Adaptive Fourier Neural Operators (AFNO) operating in the spectral 2D Fourier domain with spatial token mixing.
- **Inference Horizon**: 72 hours lead time with 6-hour progressive auto-regressive rollout ($t_0 \to t_{+72h}$).
- **Prognostic Variables**:
  - Surface: Total Precipitation (`tp`), 10-meter wind vectors (`u10m`, `v10m`), 2-meter temperature (`t2m`), Mean Sea Level Pressure (`msl`).
  - Atmospheric Levels: 850 hPa wind & geopotential, 500 hPa geopotential height (`z500`), 700 hPa specific humidity (`q700`).
- **Ground Truth Baseline**: ECMWF ERA5 Hourly Reanalysis + regional automated telemetry network.

---

## 📊 Quantitative Evaluation Metrics

| Metric | Target Threshold | Description |
| :--- | :--- | :--- |
| **Convective Displacement** | $< 15.0\text{ km}$ | Center-of-mass spatial offset of maximum rain cell |
| **Domain Mean Absolute Error (MAE)** | $< 2.50\text{ mm/h}$ | Grid-averaged residual error over Calabria domain |
| **Peak Precipitation Error** | $< 12.0\%$ | Extreme accumulation capture at orographic peak |
| **GPU Inference Latency** | $< 0.30\text{ s}$ | End-to-end 72h auto-regressive rollout on Tensor Core GPU |

---

## 📁 Module Artifacts

- `calabria_experiment_config.json`: Production execution configuration for Earth-2 Studio pipelines.
- `scripts/visualizations/calabria_earth2_validation.py`: Publication-grade visualization generator.
- `reports/figures/calabria_earth2_validation.png`: 300 DPI high-resolution 4-panel scientific diagnostic chart.
- `reports/figures/calabria_earth2_validation.pdf`: Publication-ready vector graphic.

---

## 🔗 Milestone & Certification Alignment
- **Milestone**: Days 31–60 (`earth2studio` & `Cosmos`)
- **Target Certification**: NVIDIA Earth-2 Fundamentals / NVIDIA Certified Associate - Applied Multimodal AI & Data
