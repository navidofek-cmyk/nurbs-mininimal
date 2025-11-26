"""
Příklad: Vytvoření kruhu pomocí NURBS křivky
Kruh lze přesně reprezentovat pomocí racionálních kvadratických NURBS křivek
"""

import sys
import os
import math

# Přidat parent directory do path pro import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nurbs import NURBSCurve


def create_circle_quarter(radius=1.0):
    """
    Vytvoří čtvrtinu kruhu (0° až 90°) pomocí kvadratické NURBS křivky.
    
    :param radius: poloměr kruhu
    :return: NURBSCurve reprezentující čtvrtinu kruhu
    """
    # Kvadratická křivka (stupeň 2)
    curve = NURBSCurve(degree=2)
    
    # Kontrolní body pro čtvrtinu kruhu v XY rovině
    # P0: (r, 0)    - začátek (0°)
    # P1: (r, r)    - rohový bod
    # P2: (0, r)    - konec (90°)
    curve.control_points = [
        [radius, 0, 0],
        [radius, radius, 0],
        [0, radius, 0]
    ]
    
    # Váhy pro přesnou reprezentaci kruhu
    # Prostřední bod má váhu w = sqrt(2)/2 ≈ 0.707
    w = math.sqrt(2) / 2
    curve.weights = [1.0, w, 1.0]
    
    # Clamped knot vektor pro čtvrtinu kruhu
    curve.knot_vector = [0, 0, 0, 1, 1, 1]
    
    return curve


def create_full_circle(radius=1.0):
    """
    Vytvoří celý kruh spojením 4 čtvrtin.
    
    :param radius: poloměr kruhu
    :return: NURBSCurve reprezentující celý kruh
    """
    # Kvadratická křivka
    curve = NURBSCurve(degree=2)
    
    w = math.sqrt(2) / 2
    
    # 9 kontrolních bodů (4 čtvrtiny, poslední bod = první)
    # Rozložení po 90° krocích
    curve.control_points = [
        [radius, 0, 0],          # 0°
        [radius, radius, 0],     # rohový bod
        [0, radius, 0],          # 90°
        [-radius, radius, 0],    # rohový bod
        [-radius, 0, 0],         # 180°
        [-radius, -radius, 0],   # rohový bod
        [0, -radius, 0],         # 270°
        [radius, -radius, 0],    # rohový bod
        [radius, 0, 0],          # 360° (= 0°)
    ]
    
    # Váhy - prostřední body mají w = sqrt(2)/2
    curve.weights = [1.0, w, 1.0, w, 1.0, w, 1.0, w, 1.0]
    
    # Knot vektor pro uzavřený kruh (4 segmenty)
    curve.knot_vector = [0, 0, 0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1, 1, 1]
    
    return curve


def verify_circle(curve, radius, num_samples=20):
    """
    Ověří, že křivka je skutečně kruh vypočítáním vzdáleností od středu.
    
    :param curve: NURBS křivka
    :param radius: očekávaný poloměr
    :param num_samples: počet bodů k testování
    :return: tuple (max_error, avg_error)
    """
    points = curve.evaluate_multi(num_samples)
    errors = []
    
    for point in points:
        # Vzdálenost od středu (0, 0)
        distance = math.sqrt(point[0]**2 + point[1]**2)
        error = abs(distance - radius)
        errors.append(error)
    
    return max(errors), sum(errors) / len(errors)


def main():
    print("=" * 60)
    print("NURBS reprezentace kruhu")
    print("=" * 60)
    
    radius = 2.0
    
    # Čtvrtina kruhu
    print("\n1. Čtvrtina kruhu (0° až 90°)")
    print("-" * 60)
    
    quarter = create_circle_quarter(radius)
    print(f"Křivka: {quarter}")
    print(f"Kontrolní body:")
    for i, cp in enumerate(quarter.control_points):
        print(f"  P{i}: [{cp[0]:.3f}, {cp[1]:.3f}, {cp[2]:.3f}]")
    print(f"Váhy: {[f'{w:.3f}' for w in quarter.weights]}")
    
    # Vypočítat body na čtvrtině kruhu
    num_points = 5
    points = quarter.evaluate_multi(num_points)
    print(f"\n{num_points} bodů na čtvrtině kruhu:")
    for i, point in enumerate(points):
        angle = 90 * i / (num_points - 1)
        distance = math.sqrt(point[0]**2 + point[1]**2)
        print(f"  {angle:5.1f}°: [{point[0]:6.3f}, {point[1]:6.3f}] "
              f"(vzdálenost od středu: {distance:.4f})")
    
    # Ověření přesnosti
    max_err, avg_err = verify_circle(quarter, radius, 100)
    print(f"\nPřesnost (100 bodů):")
    print(f"  Max chyba: {max_err:.2e}")
    print(f"  Průměrná chyba: {avg_err:.2e}")
    
    # Celý kruh
    print("\n" + "=" * 60)
    print("2. Celý kruh (360°)")
    print("-" * 60)
    
    circle = create_full_circle(radius)
    print(f"Křivka: {circle}")
    print(f"Kontrolní body: {len(circle.control_points)}")
    print(f"Váhy: {[f'{w:.3f}' for w in circle.weights]}")
    
    # Vypočítat body po celém kruhu
    num_points = 12
    points = circle.evaluate_multi(num_points)
    print(f"\n{num_points} bodů po celém kruhu:")
    for i, point in enumerate(points):
        angle = 360 * i / (num_points - 1)
        distance = math.sqrt(point[0]**2 + point[1]**2)
        print(f"  {angle:6.1f}°: [{point[0]:6.3f}, {point[1]:6.3f}] "
              f"(r={distance:.4f})")
    
    # Ověření přesnosti celého kruhu
    max_err, avg_err = verify_circle(circle, radius, 100)
    print(f"\nPřesnost (100 bodů):")
    print(f"  Max chyba: {max_err:.2e}")
    print(f"  Průměrná chyba: {avg_err:.2e}")
    
    # Tečné vektory
    print("\n" + "-" * 60)
    print("Tečné vektory (derivace)")
    print("-" * 60)
    
    for angle_deg in [0, 90, 180, 270]:
        u = angle_deg / 360.0
        if u == 1.0:
            u = 0.9999  # Avoid endpoint
        
        point = circle.evaluate(u)
        tangent = circle.derivative(u, order=1)
        
        # Normalizovat tečný vektor
        length = math.sqrt(sum(t**2 for t in tangent))
        tangent_norm = [t/length for t in tangent]
        
        print(f"\n{angle_deg:3d}° (u={u:.3f}):")
        print(f"  Bod: [{point[0]:6.3f}, {point[1]:6.3f}]")
        print(f"  Tečný vektor: [{tangent_norm[0]:6.3f}, {tangent_norm[1]:6.3f}]")
    
    print("\n" + "=" * 60)
    print("NURBS může přesně reprezentovat kruhy a kužely!")
    print("=" * 60)


if __name__ == "__main__":
    main()
