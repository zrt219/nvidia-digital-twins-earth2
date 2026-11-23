"""
Unit and Integration Test Suite for Earth-2 Inference Pipeline & Cosmos Physical AI Tokenizer.
Validates:
1. Bounding box constraints and coordinate bounds (38.0-40.2N, 15.5-17.5E).
2. Earth-2 FourCastNet / AFNO meteorological vector field ranges and physical limits.
3. Cosmos mesh tokenizer discrete wind pressure tokens and continuous PhysX 5 PBD ingress vectors.
4. Exported payload schema compliance and physical realism.
"""

import json
import math
import sys
from pathlib import Path
import pytest
import numpy as np

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "modules" / "02_earth2_calabria"))
sys.path.insert(0, str(_REPO_ROOT / "modules" / "03_cosmos_physical_ai"))

from earth2studio_inference_pipeline import Earth2StudioPipeline
from cosmos_mesh_tokenizer import CosmosMeshTokenizer


@pytest.fixture(scope="module")
def repo_root():
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def earth2_pipeline(repo_root):
    config_path = repo_root / "modules" / "02_earth2_calabria" / "calabria_experiment_config.json"
    pipeline = Earth2StudioPipeline(config_path=config_path)
    return pipeline


@pytest.fixture(scope="module")
def earth2_payload(earth2_pipeline):
    payload = earth2_pipeline.execute_rollout(target_step=4)
    return payload


@pytest.fixture(scope="module")
def cosmos_tokenizer(repo_root):
    tokenizer = CosmosMeshTokenizer()
    return tokenizer


@pytest.fixture(scope="module")
def cosmos_spec(cosmos_tokenizer):
    spec = cosmos_tokenizer.generate_token_spec()
    return spec


# ==============================================================================
# 1. Domain Bounding Box & Geospatial Constraints
# ==============================================================================

def test_bounding_box_constraints(earth2_pipeline):
    """Verifies that the Calabria domain strictly adheres to 38.0-40.2°N, 15.5-17.5°E."""
    assert earth2_pipeline.lat_min == 38.0
    assert earth2_pipeline.lat_max == 40.2
    assert earth2_pipeline.lon_min == 15.5
    assert earth2_pipeline.lon_max == 17.5
    assert earth2_pipeline.lat_max > earth2_pipeline.lat_min
    assert earth2_pipeline.lon_max > earth2_pipeline.lon_min


def test_grid_resolution_and_coverage(earth2_pipeline):
    """Verifies grid resolution and that coordinates span the full bounding box."""
    assert earth2_pipeline.res_deg == 0.05
    assert len(earth2_pipeline.lats) >= 40
    assert len(earth2_pipeline.lons) >= 40
    assert np.isclose(earth2_pipeline.lats[0], 38.0)
    assert np.isclose(earth2_pipeline.lats[-1], 40.2)
    assert np.isclose(earth2_pipeline.lons[0], 15.5)
    assert np.isclose(earth2_pipeline.lons[-1], 17.5)


def test_key_regions_within_bounds(earth2_pipeline):
    """Verifies all civil protection monitoring stations reside within the Calabria bounding box."""
    for region in earth2_pipeline.key_regions:
        lat = region["lat"]
        lon = region["lon"]
        assert 38.0 <= lat <= 40.2, f"{region['name']} lat {lat} out of bounds"
        assert 15.5 <= lon <= 17.5, f"{region['name']} lon {lon} out of bounds"
        assert region["elevation_m"] >= 0


# ==============================================================================
# 2. Earth-2 FourCastNet / AFNO Physical Parameter Ranges
# ==============================================================================

def test_earth2_payload_file_exists(repo_root):
    """Ensures calabria_forecast_step.json is present on disk."""
    json_path = repo_root / "modules" / "02_earth2_calabria" / "calabria_forecast_step.json"
    assert json_path.exists(), f"Payload missing at {json_path}"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["schema_version"] == "1.0.0"
    assert "selected_step" in data


def test_earth2_meteorological_physical_ranges(earth2_payload):
    """Validates realistic physical limits for all prognostic atmospheric fields."""
    step = earth2_payload["selected_step"]
    stats = step["domain_statistics"]

    # 1. 10m Wind vectors (u10, v10)
    u_min, u_max = stats["u10_range_m_s"]
    v_min, v_max = stats["v10_range_m_s"]
    assert -50.0 <= u_min <= 50.0
    assert -50.0 <= u_max <= 50.0
    assert -50.0 <= v_min <= 50.0
    assert -50.0 <= v_max <= 50.0

    # 2. Wind Speed
    wind_max = stats["wind_speed_max_m_s"]
    wind_mean = stats["wind_speed_mean_m_s"]
    assert 0.0 <= wind_mean <= wind_max
    assert wind_max <= 75.0  # Max Mediterranean gale speed

    # 3. Precipitation Rate (mm/h)
    precip_max = stats["precipitation_rate_max_mm_h"]
    precip_mean = stats["precipitation_rate_mean_mm_h"]
    assert precip_mean >= 0.0
    assert precip_max >= precip_mean
    assert precip_max <= 150.0  # Physical extreme limit for convective cell

    # 4. Surface Pressure (MSL in hPa)
    msl_min = stats["msl_pressure_min_hpa"]
    msl_max = stats["msl_pressure_max_hpa"]
    assert 940.0 <= msl_min <= 1040.0
    assert 960.0 <= msl_max <= 1050.0
    assert msl_min <= msl_max

    # 5. Surface Temperature (T2m in Kelvin)
    t_min, t_max = stats["t2m_range_k"]
    assert 260.0 <= t_min <= 315.0
    assert 260.0 <= t_max <= 315.0


