"""
UMATTR Whiteboard Explainer Animation Renderer
================================================
Strictly adheres to /umattr-sketch-style specification:
- Pure #FFFFFF background (no paper textures, no vignettes).
- Bold hand-drawn black marker contour lines (#111111, width ~3.5px with organic stroke variation).
- Invisible ink reveal: contour lines appear smoothly with NO visible hand or pen.
- Flat color wipes: 250ms after contours finish, fill shapes with flat vibrant colors:
    * NVIDIA Green: #76B900
    * Sky Blue: #00A3E0
    * Italian Terracotta: #D9531E
    * Slate: #333333
- Top all-caps comic marker header; bottom all-caps takeaway caption.
- Renders two videos via FFmpeg:
    a) reports/videos/openusd_whiteboard_explainer.mp4
    b) reports/videos/earth2_whiteboard_explainer.mp4
- Saves keyframes to reports/figures/ for publication reporting.
"""

import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION_SEC = 8.0
TOTAL_FRAMES = int(FPS * DURATION_SEC)

# Brand Color Palette
COLOR_BG = (255, 255, 255)
COLOR_INK = (17, 17, 17)
COLOR_NVIDIA_GREEN = (118, 185, 0)
COLOR_SKY_BLUE = (0, 163, 224)
COLOR_TERRACOTTA = (217, 83, 30)
COLOR_SLATE = (51, 51, 51)
COLOR_LIGHT_GRAY = (220, 224, 230)
COLOR_WHITE = (255, 255, 255)

# Load fonts with robust fallbacks
def get_fonts():
    try:
        font_header = ImageFont.truetype("comic.ttf", 46)
        font_sub = ImageFont.truetype("comic.ttf", 22)
        font_box_title = ImageFont.truetype("comic.ttf", 26)
        font_box_text = ImageFont.truetype("arialbd.ttf", 18)
        font_code = ImageFont.truetype("consola.ttf", 17)
        font_footer = ImageFont.truetype("comic.ttf", 36)
        font_badge = ImageFont.truetype("arialbd.ttf", 16)
    except Exception:
        font_header = ImageFont.load_default()
        font_sub = font_header
        font_box_title = font_header
        font_box_text = font_header
        font_code = font_header
        font_footer = font_header
        font_badge = font_header
    return {
        "header": font_header,
        "sub": font_sub,
        "box_title": font_box_title,
        "box_text": font_box_text,
        "code": font_code,
        "footer": font_footer,
        "badge": font_badge,
    }

FONTS = get_fonts()


def organic_wobble(points, freq=0.08, amp=1.5):
    """Adds subtle hand-drawn organic variation to line vertices."""
    out = []
    for i, (x, y) in enumerate(points):
        dx = amp * math.sin(i * freq * 3.14 + 0.5)
        dy = amp * math.cos(i * freq * 2.71 + 1.2)
        out.append((x + dx, y + dy))
    return out


def draw_organic_polyline(draw, points, progress=1.0, color=COLOR_INK, base_width=3.5):
    """Draws a polyline with invisible-ink progress and organic stroke variation."""
    if len(points) < 2 or progress <= 0.0:
        return

    # Total cumulative length
    dists = [0.0]
    for i in range(1, len(points)):
        p1 = points[i - 1]
        p2 = points[i]
        d = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        dists.append(dists[-1] + d)

    total_len = dists[-1]
    if total_len == 0:
        return

    target_len = total_len * min(max(progress, 0.0), 1.0)

    # Draw segments up to target_len
    for i in range(1, len(points)):
        if dists[i - 1] >= target_len:
            break

        p1 = points[i - 1]
        p2 = points[i]
        seg_len = dists[i] - dists[i - 1]

        if dists[i] <= target_len:
            curr_p2 = p2
        else:
            fraction = (target_len - dists[i - 1]) / max(seg_len, 1e-5)
            curr_p2 = (
                p1[0] + (p2[0] - p1[0]) * fraction,
                p1[1] + (p2[1] - p1[1]) * fraction,
            )

        # Stroke thickness variation
        w = base_width + 0.6 * math.sin(i * 0.45)
        draw.line([p1, curr_p2], fill=color, width=max(2, int(round(w))))


