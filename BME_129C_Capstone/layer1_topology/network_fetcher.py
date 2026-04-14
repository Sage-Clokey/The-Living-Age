"""
Network Fetcher — Layer 1: Network Topology
============================================
Retrieves real biological networks from public databases and constructs
NetworkX graphs for topological analysis.

Data Sources:
    1. RegulonDB — E. coli gene regulatory network (TF → gene interactions)
       Gold standard for prokaryotic GRN. ~4,500 regulatory interactions.
       Download: regulondb.ccg.unam.mx/menu/download/datasets/

    2. KEGG REST API — Metabolic pathway networks
       Reaction networks for E. coli (eco), yeast (sce), human (hsa).
       Nodes = enzymes + metabolites, edges = reactions.

    3. STRING — Protein-protein interaction networks
       High-confidence physical and functional associations.
       E. coli (taxid 511145), yeast (taxid 4932).

Each network is cached locally after first fetch to avoid repeated API calls.
"""

from __future__ import annotations
import os
import json
import time
import csv
import io
from pathlib import Path

import requests
import networkx as nx

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REGULONDB_DIR = DATA_DIR / "regulondb"
KEGG_DIR = DATA_DIR / "kegg"
STRING_DIR = DATA_DIR / "string"


# ---------------------------------------------------------------------------
# 1. RegulonDB — E. coli Gene Regulatory Network
# ---------------------------------------------------------------------------

REGULONDB_URL = (
    "https://regulondb.ccg.unam.mx/menu/download/datasets/"
    "files/network_tf_gene.txt"
)

# Backup: curated dataset embedded as fallback
# RegulonDB format: TF_name \t gene_name \t regulatory_effect (+/-/?)
# Lines starting with # are comments


def fetch_regulondb_grn(force: bool = False) -> nx.DiGraph:
    """
    Fetch E. coli gene regulatory network from RegulonDB.

    Returns a directed graph where:
        - Nodes = genes and transcription factors
        - Edges = regulatory interactions (activation/repression)
        - Edge attributes: effect ('+' = activation, '-' = repression, '?' = unknown)
    """
    cache_file = REGULONDB_DIR / "network_tf_gene.txt"

    if cache_file.exists() and not force:
        print(f"[RegulonDB] Loading cached GRN from {cache_file}")
        text = cache_file.read_text(encoding="utf-8", errors="replace")
    else:
        print(f"[RegulonDB] Downloading E. coli GRN...")
        try:
            resp = requests.get(REGULONDB_URL, timeout=30)
            resp.raise_for_status()
            text = resp.text
            REGULONDB_DIR.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(text, encoding="utf-8")
            print(f"[RegulonDB] Cached to {cache_file}")
        except requests.RequestException as e:
            print(f"[RegulonDB] Download failed: {e}")
            print("[RegulonDB] Falling back to built-in E. coli GRN subset...")
            return _builtin_ecoli_grn()

    return _parse_regulondb(text)


