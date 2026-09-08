# Conference talk — MARBLE 2026

The slide deck for *Optimal Block Time for AMM Liquidity Providers under Jump-Diffusion Prices*
at MARBLE 2026, 7th International Conference on Mathematical Research for Blockchain Economy,
Cyprus, 16–18 September 2026.

## Length

**All MARBLE 2026 talks: 15–17 minutes plus 3–5 minutes of Q&A**, per the organisers.

Note that the co-located EAI BlockTEA
[on-site presentation guide](https://blocktea.eai-conferences.org/2026/on-site-presentation-guide/)
advertises a 30-minute slot covering presentation and Q&A; the organisers' 15–17 minutes is the
binding number and is what this deck is built for. That guide is still the source for the practical
details: slides in `.pptx` or PDF, brought on a USB drive or emailed to the organisers in advance.

The main deck is therefore **17 content slides**, roughly a minute each, plus a title, four section
dividers and the two closing slides. Everything cut to fit lives after `\appendix` as **backup
slides** — limitations, the two-channel plot of `ℓ₀(Δt)`, the fee-split accounting, the
two-discount figure, the (σ, λ) regime grid, the optimum's sensitivity tables, and the
reset-to-zero pitfall — so the material is one page-forward away if a question calls for it.

The mispricing process is introduced as a single three-slide sequence — define `z`, draw it, then
turn it into a rate — and everything after it (the two lemmas, Theorem 2, Theorem 3) builds on that
one expression for `ℓ(Δt)`.

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
| `fig_rate_vs_dt.pdf` | The two channels of `ℓ₀(Δt)`, with the jump floor as a constant band (backup slide) |
| `fig_discounts.pdf` | The two fee discounts — `F(κ)` collapsing against a flat `Ψ(γ/δ)` (backup slide) |
| `fig_welfare.pdf` | `W(Δt) = ℓ₀(Δt) + c/Δt`, its optimum at 8.4 s and its flatness |
| `fig_mispricing_path.pdf` | Copied from `../arxiv/`; the paper's Figure 1, the middle slide of the mispricing sequence |
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
