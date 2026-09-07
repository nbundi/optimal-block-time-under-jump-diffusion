# Build the MARBLE 2026 talk.
#
#   make          build talk.pdf (regenerating the figures first)
#   make figures  regenerate the matplotlib figures only
#   make clean    remove LaTeX build intermediates
#   make distclean also remove talk.pdf and the generated figures
#
# Uses latexmk when available and falls back to two pdflatex passes; the title
# page positions its parts with TikZ 'remember picture', which needs a second.

DECK    := talk
FIGS    := fig_rate_vs_dt.pdf fig_discounts.pdf fig_welfare.pdf
LATEXMK := $(shell command -v latexmk 2>/dev/null)
LFLAGS  := -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all figures clean distclean

all: $(DECK).pdf

$(DECK).pdf: $(DECK).tex presentation-info.tex zhaw-theme.sty $(FIGS)
ifdef LATEXMK
	@$(LATEXMK) $(LFLAGS) $(DECK).tex
else
	@pdflatex -interaction=nonstopmode -halt-on-error -file-line-error $(DECK).tex
	@pdflatex -interaction=nonstopmode -halt-on-error -file-line-error $(DECK).tex
endif

figures: $(FIGS)

$(FIGS): figures.py ../code.py
	@python3 figures.py

clean:
	@rm -f *.aux *.log *.out *.nav *.snm *.toc *.vrb *.fls *.fdb_latexmk
	@echo "cleaned LaTeX build intermediates"

distclean: clean
	@rm -f $(DECK).pdf $(FIGS)
	@echo "removed the deck and the generated figures"