def _parse_regulondb(text: str) -> nx.DiGraph:
    """Parse RegulonDB TF-gene network file into a NetworkX DiGraph."""
    G = nx.DiGraph()

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split("\t")
        if len(parts) < 3:
            continue

        tf = parts[0].strip()
        gene = parts[1].strip()
        effect = parts[2].strip() if len(parts) > 2 else "?"

        if not tf or not gene:
            continue

        G.add_node(tf, node_type="TF")
        G.add_node(gene, node_type="gene")
        G.add_edge(tf, gene, effect=effect)

    print(f"[RegulonDB] Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


def _builtin_ecoli_grn() -> nx.DiGraph:
    """
    Fallback: a curated subset of the E. coli GRN based on well-known
    regulatory interactions from the literature.
    """
    G = nx.DiGraph()

    # Major E. coli transcription factors and their targets
    # Source: RegulonDB literature, Shen-Orr et al. 2002
    interactions = [
        # CRP (global regulator) — activates ~200 operons
        ("CRP", "lacZ", "+"), ("CRP", "galE", "+"), ("CRP", "malT", "+"),
        ("CRP", "araC", "+"), ("CRP", "manX", "+"), ("CRP", "glpF", "+"),
        ("CRP", "tsx", "+"), ("CRP", "ompA", "+"), ("CRP", "deoC", "+"),
        ("CRP", "ptsG", "+"), ("CRP", "aceB", "+"), ("CRP", "glpA", "+"),
        ("CRP", "rbsA", "+"), ("CRP", "uxuA", "+"), ("CRP", "nmpC", "+"),
        # FNR — anaerobic regulator
        ("FNR", "narG", "+"), ("FNR", "dmsA", "+"), ("FNR", "focA", "+"),
        ("FNR", "nirB", "+"), ("FNR", "aspA", "+"), ("FNR", "frdA", "+"),
        ("FNR", "ndh", "-"), ("FNR", "cyoA", "-"), ("FNR", "cydA", "+"),
        # ArcA — aerobic respiration control
        ("ArcA", "cyoA", "-"), ("ArcA", "cydA", "+"), ("ArcA", "sdh", "-"),
        ("ArcA", "lctD", "+"), ("ArcA", "icdA", "-"),
        # LexA — SOS response
        ("LexA", "recA", "-"), ("LexA", "uvrA", "-"), ("LexA", "sulA", "-"),
        ("LexA", "umuD", "-"), ("LexA", "dinF", "-"),
        # Fur — iron homeostasis
        ("Fur", "fepA", "-"), ("Fur", "fhuA", "-"), ("Fur", "tonB", "-"),
        ("Fur", "entC", "-"), ("Fur", "cirA", "-"), ("Fur", "sodB", "+"),
        # IHF — DNA bending / chromatin
        ("IHF", "nifH", "+"), ("IHF", "ilvG", "+"), ("IHF", "xylA", "+"),
        # Fis — growth phase dependent
        ("Fis", "rrnB", "+"), ("Fis", "rrnA", "+"), ("Fis", "rrnC", "+"),
        ("Fis", "rrnD", "+"), ("Fis", "tyrT", "+"), ("Fis", "nrd", "+"),
        # H-NS — silencing xenogeneic DNA
        ("H-NS", "proV", "-"), ("H-NS", "bglG", "-"), ("H-NS", "csgD", "-"),
        ("H-NS", "flhD", "-"), ("H-NS", "gadA", "-"),
        # OxyR — oxidative stress
        ("OxyR", "katG", "+"), ("OxyR", "ahpC", "+"), ("OxyR", "gorA", "+"),
        ("OxyR", "grxA", "+"), ("OxyR", "dps", "+"),
        # RpoS — stationary phase sigma factor
        ("RpoS", "osmY", "+"), ("RpoS", "bolA", "+"), ("RpoS", "dps", "+"),
        ("RpoS", "katE", "+"), ("RpoS", "gadB", "+"), ("RpoS", "otsA", "+"),
        # NarL — nitrate/nitrite response
        ("NarL", "narG", "+"), ("NarL", "nirB", "+"), ("NarL", "frdA", "-"),
        ("NarL", "dmsA", "-"),
        # LacI — lac operon repressor
        ("LacI", "lacZ", "-"), ("LacI", "lacY", "-"), ("LacI", "lacA", "-"),
        # AraC — arabinose operon
        ("AraC", "araB", "+"), ("AraC", "araA", "+"), ("AraC", "araD", "+"),
        # TrpR — tryptophan repressor
        ("TrpR", "trpE", "-"), ("TrpR", "trpD", "-"), ("TrpR", "trpC", "-"),
        # PhoB — phosphate starvation
        ("PhoB", "phoA", "+"), ("PhoB", "pstS", "+"), ("PhoB", "ugpB", "+"),
        # FlhDC — flagellar master regulator
        ("FlhDC", "flgA", "+"), ("FlhDC", "fliA", "+"), ("FlhDC", "fliC", "+"),
        ("FlhDC", "motA", "+"),
        # Cross-regulation (TF regulating TF)
        ("CRP", "flhD", "+"), ("H-NS", "rpoS", "-"), ("RpoS", "csgD", "+"),
        ("FNR", "arcA", "+"), ("OxyR", "fur", "+"),
    ]

    for tf, gene, effect in interactions:
        G.add_node(tf, node_type="TF")
        G.add_node(gene, node_type="gene")
        G.add_edge(tf, gene, effect=effect)

    print(f"[RegulonDB-builtin] Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


# ---------------------------------------------------------------------------
# 2. KEGG REST API — Metabolic Networks
# ---------------------------------------------------------------------------

KEGG_BASE = "https://rest.kegg.jp"

# Key metabolic pathways to fetch
KEGG_PATHWAYS = {
    "eco": {  # E. coli
        "eco00010": "Glycolysis / Gluconeogenesis",
        "eco00020": "Citrate cycle (TCA cycle)",
        "eco00190": "Oxidative phosphorylation",
        "eco00230": "Purine metabolism",
        "eco00240": "Pyrimidine metabolism",
        "eco00061": "Fatty acid biosynthesis",
        "eco00260": "Glycine, serine and threonine metabolism",
        "eco00620": "Pyruvate metabolism",
    },
    "sce": {  # Yeast
        "sce00010": "Glycolysis / Gluconeogenesis",
        "sce00020": "Citrate cycle (TCA cycle)",
        "sce00190": "Oxidative phosphorylation",
    },
}


def fetch_kegg_metabolic_network(
    organism: str = "eco",
    force: bool = False,
) -> nx.DiGraph:
    """
    Build a metabolic network from KEGG pathway data.

    Nodes = enzymes (EC numbers) + metabolites (compound IDs)
    Edges = reaction links (enzyme catalyzes conversion of compound A to B)

    Returns a directed graph representing metabolic flow.
    """
    cache_file = KEGG_DIR / f"{organism}_metabolic_network.json"
    raw_cache = KEGG_DIR / f"{organism}_pathways.json"

    # Check if we have a valid cached network (non-empty)
    if cache_file.exists() and not force:
        data = json.loads(cache_file.read_text())
        if data.get("nodes"):
            print(f"[KEGG] Loading cached {organism} metabolic network...")
            G = nx.node_link_graph(data)
            print(f"[KEGG] Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
            return G

    # Build from raw pathway cache if available (preferred — avoids flaky API)
    if raw_cache.exists():
        print(f"[KEGG] Building {organism} metabolic network from cached pathway data...")
        G = _build_kegg_network_from_cache(raw_cache)
        data = nx.node_link_data(G)
        cache_file.write_text(json.dumps(data, indent=2))
        print(f"[KEGG] Built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G

    # Fallback: fetch from API
    print(f"[KEGG] Fetching {organism} metabolic pathways...")
    KEGG_DIR.mkdir(parents=True, exist_ok=True)

    G = nx.DiGraph()
    pathways = KEGG_PATHWAYS.get(organism, {})

    for pathway_id, pathway_name in pathways.items():
        print(f"  Fetching {pathway_id}: {pathway_name}...")
        try:
            resp = requests.get(f"{KEGG_BASE}/get/{pathway_id}", timeout=15)
            resp.raise_for_status()
            time.sleep(0.5)
            _parse_kegg_pathway_text(G, resp.text, pathway_name)
        except requests.RequestException as e:
            print(f"  Warning: failed to fetch {pathway_id}: {e}")

    # Cache the result
    data = nx.node_link_data(G)
    cache_file.write_text(json.dumps(data, indent=2))
    print(f"[KEGG] Built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"[KEGG] Cached to {cache_file}")

    return G


def _build_kegg_network_from_cache(raw_cache: Path) -> nx.DiGraph:
    """Build a metabolic network from cached pathway JSON.

    Creates a bipartite-style network: genes and compounds within the same
    pathway are connected (gene → compound = catalysis, compound → gene =
    substrate usage). Genes sharing compounds across pathways get indirect
    connections, creating the metabolic web.
    """
    pathways = json.loads(raw_cache.read_text())
    G = nx.DiGraph()

    for pathway_id, pdata in pathways.items():
        pathway_name = pdata.get("name", pathway_id)
        genes = pdata.get("genes", [])
        compounds = pdata.get("compounds", [])

        # Add nodes
        for g in genes:
            G.add_node(g, node_type="gene", pathway=pathway_name)
        for c in compounds:
            G.add_node(c, node_type="compound", pathway=pathway_name)

        # Connect genes to compounds within pathway (bipartite edges)
        # Each gene in a pathway is linked to the compounds it processes
        for g in genes:
            for c in compounds:
                G.add_edge(g, c, pathway=pathway_name, edge_type="catalysis")

    # The bipartite graph is very dense; project onto compound-compound network
    # by connecting compounds that share genes (co-metabolism)
    compound_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "compound"]
    gene_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "gene"]

    # Build projected network: compounds linked if they share a gene
    G_projected = nx.DiGraph()
    for c in compound_nodes:
        G_projected.add_node(c, node_type="compound")
    for g in gene_nodes:
        G_projected.add_node(g, node_type="gene")

    # Gene-gene edges: genes sharing a compound
    from collections import defaultdict
    compound_to_genes: dict[str, set[str]] = defaultdict(set)
    for g in gene_nodes:
        for c in G.successors(g):
            if G.nodes[c].get("node_type") == "compound":
                compound_to_genes[c].add(g)

    for c, gene_set in compound_to_genes.items():
        gene_list = sorted(gene_set)
        for i, g1 in enumerate(gene_list):
            G_projected.add_node(g1, node_type="gene")
            for g2 in gene_list[i + 1:]:
                G_projected.add_edge(g1, g2, shared_compound=c)
                G_projected.add_edge(g2, g1, shared_compound=c)

    # Also add compound-compound edges: compounds in the same pathway
    from itertools import combinations
    pathway_compounds: dict[str, list[str]] = defaultdict(list)
    for pathway_id, pdata in json.loads(raw_cache.read_text()).items():
        for c in pdata.get("compounds", []):
            pathway_compounds[pathway_id].append(c)

    for pid, cpds in pathway_compounds.items():
        for c1, c2 in combinations(cpds, 2):
            G_projected.add_edge(c1, c2, pathway=pid)

    return G_projected


def _parse_kegg_pathway_text(G: nx.DiGraph, text: str, pathway_name: str):
    """Parse a KEGG pathway GET response into graph edges."""
    import re
    genes = []
    compounds = []
    for line in text.split("\n"):
        if line.startswith("GENE") or (genes and line.startswith("            ")):
            gene_match = re.findall(r"(\d+)\s+(\w+);", line)
            for _, gene_name in gene_match:
                genes.append(gene_name)
        if "cpd:" in line:
            compounds.extend(re.findall(r"cpd:(C\d{5})", line))

    for g in genes:
        G.add_node(g, node_type="gene", pathway=pathway_name)
    for c in set(compounds):
        G.add_node(c, node_type="compound", pathway=pathway_name)
    for g in genes:
        for c in set(compounds):
            G.add_edge(g, c, pathway=pathway_name)


# ---------------------------------------------------------------------------
# 3. STRING — Protein-Protein Interaction Network
# ---------------------------------------------------------------------------

STRING_API = "https://string-db.org/api"

# Organism taxonomy IDs
STRING_SPECIES = {
    "ecoli": 511145,      # E. coli K-12 MG1655
    "yeast": 4932,        # S. cerevisiae
    "human": 9606,        # H. sapiens
}


def fetch_string_ppi(
    organism: str = "ecoli",
    score_threshold: int = 700,
    force: bool = False,
) -> nx.Graph:
    """
    Fetch protein-protein interaction network from STRING database.

    Args:
        organism: key from STRING_SPECIES
        score_threshold: minimum combined score (0-1000). 700 = high confidence.
        force: re-download even if cached

    Returns undirected graph where:
        - Nodes = proteins
        - Edges = interactions with confidence score
    """
    species = STRING_SPECIES.get(organism)
    if not species:
        raise ValueError(f"Unknown organism '{organism}'. Choose from: {list(STRING_SPECIES)}")

    cache_file = STRING_DIR / f"{organism}_ppi_{score_threshold}.json"
    # Also check for cache files without score suffix (from bulk download scripts)
    cache_file_alt = STRING_DIR / f"{organism}_ppi.json"

    for cf in (cache_file, cache_file_alt):
        if cf.exists() and not force:
            print(f"[STRING] Loading cached {organism} PPI network from {cf.name}...")
            data = json.loads(cf.read_text())

            # Handle two cache formats:
            # 1. NetworkX node_link_data dict (from our own caching)
            # 2. List of {protein_a, protein_b, score} dicts (from download scripts)
            if isinstance(data, list):
                G = nx.Graph()
                for row in data:
                    a = row.get("protein_a", "")
                    b = row.get("protein_b", "")
                    s = float(row.get("score", 0))
                    if a and b:
                        G.add_node(a, node_type="protein")
                        G.add_node(b, node_type="protein")
                        G.add_edge(a, b, score=s)
            else:
                G = nx.node_link_graph(data)

            print(f"[STRING] Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
            return G

    print(f"[STRING] Fetching {organism} PPI network (taxid={species})...")
    STRING_DIR.mkdir(parents=True, exist_ok=True)

    G = nx.Graph()

    # STRING bulk download via the network endpoint
    # Use a set of well-known genes as seeds, then expand
    seed_genes = _get_seed_genes(organism)

    for batch_start in range(0, len(seed_genes), 10):
        batch = seed_genes[batch_start:batch_start + 10]
        identifiers = "%0d".join(batch)

        try:
            url = (
                f"{STRING_API}/tsv/network"
                f"?identifiers={identifiers}"
                f"&species={species}"
                f"&required_score={score_threshold}"
                f"&limit=200"
            )
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            time.sleep(1.0)  # STRING rate limit

            reader = csv.DictReader(io.StringIO(resp.text), delimiter="\t")
            for row in reader:
                prot_a = row.get("preferredName_A", row.get("stringId_A", ""))
                prot_b = row.get("preferredName_B", row.get("stringId_B", ""))
                score_raw = row.get("score", 0)
                try:
                    score = int(float(score_raw) * 1000) if float(score_raw) <= 1 else int(score_raw)
                except (ValueError, TypeError):
                    score = 0

                if prot_a and prot_b and score >= score_threshold:
                    G.add_node(prot_a, node_type="protein")
                    G.add_node(prot_b, node_type="protein")
                    G.add_edge(prot_a, prot_b, score=score)

        except requests.RequestException as e:
            print(f"  Warning: STRING batch failed: {e}")
            continue

    # Cache result
    data = nx.node_link_data(G)
    cache_file.write_text(json.dumps(data, indent=2))
    print(f"[STRING] Built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"[STRING] Cached to {cache_file}")

    return G


def _get_seed_genes(organism: str) -> list[str]:
    """Return a set of well-known genes to seed the STRING PPI query."""
    seeds = {
        "ecoli": [
            # Global regulators
            "crp", "fnr", "arcA", "lexA", "fur", "fis", "hns", "oxyR", "rpoS",
            # Central metabolism
            "pgi", "pfkA", "fbaA", "gapA", "pgk", "eno", "pykF",
            "gltA", "acnA", "icdA", "sucA", "sucC", "sdhA", "fumA", "mdh",
            # DNA replication/repair
            "dnaA", "dnaB", "dnaG", "polA", "recA", "uvrA",
            # Ribosomal
            "rpsA", "rplA", "rpoA", "rpoB",
            # Stress response
            "dnaK", "groEL", "clpB", "lon",
            # Membrane/transport
            "ompA", "ompF", "ptsG", "malE",
        ],
        "yeast": [
            # Cell cycle
            "CDC28", "CLN1", "CLN2", "CLN3", "CLB1", "CLB2",
            # Metabolism
            "HXK2", "PFK1", "TPI1", "PGK1", "ENO1", "PYK1",
            "CIT1", "ACO1", "IDH1", "KGD1", "SDH1", "FUM1", "MDH1",
            # Transcription
            "TBP", "TAF1", "RPB1", "GAL4", "GCN4",
            # Stress
            "HSP82", "SSA1", "HSP104",
            # Signaling
            "RAS2", "TOR1", "SNF1",
        ],
        "human": [
            "TP53", "BRCA1", "MYC", "RAS", "AKT1", "EGFR",
            "GAPDH", "ACTB", "HSP90AA1", "MAPK1",
        ],
    }
    return seeds.get(organism, seeds["ecoli"])


# ---------------------------------------------------------------------------
# Convenience: load all networks
# ---------------------------------------------------------------------------

def load_all_networks(force: bool = False) -> dict[str, nx.Graph]:
    """
    Load all biological networks used in Layer 1 analysis.

    Returns dict with keys:
        'ecoli_grn'          — E. coli gene regulatory network (directed)
        'ecoli_metabolic'    — E. coli metabolic network (directed)
        'yeast_metabolic'    — Yeast metabolic network (directed)
        'ecoli_ppi'          — E. coli protein interaction network (undirected)
        'yeast_ppi'          — Yeast protein interaction network (undirected)
    """
    networks = {}

    networks["ecoli_grn"] = fetch_regulondb_grn(force=force)
    networks["ecoli_metabolic"] = fetch_kegg_metabolic_network("eco", force=force)
    networks["yeast_metabolic"] = fetch_kegg_metabolic_network("sce", force=force)
    networks["ecoli_ppi"] = fetch_string_ppi("ecoli", force=force)
    networks["yeast_ppi"] = fetch_string_ppi("yeast", force=force)

    return networks


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Layer 1: Network Fetcher")
    print("Fetching biological networks from public databases...")
    print("=" * 60)
    print()

    networks = load_all_networks()

    print()
    print("=" * 60)
    print("Summary:")
    for name, G in networks.items():
        directed = "directed" if G.is_directed() else "undirected"
        print(f"  {name}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges ({directed})")
    print("=" * 60)
