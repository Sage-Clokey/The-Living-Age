"""
Generate Figure 2: Biological PPI Networks Are Decentralized
============================================================
Three-panel figure comparing real protein-protein interaction networks
(E. coli, yeast) against centralized reference architectures (star,
hub-and-spoke) and random/lattice controls.

Panel A: Degree distribution (log-log) — power-law vs spike
Panel B: Betweenness Gini coefficient — distributed vs concentrated
Panel C: Robustness curves — graceful degradation vs cliff collapse
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import Counter

from layer1_topology.network_fetcher import load_all_networks
from layer1_topology.topology_analysis import analyze_topology, _gini, _robustness_curve
from layer1_topology.centralized_comparison import build_comparison_networks


# ---------------------------------------------------------------------------
# Academic palette (white background, colorblind-friendly)
# ---------------------------------------------------------------------------
BIO_COLORS = {
    "ecoli_ppi":  "#2d6a4f",   # deep green
    "yeast_ppi":  "#52b788",   # mid green
    "ecoli_grn":  "#1b4332",   # dark forest
}
REF_COLORS = {
    "Star (centralized)":   "#d62828",  # red
    "Hub-and-spoke":        "#f77f00",  # orange
    "Random (Erdos-Renyi)": "#7b7b7b",  # gray
}
FIGURES_DIR = PROJECT_ROOT / "paper" / "figures"


def main():
    # Load networks
    print("Loading biological networks...")
    networks = load_all_networks()

    # Focus on PPI + GRN (skip metabolic — too dense, different structure)
    bio_keys = ["ecoli_ppi", "yeast_ppi", "ecoli_grn"]
    bio_nets = {k: networks[k] for k in bio_keys}

    # Analyze biological networks
    bio_reports = {}
    for name, G in bio_nets.items():
        print(f"Analyzing {name}...")
        bio_reports[name] = analyze_topology(G, name=name)

    # Build reference networks matched to E. coli PPI size
    ref_n = bio_nets["ecoli_ppi"].number_of_nodes()
    ref_m = bio_nets["ecoli_ppi"].number_of_edges()
    ref_nets = build_comparison_networks(n_nodes=ref_n, n_edges=ref_m)

    # Only keep star, hub-and-spoke, random
    ref_keep = ["Star (centralized)", "Hub-and-spoke", "Random (Erdos-Renyi)"]
    ref_reports = {}
    for name in ref_keep:
        if name in ref_nets:
            print(f"Analyzing reference: {name}...")
            ref_reports[name] = analyze_topology(ref_nets[name], name=name)

    # --- Build figure ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.patch.set_facecolor("white")

    # ===== Panel A: Degree Distribution (log-log) =====
    ax = axes[0]
    for name, report in bio_reports.items():
        counts = Counter(report.degree_sequence)
        total = sum(counts.values())
        k_vals = sorted(counts.keys())
        probs = [counts[k] / total for k in k_vals]
        ax.scatter(k_vals, probs, s=25, color=BIO_COLORS[name],
                   label=_nice_name(name), alpha=0.85, zorder=3)

    for name, report in ref_reports.items():
        counts = Counter(report.degree_sequence)
        total = sum(counts.values())
        k_vals = sorted(counts.keys())
        probs = [counts[k] / total for k in k_vals]
        ax.scatter(k_vals, probs, s=20, color=REF_COLORS[name],
                   marker="x", label=name, alpha=0.7, zorder=2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Degree (k)", fontsize=11)
    ax.set_ylabel("P(k)", fontsize=11)
    ax.set_title("A. Degree Distribution", fontsize=12, fontweight="bold", loc="left")
    ax.legend(fontsize=7, framealpha=0.9, loc="upper right")
    ax.grid(True, alpha=0.2)
    # Annotate power-law
    ax.text(0.05, 0.05,
            f"E. coli PPI: α = {bio_reports['ecoli_ppi'].powerlaw_alpha:.2f}\n"
            f"Yeast PPI: α = {bio_reports['yeast_ppi'].powerlaw_alpha:.2f}\n"
            f"E. coli GRN: α = {bio_reports['ecoli_grn'].powerlaw_alpha:.2f}",
            transform=ax.transAxes, fontsize=7.5, verticalalignment="bottom",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#cccccc"))

    # ===== Panel B: Betweenness Gini Coefficient =====
    ax = axes[1]
    all_names = list(bio_reports.keys()) + list(ref_reports.keys())
    all_gini = [bio_reports[k].betweenness_gini for k in bio_reports] + \
               [ref_reports[k].betweenness_gini for k in ref_reports]
    all_colors = [BIO_COLORS[k] for k in bio_reports] + \
                 [REF_COLORS[k] for k in ref_reports]
    all_labels = [_nice_name(k) for k in bio_reports] + list(ref_reports.keys())

    x = np.arange(len(all_names))
    bars = ax.bar(x, all_gini, color=all_colors, edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(all_labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Betweenness Gini Coefficient", fontsize=11)
    ax.set_title("B. Centrality Inequality", fontsize=12, fontweight="bold", loc="left")
    ax.set_ylim(0, 1.05)
    ax.axhline(y=0.5, color="#999999", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.text(len(all_names) - 0.3, 0.52, "← more distributed | more centralized →",
            fontsize=7, ha="right", color="#666666")
    ax.grid(True, axis="y", alpha=0.2)

    # Add value labels on bars
    for bar, val in zip(bars, all_gini):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{val:.2f}", ha="center", va="bottom", fontsize=7)

    # ===== Panel C: Robustness Curves =====
    ax = axes[2]
    removal_fracs = np.linspace(0, 0.95, 50)

    for name, report in bio_reports.items():
        if report.robustness_random:
            ax.plot(removal_fracs[:len(report.robustness_random)],
                    report.robustness_random,
                    color=BIO_COLORS[name], linewidth=2,
                    label=f"{_nice_name(name)} (random)", zorder=3)
        if report.robustness_targeted:
            ax.plot(removal_fracs[:len(report.robustness_targeted)],
                    report.robustness_targeted,
                    color=BIO_COLORS[name], linewidth=2, linestyle="--",
                    label=f"{_nice_name(name)} (targeted)", zorder=3)

    for name, report in ref_reports.items():
        if name == "Random (Erdos-Renyi)":
            continue  # skip for clarity
        if report.robustness_targeted:
            ax.plot(removal_fracs[:len(report.robustness_targeted)],
                    report.robustness_targeted,
                    color=REF_COLORS[name], linewidth=1.5, linestyle="--",
                    label=f"{name} (targeted)", alpha=0.7, zorder=2)

    ax.axhline(y=0.5, color="#999999", linestyle=":", linewidth=0.8, alpha=0.6)
    ax.set_xlabel("Fraction of Nodes Removed", fontsize=11)
    ax.set_ylabel("Giant Component / Original", fontsize=11)
    ax.set_title("C. Robustness Under Attack", fontsize=12, fontweight="bold", loc="left")
    ax.legend(fontsize=6.5, framealpha=0.9, loc="upper right")
    ax.set_xlim(0, 0.95)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.2)
    # Annotate the key comparison
    ax.annotate("Star collapses\nimmediately",
                xy=(0.02, 0.0), xytext=(0.15, 0.15),
                fontsize=7, color="#d62828",
                arrowprops=dict(arrowstyle="->", color="#d62828", lw=1))

    plt.tight_layout()

    # Save
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_png = FIGURES_DIR / "figure2_network_topology.png"
    out_pdf = FIGURES_DIR / "figure2_network_topology.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    print(f"\nSaved: {out_png}")
    print(f"Saved: {out_pdf}")

    # Print summary table for figure legend
    print("\n" + "=" * 70)
    print("FIGURE 2 DATA SUMMARY")
    print("=" * 70)
    for name, r in {**bio_reports, **ref_reports}.items():
        label = _nice_name(name) if name in bio_reports else name
        print(f"\n{label}:")
        print(f"  Nodes: {r.n_nodes}, Edges: {r.n_edges}")
        print(f"  Power-law α: {r.powerlaw_alpha:.2f}, Scale-free: {r.is_scale_free}")
        print(f"  Betweenness Gini: {r.betweenness_gini:.3f}")
        print(f"  Max betweenness node: {r.max_betweenness_node} ({r.max_betweenness:.3f})")
        print(f"  Clustering coefficient: {r.avg_clustering:.4f}")
        print(f"  Giant component: {r.giant_component_fraction:.1%}")
        print(f"  Robustness (random): {r.robustness_random_half:.1%} removed before GC<50%")
        print(f"  Robustness (targeted): {r.robustness_targeted_half:.1%} removed before GC<50%")

    plt.close()


def _nice_name(key: str) -> str:
    names = {
        "ecoli_ppi": "E. coli PPI",
        "yeast_ppi": "Yeast PPI",
        "ecoli_grn": "E. coli GRN",
    }
    return names.get(key, key)


if __name__ == "__main__":
    main()
