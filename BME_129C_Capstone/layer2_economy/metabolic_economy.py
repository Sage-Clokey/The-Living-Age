"""
Metabolic Economy — Layer 2: Economic Modeling
===============================================
Models metabolic pathways as economic agents in a decentralized market.

Each pathway:
    - Consumes resources (demand)
    - Produces outputs (supply)
    - Operates within an ATP budget (currency)
    - Responds to local metabolite concentrations (price signals)
    - Competes for shared substrates (market competition)

Two allocation regimes are simulated:
    1. Distributed (biological): agents trade through shared metabolite pools,
       adjust production based on local feedback. No central allocator.
    2. Centralized (planned): a single allocator controls all production
       and distributes resources globally. Optimizes for total output.

The thesis: distributed allocation reaches stable equilibrium, recovers
from perturbation faster, and approaches Pareto efficiency — all without
a planner. This mirrors the First Welfare Theorem.

Foundation:
    Extends PathwayProfile from adaptive_Automation/compatibility/pathway.py
    The 12 existing pathway profiles already have consumes[], produces[],
    atp_cost, signal_inputs[], signal_outputs[] — they ARE economic agents.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import sys
from pathlib import Path

import numpy as np

# Import existing pathway profiles from adaptive_Automation
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "adaptive_Automation"))

try:
    from compatibility.pathway import PathwayProfile, PATHWAY_CATALOG
    print(f"[economy] Loaded {len(PATHWAY_CATALOG)} pathway profiles from adaptive_Automation")
except ImportError:
    print("[economy] Warning: could not import from adaptive_Automation. Using built-in catalog.")
    PATHWAY_CATALOG = []

    @dataclass
    class PathwayProfile:
        name: str
        capability: str
        consumes: list[str] = field(default_factory=list)
        produces: list[str] = field(default_factory=list)
        signal_inputs: list[str] = field(default_factory=list)
        signal_outputs: list[str] = field(default_factory=list)
        activates_tfs: list[str] = field(default_factory=list)
        inhibits_tfs: list[str] = field(default_factory=list)
        amino_acid_load: dict[str, str] = field(default_factory=dict)
        atp_cost: str = "medium"
        compartment: str = "cytoplasm"
        notes: str = ""


# ---------------------------------------------------------------------------
# Economic Agent
# ---------------------------------------------------------------------------

ATP_COST_MAP = {"low": 1.0, "medium": 2.0, "high": 3.0, "very_high": 4.0}


@dataclass
class EconomicAgent:
    """
    A metabolic pathway modeled as an economic agent.

    Each agent has:
        - A production function (consumes inputs, produces outputs)
        - An ATP budget (currency)
        - An inventory of metabolites
        - A production rate that adjusts based on local conditions
    """
    pathway: PathwayProfile
    name: str = ""

    # Economic state
    atp_budget: float = 10.0
    inventory: dict[str, float] = field(default_factory=dict)

    # Production parameters
    base_production_rate: float = 1.0
    current_production_rate: float = 1.0

    # History (for plotting)
    production_history: list[float] = field(default_factory=list)
    budget_history: list[float] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = self.pathway.name
        # Initialize inventory with small amounts of produced goods
        for product in self.pathway.produces:
            self.inventory.setdefault(product, 1.0)

    @property
    def atp_cost_per_cycle(self) -> float:
        return ATP_COST_MAP.get(self.pathway.atp_cost, 2.0)

    def can_produce(self, pool: "MetabolitePool") -> bool:
        """Check if all required substrates are available in the shared pool."""
        for substrate in self.pathway.consumes:
            if substrate == "ATP":
                if self.atp_budget < self.atp_cost_per_cycle:
                    return False
            elif pool.get(substrate) < 0.1:
                return False
        return True

    def produce(self, pool: "MetabolitePool", rate_multiplier: float = 1.0):
        """
        Execute one production cycle.
        Consume from the shared pool, produce into the shared pool.
        """
        rate = self.current_production_rate * rate_multiplier

        # Consume
        for substrate in self.pathway.consumes:
            if substrate == "ATP":
                self.atp_budget -= self.atp_cost_per_cycle * rate
            else:
                consumed = min(rate, pool.get(substrate))
                pool.withdraw(substrate, consumed)

        # Produce
        for product in self.pathway.produces:
            pool.deposit(product, rate)
            self.inventory[product] = self.inventory.get(product, 0) + rate

        # Record history
        self.production_history.append(rate)
        self.budget_history.append(self.atp_budget)

    def adjust_rate_distributed(self, pool: "MetabolitePool"):
        """
        Distributed feedback: adjust production rate based on local conditions.

        If my products are accumulating (oversupply) → slow down.
        If my substrates are scarce (high demand) → slow down.
        If my substrates are abundant → speed up.

        This is the invisible hand: no planner needed, just local signals.
        """
        # Product feedback: if my products are piling up, reduce rate
        product_signal = 1.0
        for product in self.pathway.produces:
            level = pool.get(product)
            if level > 5.0:
                product_signal *= 0.7  # oversupply, slow down
            elif level < 1.0:
                product_signal *= 1.3  # high demand, speed up

        # Substrate feedback: if my inputs are scarce, reduce rate
        substrate_signal = 1.0
        for substrate in self.pathway.consumes:
            if substrate == "ATP":
                continue
            level = pool.get(substrate)
            if level < 0.5:
                substrate_signal *= 0.5  # scarcity
            elif level > 3.0:
                substrate_signal *= 1.2  # abundance

        # ATP feedback
        atp_signal = 1.0
        if self.atp_budget < 2.0:
            atp_signal = 0.3
        elif self.atp_budget > 15.0:
            atp_signal = 1.5

        self.current_production_rate = (
            self.base_production_rate
            * product_signal
            * substrate_signal
            * atp_signal
        )
        # Clamp
        self.current_production_rate = max(0.01, min(5.0, self.current_production_rate))


# ---------------------------------------------------------------------------
# Metabolite Pool (shared market)
# ---------------------------------------------------------------------------

@dataclass
class MetabolitePool:
    """
    The shared metabolite pool — the marketplace where agents trade.

    In biology: the cytoplasm, the extracellular space, the bloodstream.
    In economics: the market where supply meets demand.

    No allocator controls this pool. Agents deposit and withdraw freely.
    Prices (concentrations) emerge from aggregate behavior.
    """
    levels: dict[str, float] = field(default_factory=dict)
    history: dict[str, list[float]] = field(default_factory=dict)

    def get(self, metabolite: str) -> float:
        return self.levels.get(metabolite, 0.0)

    def deposit(self, metabolite: str, amount: float):
        self.levels[metabolite] = self.levels.get(metabolite, 0.0) + amount

    def withdraw(self, metabolite: str, amount: float) -> float:
        available = self.levels.get(metabolite, 0.0)
        taken = min(amount, available)
        self.levels[metabolite] = available - taken
        return taken

    def record(self):
        """Snapshot current levels into history."""
        for met, level in self.levels.items():
            self.history.setdefault(met, []).append(level)

    def total_output(self) -> float:
        """Total metabolites in the pool (GDP proxy)."""
        return sum(self.levels.values())


# ---------------------------------------------------------------------------
# Simulation Engine
# ---------------------------------------------------------------------------

@dataclass
class SimulationResult:
    """Results from running an economic simulation."""
    regime: str                    # "distributed" or "centralized"
    n_steps: int = 0
    agents: list[EconomicAgent] = field(default_factory=list)
    pool: MetabolitePool = field(default_factory=MetabolitePool)
    gdp_history: list[float] = field(default_factory=list)
    converged: bool = False
    convergence_step: int = 0

    def final_gdp(self) -> float:
        return self.gdp_history[-1] if self.gdp_history else 0.0

    def mean_gdp(self, last_n: int = 20) -> float:
        if not self.gdp_history:
            return 0.0
        return np.mean(self.gdp_history[-last_n:])

    def gdp_variance(self, last_n: int = 20) -> float:
        if not self.gdp_history:
            return 0.0
        return np.var(self.gdp_history[-last_n:])


def run_distributed(
    pathways: list[PathwayProfile] = None,
    n_steps: int = 200,
    atp_regeneration: float = 2.0,
    base_supply: dict[str, float] = None,
) -> SimulationResult:
    """
    Run distributed (biological) economic simulation.

    Each agent adjusts its own production rate based on local feedback.
    No central allocator. Order emerges from individual decisions.
    """
    if pathways is None:
        pathways = PATHWAY_CATALOG

    # Initialize agents
    agents = [EconomicAgent(pathway=p) for p in pathways]

    # Initialize pool with baseline metabolite supply
    pool = MetabolitePool()
    _seed_pool(pool, pathways, base_supply)

    result = SimulationResult(regime="distributed", agents=agents, pool=pool)

    prev_gdp = 0.0
    stable_count = 0

    for step in range(n_steps):
        # Each agent adjusts rate based on local conditions
        for agent in agents:
            agent.adjust_rate_distributed(pool)

        # Each agent produces
        for agent in agents:
            if agent.can_produce(pool):
                agent.produce(pool)

        # ATP regeneration (energy input to the system)
        for agent in agents:
            agent.atp_budget += atp_regeneration

        # External substrate supply (sun, nutrients, etc.)
        if base_supply:
            for met, amount in base_supply.items():
                pool.deposit(met, amount)

        # Record
        pool.record()
        gdp = pool.total_output()
        result.gdp_history.append(gdp)

        # Check convergence (GDP stable within 2% for 20 steps)
        if abs(gdp - prev_gdp) < 0.02 * max(abs(prev_gdp), 1.0):
            stable_count += 1
            if stable_count >= 20 and not result.converged:
                result.converged = True
                result.convergence_step = step
        else:
            stable_count = 0
        prev_gdp = gdp

    result.n_steps = n_steps
    return result


def run_centralized(
    pathways: list[PathwayProfile] = None,
    n_steps: int = 200,
    atp_regeneration: float = 2.0,
    base_supply: dict[str, float] = None,
) -> SimulationResult:
    """
    Run centralized (planned) economic simulation.

    A single allocator decides production rates for all agents.
    Strategy: allocate proportional to ATP efficiency (lowest cost first).
    Collect all output, redistribute evenly.
    """
    if pathways is None:
        pathways = PATHWAY_CATALOG

    agents = [EconomicAgent(pathway=p) for p in pathways]
    pool = MetabolitePool()
    _seed_pool(pool, pathways, base_supply)

    result = SimulationResult(regime="centralized", agents=agents, pool=pool)

    # Central allocator: rank agents by ATP efficiency
    efficiency_rank = sorted(
        agents,
        key=lambda a: a.atp_cost_per_cycle,
    )

    prev_gdp = 0.0
    stable_count = 0

    for step in range(n_steps):
        # Central allocator assigns production rates
        # Strategy: favor low-cost agents, suppress high-cost ones
        total_budget = sum(a.atp_budget for a in agents)

        for i, agent in enumerate(efficiency_rank):
            # Allocate budget proportional to efficiency rank
            rank_weight = (len(agents) - i) / len(agents)
            allocated_rate = rank_weight * 2.0

            agent.current_production_rate = allocated_rate

            if agent.can_produce(pool):
                agent.produce(pool)

        # ATP regeneration
        for agent in agents:
            agent.atp_budget += atp_regeneration

        # External supply
        if base_supply:
            for met, amount in base_supply.items():
                pool.deposit(met, amount)

        pool.record()
        gdp = pool.total_output()
        result.gdp_history.append(gdp)

        if abs(gdp - prev_gdp) < 0.02 * max(abs(prev_gdp), 1.0):
            stable_count += 1
            if stable_count >= 20 and not result.converged:
                result.converged = True
                result.convergence_step = step
        else:
            stable_count = 0
        prev_gdp = gdp

    result.n_steps = n_steps
    return result


def run_perturbation_test(
    pathways: list[PathwayProfile] = None,
    n_trials: int = 50,
    n_steps: int = 200,
) -> dict:
    """
    Remove one agent at a time and compare recovery between regimes.

    Returns dict with robustness scores for distributed vs centralized.
    """
    if pathways is None:
        pathways = PATHWAY_CATALOG

    if not pathways:
        return {"distributed": {}, "centralized": {}}

    results = {"distributed": {}, "centralized": {}}

    # Baseline GDP for each regime
    base_dist = run_distributed(pathways, n_steps=n_steps)
    base_cent = run_centralized(pathways, n_steps=n_steps)
    baseline_dist_gdp = base_dist.mean_gdp()
    baseline_cent_gdp = base_cent.mean_gdp()

    # Remove each pathway and measure GDP recovery
    for i, removed in enumerate(pathways):
        remaining = [p for j, p in enumerate(pathways) if j != i]
        if not remaining:
            continue

        dist_result = run_distributed(remaining, n_steps=n_steps)
        cent_result = run_centralized(remaining, n_steps=n_steps)

        dist_recovery = dist_result.mean_gdp() / baseline_dist_gdp if baseline_dist_gdp > 0 else 0
        cent_recovery = cent_result.mean_gdp() / baseline_cent_gdp if baseline_cent_gdp > 0 else 0

        results["distributed"][removed.name] = dist_recovery
        results["centralized"][removed.name] = cent_recovery

    return results


def _seed_pool(
    pool: MetabolitePool,
    pathways: list[PathwayProfile],
    base_supply: dict[str, float] = None,
):
    """Seed the metabolite pool with initial amounts of all relevant metabolites."""
    all_metabolites = set()
    for p in pathways:
        all_metabolites.update(p.consumes)
        all_metabolites.update(p.produces)

    for met in all_metabolites:
        if met == "ATP":
            continue
        initial = 3.0
        if base_supply and met in base_supply:
            initial = base_supply[met]
        pool.levels[met] = initial


# ---------------------------------------------------------------------------
# Quick summary
# ---------------------------------------------------------------------------

def compare_regimes(dist: SimulationResult, cent: SimulationResult) -> str:
    """Print comparison between distributed and centralized regimes."""
    lines = [
        "=" * 60,
        "REGIME COMPARISON",
        "=" * 60,
        f"{'Metric':<35} {'Distributed':>12} {'Centralized':>12}",
        "-" * 60,
        f"{'Final GDP':<35} {dist.final_gdp():>12.1f} {cent.final_gdp():>12.1f}",
        f"{'Mean GDP (last 20 steps)':<35} {dist.mean_gdp():>12.1f} {cent.mean_gdp():>12.1f}",
        f"{'GDP Variance (last 20)':<35} {dist.gdp_variance():>12.2f} {cent.gdp_variance():>12.2f}",
        f"{'Converged':<35} {str(dist.converged):>12} {str(cent.converged):>12}",
        f"{'Convergence Step':<35} {dist.convergence_step:>12} {cent.convergence_step:>12}",
        "=" * 60,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_economy(dist: SimulationResult, cent: SimulationResult, robustness: dict):
    """Generate Layer 2 figure: GDP over time, perturbation robustness, production convergence."""
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec

    SPIRAL_GREEN = "#2d6a4f"
    SPIRAL_MID   = "#52b788"
    SPIRAL_LIGHT = "#95d5b2"
    GOLD         = "#e9c46a"
    RED          = "#e63946"
    BACKGROUND   = "#0d1117"
    PANEL_BG     = "#161b22"
    TEXT_MAIN     = "#e6edf3"
    TEXT_DIM      = "#8b949e"

    fig = plt.figure(figsize=(20, 7), facecolor=BACKGROUND)
    gs = gridspec.GridSpec(1, 3, wspace=0.3)

    # --- Panel 1: GDP Over Time ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(PANEL_BG)
    steps = range(len(dist.gdp_history))
    ax1.plot(steps, dist.gdp_history, color=SPIRAL_MID, linewidth=2, label="Distributed (biological)")
    ax1.plot(steps, cent.gdp_history, color=RED, linewidth=2, alpha=0.8, label="Centralized (planned)")
    ax1.set_xlabel("Time Step", color=TEXT_MAIN)
    ax1.set_ylabel("GDP (total metabolite output)", color=TEXT_MAIN)
    ax1.set_title("GDP Over Time: Invisible Hand vs Central Planner", color=TEXT_MAIN, fontsize=12, fontweight="bold")
    ax1.legend(facecolor=PANEL_BG, edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN)
    ax1.tick_params(colors=TEXT_DIM)
    for spine in ax1.spines.values():
        spine.set_color(TEXT_DIM)

    # --- Panel 2: Perturbation Robustness ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(PANEL_BG)

    if robustness["distributed"]:
        pathways = list(robustness["distributed"].keys())
        # Shorten names for display
        short_names = [n.replace(" pathway", "").replace(" synthesis", "")[:20] for n in pathways]
        dist_scores = [robustness["distributed"][p] for p in pathways]
        cent_scores = [robustness["centralized"][p] for p in pathways]

        x = np.arange(len(pathways))
        width = 0.35
        ax2.barh(x - width/2, dist_scores, width, color=SPIRAL_MID, label="Distributed")
        ax2.barh(x + width/2, cent_scores, width, color=RED, alpha=0.7, label="Centralized")
        ax2.set_yticks(x)
        ax2.set_yticklabels(short_names, fontsize=7, color=TEXT_MAIN)
        ax2.axvline(x=1.0, color=TEXT_DIM, linestyle="--", linewidth=0.8, alpha=0.5)
        ax2.set_xlabel("GDP Fraction Retained", color=TEXT_MAIN)
        ax2.legend(facecolor=PANEL_BG, edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN, fontsize=8)

    ax2.set_title("Robustness: GDP After Removing One Agent", color=TEXT_MAIN, fontsize=12, fontweight="bold")
    ax2.tick_params(colors=TEXT_DIM)
    for spine in ax2.spines.values():
        spine.set_color(TEXT_DIM)

    # --- Panel 3: Production Rate Convergence ---
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(PANEL_BG)

    colors = plt.cm.Set2(np.linspace(0, 1, len(dist.agents)))
    for i, agent in enumerate(dist.agents):
        if agent.production_history:
            ax3.plot(agent.production_history, color=colors[i], linewidth=1, alpha=0.7,
                     label=agent.name[:18] if i < 8 else None)
    ax3.set_xlabel("Time Step", color=TEXT_MAIN)
    ax3.set_ylabel("Production Rate", color=TEXT_MAIN)
    ax3.set_title("Distributed Rate Convergence (Price Discovery)", color=TEXT_MAIN, fontsize=12, fontweight="bold")
    ax3.legend(facecolor=PANEL_BG, edgecolor=TEXT_DIM, labelcolor=TEXT_MAIN, fontsize=6,
               loc="upper right", ncol=2)
    ax3.tick_params(colors=TEXT_DIM)
    for spine in ax3.spines.values():
        spine.set_color(TEXT_DIM)

    fig_dir = Path(__file__).resolve().parent.parent / "paper" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    out = fig_dir / "layer2_economy.png"
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor=BACKGROUND)
    plt.close(fig)
    print(f"[economy] Saved figure to {out}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Layer 2: Metabolic Economy Simulation")
    print("=" * 60)
    print()

    # Define base supply (external inputs to the system)
    base_supply = {
        "UDP-glucose": 1.0,
        "UDP-GlcNAc": 0.5,
        "Ca2+": 0.5,
        "O2": 2.0,
        "luciferin": 0.3,
        "glycine": 1.0,
        "alanine": 1.0,
        "glutamine": 0.5,
        "piRNA_precursors": 0.2,
        "Zn2+": 0.2,
        "cholesterol": 0.3,
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

    print("\nDone.")
