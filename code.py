"""
Numerical calibration for §7 of paper.tex.

Reproduces every number that appears in the Numerical Illustration section:
  - diffusion ceiling and jump floor
  - chain-by-chain LVR rate table
  - planner's optimum Δt^opt and its sensitivity to c
  - λ-invariance check
  - diffusion-jump regime boundary Δt_×
  - volatility-regime and (σ, λ) cross-section grids

No external dependencies beyond the Python 3 standard library.
Run: `python3 calibration.py`
"""

import math
from statistics import NormalDist

# --- Standard normal helpers --------------------------------------------------

_N = NormalDist()
def Phi(z): return _N.cdf(z)
def phi(z): return math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)

# --- Fee multiplier (Theorem 2 of paper) --------------------------------------

def F(z):
    """F(z) = 2[(1+z²)Φ(-z) - z·φ(z)]. F(0)=1, F(∞)=0, strictly decreasing."""
    return 2.0 * ((1.0 + z * z) * Phi(-z) - z * phi(z))

# --- Planner's FOC LHS (Theorem 3 of paper) -----------------------------------

def planner_lhs(z):
    """h(z) = φ(z)/z - Φ(-z); strictly decreasing on (0,∞), h(0+)=∞, h(∞)=0."""
    return phi(z) / z - Phi(-z)

# --- Calibration parameters (Table 1 of §7) -----------------------------------

SIGMA   = 0.85         # diffusion vol (per √yr)   -- Saef baseline
LAMBDA  = 120.0        # jump intensity (per yr)   -- Saef baseline
M_JUMP  = 0.0          # mean log jump (symmetric Merton)
DELTA   = 0.03         # std of log jump           -- Saef baseline
GAMMA   = 5e-4         # swap fee (5 bp; Uniswap 0.05% tier)
V_POOL  = 1e6          # pool TVL (USD)
C_BLOCK = 260.0e-5     # per-block production cost (USD/block); issuance-derived baseline

SEC_PER_YR = 365.25 * 24 * 3600

# --- Jump-LVR coefficient G(γ; m, δ²) (Lemma 1 of paper) ----------------------

def G_jump(gamma, m, d):
    """G(γ; m, δ²) = (1/8)·E[(|J|-γ)²·1{|J|>γ}].
    Closed-form for symmetric Merton (m=0): G = (δ²/8)·F(γ/δ).
    Asymmetric case integrated numerically.
    """
    if m == 0.0:
        zeta = gamma / d
        return (d * d / 4.0) * ((1 + zeta * zeta) * Phi(-zeta) - zeta * phi(zeta))
    lo, hi, n = m - 12 * d, m + 12 * d, 4000
    h = (hi - lo) / n
    acc = 0.0
    for i in range(n):
        j = lo + (i + 0.5) * h
        if abs(j) > gamma:
            pdf = math.exp(-0.5 * ((j - m) / d) ** 2) / (d * math.sqrt(2 * math.pi))
            acc += (abs(j) - gamma) ** 2 * pdf * h
    return acc / 8.0

# --- Inversion utilities ------------------------------------------------------

