# Figure Guide: Claims, Graphs, and What to Look For

This document maps every claim in the capstone to a specific figure, explains what the figure should show if the thesis is correct, and what the alternative (centralized) case would look like. Use this when writing the results and discussion sections.

---

## Layer 1: Network Topology — "No Master Node"

### Figure: Degree Distribution (log-log scatter plot)

**Claim:** No single gene controls the network.

**What you'd see if the thesis is correct:**
- Straight line on log-log axes = power-law distribution
- Many nodes with few connections, few nodes with many — but no single node dominates
- Power-law exponent (alpha) between 2 and 3
- Biological networks follow the same line as the Barabasi-Albert scale-free model

**What the alternative looks like:**
- Star graph: one node with degree N-1, every other node has degree 1 — a single spike, not a line
- Random (Erdos-Renyi) graph: bell curve on log-log — no hubs at all, no structure
- Lattice: every node has the same degree — a single vertical bar

**Statistical test:** Kolmogorov-Smirnov test for power-law fit. Power-law should fit better than exponential (positive log-likelihood ratio R, p < 0.05).

---

### Figure: Betweenness Gini Coefficient (bar chart)

**Claim:** No single bottleneck controls information flow.

**What you'd see if the thesis is correct:**
- Low Gini (< 0.5) for biological networks = betweenness centrality is spread across many nodes
- No single node carries a disproportionate share of shortest paths
- Multiple nodes share the load of network communication

**What the alternative looks like:**
- Star graph: Gini ≈ 1.0 — the hub carries ALL shortest paths
- Hub-and-spoke: Gini > 0.7 — a few hubs dominate
- Lattice: Gini very low but for the wrong reason — no structure at all, not distributed intelligence

**Key distinction:** Biological networks have moderate Gini — not zero (which would mean no structure) and not near 1.0 (which would mean centralization). The sweet spot is distributed but organized.

---

### Figure: Robustness Curves (line plot)

**Claim:** Decentralized networks degrade gracefully; centralized ones collapse.

**What you'd see if the thesis is correct:**
- **Random removal (solid line):** Biological network stays above 50% giant component even after removing 30-40% of nodes. Gentle downward slope.
- **Targeted attack (dashed line):** Steeper decline for biological networks (hubs matter) but still gradual — the network has multiple important nodes, not just one.
- Star graph under targeted attack: removing the single hub immediately drops giant component to near zero. A cliff, not a slope.

**What the alternative looks like:**
- Star: one removal = total collapse (targeted). Random removal is also bad because every removal disconnects one spoke.
- Random graph: collapses faster than biological under targeted attack (no redundancy).
- Lattice: degrades uniformly but slowly — resilient but rigid, unable to adapt.

