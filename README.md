# Optimal Block Time under Jump-Diffusion Prices

*Optimal Block Time for AMM Liquidity Providers under Jump-Diffusion Prices* — MARBLE 2026.
This README is the single source of truth for project and submission details.

## Files

No TeX source in the repository root; each version is self-contained in its own folder.

| Path | Purpose |
|---|---|
| `arxiv/extended.tex` / `extended.pdf` | **arXiv version.** Single file: body plus Appendix A (proofs) and B (figures) inlined. `\def\EXTENDED{}` on line 1 sets the `\ifextended` switch |
| `arxiv/extended.bbl` | Bibliography. arXiv does **not** run BibTeX, and the `.bbl` basename must match the main `.tex` |
| `arxiv/llncs.cls` | Springer class. Not in TeX Live, so it must ship with the upload |
| `arxiv/fig_*.pdf` | Appendix B figures: band dynamics of `z`; stationary law with/without jumps. From `python3 code.py --figures arxiv` |
| `arxiv/references.bib` | Source for regenerating `extended.bbl`. Not uploaded |
| `arxiv/sources.zip` | **The arXiv upload:** `extended.tex`, `extended.bbl`, `llncs.cls`, both figures |
| `arxiv/abstract.txt` | Abstract as ASCII for the submission form (`\dt` expanded, markup stripped) |
| `camera-ready/sources/main.tex` / `camera-ready/main.pdf` | **LNCS conference version.** Same body with `\EXTENDED` unset, so the appendix block is skipped |
| `camera-ready/sources/{main.bbl,references.bib}` | Bibliography, per the Springer checklist |
| `camera-ready/sources.zip` | The archive uploaded to Springer |
| `camera-ready/license.pdf` | Signed Licence to Publish |
| `code.py` | The only script. Bare: every §7 number, the Prop 1 envelope, exact-floor and mixing checks, block-schedule constants. `--calibrate <csv-dir>`: re-estimates (σ, λ, m, δ). `--figures arxiv`: regenerates Appendix B |
| `companion/` | Study companion: every derivation in full |

The two `.tex` sources are independent copies sharing a body — apply prose edits to both.
`diff arxiv/extended.tex camera-ready/sources/main.tex` should show only the `\EXTENDED` line, the
title footnote, and the inlined appendix.

## Venue

**MARBLE 2026**, 7th International Conference on Mathematical Research for Blockchain Economy,
Cyprus, 2026-09-16/18. Proceedings: Springer, *Lecture Notes in Operations Research*. Submitted via
EasyChair (camera-ready deadline was 2026-08-23).

- **Format:** `\documentclass[runningheads]{llncs}`, `splncs04` bibliography style, cite keys
  `firstauthorYYYYkeyword`. Camera-ready limit ≤16 pages excluding references.
- **Author:** Nils Bundi, Zurich University of Applied Sciences, bund@zhaw.ch. Review was
  double-blind, so the anonymization rules that governed the submitted PDF are spent — the
  camera-ready carries the real identity.
