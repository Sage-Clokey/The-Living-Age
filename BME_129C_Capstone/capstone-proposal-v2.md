# BME 129C Capstone Project Proposal

## Project Title

**The English-to-Protein Bridge: A Natural Language Interface for Biological Sequence Design**

---

## Student

Sage Clokey, B.S. Bioinformatics, Spring 2026

## Advisor

R. Dubois, BME 129C: Design/Implement BME

---

## Why This Matters

Nature has already solved the structural and functional problems that engineering still struggles with. Mycelium grows load-bearing networks without blueprints. Coral deposits mineral architecture from seawater. Planaria regenerate entire bodies from fragments. Spider silk outperforms steel by weight. These are not curiosities — they are 3.8-billion-year-old proofs that life knows how to build.

The question is not whether living systems can solve human problems. The question is whether we can learn to ask them to.

Today, that answer is no — not because the biology is missing, but because the tools are. A researcher who wants to design a protein with a specific biological function must navigate a fragmented landscape of specialized software: BLAST for homology search, UCSC Genome Browser for genome navigation, NCBI Entrez for sequence retrieval, codon optimization calculators, and protein structure predictors. Each tool addresses one step. Each speaks its own input language. Each returns output that requires specialist interpretation before the next step can proceed.

This fragmentation creates a problem even for specialists. Consider a concrete example: a researcher wants to design an enzyme that cross-links fungal cell wall polymers under mechanical stress — a protein that would make a mycelium structure grow stronger under load, the way bone does. Today, that researcher must manually: (1) identify relevant gene families across multiple organisms, (2) retrieve and align reference sequences from separate databases, (3) assess codon compatibility with the target expression host, (4) check for regulatory and pathway-level conflicts, and (5) interpret each result before proceeding to the next step. Each step requires different software, different query syntax, and significant time — even for someone fluent in all of them.

For the non-specialist — the architect wondering whether mycelium can be engineered to bear structural load, the community builder asking whether a living wall could repair itself — the barrier is absolute. The tools demand expertise before they offer answers.

There is no system that allows a researcher to describe a desired biological function in plain English and receive a designed, compatibility-scored protein sequence as output. This project proposes to build one — not as a technical exercise, but as the first step toward a world where designing with living systems is as accessible as describing what you want them to do.

### The Larger Vision

This capstone is the first phase of the Adaptive Genome Design System, a platform whose long-term goal is to make biological sequence design accessible to non-specialists. The north star is living architecture — houses that are organisms, that grow from a seed, strengthen under load, repair their own damage, and return to the earth when their time is done.

That vision requires solving three biological problems in sequence: molecular machines (what each gene does), control (when and where each gene activates), and form (how a culture grows into a complex 3D shape). This capstone addresses the first problem — designing proteins from functional descriptions — and lays the foundation for everything that follows.

The system is designed for open-source release. The compatibility engine, codon optimization tables, and bridge architecture are intended to be freely available to the synthetic biology community, including iGEM teams and academic researchers. Living systems belong to everyone. The design language should too.

---

## What This Project Builds

### Existing Foundation

This capstone builds on the Adaptive Genome Design System, a software platform developed by the student over the preceding quarters. The system is operational and includes the following modules:

| Module | Capability |
|--------|-----------|
| `retrieval/ucsc_client.py` | Programmatic access to 220+ genomes via the UCSC Genome Browser REST API |
| `retrieval/ncbi_client.py` | Retrieval of sequences from NCBI Entrez (Gene, Nucleotide, Protein databases) for organisms outside UCSC coverage, including fungi, coral, and invertebrates |
| `retrieval/species_search.py` | Natural language mapping to species and gene targets across eight functional capability categories |
| `models/genomic_part.py` | A unified `GenomicPart` data model that normalizes sequences from heterogeneous sources into a common representation including organism, function, GO terms, codon usage profile, regulatory signals, and interaction partners |
| `compatibility/codon.py` | Codon usage analysis using Relative Synonymous Codon Usage (RSCU) tables for five chassis organisms, with Codon Adaptation Index (CAI) scoring |
| `compatibility/regulatory.py` | Regulatory element compatibility detection, including cross-kingdom conflict identification for promoters, ribosome binding sites, and transcription factor binding sites |
| `compatibility/pathway.py` | Pathway-level conflict analysis across 12 metabolic and signaling pathway profiles, detecting resource competition, feedback loop disruption, and signaling crosstalk |
| `assembly/assembler.py` | Adaptive four-step assembly engine that resolves codon, regulatory, and pathway conflicts through iterative optimization |
| `output/formatter.py` | FASTA output generation, pathway contribution maps, modification logs, and AlphaFold/ESMFold handoff packages |

