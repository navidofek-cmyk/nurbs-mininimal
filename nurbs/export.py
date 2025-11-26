"""
Export funkcionalita pro NURBS křivky
"""

import json
import csv


def export_curve_points_txt(curve, num_points, filename):
    """
    Exportuje body na křivce do textového souboru.
    
    :param curve: NURBSCurve instance
    :param num_points: počet bodů k vygenerování
    :param filename: cesta k výstupnímu souboru
    """
    points = curve.evaluate_multi(num_points)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# NURBS Curve Points\n")
        f.write(f"# Number of points: {num_points}\n")
        f.write(f"# Degree: {curve.degree}\n")
        f.write(f"# Control points: {curve.num_control_points}\n")
        f.write(f"# Dimension: {len(points[0])}\n")
        f.write("#\n")
        
        if len(points[0]) == 2:
            f.write("# x y\n")
            for point in points:
                f.write(f"{point[0]:.6f} {point[1]:.6f}\n")
        else:
            f.write("# x y z\n")
            for point in points:
                f.write(f"{point[0]:.6f} {point[1]:.6f} {point[2]:.6f}\n")
    
    return filename


def export_curve_points_csv(curve, num_points, filename):
    """
    Exportuje body na křivce do CSV souboru.
    
    :param curve: NURBSCurve instance
    :param num_points: počet bodů k vygenerování
    :param filename: cesta k výstupnímu souboru
    """
    points = curve.evaluate_multi(num_points)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if len(points[0]) == 2:
            writer = csv.writer(f)
            writer.writerow(['x', 'y'])
            for point in points:
                writer.writerow([f"{point[0]:.6f}", f"{point[1]:.6f}"])
        else:
            writer = csv.writer(f)
            writer.writerow(['x', 'y', 'z'])
            for point in points:
                writer.writerow([f"{point[0]:.6f}", f"{point[1]:.6f}", f"{point[2]:.6f}"])
    
    return filename


def export_control_points_txt(curve, filename):
    """
    Exportuje kontrolní body (řídící polygon) do textového souboru.
    
    :param curve: NURBSCurve instance
    :param filename: cesta k výstupnímu souboru
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# NURBS Control Points (Řídící polygon)\n")
        f.write(f"# Degree: {curve.degree}\n")
        f.write(f"# Number of control points: {curve.num_control_points}\n")
        f.write(f"# Dimension: {len(curve.control_points[0])}\n")
        f.write("#\n")
        
        if len(curve.control_points[0]) == 2:
            f.write("# x y weight\n")
            for i, (cp, w) in enumerate(zip(curve.control_points, curve.weights)):
                f.write(f"{cp[0]:.6f} {cp[1]:.6f} {w:.6f}\n")
        else:
            f.write("# x y z weight\n")
            for i, (cp, w) in enumerate(zip(curve.control_points, curve.weights)):
                f.write(f"{cp[0]:.6f} {cp[1]:.6f} {cp[2]:.6f} {w:.6f}\n")
    
    return filename


def export_control_points_csv(curve, filename):
    """
    Exportuje kontrolní body do CSV souboru.
    
    :param curve: NURBSCurve instance
    :param filename: cesta k výstupnímu souboru
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        if len(curve.control_points[0]) == 2:
            writer.writerow(['x', 'y', 'weight'])
            for cp, w in zip(curve.control_points, curve.weights):
                writer.writerow([f"{cp[0]:.6f}", f"{cp[1]:.6f}", f"{w:.6f}"])
        else:
            writer.writerow(['x', 'y', 'z', 'weight'])
            for cp, w in zip(curve.control_points, curve.weights):
                writer.writerow([f"{cp[0]:.6f}", f"{cp[1]:.6f}", f"{cp[2]:.6f}", f"{w:.6f}"])
    
    return filename


def export_to_json(curve, num_curve_points, filename):
    """
    Exportuje kompletní data křivky do JSON formátu.
    Obsahuje: kontrolní body, váhy, knot vektor, body na křivce.
    
    :param curve: NURBSCurve instance
    :param num_curve_points: počet bodů křivky k vygenerování
    :param filename: cesta k výstupnímu souboru
    """
    curve_points = curve.evaluate_multi(num_curve_points)
    
    data = {
        "type": "NURBS_Curve",
        "degree": curve.degree,
        "dimension": len(curve.control_points[0]),
        "control_points": curve.control_points,
        "weights": curve.weights,
        "knot_vector": curve.knot_vector,
        "curve_points": {
            "count": num_curve_points,
            "points": curve_points
        }
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    return filename


def export_to_obj(curve, num_points, filename):
    """
    Exportuje křivku do Wavefront OBJ formátu (jako polyline).
    
    :param curve: NURBSCurve instance
    :param num_points: počet bodů k vygenerování
    :param filename: cesta k výstupnímu souboru
    """
    points = curve.evaluate_multi(num_points)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Wavefront OBJ file\n")
        f.write(f"# NURBS Curve (degree {curve.degree})\n")
        f.write(f"# Generated points: {num_points}\n\n")
        
        # Vertices
        for point in points:
            if len(point) == 2:
                f.write(f"v {point[0]:.6f} {point[1]:.6f} 0.0\n")
            else:
                f.write(f"v {point[0]:.6f} {point[1]:.6f} {point[2]:.6f}\n")
        
        # Line
        f.write("\n# Curve as polyline\n")
        f.write("l")
        for i in range(1, num_points + 1):
            f.write(f" {i}")
        f.write("\n")
        
        # Control polygon
        f.write("\n# Control points\n")
        for cp in curve.control_points:
            if len(cp) == 2:
                f.write(f"v {cp[0]:.6f} {cp[1]:.6f} 0.0\n")
            else:
                f.write(f"v {cp[0]:.6f} {cp[1]:.6f} {cp[2]:.6f}\n")
        
        f.write("\n# Control polygon\n")
        f.write("l")
        for i in range(num_points + 1, num_points + curve.num_control_points + 1):
            f.write(f" {i}")
        f.write("\n")
    
    return filename


def export_approximation(curve, num_points, filename_prefix):
    """
    Exportuje aproximaci NURBS křivky - jak body křivky, tak kontrolní body.
    Vytvoří několik souborů s různými formáty.
    
    :param curve: NURBSCurve instance
    :param num_points: počet bodů křivky k aproximaci
    :param filename_prefix: prefix pro výstupní soubory (bez přípony)
    :return: slovník s cestami k vytvořeným souborům
    """
    files = {}
    
    # Body křivky
    files['curve_txt'] = export_curve_points_txt(curve, num_points, f"{filename_prefix}_curve.txt")
    files['curve_csv'] = export_curve_points_csv(curve, num_points, f"{filename_prefix}_curve.csv")
    
    # Kontrolní body
    files['control_txt'] = export_control_points_txt(curve, f"{filename_prefix}_control.txt")
    files['control_csv'] = export_control_points_csv(curve, f"{filename_prefix}_control.csv")
    
    # Kompletní data
    files['json'] = export_to_json(curve, num_points, f"{filename_prefix}.json")
    files['obj'] = export_to_obj(curve, num_points, f"{filename_prefix}.obj")
    
    return files


def print_export_summary(files):
    """Vypíše shrnutí exportovaných souborů."""
    print("\n" + "=" * 60)
    print("Exportované soubory:")
    print("=" * 60)
    for key, path in files.items():
        print(f"  {key:15s}: {path}")
    print("=" * 60)