- **Voice:** single-author — first-person singular "I".
- **Publisher:** [step-by-step guide](https://www.springernature.com/gp/authors/publish-a-book/step-by-step-conference-proceedings);
  the binding document is the *Springer Guidelines for Authors of Proceedings*; class docs via
  `texdoc llncsdoc`.

## Build

Each version builds inside its own folder, sharing no files (TeX Live 2026, `pdflatex`; `llncs.cls`
is vendored in `arxiv/` and otherwise expected in `TEXMFHOME`):

```sh
cd arxiv                && pdflatex extended && bibtex extended && pdflatex extended && pdflatex extended
cd camera-ready/sources && pdflatex main     && bibtex main     && pdflatex main     && pdflatex main
cd companion            && pdflatex study_companion && pdflatex study_companion && pdflatex study_companion
```

Repackage the archives after any source change:

```sh
rm -rf .zipstage && mkdir -p .zipstage
cp arxiv/extended.tex arxiv/extended.bbl arxiv/llncs.cls arxiv/fig_*.pdf .zipstage/
(cd .zipstage && zip -qr ../arxiv/sources.zip . -x '.*') && rm -rf .zipstage
cd camera-ready && rm -f sources.zip && zip -qr sources.zip sources -x '.*'
```

DOCX export (optional): `pandoc camera-ready/sources/main.tex --bibliography=camera-ready/sources/references.bib --citeproc -o main.docx`

## arXiv record

Published 2026-08-31 as **[arXiv:2608.30321](https://arxiv.org/abs/2608.30321)** (v1) — primary
`q-fin.MF`, cross-listed `math.PR` and `q-fin.TR`, MSC 91G80 / 60G51 / 91B26, under the arXiv
perpetual non-exclusive licence. Springer licence clause 4(c) forbids a Creative Commons licence
here; clause 4(d)(v) requires the expanded version to state its incremental change, which the
`\thanks{}` title footnote does.

**Outstanding.** Once the MARBLE volume is published, add the Version-of-Record sentence and DOI to
the title footnote of `arxiv/extended.tex` and upload as v2; add the journal reference and DOI to
the arXiv metadata (metadata edits need no new version). The locator on the `bundi2026ext` entry
lives in `url` — never `note`, which `splncs04` typesets into the bibliography.

**On re-upload:** no `\pdfoutput=1`; no `.aux` / `.log` / `.out` / built `.pdf` (the `.bbl` is the
required exception); the abstract field is ASCII-only. arXiv distributes the source with comments
intact — re-check `grep -n '%' arxiv/extended.tex` after any edit.

## Main results

For a CPMM under jump-diffusion prices with a **symmetric, finite-activity** jump measure ν (Merton
with m = 0 the calibrated instance), swap fee γ, and Poisson blocks of rate 1/Δt:

1. **Frictionless decomposition (Thm 1).** `LVR = σ²V/8 + (λV/2)·E[(e^{J/2}−1)²]`, both parts
   invariant in Δt and γ. Holds for arbitrary ν with `∫(e^{j/2}−1)²ν(dj) < ∞`.
2. **Persistent mispricing (Lem 1).** With a fee the pool–reference log gap `z` does **not** reset
   each block — a trade leaves it at ±γ. Stationary law: uniform on the band, exponential tails.
3. **Separated rate (Thm 2).** `ℓ(Δt) = ℓ₀(Δt) + E(Δt)`, `ℓ₀(Δt) = (σ²V/8)·F(κ) + λV·G_ν(γ)`,
   `κ = γ/(σ√Δt)`, `F(κ) = 1/(1+√2 κ)` the stationary probability a block offers a profitable trade,
   `G_ν(γ) = (1/8)E_ν[(|J|−γ)₊²] = (δ²/8)Ψ(γ/δ)` for symmetric Merton.
4. **Remainder envelope (Prop 1).** Two-sided, no order symbol, **conditional on mixing condition
   (17)** `n* ≤ C(1+η²)`, `C = 2`. Six signed terms: interaction (`|M| ≤ γ` pathwise), block clock,
   single-jump thinning, multi-jump, curvature residual (exact, closed form), stationary law. At the
   calibration `E(Δt) ∈ [−0.653, +0.849]` bp/yr at 12 s, under 0.29% of the rate across deployed
   block times.
5. **Exact jump floor (Thm 3).** `ℓ(Δt) ≥ λV·G_ν(γ) > 0` for **every** Δt, no approximation or
   remainder, for symmetric ν satisfying an aggregation hypothesis (Merton does). Proved without
   touching the stationary law, so it does not inherit Prop 1's condition, and equals
   `inf_{Δt} ℓ₀(Δt)`.
6. **Approach to the floor (Cor 1).** `ℓ₀` strictly increasing; approached only as **√Δt** —
   halving the block time removes at most 29% of the diffusion term (19.5% at 12 s).
7. **Planner's optimum (Thm 4).** `η(1+η)² = Vγ²/(8c)`, `Δt^opt = 2γ²/(σ²η²)`, closed form by
   Cardano. Exactly invariant in pool size V; invariant in (λ, m, δ) for `ℓ₀`, and for the exact
   objective up to a bracket of `[7.3, 9.9]` s (Rem 10).

Fees split LVR rather than reducing it. Block-time policy acts on the diffusion channel, split
`F(κ) : 1−F(κ)` with `F(κ) → 0`; it does not act on the jump channel, split `Ψ(γ/δ) : 1−Ψ(γ/δ)`, a
function of γ/δ alone. Fees recover only `1 − Ψ(γ/δ)` = **4.1%** of jump-LVR at the calibration and
the rest is the floor — so the lever against it is the fee tier, not the block schedule.

**Scope.** Symmetry of ν, not Gaussianity, is what the results need. Thms 1, 2, 4 and Lems 1–2 hold
for arbitrary ν; **Prop 1 and Thm 3 require symmetry**. Infinite-activity models (CGMY) satisfy
Thm 1, a compensator identity, but not §5's per-block accounting, which counts jumps in an interval.

## Calibration

`(σ, λ, m, δ)` from `python3 code.py --calibrate <csv-dir>` on **Binance ETH/USDT 5-minute klines,
January 2020 – June 2026** (2,373 days, 682,946 bars), from the public monthly archives at
`data.binance.vision` (not redistributed here):

| parameter | value | estimator |
|---|---|---|
| σ | **0.8156** | continuous part of realised variance (bipower variation) |
| λ | **283.3**/yr | Lee–Mykland jump test, α = 1%, K = 270 |
| δ | **0.0192** | detected jump sizes, corrected for their diffusive component |
| m | **0** (modelling choice) | m̂ = −0.0012 with a centred local-volatility window; the 99% interval `[−0.0026, +0.0003]` contains zero |

Remaining choices: γ = 5 bp (Uniswap 0.05% tier), V = $1M, c = $260×10⁻⁵/block (Ethereum gross
issuance, attributed pro-rata by value secured). Diffusion ceiling σ²V/8 = **832** bp/yr; jump floor
λVG = **125** bp/yr.

| Δt | ℓ (bp/yr) | diffusion share |
|---|---|---|
| 12 s (Ethereum) | 471 | 73% |
| 2 s (L2) | 312 | 60% |
| 400 ms (Solana) | 221 | 43% |
| 250 ms (Arbitrum) | 203 | 38% |
| 50 ms (app-chain) | 162 | 23% |
| Δt → 0 | **125** | 0% |

- 50/50 crossover Δt× ≈ 0.75 s; the diffusion term reaches 10% of the floor only at Δt ≈ 5.5 ms
- Planner optimum at c = $260×10⁻⁵/block: **Δt^opt ≈ 8.4 s** (W falls 539 → 533 bp/yr, under 2%)
- Reset-to-zero shortcut (Ψ(κ) instead of P_trade) understates the diffusion term by 2.7× at 12 s,
  76× at 2 s, 4×10⁷ at 400 ms

## Block schedule

Poisson arrivals follow Milionis–Moallemi–Roughgarden, who call them "an approximation that is
necessary for tractability" since modern PoS chains are deterministic. Under deterministic slots the
same shape holds with `C = −ζ(1/2)/√(2π) ≈ 0.583` (the Broadie–Glasserman–Kou continuity-correction
constant) in place of `1/√2 ≈ 0.707`, the `C/(C+κ)` fit accurate to 0.1%; randomising the slot
inflates ARB by ~21%, consistent with Nezlobin–Tassy (2025) showing ARB is minimised by the
deterministic schedule. Δt^opt moves by 5%.

## Dependencies

`code.py` needs only the standard library for every headline number. The quasi-exact stationary
validation, the true-stationary fixed-point solver (`stationary_lvr_bp`) and the deterministic-slot
solver additionally use numpy/scipy; without them those sections are skipped. `--calibrate` is
standard-library only but needs the Binance CSVs on disk. `--figures` needs numpy and matplotlib;
the generated PDFs are committed under `arxiv/`, so the LaTeX build never requires them.
