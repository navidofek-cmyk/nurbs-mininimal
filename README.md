*[English](#english) · [Čeština](#čeština)*

---

## English

# NURBS Curve — Minimal Python Implementation

Standalone Python library for NURBS and B-spline curve evaluation. Extracted and stripped down from [geomdl](https://github.com/orbingol/NURBS-Python) to a single-purpose, dependency-free module.

### Engineering Use

NURBS are the standard geometry representation in CAD systems (IGES, STEP, CATIA, SOLIDWORKS). In an engineering workflow they appear at the CFD pre-processing stage:

- **Blade and airfoil profiles** — define parametric geometry for turbomachinery and aerodynamics cases
- **Hull and duct cross-sections** — exact curve representation for pipe fittings, nozzle inlets, diffusers
- **Parametric geometry loops** — drive shape parameters programmatically for optimisation or design-of-experiments runs
- **Mesh boundary definition** — export evaluated point sets as boundary curves for meshing tools

### Methods

Implemented from *The NURBS Book* (Piegl & Tiller):

- **Cox–de Boor recursion** — basis function evaluation for B-spline and NURBS curves
- **Homogeneous coordinates** — rational weighting for exact conic sections (circles, ellipses)
- **Automatic knot vector generation** — uniform and clamped knot sequences
- **Derivative computation** — first-order tangent vectors via analytical differentiation

Supports 2D and 3D curves of arbitrary degree.

### Usage

```python
from nurbs import NURBSCurve

curve = NURBSCurve(degree=3)
curve.control_points = [
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 0.0],
    [3.0, 1.0, 0.0],
    [4.0, 0.0, 0.0],
]
curve.weights = [1.0, 1.0, 2.0, 1.0]  # optional, default 1.0 gives plain B-spline
curve.auto_knot_vector()

points  = curve.evaluate_multi(50)     # 50 points along the curve
point   = curve.evaluate(0.5)          # single point at t=0.5
tangent = curve.derivative(0.5, order=1)
```

### Install

```bash
pip install -e .
```

### Structure

```
nurbs/
├── curve.py       # NURBSCurve class
└── helpers.py     # Basis functions, knot vector utilities
examples/
tests/
```

### Reference

Piegl, L. & Tiller, W. — *The NURBS Book*, 2nd ed., Springer, 1997.

---

## Čeština

# NURBS křivka — minimální implementace v Pythonu

Samostatná Python knihovna pro výpočet NURBS a B-spline křivek. Extrahováno a zjednodušeno z projektu [geomdl](https://github.com/orbingol/NURBS-Python) na jednoúčelový modul bez externích závislostí.

### Inženýrské využití

NURBS jsou standardní reprezentací geometrie v CAD systémech (IGES, STEP, CATIA, SOLIDWORKS). V inženýrském workflow se objevují ve fázi CFD pre-processingu:

- **Profily lopatek a křídel** — parametrická definice geometrie pro turbomachinery a aerodynamické případy
- **Průřezy potrubí a kanálů** — přesná reprezentace křivek pro tvarovky, vstupní hrdla trysek, difuzory
- **Parametrické geometrické smyčky** — programové řízení parametrů tvaru pro optimalizaci nebo design-of-experiments
- **Definice hranic sítě** — export vypočtených bodů jako hraničních křivek pro meshing nástroje

### Metody

Implementováno podle *The NURBS Book* (Piegl & Tiller):

- **Cox–de Boor rekurze** — výpočet bázových funkcí pro B-spline a NURBS křivky
- **Homogenní souřadnice** — racionální váhování pro přesné kuželosečky (kružnice, elipsy)
- **Automatické generování knot vektorů** — uniformní a upnuté knot sekvence
- **Výpočet derivací** — tečné vektory prvního řádu analytickou diferenciací

Podporuje 2D a 3D křivky libovolného stupně.

### Použití

```python
from nurbs import NURBSCurve

curve = NURBSCurve(degree=3)
curve.control_points = [
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 0.0],
    [3.0, 1.0, 0.0],
    [4.0, 0.0, 0.0],
]
curve.weights = [1.0, 1.0, 2.0, 1.0]  # volitelné, výchozí 1.0 = plain B-spline
curve.auto_knot_vector()

points  = curve.evaluate_multi(50)      # 50 bodů podél křivky
point   = curve.evaluate(0.5)           # jeden bod pro t=0.5
tangent = curve.derivative(0.5, order=1)
```

### Instalace

```bash
pip install -e .
```

### Struktura

```
nurbs/
├── curve.py       # třída NURBSCurve
└── helpers.py     # bázové funkce, knot vektory
examples/
tests/
```

### Reference

Piegl, L. & Tiller, W. — *The NURBS Book*, 2. vydání, Springer, 1997.
