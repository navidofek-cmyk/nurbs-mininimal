"""
Jednoduché testy pro NURBS křivku
"""

import sys
import os
import math

# Přidat parent directory do path pro import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nurbs import NURBSCurve


def test_basic_curve():
    """Test základní funkčnosti"""
    print("Test 1: Základní funkčnost... ", end="")
    
    curve = NURBSCurve(degree=3)
    curve.control_points = [[0, 0, 0], [1, 1, 0], [2, -1, 0], [3, 0, 0]]
    curve.auto_knot_vector()
    
    # Test vyhodnocení
    point = curve.evaluate(0.5)
    assert len(point) == 3
    assert isinstance(point[0], float)
    
    # Test více bodů
    points = curve.evaluate_multi(10)
    assert len(points) == 10
    
    print("OK")


def test_weights():
    """Test vah"""
    print("Test 2: Váhy... ", end="")
    
    curve = NURBSCurve(degree=2)
    curve.control_points = [[0, 0, 0], [1, 1, 0], [2, 0, 0]]
    
    # Test s váhami = 1 (B-spline)
    curve.weights = [1, 1, 1]
    curve.auto_knot_vector()
    point1 = curve.evaluate(0.5)
    
    # Test s jinou váhou
    curve.weights = [1, 2, 1]
    point2 = curve.evaluate(0.5)
    
    # Body by měly být různé
    assert point1 != point2
    
    print("OK")


def test_derivatives():
    """Test derivací"""
    print("Test 3: Derivace... ", end="")
    
    curve = NURBSCurve(degree=3)
    curve.control_points = [[0, 0, 0], [1, 1, 0], [2, 1, 0], [3, 0, 0]]
    curve.auto_knot_vector()
    
    # Test první derivace
    tangent = curve.derivative(0.5, order=1)
    assert len(tangent) == 3
    assert isinstance(tangent[0], float)
    
    # Tečný vektor by neměl být nulový
    length = math.sqrt(sum(t**2 for t in tangent))
    assert length > 0
    
    print("OK")


def test_circle():
    """Test přesnosti kruhu"""
    print("Test 4: Kruh (přesnost)... ", end="")
    
    curve = NURBSCurve(degree=2)
    radius = 1.0
    w = math.sqrt(2) / 2
    
    # Čtvrtina kruhu
    curve.control_points = [
        [radius, 0, 0],
        [radius, radius, 0],
        [0, radius, 0]
    ]
    curve.weights = [1.0, w, 1.0]
    curve.knot_vector = [0, 0, 0, 1, 1, 1]
    
    # Ověření přesnosti
    points = curve.evaluate_multi(50)
    max_error = 0
    
    for point in points:
        distance = math.sqrt(point[0]**2 + point[1]**2)
        error = abs(distance - radius)
        max_error = max(max_error, error)
    
    # Chyba by měla být velmi malá (numerická přesnost)
    assert max_error < 1e-10, f"Max error: {max_error}"
    
    print(f"OK (max error: {max_error:.2e})")


def test_knot_vector():
    """Test generování knot vektoru"""
    print("Test 5: Generování knot vektoru... ", end="")
    
    curve = NURBSCurve(degree=3)
    curve.control_points = [[i, 0, 0] for i in range(5)]
    
    # Clamped
    curve.auto_knot_vector(clamped=True)
    expected_len = 5 + 3 + 1  # n + p + 1
    assert len(curve.knot_vector) == expected_len, f"Expected {expected_len}, got {len(curve.knot_vector)}"
    assert curve.knot_vector[0] == curve.knot_vector[3]  # Opakování na začátku
    assert curve.knot_vector[-1] == curve.knot_vector[-4]  # Opakování na konci
    
    # Unclamped - unclamped má stejnou délku, ale žádné opakování
    curve.auto_knot_vector(clamped=False)
    assert len(curve.knot_vector) == expected_len
    # Unclamped nemá opakování na koncích
    assert curve.knot_vector[0] != curve.knot_vector[1]
    
    print("OK")


def test_2d_curve():
    """Test 2D křivky"""
    print("Test 6: 2D křivka... ", end="")
    
    curve = NURBSCurve(degree=2)
    # 2D kontrolní body
    curve.control_points = [[0, 0], [1, 2], [2, 0]]
    curve.auto_knot_vector()
    
    point = curve.evaluate(0.5)
    assert len(point) == 2  # 2D výstup
    
    print("OK")


def test_endpoint_interpolation():
    """Test interpolace koncových bodů (clamped křivka)"""
    print("Test 7: Interpolace koncových bodů... ", end="")
    
    curve = NURBSCurve(degree=3)
    control_points = [[0, 0, 0], [1, 1, 0], [2, -1, 0], [3, 0, 0]]
    curve.control_points = control_points
    curve.auto_knot_vector(clamped=True)
    
    # První bod křivky by měl být první kontrolní bod
    first_point = curve.evaluate(0.0)
    assert all(abs(first_point[i] - control_points[0][i]) < 1e-10 for i in range(3))
    
    # Poslední bod křivky by měl být poslední kontrolní bod
    last_point = curve.evaluate(1.0)
    assert all(abs(last_point[i] - control_points[-1][i]) < 1e-10 for i in range(3))
    
    print("OK")


def run_all_tests():
    print("=" * 60)
    print("NURBS Curve - Testy")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_curve,
        test_weights,
        test_derivatives,
        test_circle,
        test_knot_vector,
        test_2d_curve,
        test_endpoint_interpolation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Výsledky: {passed} úspěšných, {failed} neúspěšných")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
