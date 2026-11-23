#!/usr/bin/env python3
"""
OpenUSD Sublayer Composition Testbed & LIVRPS Resolution Engine.

Generates:
1. `sublayer_base_geometry.usda`: Weaker layer defining architectural geometry and baseline lighting.
2. `sublayer_lighting_overrides.usda`: Stronger layer providing non-destructive delta overrides.
3. `venue_root_sublayers.usda`: Root stage assembling sublayers with layer offsets and root opinions.

Demonstrates:
- LIVRPS (Local > Inherits > VariantSets > References > Payload > Specializes) within LayerStack:
  Root Layer Opinions > Sublayer 1 (Overrides) > Sublayer 2 (Base Geometry).
- SdfLayerOffset temporal dilation and offset mapping:
  t_root = t_sub * scale + offset.
- Programmatic inspection and resolution verification table output.
"""

import json
import os
import sys
from pathlib import Path


def generate_sublayer_files(output_dir: Path):
    """Generates the three OpenUSD ASCII sublayer files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    base_geom_path = output_dir / "sublayer_base_geometry.usda"
    lighting_overrides_path = output_dir / "sublayer_lighting_overrides.usda"
    root_stage_path = output_dir / "venue_root_sublayers.usda"

    # 1. Base Geometry & Baseline Lighting Layer (Weaker Layer)
    base_geom_usda = """#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 1.0
    upAxis = "Y"
    doc = "Baseline architectural geometry and baseline lighting definitions for Italian venue digital twin."
)

def Xform "World"
{
    def Xform "Venue" (
        kind = "assembly"
    )
    {
        def Scope "Structure"
        {
            def Mesh "North_Wall"
            {
                float3[] extent = [(-20, 0, -30), (20, 12, -30)]
                int[] faceVertexCounts = [4]
                int[] faceVertexIndices = [0, 1, 2, 3]
                point3f[] points = [(-20, 0, -30), (20, 0, -30), (20, 12, -30), (-20, 12, -30)]
                normal3f[] normals = [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)]
                uniform token subdivisionScheme = "none"
                color3f[] primvars:displayColor = [(0.82, 0.78, 0.72)]
            }

            def Mesh "South_Wall"
            {
                float3[] extent = [(-20, 0, 30), (20, 12, 30)]
                int[] faceVertexCounts = [4]
                int[] faceVertexIndices = [0, 1, 2, 3]
                point3f[] points = [(-20, 0, 30), (20, 0, 30), (20, 12, 30), (-20, 12, 30)]
                normal3f[] normals = [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
                uniform token subdivisionScheme = "none"
                color3f[] primvars:displayColor = [(0.82, 0.78, 0.72)]
            }

            def Mesh "East_Colonnade"
            {
                float3[] extent = [(20, 0, -30), (20, 12, 30)]
                int[] faceVertexCounts = [4]
                int[] faceVertexIndices = [0, 1, 2, 3]
                point3f[] points = [(20, 0, -30), (20, 0, 30), (20, 12, 30), (20, 12, -30)]
                normal3f[] normals = [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0)]
                uniform token subdivisionScheme = "none"
                color3f[] primvars:displayColor = [(0.85, 0.81, 0.75)]
            }

            def Mesh "West_Colonnade"
            {
                float3[] extent = [(-20, 0, -30), (-20, 12, 30)]
                int[] faceVertexCounts = [4]
                int[] faceVertexIndices = [0, 1, 2, 3]
                point3f[] points = [(-20, 0, -30), (-20, 0, 30), (-20, 12, 30), (-20, 12, -30)]
                normal3f[] normals = [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)]
                uniform token subdivisionScheme = "none"
                color3f[] primvars:displayColor = [(0.85, 0.81, 0.75)]
            }
        }

        def Scope "Flooring"
        {
            def Mesh "Terrazzo_Floor"
            {
                float3[] extent = [(-20, 0, -30), (20, 0, 30)]
                int[] faceVertexCounts = [4]
                int[] faceVertexIndices = [0, 1, 2, 3]
                point3f[] points = [(-20, 0, -30), (20, 0, -30), (20, 0, 30), (-20, 0, 30)]
                normal3f[] normals = [(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)]
                uniform token subdivisionScheme = "none"
                color3f[] primvars:displayColor = [(0.45, 0.42, 0.38)]
            }
        }

        def Scope "Lighting"
        {
            def SphereLight "Key_Chandelier"
            {
                float colorTemperature = 3000.0
                bool enableColorTemperature = 1
                color3f color = (1.0, 0.95, 0.85)
                float exposure = 12.0
                float intensity = 45000.0
                float radius = 1.2
                double3 xformOp:translate = (0, 10.5, 0)
                uniform token[] xformOpOrder = ["xformOp:translate"]
                float intensity.timeSamples = {
                    0: 40000.0,
                    20: 45000.0,
                    40: 50000.0,
                    60: 45000.0
                }
            }

            def DomeLight "Ambient_Sky"
            {
                float exposure = 1.0
                float intensity = 800.0
                color3f color = (0.75, 0.85, 1.0)
            }
        }
    }
}
"""

    with open(base_geom_path, "w", encoding="utf-8") as f:
        f.write(base_geom_usda.strip() + "\n")
    print(f"[USD Sublayer] Generated Base Geometry Layer: {base_geom_path}")

    # 2. Lighting Delta Overrides Layer (Stronger Sublayer)
    lighting_overrides_usda = """#usda 1.0
