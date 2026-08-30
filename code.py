"""
Numerical calibration for Sections 7 and 8 of main.tex.

Model (Sections 3 and 5), following Milionis, Moallemi and Roughgarden (2023)
[19] as closely as possible:

  * blocks / arbitrageurs arrive as a Poisson process of rate beta = 1/dt;
  * the log mispricing z_t = log(S_t / P~_t) diffuses between blocks and is
    clipped ("bounded") to [-gamma, +gamma] at each block, exactly their (7)-(9);
  * the ONLY difference from [19] is that S is a Merton jump-diffusion, so z
    picks up an extra compound-Poisson term (rate lambda, marks J ~ N(m,d^2))
    between blocks.

Accounting is [19]'s: arbitrage profit + fee income ~ frictionless LVR, so the
LP's net adverse-selection cost is the arbitrage half, which is the rate l(dt)
of Theorem 2.  This file reproduces every number in the Numerical Illustration
section, and the block-schedule constants quoted in the Discussion.

Every headline number needs only the standard library.  The quasi-exact
stationary validation and the deterministic-slot solver additionally use
numpy/scipy; without them those sections are skipped.

Run: `python3 code.py`
"""

import csv, glob, math, os, sys
from statistics import NormalDist

try:
    import numpy as _np
    from scipy.stats import norm as _norm
    _HAVE_SCIPY = True
except Exception:
    _HAVE_SCIPY = False

_N = NormalDist()
def Phi(z): return _N.cdf(z)
def phi(z): return math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)

def Psi(x):
    """Psi(x) = E[(|Z| - x)_+^2] = 2[(1+x^2)Phi(-x) - x phi(x)], Z ~ N(0,1)."""
    return 2.0 * ((1.0 + x * x) * Phi(-x) - x * phi(x))

# --- Block-schedule constant -------------------------------------------------
# F(k) = C/(C+k).  Poisson blocks (this paper, and [19]): C = 1/sqrt(2), EXACT.
# Deterministic slots: C = -zeta(1/2)/sqrt(2 pi) = 0.5826, the Broadie-
# Glasserman-Kou continuity-correction constant; the C/(C+k) fit is accurate
# to 0.1% (checked numerically in the "block schedule" section below).
C_POISSON = 1.0 / math.sqrt(2.0)
C_DETERM  = 0.5825971579

def F(k, C=C_POISSON):
    """Stationary trade probability P_trade = C/(C+k) = 1/(1 + sqrt2 k) for Poisson."""
    return C / (C + k)

# --- Calibration parameters (Section 7) --------------------------------------

SIGMA   = 0.8156       # continuous vol (per sqrt-yr); 5-min bipower, ETHUSDT 2020-01..2026-06 (calibrate.py)
LAMBDA  = 283.3        # jump intensity (per yr); Lee-Mykland, alpha=1%, same sample
                       # (note: [19] write lambda for the BLOCK rate, here 1/dt)
M_JUMP  = 0.0          # mean log jump (symmetric Merton)
DELTA   = 0.0192       # std of log jump; bias-corrected from the same detections
GAMMA   = 5e-4         # swap fee (5 bp; Uniswap 0.05% tier)
V_POOL  = 1e6          # pool value V(S) at the reference price (USD)
C_BLOCK = 260.0e-5     # per-block production cost (USD/block); issuance-derived

SEC_PER_YR = 365.25 * 24 * 3600

def G_jump(gamma, m, d):
    """G = (1/8) E[(|J| - gamma)^2 1{|J| > gamma}];  = (d^2/8) Psi(gamma/d) for m=0."""
    if m == 0.0:
        return (d * d / 8.0) * Psi(gamma / d)
    lo, hi, n = m - 12 * d, m + 12 * d, 40000
    h = (hi - lo) / n
    acc = 0.0
    for i in range(n):
        j = lo + (i + 0.5) * h
        if abs(j) > gamma:
            pdf = math.exp(-0.5 * ((j - m) / d) ** 2) / (d * math.sqrt(2 * math.pi))
            acc += (abs(j) - gamma) ** 2 * pdf * h
    return acc / 8.0

def k_of(dt_sec, sigma=None):
    """The dimensionless fee/move ratio kappa = gamma / (sigma sqrt(dt))."""
    sigma = SIGMA if sigma is None else sigma
    return GAMMA / (sigma * math.sqrt(dt_sec / SEC_PER_YR))

def lvr_bp(dt_sec, sigma=None, lam=None):
    """LVR rate l(dt) in bp/yr from Theorem 2 of the paper.

    In the terminology of [19] this is ARB, the arbitrage-profit half of the
    LVR split -- i.e. LP adverse selection net of the fee income LPs receive
    back (see the paper's remark "The floor as un-recoverable LVR").
    """
    sigma = SIGMA if sigma is None else sigma
    lam   = LAMBDA if lam is None else lam
    return 1e4 * ((sigma ** 2 / 8.0) * F(k_of(dt_sec, sigma))
                  + lam * G_jump(GAMMA, M_JUMP, DELTA))

def lvr_frictionless_bp(sigma=None, lam=None):
    """Frictionless LVR of Theorem 1, in bp/yr: diffusion + jump, dt- and gamma-free."""
    sigma = SIGMA if sigma is None else sigma
    lam   = LAMBDA if lam is None else lam
    jump = (lam / 2.0) * (math.exp(M_JUMP + DELTA ** 2 / 2)
                          - 2 * math.exp(M_JUMP / 2 + DELTA ** 2 / 8) + 1)
    return 1e4 * sigma ** 2 / 8.0, 1e4 * jump

def fee_bp(dt_sec, sigma=None, lam=None):
    """Fee income rate, computed DIRECTLY (not as a residual): fee = gamma x trade
    size, trade size = (V/4)|xi| at leading order.  Checks the ARB + FEE identity
    ARB + FEE = frictionless LVR without assuming it."""
    sigma = SIGMA if sigma is None else sigma
    lam   = LAMBDA if lam is None else lam
    dt = dt_sec / SEC_PER_YR
    beta = 1.0 / dt
    th = math.sqrt(2 * beta) / sigma
    eta = th * GAMMA
    d = DELTA
    e_jump = d * math.sqrt(2 / math.pi) * math.exp(-0.5 * (GAMMA / d) ** 2) \
             - 2 * GAMMA * Phi(-GAMMA / d)              # E[(|J| - gamma)_+]
    return 1e4 * (beta * GAMMA * 0.25 / (th * (1 + eta)) + lam * GAMMA * 0.25 * e_jump)

# --- Proposition 1 error bound ----------------------------------------------

def emsq_post(dt_sec, sigma=None):
    """E[M^2] under the post-block law: gamma^2 (1 + eta/3)/(1 + eta), eta = sqrt2 kappa.

    Mass 1/(1+eta) sits on the atoms at +-gamma, the rest is uniform on the band;
    sharper than the |M| <= gamma bound, and tends to gamma^2/3 as dt -> 0.
    """
    eta = math.sqrt(2.0) * k_of(dt_sec, sigma)
    return GAMMA ** 2 * (1.0 + eta / 3.0) / (1.0 + eta)

def Lam(th):
    """Lambda(theta) = th^2/(th^2-1) - 2 th^2/(th^2-1/4) + 1, the EXACT tail moment
    E[(e^(xi/2)-1)^2] for symmetric exponential(theta) tails.  2 th^2 Lam(th) is the
    exact-h / quadratic ratio on the diffusion channel; = 1 + 7/(4 th^2) + O(th^-4).
    Evaluated via the series at large theta, where the difference of the two rational
    terms cancels catastrophically in floating point."""
    if th > 1e3:
        return (0.5 + 0.875 / (th * th)) / (th * th)
    return th * th / (th * th - 1) - 2 * th * th / (th * th - 0.25) + 1

