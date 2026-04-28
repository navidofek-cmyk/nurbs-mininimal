# NURBS Curve — Minimal Python Implementation

Standalone Python library for NURBS and B-spline curve evaluation. Extracted and stripped down from [geomdl](https://github.com/orbingol/NURBS-Python) to a single-purpose, dependency-free module.

---

## Engineering Use

NURBS are the standard geometry representation in CAD systems (IGES, STEP, CATIA, SOLIDWORKS). In an engineering workflow they appear at the CFD pre-processing stage:

- **Blade and airfoil profiles** — import or define parametric geometry for turbomachinery and aerodynamics cases
- **Hull and duct cross-sections** — exact curve representation for pipe fittings, nozzle inlets, diffusers
- **Parametric geometry loops** — drive shape parameters (control point positions, weights) programmatically for optimisation or design-of-experiments runs
- **Mesh boundary definition** — export evaluated point sets as boundary curves for meshing tools

This library handles the evaluation side: given a curve definition, compute points and tangents at arbitrary parameter values.

---

## Methods

Implemented from *The NURBS Book* (Piegl & Tiller):

- **Cox–de Boor recursion** — basis function evaluation for B-spline and NURBS curves
- **Homogeneous coordinates** — rational weighting for exact conic sections (circles, ellipses)
- **Automatic knot vector generation** — uniform and clamped knot sequences
- **Derivative computation** — first-order tangent vectors via analytical differentiation of basis functions

Supports 2D and 3D curves of arbitrary degree.

---

## Usage

```python
from nurbs import NURBSCurve

curve = NURBSCurve(degree=3)

curve.control_points = [
    [0.0, 0.0, 0.0],
    [1.0, 2.0, 0.0],
    [3.0, 1.0, 0.0],
    [4.0, 0.0, 0.0],
]

# Optional: non-uniform weights (default 1.0 gives plain B-spline)
curve.weights = [1.0, 1.0, 2.0, 1.0]

curve.auto_knot_vector()

# Evaluate 50 points along the curve
points = curve.evaluate_multi(50)

# Single point at parameter t=0.5
point = curve.evaluate(0.5)

# Tangent vector at t=0.5
tangent = curve.derivative(0.5, order=1)
```

---

## Install

```bash
pip install -e .
```

Or without installation:

```bash
python examples/basic_example.py
```

---

## Structure

```
nurbs/
├── curve.py       # NURBSCurve class
└── helpers.py     # Basis functions, knot vector utilities
examples/
tests/
```

---

## Reference

Piegl, L. & Tiller, W. — *The NURBS Book*, 2nd ed., Springer, 1997.