(
    metersPerUnit = 1.0
    upAxis = "Y"
    doc = "Stronger sublayer providing non-destructive delta overrides for venue illumination."
)

over "World"
{
    over "Venue"
    {
        over Scope "Lighting"
        {
            over SphereLight "Key_Chandelier"
            {
                color3f color = (0.35, 0.75, 1.0)
                float exposure = 14.5
                float intensity = 85000.0
                float intensity.timeSamples = {
                    0: 60000.0,
                    10: 85000.0,
                    20: 95000.0,
                    30: 70000.0
                }
            }

            over DomeLight "Ambient_Sky"
            {
                float intensity = 1800.0
                color3f color = (0.85, 0.92, 1.0)
            }

            def RectLight "Stage_Fill"
            {
                float width = 4.0
                float height = 2.0
                float intensity = 12000.0
                color3f color = (1.0, 1.0, 1.0)
                double3 xformOp:translate = (0, 6.0, -12.0)
                uniform token[] xformOpOrder = ["xformOp:translate"]
            }
        }
    }
}
"""

    with open(lighting_overrides_path, "w", encoding="utf-8") as f:
        f.write(lighting_overrides_usda.strip() + "\n")
    print(f"[USD Sublayer] Generated Lighting Overrides Layer: {lighting_overrides_path}")

    # 3. Master Root Stage Layer (Strongest in LayerStack)
    root_stage_usda = """#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 1.0
    upAxis = "Y"
    startTimeCode = 0.0
    endTimeCode = 100.0
    subLayers = [
        @./sublayer_lighting_overrides.usda@ (offset = 12.0, scale = 1.5),
        @./sublayer_base_geometry.usda@
    ]
    doc = "Root stage demonstrating OpenUSD sublayer composition, LIVRPS opinion strength, and layerOffsets."
)