The full pipeline runs end-to-end via `main.py`. All modules are functional and tested. The codebase is available at github.com/Sage-Clokey/adaptive-Automation.

### Proposed Extension

This project extends the existing system with two new layers:

1. **An English interpretation layer** (Claude API) that parses free-form natural language descriptions of desired biological functions into structured biological specifications — including GO terms, target organisms, functional constraints, and estimated sequence parameters.

2. **A protein language model bridge** (ESM-3) that accepts these structured specifications, generates candidate amino acid sequences conditioned on the specified function, and feeds them into the existing compatibility and assembly pipeline for codon optimization, regulatory analysis, and pathway conflict detection.

The result is an end-to-end system where a user provides a single English sentence describing what they want a protein to do, and the system returns designed, scored, and explained candidate sequences.

A terminal-based interactive interface (REPL) provides the user-facing interaction layer, displaying each pipeline stage in real time with streaming LLM output and structured result panels.

---

## Background and Prior Work

### Protein Language Models

ESM-3 (Evolutionary Scale Modeling, version 3) is a 1.4-billion-parameter protein language model developed by the EvolutionaryScale team at Meta FAIR (Lin et al., 2023; Hayes et al., 2024). Trained on billions of protein sequences, ESM-3 learns the statistical grammar of protein space and can generate novel amino acid sequences conditioned on functional annotations, including Gene Ontology (GO) terms. ESM-3 accepts function annotation tokens as conditioning input and generates sequences via iterative sampling, producing proteins that are statistically consistent with the specified function.

The open-weight variant (`esm3-sm-open-v1`) is available for non-commercial research use and runs on consumer-grade GPU hardware.

### Large Language Models as Biological Interpreters

Large language models (LLMs) such as Claude (Anthropic) have demonstrated strong performance in biological text comprehension, including extraction of gene names, GO terms, organism identifiers, and functional relationships from unstructured descriptions. The Claude API supports structured output (JSON schemas), extended reasoning (chain-of-thought), and streaming responses, making it suitable as an interpretation layer that translates natural language into the structured biological specifications required by downstream computational tools.

### Relevant Literature

- Lin, Z. et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*, 379(6637), 1123-1130.
- Hayes, T. et al. (2024). Simulating 500 million years of evolution with a language model. *bioRxiv*.
- Rives, A. et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*, 118(15).
- Ashburner, M. et al. (2000). Gene ontology: tool for the unification of biology. *Nature Genetics*, 25(1), 25-29.
- Sharp, P.M. & Li, W.H. (1987). The codon adaptation index -- a measure of directional synonymous codon usage bias, and its potential applications. *Nucleic Acids Research*, 15(3), 1281-1295.
- Kent, W.J. et al. (2002). The human genome browser at UCSC. *Genome Research*, 12(6), 996-1006.

---

## Technical Approach

### Phase 1a: English Interpretation Layer

**Module:** `llm/claude_interface.py`

The interpretation layer accepts a free-form English string (e.g., "design a protein that cross-links fungal cell walls under mechanical stress") and returns a `BiologicalSpec` data structure containing:

- A precise biological function description, technically normalized
- Gene Ontology term IDs capturing the requested function (e.g., GO:0005618 for cell wall, GO:0016491 for oxidoreductase activity, GO:0009612 for response to mechanical stimulus)
- Target organism for expression (default: *Ganoderma lucidum*, a well-characterized fungal chassis)
- Chassis type classification (eukaryote_fungal, prokaryote, plant, etc.)
- Desired physical and biochemical properties (secreted, membrane-bound, mechanosensitive, etc.)
- Estimated amino acid sequence length
- Biological rationale for all parameter choices
- Caveats and confidence qualifications

Implementation uses the Claude API with structured JSON output schemas and extended thinking enabled, ensuring that biological translation is treated as a non-trivial reasoning task. The system prompt encodes domain knowledge about protein families, organism capabilities, and the mapping between colloquial functional descriptions and formal biological ontology.

### Phase 1b: ESM-3 Protein Generation Bridge

**Module:** `bridge/esm_bridge.py`

The bridge layer accepts a `BiologicalSpec` and performs the following:

1. **GO term mapping:** Translates GO term IDs from the biological specification into ESM-3 function annotation tokens (`FunctionAnnotation(label=go_term, start=0, end=length)`).

