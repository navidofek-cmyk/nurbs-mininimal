"""
Příklad exportu bodů NURBS křivky do různých formátů
"""

import sys
import os

# Přidat parent directory do path pro import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nurbs import NURBSCurve, export


def main():
    print("=" * 60)
    print("Export NURBS křivky - Příklad")
    print("=" * 60)
    
    # Vytvořit kubickou NURBS křivku
    curve = NURBSCurve(degree=3)
    
    # Nastavit kontrolní body
    curve.control_points = [
        [0, 0, 0],
        [1, 2, 0],
        [3, 2, 0],
        [4, 0, 0],
        [5, -1, 0]
    ]
    
    # Nastavit váhy (prostřední bod má větší váhu)
    curve.weights = [1.0, 1.0, 2.0, 1.0, 1.0]
    
    # Vygenerovat knot vektor
    curve.auto_knot_vector()
    
    print(f"\nKřivka: {curve}")
    print(f"Kontrolní body: {curve.num_control_points}")
    print(f"Váhy: {curve.weights}")
    
    # Vytvořit výstupní složku
    output_dir = "export_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nVýstupní složka: {output_dir}/")
    
    # 1. Export bodů křivky do TXT
    print("\n" + "-" * 60)
    print("1. Export bodů křivky (approximation)")
    print("-" * 60)
    
    num_points = 50
    txt_file = os.path.join(output_dir, "curve_points.txt")
    export.export_curve_points_txt(curve, num_points, txt_file)
    print(f"✓ TXT: {txt_file} ({num_points} bodů)")
    
    # 2. Export bodů křivky do CSV
    csv_file = os.path.join(output_dir, "curve_points.csv")
    export.export_curve_points_csv(curve, num_points, csv_file)
    print(f"✓ CSV: {csv_file} ({num_points} bodů)")
    
    # 3. Export kontrolních bodů (řídící polygon)
    print("\n" + "-" * 60)
    print("2. Export kontrolních bodů (řídící polygon)")
    print("-" * 60)
    
    control_txt = os.path.join(output_dir, "control_points.txt")
    export.export_control_points_txt(curve, control_txt)
    print(f"✓ TXT: {control_txt} ({curve.num_control_points} bodů)")
    
    control_csv = os.path.join(output_dir, "control_points.csv")
    export.export_control_points_csv(curve, control_csv)
    print(f"✓ CSV: {control_csv} ({curve.num_control_points} bodů)")
    
    # 4. Export do JSON (kompletní data)
    print("\n" + "-" * 60)
    print("3. Export kompletních dat (JSON)")
    print("-" * 60)
    
    json_file = os.path.join(output_dir, "curve_complete.json")
    export.export_to_json(curve, num_points, json_file)
    print(f"✓ JSON: {json_file}")
    print(f"  - Obsahuje: kontrolní body, váhy, knot vektor, body křivky")
    
    # 5. Export do OBJ (pro 3D software)
    print("\n" + "-" * 60)
    print("4. Export do OBJ formátu")
    print("-" * 60)
    
    obj_file = os.path.join(output_dir, "curve.obj")
    export.export_to_obj(curve, num_points, obj_file)
    print(f"✓ OBJ: {obj_file}")
    print(f"  - Křivka jako polyline + řídící polygon")
    print(f"  - Lze otevřít v Blenderu, MeshLab, atd.")
    
    # 6. Kompletní export (všechny formáty najednou)
    print("\n" + "-" * 60)
    print("5. Kompletní export (všechny formáty)")
    print("-" * 60)
    
    prefix = os.path.join(output_dir, "my_curve")
    files = export.export_approximation(curve, 100, prefix)
    
    print(f"Exportováno {len(files)} souborů:")
    for key, path in files.items():
        print(f"  ✓ {key:15s}: {os.path.basename(path)}")
    
    # Ukázka obsahu některých souborů
    print("\n" + "=" * 60)
    print("Ukázka obsahu souborů")
    print("=" * 60)
    
    # Ukázka TXT souboru s body křivky
    print(f"\n{txt_file}:")
    print("-" * 60)
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:15]  # prvních 15 řádků
        print("".join(lines))
        if len(lines) == 15:
            print("...")
    
    # Ukázka kontrolních bodů
    print(f"\n{control_txt}:")
    print("-" * 60)
    with open(control_txt, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    
    print("\n" + "=" * 60)
    print("Hotovo!")
    print("=" * 60)
    print(f"\nVšechny soubory jsou v: {os.path.abspath(output_dir)}/")
    
    # Návod na použití
    print("\n" + "=" * 60)
    print("Jak použít exportované soubory")
    print("=" * 60)
    print("""
1. TXT/CSV soubory:
   - Otevřít v Excelu, LibreOffice, Python (pandas, numpy)
   - Body křivky = aproximace NURBS křivky
   - Kontrolní body = řídící polygon
   
2. JSON soubor:
   - Kompletní definice křivky
   - Lze načíst zpět do programu
   - Přenositelný formát
   
3. OBJ soubor:
   - Otevřít v Blenderu: File → Import → Wavefront (.obj)
   - Nebo v MeshLab, Maya, 3ds Max, atd.
   - Obsahuje křivku i řídící polygon
   
4. Python zpracování:
   import pandas as pd
   df = pd.read_csv('curve_points.csv')
   print(df)
""")


if __name__ == "__main__":
    main()
