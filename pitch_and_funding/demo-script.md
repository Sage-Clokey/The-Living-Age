# Living Age -- Laptop Demo Script

**Total runtime:** Under 3 minutes
**Presenter:** Sage Clokey
**Default audience:** SynBioBeta (synthetic biology). See Adaptation Notes at the end for other conferences.

---

## 1. SETUP (before anyone walks up)

Have these three things open and ready, left to right across your desktop:

1. **Terminal 1** -- `cd` into `adaptive_Automation/`. Have `python main.py` ready to run but not yet executed. Make the font large enough to read from three feet away.
2. **Terminal 2** -- `cd` into `Living works by the word/3D-Model_Living_Design/`. Have `python main.py tree --animate` typed and ready.
3. **Browser** -- The live site loaded: `https://sage-clokey.github.io/Living-works-by-the-word/`. Scrolled to the top.

Close everything else. No notifications. No extra tabs.

---

## 2. THE HOOK (10 seconds)

"Nature already knows how to build load-bearing structures, self-repairing walls, and temperature-regulating surfaces -- it just does it in separate organisms. We built the software that finds those capabilities across the tree of life and combines them into a single designable construct."

[Pause. Let it land. Then gesture at the laptop.]

"Let me show you what that looks like."

---

## 3. DEMO 1: Adaptive Automation Pipeline (60 seconds)

[Switch to Terminal 1.]

"This is the Adaptive Genome Design System. It takes a plain English description of what you want a living organism to do and turns it into a designed DNA sequence."

[Run `python main.py`. When the menu appears, type `1` and press Enter.]

[The pipeline will print four steps. As each one appears, narrate:]

**Step 1 -- Interpret:**
"It reads the description -- 'grow a load-bearing structure that self-repairs' -- and maps it to specific genes and organisms. Mycelium for structural scaffolding. Axolotl for regeneration. Coral for biomineralization."

[Point at the organism names and gene symbols as they print.]

**Step 2 -- Retrieve:**
"It pulls real genomic data from UCSC Genome Browser and NCBI -- 220-plus genomes. These are not made-up sequences. This is the actual genetic code that does the job in nature."

[Point at the base-pair counts as each part comes back.]

**Step 3 -- Assemble:**
"Now it checks compatibility -- codon bias, regulatory signals, pathway conflicts -- and adapts the sequences to work together in a single chassis organism. Right now that is Ganoderma, a structural fungus."

**Step 4 -- Output:**
"It writes a FASTA file ready for synthesis, a pathway map showing which organism contributed which part, and a handoff package for AlphaFold to validate the protein structures."

[Let the summary print. Then:]

"That is the pipeline. English in, designed DNA out. The next layer we are building is the bridge between natural language and protein structure using ESM-3."

---

## 4. DEMO 2: Morphogenesis Engine (60 seconds)

[Switch to Terminal 2.]

"The genome pipeline designs what the organism can do. This next piece simulates how it grows."

[Run `python main.py tree --animate`.]

[A 3D window will open and the structure will grow in real time -- branches extending, splitting, tapering.]

"This is a morphogenesis engine. It simulates branching growth with real biophysical parameters -- tropism, collision avoidance, taper, branching probability. What you are watching is not animation. It is simulation. Each branch tip makes decisions based on its local environment."

[Let it grow for about 15 seconds. Then:]

"We have three modes built."

[Close the window. Run `python main.py coral --animate`.]

"Coral -- spreading, mineral-depositing growth."

[Let it run 10 seconds, then close. Run `python main.py spiral --animate`.]

"And spiral -- the geometry you see across shells, horns, and plant growth."

[Let it run 10 seconds.]

"There is also a gene regulatory network mode that drives growth decisions through simulated gene expression -- not just geometry, but developmental logic. The long-term goal is to connect the genome pipeline to this engine so you can design an organism and then watch it grow before you ever touch a lab bench."

[Close the viewer.]

---

## 5. DEMO 3: The Website (30 seconds)

[Switch to the browser.]

"This is the public-facing site for the project."

[Scroll slowly from the top.]

"The vision -- designing with life instead of against it."

[Scroll to the poster section if visible.]

"We have a full poster collection across structural biology, morphogenesis, and the philosophical framework behind the work."

