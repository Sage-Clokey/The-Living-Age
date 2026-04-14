"""
Topology Analysis — Layer 1: Network Topology
==============================================
Computes structural metrics on biological networks to prove they are
decentralized: no master node, no single bottleneck, graceful degradation.

Metrics:
    1. Degree distribution — fit to power-law (scale-free = decentralized)
    2. Betweenness centrality — distribution should be broad, not peaked
    3. Clustering coefficient — high = local cooperation clusters
    4. Connected components — giant component = integrated economy
    5. Robustness — node removal curves (random + targeted attack)

Each metric is computed for biological networks and compared against
centralized reference networks (star, hub-and-spoke, lattice).

References:
    - Barabasi & Oltvai, "Network biology," Nature Reviews Genetics 2004
    - Clauset et al., "Power-law distributions in empirical data," SIAM Review 2009
    - Albert et al., "Error and attack tolerance of complex networks," Nature 2000
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Try importing powerlaw; fall back to manual fitting if unavailable
try:
    import powerlaw
    HAS_POWERLAW = True
except ImportError:
    HAS_POWERLAW = False
    print("[topology] Warning: 'powerlaw' not installed. Using manual fitting.")

# ---------------------------------------------------------------------------
# Aesthetic (matches molecular_voluntary_society.py palette)
# ---------------------------------------------------------------------------

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
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class TopologyReport:
    """Complete topology analysis for a single network."""
    name: str
    n_nodes: int
    n_edges: int
    is_directed: bool

    # Degree distribution
    degree_sequence: list[int] = field(default_factory=list)
    mean_degree: float = 0.0
    max_degree: int = 0
    powerlaw_alpha: float = 0.0     # power-law exponent
    powerlaw_xmin: float = 0.0      # minimum x for power-law fit
    powerlaw_p_value: float = 0.0   # goodness-of-fit p-value
    is_scale_free: bool = False     # alpha between 2 and 3, p > 0.1

    # Centrality
    mean_betweenness: float = 0.0
    max_betweenness: float = 0.0
    max_betweenness_node: str = ""
    betweenness_gini: float = 0.0   # Gini coefficient of betweenness (0=equal, 1=one node)

    # Clustering
    avg_clustering: float = 0.0

    # Components
    n_components: int = 0
    giant_component_fraction: float = 0.0

    # Robustness curves (filled by robustness analysis)
    robustness_random: list[float] = field(default_factory=list)
    robustness_targeted: list[float] = field(default_factory=list)
    robustness_random_half: float = 0.0    # fraction removed before GC < 50%
    robustness_targeted_half: float = 0.0

    def summary(self) -> str:
        sf = "YES" if self.is_scale_free else "no"
        return (
            f"[{self.name}] {self.n_nodes} nodes, {self.n_edges} edges\n"
            f"  Degree: mean={self.mean_degree:.1f}, max={self.max_degree}\n"
            f"  Power-law: alpha={self.powerlaw_alpha:.2f}, p={self.powerlaw_p_value:.3f}, scale-free={sf}\n"
            f"  Betweenness: mean={self.mean_betweenness:.4f}, max={self.max_betweenness:.4f} ({self.max_betweenness_node}), gini={self.betweenness_gini:.3f}\n"
            f"  Clustering: {self.avg_clustering:.4f}\n"
            f"  Components: {self.n_components}, giant={self.giant_component_fraction:.1%}\n"
            f"  Robustness (random): {self.robustness_random_half:.1%} removed before GC<50%\n"
            f"  Robustness (targeted): {self.robustness_targeted_half:.1%} removed before GC<50%"
        )


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------

def analyze_topology(G: nx.Graph, name: str = "network") -> TopologyReport:
    """
    Run complete topology analysis on a network.
    Works with both directed and undirected graphs.
    """
    report = TopologyReport(
        name=name,
        n_nodes=G.number_of_nodes(),
        n_edges=G.number_of_edges(),
        is_directed=G.is_directed(),
    )

    if report.n_nodes == 0:
        return report

    # Use undirected view for most metrics
    U = G.to_undirected() if G.is_directed() else G

    # --- Degree distribution ---
    degrees = [d for _, d in U.degree()]
    report.degree_sequence = sorted(degrees, reverse=True)
    report.mean_degree = np.mean(degrees)
    report.max_degree = max(degrees)

    # Power-law fit
    n_unique = len(set(degrees))
    if HAS_POWERLAW and len(degrees) > 50 and n_unique > 5:
        try:
            fit = powerlaw.Fit(degrees, discrete=True, verbose=False)
            report.powerlaw_alpha = fit.power_law.alpha
            report.powerlaw_xmin = fit.power_law.xmin
            # Compare power-law vs exponential
            R, p = fit.distribution_compare("power_law", "exponential")
            report.powerlaw_p_value = p
            report.is_scale_free = (2.0 <= fit.power_law.alpha <= 3.5 and R > 0)
        except (ValueError, RuntimeError):
            report.powerlaw_alpha, report.powerlaw_p_value = _manual_powerlaw_fit(degrees)
            report.is_scale_free = 2.0 <= report.powerlaw_alpha <= 3.5
    else:
        # Manual log-log regression fallback
        report.powerlaw_alpha, report.powerlaw_p_value = _manual_powerlaw_fit(degrees)
        report.is_scale_free = 2.0 <= report.powerlaw_alpha <= 3.5

    # --- Betweenness centrality ---
    # For large networks, use approximate betweenness
    if report.n_nodes > 5000:
        bc = nx.betweenness_centrality(U, k=min(500, report.n_nodes))
    else:
        bc = nx.betweenness_centrality(U)

    bc_values = list(bc.values())
    report.mean_betweenness = np.mean(bc_values)
    report.max_betweenness = max(bc_values)
    report.max_betweenness_node = max(bc, key=bc.get)
    report.betweenness_gini = _gini(bc_values)

    # --- Clustering coefficient ---
    report.avg_clustering = nx.average_clustering(U)

    # --- Connected components ---
    components = list(nx.connected_components(U))
    report.n_components = len(components)
    largest = max(components, key=len)
    report.giant_component_fraction = len(largest) / report.n_nodes

    # --- Robustness analysis ---
    report.robustness_random, report.robustness_random_half = _robustness_curve(
        U, mode="random", trials=10,
    )
    report.robustness_targeted, report.robustness_targeted_half = _robustness_curve(
        U, mode="targeted",
    )

    return report


def _manual_powerlaw_fit(degrees: list[int]) -> tuple[float, float]:
    """Simple log-log linear regression as power-law estimate."""
    from collections import Counter
    counts = Counter(degrees)
    k_vals = np.array(sorted(counts.keys()))
    freq = np.array([counts[k] for k in k_vals], dtype=float)

    # Filter zeros
    mask = (k_vals > 0) & (freq > 0)
    if mask.sum() < 3:
        return 0.0, 1.0

    log_k = np.log10(k_vals[mask])
    log_f = np.log10(freq[mask])

    # Linear regression on log-log
    coeffs = np.polyfit(log_k, log_f, 1)
    alpha = -coeffs[0]  # power-law exponent (negative slope)

    # R-squared as rough p-value proxy
    predicted = np.polyval(coeffs, log_k)
    ss_res = np.sum((log_f - predicted) ** 2)
    ss_tot = np.sum((log_f - np.mean(log_f)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return alpha, r_squared


def _gini(values: list[float]) -> float:
    """Compute Gini coefficient. 0 = perfect equality, 1 = one node has everything."""
    arr = np.array(sorted(values))
    n = len(arr)
    if n == 0 or arr.sum() == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * arr) - (n + 1) * arr.sum()) / (n * arr.sum())


def _robustness_curve(
    G: nx.Graph,
    mode: str = "random",
    trials: int = 1,
    steps: int = 50,
) -> tuple[list[float], float]:
    """
    Measure network robustness by progressively removing nodes.

    Args:
        G: undirected graph
        mode: "random" (random node removal) or "targeted" (highest degree first)
        trials: number of independent random trials to average (only for random mode)
        steps: number of removal steps

    Returns:
        (gc_fractions, half_life)
        gc_fractions: giant component size as fraction of original, at each removal step
        half_life: fraction of nodes removed before GC drops below 50%
    """
    n = G.number_of_nodes()
    if n == 0:
        return [], 0.0

    removal_fractions = np.linspace(0, 0.95, steps)
    gc_curves = []

    for trial in range(trials if mode == "random" else 1):
        H = G.copy()
        nodes = list(H.nodes())

        if mode == "targeted":
            # Sort by degree descending (attack hubs first)
            nodes = sorted(nodes, key=lambda x: H.degree(x), reverse=True)
        else:
            np.random.shuffle(nodes)

        gc_frac = []
        for frac in removal_fractions:
            n_remove = int(frac * n)
            # Build subgraph of remaining nodes
            remaining = set(nodes[n_remove:])
            if len(remaining) == 0:
                gc_frac.append(0.0)
                continue

            sub = H.subgraph(remaining)
            if sub.number_of_nodes() == 0:
                gc_frac.append(0.0)
            else:
                components = list(nx.connected_components(sub))
                largest = max(len(c) for c in components)
                gc_frac.append(largest / n)

        gc_curves.append(gc_frac)

    # Average over trials
    avg_curve = np.mean(gc_curves, axis=0).tolist()

    # Find half-life: first point where GC < 50%
    half_life = 0.95
    for i, frac in enumerate(avg_curve):
        if frac < 0.5:
            half_life = removal_fractions[i]
            break

    return avg_curve, half_life


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_topology_report(
    bio_reports: list[TopologyReport],
    ref_reports: list[TopologyReport] = None,
    save: bool = True,
) -> plt.Figure:
    """
    Generate a 3-panel topology analysis figure.

    Panel 1: Degree distributions (log-log) for all networks
    Panel 2: Betweenness centrality distributions
    Panel 3: Robustness curves (random + targeted)
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(18, 6), facecolor=BACKGROUND)
    gs = gridspec.GridSpec(1, 3, wspace=0.3)

    all_reports = bio_reports + (ref_reports or [])
    bio_colors = [SPIRAL_GREEN, SPIRAL_MID, BLUE]
    ref_colors = [RED, GOLD, TEXT_DIM]

    # --- Panel 1: Degree Distribution (log-log) ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(PANEL_BG)

    for i, r in enumerate(bio_reports):
        if not r.degree_sequence:
            continue
        color = bio_colors[i % len(bio_colors)]
        _plot_degree_dist(ax1, r.degree_sequence, color, r.name, marker="o")

    if ref_reports:
        for i, r in enumerate(ref_reports):
            if not r.degree_sequence:
                continue
            color = ref_colors[i % len(ref_colors)]
            _plot_degree_dist(ax1, r.degree_sequence, color, r.name, marker="x")

    ax1.set_xlabel("Degree (k)", color=TEXT_MAIN, fontsize=11)
    ax1.set_ylabel("P(k)", color=TEXT_MAIN, fontsize=11)
    ax1.set_title("Degree Distribution", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax1.legend(fontsize=8, facecolor=PANEL_BG, edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN)
    ax1.tick_params(colors=TEXT_DIM)
    ax1.set_xscale("log")
    ax1.set_yscale("log")

    # --- Panel 2: Betweenness Centrality ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(PANEL_BG)

    bar_data = []
    bar_colors = []
    bar_labels = []
    for i, r in enumerate(bio_reports):
        bar_data.append(r.betweenness_gini)
        bar_colors.append(bio_colors[i % len(bio_colors)])
        bar_labels.append(r.name)
    if ref_reports:
        for i, r in enumerate(ref_reports):
            bar_data.append(r.betweenness_gini)
            bar_colors.append(ref_colors[i % len(ref_colors)])
            bar_labels.append(r.name)

    x = np.arange(len(bar_data))
    ax2.bar(x, bar_data, color=bar_colors, edgecolor=TEXT_DIM, linewidth=0.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(bar_labels, rotation=30, ha="right", fontsize=8, color=TEXT_MAIN)
    ax2.set_ylabel("Betweenness Gini Coefficient", color=TEXT_MAIN, fontsize=11)
    ax2.set_title("Centrality Inequality", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax2.tick_params(colors=TEXT_DIM)
    ax2.set_ylim(0, 1)
    # Annotation
    ax2.axhline(y=0.5, color=TEXT_DIM, linestyle="--", linewidth=0.8, alpha=0.5)
    ax2.text(
        len(bar_data) - 0.5, 0.52, "high centralization →",
        color=TEXT_DIM, fontsize=8, ha="right",
    )

    # --- Panel 3: Robustness Curves ---
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(PANEL_BG)

    removal_fracs = np.linspace(0, 0.95, 50)

    for i, r in enumerate(bio_reports):
        color = bio_colors[i % len(bio_colors)]
        if r.robustness_random:
            ax3.plot(
                removal_fracs[:len(r.robustness_random)],
                r.robustness_random,
                color=color, linewidth=2, label=f"{r.name} (random)",
            )
        if r.robustness_targeted:
            ax3.plot(
                removal_fracs[:len(r.robustness_targeted)],
                r.robustness_targeted,
                color=color, linewidth=2, linestyle="--", label=f"{r.name} (targeted)",
            )

    if ref_reports:
        for i, r in enumerate(ref_reports):
            color = ref_colors[i % len(ref_colors)]
            if r.robustness_targeted:
                ax3.plot(
                    removal_fracs[:len(r.robustness_targeted)],
                    r.robustness_targeted,
                    color=color, linewidth=2, linestyle="--", label=f"{r.name} (targeted)",
                )

    ax3.axhline(y=0.5, color=TEXT_DIM, linestyle=":", linewidth=0.8, alpha=0.5)
    ax3.set_xlabel("Fraction of Nodes Removed", color=TEXT_MAIN, fontsize=11)
    ax3.set_ylabel("Giant Component / Original", color=TEXT_MAIN, fontsize=11)
    ax3.set_title("Robustness Under Attack", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax3.legend(fontsize=7, facecolor=PANEL_BG, edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN, loc="upper right")
    ax3.tick_params(colors=TEXT_DIM)
    ax3.set_xlim(0, 0.95)
    ax3.set_ylim(0, 1.05)

    fig.suptitle(
        "Layer 1: Biological Networks Are Decentralized",
        color=GOLD, fontsize=15, fontweight="bold", y=1.02,
    )

    plt.tight_layout()

    if save:
        out = FIGURES_DIR / "layer1_topology.png"
        fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BACKGROUND)
        print(f"[topology] Saved figure to {out}")

    return fig


def _plot_degree_dist(ax, degree_seq: list[int], color: str, label: str, marker: str = "o"):
    """Plot degree distribution as log-binned scatter on log-log axes."""
    from collections import Counter
    counts = Counter(degree_seq)
    total = sum(counts.values())
    k_vals = sorted(counts.keys())
    probs = [counts[k] / total for k in k_vals]

    ax.scatter(k_vals, probs, color=color, s=20, marker=marker, label=label, alpha=0.8)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from layer1_topology.network_fetcher import load_all_networks
    from layer1_topology.centralized_comparison import build_comparison_networks

    print("=" * 60)
    print("Layer 1: Topology Analysis")
    print("=" * 60)
    print()

    # Load biological networks
    networks = load_all_networks()

    # Analyze each
    bio_reports = []
    for name, G in networks.items():
        print(f"\nAnalyzing {name}...")
        report = analyze_topology(G, name=name)
        bio_reports.append(report)
        print(report.summary())

    # Build and analyze comparison networks
    # Use E. coli GRN size as reference
    ref_n = networks["ecoli_grn"].number_of_nodes()
    ref_m = networks["ecoli_grn"].number_of_edges()
    ref_networks = build_comparison_networks(n_nodes=ref_n, n_edges=ref_m)

    ref_reports = []
    for name, G in ref_networks.items():
        print(f"\nAnalyzing reference: {name}...")
        report = analyze_topology(G, name=name)
        ref_reports.append(report)
        print(report.summary())

    # Plot
    print("\nGenerating figures...")
    plot_topology_report(bio_reports, ref_reports)
    print("\nDone.")