2. **Sequence generation:** Calls ESM-3 to generate N candidate amino acid sequences (default: 3) conditioned on the function annotations and target length. Generation uses iterative decoding with 8 sampling steps at temperature 0.7, balancing sequence diversity against functional plausibility.

3. **Sequence scoring:** Each candidate is scored using ESM-3's log-likelihood metric, which measures how consistent the generated sequence is with the model's learned distribution of functional proteins. Higher scores indicate greater biological plausibility.

4. **Validation:** Generated sequences are checked for internal stop codons, anomalous amino acid composition, and known problematic sequence motifs.

A mock fallback mode generates synthetic placeholder sequences (clearly labeled) when ESM-3 is unavailable, allowing the full pipeline to be demonstrated and tested without GPU resources.

### Phase 1c: Codon Back-Translation and Compatibility Integration

Each generated amino acid sequence is back-translated to a codon-optimized DNA sequence using the target organism's RSCU table from the existing `compatibility/codon.py` module. Back-translation is deterministic: for each amino acid, the codon with the highest RSCU value in the target organism is selected.

The resulting DNA sequences are wrapped in `GenomicPart` objects and passed through the full compatibility pipeline:

- **Codon analysis:** CAI scoring against the target organism's usage table, GC content assessment
- **Regulatory analysis:** Detection of inadvertent cross-kingdom regulatory signals, promoter/terminator compatibility
- **Pathway analysis:** Metabolic resource competition (e.g., O2 consumption for oxidoreductases competing with other engineered pathways), feedback loop integrity

### Phase 1d: Interactive Terminal Interface (REPL)

**Module:** `main.py` (extended)

The REPL provides an interactive design session using the `rich` Python library for formatted terminal output. Each pipeline stage is displayed as it executes:

1. Claude's interpretation streams in real time, showing GO term extraction and biological reasoning
2. ESM-3 generation progress displays per-candidate scores as sequences complete
3. Codon optimization results show CAI and GC content per candidate
4. Compatibility analysis results display pass/warn/fail indicators per analysis type
5. Claude's final explanation streams as a plain-English summary of what was designed and why

The interface supports command-line flags (`--organism` to override default chassis, `--candidates N` for sequence count, `--mock` for demo mode without ESM-3) and conversational follow-up within a design session.

---

## Deliverables

### Weeks 1-3: English Interpretation Layer

- Implement `llm/claude_interface.py` with `BiologicalSpec` output schema
- Develop and validate system prompt for biological interpretation
- Test against 10+ diverse natural language input descriptions
- Validate GO term extraction accuracy against manual annotation
- Deliverable: Claude correctly parses natural language design requests into structured biological specifications

### Weeks 4-6: ESM-3 Bridge and Protein Generation Pipeline

- Implement `bridge/esm_bridge.py` with GO-to-function-token mapping
- Implement sequence generation, scoring, and validation pipeline
- Implement mock fallback for GPU-free testing
- Implement codon back-translation using existing RSCU tables
- Test generated sequences for structural plausibility (length distribution, amino acid composition, absence of pathological motifs)
- Deliverable: The system generates candidate protein sequences from structured biological specifications

### Weeks 7-8: Integration with Compatibility Engine

- Connect ESM-3 bridge output to existing `GenomicPart` model and compatibility pipeline
- Validate end-to-end flow: English input to compatibility-scored DNA output
- Implement Claude explanation of combined results (sequences + compatibility analysis)
- Test with the reference design problem: "design a protein that cross-links fungal cell walls under mechanical stress"
- Deliverable: Full pipeline runs end-to-end, producing scored and explained candidates

### Weeks 9-10: Interface, Testing, Documentation, and Final Demo

- Implement rich terminal REPL with streaming display
- Conduct usability testing: can a user without bioinformatics expertise operate the system?
- Write technical documentation for all new modules
- Prepare final demonstration covering multiple design scenarios
- Deliverable: Polished interactive system with documentation, demonstrated on diverse design problems

---

## Evaluation Criteria

The system will be evaluated against the following criteria:

1. **Interpretation accuracy.** Given 10+ diverse natural language design requests spanning different protein functions, organisms, and design constraints, does Claude extract biologically correct GO terms, appropriate target organisms, and reasonable sequence parameters? Validation by comparison to manual expert annotation.

2. **Sequence validity.** Do ESM-3-generated protein sequences exhibit properties consistent with the requested function? Metrics include: ESM-3 log-likelihood scores, amino acid composition statistics, absence of internal stop codons, and sequence length consistency with known proteins of similar function.

