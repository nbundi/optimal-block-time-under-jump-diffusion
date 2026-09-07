# Conference talk — MARBLE 2026

The slide deck for *Optimal Block Time for AMM Liquidity Providers under Jump-Diffusion Prices*
at MARBLE 2026, 7th International Conference on Mathematical Research for Blockchain Economy,
Cyprus, 16–18 September 2026.

## Length

MARBLE 2026 is co-located with EAI BlockTEA 2026 and shares its programme and speaker
instructions. The [on-site presentation guide](https://blocktea.eai-conferences.org/2026/on-site-presentation-guide/)
gives a **30-minute slot covering presentation and Q&A**, with slides in `.pptx` or PDF, brought on
a USB drive or emailed to the organisers in advance. The
[programme](https://blocktea.eai-conferences.org/2026/program/) is consistent with that: the four
MARBLE technical sessions run 100–150 minutes each.

The deck is therefore built for **~20 minutes of talking**, leaving ~10 for questions: 21 content
slides plus a title, five section dividers and the two closing slides.

## Files

| Path | Purpose |
|---|---|
| `talk.tex` | The deck. The only file to edit for content |
| `presentation-info.tex` | Author, institute, date, footer, and the contact block on the closing slide |
| `figures.py` | Generates the three talk figures by importing `../code.py`, so the slides cannot drift from the paper. Needs numpy and matplotlib |
| `fig_rate_vs_dt.pdf` | The headline picture: the two channels of `ℓ₀(Δt)`, with the jump floor as a constant band |
| `fig_discounts.pdf` | The two fee discounts — `F(κ)` collapsing against a flat `Ψ(γ/δ)` |
| `fig_welfare.pdf` | `W(Δt) = ℓ₀(Δt) + c/Δt`, its optimum at 8.4 s and its flatness |
| `fig_mispricing_path.pdf` | Copied from `../arxiv/`; the paper's Figure 1 |
| `zhaw-theme.sty`, `zhaw_logo_*.png`, `zhaw_title_bg.jpg` | The [ZHAW beamer template](https://github.com/nbundi/zhaw-beamer-template), vendored so the folder is self-contained |

## Build

```sh
make            # regenerates the figures if code.py changed, then builds talk.pdf
make figures    # figures only
make clean      # remove LaTeX intermediates
```

`make` uses `latexmk` when it is on `PATH` and otherwise runs `pdflatex` twice — the title page
positions its parts with TikZ `remember picture`, which needs the second pass.

## Numbers

Every figure and every table in the deck is the paper's, and the figures are computed at build time
from `../code.py`. Editing a calibration constant there and rerunning `make` propagates it into the
slides. The tables in `talk.tex` are transcribed, so check them against the root `README.md` if the
calibration changes.