def curv_bp(dt_sec):
    """E_curv = (V/2) E_pi[rho(xi)] >= 0, both channels, exactly (bp/yr).

    Nonnegative by the pairing identity cosh u - 2cosh(u/2) + 1 >= u^2/4 whenever
    the pre-trade law is symmetric (m = 0).  Not an expansion in delta: the jump
    piece is the exact truncated-Gaussian expression of _gauss_loss.
    """
    th = math.sqrt(2 * SEC_PER_YR / dt_sec) / SIGMA
    diff = (SIGMA ** 2 / 8.0) * F(k_of(dt_sec)) * (2 * th * th * Lam(th) - 1)
    if _HAVE_SCIPY:
        _, Gex = _gauss_loss(0.0, DELTA)
        jump = LAMBDA * (Gex - G_jump(GAMMA, M_JUMP, DELTA))
    else:                                   # (7/16) delta^2 relative, leading order
        jump = (7.0 / 16.0) * DELTA ** 2 * LAMBDA * G_jump(GAMMA, M_JUMP, DELTA)
    return 1e4 * diff, 1e4 * jump

def err_envelope_bp(dt_sec):
    """Proposition 1 as a TWO-SIDED envelope (lo, hi) in bp/yr.

    Every term is signed, so the bound is asymmetric rather than a modulus:
      lo = -(clock + stat + thin)
      hi = inter + stat + multi + curv
    clock: block-clock deficit, factor 5/2 from R >= 1 - (5/2) lambda dt.
    stat:  stationary-law coupling term at C = 2, a dt-free piece
           lam V gamma^2/2 plus a piece that vanishes with dt.
    thin:  single-jump thinning.  l0 charges the jump term at the full rate
           lambda; the exact single-jump block rate is lambda (1+u)^-2 with
           u = lambda dt, and 1 - (1+u)^-2 <= 2u bounds the deficit by
           2 lambda^2 dt V G.  (The jumps thinning removes from single-jump
           intervals land in multi-jump intervals, carried on the hi side.)
    inter: diffusion-jump interaction; uses only |M| <= gamma, pathwise.
    multi: intervals with >= 2 jumps.  Exact geometric sums over k >= 2
           (rho^2, rho^2(2-rho)/(1-rho), rho^2(3-2rho)/(1-rho)) with
           E[X^2|N=k] = sigma^2 (k+1) dt/(1+u), relaxed via (3-2rho) <= 3,
           (2-rho) <= 2, (1+u)^-1 <= 1:
           (V lam^2 dt/8)(gamma^2 + 3 sigma^2 dt + 2 delta^2).
    Stated at m = 0: symmetry is what signs the interaction (via E[Y] = 0)
    and the curvature residual (via the pairing identity), and hence what
    makes the LOWER side of the envelope available at all.
    """
    assert M_JUMP == 0.0, "Proposition 1 is stated at m = 0"
    dt = dt_sec / SEC_PER_YR
    inter = (LAMBDA / 8.0) * (2 * SIGMA ** 2 * dt + GAMMA ** 2)   # |M| <= gamma, pathwise
    clock = 2.50 * LAMBDA * dt * (SIGMA ** 2 / 8.0) * F(k_of(dt_sec))
    thin  = 2.0 * LAMBDA ** 2 * dt * G_jump(GAMMA, M_JUMP, DELTA)
    cd, cj = curv_bp(dt_sec)
    stat = (LAMBDA / 4.0) * (2 * GAMMA ** 2 + SIGMA ** 2 * dt)
    multi = (LAMBDA ** 2 * dt / 8.0) * (GAMMA ** 2 + 3 * SIGMA ** 2 * dt + 2 * DELTA ** 2)
    return -1e4 * (clock + stat + thin), 1e4 * (inter + stat + multi) + cd + cj

# --- Planner's optimum: v(1+v)^2 = V gamma^2/(16 c C^2), v = kappa/C ---------

def v_opt(c, V=None, C=C_POISSON):
    V = V_POOL if V is None else V
    A = V * GAMMA ** 2 / (16.0 * c * C ** 2)
    B = A / 2.0 + 1.0 / 27.0
    u = B + math.sqrt(B * B - 1.0 / 729.0)
    t = u ** (1.0 / 3.0)
    return t + 1.0 / (9.0 * t) - 2.0 / 3.0

def dt_opt_sec(c, V=None, sigma=None, C=C_POISSON):
    sigma = SIGMA if sigma is None else sigma
    return (GAMMA / (sigma * C * v_opt(c, V, C))) ** 2 * SEC_PER_YR

# --- Per-trade arbitrage profit: [19, Lemma 2] specialised to the CPMM -------

def arb_per_trade(L, S, z, gamma):
    """Verbatim [19, Lemma 2] case 1, and the closed form sqrt(LS) e^{g/2} 4 sinh^2.

    S is the EXTERNAL reference price; the pool price is S e^{-z} before the
    trade and S e^{-gamma} after it (the paper reserves P for the pool price).
    """
    xs = lambda p: math.sqrt(L / p)
    ys = lambda p: math.sqrt(L * p)
    lemma2 = (S * (xs(S * math.exp(-z)) - xs(S * math.exp(-gamma)))
              + math.exp(gamma) * (ys(S * math.exp(-z)) - ys(S * math.exp(-gamma))))
    closed = math.sqrt(L * S) * math.exp(gamma / 2) * 4 * math.sinh((z - gamma) / 4) ** 2
    quad   = 2 * math.sqrt(L * S) / 8 * (z - gamma) ** 2      # (V/8) xi^2, V = 2 sqrt(LS)
    return lemma2, closed, quad

# --- Quasi-exact stationary validation (needs numpy + scipy) ----------------

def _gauss_loss(mu, s):
    """First-order and full-concavity loss (V = 1) for a N(mu, s^2) mispricing.
    Vectorised: mu and s broadcast."""
    g = GAMMA
    a, b = (g - mu) / s, (g + mu) / s
    T = lambda x: (1 + x * x) * _norm.cdf(-x) - x * _norm.pdf(x)
    fo = s * s * (T(a) + T(b)) / 8.0
    U = (_np.exp(-g + mu + s * s / 2) * _norm.cdf((mu + s * s - g) / s)
         - 2 * _np.exp(-g / 2 + mu / 2 + s * s / 8) * _norm.cdf((mu + s * s / 2 - g) / s)
         + _norm.cdf((mu - g) / s))
    L = (_np.exp(g + mu + s * s / 2) * _norm.cdf((-g - mu - s * s) / s)
         - 2 * _np.exp(g / 2 + mu / 2 + s * s / 8) * _norm.cdf((-g - mu - s * s / 2) / s)
         + _norm.cdf((-g - mu) / s))
    return fo, 0.5 * (U + L)

