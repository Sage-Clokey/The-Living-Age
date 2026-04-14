# Living Systems as Decentralized Economies

**BME 129C Capstone — Sage Clokey, Spring 2026, UC Santa Cruz**

---

## The Question

Every living system on Earth — from the gene regulatory network inside a single bacterium to the mycorrhizal web beneath a forest — coordinates without a central controller. No master gene runs your body. No forester runs a forest. Yet these systems allocate resources, respond to shocks, and adapt to change more robustly than anything industrial civilization has built.

Economics has a word for this: **decentralized market**. Agents with local information trade through shared pools, prices emerge from feedback, and order arises without a planner.

This project asks: **are living systems literally decentralized economies?** Not as metaphor — as measurable, quantifiable, structurally equivalent systems. And if so, does the decentralized architecture outperform centralized alternatives?

---

## The Thesis

Living systems — from intracellular gene regulatory networks to cross-species symbioses — operate as decentralized economies: resources allocated through distributed negotiation, not central command. This is provable with real biological data.

---

## Three Layers of Evidence

### Layer 1: Network Topology — "No Master Node"

Pull real gene regulatory networks (E. coli, ~4,500 interactions from RegulonDB) and metabolic networks (KEGG) into graph structures. Measure degree distribution, betweenness centrality, clustering, and robustness under node removal. Compare to centralized architectures (star graphs, hub-and-spoke networks).

**What it proves:** Biological networks are scale-free and decentralized. No single node controls the system. Remove any node and the network degrades gracefully — unlike centralized systems, which collapse when the hub fails.

#### Layer 1b: Single-Cell Analysis — "Cells as Economic Agents"

Analyze pre-processed single-cell RNA sequencing data (human PBMCs from CellxGene) to show that individual cells in a tissue behave as specialized agents in a decentralized economy. Each cell type has a distinct gene expression program (division of labor), communicates through ligand-receptor pairs (local price signals), and no single cell type controls the others (no central planner). UMAP visualization maps the economy's sectors; cell-cell communication networks prove the coordination is distributed.

**What it proves:** The same genome produces specialized agents that coordinate without hierarchy — a decentralized economy at the cellular scale.

### Layer 2: Economic Modeling — "Pathways as Agents"

Model metabolic pathways as economic agents. Each pathway consumes resources (demand), produces outputs (supply), operates within an energy budget (ATP), and responds to local signals (price feedback). Simulate resource allocation under two regimes — distributed (biological) and centralized (planned) — and measure efficiency, robustness, and equilibrium properties.

**What it proves:** The distributed regime reaches stable equilibrium through local feedback alone (Nash equilibrium without a planner), and recovers from perturbation faster than the centralized regime. This mirrors the First Welfare Theorem: decentralized markets approximate optimal allocation.

### Layer 3: Cross-Species Trade — "Comparative Advantage"

Map gene transferability across organisms as a trade network. Codon usage distance = trade friction. Regulatory incompatibility (prokaryote vs eukaryote) = different legal frameworks. Each organism's unique capabilities (coral→biomineralization, spider→silk) = comparative advantage.

**What it proves:** Cross-species gene exchange follows the same structural patterns as international trade. Lower barriers enable more exchange. Organisms "export" their specialties. The tree of life is a trade network.

---

## Why This Matters

### For Biology

Understanding biological coordination as economic coordination gives us new tools for old problems. Drug resistance is a market routing around a disruption. Cancer is a cell defecting from cooperative resource allocation. Microbiome dysbiosis is an economy in recession.

### For Economics

If decentralized coordination is not just a human invention but a 4-billion-year-old biological strategy, that changes the weight of the argument. The genome is a receipt for what works over deep time — and what it shows is distributed systems, voluntary cooperation, and emergent order.

### For Synthetic Biology

If you are designing a multi-gene construct — combining cellulose synthesis from bacteria, biomineralization from coral, and self-repair from planaria into a single organism — you are building a small economy. Understanding the economic principles (trade friction, comparative advantage, resource competition) directly informs how to balance pathways, choose chassis organisms, and avoid metabolic conflicts.

### For the Living Age

This project is the bridge between the philosophy and the technology. The Living Age argues that life organizes better than control systems. This capstone proves it with data.

---

## Data Sources

| Database | What It Provides |
|----------|-----------------|
| [RegulonDB](https://regulondb.ccg.unam.mx) | E. coli gene regulatory network (~4,500 TF-gene interactions) |
| [KEGG REST API](https://rest.kegg.jp) | Metabolic pathway networks with real reaction stoichiometry |
| [STRING](https://string-db.org) | Protein-protein interaction networks |
| [CellxGene](https://cellxgene.cziscience.com) | Pre-processed single-cell RNA sequencing datasets (human PBMCs) |
| [UCSC Genome Browser](https://api.genome.ucsc.edu) | Gene sequences from 220+ genomes |
| [NCBI Entrez](https://eutils.ncbi.nlm.nih.gov) | Gene search and sequence retrieval across all kingdoms |
| [Kazusa Codon Usage DB](https://www.kazusa.or.jp/codon/) | Codon usage tables for thousands of organisms |

---

## Built On

This capstone builds on the [Adaptive Genome Design System](https://github.com/Sage-Clokey/adaptive-Automation), a pipeline developed over prior quarters that retrieves real genes from across the tree of life, checks cross-species compatibility (codon bias, regulatory signals, pathway conflicts), and assembles optimized DNA constructs. The compatibility engine — with its codon adaptation scoring, regulatory element detection, and pathway conflict analysis — provides direct infrastructure for Layers 2 and 3.

---

## Project Structure

```
BME_129C_Capstone/
├── README.md
├── requirements.txt
├── run_all.py
├── data/                        # Cached API responses
│   ├── regulondb/
│   ├── kegg/
│   └── string/
├── layer1_topology/             # Network topology analysis
│   ├── network_fetcher.py
│   ├── topology_analysis.py
│   ├── centralized_comparison.py
│   └── single_cell_economy.py   # scRNA-seq: cells as economic agents
├── layer2_economy/              # Economic modeling
│   ├── metabolic_economy.py
│   ├── resource_simulator.py
│   └── equilibrium_analysis.py
├── layer3_trade/                # Cross-species trade mapping
│   ├── trade_network.py
│   ├── trade_cost_calculator.py
│   └── trade_visualization.py
├── synthesis/                   # Unified dashboard + statistics
│   ├── dashboard.py
│   └── statistical_tests.py
└── paper/
    ├── figures/
    └── capstone_paper.md
```

---

*Prepared for BME 129C: Design/Implement BME, Spring 2026, UC Santa Cruz.*
*Advisor: R. Dubois*
