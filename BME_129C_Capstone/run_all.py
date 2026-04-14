"""
Living Systems as Decentralized Economies
==========================================
Master script — runs all three layers of analysis.

BME 129C Capstone, Sage Clokey, Spring 2026, UC Santa Cruz

Usage:
    python run_all.py              # run everything
    python run_all.py --layer 1    # run only Layer 1 (topology)
    python run_all.py --layer 1b   # run only Layer 1b (single-cell)
    python run_all.py --layer 2    # run only Layer 2 (economic modeling)
    python run_all.py --layer 3    # run only Layer 3 (trade network)
    python run_all.py --quick      # quick mode (skip API calls, use cached/built-in data)
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def run_layer1(quick: bool = False):
    """Layer 1: Network Topology — No Master Node"""
    print()
    print("=" * 70)
    print("  LAYER 1: NETWORK TOPOLOGY — 'No Master Node'")
    print("=" * 70)
    print()

    from layer1_topology.network_fetcher import load_all_networks, fetch_regulondb_grn
    from layer1_topology.topology_analysis import analyze_topology, plot_topology_report
    from layer1_topology.centralized_comparison import build_comparison_networks

    if quick:
        # Use built-in fallback (no API calls)
        from layer1_topology.network_fetcher import _builtin_ecoli_grn
        networks = {"ecoli_grn": _builtin_ecoli_grn()}
    else:
        networks = load_all_networks()

    # Analyze biological networks
    bio_reports = []
    for name, G in networks.items():
        print(f"\nAnalyzing {name}...")
        report = analyze_topology(G, name=name)
        bio_reports.append(report)
        print(report.summary())

    # Build and analyze comparison networks
    ref_n = max(G.number_of_nodes() for G in networks.values())
    ref_m = max(G.number_of_edges() for G in networks.values())
    ref_networks = build_comparison_networks(n_nodes=ref_n, n_edges=ref_m)

    ref_reports = []
    for name, G in ref_networks.items():
        print(f"\nAnalyzing reference: {name}...")
        report = analyze_topology(G, name=name)
        ref_reports.append(report)
        print(report.summary())

    # Plot
    print("\nGenerating Layer 1 figures...")
    plot_topology_report(bio_reports, ref_reports)

    return bio_reports, ref_reports


def run_layer1b():
    """Layer 1b: Single-Cell Economy — Cells as Economic Agents"""
    print()
    print("=" * 70)
    print("  LAYER 1b: SINGLE-CELL ECONOMY — 'Cells as Economic Agents'")
    print("=" * 70)
    print()

    from layer1_topology.single_cell_economy import (
        load_pbmc_data, analyze_cell_economy,
        _build_communication_network, plot_cell_economy,
    )

    adata = load_pbmc_data("scanpy")
    report = analyze_cell_economy(adata)
    print()
    print(report.summary())

    # Build communication graph for visualization
    cell_types = sorted(adata.obs["cell_type"].astype(str).unique())
    comm_graph = _build_communication_network(adata, cell_types)

    print("\nGenerating Layer 1b figures...")
    plot_cell_economy(adata, report, comm_graph)

    print("\nRobustness (fraction of communication surviving cell type removal):")
    for ct, score in sorted(report.robustness_scores.items(), key=lambda x: x[1]):
        print(f"  Remove {ct}: {score:.1%} edges survive")

    return report


def run_layer2():
    """Layer 2: Economic Modeling — Pathways as Agents"""
    print()
    print("=" * 70)
    print("  LAYER 2: ECONOMIC MODELING — 'Pathways as Agents'")
    print("=" * 70)
    print()

    from layer2_economy.metabolic_economy import (
        run_distributed, run_centralized,
        run_perturbation_test, compare_regimes, plot_economy,
    )

    base_supply = {
        "UDP-glucose": 1.0, "UDP-GlcNAc": 0.5, "Ca2+": 0.5,
        "O2": 2.0, "luciferin": 0.3, "glycine": 1.0,
        "alanine": 1.0, "glutamine": 0.5, "piRNA_precursors": 0.2,
        "Zn2+": 0.2, "cholesterol": 0.3,
    }

    print("Running distributed simulation...")
    dist = run_distributed(n_steps=200, base_supply=base_supply)

    print("Running centralized simulation...")
    cent = run_centralized(n_steps=200, base_supply=base_supply)

    print()
    print(compare_regimes(dist, cent))

    print("\nRunning perturbation test...")
    robustness = run_perturbation_test(n_steps=100)

    print("\nRobustness (GDP fraction retained after removing one agent):")
    print(f"{'Pathway Removed':<35} {'Distributed':>12} {'Centralized':>12}")
    print("-" * 60)
    for pathway_name in robustness["distributed"]:
        d = robustness["distributed"][pathway_name]
        c = robustness["centralized"][pathway_name]
        print(f"{pathway_name:<35} {d:>11.1%} {c:>11.1%}")

    print("\nGenerating Layer 2 figures...")
    plot_economy(dist, cent, robustness)

    return dist, cent, robustness


def run_layer3():
    """Layer 3: Cross-Species Trade — Comparative Advantage"""
    print()
    print("=" * 70)
    print("  LAYER 3: CROSS-SPECIES TRADE — 'Comparative Advantage'")
    print("=" * 70)
    print()

    from layer3_trade.trade_network import (
        build_trade_network, compute_trade_matrix,
        comparative_advantage_table, plot_trade_network,
    )

    G = build_trade_network()
    print(f"Trade network: {G.number_of_nodes()} organisms, {G.number_of_edges()} trade links")

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

    print("\nComparative Advantage:")
    for org, caps in comparative_advantage_table().items():
        print(f"  {org}: {', '.join(caps)}")

    print("\nFree Trade Zones (lowest cost pairs):")
    pairs = []
    for u, v, data in G.edges(data=True):
        pairs.append((u, v, data["trade_cost"]))
    pairs.sort(key=lambda x: x[2])
    for u, v, tc in pairs[:5]:
        print(f"  {u} <-> {v}: cost={tc:.3f}")

    print("\nGenerating Layer 3 figures...")
    plot_trade_network()

    return G, names, matrix


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Living Systems as Decentralized Economies — BME 129C Capstone",
    )
    parser.add_argument(
        "--layer", type=str, default="all",
        choices=["all", "1", "1b", "2", "3"],
        help="Which layer to run (default: all)",
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Quick mode: use built-in data, skip API calls",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("  LIVING SYSTEMS AS DECENTRALIZED ECONOMIES")
    print("  BME 129C Capstone — Sage Clokey — Spring 2026")
    print("=" * 70)

    if args.layer in ("all", "1"):
        run_layer1(quick=args.quick)

    if args.layer in ("all", "1b"):
        run_layer1b()

    if args.layer in ("all", "2"):
        run_layer2()

    if args.layer in ("all", "3"):
        run_layer3()

    print()
    print("=" * 70)
    print("  COMPLETE")
    print("  Figures saved to: paper/figures/")
    print("=" * 70)


if __name__ == "__main__":
    main()
