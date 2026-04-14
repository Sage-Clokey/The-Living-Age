# BME 129C Capstone Project Proposal

## Project Title

**Spontaneous Order in Living Systems: A Bioinformatics Analysis of Decentralized Organization in Biological Networks**

---

## Student

Sage Clokey, B.S. Bioinformatics, Spring 2026

## Advisor

R. Dubois, BME 129C: Design/Implement BME

---

## Problem Statement

Modern synthetic biology and biomedical engineering overwhelmingly frame biological systems as machines — devices to be designed, parts to be swapped, circuits to be wired. The dominant paradigm treats organisms as centrally controlled systems whose behavior can be predicted and commanded through specification of individual components.

This framing is reductionist, and it is increasingly contradicted by the data. Gene regulatory networks do not have master controllers. Cell differentiation does not follow top-down blueprints. Morphogenesis is not assembly. Ecosystems are not engineered. In each case, complex functional order arises from local interactions among components that have no global knowledge of the system — a phenomenon that biology shares with economics, information networks, and other complex adaptive systems under the name **spontaneous order.**

Yet there is no unified, data-driven analysis that systematically demonstrates the prevalence and mechanisms of spontaneous order across multiple scales of biological organization — from gene regulation to cellular differentiation to tissue morphogenesis to ecosystem dynamics — using publicly available bioinformatics data.

This project proposes to build that analysis.

---

## Background

### Spontaneous Order

Spontaneous order is the emergence of structured, functional organization without central planning or top-down control. The concept has deep roots in multiple disciplines:

- **Economics:** Adam Smith's "invisible hand" (1776); Friedrich Hayek's analysis of prices as emergent information systems (*The Use of Knowledge in Society*, 1945); Elinor Ostrom's work on self-governing commons (*Governing the Commons*, 1990)
- **Physics:** Ilya Prigogine's dissipative structures and self-organization in far-from-equilibrium thermodynamic systems (Nobel Prize, 1977)
- **Biology:** Stuart Kauffman's self-organization in gene regulatory networks (*The Origins of Order*, 1993); Alan Turing's reaction-diffusion model of morphogenesis (1952); Michael Levin's work on bioelectric signaling and distributed intelligence in cell collectives

The thesis of this project is that **biology is the strongest empirical proof that spontaneous order works** — that complex, functional, adaptive systems can and do arise without central control, and that the data in public genomic and biological databases demonstrates this at every scale of organization.

### The Machine Metaphor and Its Limitations

The International Genetically Engineered Machine (iGEM) competition, BioBricks standardization, and the "genetic circuit" paradigm all treat organisms as machines. This approach has produced results — engineered metabolic pathways, synthetic gene circuits, biosensors — but it encounters systematic failures when scaling beyond single-pathway modifications:

- **Context-dependence:** The same genetic part behaves differently in different cellular contexts. BioBricks that work in isolation fail when combined (Kwok, 2010; Brophy & Voigt, 2014).
- **Emergent behavior:** Engineered gene circuits produce unexpected dynamics because cells are not passive substrates — they actively remodel their regulatory landscape in response to perturbation (Cardinale & Arkin, 2012).
- **Robustness paradox:** Living systems are extraordinarily robust to perturbation; engineered circuits are fragile. This difference arises because living systems achieve robustness through distributed, redundant, context-sensitive regulation — not through precise specification of components (Kitano, 2004).

These failures are not technical bugs to be fixed. They are evidence that **the machine metaphor is wrong** — that life does not work the way machines work, and that designing with life requires understanding how it actually organizes itself.

---

## Proposed Analysis

This project uses publicly available bioinformatics data to demonstrate spontaneous order at four scales of biological organization:

### Layer 1: Gene Regulatory Network Topology — Decentralization

**Data sources:** RegulonDB (E. coli transcriptional regulation), ENCODE (human regulatory elements), JASPAR (transcription factor binding profiles), STRING (protein-protein interaction networks)

**Analysis:**
- Extract the full transcriptional regulatory network for E. coli and the human genome
- Compute network topology metrics: **degree distribution, betweenness centrality, clustering coefficient, and network controllability**
- Test for the presence of **scale-free topology** (power-law degree distribution) — the signature of decentralized networks where no single node is essential
- Quantify **network controllability** using the Liu-Slotine-Barabási framework (2011): what fraction of nodes must be externally controlled to drive the entire network? In truly decentralized systems, this fraction is low — the network organizes itself.
- Compare against equivalent-size random networks and engineered circuit topologies to demonstrate that biological networks are **structurally decentralized** in ways that engineered systems are not

**Expected result:** Biological gene regulatory networks exhibit scale-free, highly distributed topology with low controllability fractions — meaning the system self-organizes without requiring central control of individual nodes.

### Layer 2: Metabolic Network Self-Organization — Emergent Economy

**Data sources:** KEGG (metabolic pathways), BiGG Models (genome-scale metabolic reconstructions), MetaCyc (metabolic pathway database)

