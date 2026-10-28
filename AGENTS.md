# AGENTS.md

## Project purpose

This repository contains a paper proposing ten desiderata for continual reinforcement learning (CRL), reviewing representative literature, and outlining a companion benchmark.

The manuscript is an opinionated scientific synthesis, not a comprehensive survey.
Edits should preserve the distinction between:

- what a desideratum means;
- what cited work actually demonstrates;
- assumptions and evaluation limitations;
- what remains unestablished for the paper's broader CRL target.

## Authoritative files

- `crl_desiderata.tex` is the canonical manuscript.
- `crl_desiderata.bib` is the canonical bibliography.
- `figures/` contains the manuscript figures and their editable sources.
- `build/` contains generated LaTeX output and should not be edited manually.

## Collaboration workflow

- When asked to discuss, assess, or propose wording, do not edit files until the user approves a concrete version.
- When asked to apply, fix, add, or remove something, edit the relevant source files and validate according to the type of change, as described under Building and validation.
- Before revising prose, read the complete surrounding paragraph and enough of the neighboring paragraphs to preserve the argument's flow.
- Make focused changes. Do not rewrite unrelated passages or silently apply reviewer suggestions beyond the requested scope.
- Preserve deliberate notes and draft material unless asked to turn them into prose.
- When renaming or reframing a desideratum, search for all textual occurrences and check the subsection title, brief box, benchmark coverage table (`tab:benchmark-coverage`), companion diagnostics table (`tab:companion-diagnostics`), cross-references, benchmark discussion, conclusion, and overview figure.

## Manuscript style

- Write the paper in US English and use US spelling consistently.
- In continuous prose, including captions and content notes, place each complete grammatical sentence on exactly one source line: do not put more than one sentence on a line or split one sentence across multiple lines; only structural LaTeX, tabular rows, and sentences interrupted by a displayed equation are exempt.
- Match the existing scientific style: direct, readable, compact, and precise.
- Prefer simple words when they express the same claim accurately.
- Build paragraphs around one identifiable argument. Sentences should connect logically rather than read as independent observations.
- Avoid paragraph openings with unclear references such as "This," "These," or "Such" when the antecedent lies in another paragraph.
- Avoid repeatedly relying on constructions such as "A rather than B," "however," "although," or long enumerations.
- Avoid vague formulations such as "makes [...] concrete" or "makes [...] explicit"; state specifically what a method demonstrates, illustrates, implements, or operationalizes.
- Be cautious with anthropomorphic language. Prefer operational descriptions of what an agent or system computes or does; retain established terms such as memory, attention, or reasoning only when their technical meaning is clear from context.
- Do not add roadmap sentences that merely announce what the following prose will say when the argument can begin directly.
- Preserve the paper's position that the ten desiderata are desirable properties, not necessary conditions or a definition of CRL.

## Project terminology and conceptual boundaries