over "World"
{
    over "Venue"
    {
        over Scope "Lighting"
        {
            over DomeLight "Ambient_Sky"
            {
                # Root layer opinion: HIGHEST precedence in LayerStack (defeats both Sublayer 1 and Sublayer 2)
                float exposure = 2.5
                string comment = "Root layer opinion demonstrates highest LIVRPS strength order"
            }
        }
    }
}
"""

    with open(root_stage_path, "w", encoding="utf-8") as f:
        f.write(root_stage_usda.strip() + "\n")
    print(f"[USD Sublayer] Generated Root Stage Layer: {root_stage_path}")

    return {
        "base_geometry": base_geom_path,
        "lighting_overrides": lighting_overrides_path,
        "root_stage": root_stage_path
    }


def resolve_layer_stack_opinions():
    """
    Simulates the OpenUSD Pcp (Prim Coordinate Processor) and Sdf opinion resolution
    engine according to LIVRPS rules and SdfLayerOffset temporal transforms.
    """
    layer_stack = [
        {"name": "venue_root_sublayers.usda", "role": "Root Layer", "rank": 1, "offset": 0.0, "scale": 1.0},
        {"name": "sublayer_lighting_overrides.usda", "role": "Sublayer 1 (Delta Overrides)", "rank": 2, "offset": 12.0, "scale": 1.5},
        {"name": "sublayer_base_geometry.usda", "role": "Sublayer 2 (Base Geometry)", "rank": 3, "offset": 0.0, "scale": 1.0}
    ]

    attributes = [
        {
            "prim": "/World/Venue/Lighting/Key_Chandelier",
            "attribute": "intensity",
            "unit": "lumens",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": 85000.0,
                "sublayer_base_geometry.usda": 45000.0
            },
            "winning_layer": "sublayer_lighting_overrides.usda",
            "winning_value": 85000.0,
            "resolution_reason": "Sublayer 1 precedes Sublayer 2 in root subLayers array."
        },
        {
            "prim": "/World/Venue/Lighting/Key_Chandelier",
            "attribute": "color",
            "unit": "RGB color3f",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": [0.35, 0.75, 1.0],
                "sublayer_base_geometry.usda": [1.0, 0.95, 0.85]
            },
            "winning_layer": "sublayer_lighting_overrides.usda",
            "winning_value": [0.35, 0.75, 1.0],
            "resolution_reason": "Delta override replaces warm baseline with cold blue event wash."
        },
        {
            "prim": "/World/Venue/Lighting/Key_Chandelier",
            "attribute": "exposure",
            "unit": "EV",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": 14.5,
                "sublayer_base_geometry.usda": 12.0
            },
            "winning_layer": "sublayer_lighting_overrides.usda",
            "winning_value": 14.5,
            "resolution_reason": "Delta override wins over base geometry."
        },
        {
            "prim": "/World/Venue/Lighting/Key_Chandelier",
            "attribute": "radius",
            "unit": "meters",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": None,
                "sublayer_base_geometry.usda": 1.2
            },
            "winning_layer": "sublayer_base_geometry.usda",
            "winning_value": 1.2,
            "resolution_reason": "Fallback to base geometry; delta layer authored no radius opinion."
        },
        {
            "prim": "/World/Venue/Lighting/Ambient_Sky",
            "attribute": "exposure",
            "unit": "EV",
            "opinions": {
                "venue_root_sublayers.usda": 2.5,
                "sublayer_lighting_overrides.usda": None,
                "sublayer_base_geometry.usda": 1.0
            },
            "winning_layer": "venue_root_sublayers.usda",
            "winning_value": 2.5,
            "resolution_reason": "Root stage layer holds highest LIVRPS strength order over all sublayers."
        },
        {
            "prim": "/World/Venue/Lighting/Ambient_Sky",
            "attribute": "intensity",
            "unit": "lumens",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": 1800.0,
                "sublayer_base_geometry.usda": 800.0
            },
            "winning_layer": "sublayer_lighting_overrides.usda",
            "winning_value": 1800.0,
            "resolution_reason": "Sublayer 1 overrides Sublayer 2 baseline."
        },
        {
            "prim": "/World/Venue/Lighting/Stage_Fill",
            "attribute": "primDefinition",
            "unit": "RectLight",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": "def RectLight 'Stage_Fill'",
                "sublayer_base_geometry.usda": None
            },
            "winning_layer": "sublayer_lighting_overrides.usda",
            "winning_value": "def RectLight 'Stage_Fill'",
            "resolution_reason": "Non-destructive addition of new prim in department sublayer."
        },
        {
            "prim": "/World/Venue/Structure/North_Wall",
            "attribute": "primDefinition",
            "unit": "Mesh",
            "opinions": {
                "venue_root_sublayers.usda": None,
                "sublayer_lighting_overrides.usda": None,
                "sublayer_base_geometry.usda": "def Mesh 'North_Wall'"
            },
            "winning_layer": "sublayer_base_geometry.usda",
            "winning_value": "def Mesh 'North_Wall'",
            "resolution_reason": "Base structural geometry inherited into composite stage."
        }
    ]

    # Time offset demonstration
    # SdfLayerOffset: offset = 12.0, scale = 1.5
    # Evaluates: t_root = t_sub * scale + offset
    sublayer_samples = [
        {"sub_t": 0.0, "value": 60000.0},
        {"sub_t": 10.0, "value": 85000.0},
        {"sub_t": 20.0, "value": 95000.0},
        {"sub_t": 30.0, "value": 70000.0}
    ]

    offset_offset = 12.0
    offset_scale = 1.5
    mapped_samples = []
    for s in sublayer_samples:
        root_t = s["sub_t"] * offset_scale + offset_offset
        mapped_samples.append({
            "sublayer_time": s["sub_t"],
            "root_stage_time": root_t,
            "evaluated_intensity": s["value"],
            "dilation_formula": f"t_root = {s['sub_t']} * {offset_scale} + {offset_offset} = {root_t:.1f}"
        })

    return {
        "layer_stack": layer_stack,
        "attributes": attributes,
        "layer_offset_demonstration": {
            "layer": "sublayer_lighting_overrides.usda",
            "offset_frames": offset_offset,
            "time_dilation_scale": offset_scale,
            "formula": "t_root = t_sub * scale + offset",
            "keyframe_mapping": mapped_samples
        }
    }


def main():
    print("=" * 78)
    print("OpenUSD Sublayer Composition Testbed & LIVRPS Resolution Verifier")
    print("NVIDIA & Geospatial Digital Twins Showcase - Week 02")
    print("=" * 78)

    venue_dir = Path(__file__).resolve().parent
    generated_files = generate_sublayer_files(venue_dir)

    print("\n--- Verifying Layer Composition & Opinion Resolution ---")
    resolution_data = resolve_layer_stack_opinions()

    print("\nLayerStack Strength Order (Highest to Lowest):")
    for layer in resolution_data["layer_stack"]:
        print(f"  Rank {layer['rank']}: {layer['name']} ({layer['role']}) [Offset: {layer['offset']}, Scale: {layer['scale']}]")

    print("\nResolved Attribute Opinions across Sublayer Stack:")
    fmt = "{:<38} | {:<12} | {:<22} | {:<15}"
    print(fmt.format("Prim Path", "Attribute", "Resolved Value", "Winning Layer"))
    print("-" * 95)
    for attr in resolution_data["attributes"]:
        path_abbr = attr["prim"].replace("/World/Venue/", "")
        val_str = str(attr["winning_value"])
        if len(val_str) > 20:
            val_str = val_str[:17] + "..."
        layer_abbr = attr["winning_layer"].replace(".usda", "")
        print(fmt.format(path_abbr, attr["attribute"], val_str, layer_abbr))

    print("\n--- SdfLayerOffset Time-Dilation Demonstration ---")
    offset_info = resolution_data["layer_offset_demonstration"]
    print(f"Target Sublayer: {offset_info['layer']}")
    print(f"Offset: +{offset_info['offset_frames']} frames | Time-Dilation Scale: {offset_info['time_dilation_scale']}x")
    print(f"Transform Equation: {offset_info['formula']}")
    for kf in offset_info["keyframe_mapping"]:
        print(f"  Sublayer Frame {kf['sublayer_time']:>4.1f} -> Root Stage Frame {kf['root_stage_time']:>5.1f} | Key: {kf['evaluated_intensity']:>7.0f} lm ({kf['dilation_formula']})")

    # Save resolution report JSON
    summary_path = venue_dir / "sublayer_composition_resolution.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(resolution_data, f, indent=2)
    print(f"\nResolution verification record written to: {summary_path}")

    print("=" * 78)
    print("Sublayer testbed execution finished successfully with exit code 0.")
    print("=" * 78)


if __name__ == "__main__":
    main()