**Analysis:**
- Extract genome-scale metabolic models for E. coli (iML1515), S. cerevisiae (yeast), and H. sapiens
- Compute **flux balance analysis (FBA)** to identify how metabolic resources are allocated across pathways
- Analyze **metabolic flux distributions** for signatures of emergent optimization — does the cell allocate resources efficiently without a central allocator?
- Map the metabolic network as an **economic system**: metabolites as currencies, enzymes as producers, pathways as supply chains. Compute metrics of resource allocation efficiency and compare to known results from economic network analysis.
- Identify **redundancy and robustness**: how many alternative pathways exist for essential functions? How does the network respond to simulated knockouts?

**Expected result:** Metabolic networks exhibit emergent resource allocation that mirrors the properties of decentralized economic systems — efficient distribution without central planning, redundancy that provides robustness, and adaptive rerouting in response to perturbation.

### Layer 3: Horizontal Gene Transfer — Open-Source Biology

**Data sources:** NCBI GenBank, IslandViewer (genomic islands), ICEberg (integrative conjugative elements), ACLAME (mobile genetic elements)

**Analysis:**
- Identify horizontally transferred genes across bacterial, archaeal, and eukaryotic genomes using phylogenetic incongruence and GC content deviation
- Map the **network of gene sharing** across species — which organisms share genetic material, how frequently, and for what functions?
- Quantify the functional categories of horizontally transferred genes: are they primarily metabolic, defense-related, regulatory?
- Analyze whether horizontal gene transfer follows **open-source dynamics**: is shared genetic material adopted, modified, and re-shared in patterns analogous to open-source software development?
- Compute the **information-theoretic contribution** of horizontal transfer to genomic diversity — what fraction of an organism's functional capability comes from shared rather than vertically inherited genes?

**Expected result:** Life is natively open-source. Organisms routinely share genetic information across species boundaries, and this sharing is not parasitic — it is cooperative, functional, and a primary driver of adaptive capability. The tree of life is not a tree; it is a network, and the network operates on principles of voluntary exchange.

### Layer 4: Morphogenesis — Emergent Form

**Data sources:** Published Turing pattern and reaction-diffusion datasets, gene expression atlases (Allen Brain Atlas, Drosophila gene expression databases), the student's existing morphogenesis simulation engine

**Analysis:**
- Demonstrate **Turing pattern formation** using reaction-diffusion simulation: two diffusing morphogens with activator-inhibitor dynamics produce spatial patterns (stripes, spots, spirals) with no global template
- Compare simulated Turing patterns against real biological patterning data: zebrafish pigmentation, Drosophila segment polarity, mammalian digit formation
- Use the student's existing **GRN-based morphogenesis engine** to simulate tissue growth driven by local gene regulatory interactions, demonstrating that complex 3D structures (branching, spiraling, sheltering) emerge from local rules without global blueprints
- Analyze published single-cell RNA sequencing data to show that cell fate decisions during differentiation are driven by **local signaling gradients**, not central instruction — the same genome produces different cell types based on position and context

**Expected result:** Biological form — from skin patterns to organ structure to whole-body architecture — arises from local interactions without central control. Morphogenesis is the strongest visual proof that spontaneous order produces complex functional structure.

---

## Integration: The Unified Argument

The four layers form a single argument across scales:

| Scale | System | Spontaneous Order Mechanism | Data Source |
|-------|--------|---------------------------|-------------|
| **Molecular** | Gene regulatory networks | Scale-free topology, distributed control | RegulonDB, ENCODE, STRING |
| **Cellular** | Metabolic networks | Emergent resource allocation | KEGG, BiGG, MetaCyc |
| **Genomic** | Horizontal gene transfer | Open-source information sharing | GenBank, IslandViewer, ICEberg |
| **Organismal** | Morphogenesis | Turing patterns, local signaling | Expression atlases, simulation engine |

At every scale, the same principle holds: **functional order emerges from local interactions without central control.** The gene network has no master gene. The metabolic network has no central allocator. The genome has no closed borders. The body plan has no blueprint.

The final deliverable integrates all four analyses into a unified visualization and written argument demonstrating that biology is the empirical proof of spontaneous order — and that designing with living systems requires working with this principle rather than against it.

---

## Deliverables

### Weeks 1-3: Gene Regulatory Network Analysis

- Extract and process E. coli and human GRN data from RegulonDB and ENCODE
- Compute topology metrics (degree distribution, centrality, controllability)
- Generate network visualizations
- Deliverable: Analysis showing biological GRNs are structurally decentralized

### Weeks 4-5: Metabolic Network Analysis

- Extract genome-scale metabolic models from BiGG
- Run flux balance analysis and knockout simulations
- Map metabolic-to-economic network parallels
- Deliverable: Analysis showing metabolic networks self-organize resource allocation

### Weeks 6-7: Horizontal Gene Transfer Analysis

- Identify HGT events across selected genomes
- Build gene-sharing network and compute transfer statistics
- Analyze functional categories and open-source dynamics
- Deliverable: Analysis showing life operates as an open-source information network

### Weeks 8-9: Morphogenesis Analysis

- Run Turing pattern simulations and compare to biological data
- Use existing GRN morphogenesis engine to demonstrate emergent structure
- Analyze published scRNA-seq data for local signaling in differentiation
- Deliverable: Analysis showing biological form emerges from local rules