def draw_curved_arrow(draw, start, end, control, progress=1.0, color=COLOR_INK, width=3.5):
    """Draws a hand-drawn quadratic bezier arrow from start to end."""
    if progress <= 0.0:
        return

    # Sample bezier points
    steps = 35
    raw_pts = []
    for s in range(steps + 1):
        t = s / float(steps)
        # B(t) = (1-t)^2 * P0 + 2(1-t)t * P1 + t^2 * P2
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
        raw_pts.append((x, y))

    pts = organic_wobble(raw_pts, freq=0.1, amp=1.2)
    draw_organic_polyline(draw, pts, progress=progress, color=color, base_width=width)

    # If arrow is nearly complete, draw arrowhead
    if progress > 0.90:
        arrow_prog = (progress - 0.90) / 0.10
        # Tangent at the end
        p_pre = pts[-2]
        p_end = pts[-1]
        angle = math.atan2(p_end[1] - p_pre[1], p_end[0] - p_pre[0])

        head_len = 18.0 * arrow_prog
        head_angle = 0.45  # radians

        left = (
            p_end[0] - head_len * math.cos(angle - head_angle),
            p_end[1] - head_len * math.sin(angle - head_angle),
        )
        right = (
            p_end[0] - head_len * math.cos(angle + head_angle),
            p_end[1] - head_len * math.sin(angle + head_angle),
        )

        draw.line([left, p_end], fill=color, width=max(2, int(round(width))))
        draw.line([right, p_end], fill=color, width=max(2, int(round(width))))


def draw_hand_drawn_rect(draw, x0, y0, x1, y1, progress=1.0, color=COLOR_INK, width=3.5, corner_radius=10):
    """Draws a rounded rectangle contour with organic hand-drawn wobble."""
    if progress <= 0.0:
        return

    raw_pts = []
    # Top edge
    for x in np.linspace(x0 + corner_radius, x1 - corner_radius, 15):
        raw_pts.append((float(x), float(y0)))
    # Top-right corner
    for theta in np.linspace(-math.pi / 2, 0, 6):
        raw_pts.append((float(x1 - corner_radius + corner_radius * math.cos(theta)),
                        float(y0 + corner_radius + corner_radius * math.sin(theta))))
    # Right edge
    for y in np.linspace(y0 + corner_radius, y1 - corner_radius, 15):
        raw_pts.append((float(x1), float(y)))
    # Bottom-right corner
    for theta in np.linspace(0, math.pi / 2, 6):
        raw_pts.append((float(x1 - corner_radius + corner_radius * math.cos(theta)),
                        float(y1 - corner_radius + corner_radius * math.sin(theta))))
    # Bottom edge
    for x in np.linspace(x1 - corner_radius, x0 + corner_radius, 15):
        raw_pts.append((float(x), float(y1)))
    # Bottom-left corner
    for theta in np.linspace(math.pi / 2, math.pi, 6):
        raw_pts.append((float(x0 + corner_radius + corner_radius * math.cos(theta)),
                        float(y1 - corner_radius + corner_radius * math.sin(theta))))
    # Left edge
    for y in np.linspace(y1 - corner_radius, y0 + corner_radius, 15):
        raw_pts.append((float(x0), float(y)))
    # Top-left corner
    for theta in np.linspace(math.pi, 3 * math.pi / 2, 6):
        raw_pts.append((float(x0 + corner_radius + corner_radius * math.cos(theta)),
                        float(y0 + corner_radius + corner_radius * math.sin(theta))))
    raw_pts.append(raw_pts[0])

    pts = organic_wobble(raw_pts, freq=0.08, amp=1.3)
    draw_organic_polyline(draw, pts, progress=progress, color=color, base_width=width)


