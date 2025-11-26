"""
NURBS křivka - racionální B-spline křivka s váhami
"""

from . import helpers


class NURBSCurve:
    """
    Třída pro NURBS (Non-Uniform Rational B-Spline) křivku.
    
    NURBS křivka je definována:
    - Stupněm (degree)
    - Kontrolními body (control points)
    - Váhami (weights)
    - Knot vektorem
    
    Příklad použití:
        curve = NURBSCurve(degree=3)
        curve.control_points = [[0, 0, 0], [1, 2, 0], [3, 1, 0], [4, 0, 0]]
        curve.weights = [1, 1, 2, 1]  # volitelné, výchozí jsou 1
        curve.auto_knot_vector()  # nebo nastavit manuálně
        points = curve.evaluate_multi(50)  # 50 bodů na křivce
    """
    
    def __init__(self, degree=3):
        """
        Inicializace NURBS křivky.
        
        :param degree: stupeň křivky (např. 3 pro kubickou)
        """
        self._degree = degree
        self._control_points = []
        self._weights = []
        self._knot_vector = []
        self._dimension = 3  # výchozí 3D
    
    @property
    def degree(self):
        """Stupeň křivky"""
        return self._degree
    
    @degree.setter
    def degree(self, value):
        if value < 1:
            raise ValueError("Stupeň musí být >= 1")
        self._degree = value
    
    @property
    def control_points(self):
        """Kontrolní body"""
        return self._control_points
    
    @control_points.setter
    def control_points(self, points):
        if not points:
            raise ValueError("Musí být alespoň jeden kontrolní bod")
        self._control_points = [list(p) for p in points]
        self._dimension = len(self._control_points[0])
        # Inicializovat váhy pokud nejsou nastaveny
        if not self._weights:
            self._weights = [1.0] * len(self._control_points)
    
    @property
    def weights(self):
        """Váhy kontrolních bodů"""
        return self._weights
    
    @weights.setter
    def weights(self, w):
        if len(w) != len(self._control_points):
            raise ValueError("Počet vah musí odpovídat počtu kontrolních bodů")
        self._weights = list(w)
    
    @property
    def knot_vector(self):
        """Knot vektor"""
        return self._knot_vector
    
    @knot_vector.setter
    def knot_vector(self, kv):
        expected_len = len(self._control_points) + self._degree + 1
        if len(kv) != expected_len:
            raise ValueError(f"Knot vektor musí mít délku {expected_len}")
        self._knot_vector = list(kv)
    
    @property
    def num_control_points(self):
        """Počet kontrolních bodů"""
        return len(self._control_points)
    
    def auto_knot_vector(self, clamped=True):
        """
        Automaticky vygeneruje uniformní knot vektor.
        
        :param clamped: True pro clamped (uzavřený) knot vektor
        """
        if not self._control_points:
            raise ValueError("Nejprve nastavte kontrolní body")
        
        self._knot_vector = helpers.generate_knot_vector(
            self._degree, 
            len(self._control_points),
            clamped
        )
    
    def _get_weighted_control_points(self):
        """Vrátí homogenní souřadnice (Pw) = kontrolní body * váhy"""
        pw = []
        for i, cp in enumerate(self._control_points):
            w = self._weights[i]
            pw.append([coord * w for coord in cp] + [w])
        return pw
    
    def evaluate(self, u):
        """
        Vypočítá bod na křivce pro parametr u.
        
        :param u: parametr (obvykle mezi 0 a 1)
        :return: bod na křivce [x, y, z, ...]
        """
        if not self._control_points or not self._knot_vector:
            raise ValueError("Křivka není kompletně definována")
        
        # Najít span
        span = helpers.find_span(
            self._degree,
            self._knot_vector,
            self.num_control_points,
            u
        )
        
        # Vypočítat bázové funkce
        basis = helpers.basis_functions(
            span,
            u,
            self._degree,
            self._knot_vector
        )
        
        # Získat vážené kontrolní body (homogenní souřadnice)
        ctrlpts_w = self._get_weighted_control_points()
        
        # Vypočítat bod v homogenních souřadnicích
        point_w = [0.0] * (self._dimension + 1)
        for i, b in enumerate(basis):
            idx = span - self._degree + i
            for j in range(self._dimension + 1):
                point_w[j] += b * ctrlpts_w[idx][j]
        
        # Převést zpět z homogenních souřadnic
        w = point_w[-1]
        point = [coord / w for coord in point_w[:-1]]
        
        return point
    
    def evaluate_multi(self, num_points):
        """
        Vypočítá více bodů na křivce.
        
        :param num_points: počet bodů k vypočítání
        :return: seznam bodů na křivce
        """
        if num_points < 2:
            raise ValueError("Počet bodů musí být >= 2")
        
        points = []
        u_min = self._knot_vector[self._degree]
        u_max = self._knot_vector[-(self._degree + 1)]
        
        for i in range(num_points):
            u = u_min + (u_max - u_min) * i / (num_points - 1)
            points.append(self.evaluate(u))
        
        return points
    
    def derivative(self, u, order=1):
        """
        Vypočítá derivaci křivky v parametru u.
        
        :param u: parametr
        :param order: řád derivace (1, 2, ...)
        :return: vektor derivace
        """
        if not self._control_points or not self._knot_vector:
            raise ValueError("Křivka není kompletně definována")
        
        # Najít span
        span = helpers.find_span(
            self._degree,
            self._knot_vector,
            self.num_control_points,
            u
        )
        
        # Vypočítat bázové funkce a derivace
        ders = helpers.basis_functions_ders(
            span,
            u,
            self._degree,
            self._knot_vector,
            order
        )
        
        # Získat vážené kontrolní body
        ctrlpts_w = self._get_weighted_control_points()
        
        # Vypočítat derivace v homogenních souřadnicích
        CK = [[0.0] * (self._dimension + 1) for _ in range(order + 1)]
        
        for k in range(order + 1):
            for i in range(self._degree + 1):
                idx = span - self._degree + i
                for j in range(self._dimension + 1):
                    CK[k][j] += ders[k][i] * ctrlpts_w[idx][j]
        
        # Převést derivace zpět z homogenních souřadnic (Algoritmus A4.2)
        derivatives = [[0.0] * self._dimension for _ in range(order + 1)]
        
        for k in range(order + 1):
            v = list(CK[k][:-1])
            
            for i in range(1, k + 1):
                # Binomický koeficient
                bc = 1
                for j in range(2, i + 1):
                    bc = bc * (k - j + 1) // j
                
                for j in range(self._dimension):
                    v[j] -= bc * CK[i][-1] * derivatives[k - i][j]
            
            for j in range(self._dimension):
                derivatives[k][j] = v[j] / CK[0][-1]
        
        return derivatives[order]
    
    def __str__(self):
        """Textová reprezentace křivky"""
        return (f"NURBSCurve(degree={self._degree}, "
                f"control_points={self.num_control_points}, "
                f"dimension={self._dimension})")
    
    def __repr__(self):
        return self.__str__()
