CHECK_SCRIPT := sh ./check.sh
EXPERIMENT_PYTHON ?= experiments/venv/bin/python

ARXIV_ARCHIVE := build/crl_desiderata-arxiv.zip
ARXIV_SOURCES := \
    crl_desiderata.tex \
    crl_desiderata.bib \
    appendix.tex \
    figures/01_overview/overview_tikz.tex \
    figures/02_screenshot/screenshot.png \
    figures/03_table/benchmark.tex \
    figures/04_companion_traces/companion-traces.png

ARXIV_LOGS := \
    experiments/GPT6_Luna_high/seed-42.jsonl.xz \
    experiments/GPT6_Luna_high/seed-43.jsonl.xz \
    experiments/GPT6_Luna_high/seed-44.jsonl.xz \
    experiments/Qwen38_27b_8FP_xhigh/seed-42.jsonl.xz \
    experiments/Qwen38_27b_8FP_xhigh/seed-43.jsonl.xz \
    experiments/Qwen38_27b_8FP_xhigh/seed-44.jsonl.xz

ARXIV_ANCILLARY := $(ARXIV_LOGS:experiments/%=build/anc/%)

.PHONY: all pdf check companion-analysis arxiv clean

all: check

pdf:
	latexmk

check:
	$(CHECK_SCRIPT)

companion-analysis:
	$(EXPERIMENT_PYTHON) experiments/plot_runs.py

arxiv: $(ARXIV_ARCHIVE)

build/anc/%: experiments/%
	mkdir -p "$(@D)"
	cp "$<" "$@"

$(ARXIV_ARCHIVE): $(ARXIV_SOURCES) $(ARXIV_ANCILLARY) Makefile | check
	rm -f "$@.tmp.zip"
	zip -X "$@.tmp.zip" $(ARXIV_SOURCES)
	cd build && zip -X "$(abspath $@).tmp.zip" $(ARXIV_ANCILLARY:build/%=%)
	mv "$@.tmp.zip" "$@"

clean:
	latexmk -c
