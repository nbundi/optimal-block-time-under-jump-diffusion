# Conference talk — MARBLE 2026

The slide deck for *Optimal Block Time for AMM Liquidity Providers under Jump-Diffusion Prices*
at MARBLE 2026, 7th International Conference on Mathematical Research for Blockchain Economy,
Limassol, 16–18 September 2026.

## Length

**All MARBLE 2026 talks: 15–17 minutes plus 3–5 minutes of Q&A**, per the organisers.

Note that the co-located EAI BlockTEA
[on-site presentation guide](https://blocktea.eai-conferences.org/2026/on-site-presentation-guide/)
advertises a 30-minute slot covering presentation and Q&A; the organisers' 15–17 minutes is the
binding number and is what this deck is built for. That guide is still the source for the practical
details: slides in `.pptx` or PDF, brought on a USB drive or emailed to the organisers in advance.

The main deck is therefore **17 content slides**, roughly a minute each, plus a title, four section
dividers and the two closing slides. Policy and Conclusion close the talk; the Conclusion carries the
limitations in its right-hand column, so there is no separate limitations slide.

The appendix is deliberately small — two figures and nothing else: the welfare curve `W(Δt)` with its
shallow optimum, and the stationary law of the mispricing. Everything else cut along the way lives in
the paper rather than the deck.

The mispricing process is introduced as a two-slide pair — define `z`, then draw it — and the two
lemmas, Theorem 2 and Theorem 3 build on it. The step from the process to a rate (the quadratic
surrogate `Vξ²/8` and the signed residual `ρ`) is not in the deck at all: the main deck states the two
channel expressions directly and leaves their derivation to the paper.

The final section runs theory first, then numbers: a slide motivating why an optimum exists at all,
Theorem 4, the calibration (price **and** consensus cost), and the results table with `Δt^opt`.

Proposition 1's mixing condition `n* ≤ 2(1+η²)` is stated on the Theorem 2 slide rather than left
implicit, along with the fact that it is checked numerically rather than proved.

## Framing

The talk opens on two live proposals that invoke the GBM result the paper revisits, and returns to
them on the policy slide with the model's own numbers:

- [The power of faster blocks](https://research.arbitrum.io/t/the-power-of-faster-blocks/9609)
  (Ed Felten, Arbitrum Research, 31 May 2024) — "Arbitrum's 250 millisecond block time leads to 65%
  lower arbitrage loss compared to a 2 second block time", from the √Δt scaling of "LVR with fees".
  The model gives 312 → 203 bp/yr, a 35% cut.
- [EIP-7782, Reduce Block Latency](https://eips.ethereum.org/EIPS/eip-7782) (Adams, Feist, Silva,
  Harris; draft for Glamsterdam) — 12 s → 6 s, motivated in part because "more frequent blocks
  decrease LVR ... which improves the economics for liquidity providers". √Δt predicts 29%; the
  model gives 471 → 403 bp/yr, a 14% cut.

Both figures are recomputed from `../code.py`, not transcribed.

## Files

| Path | Purpose |
|---|---|
| `talk.tex` | The deck. The only file to edit for content |
| `presentation-info.tex` | Author, institute, date, footer, and the contact block on the closing slide |
| `figures.py` | Generates the three talk figures by importing `../code.py`, so the slides cannot drift from the paper. Needs numpy and matplotlib |
| `fig_rate_vs_dt.pdf` | The two channels of `ℓ₀(Δt)`, with the jump floor as a constant band (built, not in the deck) |
| `fig_discounts.pdf` | The two fee discounts — `F(κ)` collapsing against a flat `Ψ(γ/δ)` (built, not in the deck) |
| `fig_welfare.pdf` | `W(Δt) = ℓ₀(Δt) + c/Δt`, its optimum at 8.4 s and its flatness (backup slide) |
| `fig_mispricing_path.pdf` | Copied from `../arxiv/` by `make`; the paper's Figure 1, the second slide of the mispricing pair |
| `fig_stationary_law.pdf` | Copied from `../arxiv/` by `make`; the paper's Figure 2, the second backup slide |
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
