import React from 'react';
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from '@open-motion/core';

// Color Palette
const COLORS = {
  bg: '#0F141C',
  panelBg: '#1A2230',
  nvidiaGreen: '#76B900',
  skyBlue: '#00A3E0',
  terracotta: '#D9531E',
  gold: '#F5A623',
  textPrimary: '#FFFFFF',
  textSecondary: '#94A3B8',
  border: '#2E3D52',
  accentDark: '#131A24',
};

export const VenueShowcaseVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  // Global camera pan & zoom interpolation (0 to 300 frames)
  const cameraZ = interpolate(frame, [0, 100, 200, 300], [1.0, 1.15, 1.25, 1.3], {
    extrapolateRight: 'clamp',
  });
  const cameraX = interpolate(frame, [0, 150, 300], [0, -40, 20], {
    extrapolateRight: 'clamp',
  });
  const cameraY = interpolate(frame, [0, 150, 300], [0, -20, -10], {
    extrapolateRight: 'clamp',
  });

  // Variant Transition Timeline (Standard Seating -> Gala Banquet at Frame 150)
  const isGalaVariant = frame >= 150;
  const variantTransitionProgress = spring({
    frame: frame - 150,
    fps,
    config: { damping: 15, mass: 0.8, stiffness: 100 },
  });

  // Stage Hierarchy Tree Unfold Animation
  const treeProgress = spring({
    frame: frame - 15,
    fps,
    config: { damping: 20, mass: 1 },
  });

  return (
    <div
      style={{
        width,
        height,
        backgroundColor: COLORS.bg,
        color: COLORS.textPrimary,
        fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background Subtle Coordinate Grid */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'radial-gradient(circle at 1px 1px, #263345 1px, transparent 0)',
          backgroundSize: '40px 40px',
          opacity: 0.4,
        }}
      />

      {/* Top Banner / Telemetry Bar */}
      <header
        style={{
          height: 90,
          borderBottom: `1px solid ${COLORS.border}`,
          backgroundColor: `${COLORS.accentDark}EE`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 48px',
          zIndex: 10,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div
            style={{
              width: 14,
              height: 14,
              borderRadius: '50%',
              backgroundColor: COLORS.nvidiaGreen,
              boxShadow: `0 0 12px ${COLORS.nvidiaGreen}`,
            }}
          />
          <div>
            <div style={{ fontSize: 20, fontWeight: 700, letterSpacing: '0.04em' }}>
              NVIDIA Omniverse & OpenUSD Digital Twin
            </div>
            <div style={{ fontSize: 13, color: COLORS.textSecondary }}>
              Italian Venue Stage · LIVRPS Composition Engine
            </div>
          </div>
        </div>

        {/* VariantSet Indicator Badge */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div
            style={{
              fontSize: 12,
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
              color: COLORS.textSecondary,
            }}
          >
            Active Variant:
          </div>
          <div
            style={{
              padding: '6px 16px',
              borderRadius: 6,
              fontSize: 14,
              fontWeight: 600,
              backgroundColor: isGalaVariant ? COLORS.terracotta : COLORS.skyBlue,
              color: '#FFFFFF',
              boxShadow: `0 0 16px ${
                isGalaVariant ? `${COLORS.terracotta}66` : `${COLORS.skyBlue}66`
              }`,
              transition: 'background-color 0.3s ease',
            }}
          >
            {isGalaVariant ? 'gala_banquet (12 Tables / 120 Guests)' : 'standard_seating (Auditorium / 120 Seats)'}
          </div>
        </div>
      </header>

      {/* Main Split View: Left (Stage Tree) | Right (Spatial Venue Viewport) */}
      <div style={{ display: 'flex', flex: 1, position: 'relative', zIndex: 5 }}>
        {/* Left Pane: Stage Prim Hierarchy */}
        <div
          style={{
            width: 480,
            borderRight: `1px solid ${COLORS.border}`,
            backgroundColor: `${COLORS.panelBg}BB`,
            padding: '32px 36px',
            display: 'flex',
            flexDirection: 'column',
            gap: 16,
          }}
        >
          <div
            style={{
              fontSize: 14,
              fontWeight: 700,
              color: COLORS.nvidiaGreen,
              letterSpacing: '0.06em',
              textTransform: 'uppercase',
            }}
          >
            Stage Prim Hierarchy (LIVRPS)
          </div>

          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 12,
              marginTop: 12,
              opacity: treeProgress,
              transform: `translateY(${(1 - treeProgress) * 20}px)`,
            }}
          >
            {/* Prim 1: /World */}
            <PrimRow name="/World" type="Xform" role="Default Prim (Stage Root)" active />

            {/* Prim 2: /World/Venue */}
            <div style={{ paddingLeft: 24 }}>
              <PrimRow name="Venue" type="Xform [assembly]" role="Measured Space" active />
            </div>

            {/* Prim 3: /World/Venue/Architecture (Payload) */}
            <div style={{ paddingLeft: 48 }}>
              <PrimRow
                name="Architecture"
                type="Payload Arc"
                role="@venue_architecture_payload.usda@"
                badge="Payload (Deferred)"
                badgeColor={COLORS.skyBlue}
                active
              />
            </div>

            {/* Prim 4: /World/Venue/Lighting */}
            <div style={{ paddingLeft: 48 }}>
              <PrimRow
                name="Lighting"
                type="Scope"
                role="DomeLight + Key SphereLight"
                active
              />
            </div>

            {/* Prim 5: /World/Venue/Layout (VariantSet) */}
            <div style={{ paddingLeft: 48 }}>
              <PrimRow
                name="Layout"
                type="VariantSet"
                role="layoutVariant"
                badge={isGalaVariant ? 'gala_banquet' : 'standard_seating'}
                badgeColor={isGalaVariant ? COLORS.terracotta : COLORS.gold}
                active
              />
            </div>
          </div>

          {/* Telemetry Card: Payload Memory Savings */}
          <div
            style={{
              marginTop: 'auto',
              padding: 20,
              borderRadius: 8,
              backgroundColor: COLORS.accentDark,
              border: `1px solid ${COLORS.border}`,
            }}
          >
            <div style={{ fontSize: 12, color: COLORS.textSecondary, marginBottom: 6 }}>
              SCENE OPTIMIZATION BENEFIT
            </div>
            <div style={{ fontSize: 24, fontWeight: 700, color: COLORS.nvidiaGreen }}>
              94.2% Memory Reduction
            </div>
            <div style={{ fontSize: 12, color: COLORS.textSecondary, marginTop: 4 }}>
              Payload deferral + VariantSet switching prevents duplicating 2.4GB mesh geometry across floorplan permutations.
            </div>
          </div>
        </div>

        {/* Right Pane: Animated 2.5D Venue Spatial Projection */}
        <div
          style={{
            flex: 1,
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden',
          }}
        >
          {/* Spatial Canvas Container with Dynamic Camera Transform */}
          <div
            style={{
              transform: `translate(${cameraX}px, ${cameraY}px) scale(${cameraZ})`,
              transition: 'transform 0.1s linear',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            {/* SVG Representation of Measured Venue Floorplan */}
            <svg width="800" height="520" viewBox="0 0 800 520">
              {/* Outer Palazzo Stone Walls */}
              <rect
                x="80"
                y="60"
                width="640"
                height="400"
                rx="12"
                fill="#161D29"
                stroke="#475569"
                strokeWidth="4"
              />

              {/* Terrazzo Floor Grid Pattern */}
              <pattern id="floor-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#232E3F" strokeWidth="1" />
              </pattern>
              <rect x="84" y="64" width="632" height="392" fill="url(#floor-grid)" />

              {/* Colonnade Architectural Pillars */}
              {[120, 200, 280, 360, 440, 520, 600, 680].map((cx, idx) => (
                <React.Fragment key={idx}>
                  <circle cx={cx} cy="80" r="10" fill="#64748B" stroke="#94A3B8" strokeWidth="2" />
                  <circle cx={cx} cy="440" r="10" fill="#64748B" stroke="#94A3B8" strokeWidth="2" />
                </React.Fragment>
              ))}

              {/* VARIANT 1: Standard Seating (Auditorium Rows) */}
              <g
                style={{
                  opacity: 1 - variantTransitionProgress,
                  transform: `translateY(${-variantTransitionProgress * 30}px)`,
                  transition: 'opacity 0.4s ease',
                }}
              >
                {/* Speaker Stage Podium */}
                <rect x="300" y="110" width="200" height="40" rx="4" fill="#3B82F6" opacity="0.8" />
                <text x="400" y="135" textAnchor="middle" fill="#FFFFFF" fontSize="13" fontWeight="bold">
                  PODIUM / LECTERN
                </text>

                {/* 10 Auditorium Seating Rows */}
                {[0, 1, 2, 3, 4, 5, 6, 7].map((rowIdx) => (
                  <rect
                    key={rowIdx}
                    x="200"
                    y={180 + rowIdx * 26}
                    width="400"
                    height="14"
                    rx="3"
                    fill="#1E293B"
                    stroke="#00A3E0"
                    strokeWidth="1.5"
                  />
                ))}
              </g>

              {/* VARIANT 2: Gala Banquet (Round Dining Tables) */}
              <g
                style={{
                  opacity: variantTransitionProgress,
                  transform: `translateY(${(1 - variantTransitionProgress) * 30}px)`,
                  transition: 'opacity 0.4s ease',
                }}
              >
                {/* 6 Distributed Round Banquet Tables */}
                {[
                  { cx: 240, cy: 160 },
                  { cx: 400, cy: 160 },
                  { cx: 560, cy: 160 },
                  { cx: 240, cy: 280 },
                  { cx: 400, cy: 280 },
                  { cx: 560, cy: 280 },
                  { cx: 240, cy: 380 },
                  { cx: 400, cy: 380 },
                  { cx: 560, cy: 380 },
                ].map((pos, tableIdx) => (
                  <g key={tableIdx}>
                    <circle
                      cx={pos.cx}
                      cy={pos.cy}
                      r="32"
                      fill="#2A1B16"
                      stroke={COLORS.terracotta}
                      strokeWidth="2.5"
                    />
                    <circle cx={pos.cx} cy={pos.cy} r="6" fill="#F5A623" />
                    <text
                      x={pos.cx}
                      y={pos.cy + 4}
                      textAnchor="middle"
                      fill="#E2E8F0"
                      fontSize="10"
                      fontWeight="600"
                    >
                      T{tableIdx + 1}
                    </text>
                  </g>
                ))}
              </g>
            </svg>

            {/* Bottom In-Viewport Overlay Label */}
            <div
              style={{
                marginTop: 18,
                padding: '8px 20px',
                borderRadius: 20,
                backgroundColor: `${COLORS.accentDark}CC`,
                border: `1px solid ${COLORS.border}`,
                fontSize: 13,
                color: COLORS.textSecondary,
                display: 'flex',
                gap: 16,
              }}
            >
              <span>Frame: <strong>{frame} / {durationInFrames}</strong></span>
              <span>•</span>
              <span>Camera: <strong>X:{cameraX.toFixed(1)} Y:{cameraY.toFixed(1)} Zoom:{cameraZ.toFixed(2)}x</strong></span>
              <span>•</span>
              <span>Payload: <strong>LOADED</strong></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Reusable Prim Row Component
interface PrimRowProps {
  name: string;
  type: string;
  role: string;
  badge?: string;
  badgeColor?: string;
  active?: boolean;
}

const PrimRow: React.FC<PrimRowProps> = ({
  name,
  type,
  role,
  badge,
  badgeColor = COLORS.skyBlue,
  active = true,
}) => (
  <div
    style={{
      padding: '10px 14px',
      borderRadius: 6,
      backgroundColor: active ? COLORS.accentDark : 'transparent',
      border: `1px solid ${COLORS.border}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
    }}
  >
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontSize: 14, fontWeight: 700, color: COLORS.textPrimary }}>
          {name}
        </span>
        <span style={{ fontSize: 11, color: COLORS.textSecondary }}>[{type}]</span>
      </div>
      <div style={{ fontSize: 11, color: COLORS.textSecondary, marginTop: 2 }}>
        {role}
      </div>
    </div>
    {badge && (
      <span
        style={{
          fontSize: 10,
          fontWeight: 700,
          padding: '4px 8px',
          borderRadius: 4,
          backgroundColor: `${badgeColor}22`,
          color: badgeColor,
          border: `1px solid ${badgeColor}66`,
          textTransform: 'uppercase',
        }}
      >
        {badge}
      </span>
    )}
  </div>
);
