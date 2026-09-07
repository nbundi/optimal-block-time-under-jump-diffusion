"""Talk figures for the MARBLE 2026 slide deck.

Every number comes from ../code.py, the same script that produces the paper's
tables, so the slides cannot drift from the paper.  Run from this folder:

    python3 figures.py

Writes fig_rate_vs_dt.pdf, fig_discounts.pdf and fig_welfare.pdf.
Needs numpy and matplotlib (code.py itself does not).
"""

import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import code as paper  # noqa: E402  -- ../code.py

# --- ZHAW palette (corporate design in force since 2025) --------------------
BLUE, NIGHT, SKY = "#0064A6", "#05366C", "#9ADCF6"
TEAL, RED, ORANGE, GREEN = "#00919B", "#E62154", "#FFA70E", "#00795D"
GREY = "#6E6E6E"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#444444",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "legend.frameon": False,
    "figure.dpi": 150,
})

SEC = paper.SEC_PER_YR
FLOOR = 1e4 * paper.LAMBDA * paper.G_jump(paper.GAMMA, paper.M_JUMP, paper.DELTA)
CEIL = 1e4 * paper.SIGMA ** 2 / 8.0
CHAINS = [(12.0, "Ethereum L1\n12 s"), (2.0, "L2\n2 s"),
          (0.4, "Solana\n400 ms"), (0.05, "app-chain\n50 ms")]


def _logticks(ax):
    ax.set_xscale("log")
    ax.set_xticks([0.005, 0.05, 0.4, 2, 12, 60])
    ax.set_xticklabels(["5 ms", "50 ms", "400 ms", "2 s", "12 s", "60 s"])
    ax.set_xlim(0.005, 60)


def fig_rate_vs_dt(path="fig_rate_vs_dt.pdf"):
    """The headline picture: one channel bends with the block schedule, one does not."""
    dt = np.logspace(math.log10(0.005), math.log10(60), 600)
    total = np.array([paper.lvr_bp(t) for t in dt])
    floor = np.full_like(dt, FLOOR)

    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.fill_between(dt, 0, floor, color=NIGHT, alpha=0.85, lw=0,
                    label=r"jump channel  $\lambda V G_\nu(\gamma)$  —  no $\Delta t$ in it")
    ax.fill_between(dt, floor, total, color=SKY, alpha=0.9, lw=0,
                    label=r"diffusion channel  $\frac{\sigma^2 V}{8}F(\gamma/\sigma\sqrt{\Delta t})$")
    ax.plot(dt, total, color=BLUE, lw=2.2, zorder=5)
    ax.axhline(FLOOR, color=RED, lw=1.4, ls="--", zorder=6)
    ax.text(0.0065, FLOOR - 40, f"jump floor  $\\lambda V G = {FLOOR:.0f}$ bp/yr", color="white",
            fontsize=11, fontweight="bold")

    for t, label in CHAINS:
        val = paper.lvr_bp(t)
        ax.plot([t], [val], "o", color=NIGHT, ms=6, zorder=7)
        ax.annotate(f"{label}\n{val:.0f} bp/yr", xy=(t, val), xytext=(0, 16),
                    textcoords="offset points", ha="center", fontsize=9, color=NIGHT,
                    linespacing=1.25)

    ax.set_xlabel(r"mean block time $\Delta t$   (log scale)")
    ax.set_ylabel("LVR rate  $\\ell(\\Delta t)$   (bp/yr)")
    ax.set_ylim(0, 640)
    _logticks(ax)
    ax.legend(loc="upper left", fontsize=10)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def fig_discounts(path="fig_discounts.pdf"):
    """The two fee discounts: F collapses with the schedule, Psi does not move."""
    dt = np.logspace(math.log10(0.005), math.log10(60), 600)
    Fv = np.array([paper.F(paper.k_of(t)) for t in dt])
    psi = paper.Psi(paper.GAMMA / paper.DELTA)

    fig, ax = plt.subplots(figsize=(9.6, 4.3))
    ax.plot(dt, Fv, color=BLUE, lw=2.4,
            label=r"diffusion:  $F(\kappa)=1/(1+\sqrt{2}\,\kappa)$,   $\kappa=\gamma/\sigma\sqrt{\Delta t}$")
    ax.axhline(psi, color=RED, lw=2.4,
               label=r"jumps:  $\Psi(\gamma/\delta)=0.959$   —   flat in $\Delta t$")
    ax.fill_between(dt, Fv, psi, where=(psi > Fv), color=GREY, alpha=0.07, lw=0)

    for t, _ in CHAINS:
        ax.plot([t], [paper.F(paper.k_of(t))], "o", color=NIGHT, ms=5, zorder=6)
    ax.annotate("only this channel\nresponds to block time",
                xy=(0.05, paper.F(paper.k_of(0.05))), xytext=(0.09, 0.42),
                fontsize=10, color=NIGHT, ha="left", linespacing=1.3,
                arrowprops=dict(arrowstyle="->", color=NIGHT, lw=1.1))

    ax.set_xlabel(r"mean block time $\Delta t$   (log scale)")
    ax.set_ylabel("share of the channel left to the arbitrageur")
    ax.set_ylim(0, 1.05)
    _logticks(ax)
    ax.legend(loc="upper left", fontsize=10)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