[Scroll to the design lab section if visible.]

"And here is the design lab -- where the simulations and genome tools live on the web."

[Stop scrolling.]

"Everything is open. The code is on GitHub. The writings are published. This is not a stealth project. We are building in the open because the idea is bigger than any one lab."

---

## 6. THE ASK (15 seconds)

"What we need next is wet lab access. The software designs constructs. We need a bench to test them. We are looking for three things:"

[Count on fingers.]

"One -- a lab partnership or residency where we can validate the first designs in vivo."

"Two -- collaborators in synthetic biology, developmental biology, or biomaterials who want to work on living architecture."

"Three -- funding to bridge from software to physical prototypes. We have SBIR applications in progress and we are open to the right investor or grant."

[Hand them a card or point to the site URL.]

"The site has everything -- the code, the writings, the pitch deck. I would rather you read it than take my word for it."

---

## 7. ADAPTATION NOTES

### SynBioBeta (default -- lead with the technology)

Use the script as written above. This audience wants to see working tools and real data. Emphasize:
- The retrieval layer pulls from real databases (UCSC, NCBI), not synthetic data.
- The compatibility engine addresses actual integration challenges (codon bias, regulatory conflicts).
- The morphogenesis engine is simulation, not rendering.
- The ask is lab access and collaborators.

### FreedomFest (lead with philosophy, show biology as proof)

Replace THE HOOK with:

"Every centralized system eventually fails because it fights the pattern that living things follow -- distributed intelligence, local adaptation, voluntary cooperation. That is not a metaphor. It is biology. And we built software that works with that pattern instead of against it."

Run Demo 1 the same way, but reframe the narration:

"Notice what this system does not do. It does not engineer from the top down. It finds what nature already solved, respects the boundaries of each organism, and adapts the parts to cooperate. No central authority decides the design. The design emerges from compatibility."

Skip Demo 3 or replace it with a quick scroll through the philosophical writings on the site. Adjust THE ASK to emphasize intellectual allies and the libertarian case for decentralized biotech.

### YALCON (lead with the invitation to join)

Replace THE HOOK with:

"You are the generation that will either inherit a world designed against life or build one designed with it. This is what building with it looks like."

Keep the demos short -- 30 seconds each. Spend more time on the vision and the invitation. Adjust THE ASK to:

"If this resonates with you, there is a place in this project for you. Writers, coders, biologists, philosophers. The site has everything. The code is open. Start reading and reach out."

### Cato University (lead with the intellectual argument)

Replace THE HOOK with:

"The engineering paradigm of the last two centuries treats nature as raw material to be controlled. The result is brittle systems that require constant maintenance and centralized management. There is an alternative -- designing with the logic that living systems already use. Distributed, adaptive, self-repairing. We built the first tools to do that at the genomic level."

Run Demo 1 with emphasis on the assembly logic -- how the system resolves conflicts through adaptation rather than override. Frame it as an example of spontaneous order applied to biotechnology.

For THE ASK, emphasize the intellectual contribution: "We need rigorous thinkers who understand why decentralized systems outperform centralized ones and who want to see that principle applied beyond economics."

---

## Timing Checklist

| Section | Target | Running Total |
|---------|--------|---------------|
| Hook | 10 sec | 0:10 |
| Demo 1: Genome Pipeline | 60 sec | 1:10 |
| Demo 2: Morphogenesis | 60 sec | 2:10 |
| Demo 3: Website | 30 sec | 2:40 |
| The Ask | 15 sec | 2:55 |

If you are running long, cut Demo 3 entirely. The two technical demos carry the weight.

---

## Failure Modes and Recovery

**If the genome pipeline errors on network calls:**
Say: "The retrieval layer hits live databases -- UCSC and NCBI -- so it depends on conference Wi-Fi. Let me show you a cached run." Then open a previously saved output directory and walk through the FASTA file and pathway map.

**If the 3D viewer does not render (no GPU, display issues):**
Run with `--export --no-view` instead. Open the exported JSON in a text editor and say: "The simulation ran -- here are the segment coordinates. On a proper display this renders as a branching 3D structure." Then pull up a screenshot if you have one saved.

**If someone asks a question mid-demo:**
Answer it. The demo is a conversation starter, not a performance. If the question is better than the next demo, follow the question.
