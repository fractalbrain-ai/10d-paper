# Continual Reinforcement Learning Is an Integration Problem

[![Paper PDF][pdf-badge]][paper-pdf]
[![Playable companion][companion-badge]][browser-game]

This repository contains the LaTeX sources for *Continual Reinforcement Learning
Is an Integration Problem*. The paper presents ten desiderata for continual
reinforcement learning and examines representative approaches and evaluation
settings.

The paper also introduces a small game as a playable companion to the
desiderata and outlines a proposed benchmark based on its rules. The game
takes place in a persistent world designed to illustrate how several
behavioral capabilities interact within one agent's lifetime. Its implementation
is available in the [10d-game repository][companion], and you can
[play it in your browser][browser-game] without installing anything.

## Repository files

- [`crl_desiderata.tex`][manuscript] is the main source of the paper.
- [`crl_desiderata.bib`][bibliography] contains the bibliography.
- [`figures/`][figures] contains the figures and more complex tables.
- [`AGENTS.md`][editing] summarizes the editing conventions and terminology.

## Development

### Build the paper

The paper uses pdfLaTeX and BibTeX from a LaTeX installation such as TeX Live.
With latexmk installed, run the following command from the repository root so
that it picks up the [project configuration][latexmk-config]:

```bash
latexmk
```

The PDF is written to `build/crl_desiderata.pdf` (note that the `build/`
directory is listed in `.gitignore`).

Under the hood, latexmk runs the pdfLaTeX and BibTeX passes needed to resolve
citations and cross-references. To run these passes yourself:

```bash
mkdir -p build
pdflatex -output-directory=build crl_desiderata.tex
bibtex build/crl_desiderata
pdflatex -output-directory=build crl_desiderata.tex
pdflatex -output-directory=build crl_desiderata.tex
pdflatex -output-directory=build crl_desiderata.tex
```

LaTeX believes in repeated experience. We recommend the magic of `latexmk`. 🪄

### Check the sources

The [Makefile][makefile] also offers a build with additional checks:

```bash
make
```

This is equivalent to `make check`: both run `check.sh`, which calls latexmk
and checks source formatting, unresolved citations and references, and overfull
boxes. Remove auxiliary build files with:

```bash
make clean
```

### Prepare an arXiv upload

With `zip` installed, run:

```bash
make arxiv
```

This runs the checks above and creates `build/crl_desiderata-arxiv.zip` with
the LaTeX sources, bibliography, and required images.
The archive is rebuilt only when its sources or packaging rules change.

### Automated builds

Pushes to `main` trigger the GitHub Actions workflow, which runs `make check`
and updates the [PDF hosted on GitHub Pages][paper-pdf] if all checks pass.

[pdf-badge]: https://img.shields.io/badge/paper-PDF-B85450
[companion-badge]: https://img.shields.io/badge/companion-play-2B7A78
[companion]: https://github.com/fractalbrain-ai/10d-game
[browser-game]: https://fractalbrain-ai.github.io/10d-game/
[manuscript]: crl_desiderata.tex
[bibliography]: crl_desiderata.bib
[figures]: figures/
[editing]: AGENTS.md
[latexmk-config]: .latexmkrc
[makefile]: Makefile
[paper-pdf]: https://fractalbrain-ai.github.io/10d-paper/crl_desiderata.pdf
