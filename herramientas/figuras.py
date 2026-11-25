"""Genera las figuras del libro (SVG) en figuras/.

Uso, desde la raíz del libro:   python3 herramientas/figuras.py [--png]
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
"""
import pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def lienzo(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc,
                linespacing=1.2, fontweight=peso)


def flecha(ax, a, b, color=TINTA2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))


def pagina(ax, x, y, w, h, titulo):
    caja(ax, x, y, w, h, None, fc=SUP, ec=TINTA2, r=0.06)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.35), w, 0.35, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=CAJA, ec=TINTA2, lw=1.2))
    ax.text(x + 0.15, y + h - 0.175, titulo, ha="left", va="center", fontsize=9, color=TINTA2)
    for i in range(5):
        ax.plot([x + 0.2, x + w - 0.2 - (0.5 if i % 2 else 0)], [y + h - 0.7 - i * 0.32] * 2,
                color=GRIS, lw=3, solid_capstyle="round")





def c2_barras():
    import numpy as np
    rng = np.random.default_rng(8)
    muestras = [rng.normal(6, 1, 20), np.r_[rng.normal(5.4, 0.5, 19), 17.4], np.r_[rng.normal(4, 0.5, 10), rng.normal(8, 0.5, 10)], np.array([4.5, 6.2, 7.3])]
    muestras = [m - m.mean() + 6 for m in muestras]
    nombres = ["Simétrica", "Con un atípico", "Bimodal", "n = 3"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for i, m in enumerate(muestras):
        a1.bar(i, m.mean(), color=S[i], width=.6)
        a1.errorbar(i, m.mean(), yerr=m.std(ddof=1) / np.sqrt(len(m)), color=TINTA, capsize=5, lw=1.4)
        a2.scatter(i + rng.uniform(-.15, .15, len(m)), m, color=S[i], s=22, edgecolor=SUP, lw=.5, zorder=3)
        a2.hlines(m.mean(), i - .25, i + .25, color=TINTA, lw=2)
    for a, t in ((a1, "Barras: parecen iguales"), (a2, "Puntos: son muy distintas")):
        a.set_xticks(range(4)); a.set_xticklabels(nombres, fontsize=9.5); a.set_title(t, fontsize=11, color=TINTA)
        for s_ in ("top", "right"): a.spines[s_].set_visible(False)
        a.tick_params(colors=TINTA2)
    a1.set_ylabel("Valor", fontsize=10, color=TINTA2)
    fig.text(0.5, -0.02, "Las cuatro muestras tienen la misma media (6). Datos simulados.", ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "c2_barras.svg")


if __name__ == "__main__":
    c2_barras()