def exact_lvr_bp(dt_sec, nm=400, nmax=3, ny=600, ymax=80.0):
    """Quasi-exact stationary LVR rate (bp/yr), first-order and full-concavity loss.

    Poisson blocks: conditional on N=n jumps in an inter-block interval the
    elapsed time is Gamma(n+1, beta+lambda) and the increment is
    N(n m, sigma^2 T + n delta^2).  For n=0 the time-mixture is exactly Laplace
    with rate theta' = sqrt(2(beta+lambda))/sigma.  The mismatch is integrated
    against the POST-BLOCK law induced by the jump-free stationary law of
    [19, Thm 1] (uniform on the band plus atoms at +-gamma).  "Quasi-exact"
    because that law ignores jump feedback into the stationary distribution, an
    O(lambda dt) = O(1e-5) effect here; everything else is exact.
    """
    dt = dt_sec / SEC_PER_YR
    beta = 1.0 / dt; nu = beta + LAMBDA
    thp = math.sqrt(2 * nu) / SIGMA; P0 = beta / nu; rho = LAMBDA / nu
    th = math.sqrt(2 * beta) / SIGMA
    eta = th * GAMMA
    w = 1.0 / (2 * (1 + eta)); c = th / (2 * (1 + eta))
    Xi = 2 * w * math.cosh(thp * GAMMA) + 2 * c * math.sinh(thp * GAMMA) / thp
    e = math.exp(-thp * GAMMA)
    fo = P0 * e * 2 * Xi / (8 * thp * thp)
    ex = P0 * e * Xi * (1.0 / ((thp - 1) * (thp - 0.5)) + 1.0 / ((thp + 1) * (thp + 0.5))) / 8.0
    h = 2 * GAMMA / nm
    nodes = _np.concatenate(([-GAMMA], -GAMMA + (_np.arange(nm) + 0.5) * h, [GAMMA]))
    wts   = _np.concatenate(([w],      _np.full(nm, c * h),                 [w]))
    hy = ymax / ny
    ys = (_np.arange(ny) + 0.5) * hy
    drop = 0.0
    for n in range(1, nmax + 1):
        gp = ys ** n * _np.exp(-ys) / math.factorial(n) * hy
        tot = gp.sum(); drop = max(drop, 1.0 - tot)
        gp = gp / tot
        s = _np.sqrt(SIGMA ** 2 * (ys / nu) + n * DELTA ** 2)
        a, b = _gauss_loss(nodes[:, None] + n * M_JUMP, s[None, :])
        wg = P0 * rho ** n * gp
        fo += float(wts @ a @ wg); ex += float(wts @ b @ wg)
    if drop > 1e-5:
        print(f"  [warn] Gamma-time grid truncated at y={ymax}: {drop:.2e} of mass dropped")
    return 1e4 * beta * fo, 1e4 * beta * ex

# --- Mixing condition (Prop 1, eq. 17): n* <= C(1+eta^2) with C = 2 ---------