def test_venue_microclimate_boundary(earth2_payload):
    """Validates venue localized microclimate boundary condition mapping."""
    boundary = earth2_payload["selected_step"]["venue_microclimate_boundary"]
    assert 38.0 <= boundary["latitude"] <= 40.2
    assert 15.5 <= boundary["longitude"] <= 17.5
    wind = boundary["wind_vector_m_s"]
    assert 0.0 <= wind["speed"] <= 60.0
    assert wind["gust"] >= wind["speed"]
    assert 0.0 <= wind["direction_deg"] < 360.0
    assert boundary["precipitation_mm_h"] >= 0.0
    assert boundary["flood_risk_category"] in ["LOW", "MODERATE", "HIGH"]
    assert boundary["air_density_kg_m3"] == 1.225


def test_earth2_latency_target(earth2_payload):
    """Ensures GPU inference latency satisfies the <0.30s benchmark target."""
    latency = earth2_payload["model_metadata"]["gpu_inference_latency_seconds"]
    assert latency < 0.30


# ==============================================================================
# 3. Cosmos Mesh Tokenizer & Physical AI Token Specification
# ==============================================================================

def test_cosmos_token_spec_exists(repo_root):
    """Ensures cosmos_token_spec.json exists and parses correctly."""
    spec_path = repo_root / "modules" / "03_cosmos_physical_ai" / "cosmos_token_spec.json"
    assert spec_path.exists(), f"Token spec missing at {spec_path}"
    with open(spec_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["token_specification_version"] == "1.0.0"
    assert "discrete_spatial_tokens" in data
    assert "continuous_physical_ingress_tokens" in data


def test_discrete_spatial_wind_tokens(cosmos_spec):
    """Validates structural wind load pressure tokens mapped to OpenUSD prims."""
    tokens = cosmos_spec["discrete_spatial_tokens"]["tokens"]
    assert len(tokens) == 6  # 4 walls/colonnades, floor, roof

    expected_prims = {
        "/World/Venue/Architecture/Perimeter_Structure/North_Wall",
        "/World/Venue/Architecture/Perimeter_Structure/South_Wall",
        "/World/Venue/Architecture/Perimeter_Structure/East_Colonnade",
        "/World/Venue/Architecture/Perimeter_Structure/West_Colonnade",
        "/World/Venue/Architecture/Flooring/Terrazzo_Floor",
        "/World/Venue/Architecture/Ceiling_Vaults/Vaulted_Arch",
    }
    found_prims = {t["prim_path"] for t in tokens}
    assert found_prims == expected_prims

    for token in tokens:
        assert token["surface_area_m2"] > 0
        assert token["mean_dynamic_pressure_pa"] >= 0
        assert token["peak_gust_pressure_pa"] >= token["mean_dynamic_pressure_pa"]
        # Force = pressure * area / 1000
        calc_force = (token["mean_dynamic_pressure_pa"] * token["surface_area_m2"]) / 1000.0
        assert math.isclose(token["total_force_kn"], calc_force, rel_tol=1e-2, abs_tol=0.1)
        # Quantized token code in byte range 0-255
        assert 0 <= token["quantized_token_code"] <= 255
        # Structural safety factor must be positive
        assert token["structural_safety_factor"] > 1.0


def test_continuous_physx5_pbd_tokens(cosmos_spec):
    """Validates PhysX 5 Position-Based Dynamics parameters for flood ingress."""
    ingress_tokens = cosmos_spec["continuous_physical_ingress_tokens"]["tokens"]
    assert len(ingress_tokens) >= 3

    for token in ingress_tokens:
        vel = token["continuous_velocity_vector_m_s"]
        assert len(vel) == 3
        speed = math.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2)
        assert 0.1 <= speed <= 5.0  # Realistic ingress flood flow velocity

        flow_l_s = token["flow_rate_liters_s"]
        assert flow_l_s >= 0.0

        pbd = token["physx5_pbd_parameters"]
        assert pbd["solver_type"] == "PositionBasedDynamics_Fluid_PBD"
        assert pbd["particle_radius_m"] > 0.0
        assert pbd["rest_density_kg_m3"] == 1000.0
        assert pbd["dynamic_viscosity_pa_s"] > 0.0
        assert pbd["continuous_contact_detection"] is True
        assert pbd["pbd_substep_iterations"] >= 4