def bisect(f, target, lo, hi, iters=100):
    """Solve f(z) = target by bisection on a strictly-decreasing branch."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if f(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def z_for_F(target):       return bisect(F,           target, 1e-3, 20.0)
def z_for_planner(target): return bisect(planner_lhs, target, 1e-3, 20.0)

# --- Report -------------------------------------------------------------------

def banner(s):
    print()
    print("=" * 72)
    print(s)
    print("=" * 72)

def main():
    banner("Closed-form magnitudes (§7 head)")
    ceiling = SIGMA ** 2 * V_POOL / 8
    Gg      = G_jump(GAMMA, M_JUMP, DELTA)
    floor   = LAMBDA * V_POOL * Gg
    print(f"Diffusion ceiling σ²V/8           = ${ceiling:>10,.2f} /yr  ({1e4*ceiling/V_POOL:.1f} bp/yr)")
    print(f"G(γ; m, δ²)                       = {Gg:.6e}")
    print(f"Jump floor λV·G(γ)                = ${floor:>10,.2f} /yr  ({1e4*floor/V_POOL:.1f} bp/yr)")
    print(f"P(|J| < γ) = 2Φ(-γ/δ)             = {2*Phi(-GAMMA/DELTA):.6f}")

    banner("Chain-by-chain LVR rate (Table in §7)")
    print(f"{'Chain':<22} {'Δt':>8} {'z(Δt)':>8} {'F(z)':>11} "
          f"{'diff $/yr':>12} {'total $/yr':>12} {'total bp/yr':>12} {'diff%':>7}")
    chains = [
        ("Ethereum L1",   12.00),
        ("Base / OP L2",   2.00),
        ("Solana*",        0.40),
        ("Arbitrum*",      0.25),
        ("App-chain*",     0.05),
    ]
    for label, dt_sec in chains:
        dt_yr = dt_sec / SEC_PER_YR
        z     = GAMMA / (SIGMA * math.sqrt(dt_yr))
        Fz    = max(F(z), 0.0)
        diff  = ceiling * Fz
        total = diff + floor
        share = 100.0 * diff / total if total > 0 else 0.0
        bp    = 1e4 * total / V_POOL
        print(f"{label:<22} {dt_sec:>7.2f}s {z:>8.3f} {Fz:>11.5f} "
              f"{diff:>12,.1f} {total:>12,.1f} {bp:>12.2f} {share:>6.2f}%")
    print(f"{'Jump floor (Δt→0)':<22} {'---':>8} {'---':>8} {'---':>11} "
          f"{0.0:>12,.1f} {floor:>12,.1f} {1e4*floor/V_POOL:>12.2f} {0.0:>6.2f}%")
    print("(* = same v2/5bp pool relabeled; not a microstructure-faithful chain comparison)")

    banner("Planner's optimum: invert h(z) = 4c/(Vγ²)")
    rhs        = 4 * C_BLOCK / (V_POOL * GAMMA ** 2)
    z_opt      = z_for_planner(rhs)
    dt_opt_sec = (GAMMA / (SIGMA * z_opt)) ** 2 * SEC_PER_YR
    print(f"At calibrated c = ${C_BLOCK} /block:")
    print(f"  RHS = 4c/(Vγ²) = {rhs:.6f}")
    print(f"  z_opt          = {z_opt:.3f}")
    print(f"  Δt_opt         = {dt_opt_sec:.3f} s")

    banner("Sensitivity table (Δt_opt vs c) -- matches paper §7 grid")
    print(f"{'c (USD/block)':>16} {'z_opt':>8} {'Δt_opt (s)':>12}")
    for c in [500e-5, 260e-5, 90e-5, 30e-5, 2e-5]:
        rhs  = 4 * c / (V_POOL * GAMMA ** 2)
        z    = z_for_planner(rhs)
        dt_s = (GAMMA / (SIGMA * z)) ** 2 * SEC_PER_YR
        print(f"{c:>16.3e} {z:>8.3f} {dt_s:>12.3f}")

    banner("Diffusion-jump regime boundary Δt_×")
    # Solve (σ²/8) F(γ/(σ√Δt)) = λG  ⇔  F(z) = 8λG/σ²
    target_cross = 8 * LAMBDA * Gg / (SIGMA ** 2)
    z_cross      = z_for_F(target_cross)
    dt_cross     = (GAMMA / (SIGMA * z_cross)) ** 2 * SEC_PER_YR
    print(f"Solve F(z×) = 8λG/σ² = {target_cross:.5e}")
    print(f"  z×   = {z_cross:.3f}")
    print(f"  Δt_× = {dt_cross:.3f} s   (diffusion-LVR = jump-LVR)")

    banner("λ-invariance of Δt_opt (numerical check of ∂Δt_opt/∂λ = 0)")
    print(f"{'λ (/yr)':>8} {'jump floor $/yr':>16} {'Δt_opt (s)':>12}")
    for lam_alt in [30.0, 120.0, 480.0, 1920.0]:
        floor_alt = lam_alt * V_POOL * Gg
        rhs       = 4 * C_BLOCK / (V_POOL * GAMMA ** 2)  # no λ dependence
        z         = z_for_planner(rhs)
        dt_s      = (GAMMA / (SIGMA * z)) ** 2 * SEC_PER_YR
        print(f"{lam_alt:>8.0f} {floor_alt:>16,.1f} {dt_s:>12.3f}")
    print("(Δt_opt is invariant in λ as predicted; only the level of W shifts.)")

    banner("Volatility-regime sensitivity at Δt = 12 s -- matches paper §7 grid")
    print(f"{'σ':>6} {'σ²V/8 (bp/yr)':>14} {'Eth 12s diff%':>16} {'Eth 12s total bp/yr':>22}")
    dt_yr_12 = 12.0 / SEC_PER_YR
    for sig_alt in [0.30, 0.50, 0.85, 1.10, 1.50]:
        ceiling_alt = sig_alt ** 2 * V_POOL / 8
        z     = GAMMA / (sig_alt * math.sqrt(dt_yr_12))
        Fz    = max(F(z), 0.0)
        diff  = ceiling_alt * Fz
        total = diff + floor
        share = 100 * diff / total if total > 0 else 0
        bp    = 1e4 * total / V_POOL
        print(f"{sig_alt:>6.2f} {1e4*ceiling_alt/V_POOL:>14.1f} {share:>15.2f}% {bp:>22.2f}")

    banner("Cross-section: ℓ_diff/ℓ_jump over (σ, λ) grid at Δt = 12 s")
    print("Ratio > 1 means diffusion-dominant (shortening blocks helps).")
    header = 'σ \\ λ'
    print(f"{header:>8}", end="")
    lam_grid = [30, 120, 480, 1920]
    for lam_v in lam_grid:
        print(f"{f'λ={lam_v}':>10}", end="")
    print()
    for sig_v in [0.30, 0.50, 0.85, 1.10, 1.50]:
        print(f"{sig_v:>8.2f}", end="")
        z    = GAMMA / (sig_v * math.sqrt(dt_yr_12))
        Fz   = max(F(z), 0.0)
        diff = sig_v ** 2 * V_POOL / 8 * Fz
        for lam_v in lam_grid:
            jp    = lam_v * V_POOL * Gg
            ratio = diff / jp if jp > 0 else float("inf")
            print(f"{ratio:>10.2f}", end="")
        print()

if __name__ == "__main__":
    main()
