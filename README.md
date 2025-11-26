# NURBS Curve Minimal

Minimální samostatný projekt pro práci s NURBS (Non-Uniform Rational B-Spline) křivkami.

Extrahováno z projektu [NURBS-Python (geomdl)](https://github.com/orbingol/NURBS-Python).

## Co je NURBS?

NURBS jsou racionální B-spline křivky používané v CAD, počítačové grafice a animaci. 
Umožňují přesně reprezentovat jak analytické tvary (kruhy, elipsy) tak volné křivky.

## Instalace

```bash
pip install -e .
```

Nebo jednodušše bez instalace:
```bash
cd nurbs-curve-minimal
python examples/basic_example.py
```

## Rychlý start

```python
from nurbs import NURBSCurve

# Vytvořit NURBS křivku stupně 3 (kubickou)
curve = NURBSCurve(degree=3)

# Nastavit kontrolní body
curve.control_points = [
    [0, 0, 0],
    [1, 2, 0],
    [3, 1, 0],
    [4, 0, 0]
]

# Nastavit váhy (volitelné, výchozí jsou všechny 1.0)
curve.weights = [1, 1, 2, 1]

# Automaticky vygenerovat knot vektor
curve.auto_knot_vector()

# Vypočítat body na křivce
points = curve.evaluate_multi(50)

# Vypočítat jeden bod
point = curve.evaluate(0.5)

# Vypočítat derivaci
tangent = curve.derivative(0.5, order=1)
```

## Funkce

- ✅ NURBS křivky s váhami
- ✅ B-spline křivky (NURBS s váhami = 1)
- ✅ Vyhodnocení bodů na křivce
- ✅ Výpočet derivací
- ✅ Automatické generování knot vektorů
- ✅ Podpora 2D i 3D křivek

## Struktura projektu

```
nurbs-curve-minimal/
├── nurbs/
│   ├── __init__.py      # Hlavní balíček
│   ├── curve.py         # Třída NURBSCurve
│   └── helpers.py       # Pomocné funkce (basis functions, knot vectors)
├── examples/
│   ├── basic_example.py
│   └── circle_example.py
├── tests/
│   └── test_curve.py
├── README.md
├── setup.py
└── requirements.txt
```

## Reference

Implementace je založena na algoritmech z knihy:
**"The NURBS Book"** by Les Piegl and Wayne Tiller

## Licence

MIT License (stejně jako původní geomdl projekt)

## Původní projekt

Tento projekt je minimální extrakcí z [geomdl](https://github.com/orbingol/NURBS-Python).
Pro komplexnější práci s NURBS (plochy, trimming, vizualizace) použijte plnou verzi geomdl.
