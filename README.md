# Optimal Block Time under Jump-Diffusion Prices

Working paper / conference submission: *Optimal Block Time for AMM Liquidity Providers under Jump-Diffusion Prices*.

This README is the single source of truth for all project and submission-venue details. Tooling and Claude instructions defer to it.

## Files

| File | Purpose |
|---|---|
| `paper.tex` / `paper.pdf` | LNCS-formatted, anonymized 16-page manuscript |
| `references.bib` | Bibliography (`splncs04` style) |
| `code.py` | Reproduces every §7 number (stdlib only; `python3 code.py`) |
| `literature/` | Cited PDFs, one per reference |
| `audits/` | Submission package, citation audit, review logs |
| `companion/` | Pedagogical study companion walking through the math step-by-step |

## Target venue & submission requirements

**Primary venue.** MARBLE 2026 — 7th International Conference on Mathematical Research for Blockchain Economy. Cyprus, 2026-09-16 to 2026-09-18.

**Deadlines (AoE).**
- Full paper: **2026-06-14, 23:59:59**
- Notification: 2026-07-31
- Camera-ready: 2026-08-23, 23:59:59

**Submission channel.** EasyChair (link on the MARBLE 2026 CFP page). Upload `paper.pdf`.

**Format.**
- Template: Springer LNCS, `\documentclass[runningheads]{llncs}`.
- Citation / bibliography style: `splncs04` (numbered LNCS style). Bib entries live in `references.bib`; cite keys follow `firstauthorYYYYkeyword`.
- Length: ≤16 pages full paper (≤8 pages short), references included. Current manuscript is 16 pages.

**Review model: double-blind.** The submitted PDF must carry no identifying information. Anonymization requirements:
- `\author{Anonymous Submission}`, `\institute{Anonymous Institution}`, email a placeholder only.
- No `\thanks{}`, no acknowledgments that reveal identity.
- No author-name tokens anywhere in the body (no "Bundi", "nbundi", "proton", no "our previous work").
- No self-citations in `references.bib`.
- `\titlerunning` / `\authorrunning` must not reveal identity.
- PDF metadata (Author, Title, Subject, Keywords) emptied — verify by binary scan before upload.

**Real author identity (camera-ready only, once accepted).** Nils Bundi, Zurich University of Applied Sciences, bund@zhaw.ch. Do **not** place this in the manuscript while the submission is anonymized.

**Writing voice.** Single-author paper — use first-person singular "I" (see `academic-writing-style.md`).

## Build

```sh
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

(TeX Live 2026 / pdflatex with `llncs` + `splncs04`. No `tectonic` needed.)

DOCX export (optional, requires pandoc):

```sh
pandoc paper.tex --bibliography=references.bib --citeproc -o paper.docx
```

## Main results

1. **LVR decomposition (Thm 1).** Under Merton jump-diffusion, the constant-product LVR rate decomposes additively into σ²V/8 (diffusion) and (λV/2)·E[(e^(J/2)−1)²] (jump).
2. **Fee + block-time formula (Thm 2).** ℓ(Δt) = (σ²V/8)·F(γ/(σ√Δt)) + λV·G(γ; m, δ²), with closed-form F and G.
3. **Jump-LVR floor (Cor 1).** lim_{Δt → 0} ℓ(Δt) = λV·G > 0. Shorter blocks cannot reduce LVR below this floor.
4. **Planner's optimum (Thm 3).** Unique Δt^opt solving φ(z)/z − Φ(−z) = 4c/(Vγ²) where z = γ/(σ√Δt); invariant in (λ, m, δ).

## Calibration headline (illustrative — see §7)

For Saef-calibrated σ=0.85, λ=120/yr, δ=3%, γ=5bp, V=$1M, m=0:
- Diffusion ceiling σ²V/8 ≈ 903 bp/yr
- Jump floor λV·G(γ) ≈ 131 bp/yr
- Ethereum L1 (12s): LVR ≈ 282 bp/yr ($28.2k/yr), 53% diffusion
- Base / OP L2 (2s): LVR ≈ 135 bp/yr, 3% diffusion
- Sub-second chains (Solana, app-chains): LVR ≈ 131 bp/yr (jump floor binding)
- Parameter-free 50/50 crossover: Δt× ≈ 10.6 s
- LP-side planner optimum at issuance-derived c = $260×10⁻⁵/block: Δt^opt ≈ 7.1 s

The (σ, λ) cross-section in §7 shows the diffusion-to-jump ratio spans four orders of magnitude — the policy reading is regime-dependent and we make no unconditional claim.

## Open follow-ups (deferred to companion / future work)

- Empirical estimation of (σ, λ, m, δ) for ETH/BTC/SOL on high-frequency CEX data
- Active-tick dynamics for concentrated-liquidity LPs (the smooth-curve result applies within a tick range per Milionis et al. Remark 1; tick-crossing jumps inflate G)
- Strategic-arbitrageur model: finite capital, latency, order-flow auctions
- Multi-component social welfare (MEV redistribution, finality, censorship, oracle freshness)
- Kou / CGMY closed forms for asymmetric or heavy-tailed jumps
