# Build the MARBLE 2026 talk.
#
#   make          build talk.pdf (regenerating the figures first)
#   make figures  regenerate the matplotlib figures only
#   make clean    remove LaTeX build intermediates
#   make distclean also remove talk.pdf and the generated figures
#
# Uses latexmk when available and falls back to two pdflatex passes; the title
# page positions its parts with TikZ 'remember picture', which needs a second.
#
# LaTeX truncates and rewrites its output in place, and needs two passes, so a
# viewer that opens talk.pdf mid-build sees a half-written file and reports it
# as damaged. Everything is therefore built inside $(BUILD) and moved into
# place with a single rename, which is atomic: talk.pdf is either the previous
# build or the new one, never a partial one.

DECK    := talk
BUILD   := .build
FIGS    := fig_cpmm.pdf fig_rate_vs_dt.pdf fig_discounts.pdf fig_welfare.pdf
# the paper's own figures, copied rather than regenerated
PFIGS   := fig_mispricing_path.pdf fig_stationary_law.pdf
LATEXMK := $(shell command -v latexmk 2>/dev/null)
LFLAGS  := -pdf -interaction=nonstopmode -halt-on-error -file-line-error
PFLAGS  := -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all figures clean distclean

all: $(DECK).pdf

$(DECK).pdf: $(DECK).tex presentation-info.tex zhaw-theme.sty $(FIGS) $(PFIGS)
	@mkdir -p $(BUILD)
ifdef LATEXMK
	@$(LATEXMK) $(LFLAGS) -outdir=$(BUILD) $(DECK).tex
else
	@pdflatex $(PFLAGS) -output-directory=$(BUILD) $(DECK).tex
	@pdflatex $(PFLAGS) -output-directory=$(BUILD) $(DECK).tex
endif
	@cp $(BUILD)/$(DECK).pdf $(DECK).pdf.tmp && mv -f $(DECK).pdf.tmp $(DECK).pdf

figures: $(FIGS) $(PFIGS)

$(FIGS): figures.py ../code.py
	@python3 figures.py

$(PFIGS): %.pdf: ../arxiv/%.pdf
	@cp $< $@

clean:
	@rm -rf $(BUILD)
	@rm -f *.aux *.log *.out *.nav *.snm *.toc *.vrb *.fls *.fdb_latexmk $(DECK).pdf.tmp
	@echo "cleaned LaTeX build intermediates"

distclean: clean
	@rm -f $(DECK).pdf $(FIGS) $(PFIGS)
	@echo "removed the deck and the generated figures"
