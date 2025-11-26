# Jak používat NURBS Curve Minimal

## Instalace

### Možnost 1: Bez instalace (doporučeno pro vyzkoušení)
```bash
cd nurbs-curve-minimal
python examples/basic_example.py
```

### Možnost 2: Instalace balíčku
```bash
cd nurbs-curve-minimal
pip install -e .
```

Poté můžete importovat odkudkoliv:
```python
from nurbs import NURBSCurve
```

## Rychlý přehled

### Co je NURBS?

**NURBS** (Non-Uniform Rational B-Spline) je matematická reprezentace křivek a ploch
používaná v CAD, 3D modelování, počítačové grafice a animaci.

**Výhody NURBS:**
- ✅ Přesná reprezentace analytických tvarů (kruhy, elipsy, hyperboly)
- ✅ Flexibilní tvar kontrolovaný váhami
- ✅ Hladké křivky s kontrolovanou spojitostí
- ✅ Standardizovaný formát (používá Rhino, CATIA, SolidWorks, atd.)

### Základní použití

```python
from nurbs import NURBSCurve

# 1. Vytvoření křivky
curve = NURBSCurve(degree=3)  # kubická křivka

# 2. Nastavení kontrolních bodů
curve.control_points = [
    [0, 0, 0],    # první bod
    [1, 2, 0],    # druhý bod
    [3, 1, 0],    # třetí bod
    [4, 0, 0]     # čtvrtý bod
]

# 3. Nastavení vah (volitelné, výchozí jsou 1.0)
curve.weights = [1, 1, 2, 1]  # prostřední bod má větší váhu

# 4. Generování knot vektoru
curve.auto_knot_vector()  # automaticky

# 5. Vyhodnocení křivky
points = curve.evaluate_multi(50)  # 50 bodů na křivce
point = curve.evaluate(0.5)        # jeden bod v u=0.5

# 6. Derivace (tečný vektor)
tangent = curve.derivative(0.5, order=1)
```

## Příklady

### 1. Jednoduchá 2D křivka

```python
from nurbs import NURBSCurve

curve = NURBSCurve(degree=2)
curve.control_points = [[0, 0], [1, 2], [2, 0]]
curve.auto_knot_vector()

# Získat body
points = curve.evaluate_multi(20)
for p in points:
    print(f"x={p[0]:.2f}, y={p[1]:.2f}")
```

### 2. Kruh (přesná reprezentace)

```python
import math
from nurbs import NURBSCurve

# Čtvrtina kruhu
curve = NURBSCurve(degree=2)
radius = 1.0
w = math.sqrt(2) / 2  # speciální váha pro kruh

curve.control_points = [
    [radius, 0, 0],
    [radius, radius, 0],
    [0, radius, 0]
]
curve.weights = [1.0, w, 1.0]
curve.knot_vector = [0, 0, 0, 1, 1, 1]

# Vygenerovat body na kruhu
points = curve.evaluate_multi(50)
```

### 3. Vlastní knot vektor

```python
curve = NURBSCurve(degree=3)
curve.control_points = [[i, 0, 0] for i in range(6)]
curve.weights = [1, 1, 1, 1, 1, 1]

# Manuální knot vektor (musí mít délku n + p + 1 = 6 + 3 + 1 = 10)
curve.knot_vector = [0, 0, 0, 0, 0.25, 0.5, 0.75, 1, 1, 1]

points = curve.evaluate_multi(100)
```

## API Reference

### Třída NURBSCurve

#### Konstruktor
```python
NURBSCurve(degree=3)
```
- `degree`: stupeň křivky (1=lineární, 2=kvadratická, 3=kubická, atd.)

#### Properties

- `control_points` - seznam kontrolních bodů [x, y] nebo [x, y, z]
- `weights` - seznam vah pro každý kontrolní bod
- `knot_vector` - knot vektor (seznam float hodnot)
- `degree` - stupeň křivky
- `num_control_points` - počet kontrolních bodů (read-only)

#### Metody

##### `auto_knot_vector(clamped=True)`
Automaticky vygeneruje uniformní knot vektor.
- `clamped=True`: křivka prochází prvním a posledním kontrolním bodem
- `clamped=False`: křivka neprochází krajními body

##### `evaluate(u)`
Vypočítá bod na křivce pro parametr u ∈ [0, 1].
- Vrací: `[x, y, z]` nebo `[x, y]`

