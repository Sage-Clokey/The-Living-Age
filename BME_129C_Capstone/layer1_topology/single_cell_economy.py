"""
Single-Cell Economy — Layer 1b
================================
Analyzes single-cell RNA sequencing data to show that cells in a tissue
behave as specialized agents in a decentralized economy.

Same genome. Different expression. No master cell. Emergent coordination.

Data Source:
    Pre-processed human PBMC (peripheral blood mononuclear cells) dataset.
    Options:
        1. CellxGene Census API (cellxgene_census) — curated, pre-annotated
        2. 10x Genomics free PBMC 10k dataset — direct H5AD download
        3. scanpy built-in pbmc3k dataset — smallest, good for testing

    All come pre-normalized and cell-type annotated.
    We do economic interpretation, not bioinformatics grunt work.

Analyses:
    1. UMAP as economic map — cell clusters = economic sectors
    2. Specialization score — expression entropy per cell type
       (low entropy = high specialization = comparative advantage)
    3. Cell-cell communication network — ligand-receptor interactions
       inferred from expression, built as a graph, shown to be decentralized
    4. Robustness — remove a cell type, measure communication network degradation

References:
    - Zheng et al., "Massively parallel digital transcriptional profiling
      of single cells," Nature Communications 2017
    - Ramilowski et al., "A draft network of ligand-receptor-mediated
      multicellular signalling in human," Nature Communications 2015
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx

# Lazy imports for heavy dependencies
scanpy = None
anndata = None

FIGURES_DIR = Path(__file__).resolve().parent.parent / "paper" / "figures"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

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


# ---------------------------------------------------------------------------
# Curated ligand-receptor database
# ---------------------------------------------------------------------------
# Subset of well-characterized human ligand-receptor pairs relevant to
# immune cell communication. Source: Ramilowski et al. 2015, CellChat DB.

LIGAND_RECEPTOR_PAIRS = [
    # (ligand_gene, receptor_gene, pathway/function)
    ("TNF", "TNFRSF1A", "inflammation"),
    ("TNF", "TNFRSF1B", "inflammation"),
    ("IFNG", "IFNGR1", "antiviral/activation"),
    ("IL2", "IL2RA", "T cell proliferation"),
    ("IL2", "IL2RB", "T cell proliferation"),
    ("IL6", "IL6R", "acute phase response"),
    ("IL10", "IL10RA", "anti-inflammatory"),
    ("IL4", "IL4R", "Th2 differentiation"),
    ("IL1B", "IL1R1", "inflammation"),
    ("CXCL8", "CXCR1", "neutrophil chemotaxis"),
    ("CXCL8", "CXCR2", "neutrophil chemotaxis"),
    ("CCL2", "CCR2", "monocyte recruitment"),
    ("CCL5", "CCR5", "T cell/monocyte chemotaxis"),
    ("CXCL12", "CXCR4", "homing/migration"),
    ("CXCL10", "CXCR3", "Th1 chemotaxis"),
    ("CD40LG", "CD40", "B cell activation"),
    ("FASLG", "FAS", "apoptosis"),
    ("TGFB1", "TGFBR1", "immunosuppression"),
    ("TGFB1", "TGFBR2", "immunosuppression"),
    ("CSF1", "CSF1R", "macrophage survival"),
    ("CSF2", "CSF2RA", "myeloid differentiation"),
    ("VEGFA", "FLT1", "angiogenesis"),
    ("HLA-A", "CD8A", "antigen presentation"),
    ("HLA-DRA", "CD4", "antigen presentation"),
    ("ICAM1", "ITGAL", "adhesion/immune synapse"),
    ("CD80", "CD28", "co-stimulation"),
    ("CD80", "CTLA4", "co-inhibition"),
    ("PDL1", "PDCD1", "immune checkpoint"),
    ("BTLA", "TNFRSF14", "co-inhibition"),
    ("LTA", "LTBR", "lymphoid organogenesis"),
]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _import_scanpy():
    """Lazy import scanpy to avoid startup cost."""
    global scanpy, anndata
    if scanpy is None:
        import scanpy as _sc
        import anndata as _ad
        scanpy = _sc
        anndata = _ad


def load_pbmc_data(source: str = "scanpy") -> "anndata.AnnData":
    """
    Load pre-processed PBMC single-cell dataset.

    Args:
        source: 'scanpy' (built-in pbmc3k, smallest),
                'cellxgene' (CellxGene Census API, larger),
                or a path to an .h5ad file

    Returns:
        AnnData object with cell type annotations in adata.obs['cell_type']
    """
    _import_scanpy()

    if source == "scanpy":
        print("[single-cell] Loading scanpy pbmc3k dataset (full gene set)...")
        # Load processed for cell type labels and UMAP coordinates
        processed = scanpy.datasets.pbmc3k_processed()
        if "louvain" in processed.obs.columns and "cell_type" not in processed.obs.columns:
            processed.obs["cell_type"] = processed.obs["louvain"]

        # Load raw for full gene set (needed for ligand-receptor analysis)
        raw = scanpy.datasets.pbmc3k()
        # Basic preprocessing of raw data
        scanpy.pp.filter_cells(raw, min_genes=200)
        scanpy.pp.filter_genes(raw, min_cells=3)
        scanpy.pp.normalize_total(raw, target_sum=1e4)
        scanpy.pp.log1p(raw)

        # Transfer cell type labels and UMAP from processed to raw
        # Match by cell barcode (index)
        common_cells = raw.obs.index.intersection(processed.obs.index)
        raw = raw[common_cells].copy()
        raw.obs["cell_type"] = processed.obs.loc[common_cells, "cell_type"]
        if "X_umap" in processed.obsm:
            raw.obsm["X_umap"] = processed[common_cells].obsm["X_umap"]

        adata = raw
        print(f"[single-cell] Loaded: {adata.n_obs} cells, {adata.n_vars} genes")
        return adata

    elif source == "cellxgene":
        print("[single-cell] Loading from CellxGene Census...")
        try:
            import cellxgene_census
            census = cellxgene_census.open_soma()
            adata = cellxgene_census.get_anndata(
                census,
                organism="Homo sapiens",
                obs_value_filter="tissue_general == 'blood' and disease == 'normal'",
                obs_column_names=["cell_type", "tissue", "assay"],
            )
            # Subsample if too large
            if adata.n_obs > 20000:
                scanpy.pp.subsample(adata, n_obs=20000, random_state=42)
            print(f"[single-cell] Loaded: {adata.n_obs} cells, {adata.n_vars} genes")
            return adata
        except ImportError:
            print("[single-cell] cellxgene_census not installed. Falling back to scanpy dataset.")
            return load_pbmc_data("scanpy")

    else:
        # Assume it's a file path
        print(f"[single-cell] Loading from {source}...")
        adata = anndata.read_h5ad(source)
        print(f"[single-cell] Loaded: {adata.n_obs} cells, {adata.n_vars} genes")
        return adata


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

@dataclass
class CellEconomyReport:
    """Results of single-cell economic analysis."""
    n_cells: int = 0
    n_genes: int = 0
    n_cell_types: int = 0
    cell_type_counts: dict[str, int] = field(default_factory=dict)

    # Specialization: entropy per cell type (lower = more specialized)
    specialization_scores: dict[str, float] = field(default_factory=dict)
    # Most specialized (lowest entropy) cell type
    most_specialized: str = ""
    # Least specialized (highest entropy) cell type
    least_specialized: str = ""

    # Communication network
    communication_edges: int = 0
    communication_nodes: int = 0
    comm_betweenness_gini: float = 0.0
    comm_max_betweenness_node: str = ""
    comm_is_decentralized: bool = False

    # Robustness
    robustness_scores: dict[str, float] = field(default_factory=dict)
    # cell_type -> fraction of communication edges remaining after removal

    def summary(self) -> str:
        return (
            f"[Single-Cell Economy] {self.n_cells} cells, {self.n_genes} genes, "
            f"{self.n_cell_types} cell types\n"
            f"  Most specialized: {self.most_specialized} "
            f"(entropy={self.specialization_scores.get(self.most_specialized, 0):.3f})\n"
            f"  Least specialized: {self.least_specialized} "
            f"(entropy={self.specialization_scores.get(self.least_specialized, 0):.3f})\n"
            f"  Communication network: {self.communication_nodes} nodes, "
            f"{self.communication_edges} edges\n"
            f"  Betweenness Gini: {self.comm_betweenness_gini:.3f} "
            f"(decentralized={self.comm_is_decentralized})\n"
            f"  Most central communicator: {self.comm_max_betweenness_node}"
        )


def analyze_cell_economy(adata: "anndata.AnnData") -> CellEconomyReport:
    """
    Run full economic analysis on single-cell data.

    1. Compute specialization scores (expression entropy per cell type)
    2. Build cell-cell communication network from ligand-receptor pairs
    3. Analyze communication network topology
    4. Measure robustness (cell type removal)
    """
    _import_scanpy()

    report = CellEconomyReport(
        n_cells=adata.n_obs,
        n_genes=adata.n_vars,
    )

    cell_types = adata.obs["cell_type"].astype(str)
    unique_types = sorted(cell_types.unique())
    report.n_cell_types = len(unique_types)
    report.cell_type_counts = cell_types.value_counts().to_dict()

    # --- 1. Specialization scores (expression entropy) ---
    print("[single-cell] Computing specialization scores...")
    report.specialization_scores = _compute_specialization(adata, unique_types)

    if report.specialization_scores:
        report.most_specialized = min(
            report.specialization_scores, key=report.specialization_scores.get
        )
        report.least_specialized = max(
            report.specialization_scores, key=report.specialization_scores.get
        )

    # --- 2. Cell-cell communication network ---
    print("[single-cell] Building communication network...")
    comm_graph = _build_communication_network(adata, unique_types)

    report.communication_nodes = comm_graph.number_of_nodes()
    report.communication_edges = comm_graph.number_of_edges()

    if comm_graph.number_of_nodes() > 1:
        bc = nx.betweenness_centrality(comm_graph, weight="weight")
        bc_values = list(bc.values())
        report.comm_betweenness_gini = _gini(bc_values)
        report.comm_max_betweenness_node = max(bc, key=bc.get) if bc else ""
        # Decentralized if Gini < 0.5 (no single dominant communicator)
        report.comm_is_decentralized = report.comm_betweenness_gini < 0.5

    # --- 3. Robustness ---
    print("[single-cell] Testing robustness (cell type removal)...")
    report.robustness_scores = _robustness_cell_removal(comm_graph, unique_types)

    return report


def _compute_specialization(
    adata: "anndata.AnnData",
    cell_types: list[str],
) -> dict[str, float]:
    """
    Compute expression entropy for each cell type.

    Low entropy = few genes dominate expression = high specialization.
    High entropy = many genes expressed equally = generalist.

    This is comparative advantage: a cell type with low entropy has
    invested its transcriptional resources into a narrow program.
    """
    _import_scanpy()
    scores = {}

    for ct in cell_types:
        mask = adata.obs["cell_type"].astype(str) == ct
        if mask.sum() == 0:
            continue

        # Mean expression per gene across cells of this type
        subset = adata[mask]
        if hasattr(subset.X, "toarray"):
            mean_expr = np.array(subset.X.toarray().mean(axis=0)).flatten()
        else:
            mean_expr = np.array(subset.X.mean(axis=0)).flatten()

        # Normalize to probability distribution
        total = mean_expr.sum()
        if total == 0:
            scores[ct] = 0.0
            continue

        p = mean_expr / total
        p = p[p > 0]  # remove zeros for log

        # Shannon entropy
        entropy = -np.sum(p * np.log2(p))

        # Normalize by max possible entropy (log2 of number of expressed genes)
        max_entropy = np.log2(len(p)) if len(p) > 0 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        scores[ct] = normalized_entropy

    return scores


def _build_communication_network(
    adata: "anndata.AnnData",
    cell_types: list[str],
) -> nx.Graph:
    """
    Build cell-cell communication network from ligand-receptor expression.

    Nodes = cell types
    Edges = active ligand-receptor channels between cell types
    Edge weight = number of active L-R pairs

    A ligand-receptor pair is "active" between cell type A and B if:
        - Cell type A expresses the ligand (mean expression > threshold)
        - Cell type B expresses the receptor (mean expression > threshold)
    """
    _import_scanpy()
    G = nx.Graph()

    # Get gene names from adata
    gene_names = set(adata.var_names)

    # Filter L-R pairs to those present in the dataset
    available_pairs = []
    for ligand, receptor, pathway in LIGAND_RECEPTOR_PAIRS:
        if ligand in gene_names and receptor in gene_names:
            available_pairs.append((ligand, receptor, pathway))

    if not available_pairs:
        print(f"  Warning: no L-R pairs found in gene set. Available: {len(gene_names)} genes")
        # Try case-insensitive matching
        gene_upper = {g.upper(): g for g in gene_names}
        for ligand, receptor, pathway in LIGAND_RECEPTOR_PAIRS:
            l_match = gene_upper.get(ligand.upper())
            r_match = gene_upper.get(receptor.upper())
            if l_match and r_match:
                available_pairs.append((l_match, r_match, pathway))

    print(f"  {len(available_pairs)} ligand-receptor pairs available in dataset")

    # Compute mean expression per cell type for each L-R gene
    ct_expression = {}
    for ct in cell_types:
        mask = adata.obs["cell_type"].astype(str) == ct
        if mask.sum() == 0:
            continue
        subset = adata[mask]
        if hasattr(subset.X, "toarray"):
            means = pd.Series(
                np.array(subset.X.toarray().mean(axis=0)).flatten(),
                index=adata.var_names,
            )
        else:
            means = pd.Series(
                np.array(subset.X.mean(axis=0)).flatten(),
                index=adata.var_names,
            )
        ct_expression[ct] = means

    # Threshold: gene is "expressed" if mean > 0.1 (log-normalized data)
    threshold = 0.1

    # Build edges
    for ct_a in cell_types:
        if ct_a not in ct_expression:
            continue
        G.add_node(ct_a)
        for ct_b in cell_types:
            if ct_b not in ct_expression:
                continue
            G.add_node(ct_b)

            # Count active L-R channels from A (ligand) to B (receptor)
            n_channels = 0
            active_channels = []
            for ligand, receptor, pathway in available_pairs:
                lig_expr = ct_expression[ct_a].get(ligand, 0)
                rec_expr = ct_expression[ct_b].get(receptor, 0)
                if lig_expr > threshold and rec_expr > threshold:
                    n_channels += 1
                    active_channels.append(pathway)

            if n_channels > 0 and ct_a != ct_b:
                # Add or update edge
                if G.has_edge(ct_a, ct_b):
                    G[ct_a][ct_b]["weight"] += n_channels
                    G[ct_a][ct_b]["channels"].extend(active_channels)
                else:
                    G.add_edge(ct_a, ct_b, weight=n_channels, channels=active_channels)

    return G


def _robustness_cell_removal(
    comm_graph: nx.Graph,
    cell_types: list[str],
) -> dict[str, float]:
    """
    For each cell type, remove it and measure what fraction of
    communication edges survive. Decentralized systems should show
    graceful degradation — no single removal destroys the network.
    """
    total_edges = comm_graph.number_of_edges()
    if total_edges == 0:
        return {}

    scores = {}
    for ct in cell_types:
        if ct not in comm_graph:
            scores[ct] = 1.0
            continue

        H = comm_graph.copy()
        H.remove_node(ct)
        remaining_edges = H.number_of_edges()
        scores[ct] = remaining_edges / total_edges

    return scores


def _gini(values: list[float]) -> float:
    """Gini coefficient. 0 = equal, 1 = maximally unequal."""
    arr = np.array(sorted(values))
    n = len(arr)
    if n == 0 or arr.sum() == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * arr) - (n + 1) * arr.sum()) / (n * arr.sum())


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_cell_economy(
    adata: "anndata.AnnData",
    report: CellEconomyReport,
    comm_graph: nx.Graph = None,
    save: bool = True,
) -> plt.Figure:
    """
    Generate a 3-panel single-cell economy figure.

    Panel 1: UMAP colored by cell type (the economic map)
    Panel 2: Specialization scores per cell type (comparative advantage)
    Panel 3: Cell-cell communication network (decentralized coordination)
    """
    _import_scanpy()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(18, 6), facecolor=BACKGROUND)
    gs = gridspec.GridSpec(1, 3, wspace=0.3)

    # --- Panel 1: UMAP ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(PANEL_BG)

    if "X_umap" in adata.obsm:
        umap_coords = adata.obsm["X_umap"]
        cell_types = adata.obs["cell_type"].astype(str)
        unique_ct = sorted(cell_types.unique())

        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_ct)))
        for i, ct in enumerate(unique_ct):
            mask = cell_types == ct
            ax1.scatter(
                umap_coords[mask, 0], umap_coords[mask, 1],
                s=3, alpha=0.5, color=colors[i], label=ct,
            )

        ax1.legend(
            fontsize=6, markerscale=3, facecolor=PANEL_BG,
            edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN,
            loc="upper left", ncol=1,
        )
    else:
        ax1.text(0.5, 0.5, "No UMAP available", transform=ax1.transAxes,
                 color=TEXT_DIM, ha="center", fontsize=12)

    ax1.set_xlabel("UMAP 1", color=TEXT_MAIN)
    ax1.set_ylabel("UMAP 2", color=TEXT_MAIN)
    ax1.set_title("Economic Map: Cell Type Sectors", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax1.tick_params(colors=TEXT_DIM)

    # --- Panel 2: Specialization Scores ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(PANEL_BG)

    if report.specialization_scores:
        sorted_ct = sorted(
            report.specialization_scores.items(),
            key=lambda x: x[1],
        )
        names = [ct for ct, _ in sorted_ct]
        scores = [s for _, s in sorted_ct]
        colors_bar = [SPIRAL_GREEN if s < 0.85 else GOLD for s in scores]

        y_pos = np.arange(len(names))
        ax2.barh(y_pos, scores, color=colors_bar, edgecolor=TEXT_DIM, linewidth=0.5)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(names, fontsize=8, color=TEXT_MAIN)
        ax2.set_xlabel("Normalized Entropy (lower = more specialized)", color=TEXT_MAIN, fontsize=10)
        ax2.axvline(x=0.85, color=TEXT_DIM, linestyle="--", linewidth=0.8, alpha=0.5)
        ax2.text(0.855, len(names) - 0.5, "generalist →", color=TEXT_DIM, fontsize=7)

    ax2.set_title("Division of Labor: Specialization", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax2.tick_params(colors=TEXT_DIM)

    # --- Panel 3: Communication Network ---
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(PANEL_BG)

    if comm_graph and comm_graph.number_of_nodes() > 0:
        pos = nx.spring_layout(comm_graph, seed=42, k=2)

        # Node sizes proportional to degree
        degrees = dict(comm_graph.degree(weight="weight"))
        max_deg = max(degrees.values()) if degrees and max(degrees.values()) > 0 else 1
        node_sizes = [300 + 700 * (degrees.get(n, 0) / max_deg) for n in comm_graph.nodes()]

        # Edge widths proportional to weight
        edge_weights = [comm_graph[u][v].get("weight", 1) for u, v in comm_graph.edges()]
        max_w = max(edge_weights) if edge_weights else 1
        edge_widths = [1 + 3 * (w / max_w) for w in edge_weights]

        nx.draw_networkx_edges(
            comm_graph, pos, ax=ax3,
            width=edge_widths, edge_color=SPIRAL_LIGHT, alpha=0.4,
        )
        nx.draw_networkx_nodes(
            comm_graph, pos, ax=ax3,
            node_size=node_sizes, node_color=SPIRAL_MID, edgecolors=TEXT_DIM,
        )
        nx.draw_networkx_labels(
            comm_graph, pos, ax=ax3,
            font_size=7, font_color=TEXT_MAIN,
        )

        # Annotate Gini
        ax3.text(
            0.02, 0.02,
            f"Betweenness Gini: {report.comm_betweenness_gini:.3f}\n"
            f"({'Decentralized' if report.comm_is_decentralized else 'Centralized'})",
            transform=ax3.transAxes, fontsize=8, color=GOLD,
            verticalalignment="bottom",
        )

    ax3.set_title("Communication Network", color=TEXT_MAIN, fontsize=13, fontweight="bold")
    ax3.axis("off")

    fig.suptitle(
        "Layer 1b: Cells Are a Decentralized Economy",
        color=GOLD, fontsize=15, fontweight="bold", y=1.02,
    )

    plt.tight_layout()

    if save:
        out = FIGURES_DIR / "layer1b_single_cell_economy.png"
        fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BACKGROUND)
        print(f"[single-cell] Saved figure to {out}")

    return fig


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Layer 1b: Single-Cell Economy Analysis")
    print("=" * 60)
    print()

    # Load data
    adata = load_pbmc_data("scanpy")

    # Analyze
    report = analyze_cell_economy(adata)
    print()
    print(report.summary())

    # Build communication graph for visualization
    cell_types = sorted(adata.obs["cell_type"].astype(str).unique())
    comm_graph = _build_communication_network(adata, cell_types)

    # Plot
    print("\nGenerating figures...")
    plot_cell_economy(adata, report, comm_graph)

    # Print robustness
    print("\nRobustness (fraction of communication surviving cell type removal):")
    for ct, score in sorted(report.robustness_scores.items(), key=lambda x: x[1]):
        print(f"  Remove {ct}: {score:.1%} edges survive")

    print("\nDone.")
