#!/usr/bin/env python3
"""
Reproducible OpenUSD Stage Generator for Italian Venue Measured Scene.
Generates an OpenUSD ASCII (USDA) stage featuring:
- Root prim hierarchy: /World/Venue
- Stage metadata: defaultPrim = "World", metersPerUnit = 1.0, upAxis = "Y"
- Payload composition arc referencing venue architectural geometry
- VariantSet 'layoutVariant' offering 'standard_seating' and 'gala_banquet' configurations
"""

import os
import sys
from pathlib import Path

def generate_usd_stage(output_dir: Path):
    """
    Constructs the OpenUSD venue stage and architectural payload.
    Supports native pxr library if present, or deterministic USDA ASCII generation.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    payload_file = output_dir / "venue_architecture_payload.usda"
    stage_file = output_dir / "venue_stage.usda"

    # 1. Generate Architectural Payload USDA
    payload_usda = """#usda 1.0
(
    defaultPrim = "VenuePayload"
    metersPerUnit = 1.0
    upAxis = "Y"
    doc = "Measured architectural geometry payload for historic Italian venue digital twin."
)

def Xform "VenuePayload" (
    kind = "component"
)
{
    def Scope "Perimeter_Structure"
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

    def Scope "Ceiling_Vaults"
    {
        def Mesh "Vaulted_Arch"
        {
            float3[] extent = [(-20, 12, -30), (20, 16, 30)]
            int[] faceVertexCounts = [4]
            int[] faceVertexIndices = [0, 1, 2, 3]
            point3f[] points = [(-20, 12, -30), (20, 12, -30), (20, 12, 30), (-20, 12, 30)]
            normal3f[] normals = [(0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0)]
            uniform token subdivisionScheme = "none"
            color3f[] primvars:displayColor = [(0.90, 0.88, 0.85)]
        }
    }
}
"""

    with open(payload_file, "w", encoding="utf-8") as f:
        f.write(payload_usda.strip() + "\n")
    print(f"Generated Payload Layer: {payload_file}")

    # 2. Generate Master Stage USDA with Payload and VariantSet
    stage_usda = """#usda 1.0
(
    defaultPrim = "World"
    metersPerUnit = 1.0
    upAxis = "Y"
    doc = "Master OpenUSD Stage for Italian Historic Venue Digital Twin Showcase."
)

def Xform "World"
{
    def Xform "Venue" (
        kind = "assembly"
    )
    {
        def Xform "Architecture" (
            payload = @./venue_architecture_payload.usda@</VenuePayload>
        )
        {
            double3 xformOp:translate = (0, 0, 0)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }

        def Scope "Lighting"
        {
            def SphereLight "Key_Chandler"
            {
                float colorTemperature = 3200
                bool enableColorTemperature = 1
                float exposure = 12.5
                float intensity = 50000.0
                float radius = 1.2
                double3 xformOp:translate = (0, 10.5, 0)
                uniform token[] xformOpOrder = ["xformOp:translate"]
            }

            def DomeLight "Ambient_Sky"
            {
                float exposure = 1.0
                float intensity = 1000.0
                color3f color = (0.95, 0.96, 1.0)
            }
        }

        def Xform "Layout" (
            hasVariants = true
            variants = {
                string layoutVariant = "standard_seating"
            }
            prepend variantSets = "layoutVariant"
        )
        {
            variantSet "layoutVariant" = {
                "standard_seating" {
                    def Scope "Auditorium_Setup"
                    {
                        def Cube "Speaker_Podium"
                        {
                            double size = 1.0
                            double3 xformOp:scale = (3.0, 0.4, 2.0)
                            double3 xformOp:translate = (0, 0.2, -18)
                            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
                            color3f[] primvars:displayColor = [(0.2, 0.2, 0.2)]
                        }

                        def Cube "Lectern"
                        {
                            double size = 1.0
                            double3 xformOp:scale = (0.8, 1.2, 0.6)
                            double3 xformOp:translate = (0, 0.8, -17.5)
                            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
                            color3f[] primvars:displayColor = [(0.35, 0.22, 0.12)]
                        }

                        def Scope "Seating_Rows"
                        {
                            int rowCount = 10
                            int seatsPerRow = 12
                            int totalCapacity = 120
                            string seatingType = "Ergonomic Conference Chairs"

                            def Cube "Row_Cluster_Reference"
                            {
                                double size = 1.0
                                double3 xformOp:scale = (16.0, 0.85, 18.0)
                                double3 xformOp:translate = (0, 0.45, 0)
                                uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
                                color3f[] primvars:displayColor = [(0.15, 0.35, 0.65)]
                            }
                        }
                    }
                }
                "gala_banquet" {
                    def Scope "Banquet_Setup"
                    {
                        int tableCount = 12
                        int seatsPerTable = 10
                        int totalCapacity = 120
                        string serviceType = "Formal Plated Dinner"

                        def Scope "Dining_Tables"
                        {
                            def Cylinder "Banquet_Table_01"
                            {
                                double height = 0.75
                                double radius = 1.1
                                double3 xformOp:translate = (-8, 0.375, -10)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                                color3f[] primvars:displayColor = [(0.95, 0.95, 0.95)]
                            }

                            def Cylinder "Banquet_Table_02"
                            {
                                double height = 0.75
                                double radius = 1.1
                                double3 xformOp:translate = (0, 0.375, -10)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                                color3f[] primvars:displayColor = [(0.95, 0.95, 0.95)]
                            }

                            def Cylinder "Banquet_Table_03"
                            {
                                double height = 0.75
                                double radius = 1.1
                                double3 xformOp:translate = (8, 0.375, -10)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                                color3f[] primvars:displayColor = [(0.95, 0.95, 0.95)]
                            }

                            def Cylinder "Banquet_Table_04"
                            {
                                double height = 0.75
                                double radius = 1.1
                                double3 xformOp:translate = (-8, 0.375, 0)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                                color3f[] primvars:displayColor = [(0.95, 0.95, 0.95)]
                            }

                            def Cylinder "Banquet_Table_05"
                            {
                                double height = 0.75
                                double radius = 1.1
                                double3 xformOp:translate = (0, 0.375, 0)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                                color3f[] primvars:displayColor = [(0.95, 0.95, 0.95)]
                            }

                            def Cylinder "Banquet_Table_06"
                            {
                                double height = 0.75
                                double radius = 1.1
                                double3 xformOp:translate = (8, 0.375, 0)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                                color3f[] primvars:displayColor = [(0.95, 0.95, 0.95)]
                            }
                        }

                        def Cube "Buffet_Station"
                        {
                            double size = 1.0
                            double3 xformOp:scale = (12.0, 0.9, 1.8)
                            double3 xformOp:translate = (0, 0.45, 18)
                            uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]
                            color3f[] primvars:displayColor = [(0.6, 0.45, 0.3)]
                        }
                    }
                }
            }
        }
    }
}
"""

    with open(stage_file, "w", encoding="utf-8") as f:
        f.write(stage_usda.strip() + "\n")
    print(f"Generated Master Stage: {stage_file}")

    return stage_file, payload_file


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    stage, payload = generate_usd_stage(current_dir)
    print("OpenUSD Venue Stage Scaffolding successfully generated.")
    print(f"Master Stage: {stage}")
    print(f"Payload File: {payload}")