##### `evaluate_multi(num_points)`
Vypočítá více bodů na křivce.
- `num_points`: počet bodů k vygenerování
- Vrací: seznam bodů

##### `derivative(u, order=1)`
Vypočítá derivaci křivky v parametru u.
- `u`: parametr ∈ [0, 1]
- `order`: řád derivace (1=tečný vektor, 2=druhá derivace, atd.)
- Vrací: vektor derivace

## Matematické detaily

### Definice NURBS křivky

NURBS křivka stupně *p* je definována:

```
C(u) = Σ(i=0 to n) [N(i,p)(u) * w(i) * P(i)] / Σ(i=0 to n) [N(i,p)(u) * w(i)]
```

Kde:
- `N(i,p)(u)` jsou B-spline bázové funkce
- `w(i)` jsou váhy
- `P(i)` jsou kontrolní body
- `u` je parametr ∈ [0, 1]

### Knot vektor

Knot vektor určuje, kde a jak se bázové funkce mění:
- **Clamped**: opakované knoty na začátku/konci → křivka prochází krajními body
- **Unclamped**: uniformní knoty → křivka neprochází krajními body

Příklad clamped knot vektoru (degree=3, n=4):
```
[0, 0, 0, 0, 1, 1, 1, 1]
```

### Váhy

Váhy ovlivňují "přitažlivost" kontrolních bodů:
- `w = 1`: standardní B-spline chování
- `w > 1`: křivka se přitáhne k bodu
- `w < 1`: křivka se od bodu oddálí

## Testování

```bash
python tests/test_curve.py
```

Měli byste vidět:
```
NURBS Curve - Testy
============================================================
Test 1: Základní funkčnost... OK
Test 2: Váhy... OK
Test 3: Derivace... OK
Test 4: Kruh (přesnost)... OK (max error: 1.11e-16)
Test 5: Generování knot vektoru... OK
Test 6: 2D křivka... OK
Test 7: Interpolace koncových bodů... OK

Výsledky: 7 úspěšných, 0 neúspěšných
```

## Časté otázky

### Jak velký stupeň zvolit?

- **degree=1**: Lomená čára (lineární segmenty)
- **degree=2**: Kvadratické křivky (paraboly)
- **degree=3**: Kubické křivky (nejběžnější, hladké)
- **degree≥4**: Vyšší hladkost, více výpočetně náročné

### Kolik kontrolních bodů potřebuji?

Minimálně `degree + 1` bodů. Např. pro kubickou křivku (degree=3) potřebujete alespoň 4 body.

### Jak vytvořit uzavřenou křivku?

Nastavte první a poslední kontrolní bod na stejnou pozici a použijte periodický knot vektor.

### Proč mi křivka neprochází kontrolními body?

NURBS křivky obecně neprochází kontrolními body (kromě prvního a posledního u clamped křivek).
Kontrolní body tvoří "ovládací rám", který určuje tvar křivky.

## Reference

Implementace je založena na algoritmech z:

**"The NURBS Book" (2nd Edition)**  
Les Piegl & Wayne Tiller  
Springer, 1997  
ISBN: 978-3540615453

Konkrétní algoritmy:
- A2.1: Find Span (find_span)
- A2.2: Basis Functions (basis_functions)
- A2.3: Basis Functions Derivatives (basis_functions_ders)
- A3.1: Curve Point (evaluate)
- A4.2: Curve Derivatives (derivative)

## Porovnání s geomdl

Tento projekt je minimální extrakt z [geomdl](https://github.com/orbingol/NURBS-Python).

| Funkce | nurbs-curve-minimal | geomdl (plná verze) |
|--------|---------------------|---------------------|
| NURBS křivky | ✅ | ✅ |
| NURBS plochy | ❌ | ✅ |
| Vizualizace | ❌ | ✅ (Matplotlib, VTK, Plotly) |
| Import/Export | ❌ | ✅ (JSON, OBJ, STL, atd.) |
| Trimming | ❌ | ✅ |
| Knot insertion | ❌ | ✅ |
| Velikost | ~300 řádků | ~15,000+ řádků |
| Závislosti | 0 | několik |

**Kdy použít nurbs-curve-minimal:**
- Potřebujete jen základní NURBS křivky
- Chcete minimální závislosti
- Učíte se NURBS algoritmy
- Embedujete do jiného projektu

**Kdy použít geomdl:**
- Potřebujete NURBS plochy
- Chcete vizualizaci
- Potřebujete import/export souborů
- Pokročilé operace (trimming, lofting, atd.)