def fig_welfare(path="fig_welfare.pdf"):
    """W(dt) = l0(dt) + c/dt: a shallow optimum near 8 s."""
    dt = np.linspace(0.5, 30, 800)
    lvr = np.array([paper.lvr_bp(t) for t in dt])
    cost = np.array([1e4 * paper.C_BLOCK * (SEC / t) / paper.V_POOL for t in dt])
    W = lvr + cost
    opt = paper.dt_opt_sec(paper.C_BLOCK)
    Wopt = paper.lvr_bp(opt) + 1e4 * paper.C_BLOCK * (SEC / opt) / paper.V_POOL

    fig, ax = plt.subplots(figsize=(9.6, 4.5))
    band = dt[(W <= Wopt + 1.0)]
    ax.axvspan(band.min(), band.max(), color=SKY, alpha=0.35, lw=0)
    ax.plot(dt, lvr, color=SKY, lw=1.8, ls="--", label=r"LVR rate  $\ell_0(\Delta t)$")
    ax.plot(dt, cost, color=ORANGE, lw=1.8, ls=":", label=r"consensus cost  $c/\Delta t$")
    ax.plot(dt, W, color=BLUE, lw=2.6, label=r"objective  $W(\Delta t)=\ell_0+c/\Delta t$")

    ax.plot([opt], [Wopt], "o", color=RED, ms=8, zorder=6)
    ax.annotate(f"$\\Delta t^{{\\mathrm{{opt}}}} = {opt:.1f}$ s\n$W = {Wopt:.0f}$ bp/yr",
                xy=(opt, Wopt), xytext=(opt + 1.6, Wopt + 62), fontsize=10.5, color=RED,
                linespacing=1.3, arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    W12 = paper.lvr_bp(12.0) + 1e4 * paper.C_BLOCK * (SEC / 12.0) / paper.V_POOL
    ax.plot([12.0], [W12], "o", color=NIGHT, ms=6, zorder=6)
    ax.annotate(f"Ethereum, 12 s\n$W = {W12:.0f}$ bp/yr", xy=(12.0, W12), xytext=(14.0, W12 + 34),
                fontsize=10, color=NIGHT, linespacing=1.3,
                arrowprops=dict(arrowstyle="->", color=NIGHT, lw=1.0))
    ax.text(band.mean(), 250, f"within 1 bp/yr of the minimum\nover [{band.min():.1f}, {band.max():.1f}] s",
            ha="center", fontsize=9.5, color=NIGHT, linespacing=1.3)

    ax.set_xlabel(r"mean block time $\Delta t$   (seconds)")
    ax.set_ylabel("cost rate   (bp/yr)")
    ax.set_xlim(0.5, 30)
    ax.set_ylim(0, 780)
    ax.legend(loc="upper right", fontsize=10)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in (fig_rate_vs_dt, fig_discounts, fig_welfare):
        print("wrote", fn(os.path.join(here, fn.__name__.replace("fig_", "fig_", 1) + ".pdf")))