### Week 10: Integration and Final Presentation

- Integrate all four layers into unified argument and visualization
- Write final paper connecting bioinformatics evidence to spontaneous order theory
- Prepare and deliver final presentation
- Deliverable: Complete capstone paper and presentation

---

## Evaluation Criteria

1. **Data quality.** Are the bioinformatics analyses technically sound? Are the right databases used, the right metrics computed, and the results correctly interpreted?

2. **Analytical rigor.** Do the network topology metrics, flux analyses, phylogenetic analyses, and simulation results actually demonstrate decentralized organization? Are alternative explanations considered?

3. **Cross-scale integration.** Does the project successfully connect molecular, cellular, genomic, and organismal evidence into a coherent unified argument?

4. **Novelty.** While individual analyses (GRN topology, FBA, HGT mapping, Turing patterns) exist in the literature, has the student produced a novel synthesis that demonstrates spontaneous order as a unifying biological principle across all four scales?

5. **Communication.** Is the final paper and presentation clear, well-argued, and accessible to a biomedical engineering audience?

---

## Relevance to Biomedical Engineering

This project is relevant to biomedical engineering in three ways:

**Synthetic biology design philosophy.** The dominant paradigm in synthetic biology treats organisms as machines to be engineered. This project provides data-driven evidence for an alternative paradigm: **designing with the self-organizing properties of living systems** rather than against them. This has direct implications for the reliability and scalability of synthetic biology applications in medicine, materials, and agriculture.

**Bioinformatics methodology.** The project integrates network analysis, flux balance analysis, phylogenomics, and developmental biology simulation into a unified analytical framework. Each technique is individually standard in bioinformatics; their integration across scales is novel.

**Biomaterials and living architecture.** The morphogenesis analysis directly connects to emerging work in biological materials and living construction. Understanding how biological form emerges from local rules — without centralized blueprints — is foundational for any future engineering of self-growing, self-repairing structures.

---

## Existing Tools and Foundation

This capstone builds on work the student has already completed:

- **GRN-based morphogenesis simulation engine** (`Living works by the word/3D-Model_Living_Design/`) — a working simulation that generates 3D biological structures from gene regulatory network interactions, with natural language input via `prompt_translate.py`
- **Adaptive Genome Design System** (`adaptive_Automation/`) — genome retrieval from 220+ organisms via UCSC and NCBI, compatibility analysis, assembly pipeline
- **Network analysis skills** from bioinformatics coursework
- **Python ecosystem:** NetworkX (graph analysis), COBRApy (flux balance analysis), scikit-learn, matplotlib, the `rich` library for visualization

---

## Tools and Technologies

| Component | Tool | Role |
|-----------|------|------|
| GRN topology | NetworkX, RegulonDB, ENCODE | Network extraction and analysis |
| Metabolic modeling | COBRApy, BiGG Models | Flux balance analysis and knockout simulation |
| HGT analysis | Biopython, NCBI GenBank, IslandViewer | Phylogenetic analysis and transfer detection |
| Morphogenesis simulation | Existing GRN engine (PyTorch) | Turing pattern and emergent structure simulation |
| Visualization | matplotlib, NetworkX, Three.js (existing viewer) | Network graphs, metabolic maps, 3D structures |
| Language | Python 3.11+ | All analyses |

---

## References

1. Kauffman, S. (1993). *The Origins of Order: Self-Organization and Selection in Evolution.* Oxford University Press.
2. Hayek, F.A. (1945). The use of knowledge in society. *American Economic Review*, 35(4), 519-530.
3. Turing, A.M. (1952). The chemical basis of morphogenesis. *Philosophical Transactions of the Royal Society B*, 237(641), 37-72.
4. Liu, Y.Y., Slotine, J.J., & Barabási, A.L. (2011). Controllability of complex networks. *Nature*, 473, 167-173.
5. Barabási, A.L. & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509-512.
6. Kitano, H. (2004). Biological robustness. *Nature Reviews Genetics*, 5, 826-837.
7. Brophy, J.A. & Voigt, C.A. (2014). Principles of genetic circuit design. *Nature Methods*, 11, 508-520.
8. Cardinale, S. & Arkin, A.P. (2012). Contextualizing context for synthetic biology. *Biotechnology and Bioengineering*, 109(5), 1084-1087.
9. Kwok, R. (2010). Five hard truths for synthetic biology. *Nature*, 463, 288-290.
10. Prigogine, I. & Stengers, I. (1984). *Order Out of Chaos: Man's New Dialogue with Nature.* Bantam Books.
11. Levin, M. (2023). Bioelectric signaling: reprogrammable circuits underlying embryogenesis, regeneration, and cancer. *Cell*, 184(6), 1545-1567.
12. Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action.* Cambridge University Press.
13. Santos-Moreno, J. & Schaerli, Y. (2020). Using synthetic biology to engineer spatial patterns. *Advanced Biosystems*, 4(5), 1900221.

---

*Prepared for BME 129C: Design/Implement BME, Spring 2026, UC Santa Cruz.*
*To be aligned with actual assignment when received.*