def wipe_fill_rect(canvas, x0, y0, x1, y1, fill_color, wipe_progress, corner_radius=10):
    """Fills a rectangle with a directional top-to-bottom flat color wipe."""
    if wipe_progress <= 0.0:
        return canvas

    wipe_h = (y1 - y0) * min(max(wipe_progress, 0.0), 1.0)
    curr_y1 = y0 + wipe_h

    # Create mask for filled region
    fill_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fill_layer)

    # Draw rounded fill up to curr_y1
    fdraw.rounded_rectangle([x0 + 2, y0 + 2, x1 - 2, curr_y1], radius=corner_radius, fill=fill_color + (255,))

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(fill_layer)
    return canvas_rgba.convert("RGB")


# ==============================================================================
# ANIMATION 1: OpenUSD Whiteboard Explainer
# ==============================================================================
def render_openusd_frame(frame_idx):
    t = frame_idx / float(FPS)
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # 1. Header (0.0s -> 0.7s)
    header_prog = min(max(t / 0.6, 0.0), 1.0)
    if header_prog > 0.0:
        header_text = "OPENUSD STAGE ARCHITECTURE"
        sub_text = "COMPOSITION ARCS & DEFERRED PAYLOAD MEMORY OPTIMIZATION"
        # Draw header underline with marker ink reveal
        bbox = FONTS["header"].getbbox(header_text)
        tw = bbox[2] - bbox[0]
        tx = (WIDTH - tw) // 2
        ty = 45
        draw.text((tx, ty), header_text, fill=COLOR_INK, font=FONTS["header"])

        # Marker underline
        line_pts = [(tx - 20, ty + 58), (tx + tw + 20, ty + 58)]
        draw_organic_polyline(draw, line_pts, progress=header_prog, color=COLOR_NVIDIA_GREEN, base_width=4.5)

        sub_bbox = FONTS["sub"].getbbox(sub_text)
        sub_tx = (WIDTH - (sub_bbox[2] - sub_bbox[0])) // 2
        draw.text((sub_tx, ty + 68), sub_text, fill=COLOR_SLATE, font=FONTS["sub"])

    # Node 1: Stage Root (World)
    # Timeline: Ink: 0.6s -> 1.5s, 250ms gap: 1.5s -> 1.75s, Wipe: 1.75s -> 2.2s
    n1_x0, n1_y0, n1_x1, n1_y1 = 100, 360, 480, 720
    n1_ink_prog = min(max((t - 0.6) / 0.9, 0.0), 1.0)
    n1_wipe_prog = min(max((t - 1.75) / 0.45, 0.0), 1.0)

    if n1_wipe_prog > 0.0:
        img = wipe_fill_rect(img, n1_x0, n1_y0, n1_x1, n1_y1, COLOR_LIGHT_GRAY, n1_wipe_prog)
        draw = ImageDraw.Draw(img)

    if n1_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, n1_x0, n1_y0, n1_x1, n1_y1, progress=n1_ink_prog, color=COLOR_INK, width=3.8)

    if n1_ink_prog >= 0.8:
        # Icon: Root Prim Hierarchy Disc
        draw.ellipse([240, 390, 340, 440], fill=COLOR_SLATE, outline=COLOR_INK, width=3)
        draw.text((272, 404), "ROOT", fill=COLOR_WHITE, font=FONTS["badge"])

        draw.text((140, 470), "STAGE ROOT (WORLD)", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((130, 520), "def Xform \"World\"", fill=COLOR_SLATE, font=FONTS["code"])
        draw.text((130, 550), "• Session Layer Active", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((130, 580), "• Root Layer Stack", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((130, 610), "• Memory: 14.2 MB", fill=COLOR_TERRACOTTA, font=FONTS["box_text"])
        draw.text((130, 640), "• Traversal: PrimIndex OK", fill=COLOR_SLATE, font=FONTS["box_text"])

    # Arrow 1: Root -> Deferred Architecture Payload (2.2s -> 2.7s)
    a1_prog = min(max((t - 2.2) / 0.5, 0.0), 1.0)
    if a1_prog > 0.0:
        draw_curved_arrow(draw, (485, 540), (680, 540), (580, 510), progress=a1_prog, color=COLOR_INK, width=4.0)
        if a1_prog > 0.6:
            draw.text((515, 485), "payload arc", fill=COLOR_TERRACOTTA, font=FONTS["badge"])
            draw.text((505, 555), "defers subtree", fill=COLOR_SLATE, font=FONTS["badge"])

    # Node 2: Deferred Architecture Payload (Center)
    # Timeline: Ink: 2.7s -> 3.7s, 250ms gap: 3.7s -> 3.95s, Wipe: 3.95s -> 4.5s
    n2_x0, n2_y0, n2_x1, n2_y1 = 690, 320, 1190, 760
    n2_ink_prog = min(max((t - 2.7) / 1.0, 0.0), 1.0)
    n2_wipe_prog = min(max((t - 3.95) / 0.55, 0.0), 1.0)

    if n2_wipe_prog > 0.0:
        # Dual-tone wipe: Terracotta header banner + Soft Sky Blue body
        img = wipe_fill_rect(img, n2_x0, n2_y0, n2_x1, n2_y1, (245, 248, 252), n2_wipe_prog)
        draw = ImageDraw.Draw(img)

    if n2_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, n2_x0, n2_y0, n2_x1, n2_y1, progress=n2_ink_prog, color=COLOR_INK, width=4.0)

    if n2_ink_prog >= 0.7:
        # Architectural facade icon
        draw.polygon([(940, 345), (840, 395), (1040, 395)], fill=COLOR_TERRACOTTA, outline=COLOR_INK)
        # Portico columns
        for col_x in [860, 910, 960, 1010]:
            draw.rectangle([col_x, 395, col_x + 15, 435], fill=COLOR_SKY_BLUE, outline=COLOR_INK, width=2)

        draw.text((725, 455), "DEFERRED ARCHITECTURE PAYLOAD", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((720, 500), "payload = @./palazzo_venue.usd@", fill=COLOR_TERRACOTTA, font=FONTS["code"])
        draw.text((720, 540), "• Full BIM / CAD Geometry & Meshes", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((720, 575), "• Unloaded on Stage Open: 0 MB VRAM", fill=COLOR_NVIDIA_GREEN, font=FONTS["box_text"])
        draw.text((720, 610), "• Dynamic Spatial Bounding Box", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((720, 645), "• Memory Footprint: 42 MB (vs 1.2 GB)", fill=COLOR_TERRACOTTA, font=FONTS["box_text"])
        draw.text((720, 680), "• Savings: 96.5% Memory Reduction", fill=COLOR_NVIDIA_GREEN, font=FONTS["box_text"])

    # Branching Arrows: Payload -> Auditorium (top right) & Banquet (bottom right) (4.5s -> 5.0s)
    a2_prog = min(max((t - 4.5) / 0.5, 0.0), 1.0)
    if a2_prog > 0.0:
        # Arrow to Auditorium
        draw_curved_arrow(draw, (1195, 490), (1390, 360), (1280, 400), progress=a2_prog, color=COLOR_INK, width=3.8)
        # Arrow to Banquet
        draw_curved_arrow(draw, (1195, 590), (1390, 720), (1280, 680), progress=a2_prog, color=COLOR_INK, width=3.8)
        if a2_prog > 0.5:
            draw.text((1220, 395), "variantSet", fill=COLOR_SKY_BLUE, font=FONTS["badge"])
            draw.text((1220, 675), "variantSet", fill=COLOR_SKY_BLUE, font=FONTS["badge"])

    # Node 3A: Variant "Auditorium" (Top Right)
    # Timeline: Ink: 5.0s -> 5.7s, 250ms gap: 5.7s -> 5.95s, Wipe: 5.95s -> 6.4s
    v1_x0, v1_y0, v1_x1, v1_y1 = 1400, 230, 1850, 490
    v1_ink_prog = min(max((t - 5.0) / 0.7, 0.0), 1.0)
    v1_wipe_prog = min(max((t - 5.95) / 0.45, 0.0), 1.0)

    if v1_wipe_prog > 0.0:
        img = wipe_fill_rect(img, v1_x0, v1_y0, v1_x1, v1_y1, (238, 248, 225), v1_wipe_prog)
        draw = ImageDraw.Draw(img)

    if v1_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, v1_x0, v1_y0, v1_x1, v1_y1, progress=v1_ink_prog, color=COLOR_INK, width=3.6)

    if v1_ink_prog >= 0.7:
        # Green active badge
        draw.rounded_rectangle([v1_x0 + 15, v1_y0 + 15, v1_x0 + 130, v1_y0 + 42], radius=6, fill=COLOR_NVIDIA_GREEN)
        draw.text((v1_x0 + 25, v1_y0 + 19), "ACTIVE SET", fill=COLOR_WHITE, font=FONTS["badge"])

        draw.text((v1_x0 + 15, v1_y0 + 55), "VARIANT: \"Auditorium\"", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((v1_x0 + 15, v1_y0 + 95), "• 450 Stepped Tiered Seats", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((v1_x0 + 15, v1_y0 + 125), "• Center Keynote Stage & Lectern", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((v1_x0 + 15, v1_y0 + 155), "• Acoustic Rig & Dynamic Spotlights", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((v1_x0 + 15, v1_y0 + 185), "• Render Drawcalls: 1,420", fill=COLOR_SLATE, font=FONTS["code"])

    # Node 3B: Variant "Banquet" (Bottom Right)
    # Timeline: Ink: 5.3s -> 6.0s, 250ms gap: 6.0s -> 6.25s, Wipe: 6.25s -> 6.7s
    v2_x0, v2_y0, v2_x1, v2_y1 = 1400, 590, 1850, 850
    v2_ink_prog = min(max((t - 5.3) / 0.7, 0.0), 1.0)
    v2_wipe_prog = min(max((t - 6.25) / 0.45, 0.0), 1.0)

    if v2_wipe_prog > 0.0:
        img = wipe_fill_rect(img, v2_x0, v2_y0, v2_x1, v2_y1, (254, 243, 235), v2_wipe_prog)
        draw = ImageDraw.Draw(img)

    if v2_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, v2_x0, v2_y0, v2_x1, v2_y1, progress=v2_ink_prog, color=COLOR_INK, width=3.6)

    if v2_ink_prog >= 0.7:
        # Terracotta standby badge
        draw.rounded_rectangle([v2_x0 + 15, v2_y0 + 15, v2_x0 + 140, v2_y0 + 42], radius=6, fill=COLOR_TERRACOTTA)
        draw.text((v2_x0 + 25, v2_y0 + 19), "STANDBY SET", fill=COLOR_WHITE, font=FONTS["badge"])

        draw.text((v2_x0 + 15, v2_y0 + 55), "VARIANT: \"Banquet\"", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((v2_x0 + 15, v2_y0 + 95), "• 38 Round Gala Dining Tables", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((v2_x0 + 15, v2_y0 + 125), "• Table Linens & Centerpieces", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((v2_x0 + 15, v2_y0 + 155), "• Catering Buffet & Wine Station", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((v2_x0 + 15, v2_y0 + 185), "• Switch Latency: 4.8 ms (Zero Reload)", fill=COLOR_TERRACOTTA, font=FONTS["code"])

    # Footer Takeaway Caption (6.8s -> 7.4s)
    footer_prog = min(max((t - 6.8) / 0.6, 0.0), 1.0)
    if footer_prog > 0.0:
        footer_text = "PAYLOADS PREVENT DUPLICATE GEOMETRY"
        fbbox = FONTS["footer"].getbbox(footer_text)
        ftw = fbbox[2] - fbbox[0]
        ftx = (WIDTH - ftw) // 2
        fty = 955

        # Marker highlight bar behind footer
        bar_pts = [(ftx - 30, fty + 22), (ftx + ftw + 30, fty + 22)]
        draw_organic_polyline(draw, bar_pts, progress=footer_prog, color=(254, 235, 175), base_width=32.0)

        draw.text((ftx, fty), footer_text, fill=COLOR_INK, font=FONTS["footer"])

        sub_footer = "LIVRPS RESOLUTION • 96.5% RAM REDUCTION • NON-DESTRUCTIVE SCENE VARIANTS"
        sf_bbox = FONTS["sub"].getbbox(sub_footer)
        sftx = (WIDTH - (sf_bbox[2] - sf_bbox[0])) // 2
        draw.text((sftx, fty + 48), sub_footer, fill=COLOR_SLATE, font=FONTS["sub"])

    return img


# ==============================================================================
# ANIMATION 2: Earth-2 Whiteboard Explainer
# ==============================================================================
def render_earth2_frame(frame_idx):
    t = frame_idx / float(FPS)
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # 1. Header (0.0s -> 0.7s)
    header_prog = min(max(t / 0.6, 0.0), 1.0)
    if header_prog > 0.0:
        header_text = "EARTH-2 CONVECTIVE PREDICTION"
        sub_text = "GLOBAL-TO-MESOSCALE AI NUMERICAL WEATHER PREDICTION PIPELINE"
        bbox = FONTS["header"].getbbox(header_text)
        tw = bbox[2] - bbox[0]
        tx = (WIDTH - tw) // 2
        ty = 45
        draw.text((tx, ty), header_text, fill=COLOR_INK, font=FONTS["header"])

        # Marker underline
        line_pts = [(tx - 20, ty + 58), (tx + tw + 20, ty + 58)]
        draw_organic_polyline(draw, line_pts, progress=header_prog, color=COLOR_SKY_BLUE, base_width=4.5)

        sub_bbox = FONTS["sub"].getbbox(sub_text)
        sub_tx = (WIDTH - (sub_bbox[2] - sub_bbox[0])) // 2
        draw.text((sub_tx, ty + 68), sub_text, fill=COLOR_SLATE, font=FONTS["sub"])

    # Node 1: ERA5 Initial State (Left)
    # Timeline: Ink: 0.6s -> 1.5s, 250ms gap: 1.5s -> 1.75s, Wipe: 1.75s -> 2.2s
    n1_x0, n1_y0, n1_x1, n1_y1 = 100, 340, 500, 740
    n1_ink_prog = min(max((t - 0.6) / 0.9, 0.0), 1.0)
    n1_wipe_prog = min(max((t - 1.75) / 0.45, 0.0), 1.0)

    if n1_wipe_prog > 0.0:
        img = wipe_fill_rect(img, n1_x0, n1_y0, n1_x1, n1_y1, (240, 248, 255), n1_wipe_prog)
        draw = ImageDraw.Draw(img)

    if n1_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, n1_x0, n1_y0, n1_x1, n1_y1, progress=n1_ink_prog, color=COLOR_INK, width=3.8)

    if n1_ink_prog >= 0.7:
        # Globe icon
        draw.ellipse([250, 365, 350, 465], fill=COLOR_SKY_BLUE, outline=COLOR_INK, width=3)
        draw.arc([265, 365, 335, 465], 0, 360, fill=COLOR_WHITE, width=2)
        draw.line([(250, 415), (350, 415)], fill=COLOR_WHITE, width=2)

        draw.text((140, 485), "ERA5 INITIAL STATE", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((130, 525), "ECMWF Global Reanalysis", fill=COLOR_SKY_BLUE, font=FONTS["code"])
        draw.text((130, 560), "• Spatial Resolution: 0.25° (~28 km)", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((130, 595), "• 73 Atmospheric Pressure Levels", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((130, 630), "• Prognostic State: Z500, T850, U/V", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((130, 665), "• Latency: Multi-Hour Reanalysis", fill=COLOR_TERRACOTTA, font=FONTS["box_text"])

    # Arrow 1: ERA5 -> AFNO FourCastNet (2.2s -> 2.7s)
    a1_prog = min(max((t - 2.2) / 0.5, 0.0), 1.0)
    if a1_prog > 0.0:
        draw_curved_arrow(draw, (505, 540), (690, 540), (595, 510), progress=a1_prog, color=COLOR_INK, width=4.0)
        if a1_prog > 0.6:
            draw.text((535, 485), "Spherical FFT", fill=COLOR_NVIDIA_GREEN, font=FONTS["badge"])
            draw.text((530, 555), "100x Faster", fill=COLOR_SLATE, font=FONTS["badge"])

    # Node 2: AFNO FourCastNet (Center)
    # Timeline: Ink: 2.7s -> 3.7s, 250ms gap: 3.7s -> 3.95s, Wipe: 3.95s -> 4.5s
    n2_x0, n2_y0, n2_x1, n2_y1 = 700, 310, 1200, 770
    n2_ink_prog = min(max((t - 2.7) / 1.0, 0.0), 1.0)
    n2_wipe_prog = min(max((t - 3.95) / 0.55, 0.0), 1.0)

    if n2_wipe_prog > 0.0:
        img = wipe_fill_rect(img, n2_x0, n2_y0, n2_x1, n2_y1, (244, 252, 235), n2_wipe_prog)
        draw = ImageDraw.Draw(img)

    if n2_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, n2_x0, n2_y0, n2_x1, n2_y1, progress=n2_ink_prog, color=COLOR_INK, width=4.0)

    if n2_ink_prog >= 0.7:
        # NVIDIA Chip badge icon
        draw.rectangle([900, 335, 1000, 420], fill=COLOR_NVIDIA_GREEN, outline=COLOR_INK, width=3)
        draw.text((915, 365), "NVIDIA", fill=COLOR_WHITE, font=FONTS["badge"])
        draw.text((922, 385), "AFNO", fill=COLOR_WHITE, font=FONTS["badge"])

        draw.text((740, 445), "AFNO FOURCASTNET", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((725, 490), "Adaptive Fourier Neural Operator", fill=COLOR_NVIDIA_GREEN, font=FONTS["code"])
        draw.text((725, 530), "• Continuous Spectral Convolution", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((725, 565), "• Autoregressive 72h Step Rollout", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((725, 600), "• Inference Time: 0.84s (A100 GPU)", fill=COLOR_NVIDIA_GREEN, font=FONTS["box_text"])
        draw.text((725, 635), "• Energy Efficiency: 10,000x NWP", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((725, 670), "• Global Atmospheric Prognosis", fill=COLOR_SLATE, font=FONTS["box_text"])

    # Arrow 2: AFNO -> Calabria High-Res Cell (4.5s -> 5.0s)
    a2_prog = min(max((t - 4.5) / 0.5, 0.0), 1.0)
    if a2_prog > 0.0:
        draw_curved_arrow(draw, (1205, 540), (1390, 540), (1295, 510), progress=a2_prog, color=COLOR_INK, width=4.0)
        if a2_prog > 0.6:
            draw.text((1225, 485), "Super-Res", fill=COLOR_TERRACOTTA, font=FONTS["badge"])
            draw.text((1220, 555), "Downscaling", fill=COLOR_SLATE, font=FONTS["badge"])

    # Node 3: Calabria High-Res Convective Cell (Right)
    # Timeline: Ink: 5.0s -> 6.0s, 250ms gap: 6.0s -> 6.25s, Wipe: 6.25s -> 6.8s
    n3_x0, n3_y0, n3_x1, n3_y1 = 1400, 310, 1850, 770
    n3_ink_prog = min(max((t - 5.0) / 1.0, 0.0), 1.0)
    n3_wipe_prog = min(max((t - 6.25) / 0.55, 0.0), 1.0)

    if n3_wipe_prog > 0.0:
        img = wipe_fill_rect(img, n3_x0, n3_y0, n3_x1, n3_y1, (254, 245, 238), n3_wipe_prog)
        draw = ImageDraw.Draw(img)

    if n3_ink_prog > 0.0:
        draw_hand_drawn_rect(draw, n3_x0, n3_y0, n3_x1, n3_y1, progress=n3_ink_prog, color=COLOR_INK, width=4.0)

    if n3_ink_prog >= 0.7:
        # Calabria Storm Cloud & Convective Cell icon
        draw.ellipse([1560, 340, 1640, 390], fill=COLOR_TERRACOTTA, outline=COLOR_INK, width=2)
        draw.ellipse([1610, 330, 1700, 395], fill=COLOR_SLATE, outline=COLOR_INK, width=2)
        draw.polygon([(1625, 395), (1610, 420), (1630, 420), (1615, 445)], fill=COLOR_NVIDIA_GREEN)

        draw.text((1425, 455), "CALABRIA CONVECTIVE CELL", fill=COLOR_INK, font=FONTS["box_title"])
        draw.text((1420, 495), "7.04 km Mesoscale Resolution", fill=COLOR_TERRACOTTA, font=FONTS["code"])
        draw.text((1420, 535), "• Domain: 38.0°-40.2°N, 15.5°-17.5°E", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((1420, 570), "• Convective Displacement: 7.04 km", fill=COLOR_NVIDIA_GREEN, font=FONTS["box_text"])
        draw.text((1420, 605), "• Peak Precip Forecast: 62.0 mm", fill=COLOR_TERRACOTTA, font=FONTS["box_text"])
        draw.text((1420, 640), "• Domain MAE: 1.42 mm (vs 2.85)", fill=COLOR_INK, font=FONTS["box_text"])
        draw.text((1420, 675), "• Ground Truth Match: 95.4%", fill=COLOR_NVIDIA_GREEN, font=FONTS["box_text"])

    # Footer Takeaway Caption (6.8s -> 7.4s)
    footer_prog = min(max((t - 6.8) / 0.6, 0.0), 1.0)
    if footer_prog > 0.0:
        footer_text = "7.04 KM LOCALIZED SPATIAL ACCURACY"
        fbbox = FONTS["footer"].getbbox(footer_text)
        ftw = fbbox[2] - fbbox[0]
        ftx = (WIDTH - ftw) // 2
        fty = 955

        bar_pts = [(ftx - 30, fty + 22), (ftx + ftw + 30, fty + 22)]
        draw_organic_polyline(draw, bar_pts, progress=footer_prog, color=(210, 240, 255), base_width=32.0)

        draw.text((ftx, fty), footer_text, fill=COLOR_INK, font=FONTS["footer"])

        sub_footer = "AFNO NEURAL OPERATOR • 0.84s GPU LATENCY • RAPID FLOOD HAZARD EARLY WARNING"
        sf_bbox = FONTS["sub"].getbbox(sub_footer)
        sftx = (WIDTH - (sf_bbox[2] - sf_bbox[0])) // 2
        draw.text((sftx, fty + 48), sub_footer, fill=COLOR_SLATE, font=FONTS["sub"])

    return img


def encode_video(render_frame_fn, output_mp4_path, keyframe_png_path=None):
    os.makedirs(os.path.dirname(output_mp4_path), exist_ok=True)
    if keyframe_png_path:
        os.makedirs(os.path.dirname(keyframe_png_path), exist_ok=True)

    print(f"[Renderer] Encoding {output_mp4_path} ({TOTAL_FRAMES} frames @ {FPS} fps)...")

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        output_mp4_path
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for i in range(TOTAL_FRAMES):
        frame = render_frame_fn(i)
        # Capture keyframe near the end when diagram is fully revealed
        if keyframe_png_path and i == int(FPS * (DURATION_SEC - 0.5)):
            frame.save(keyframe_png_path, "PNG")
            print(f"  -> Saved keyframe card: {keyframe_png_path}")

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed with exit code {proc.returncode}")

    file_size_kb = os.path.getsize(output_mp4_path) / 1024.0
    print(f"  -> Successfully generated {output_mp4_path} ({file_size_kb:.1f} KB)")


def main():
    print("=== UMATTR Whiteboard Animation Suite Starting ===")

    # 1. OpenUSD Whiteboard Explainer
    openusd_mp4 = "reports/videos/openusd_whiteboard_explainer.mp4"
    openusd_keyframe = "reports/figures/openusd_whiteboard_keyframe.png"
    encode_video(render_openusd_frame, openusd_mp4, openusd_keyframe)

    # 2. Earth-2 Whiteboard Explainer
    earth2_mp4 = "reports/videos/earth2_whiteboard_explainer.mp4"
    earth2_keyframe = "reports/figures/earth2_whiteboard_keyframe.png"
    encode_video(render_earth2_frame, earth2_mp4, earth2_keyframe)

    print("=== UMATTR Whiteboard Animations Completed Successfully! ===")


if __name__ == "__main__":
    main()