**The biological advantage:** Robust to random failure (most nodes aren't critical) AND more robust than centralized to targeted attack (no single point of failure that kills everything).

---

## Layer 1b: Single-Cell Economy — "Cells as Economic Agents"

### Figure: UMAP (scatter plot colored by cell type)

**Claim:** Cells specialize like firms in an economy — same genome, different output.

**What you'd see if the thesis is correct:**
- Distinct, separated clusters on UMAP — each cell type occupies its own region of gene expression space
- Clear boundaries between sectors (T cells, B cells, monocytes, NK cells, etc.)
- This IS an economic map: each cluster is a sector of the cellular economy, producing different goods (proteins) from the same raw material (genome)

**What the alternative looks like:**
- One undifferentiated blob = no specialization, every cell doing the same thing
- That would mean centralized instruction rather than distributed differentiation

**Why this matters:** 37 trillion cells, same DNA, no master cell telling them what to be. The UMAP shows the result: a diverse, specialized economy that self-organized.

---

### Figure: Specialization Scores (horizontal bar chart)

**Claim:** Cell types exhibit division of labor — measurable comparative advantage.

**What you'd see if the thesis is correct:**
- Different cell types have different entropy scores
- Low normalized entropy (< 0.85) = specialist — concentrates transcriptional resources on a narrow gene program (e.g., megakaryocytes heavily express platelet genes)
- High normalized entropy (> 0.90) = generalist — expresses many genes more evenly
- The variation itself proves division of labor: if every cell type had the same entropy, there would be no specialization

**What the alternative looks like:**
- All bars at the same height = no specialization, no comparative advantage
- That would mean the genome produces identical cells — a factory, not an economy

**Key metric:** The spread between the most specialized and least specialized cell type. Wider spread = stronger division of labor.

---

### Figure: Cell-Cell Communication Network (graph)

**Claim:** Cells coordinate through distributed signaling, not central command.

**What you'd see if the thesis is correct:**
- Multiple nodes (cell types) with similar-sized connections — no single cell type dominates communication
- Dense network with many pathways — information flows through multiple channels
- Betweenness Gini < 0.5 — no single cell type acts as gatekeeper
- Node sizes roughly similar — communication capacity is distributed

**What the alternative looks like:**
- One cell type in the center with all edges radiating outward = master cell
- Star topology = every communication goes through one gatekeeper
- That's an autocracy, not an economy

---

### Figure: Robustness Table (cell type removal)

**Claim:** No single cell type is indispensable — the system is fault-tolerant.

**What you'd see if the thesis is correct:**
- Removing any single cell type leaves 70-90% of communication edges intact
- No single removal is catastrophic (no value below 50%)
- The system degrades gracefully — losing a sector hurts but doesn't collapse the economy

**What the alternative looks like:**
- Removing one cell type destroys > 50% of communication edges = that cell type was the central controller
- Fragile centralization: remove the boss and everything stops

---

## Layer 2: Economic Modeling — "Pathways as Agents"

### Figure: GDP Over Time (line plot, two lines)

**Claim:** Distributed allocation reaches stable equilibrium without a planner.

**What you'd see if the thesis is correct:**
- **Distributed (green line):** Starts with oscillations as agents adjust production rates based on local feedback. Oscillations dampen over time. Settles to a stable GDP. This IS the invisible hand — order from individual decisions.
- **Centralized (red line):** May reach a similar or slightly higher peak GDP faster — the planner can optimize globally. But the line is flat from the start because rates are assigned, not discovered.

**What this means:** The distributed system finds equilibrium through trial and error (biological feedback), not top-down instruction. The wobble at the start is the market discovering prices. The stability at the end is proof that distributed coordination works.

---

### Figure: GDP After Perturbation (paired bar chart)

**Claim:** Distributed systems recover from shocks better than centralized ones.

**What you'd see if the thesis is correct:**
- For each pathway removed: the distributed bar is taller than the centralized bar
- Distributed GDP drops 5-15% after losing one agent, then recovers — neighboring pathways compensate through metabolite pool adjustment
- Centralized GDP drops further because the allocator's plan is now wrong — it was optimized for 12 agents, now there are 11, and it doesn't self-correct

**What the alternative looks like:**
- Centralized bars consistently taller = centralized systems recover better
- That would mean planning outperforms markets even under stress
- (The biological evidence predicts this will NOT happen)

**Key number:** Mean robustness score across all single-agent removals. Distributed should be higher.

---

### Figure: Production Rate Convergence (line plot per agent)

**Claim:** No planner needed — agents self-organize to optimal rates.

**What you'd see if the thesis is correct:**
- Each agent's production rate starts at the base rate, then adjusts based on local feedback (product accumulation, substrate scarcity, ATP budget)
- Lines oscillate early then converge to stable values — different for each agent
- The final rates are NOT equal (that would be communism). They're proportional to each agent's efficiency and the economy's demand for its products.

**What the alternative looks like:**
- Centralized: flat lines from step 0 — rates are assigned by the allocator
- Stable but brittle: if conditions change, the assigned rates are wrong and don't self-correct

**Why this matters:** The convergence pattern is the biological equivalent of price discovery. Nobody told the agents what to produce. They figured it out from local signals.

---

### Figure: Metabolite Pool Levels Over Time (line plot per metabolite)

**Claim:** The market self-corrects through feedback.

**What you'd see if the thesis is correct:**
- When a metabolite overshoots (overproduction), producers of that metabolite slow down — the "price" drops
- When a metabolite gets scarce (high demand), producers speed up — the "price" rises
- Oscillations dampen over time as the system finds balance
- This IS supply-and-demand dynamics, happening in a cell

**What the alternative looks like:**
- Centralized: metabolite levels track the allocation plan perfectly — no oscillation
- But if the plan is wrong (or conditions change), the levels stay wrong because there's no feedback mechanism

---

## Layer 3: Cross-Species Trade — "Comparative Advantage"

### Figure: Comparative Advantage Table

**Claim:** Each organism specializes in capabilities others lack — Ricardian comparative advantage at the molecular level.

**What you'd see if the thesis is correct:**
- Each organism has 1-3 unique capabilities
- No organism does everything
- Coral exports biomineralization. Spider exports silk. Bacteria export cellulose. Planaria exports regeneration.
- The tree of life is a network of specialists, not a collection of generalists

**What this means:** Trade is beneficial BECAUSE organisms are different. Combining capabilities from across the tree of life (which is what synthetic biology does) is the biological equivalent of international trade.

---

### Figure: Trade Cost Heatmap (organisms × organisms, colored matrix)

**Claim:** Trade friction is real, measurable, and structured by evolutionary distance.

**What you'd see if the thesis is correct:**
- Diagonal = 0 (trading with yourself costs nothing)
- Same-kingdom pairs (yeast↔ganoderma, human↔axolotl) = cool colors (low cost)
- Cross-kingdom pairs (E. coli↔human, bacteria↔coral) = hot colors (high cost)
- Clear block structure: prokaryotes cluster together, eukaryotic subtypes cluster together
- The gradient mirrors evolutionary distance

**What the alternative looks like:**
- Uniform color = trade cost is the same everywhere = no structure
- That would mean codon bias and regulatory elements don't matter — biologically false

**Key pattern:** The kingdom boundary (prokaryote ↔ eukaryote) should show the sharpest jump in trade cost — like a trade embargo between different legal systems.

---

### Figure: Trade Network Graph (node-link diagram)

**Claim:** The tree of life forms natural trade blocs, like economic free trade zones.

**What you'd see if the thesis is correct:**
- Thick edges between closely related organisms (same kingdom) = easy trade
- Thin edges across kingdom boundaries = high friction
- Natural clustering: fungi cluster together, animals cluster together
- Node size proportional to number of capabilities = economic size
- No single organism at the center — it's a distributed network, not a hub-and-spoke

**What the alternative looks like:**
- One organism connected to everything = biological hegemon
- Uniform edge thickness = no trade structure
- Neither of these is expected

---

### Figure (to build): Codon Distance vs Trade Cost (scatter plot)

**Claim:** Evolutionary distance predicts trade friction — the gravity model of biology.

**What you'd see if the thesis is correct:**
- Positive correlation: organism pairs with larger RSCU distance have higher trade cost
- Spearman correlation rho > 0.7
- This mirrors the Tinbergen gravity model of international trade: physical distance predicts trade volume

**Why this is powerful:** It means the same mathematical relationship that governs human trade also governs genetic exchange across species. The principle is scale-invariant.

---

## The Meta-Claim

Every figure is falsifiable. If the E. coli GRN had a star topology, the thesis would be wrong. If removing one cell type collapsed the communication network, the thesis would be wrong. If centralized allocation recovered faster from perturbation, the thesis would be wrong. If codon distance didn't correlate with trade cost, the thesis would be wrong.

The data either shows it or it doesn't. That's what makes this science, not philosophy.