- Use `ability` for something the agent can behaviorally do. In the discussion of stability and forgetting, prefer `useful abilities` for behaviors that remain applicable or may be needed again.
- Reserve `functionality` for the operation of a model, module, or system component. Do not use it as a loose synonym for an agent's abilities.
- Use `skill` for a learned, reusable behavior or policy component, especially under `\Dref{7}` and `\Dref{10}`.
- Use `capability` for a broader property of the agent or complete learning system. Use `competence` only for an aggregate level or portfolio of abilities, not when one specific ability is meant.
- Use `experience` for the agent's interaction history, `information` for particular content that can be retained or retrieved, and `knowledge` for learned regularities or relations that can guide behavior beyond one recorded event.
- Use `representation` for the internal form in which information or knowledge is encoded. Do not treat stored data, parameters, representations, and knowledge as interchangeable.
- Preserve the distinction between `memory` and `storage`: memory is the behavioral capability to preserve, retrieve, revise, and release information under `\Dref{6}`, while storage is the physical or computational resource constrained by `\Dref{3}`.
- Keep storage, model capacity, and computation separate when discussing `\Dref{3}`. Do not use `memory` as a collective label for all three.
- A `task identity` or `task boundary` is externally supplied information about problem structure. An `objective` specifies what outcomes matter, while a `goal` or `subgoal` is a target used in planning. Task-free learning does not imply objective-free or goal-free learning.
- `Task-free` means that task identities and boundaries are not supplied to the complete learning system; the agent may still infer latent contexts or construct its own segmentation.
- `Non-episodic` concerns continuity of state and action consequences, not merely whether an implementation exposes an episode counter or termination flag.
- `Online` means that new experience can continue to affect the complete learning system and its future behavior during deployment; it does not require every neural-network parameter to keep changing.
- `Continuous` (and `continuously`) describes an uninterrupted process in temporal prose, or an explicitly mathematical property such as a continuous state or action space. Do not use `continuously learning` as a synonym for `continual learning`, since continual learning does not require uninterrupted updating.
- `Continual` describes learning and adaptation sustained over an agent's lifetime. Use `continual learning`, `continual learner`, and `continual agent` when referring to this learning capability. Updates may be intermittent, and individual components or parameter sets may remain fixed.
- `Continuing` describes the temporal structure of a task, interaction, environment, or lifetime: interaction persists without being divided into independent episodes, and state and action consequences carry forward. Continuing interaction alone does not establish continual learning, and continual learning can be studied under episodic protocols. When emphasizing persistent deployment, prefer `the same agent throughout a continuing interaction` over `a continuing learner` or `a continuing agent`.
- Use `sensing` for acquiring sensory information and `perception` for interpreting it. `Active sensing` refers to learned control over which sensory information is acquired.
- Keep the two uses of hierarchy distinct: `\Dref{4}` concerns the system's functional organization and allocation of computation, while `\Dref{10}` concerns planning with reusable skills and subplans.
- `Concurrent` planning means maintaining overlapping ongoing plans. Their actions may execute in parallel, be interleaved in one sequential action stream, or be distributed among cooperating agents; concurrency does not require literal parallel execution.
- Preserve the division among the final three behavioral desiderata: `\Dref{8}` predicts possible consequences, `\Dref{9}` compares them across time, objectives, and uncertainty, and `\Dref{10}` organizes actions and subplans to bring selected outcomes about.
- A `world model` is defined by its predictive use, not by the presence of a separately named module. An explicit world-model architecture is neither necessary nor sufficient evidence for `\Dref{8}`.
- Distinguish the Section 4 terminology consistently: `playable companion` describes the contribution's explanatory role, `scenario` denotes its world and rule set, and `benchmark` denotes an evaluative instantiation that pairs the scenario with a configuration, protocol, and diagnostic readouts.

## Desiderata conventions

- Use `\Dref{1}` through `\Dref{10}` for references to desiderata in prose so that they remain linked.
- Each desideratum with an established summary uses the following structure, shown for D1:

  ```latex
  \begin{briefbox}[protocolbrief]{D1}
      \emph{...}
  \end{briefbox}

  \noindent ...
  ```

- Preserve the existing styles: `protocolbrief` for D1, `systembrief` for D3 and D4, `boundarybrief` for D5, and `behaviorbrief` for D2 and D6--D10. D5's green dashed border is intentional.
- Brief boxes should be understandable without the detailed discussion, use the terminology from the subsection title, and state the central idea without literature review or extensive cross-references.
- Preserve the conceptual classification used in the paper:
  - `\Dref{1}` is protocol-level.
  - `\Dref{3}`--`\Dref{5}` are primarily system-level.
  - `\Dref{2}` and `\Dref{6}`--`\Dref{10}` have behavioral cores.
- The placement of `\Dref{2}` before the system-level desiderata is intentional because stability and plasticity are fundamental to the later capabilities.
- When linking desiderata, explain the boundary between them instead of merely listing related desiderata.
- Do not prescribe a particular architecture unless that restriction is part of the desideratum itself.

## Benchmark coverage

