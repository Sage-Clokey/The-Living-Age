"""Generate stylized portrait placeholders for 5 Austrian economists."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Wedge, Arc
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Palette
BG = '#0a120a'
GREENS = ['#1b4332', '#2d6a4f', '#40916c', '#52b788', '#95d5b2']
GOLD = '#e9c46a'
SUBTITLE = '#95d5b2'

DPI = 300
W, H = 400/DPI, 500/DPI  # inches at 300 DPI -> 400x500 px


def make_fig():
    fig, ax = plt.subplots(1, 1, figsize=(W, H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def add_text(ax, name, years, subtitle):
    ax.text(0.5, 0.10, name, ha='center', va='center',
            fontsize=7, fontweight='bold', color=GOLD,
            fontfamily='serif')
    ax.text(0.5, 0.055, years, ha='center', va='center',
            fontsize=4, color='#888888', fontfamily='serif')
    ax.text(0.5, 0.015, subtitle, ha='center', va='center',
            fontsize=4, fontstyle='italic', color=SUBTITLE,
            fontfamily='serif')


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=DPI, bbox_inches='tight',
                pad_inches=0.02, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {name}")


# ─── 1. MENGER — Spiral / Organic Web ───────────────────────────────
def menger():
    fig, ax = make_fig()
    # Head: large circle
    ax.add_patch(Circle((0.5, 0.58), 0.18, fc=GREENS[1], ec=GREENS[3], lw=0.5))
    # Shoulders: wide ellipse
    ax.add_patch(patches.Ellipse((0.5, 0.33), 0.55, 0.22, fc=GREENS[0], ec=GREENS[2], lw=0.5))
    # Face features: geometric
    ax.add_patch(Circle((0.42, 0.61), 0.025, fc=GREENS[3], ec='none'))
    ax.add_patch(Circle((0.58, 0.61), 0.025, fc=GREENS[3], ec='none'))
    # Nose line
    ax.plot([0.5, 0.5], [0.57, 0.52], color=GREENS[3], lw=0.8)
    # Mouth
    t = np.linspace(-0.4, 0.4, 30)
    ax.plot(0.5 + t*0.1, 0.49 + np.cos(t*3)*0.008, color=GREENS[3], lw=0.6)
    # Hair/top
    for angle in np.linspace(0.3, 2.85, 12):
        x = 0.5 + 0.19 * np.cos(angle)
        y = 0.58 + 0.19 * np.sin(angle)
        ax.add_patch(Circle((x, y), 0.025, fc=GREENS[2], ec='none', alpha=0.7))

    # ICON: Spiral (spontaneous order)
    theta = np.linspace(0, 4*np.pi, 200)
    r = 0.01 + 0.008 * theta
    sx = 0.82 + r * np.cos(theta) * 0.6
    sy = 0.85 + r * np.sin(theta) * 0.6
    ax.plot(sx, sy, color=GREENS[4], lw=0.6, alpha=0.9)
    # Small web lines radiating
    for a in np.linspace(0, 2*np.pi, 8, endpoint=False):
        ax.plot([0.82, 0.82 + 0.07*np.cos(a)], [0.85, 0.85 + 0.07*np.sin(a)],
                color=GREENS[3], lw=0.3, alpha=0.5)

    add_text(ax, 'CARL MENGER', '1840 – 1921', 'Spontaneous Order')
    save(fig, 'economist_menger.png')


# ─── 2. MISES — Broken Calculator / X ───────────────────────────────
def mises():
    fig, ax = make_fig()
    # Head: rounded rectangle
    ax.add_patch(FancyBboxPatch((0.32, 0.46), 0.36, 0.28,
                                boxstyle="round,pad=0.04", fc=GREENS[1], ec=GREENS[3], lw=0.5))
    # Shoulders: trapezoid
    trap = Polygon([(0.2, 0.3), (0.8, 0.3), (0.7, 0.46), (0.3, 0.46)],
                   closed=True, fc=GREENS[0], ec=GREENS[2], lw=0.5)
    ax.add_patch(trap)
    # Eyes: rectangles
    ax.add_patch(patches.Rectangle((0.38, 0.61), 0.06, 0.03, fc=GREENS[3], ec='none'))
    ax.add_patch(patches.Rectangle((0.56, 0.61), 0.06, 0.03, fc=GREENS[3], ec='none'))
    # Glasses bridge
    ax.plot([0.44, 0.56], [0.625, 0.625], color=GREENS[3], lw=0.5)
    # Nose
    ax.plot([0.5, 0.48, 0.52], [0.59, 0.54, 0.54], color=GREENS[3], lw=0.6)
    # Mouth: straight serious line
    ax.plot([0.43, 0.57], [0.50, 0.50], color=GREENS[3], lw=0.7)
    # Hair: angular blocks on top
    for x in np.linspace(0.34, 0.64, 7):
        ax.add_patch(patches.Rectangle((x, 0.72), 0.04, 0.04,
                                        fc=GREENS[2], ec='none', alpha=0.8))

    # ICON: Broken calculator with X
    cx, cy = 0.83, 0.85
    ax.add_patch(FancyBboxPatch((cx-0.04, cy-0.05), 0.08, 0.10,
                                boxstyle="round,pad=0.005", fc=GREENS[0], ec=GREENS[3], lw=0.4))
    # Screen
    ax.add_patch(patches.Rectangle((cx-0.03, cy+0.01), 0.06, 0.025, fc=GREENS[1], ec=GREENS[3], lw=0.3))
    # X over it
    ax.plot([cx-0.04, cx+0.04], [cy-0.05, cy+0.05], color='#c0392b', lw=1.0, alpha=0.8)
    ax.plot([cx-0.04, cx+0.04], [cy+0.05, cy-0.05], color='#c0392b', lw=1.0, alpha=0.8)

    add_text(ax, 'LUDWIG VON MISES', '1881 – 1973', 'The Calculation Problem')
    save(fig, 'economist_mises.png')


# ─── 3. HAYEK — Distributed Network ─────────────────────────────────
def hayek():
    fig, ax = make_fig()
    # Head: diamond/rotated square
    diamond = Polygon([(0.5, 0.78), (0.68, 0.58), (0.5, 0.40), (0.32, 0.58)],
                      closed=True, fc=GREENS[1], ec=GREENS[3], lw=0.5)
    ax.add_patch(diamond)
    # Shoulders: wide triangle
    shoulders = Polygon([(0.15, 0.28), (0.85, 0.28), (0.62, 0.42), (0.38, 0.42)],
                        closed=True, fc=GREENS[0], ec=GREENS[2], lw=0.5)
    ax.add_patch(shoulders)
    # Eyes: triangular
    ax.add_patch(Polygon([(0.40, 0.62), (0.46, 0.62), (0.43, 0.58)],
                         fc=GREENS[3], ec='none'))
    ax.add_patch(Polygon([(0.54, 0.62), (0.60, 0.62), (0.57, 0.58)],
                         fc=GREENS[3], ec='none'))
    # Nose
    ax.plot([0.5, 0.5], [0.56, 0.50], color=GREENS[3], lw=0.7)
    # Mouth
    ax.plot([0.44, 0.56], [0.47, 0.47], color=GREENS[3], lw=0.6)
    # Crown details
    for i, x in enumerate(np.linspace(0.40, 0.60, 5)):
        h = 0.78 + (0.03 if i % 2 == 0 else 0.015)
        ax.add_patch(Polygon([(x-0.02, 0.76), (x+0.02, 0.76), (x, h)],
                             fc=GREENS[2], ec='none', alpha=0.8))

    # ICON: Distributed network (scattered dots with connections)
    np.random.seed(42)
    nx_pts, ny_pts = 8, 8
    px = 0.82 + np.random.randn(nx_pts) * 0.04
    py = 0.85 + np.random.randn(ny_pts) * 0.04
    for i in range(nx_pts):
        ax.add_patch(Circle((px[i], py[i]), 0.008, fc=GREENS[4], ec='none'))
        for j in range(i+1, nx_pts):
            d = np.sqrt((px[i]-px[j])**2 + (py[i]-py[j])**2)
            if d < 0.06:
                ax.plot([px[i], px[j]], [py[i], py[j]], color=GREENS[3], lw=0.3, alpha=0.6)

    add_text(ax, 'FRIEDRICH HAYEK', '1899 – 1992', 'The Knowledge Problem')
    save(fig, 'economist_hayek.png')


# ─── 4. ROTHBARD — Cracking Pillar ──────────────────────────────────
def rothbard():
    fig, ax = make_fig()
    # Head: hexagonal
    angles = np.linspace(0, 2*np.pi, 7)[:-1] + np.pi/6
    hex_pts = [(0.5 + 0.17*np.cos(a), 0.58 + 0.17*np.sin(a)) for a in angles]
    ax.add_patch(Polygon(hex_pts, closed=True, fc=GREENS[1], ec=GREENS[3], lw=0.5))
    # Shoulders: curved via ellipse
    ax.add_patch(patches.Ellipse((0.5, 0.33), 0.60, 0.20, fc=GREENS[0], ec=GREENS[2], lw=0.5))
    # Eyes: circles with pupils
    for ex in [0.43, 0.57]:
        ax.add_patch(Circle((ex, 0.61), 0.03, fc=GREENS[3], ec='none'))
        ax.add_patch(Circle((ex, 0.61), 0.012, fc=GREENS[0], ec='none'))
    # Eyebrows
    ax.plot([0.38, 0.47], [0.66, 0.65], color=GREENS[3], lw=0.7)
    ax.plot([0.53, 0.62], [0.65, 0.66], color=GREENS[3], lw=0.7)
    # Nose
    ax.plot([0.5, 0.48], [0.58, 0.53], color=GREENS[3], lw=0.6)
    ax.plot([0.48, 0.52], [0.53, 0.53], color=GREENS[3], lw=0.6)
    # Mouth: slight smile
    t = np.linspace(-1, 1, 30)
    ax.plot(0.5 + t*0.06, 0.49 - t**2 * 0.01, color=GREENS[3], lw=0.6)
    # Hair patches
    for a in np.linspace(np.pi*0.3, np.pi*0.7, 6):
        x = 0.5 + 0.19*np.cos(a)
        y = 0.58 + 0.19*np.sin(a)
        ax.add_patch(patches.Rectangle((x-0.02, y), 0.04, 0.03,
                                        angle=np.degrees(a)-90,
                                        fc=GREENS[2], ec='none', alpha=0.8))

    # ICON: Cracking pillar
    px, py = 0.83, 0.82
    # Pillar body
    ax.add_patch(patches.Rectangle((px-0.02, py-0.06), 0.04, 0.12, fc=GREENS[2], ec=GREENS[3], lw=0.3))
    # Capital and base
    ax.add_patch(patches.Rectangle((px-0.03, py+0.06), 0.06, 0.015, fc=GREENS[3], ec='none'))
    ax.add_patch(patches.Rectangle((px-0.03, py-0.065), 0.06, 0.015, fc=GREENS[3], ec='none'))
    # Cracks
    crack_y = np.array([py-0.03, py-0.01, py+0.01, py+0.03, py+0.05])
    crack_x = np.array([px-0.01, px+0.015, px-0.01, px+0.01, px-0.005])
    ax.plot(crack_x, crack_y, color=BG, lw=0.8)
    # Small debris
    for dx, dy in [(-0.04, -0.02), (0.05, 0.01), (-0.03, 0.04)]:
        ax.add_patch(patches.Rectangle((px+dx, py+dy), 0.01, 0.008,
                                        angle=30, fc=GREENS[2], ec='none', alpha=0.6))

    add_text(ax, 'MURRAY ROTHBARD', '1926 – 1995', 'Fragility of Centralization')
    save(fig, 'economist_rothbard.png')


# ─── 5. KIRZNER — Magnifying Glass / Lightbulb ──────────────────────
def kirzner():
    fig, ax = make_fig()
    # Head: oval/egg shape via ellipse
    ax.add_patch(patches.Ellipse((0.5, 0.60), 0.30, 0.36, fc=GREENS[1], ec=GREENS[3], lw=0.5))
    # Shoulders
    shoulders = Polygon([(0.20, 0.28), (0.80, 0.28), (0.65, 0.42), (0.35, 0.42)],
                        closed=True, fc=GREENS[0], ec=GREENS[2], lw=0.5)
    ax.add_patch(shoulders)
    # Eyes: half-circle (alert, searching)
    for ex in [0.43, 0.57]:
        theta = np.linspace(0, np.pi, 30)
        ex_pts = ex + 0.03*np.cos(theta)
        ey_pts = 0.63 + 0.02*np.sin(theta)
        ax.fill(ex_pts, ey_pts, fc=GREENS[3], ec='none')
        ax.add_patch(Circle((ex, 0.63), 0.01, fc=GREENS[4], ec='none'))
    # Nose
    ax.plot([0.5, 0.49, 0.51], [0.59, 0.54, 0.54], color=GREENS[3], lw=0.6)
    # Mouth: open, excited
    theta = np.linspace(np.pi, 2*np.pi, 30)
    mx = 0.5 + 0.04*np.cos(theta)
    my = 0.50 + 0.015*np.sin(theta)
    ax.fill(mx, my, fc=GREENS[3], ec='none')
    # Hat / Kippah
    theta = np.linspace(0, np.pi, 30)
    hx = 0.5 + 0.12*np.cos(theta)
    hy = 0.76 + 0.04*np.sin(theta)
    ax.fill(np.append(hx, hx[0]), np.append(hy, hy[0]), fc=GREENS[2], ec=GREENS[3], lw=0.4)
    # Beard suggestion
    for i in range(8):
        bx = 0.42 + i*0.02
        ax.plot([bx, bx + 0.003], [0.47, 0.43], color=GREENS[2], lw=0.4, alpha=0.7)

    # ICON: Magnifying glass with lightbulb inside
    ix, iy = 0.83, 0.85
    # Glass circle
    theta = np.linspace(0, 2*np.pi, 50)
    ax.plot(ix + 0.04*np.cos(theta), iy + 0.04*np.sin(theta), color=GREENS[4], lw=0.8)
    # Handle
    ax.plot([ix+0.028, ix+0.055], [iy-0.028, iy-0.055], color=GREENS[3], lw=1.2)
    # Lightbulb inside
    bulb_t = np.linspace(0, np.pi, 30)
    bx = ix + 0.02*np.cos(bulb_t)
    by = iy + 0.005 + 0.02*np.sin(bulb_t)
    ax.plot(bx, by, color=GOLD, lw=0.6)
    ax.plot([ix-0.02, ix-0.015], [iy+0.005, iy-0.01], color=GOLD, lw=0.6)
    ax.plot([ix+0.02, ix+0.015], [iy+0.005, iy-0.01], color=GOLD, lw=0.6)
    ax.plot([ix-0.015, ix+0.015], [iy-0.01, iy-0.01], color=GOLD, lw=0.5)
    # Rays
    for a in np.linspace(0.3, 2.8, 5):
        ax.plot([ix + 0.025*np.cos(a), ix + 0.035*np.cos(a)],
                [iy + 0.005 + 0.025*np.sin(a), iy + 0.005 + 0.035*np.sin(a)],
                color=GOLD, lw=0.3, alpha=0.7)

    add_text(ax, 'ISRAEL KIRZNER', '1930 – present', 'Entrepreneurial Discovery')
    save(fig, 'economist_kirzner.png')


if __name__ == '__main__':
    print("Generating economist portraits...")
    menger()
    mises()
    hayek()
    rothbard()
    kirzner()
    print("Done.")