3. **Compatibility scoring.** Do generated sequences pass through the codon, regulatory, and pathway compatibility analyses without critical conflicts? Where conflicts are flagged, are they biologically meaningful (e.g., oxygen competition between oxidoreductase and bioluminescence pathways)?

4. **Usability.** Can a user who is not a bioinformatics specialist use the REPL interface to describe a desired protein function and understand the system's output? Assessed through informal usability testing with peers.

5. **End-to-end function.** Does the complete pipeline -- from English input to compatibility-scored, codon-optimized DNA output with plain-English explanation -- execute without failure across multiple design scenarios?

---

## Relevance to Biomedical Engineering

This project sits at the intersection of computational biology, synthetic biology, and human-computer interaction -- three domains central to biomedical engineering.

**Computational biology.** The system integrates protein language models (ESM-3), large language models (Claude), genome databases (UCSC, NCBI), and codon optimization algorithms into a unified design pipeline. The technical challenge of bridging natural language semantics to protein sequence space is a novel contribution to computational biodesign.

**Synthetic biology.** The output of this system -- codon-optimized DNA sequences encoding designed proteins -- is directly relevant to synthetic biology workflows. Researchers in tissue engineering, biomaterials, and therapeutic protein design face the same fragmentation problem this system addresses: translating a functional requirement into a testable sequence candidate.

**Human-computer interaction.** The natural language interface represents a new interaction paradigm for biological design tools. Current tools require users to speak the language of the tool (BLAST query syntax, genome coordinates, codon tables). This system inverts that requirement: the tool learns to speak the language of the user.

**Broader applications.** While this project uses fungal chassis organisms as the default context (motivated by the student's research in living architecture and biomaterials), the system is organism-agnostic. The same pipeline applies to therapeutic protein design, agricultural biotechnology, environmental remediation, and any domain where proteins are designed for specific functions.

---

## Existing Codebase

- **Repository:** github.com/Sage-Clokey/adaptive-Automation
- **Foundation modules (all functional):**
  - `retrieval/` -- UCSC and NCBI clients, species search
  - `models/` -- GenomicPart data model
  - `compatibility/` -- Codon, regulatory, and pathway analysis
  - `assembly/` -- Adaptive sequence assembly engine
  - `output/` -- FASTA formatting and handoff packages
- **This project extends the system.** Phase 1 adds new modules (`llm/`, `bridge/`) and extends `main.py`. It does not modify existing modules; it imports from them.

---

## Tools and Technologies

| Component | Tool | Role |
|-----------|------|------|
| English interpretation | Claude API (Anthropic) | Natural language to structured biological specification |
| Protein generation | ESM-3 (`esm3-sm-open-v1`, EvolutionaryScale/Meta FAIR) | Function-conditioned amino acid sequence generation |
| Genome retrieval | UCSC Genome Browser REST API, NCBI Entrez | Reference sequences, annotations, organism data |
| Codon optimization | Custom RSCU tables (existing module) | Back-translation from amino acid to organism-optimized DNA |
| Compatibility analysis | Custom pipeline (existing modules) | Codon, regulatory, and pathway conflict detection |
| Terminal interface | Python `rich` library | Formatted, streaming REPL display |
| Language | Python 3.11+ | All modules |
| Deep learning runtime | PyTorch | Required by ESM-3 |

---

## References

1. Lin, Z. et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*, 379(6637), 1123-1130.
2. Hayes, T. et al. (2024). Simulating 500 million years of evolution with a language model. *bioRxiv*. doi:10.1101/2024.07.01.600583.
3. Rives, A. et al. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. *PNAS*, 118(15), e2016239118.
4. Ashburner, M. et al. (2000). Gene ontology: tool for the unification of biology. *Nature Genetics*, 25(1), 25-29.
5. Sharp, P.M. & Li, W.H. (1987). The codon adaptation index -- a measure of directional synonymous codon usage bias, and its potential applications. *Nucleic Acids Research*, 15(3), 1281-1295.
6. Kent, W.J. et al. (2002). The human genome browser at UCSC. *Genome Research*, 12(6), 996-1006.
7. The Gene Ontology Consortium. (2021). The Gene Ontology resource: enriching a GOld mine. *Nucleic Acids Research*, 49(D1), D325-D334.
8. Jumper, J. et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*, 596, 583-589.

---

*Prepared for BME 129C: Design/Implement BME, Spring 2026, UC Santa Cruz.*
