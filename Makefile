CHECK_SCRIPT := sh ./check.sh
ARXIV_ARCHIVE := build/crl_desiderata-arxiv.zip
ARXIV_SOURCES := \
    crl_desiderata.tex \
    crl_desiderata.bib \
    figures/01_overview/overview_tikz.tex \
    figures/02_screenshot/screenshot.png \
    figures/03_table/benchmark.tex

.PHONY: all pdf check arxiv clean

all: check

pdf:
	latexmk

check:
	$(CHECK_SCRIPT)

arxiv: $(ARXIV_ARCHIVE)

$(ARXIV_ARCHIVE): $(ARXIV_SOURCES) Makefile | check
	rm -f $@
	zip -X $@ $(ARXIV_SOURCES)

clean:
	latexmk -c