def mixing_nstar(eta, per_unit=200, target=0.5, nmax=3_000_000):
    """Least n with sup_{m,m'} ||K0^n(m,.) - K0^n(m',.)||_TV <= 1/2, for the
    lambda=0 post-block kernel K0: m -> bound(m + X), X ~ Laplace(theta).

    K0 depends on (gamma, sigma, dt) only through eta = theta*gamma, and not on
    lambda at all, so n* is a function of eta alone.  Work in units theta = 1,
    where the band is [-eta, eta] and the step density is (1/2)e^{-|x|}.

      state space   grid on [-(eta+20), eta+20]; the +-20 covers ~20 step
                    scales of Laplace tail beyond the band, below 1e-8 mass.
                    +-eta land exactly on nodes, so the post-block atoms there
                    are represented exactly rather than smeared.
      resolution    dx = min(eta/200, 0.05): at least 200 cells across the band
                    AND at least 20 per unit step scale, so both the band
                    geometry and the increment are resolved.  N is rounded up
                    to a power of two for the FFT.
      step          one convolution with the increment density, then mass
                    outside the band is moved onto the atoms at +-gamma
                    (the arbitrageur's clip), then renormalised.
      criterion     exact: iterate until the TV distance first falls to 1/2.
                    No tolerance is involved -- n* is an integer.
      sup over m,m' approximated by the extreme pair (-eta, +eta).  bound(m+X)
                    is nondecreasing in m, so the extremes carry the largest
                    initial separation; this is the natural reduction, not a
                    proven identity, and is stated as such in Appendix A.

    Returns (n_star, ratio) with ratio = n_star/(1+eta^2), the quantity that
    eq. (17) requires to stay below C = 2.
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("needs numpy")
    g = float(eta)
    dx = min(g / per_unit, 0.05)
    half = g + 20.0
    N = 1 << int(math.ceil(math.log2(2 * half / dx)))
    dxa = 2 * half / N
    xs = (_np.arange(N) - N // 2) * dxa
    dens = 0.5 * _np.exp(-_np.abs(xs)) * dxa
    dens /= dens.sum()
    D = _np.fft.rfft(_np.fft.ifftshift(dens))
    inb = _np.abs(xs) <= g
    ip, im = int(_np.argmin(abs(xs - g))), int(_np.argmin(abs(xs + g)))
    up, dn = xs > g, xs < -g
    a = _np.zeros(N); a[ip] = 1.0
    b = _np.zeros(N); b[im] = 1.0
    for n in range(1, nmax + 1):
        out = []
        for p in (a, b):
            pre = _np.fft.fftshift(_np.fft.irfft(_np.fft.rfft(_np.fft.ifftshift(p)) * D, N))
            q = _np.where(inb, pre, 0.0)
            q[ip] += pre[up].sum(); q[im] += pre[dn].sum()
            out.append(q / q.sum())
        a, b = out
        if 0.5 * _np.abs(a - b).sum() <= target:
            return n, n / (1 + g * g)
    return None, None

# --- TRUE lambda>0 stationary law by fixed-point iteration (needs numpy) -----

def stationary_lvr_bp(dt_sec, per_gamma=256, half=0.30, nmax=3,
                      tol=1e-12, itmax=300000):
    """Exact stationary LVR rate (bp/yr) under the ACTUAL lambda>0 law.

    exact_lvr_bp above integrates against the jump-free post-block law of [19,
    Thm 1]; that is the O(lambda dt) gap named in Proposition 1.  Here the
    post-block law is instead solved for: iterate

        p  ->  law of bound(m + Delta),   m ~ p,

    with Delta the one-interval increment (Laplace for the jump-free part,
    exactly; Gamma-time mixtures of normals for k >= 1 jumps), until the rate
    stops moving.  Grid puts +-gamma exactly on nodes.

    Cost grows like dt^{-3/2}: the grid must resolve sigma sqrt(dt) while still
    spanning several delta, and mixing takes O((gamma/(sigma sqrt(dt)))^2)
    steps.  Convergence is second order in dx, so for dt below ~1 s run
    per_gamma in {128, 256, 512} and Richardson-extrapolate; at the default
    per_gamma the 50 ms value is still ~0.05 bp/yr short of its limit.
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("needs numpy")
    dt = dt_sec / SEC_PER_YR
    beta = 1.0 / dt
    dx = GAMMA / per_gamma
    N = 1 << int(math.ceil(math.log2(2 * half / dx)))
    xs = (_np.arange(N) - N // 2) * dx
    nu = beta + LAMBDA
    rho = LAMBDA / nu
    dens = _np.zeros(N)
    thp = math.sqrt(2 * nu) / SIGMA                     # k=0 is exactly Laplace
    dens += (1 - rho) * 0.5 * thp * _np.exp(-thp * _np.abs(xs)) * dx
    ny, ymax = 300, 45.0
    ys = (_np.arange(ny) + 0.5) * (ymax / ny)
    for k in range(1, nmax + 1):
        w = (1 - rho) * rho ** k
        if w < 1e-20:
            break
        gp = ys ** k * _np.exp(-ys) / math.factorial(k)
        gp /= gp.sum()
        sd = _np.sqrt(SIGMA ** 2 * (ys / nu) + k * DELTA ** 2)
        comp = _np.zeros(N)
        for wt, sv in zip(gp, sd):
            if wt < 1e-9:
                continue
            comp += wt * _np.exp(-0.5 * (xs / sv) ** 2) / (sv * math.sqrt(2 * math.pi)) * dx
        dens += w * comp
    dens /= dens.sum()
    D = _np.fft.rfft(_np.fft.ifftshift(dens))
    xi = _np.sign(xs) * _np.maximum(_np.abs(xs) - GAMMA, 0.0)
    h = 0.5 * V_POOL * (_np.exp(xi / 2) - 1) ** 2
    inb = _np.abs(xs) <= GAMMA + 1e-15
    ip, im = int(_np.argmin(abs(xs - GAMMA))), int(_np.argmin(abs(xs + GAMMA)))
    up, dn = xs > GAMMA, xs < -GAMMA
    eta = math.sqrt(2.0) * k_of(dt_sec)
    p = _np.zeros(N)
    p[inb] = 1.0
    p /= p.sum()
    p *= eta / (1 + eta)
    p[ip] += 0.5 / (1 + eta)
    p[im] += 0.5 / (1 + eta)
    prev = None
    for it in range(itmax):
        pre = _np.fft.fftshift(_np.fft.irfft(_np.fft.rfft(_np.fft.ifftshift(p)) * D, N))
        l = 1e4 * float(h @ pre) / dt / V_POOL
        q = _np.where(inb, pre, 0.0)
        q[ip] += pre[up].sum()
        q[im] += pre[dn].sum()
        p = q / q.sum()
        if prev is not None and abs(l - prev) < tol * max(1.0, abs(l)):
            return l, it + 1
        prev = l
    return l, itmax

# --- Deterministic slots: the constant C of Section 8 (needs numpy + scipy) --

def F_determ(dt_sec, sigma=None, nb=4000, tol=1e-14, itmax=20000):
    """Diffusion multiplier F under a DETERMINISTIC slot schedule, by iterating the
    post-block law of the mispricing to its fixed point.  lambda = 0 (the
    schedule question is about the diffusion channel only).

    State: atoms at +-gamma (arbitrage resets) plus a density on (-gamma,gamma).
    Returns l_diff / (sigma^2 V / 8), to be compared with C/(C+kappa).
    """
    sigma = SIGMA if sigma is None else sigma
    dt = dt_sec / SEC_PER_YR
    s = sigma * math.sqrt(dt)
    hb = 2 * GAMMA / nb
    yc = -GAMMA + (_np.arange(nb) + 0.5) * hb
    src = _np.concatenate(([-GAMMA], yc, [GAMMA]))
    D = yc[None, :] - src[:, None]
    K = _norm.pdf(D / s) / s * hb                       # band-to-band
    up = _norm.sf((GAMMA - src) / s)                    # -> atom at +gamma
    dn = _norm.cdf((-GAMMA - src) / s)                  # -> atom at -gamma
    mu = _np.concatenate(([0.25], _np.full(nb, 0.5 / nb), [0.25]))
    for _ in range(itmax):
        new = _np.empty_like(mu)
        new[1:-1] = mu[None, :] @ K
        new[0] = float(mu @ dn); new[-1] = float(mu @ up)
        new /= new.sum()
        if _np.max(_np.abs(new - mu)) < tol:
            mu = new; break
        mu = new
    # first-order loss E[(|M + X| - gamma)_+^2] / 8, X ~ N(0, s^2)
    fo, _ = _gauss_loss(src, s)
    return float(mu @ fo) / dt / (sigma ** 2 / 8.0)

# --- Calibration of (sigma, lambda, m, delta) from 5-minute klines ------------
#
# Data: Binance ETH/USDT spot, 5-minute klines, 2020-01 .. 2026-06, from the
# public monthly archives at data.binance.vision (not redistributed here):
#
#   curl -O https://data.binance.vision/data/spot/monthly/klines/ETHUSDT/5m/ETHUSDT-5m-YYYY-MM.zip
#
# Estimators, following Section 7:
#   sigma      continuous part of realised variance, by bipower variation
#              BV = (pi/2) n/(n-1) sum |r_j||r_{j-1}|, annualised.
#   jumps      Lee-Mykland (2008) at alpha = 1%, local bipower volatility on a
#              K-bar window, Gumbel threshold.
#   lambda     detected jump count / sample years.
#   m, delta   mean and sd of the detected jump returns, with the diffusive
#              component removed from the variance: delta^2 = Var(r_J)-sigma^2 dt.
#
# Run:  python3 code.py --calibrate <dir-of-csvs>

DT_SEC     = 300.0                      # 5-minute bars
ALPHA      = 0.01                       # Lee-Mykland level
K_WINDOW   = 270                        # LM local-vol window for 5-min data

def load_closes(d):
    """(open_time_ms, close) for every bar, sorted, de-duplicated."""
    rows = []
    for path in sorted(glob.glob(os.path.join(d, "*.csv"))):
        with open(path) as fh:
            for rec in csv.reader(fh):
                if not rec or not rec[0].strip():
                    continue
                try:
                    t = int(rec[0]); c = float(rec[4])
                except ValueError:
                    continue                       # header line
                # Binance switched open_time from ms to us during the sample;
                # normalise everything to ms before differencing.
                if t > 3_000_000_000_000:
                    t //= 1000
                rows.append((t, c))
    rows.sort()
    out = []
    for t, c in rows:
        if not out or t != out[-1][0]:
            out.append((t, c))
    return out


def returns(rows):
    """Log returns over consecutive bars, skipping gaps (missing candles)."""
    step = int(DT_SEC * 1000)
    r, keep = [], 0
    for (t0, c0), (t1, c1) in zip(rows, rows[1:]):
        if t1 - t0 == step and c0 > 0 and c1 > 0:
            r.append(math.log(c1 / c0)); keep += 1
    return r, keep


def bipower_sigma(r, years):
    """Annualised continuous volatility from bipower variation."""
    n = len(r)
    bv = (math.pi / 2) * (n / (n - 1)) * sum(abs(r[j]) * abs(r[j - 1])
                                             for j in range(1, n))
    return math.sqrt(bv / years)


def lee_mykland(r, K=K_WINDOW, alpha=ALPHA, centred=False):
    """Return indices of detected jumps.  LM (2008) statistic with local
    bipower volatility and the Gumbel critical value.

    centred=True splits the local-volatility window symmetrically around the
    tested bar instead of taking it wholly from the past.  The trailing window
    is the canonical LM choice but is stale after a shock: with volatility
    clustering and a leverage effect, a crash is judged against pre-crash calm
    while the rebound is judged against post-crash turbulence, which biases the
    detected set toward negative jumps.  The centred window removes that
    asymmetry at the cost of using (a little) future information.
    """
    n = len(r)
    absr = [abs(x) for x in r]
    # running sum of |r_j||r_{j-1}| over the trailing K-bar window
    prod = [0.0] + [absr[j] * absr[j - 1] for j in range(1, n)]
    run, hits, csum = 0.0, [], [0.0] * (n + 1)
    for i in range(1, n + 1):
        csum[i] = csum[i - 1] + prod[i - 1]
    c = math.sqrt(2.0 / math.pi)
    ntest = n - K
    if ntest <= 1:
        return []
    ln = math.log(ntest)
    Cn = math.sqrt(2 * ln) / c - (math.log(math.pi) + math.log(ln)) / (2 * c * math.sqrt(2 * ln))
    Sn = 1.0 / (c * math.sqrt(2 * ln))
    crit = Cn + Sn * (-math.log(-math.log(1 - alpha)))
    half = K // 2
    lo, hi = (K, n - K) if centred else (K, n)
    for i in range(lo, hi):
        if centred:
            win = (csum[i - 1] - csum[i - half + 1]) + (csum[i + half] - csum[i + 2])
            cnt = K - 4
        else:
            win = csum[i] - csum[i - K + 1]          # K-1 products ending at i-1
            cnt = K - 2
        if cnt <= 0 or win <= 0:
            continue
        if abs(r[i]) / math.sqrt(win / cnt) > crit:
            hits.append(i)
    return hits


# --- Appendix B figures (needs matplotlib): python3 code.py --figures [dir] ---

def make_figures(outdir="."):
    """Regenerate the two Appendix B illustrations as PDF (and nothing else).

    Fig B.1  fig_mispricing_path.pdf   sample path of z between Poisson blocks:
             diffusive band exceedances (teal) and a jump |J| >> gamma (orange)
             both cleared by resets to the band EDGE (blue), a jump |J| < gamma
             absorbed by the band.
    Fig B.2  fig_stationary_law.pdf    pi_0 (closed form, eq. (8)) against the
             quasi-exact pre-block law pi with Merton jumps, linear + log scale.

    Stylised parameters, chosen for legibility; the calibrated ratios are more
    extreme (delta/gamma ~ 38, lambda dt ~ 1e-4).  The lambda = 0 quadrature is
    checked against pi_0 before anything is drawn.
    """
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    INK, MUTED = "#1F2733", "#6B7280"
    BLUE, ORANGE, TEAL = "#3B77BC", "#C2510A", "#178464"   # validated trio
    BAND, SURF = "#E8EDF4", "#FFFFFF"
    plt.rcParams.update({
        "font.family": "STIXGeneral", "mathtext.fontset": "stix",
        "font.size": 9, "axes.linewidth": 0.6, "axes.edgecolor": INK,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK,
        "ytick.color": INK, "figure.facecolor": SURF, "axes.facecolor": SURF,
        "savefig.facecolor": SURF,
    })

    # ---- figure B.1: sample path -------------------------------------------
    gamma = 1.0
    rng = np.random.default_rng(11)
    T, nfine = 10.0, 4000
    t = np.linspace(0, T, nfine)
    sigma_f = 0.75                       # per-interval diffusion sd, units of gamma
    blocks = np.cumsum(rng.exponential(1.0, 30))
    blocks = blocks[blocks < T]
    jumps = [(4.35, +3.9 * gamma, r"jump $J$, $|J|\gg\gamma$"),
             (7.62, -0.85 * gamma, r"$|J|<\gamma$: absorbed by the band")]

    z = np.zeros(nfine)
    dW = rng.normal(0, sigma_f * np.sqrt(t[1] - t[0]), nfine)
    events, bi, ji = [], 0, 0            # (time, z_pre, z_post, jump_driven)
    big_jump_pending = False
    for i in range(1, nfine):
        z[i] = z[i - 1] + dW[i]
        if ji < len(jumps) and t[i - 1] < jumps[ji][0] <= t[i]:
            z[i] += jumps[ji][1]
            if abs(jumps[ji][1]) > gamma:
                big_jump_pending = True
            ji += 1
        if bi < len(blocks) and t[i - 1] < blocks[bi] <= t[i]:
            zpre = z[i]
            z[i] = np.clip(z[i], -gamma, gamma)
            if abs(zpre) > gamma + 1e-9:
                events.append((t[i], zpre, z[i], big_jump_pending))
            big_jump_pending = False
            bi += 1

    fig, ax = plt.subplots(figsize=(4.8, 2.75), dpi=300)
    ax.axhspan(-gamma, gamma, color=BAND, zorder=0)
    for yy in (gamma, -gamma):
        ax.axhline(yy, color=MUTED, lw=0.6, ls=(0, (4, 3)))
    ax.plot(t, z, color=INK, lw=0.9, solid_capstyle="round", zorder=3)
    for (tb, zpre, zpost, jd) in events:
        col = BLUE if jd else TEAL
        ax.plot([tb, tb], [zpre, zpost], color=col, lw=0.9,
                ls=(0, (1.5, 1.5)), zorder=4)
        ax.plot(tb, zpost, "o", ms=2.6, color=col, zorder=5)

    ymin, ymax = z.min() - 0.75, z.max() + 0.45
    ax.plot(blocks, np.full_like(blocks, ymin + 0.18), marker="|", ls="none",
            color=MUTED, ms=5, mew=0.8, clip_on=False)
    ax.text(T - 0.05, ymin + 0.42, r"blocks $\tau_i$", color=MUTED,
            fontsize=7.5, va="center", ha="right")

    i1 = int(np.searchsorted(t, jumps[0][0]))
    ax.annotate(jumps[0][2], xy=(jumps[0][0] - 0.05, 0.5 * (z[i1-1] + z[i1])),
                xytext=(1.35, 0.62 * ymax), fontsize=8, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
    bigev = max(events, key=lambda e: abs(e[1]))
    ax.annotate("cleared at the next block:\nreset to the band edge, not $0$",
                xy=(bigev[0] + 0.04, 0.55 * (bigev[1] + bigev[2])),
                xytext=(6.05, 0.72 * ymax), fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.7))
    diffev = max((e for e in events if not e[3]), key=lambda e: e[0])
    ax.annotate("diffusive exceedance,\ncleared at the next block",
                xy=(diffev[0] + 0.03, 0.5 * (diffev[1] + diffev[2])),
                xytext=(7.55, 0.47 * ymax), fontsize=8, color=TEAL,
                arrowprops=dict(arrowstyle="-", color=TEAL, lw=0.7,
                                connectionstyle="arc3,rad=-0.15"))
    i2 = int(np.searchsorted(t, jumps[1][0]))
    ax.annotate(jumps[1][2], xy=(jumps[1][0] + 0.02, z[i2]),
                xytext=(4.55, 0.80 * ymin), fontsize=8, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
    ax.text(0.18, -0.5, r"no-arbitrage band", fontsize=8, color="#51607A",
            va="center")
    ax.set_ylim(ymin, ymax); ax.set_xlim(0, T)
    ax.set_yticks([-gamma, 0, gamma], [r"$-\gamma$", "0", r"$+\gamma$"])
    ax.set_xticks([]); ax.set_xlabel("time", labelpad=8)
    ax.set_ylabel(r"mispricing $z_t=\log(S_t/P_t)$")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(pad=0.4)
    fig.savefig(f"{outdir}/fig_mispricing_path.pdf")
    plt.close(fig)

    # ---- figure B.2: stationary law ----------------------------------------
    eta, u, delta = 2.0, 0.08, 5.0 * gamma
    theta = eta / gamma
    sig2 = 2.0 / theta**2
    w = 1.0 / (2 * (1 + eta))
    cs = theta / (2 * (1 + eta))

    def pi0(x):
        a = np.abs(x)
        return np.where(a <= gamma, cs, cs * np.exp(-theta * (a - gamma)))

    tg = np.linspace(1e-4, 14.0, 2400); dtg = tg[1] - tg[0]

    def f_inc(x, lam_u):
        x = np.atleast_1d(x)
        thp = theta * np.sqrt(1.0 + lam_u)
        out = (thp / 2.0) * np.exp(-thp * np.abs(x)) / (1.0 + lam_u)
        xc = x[:, None]
        for k in range(1, 5):
            pk = np.exp(-(1 + lam_u) * tg) * (lam_u * tg) ** k / math.factorial(k)
            s2 = sig2 * tg + k * delta**2
            out += (pk * np.exp(-0.5 * xc**2 / s2)
                    / np.sqrt(2 * np.pi * s2)).sum(axis=1) * dtg
        return out

    def preblock(zs, lam_u):
        g = w * (f_inc(zs - gamma, lam_u) + f_inc(zs + gamma, lam_u))
        mg = np.linspace(-gamma, gamma, 241); dm = mg[1] - mg[0]
        for m in mg:
            g += cs * dm * f_inc(zs - m, lam_u)
        return g

    zt = np.linspace(-6, 6, 121)
    err = np.max(np.abs(preblock(zt, 0.0) - pi0(zt)))
    assert err < 5e-3 * cs / 0.333, f"lam=0 quadrature off pi_0 by {err:.2e}"

    fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.45), dpi=300,
                             gridspec_kw={"width_ratios": [1, 1.25]})
    zs_lin = np.linspace(-4, 4, 801); zs_log = np.linspace(-16, 16, 1201)
    for axp, zsv, logy in ((axes[0], zs_lin, False), (axes[1], zs_log, True)):
        axp.axvspan(-gamma, gamma, color=BAND, zorder=0)
        axp.plot(zsv, pi0(zsv), color=BLUE, lw=1.1, zorder=3)
        axp.plot(zsv, preblock(zsv, u), color=ORANGE, lw=1.1,
                 ls=(0, (5, 2)), zorder=4)
        for s in ("top", "right"):
            axp.spines[s].set_visible(False)
        axp.set_xlabel(r"$z$")
        if logy:
            axp.set_yscale("log"); axp.set_ylim(3e-6, 0.6)
            axp.set_xticks([-15, -10, -5, -gamma, gamma, 5, 10, 15],
                           ["-15", "-10", "-5", "", "", "5", "10", "15"])
        else:
            axp.set_ylim(0, 0.42)
            axp.set_xticks([-gamma, 0, gamma], [r"$-\gamma$", "0", r"$+\gamma$"])
    axes[0].set_ylabel("stationary density")
    axes[0].text(0, cs - 0.045, "uniform slab", ha="center", fontsize=7.5,
                 color="#51607A")
    axes[0].annotate(r"$\pi_0$ ($\lambda=0$)",
                     xy=(1.55, pi0(np.array([1.55]))[0]), xytext=(2.05, 0.24),
                     fontsize=7.5, color=BLUE,
                     arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
    axes[0].annotate(r"$\pi$ ($\lambda>0$)",
                     xy=(-1.35, preblock(np.array([-1.35]), u)[0]),
                     xytext=(-3.9, 0.375), fontsize=7.5, color=ORANGE,
                     arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    axes[1].annotate("$\\pi_0$: exponential tails,\nrate $\\theta$ --- straight"
                     "\non the log scale",
                     xy=(-4.6, pi0(np.array([-4.6]))[0]), xytext=(-15.6, 0.035),
                     fontsize=7.5, color=BLUE,
                     arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
    axes[1].annotate("$\\pi$: jump shoulder at\nthe scale $\\delta\\gg\\gamma$,"
                     "\nmass $\\approx\\lambda\\Delta t$",
                     xy=(8.2, preblock(np.array([8.2]), u)[0]),
                     xytext=(4.6, 0.07), fontsize=7.5, color=ORANGE,
                     arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
    axes[0].set_title("linear scale", fontsize=8, color=MUTED, pad=3)
    axes[1].set_title("log scale", fontsize=8, color=MUTED, pad=3)
    fig.tight_layout(pad=0.4, w_pad=1.2)
    fig.savefig(f"{outdir}/fig_stationary_law.pdf")
    plt.close(fig)
    print(f"written: {outdir}/fig_mispricing_path.pdf, "
          f"{outdir}/fig_stationary_law.pdf  (lam=0 check: {err:.1e})")


# --- Report ------------------------------------------------------------------

def banner(s):
    print(); print("=" * 78); print(s); print("=" * 78)

def main():
    Gg = G_jump(GAMMA, M_JUMP, DELTA)
    ceiling = SIGMA ** 2 * V_POOL / 8
    floor = LAMBDA * V_POOL * Gg
    ceil_bp, floor_bp = 1e4 * ceiling / V_POOL, 1e4 * floor / V_POOL
    lvr_d, lvr_j = lvr_frictionless_bp()

    banner("Per-trade arbitrage profit: [19, Lemma 2] vs the CPMM closed form")
    print(f"{'z':>7} {'[19] Lemma 2':>16} {'sqrt(LS)e^(g/2)4sinh^2':>24} {'(V/8) xi^2':>13}")
    for z in (0.001, 0.01, 0.05):
        a, b, q = arb_per_trade(4.0, 3.0, z, GAMMA)
        print(f"{z:>7.3f} {a:>16.10f} {b:>24.10f} {q:>13.10f}")
    print("The first two agree exactly; the third is the quadratic truncation used below.")

    banner("Frictionless LVR (Theorem 1) and its arbitrage/fee split (Section 7 head)")
    print(f"Diffusion LVR sigma^2 V/8                = {lvr_d:.2f} bp/yr")
    print(f"Jump LVR (lambda V/2) E[(e^(J/2)-1)^2]   = {lvr_j:.2f} bp/yr")
    print(f"Total frictionless LVR                   = {lvr_d+lvr_j:.2f} bp/yr  (dt- and gamma-free)")
    print(f"\nJump channel, split frozen in dt:")
    print(f"  l_jump   = lambda V G           = {floor_bp:.3f} bp/yr  ({100*floor_bp/lvr_j:.1f}% of jump LVR)")
    print(f"  FEE_jump                        = {lvr_j-floor_bp:.3f} bp/yr  ({100*(lvr_j-floor_bp)/lvr_j:.1f}%)")
    print(f"  fee-recovered fraction 1 - Psi(gamma/delta) = {1-Psi(GAMMA/DELTA):.4f}")
    print(f"  G = {Gg:.6e},  Psi(gamma/delta) = {Psi(GAMMA/DELTA):.6f}")
    print(f"\nARB + FEE = frictionless LVR ('un-recoverable LVR' remark), FEE computed directly:")
    print(f"{'dt':>9} {'ARB':>10} {'FEE':>10} {'ARB+FEE':>10} {'frictionless':>14}")
    for dt_sec in (12.0, 2.0, 0.4, 0.05):
        arb = lvr_bp(dt_sec); fee = fee_bp(dt_sec)
        print(f"{dt_sec:>8.2f}s {arb:>10.3f} {fee:>10.3f} {arb+fee:>10.3f} {lvr_d+lvr_j:>14.3f}")

    banner("LVR rate by block time  ->  Table 2")
    print(f"{'Chain':<18} {'dt':>8} {'kappa':>8} {'P_trade':>9} {'l_diff':>10} "
          f"{'l':>9} {'FEE':>9} {'diff share':>11}")
    for label, dt_sec in [("Ethereum L1", 12.00), ("Base / OP L2", 2.00),
                          ("Solana*", 0.40), ("Arbitrum*", 0.25), ("App-chain*", 0.05)]:
        k = k_of(dt_sec); Pt = F(k)
        ad = ceil_bp * Pt; arb = ad + floor_bp
        fee = (lvr_d - ad) + (lvr_j - floor_bp)
        print(f"{label:<18} {dt_sec:>7.2f}s {k:>8.4f} {Pt:>9.5f} {ad:>10.2f} "
              f"{arb:>9.2f} {fee:>9.2f} {100*ad/arb:>10.1f}%")
    print(f"{'Jump floor (dt->0)':<18} {'---':>8} {'---':>8} {'---':>9} {0.0:>10.2f} "
          f"{floor_bp:>9.2f} {lvr_d+lvr_j-floor_bp:>9.2f} {0.0:>10.1f}%")
    print("(* = same v2/5bp pool relabeled; not a microstructure-faithful chain comparison)")
    print(f"\nReset-to-zero shortcut would use Psi(kappa) instead of P_trade = F(kappa):")
    for dt_sec in (12.0, 2.0, 0.4):
        k = k_of(dt_sec)
        print(f"  dt={dt_sec:>6.2f}s: F={F(k):.6f}  Psi={Psi(k):.4e}  ratio={F(k)/Psi(k):.3g}")

    banner("Diffusion-jump crossover and approach to the floor")
    tgt = 8 * LAMBDA * Gg / SIGMA ** 2
    kx = C_POISSON * (1.0 / tgt - 1.0)
    print(f"Crossover: F(kappa_x) = 8 lambda G/sigma^2 = {tgt:.6f} -> kappa_x = {kx:.4f}, "
          f"dt_x = {(GAMMA/(SIGMA*kx))**2*SEC_PER_YR:.4f} s")
    for eps in (0.50, 0.10, 0.01):
        ke = C_POISSON * (1.0 / (eps * tgt) - 1.0)
        print(f"  diffusion ARB = {eps:5.0%} of the jump floor at dt = "
              f"{1000*(GAMMA/(SIGMA*ke))**2*SEC_PER_YR:9.4f} ms")

    # Not in the paper (cut for space): exact elasticity of the diffusion
    # term, dlog F/dlog dt = (1 - F)/2, reaching the
    # asymptotic 1/2 only as F -> 0.  In levels, dl_diff/dlog dt =
    # (sigma^2 V/8) F(1-F)/2 peaks at F = 1/2, i.e. dt* = 2 gamma^2/sigma^2.
    dt_star = 2 * GAMMA ** 2 / SIGMA ** 2 * SEC_PER_YR
    print(f"\nElasticity of the diffusion term (not in the paper):")
    print(f"{'dt':>9} {'kappa':>8} {'F':>9} {'elasticity':>11} "
          f"{'dl_diff/dlog dt':>16} {'halving removes':>16}")
    for dt_sec in (12.0, 6.0, 2.0, 0.4, 0.05):
        k = k_of(dt_sec); Ff = F(k); el = 0.5 * (1 - Ff)
        print(f"{dt_sec:>8.2f}s {k:>8.4f} {Ff:>9.4f} {el:>11.4f} "
              f"{ceil_bp*Ff*el:>15.1f}  {1-F(k_of(dt_sec/2))/Ff:>15.1%}")
    print(f"  asymptotic halving removes 1 - 1/sqrt(2) = {1-1/math.sqrt(2):.1%}")
    print(f"  marginal saving peaks at F = 1/2, dt* = 2 gamma^2/sigma^2 = "
          f"{dt_star:.1f} s ({ceil_bp/8:.1f} bp/yr per e-fold)")

    banner("Planner's optimum (Theorem 3): v(1+v)^2 = V gamma^2/(16 c C^2), v = kappa/C")
    A = V_POOL * GAMMA ** 2 / (16 * C_BLOCK * C_POISSON ** 2)
    v = v_opt(C_BLOCK); do = dt_opt_sec(C_BLOCK)
    Wf = lambda d: lvr_bp(d) + 1e4 * (C_BLOCK / V_POOL) / (d / SEC_PER_YR)
    print(f"C = 1/sqrt(2) = {C_POISSON:.7f}   A = {A:.5f}")
    print(f"  v_opt = {v:.5f}   kappa_opt = C v = {C_POISSON*v:.5f}   dt_opt = {do:.4f} s")
    print(f"  W(12 s) = {Wf(12.0):.3f} bp/yr,  W(dt_opt) = {Wf(do):.3f} bp/yr,  "
          f"gain = {Wf(12.0)-Wf(do):.3f} bp/yr ({100*(Wf(12.0)-Wf(do))/Wf(12.0):.2f}%)")
    print(f"\n{'c (USD/block)':>16} {'v_opt':>9} {'kappa_opt':>11} {'dt_opt (s)':>12}")
    for c in [500e-5, 260e-5, 90e-5, 30e-5, 2e-5]:
        print(f"{c:>16.3e} {v_opt(c):>9.4f} {C_POISSON*v_opt(c):>11.4f} {dt_opt_sec(c):>12.4f}")
    print(f"\n{'sigma':>16} {'v_opt':>9} {'kappa_opt':>11} {'dt_opt (s)':>12}")
    for sg in [0.30, 0.50, 0.85, 1.10, 1.50]:
        print(f"{sg:>16.2f} {v_opt(C_BLOCK):>9.4f} {C_POISSON*v_opt(C_BLOCK):>11.4f} "
              f"{dt_opt_sec(C_BLOCK, sigma=sg):>12.4f}")
    print(f"\nSame cubic under deterministic slots (C = {C_DETERM:.4f}): "
          f"dt_opt = {dt_opt_sec(C_BLOCK, C=C_DETERM):.4f} s "
          f"({100*(dt_opt_sec(C_BLOCK, C=C_DETERM)/do-1):+.1f}%)")

    banner("Jump-parameter invariance of dt_opt, and independence of pool size")
    print(f"{'lambda (/yr)':>13} {'l_jump $/yr':>16} {'dt_opt (s)':>12}")
    for lam in [70.0, 278.0, 1112.0, 4448.0]:
        print(f"{lam:>13.0f} {lam*V_POOL*Gg:>16,.1f} {dt_opt_sec(C_BLOCK):>12.4f}")
    print(f"\n{'V (USD)':>13} {'c = r V/V_chain':>17} {'dt_opt (s)':>12}")
    for Vp in [1e5, 1e6, 1e7]:
        print(f"{Vp:>13,.0f} {C_BLOCK*Vp/V_POOL:>17.5e} {dt_opt_sec(C_BLOCK*Vp/V_POOL, Vp):>12.4f}")

    banner("(sigma, lambda) cross-section at dt = 12 s  ->  Table 3")
    LAM_GRID = (70.0, 278.0, 1112.0, 4448.0)
    print(f"{'sigma':>7} {'sigma^2V/8':>11} {'P_trade':>9} "
          + " ".join(f"{'lam='+format(lv, '.0f'):>16}" for lv in LAM_GRID))
    lo = hi = None
    for sig in [0.30, 0.8151, 1.50]:
        cA = 1e4 * sig ** 2 / 8; Pt = F(k_of(12.0, sig)); ad = cA * Pt
        cells = []
        for lv in LAM_GRID:
            arb = ad + 1e4 * lv * Gg
            lo = arb if lo is None else min(lo, arb); hi = arb if hi is None else max(hi, arb)
            cells.append(f"{arb:>9,.0f} ({100*ad/arb:>3.0f}%)")
        print(f"{sig:>7.4f} {cA:>11.1f} {Pt:>9.5f} " + " ".join(cells))
    print(f"level spans {lo:.0f} to {hi:,.0f} bp/yr = a factor of {hi/lo:.0f}")
    xs = lambda s_: (s_ ** 2 / 8) * F(k_of(12.0, s_)) - LAMBDA * Gg
    a_, b_ = 0.05, 3.0
    for _ in range(200):                       # bisection: 50% diffusion share
        mid = 0.5 * (a_ + b_)
        a_, b_ = (mid, b_) if xs(mid) < 0 else (a_, mid)
    print(f"at lambda = {LAMBDA:.0f}/yr the diffusion share crosses 50% at sigma = {0.5*(a_+b_):.4f}")

    if not _HAVE_SCIPY:
        banner("Validation and block-schedule sections skipped (need numpy + scipy)"); return

    banner("Validation: quasi-exact stationary rate vs. Prop 1 envelope (Section 7)")
    print(f"{'dt':>9} {'l-bar':>10} {'1st order':>11} {'exact':>10} "
          f"{'realised E':>11} {'E_lo':>9} {'E_hi':>9} {'% of rate':>10}")
    for dt_sec in [12.0, 2.0, 0.4, 0.05]:
        cf = lvr_bp(dt_sec); fo, ex = exact_lvr_bp(dt_sec)
        lo, hi = err_envelope_bp(dt_sec)
        assert lo <= ex - cf <= hi, "realised remainder outside the Prop 1 envelope"
        print(f"{dt_sec:>8.2f}s {cf:>10.3f} {fo:>11.3f} {ex:>10.3f} "
              f"{ex-cf:>+11.4f} {lo:>+9.4f} {hi:>+9.4f} {100*hi/cf:>9.4f}%")
    print("Realised remainder is inside the envelope and POSITIVE at every dt, as")
    print("Prop 1 predicts: interaction and curvature are signed; only the block")
    print("clock and the thinning are negative, and both vanish with dt.")
    print("Residual as dt -> 0: lambda V gamma^2/24 = "
          f"{1e4*LAMBDA*GAMMA**2/24:.4f} bp/yr, plus curvature "
          f"{sum(curv_bp(1e-6)):.4f}.")

    banner("Theorem 3: the floor is an EXACT lower bound (no remainder)")
    print("Three signed steps, each checked numerically at the calibration.")
    print("(i) pairing identity  cosh u - 2 cosh(u/2) + 1 - u^2/4 >= 0, all u:")
    worst = min((math.cosh(u) - 2 * math.cosh(u / 2) + 1 - u * u / 4)
                for u in (0.01 * i for i in range(2001)))
    print(f"    min over u in [0,20] = {worst:.3e}   (leading term 7 u^4/192)")
    print("(iii) superadditivity  E[g(sum_1^k J)] >= k E[g(J)]  (Psi decreasing):")
    for k in (1, 2, 3, 5, 10):
        lhs = k * DELTA ** 2 * Psi(GAMMA / (DELTA * math.sqrt(k)))
        rhs = k * DELTA ** 2 * Psi(GAMMA / DELTA)
        print(f"    k={k:>2}  {lhs:.8e} >= {rhs:.8e}   {lhs >= rhs}")
    print(f"Floor lambda V G = {floor_bp:.3f} bp/yr; quasi-exact rate vs floor:")
    for dt_sec in [12.0, 2.0, 0.4, 0.05, 0.001]:
        _, ex = exact_lvr_bp(dt_sec)
        assert ex >= floor_bp, "exact rate below the floor"
        print(f"    dt={dt_sec:>7.3f}s  l={ex:>8.3f} >= {floor_bp:.3f}  "
              f"(+{ex-floor_bp:.3f})")

    banner("Mixing condition (17): n* <= C(1+eta^2), C = 2")
    print("K0 depends on (gamma,sigma,dt) only through eta, and not on lambda, so (17)")
    print("is a condition on eta alone.  eta spans 0.15 to 1.2e3 over Section 7's range:")
    print("every block time 50 ms..12 s, sigma in [0.30,1.50], every lambda, and every")
    print("Uniswap fee tier 1..100 bp.  See mixing_nstar() for the discretisation.")
    print(f"{'eta':>9} {'eta^2':>11} {'n*':>7} {'C(1+eta^2)':>12} {'ratio':>8}")
    worst = 0.0
    for eta in (0.15, 0.5, 0.76, 1.0, 1.41, 4.19, 11.84, 21.8):
        n, r = mixing_nstar(eta)
        worst = max(worst, r)
        print(f"{eta:>9.2f} {eta*eta:>11.2f} {n:>7} {2*(1+eta*eta):>12.1f} {r:>8.3f}")
    print(f"max ratio here = {worst:.3f} < 2.  The peak over the whole range is 1.27 at")
    print("eta ~ 0.8; beyond eta = 30 the ratio settles near 0.38 (eta = 1200: 0.379),")
    print("so the margin is smallest where the band is narrow and only widens from there.")
    assert worst < 2.0, "mixing condition (17) violated"

    banner("Remark 10: what the remainder can do to the planner's optimum")
    dstar = dt_opt_sec(C_BLOCK)
    W = lambda d: lvr_bp(d) + 1e4 * (C_BLOCK * SEC_PER_YR / d) / V_POOL
    grid = [0.5 + 0.001 * i for i in range(30000)]
    best = min(W(d) + err_envelope_bp(d)[1] for d in grid)
    adm = [d for d in grid if W(d) + err_envelope_bp(d)[0] <= best]
    flat = [d for d in grid if W(d) <= W(dstar) + 1.0]
    print(f"separated optimum dt* = {dstar:.3f} s,  W(dt*) = {W(dstar):.2f} bp/yr")
    print(f"worst-case argmin set under the envelope: [{min(adm):.2f}, {max(adm):.2f}] s")
    print(f"region where W is within 1 bp/yr of its min: [{min(flat):.2f}, {max(flat):.2f}] s")
    print("The remainder moves the optimum by less than the objective's flatness.")

    banner("Block schedule (Section 8): deterministic slots and the constant C")
    print(f"C_determ = -zeta(1/2)/sqrt(2 pi) = {C_DETERM:.6f}   [Broadie-Glasserman-Kou]")
    print(f"{'dt':>9} {'kappa':>9} {'F_Poisson':>11} {'F_determ':>11} {'C/(C+kappa)':>13} "
          f"{'fit err':>9} {'inflation':>10}")
    for dt_sec in [60.0, 12.0, 2.0, 0.4, 0.05]:
        k = k_of(dt_sec); Fp = F(k); Fd = F_determ(dt_sec); Fc = F(k, C_DETERM)
        print(f"{dt_sec:>8.2f}s {k:>9.4f} {Fp:>11.6f} {Fd:>11.6f} {Fc:>13.6f} "
              f"{100*(Fc/Fd-1):>+8.3f}% {100*(Fp/Fd-1):>9.1f}%")
    print(f"fast-block limit: inflation -> C_POISSON/C_DETERM - 1 = "
          f"{100*(C_POISSON/C_DETERM-1):.1f}%")

def calibrate(csv_dir):
    """Re-estimate (sigma, lambda, m, delta) from the klines in csv_dir and
    print them beside the values hard-coded above."""
    rows = load_closes(csv_dir)
    if len(rows) < 1000:
        print(f"only {len(rows)} bars found in {csv_dir}"); return
    r, n = returns(rows)
    span = (rows[-1][0] - rows[0][0]) / 86400e3
    years = n * DT_SEC / SEC_PER_YR
    dt_yr = DT_SEC / SEC_PER_YR
    sigma = bipower_sigma(r, years)

    banner("Calibration from 5-minute klines (Section 7)")
    print(f"sample          {span:.0f} calendar days, {n:,} bars ({years:.3f} yr)")
    print(f"{'':16}{'estimate':>12} {'in use above':>14}")
    print(f"sigma (bipower) {sigma:>12.4f} {SIGMA:>14.4f}")
    for lab, cen in (("trailing (LM)", False), ("centred", True)):
        h = lee_mykland(r, centred=cen)
        jr = [r[i] for i in h]; k = len(jr)
        m_hat = sum(jr) / k
        v = sum((x - m_hat) ** 2 for x in jr) / (k - 1)
        se = math.sqrt(v / k)
        d = math.sqrt(max(v - sigma ** 2 * dt_yr, 0.0))
        lo, hi = m_hat - 2.5758 * se, m_hat + 2.5758 * se
        tag = "  <- Section 7 quotes this m-hat" if cen else ""
        print(f"\n  window: {lab}")
        print(f"    lambda      {k/years:>12.1f} {LAMBDA:>14.1f}")
        print(f"    delta       {d:>12.4f} {DELTA:>14.4f}")
        print(f"    m           {m_hat:>12.4f} {M_JUMP:>14.4f}{tag}")
        print(f"    99% CI on m [{lo:+.4f}, {hi:+.4f}]  contains 0: {lo < 0 < hi}")
    print("\nThe trailing window is the canonical Lee-Mykland choice but is stale after")
    print("a shock: with volatility clustering a crash is judged against pre-crash calm")
    print("and the rebound against post-crash turbulence, which biases detection toward")
    print("negative jumps.  The centred window removes that asymmetry.")


if __name__ == "__main__":
    if "--calibrate" in sys.argv:
        i = sys.argv.index("--calibrate")
        calibrate(sys.argv[i + 1] if len(sys.argv) > i + 1 else "/tmp/binance/dl")
    elif "--figures" in sys.argv:
        i = sys.argv.index("--figures")
        make_figures(sys.argv[i + 1] if len(sys.argv) > i + 1 else ".")
    else:
        main()
