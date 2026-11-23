# Module 04: NVIDIA Holoscan SDK & DAQIRI Hardware Benchmarking

This module specifies the real-time sensor processing and hardware benchmarking pipeline for the **Days 61–90 Milestone** of the 90-day NVIDIA & Geospatial Digital Twins roadmap.

---

## ⚡ The Real-Time Streaming Challenge

Real-time geospatial digital twins and mission-critical physical AI systems require sub-millisecond sensor ingest and bounded glass-to-glass latency. Standard OS network stacks and PCI-e transfer hops introduce unacceptable jitter and latency spikes that violate real-time guarantees.

This module leverages the **NVIDIA Holoscan SDK** coupled with **DAQIRI hardware benchmarking** and **NVIDIA ConnectX SmartNICs** to achieve deterministic, ultra-low-latency data acquisition and visualization pipelines.

---

## 🏎️ Latency SLA Targets & Benchmarks

Operating at 4K 60fps / 120fps multi-sensor ingestion:

| Metric | Target Specification | Standard Kernel Baseline | Holoscan + ConnectX Target |
| :--- | :--- | :--- | :--- |
| **Glass-to-Glass Latency (P50)** | $< 10.0\text{ ms}$ | $45.0\text{ ms}$ | **$8.2\text{ ms}$** |
| **P95 Latency SLA** | **$< 15.0\text{ ms}$** | $72.5\text{ ms}$ | **$12.4\text{ ms}$** |
| **P99 Latency SLA** | **$< 20.0\text{ ms}$** | $110.0\text{ ms}$ | **$16.8\text{ ms}$** |
| **Packet Drop Rate** | $0.000\%$ | $0.450\%$ | **$0.000\%$** |
| **Jitter ($\sigma$)** | $< 1.2\text{ ms}$ | $14.8\text{ ms}$ | **$0.65\text{ ms}$** |

---

## 🔌 ConnectX Packet Acquisition Architecture

```
┌────────────────────────────────────────────────────────┐
│     High-Speed Sensor Array (LiDAR / 4K Cameras / RF)  │
└──────────────────────────┬─────────────────────────────┘
                           │ 100GbE / 200GbE RoCEv2 (SMPTE ST 2110 / Raw UDP)
                           ▼
┌────────────────────────────────────────────────────────┐
│      NVIDIA ConnectX-7 SmartNIC (Hardware Layer)       │
│  - Hardware PTP (IEEE 1588v2) timestamping             │
│  - Flow steering & packet filtering in silicon         │
└──────────────────────────┬─────────────────────────────┘
                           │ GPUDirect RDMA (Zero-Copy Bypass)
                           ▼
┌────────────────────────────────────────────────────────┐
│             NVIDIA GPU HBM / VRAM Direct Ingest        │
│  - No CPU copy / No host RAM bounce buffer             │
│  - Rivermax SDK packet parsing in GPU memory           │
└──────────────────────────┬─────────────────────────────┘
                           │ CUDA IPC / TensorRT Stream
                           ▼
┌────────────────────────────────────────────────────────┐
│                NVIDIA Holoscan SDK Pipeline            │
│  Operator 1: Receiver (GPUDirect Ingest)               │
│  Operator 2: Preprocessor (Debayer / PointCloud Filter)│
│  Operator 3: Inference (Cosmos / Deep Learning Model)  │
│  Operator 4: Renderer (Vulkan / Omniverse Display)     │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ Holoscan Operator Composition

The pipeline is implemented using Holoscan C++ and Python APIs:

```python
# Conceptual Holoscan Application Graph
from holoscan.core import Application
from holoscan.operators import RivermaxReceiverOp, FormatConverterOp, InferenceOp, VisualizerOp

class GeospatialStreamApp(Application):
    def compose(self):
        # 1. ConnectX-7 GPUDirect Ingest
        receiver = RivermaxReceiverOp(self, name="receiver", port="mlx5_0")
        
        # 2. TensorRT Zero-Copy Preprocessing
        converter = FormatConverterOp(self, name="converter")
        
        # 3. Low-latency AI Inference (Physical AI / Hazard Detection)
        inferer = InferenceOp(self, name="inferer", model_path="cosmos_edge.onnx")
        
        # 4. Low-latency Vulkan Output Viewport
        visualizer = VisualizerOp(self, name="visualizer")
        
        # Connect Execution FlowGraph
        self.add_flow(receiver, converter, {("rx_out", "in")})
        self.add_flow(converter, inferer, {("out", "in")})
        self.add_flow(inferer, visualizer, {("out", "in")})
```

---

## 📈 DAQIRI Instrumentation & Profiling
- **PTP Clock Sync**: Sub-microsecond synchronization with GPS/PTP master clock.
- **Hardware Event Counters**: Hardware monitoring of PCIe transaction queue depth and RDMA transfer stall cycles.
- **Real-Time Trace Visualizer**: Integration with NVIDIA Nsight Systems and Holoscan Profiler for cycle-accurate bottleneck diagnosis.

---

## 🔗 Milestone & Certification Alignment
- **Milestone**: Days 61–90 (`holoscan-sdk` & `daqiri`)
- **Target Certification**: Specialist Engineering / NVIDIA Certified Professional - OpenUSD
