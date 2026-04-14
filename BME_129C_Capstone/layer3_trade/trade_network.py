"""
Cross-Species Trade Network — Layer 3: Comparative Advantage
=============================================================
Maps gene transferability across organisms as an international trade network.

Each organism is a nation. Each gene is a good. The question:
does cross-species gene exchange follow free trade economics?

Trade friction = codon distance + regulatory barriers + pathway conflicts
Comparative advantage = each organism's unique biological capabilities
Trade network = which organisms can exchange genes most easily

Foundation (imports from adaptive_Automation):
    - codon.py → RSCU tables = "currency exchange rates"
    - regulatory.py → cross-kingdom detection = "legal frameworks"
    - species_search.py → CAPABILITY_MAP = comparative advantage catalog
    - genomic_part.py → compatibility_distance() = trade friction

References:
    - Ricardo, "On the Principles of Political Economy and Taxation," 1817
    - Tinbergen, "Shaping the World Economy," 1962 (gravity model)
    - Sharp & Li, "The codon adaptation index," NAR 1987
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import sys
import math

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Import from adaptive_Automation
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "adaptive_Automation"))

try:
    from compatibility.codon import REFERENCE_RSCU, compute_cai
    from compatibility.regulatory import cell_type, is_cross_kingdom
    from retrieval.species_search import CAPABILITY_MAP
    HAS_ADAPTIVE = True
    print(f"[trade] Loaded {len(REFERENCE_RSCU)} RSCU tables from adaptive_Automation")
except ImportError:
    HAS_ADAPTIVE = False
    print("[trade] Warning: could not import from adaptive_Automation. Using built-in data.")
    REFERENCE_RSCU = {}
    CAPABILITY_MAP = {}

# Aesthetic
SPIRAL_GREEN = "#2d6a4f"
SPIRAL_MID   = "#52b788"
SPIRAL_LIGHT = "#95d5b2"
GOLD         = "#e9c46a"
RED          = "#e63946"
BLUE         = "#4361ee"
BACKGROUND   = "#0d1117"
PANEL_BG     = "#161b22"
TEXT_MAIN     = "#e6edf3"
TEXT_DIM      = "#8b949e"

FIGURES_DIR = Path(__file__).resolve().parent.parent / "paper" / "figures"


# ---------------------------------------------------------------------------
# Extended RSCU tables (organisms not in adaptive_Automation)
# ---------------------------------------------------------------------------
# Source: Kazusa Codon Usage Database + literature

EXTENDED_RSCU = {
    # E. coli K-12 — the model prokaryote (~51% GC)
    "e_coli": {
        "TTT": 0.58, "TTC": 1.42, "TTA": 0.22, "TTG": 0.22,
        "CTT": 0.20, "CTC": 0.18, "CTA": 0.07, "CTG": 5.11,
        "ATT": 0.98, "ATC": 1.70, "ATA": 0.14, "ATG": 1.00,
        "GTT": 0.60, "GTC": 0.44, "GTA": 0.28, "GTG": 2.68,
        "TCT": 0.56, "TCC": 0.88, "TCA": 0.24, "TCG": 0.24,
        "CCT": 0.24, "CCC": 0.16, "CCA": 0.56, "CCG": 3.04,
        "ACT": 0.36, "ACC": 1.72, "ACA": 0.24, "ACG": 1.68,
        "GCT": 0.64, "GCC": 1.04, "GCA": 0.84, "GCG": 1.48,
        "TAT": 0.58, "TAC": 1.42, "CAT": 0.58, "CAC": 1.42,
        "CAA": 0.30, "CAG": 1.70, "AAT": 0.46, "AAC": 1.54,
        "AAA": 1.50, "AAG": 0.50, "GAT": 0.74, "GAC": 1.26,
        "GAA": 1.38, "GAG": 0.62, "TGT": 0.48, "TGC": 1.52,
        "TGG": 1.00, "CGT": 3.24, "CGC": 2.56, "CGA": 0.12,
        "CGG": 0.16, "AGT": 0.28, "AGC": 1.80, "AGA": 0.08,
        "AGG": 0.04, "GGT": 1.64, "GGC": 1.84, "GGA": 0.16,
        "GGG": 0.36,
    },

    # Acropora millepora — staghorn coral (~40% GC)
    "acropora": {
        "TTT": 1.14, "TTC": 0.86, "TTA": 0.72, "TTG": 1.08,
        "CTT": 1.20, "CTC": 0.84, "CTA": 0.60, "CTG": 1.56,
        "ATT": 1.20, "ATC": 1.08, "ATA": 0.72, "ATG": 1.00,
        "GTT": 1.08, "GTC": 0.84, "GTA": 0.60, "GTG": 1.48,
        "TCT": 1.32, "TCC": 1.08, "TCA": 1.02, "TCG": 0.54,
        "CCT": 1.32, "CCC": 0.96, "CCA": 1.20, "CCG": 0.52,
        "ACT": 1.20, "ACC": 1.12, "ACA": 1.12, "ACG": 0.56,
        "GCT": 1.28, "GCC": 1.08, "GCA": 1.04, "GCG": 0.60,
        "TAT": 1.16, "TAC": 0.84, "CAT": 1.16, "CAC": 0.84,
        "CAA": 1.12, "CAG": 0.88, "AAT": 1.16, "AAC": 0.84,
        "AAA": 1.20, "AAG": 0.80, "GAT": 1.16, "GAC": 0.84,
        "GAA": 1.16, "GAG": 0.84, "TGT": 1.12, "TGC": 0.88,
        "TGG": 1.00, "CGT": 0.72, "CGC": 0.84, "CGA": 0.96,
        "CGG": 0.72, "AGT": 1.02, "AGC": 1.02, "AGA": 1.56,
        "AGG": 1.20, "GGT": 1.04, "GGC": 0.88, "GGA": 1.20,
        "GGG": 0.88,
    },

    # Axolotl (Ambystoma mexicanum) — regeneration model (~44% GC)
    "axolotl": {
        "TTT": 1.00, "TTC": 1.00, "TTA": 0.42, "TTG": 0.78,
        "CTT": 0.84, "CTC": 1.14, "CTA": 0.42, "CTG": 2.40,
        "ATT": 1.02, "ATC": 1.38, "ATA": 0.60, "ATG": 1.00,
        "GTT": 0.68, "GTC": 0.92, "GTA": 0.48, "GTG": 1.92,
        "TCT": 1.02, "TCC": 1.32, "TCA": 0.78, "TCG": 0.36,
        "CCT": 1.08, "CCC": 1.28, "CCA": 1.08, "CCG": 0.56,
        "ACT": 0.88, "ACC": 1.52, "ACA": 1.04, "ACG": 0.56,
        "GCT": 0.92, "GCC": 1.64, "GCA": 0.84, "GCG": 0.60,
        "TAT": 0.88, "TAC": 1.12, "CAT": 0.84, "CAC": 1.16,
        "CAA": 0.68, "CAG": 1.32, "AAT": 0.92, "AAC": 1.08,
        "AAA": 0.88, "AAG": 1.12, "GAT": 0.92, "GAC": 1.08,
        "GAA": 0.84, "GAG": 1.16, "TGT": 0.92, "TGC": 1.08,
        "TGG": 1.00, "CGT": 0.48, "CGC": 1.08, "CGA": 0.66,
        "CGG": 1.14, "AGT": 0.84, "AGC": 1.68, "AGA": 1.32,
        "AGG": 1.32, "GGT": 0.64, "GGC": 1.36, "GGA": 1.04,
        "GGG": 0.96,
    },
}


# ---------------------------------------------------------------------------
# Organism metadata
# ---------------------------------------------------------------------------

@dataclass
class OrganismProfile:
    """Economic profile of an organism in the trade network."""
    name: str
    kingdom: str            # "prokaryote", "eukaryote_fungal", "eukaryote_plant", "eukaryote_animal"
    capabilities: list[str] = field(default_factory=list)  # what this organism "exports"
    has_rscu: bool = False


def get_all_organisms() -> dict[str, OrganismProfile]:
    """Build the full organism roster with capabilities and kingdom classification."""

    organisms = {
        "komagataeibacter": OrganismProfile(
            "komagataeibacter", "prokaryote",
            capabilities=["cellulose"],
        ),
        "e_coli": OrganismProfile(
            "e_coli", "prokaryote",
            capabilities=["model_organism", "metabolic_engineering"],
        ),
        "yeast": OrganismProfile(
            "yeast", "eukaryote_fungal",
            capabilities=["nutrient_uptake", "fermentation"],
        ),
        "ganoderma": OrganismProfile(
            "ganoderma", "eukaryote_fungal",
            capabilities=["structural", "biomaterials"],
        ),
        "arabidopsis": OrganismProfile(
            "arabidopsis", "eukaryote_plant",
            capabilities=["growth", "water_transport", "thermal_regulation"],
        ),
        "human": OrganismProfile(
            "human", "eukaryote_animal",
            capabilities=["tensile_strength", "self_repair"],
        ),
        "acropora": OrganismProfile(
            "acropora", "eukaryote_animal",
            capabilities=["biomineralization"],
        ),
        "axolotl": OrganismProfile(
            "axolotl", "eukaryote_animal",
            capabilities=["self_repair", "regeneration"],
        ),
    }

    # Mark which organisms have RSCU data
    all_rscu = {**REFERENCE_RSCU, **EXTENDED_RSCU}
    for name, org in organisms.items():
        org.has_rscu = name in all_rscu

    return organisms


# ---------------------------------------------------------------------------
# Trade cost calculation
# ---------------------------------------------------------------------------

def codon_distance(org_a: str, org_b: str) -> float:
    """
    Euclidean distance between RSCU vectors of two organisms.
    Higher = more different codon dialects = higher trade friction.

    This is the biological equivalent of linguistic trade friction:
    the more different the languages, the harder the trade.
    """
    all_rscu = {**REFERENCE_RSCU, **EXTENDED_RSCU}
    rscu_a = all_rscu.get(org_a)
    rscu_b = all_rscu.get(org_b)

    if not rscu_a or not rscu_b:
        return float("inf")

    # Get common codons
    codons = sorted(set(rscu_a.keys()) & set(rscu_b.keys()))
    if not codons:
        return float("inf")

    vec_a = np.array([rscu_a[c] for c in codons])
    vec_b = np.array([rscu_b[c] for c in codons])

    return float(np.linalg.norm(vec_a - vec_b))


def regulatory_barrier(org_a: str, org_b: str) -> float:
    """
    Regulatory trade barrier: cost of translating between legal frameworks.

    Cross-kingdom (prokaryote ↔ eukaryote): 1.0 (full regulatory replacement needed)
    Same kingdom, different class: 0.3
    Same class: 0.0
    """
    kingdoms = {
        "komagataeibacter": "prokaryote",
        "e_coli": "prokaryote",
        "yeast": "eukaryote_fungal",
        "ganoderma": "eukaryote_fungal",
        "arabidopsis": "eukaryote_plant",
        "human": "eukaryote_animal",
        "acropora": "eukaryote_animal",
        "axolotl": "eukaryote_animal",
    }

    ka = kingdoms.get(org_a, "unknown")
    kb = kingdoms.get(org_b, "unknown")

    if ka == kb:
        return 0.0

    # Cross kingdom boundary (prokaryote ↔ eukaryote)
    a_prok = ka == "prokaryote"
    b_prok = kb == "prokaryote"
    if a_prok != b_prok:
        return 1.0

    # Same domain but different class (e.g., fungal vs plant vs animal)
    return 0.3


def trade_cost(
    org_a: str,
    org_b: str,
    w_codon: float = 0.5,
    w_regulatory: float = 0.35,
    w_baseline: float = 0.15,
) -> float:
    """
    Total trade cost between two organisms.

    Weighted combination of:
        - Codon distance (linguistic friction)
        - Regulatory barrier (legal/institutional friction)
        - Baseline cost (inherent complexity of horizontal gene transfer)
    """
    cd = codon_distance(org_a, org_b)
    rb = regulatory_barrier(org_a, org_b)

    # Normalize codon distance to 0-1 range (typical range is 0-15)
    cd_norm = min(cd / 15.0, 1.0)

    return w_codon * cd_norm + w_regulatory * rb + w_baseline


# ---------------------------------------------------------------------------
# Trade network construction
# ---------------------------------------------------------------------------

def build_trade_network() -> nx.Graph:
    """
    Build the cross-species trade network.

    Nodes = organisms
    Edge weight = trade ease (1 / trade_cost) — higher = easier trade
    Node attributes: kingdom, capabilities
    Edge attributes: trade_cost, codon_distance, regulatory_barrier
    """
    organisms = get_all_organisms()
    G = nx.Graph()

    # Add nodes
    for name, org in organisms.items():
        if not org.has_rscu:
            continue
        G.add_node(
            name,
            kingdom=org.kingdom,
            capabilities=org.capabilities,
            n_capabilities=len(org.capabilities),
        )

    # Add edges
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            tc = trade_cost(a, b)
            cd = codon_distance(a, b)
            rb = regulatory_barrier(a, b)

            if tc < float("inf"):
                G.add_edge(
                    a, b,
                    trade_cost=tc,
                    trade_ease=1.0 / max(tc, 0.01),
                    codon_distance=cd,
                    regulatory_barrier=rb,
                )

    return G


def compute_trade_matrix() -> tuple[list[str], np.ndarray]:
    """
    Compute the full trade cost matrix across all organisms.
    Returns (organism_names, cost_matrix).
    """
    organisms = get_all_organisms()
    names = [n for n, o in organisms.items() if o.has_rscu]
    n = len(names)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i, j] = 0.0
            else:
                matrix[i, j] = trade_cost(names[i], names[j])

    return names, matrix


def comparative_advantage_table() -> dict[str, list[str]]:
    """
    Map each organism's comparative advantage — what it uniquely exports.

    This is Ricardo's comparative advantage at the molecular level:
    each organism has evolved capabilities that others lack.
    """
    organisms = get_all_organisms()
    return {name: org.capabilities for name, org in organisms.items()}


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_trade_network(save: bool = True) -> plt.Figure:
    """
    Generate a 3-panel trade network figure.

    Panel 1: Trade network graph
    Panel 2: Trade cost heatmap
    Panel 3: Comparative advantage table
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(18, 6), facecolor=BACKGROUND)
    gs = gridspec.GridSpec(1, 3, wspace=0.3)

    G = build_trade_network()
    names, cost_matrix = compute_trade_matrix()

    # Kingdom colors
    kingdom_colors = {
        "prokaryote": RED,
        "eukaryote_fungal": SPIRAL_GREEN,
        "eukaryote_plant": GOLD,
        "eukaryote_animal": BLUE,
    }

    # --- Panel 1: Trade Network ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(PANEL_BG)

    pos = nx.spring_layout(G, seed=42, k=3, weight="trade_ease")
    node_colors = [kingdom_colors.get(G.nodes[n]["kingdom"], TEXT_DIM) for n in G.nodes()]
    node_sizes = [400 + 200 * G.nodes[n].get("n_capabilities", 1) for n in G.nodes()]

    edge_weights = [G[u][v]["trade_ease"] for u, v in G.edges()]
    max_ease = max(edge_weights) if edge_weights else 1
    edge_widths = [1 + 4 * (w / max_ease) for w in edge_weights]

    nx.draw_networkx_edges(G, pos, ax=ax1, width=edge_widths, edge_color=SPIRAL_LIGHT, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=node_sizes, node_color=node_colors, edgecolors=TEXT_DIM)
    nx.draw_networkx_labels(G, pos, ax=ax1, font_size=7, font_color=TEXT_MAIN)

    # Legend
    for kingdom, color in kingdom_colors.items():
        ax1.scatter([], [], c=color, s=80, label=kingdom.replace("eukaryote_", ""))
    ax1.legend(fontsize=7, facecolor=PANEL_BG, edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN, loc="lower left")

    ax1.set_title("Cross-Species Trade Network", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax1.axis("off")

    # --- Panel 2: Trade Cost Heatmap ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(PANEL_BG)

    im = ax2.imshow(cost_matrix, cmap="YlOrRd", aspect="auto")
    ax2.set_xticks(range(len(names)))
    ax2.set_yticks(range(len(names)))
    ax2.set_xticklabels(names, rotation=45, ha="right", fontsize=7, color=TEXT_MAIN)
    ax2.set_yticklabels(names, fontsize=7, color=TEXT_MAIN)

    # Annotate cells
    for i in range(len(names)):
        for j in range(len(names)):
            val = cost_matrix[i, j]
            color = TEXT_MAIN if val > 0.5 else BACKGROUND
            ax2.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=6, color=color)

    cbar = fig.colorbar(im, ax=ax2, shrink=0.8)
    cbar.ax.tick_params(colors=TEXT_DIM)
    cbar.set_label("Trade Cost", color=TEXT_MAIN, fontsize=10)

    ax2.set_title("Trade Barriers Heatmap", color=TEXT_MAIN, fontsize=13, fontweight="bold")

    # --- Panel 3: Comparative Advantage ---
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(PANEL_BG)
    ax3.axis("off")

    advantages = comparative_advantage_table()
    y = 0.95
    ax3.text(0.05, y, "Organism", color=GOLD, fontsize=10, fontweight="bold",
             transform=ax3.transAxes)
    ax3.text(0.45, y, "Exports (Comparative Advantage)", color=GOLD, fontsize=10,
             fontweight="bold", transform=ax3.transAxes)
    y -= 0.05
    ax3.plot([0.02, 0.98], [y, y], color=TEXT_DIM, linewidth=0.5,
             transform=ax3.transAxes)

    for org_name, caps in advantages.items():
        y -= 0.08
        if y < 0:
            break
        kingdom = get_all_organisms()[org_name].kingdom
        color = kingdom_colors.get(kingdom, TEXT_MAIN)
        ax3.text(0.05, y, org_name, color=color, fontsize=8, transform=ax3.transAxes)
        ax3.text(0.45, y, ", ".join(caps), color=TEXT_MAIN, fontsize=8,
                 transform=ax3.transAxes)

    ax3.set_title("Comparative Advantage", color=TEXT_MAIN, fontsize=13, fontweight="bold")

    fig.suptitle(
        "Layer 3: The Tree of Life Is a Trade Network",
        color=GOLD, fontsize=15, fontweight="bold", y=1.02,
    )

    plt.tight_layout()

    if save:
        out = FIGURES_DIR / "layer3_trade_network.png"
        fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BACKGROUND)
        print(f"[trade] Saved figure to {out}")

    return fig


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Layer 3: Cross-Species Trade Network")
    print("=" * 60)
    print()

    # Build trade network
    G = build_trade_network()
    print(f"Trade network: {G.number_of_nodes()} organisms, {G.number_of_edges()} trade links")

    # Print trade cost matrix
    names, matrix = compute_trade_matrix()
    print(f"\nTrade Cost Matrix ({len(names)} organisms):")
    print(f"{'':>18}", end="")
    for n in names:
        print(f"{n:>14}", end="")
    print()
    for i, n in enumerate(names):
        print(f"{n:>18}", end="")
        for j in range(len(names)):
            print(f"{matrix[i, j]:>14.3f}", end="")
        print()

    # Comparative advantage
    print("\nComparative Advantage:")
    for org, caps in comparative_advantage_table().items():
        print(f"  {org}: {', '.join(caps)}")

    # Find free trade zones (lowest cost pairs)
    print("\nFree Trade Zones (lowest trade cost pairs):")
    pairs = []
    for u, v, data in G.edges(data=True):
        pairs.append((u, v, data["trade_cost"]))
    pairs.sort(key=lambda x: x[2])
    for u, v, tc in pairs[:5]:
        print(f"  {u} ↔ {v}: cost={tc:.3f}")

    # Find highest trade barriers
    print("\nHighest Trade Barriers:")
    for u, v, tc in pairs[-3:]:
        print(f"  {u} ↔ {v}: cost={tc:.3f}")

    # Generate figure
    print("\nGenerating figure...")
    plot_trade_network()

    print("\nDone.")