- The benchmark coverage table (`tab:benchmark-coverage`) compares benchmarks, testbeds, and diagnostic studies, not learning methods. Base ratings on the reported evaluation setups and readouts, distinguishing environmental opportunities from capabilities that the evaluations actually probe.
- For rows covering several reported setups, assess the three D1 conditions independently within the row's stated scope: a full rating means at least one included setup meets that condition. The three ratings may refer to different setups and do not establish that all three conditions coexist in one setup.
- The companion's ratings refer to a single proposed core configuration that combines all three D1 conditions with the indicated behavioral diagnostics.
- Keep ratings, symbol definitions, table notes, the evaluation-landscape discussion, and the companion diagnostics table (`tab:companion-diagnostics`) consistent. Coverage ratings describe what an evaluation probes; they do not establish that an agent satisfies a desideratum in full.

## Citations and source checking

- Read the cited paper before making or revising a substantive claim about it.
- Prefer primary sources for technical claims.
- Separate an author's stated conclusions from our interpretations and explicitly label inferences.
- Distinguish limitations of a method from limitations of its reported evaluation. Do not imply that finite or narrow experiments disprove a capability; state what they do and do not establish.
- Use cautious evidential language. Prefer "does not establish," "leaves open," or "was not evaluated" over "cannot" or "fails" unless the stronger claim is supported.
- Treat biological findings as motivation or inspiration unless they directly establish a claim about artificial systems.
- Attach citations as closely as possible to the claims they support.
- Use `et al.\ ` with protected LaTeX whitespace.
- Prefer published, peer-reviewed versions over preprints when available.
- An arXiv DOI belongs only to the arXiv version; do not attach it to a conference or journal entry.

## Bibliography conventions

- Keep `crl_desiderata.bib` alphabetically ordered by citation key.
- Use author-year keys, adding `a`, `b`, and so forth when disambiguation is necessary.
- Store the complete author list in each entry. The existing `@IEEEtranBSTCTL` entry controls displayed truncation.
- Verify author names, title, venue, volume, issue, pages or article number, year, and any DOI online against primary sources for the exact cited version; do not add an unverified DOI.
- Preserve braces needed for acronyms, proper names, and intentional capitalization.
- Keep entry types and venue fields consistent with the published version.
- The bibliography currently avoids `url` fields; do not introduce isolated URLs without a deliberate project-wide decision.
- Remove unused entries only after confirming that they are not intentionally retained for unfinished notes or sections.

## LaTeX and formatting

- Preserve IEEEtran compatibility.
- Keep `crl_desiderata.tex` and `crl_desiderata.bib` ASCII-only. Encode diacritics, special characters, and typographic punctuation with LaTeX commands, preserving the correct rendered spelling of author names and titles.
- Indent `crl_desiderata.tex` and `crl_desiderata.bib` with four spaces per indentation level and do not use tabs.
- Do not leave trailing spaces or tabs in `crl_desiderata.tex` or `crl_desiderata.bib`; blank lines must be completely empty.
- Use the existing macros and environments instead of reproducing their formatting locally.
- Define custom colors using the `HTML` model with uppercase six-digit hex values throughout the LaTeX sources, including files under `figures/`.
- Do not manually edit generated `.aux`, `.bbl`, `.log`, `.out`, `.pdf`, or SyncTeX files.
- Avoid broad mechanical reformatting.
- When changing a table, box, or figure, inspect the compiled result for page breaks, overflow, and column layout.

## Building and validation

Run `make check` (or plain `make`) from the repository root after changes to the manuscript, bibliography, figure or table sources, or LaTeX build configuration.
This compiles the paper and checks the main `.tex` and `.bib` files for ASCII, indentation tabs, and trailing spaces, and the compilation log for undefined citations or references and overfull boxes.
Use the project `.latexmkrc` for direct `latexmk` invocations; see the [README](README.md#development) for build commands and output paths.

For documentation-only changes, check Markdown formatting and links; recompiling an unchanged manuscript is unnecessary.
For workflow changes, validate YAML and shell syntax, and verify the build when compilation commands or dependencies change.
Treat ordinary underfull-box warnings as non-fatal unless the edit introduced a visible layout problem.
Report which checks ran and any relevant unresolved warnings or validation limitations.
