"""
Základní příklad použití NURBS křivky
"""

import sys
import os

# Přidat parent directory do path pro import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nurbs import NURBSCurve


def main():
    print("=" * 60)
    print("NURBS Křivka - Základní příklad")
    print("=" * 60)
    
    # Vytvořit kubickou NURBS křivku (stupeň 3)
    curve = NURBSCurve(degree=3)
    
    # Nastavit kontrolní body
    control_points = [
        [0, 0, 0],
        [1, 2, 0],
        [3, 1, 0],
        [4, 0, 0]
    ]
    curve.control_points = control_points
    
    print(f"\nKontrolní body:")
    for i, cp in enumerate(control_points):
        print(f"  P{i}: {cp}")
    
    # Nastavit váhy (2. bod má větší váhu -> křivka se k němu přitáhne)
    weights = [1.0, 1.0, 2.0, 1.0]
    curve.weights = weights
    
    print(f"\nVáhy:")
    for i, w in enumerate(weights):
        print(f"  w{i}: {w}")
    
    # Automaticky vygenerovat clamped knot vektor
    curve.auto_knot_vector(clamped=True)
    
    print(f"\nKnot vektor:")
    print(f"  {curve.knot_vector}")
    
    print(f"\nKřivka: {curve}")
    
    # Vypočítat body na křivce
    print("\n" + "-" * 60)
    print("Vyhodnocení křivky")
    print("-" * 60)
    
    num_points = 10
    points = curve.evaluate_multi(num_points)
    
    print(f"\n{num_points} bodů na křivce:")
    for i, point in enumerate(points):
        u = i / (num_points - 1)
        print(f"  u={u:.2f}: [{point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f}]")
    
    # Vypočítat derivaci (tečný vektor) v bodě u=0.5
    print("\n" + "-" * 60)
    print("Derivace")
    print("-" * 60)
    
    u = 0.5
    point = curve.evaluate(u)
    tangent = curve.derivative(u, order=1)
    
    print(f"\nV parametru u={u}:")
    print(f"  Bod: [{point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f}]")
    print(f"  Tečný vektor: [{tangent[0]:.3f}, {tangent[1]:.3f}, {tangent[2]:.3f}]")
    
    # Porovnání s B-spline (všechny váhy = 1)
    print("\n" + "=" * 60)
    print("Porovnání: NURBS vs B-spline (váhy = 1)")
    print("=" * 60)
    
    bspline = NURBSCurve(degree=3)
    bspline.control_points = control_points
    bspline.weights = [1.0, 1.0, 1.0, 1.0]  # všechny váhy = 1
    bspline.auto_knot_vector()
    
    u = 0.5
    nurbs_point = curve.evaluate(u)
    bspline_point = bspline.evaluate(u)
    
    print(f"\nV parametru u={u}:")
    print(f"  NURBS (s váhami [1, 1, 2, 1]): [{nurbs_point[0]:.3f}, {nurbs_point[1]:.3f}, {nurbs_point[2]:.3f}]")
    print(f"  B-spline (váhy [1, 1, 1, 1]): [{bspline_point[0]:.3f}, {bspline_point[1]:.3f}, {bspline_point[2]:.3f}]")
    print(f"  Rozdíl: {abs(nurbs_point[1] - bspline_point[1]):.3f} (v y-souřadnici)")
    
    print("\n" + "=" * 60)
    print("Hotovo!")
    print("=" * 60)


if __name__ == "__main__":
    main()
