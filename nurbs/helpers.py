"""
Pomocné funkce pro NURBS křivky
"""


def find_span(degree, knot_vector, num_ctrlpts, u):
    """
    Najde span v knot vektoru pomocí binárního vyhledávání.
    Implementace Algoritmu A2.1 z The NURBS Book (Piegl & Tiller).
    
    :param degree: stupeň křivky
    :param knot_vector: knot vektor
    :param num_ctrlpts: počet kontrolních bodů
    :param u: parametr
    :return: index spanu
    """
    n = num_ctrlpts - 1
    
    # Speciální případ
    if abs(knot_vector[n + 1] - u) <= 1e-6:
        return n
    
    # Binární vyhledávání
    low = degree
    high = n + 1
    mid = (low + high) // 2
    
    while u < knot_vector[mid] or u >= knot_vector[mid + 1]:
        if u < knot_vector[mid]:
            high = mid
        else:
            low = mid
        mid = (low + high) // 2
    
    return mid


def basis_functions(span, u, degree, knot_vector):
    """
    Vypočítá nenulové bázové funkce.
    Implementace Algoritmu A2.2 z The NURBS Book.
    
    :param span: knot span index
    :param u: parametr
    :param degree: stupeň
    :param knot_vector: knot vektor
    :return: pole bázových funkcí
    """
    N = [0.0] * (degree + 1)
    left = [0.0] * (degree + 1)
    right = [0.0] * (degree + 1)
    
    N[0] = 1.0
    
    for j in range(1, degree + 1):
        left[j] = u - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - u
        saved = 0.0
        
        for r in range(j):
            temp = N[r] / (right[r + 1] + left[j - r])
            N[r] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        
        N[j] = saved
    
    return N


def basis_functions_ders(span, u, degree, knot_vector, order):
    """
    Vypočítá nenulové bázové funkce a jejich derivace.
    Implementace Algoritmu A2.3 z The NURBS Book.
    
    :param span: knot span index
    :param u: parametr
    :param degree: stupeň
    :param knot_vector: knot vektor
    :param order: řád derivace
    :return: 2D pole [derivace][funkce]
    """
    ders = [[0.0 for _ in range(degree + 1)] for _ in range(order + 1)]
    ndu = [[0.0 for _ in range(degree + 1)] for _ in range(degree + 1)]
    left = [0.0] * (degree + 1)
    right = [0.0] * (degree + 1)
    
    ndu[0][0] = 1.0
    
    for j in range(1, degree + 1):
        left[j] = u - knot_vector[span + 1 - j]
        right[j] = knot_vector[span + j] - u
        saved = 0.0
        
        for r in range(j):
            ndu[j][r] = right[r + 1] + left[j - r]
            temp = ndu[r][j - 1] / ndu[j][r]
            ndu[r][j] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        
        ndu[j][j] = saved
    
    # Načtení bázových funkcí
    for j in range(degree + 1):
        ders[0][j] = ndu[j][degree]
    
    # Výpočet derivací
    a = [[0.0 for _ in range(degree + 1)] for _ in range(2)]
    
    for r in range(degree + 1):
        s1 = 0
        s2 = 1
        a[0][0] = 1.0
        
        for k in range(1, min(order, degree) + 1):
            d = 0.0
            rk = r - k
            pk = degree - k
            
            if r >= k:
                a[s2][0] = a[s1][0] / ndu[pk + 1][rk]
                d = a[s2][0] * ndu[rk][pk]
            
            j1 = 1 if rk >= -1 else -rk
            j2 = k - 1 if r - 1 <= pk else degree - r
            
            for j in range(j1, j2 + 1):
                a[s2][j] = (a[s1][j] - a[s1][j - 1]) / ndu[pk + 1][rk + j]
                d += a[s2][j] * ndu[rk + j][pk]
            
            if r <= pk:
                a[s2][k] = -a[s1][k - 1] / ndu[pk + 1][r]
                d += a[s2][k] * ndu[r][pk]
            
            ders[k][r] = d
            
            # Prohození řádků
            s1, s2 = s2, s1
    
    # Násobení faktoriálem
    r = degree
    for k in range(1, min(order, degree) + 1):
        for j in range(degree + 1):
            ders[k][j] *= r
        r *= (degree - k)
    
    return ders


def generate_knot_vector(degree, num_ctrlpts, clamped=True):
    """
    Generuje uniformní knot vektor.
    
    :param degree: stupeň křivky
    :param num_ctrlpts: počet kontrolních bodů
    :param clamped: True pro clamped (uzavřený) knot vektor
    :return: knot vektor
    """
    if degree == 0 or num_ctrlpts == 0:
        raise ValueError("Stupeň a počet kontrolních bodů musí být > 0")
    
    # Počet knotů: m + 1 = n + p + 2, kde n + 1 = num_ctrlpts
    # tedy m + 1 = num_ctrlpts + degree + 1
    m = num_ctrlpts + degree
    
    if clamped:
        # Clamped knot vektor - opakování na začátku a konci
        knot_vector = [0.0] * (degree + 1)
        
        # Vnitřní knoty
        num_inner = m - 2 * degree - 1
        for i in range(1, num_inner + 1):
            knot_vector.append(i / (num_inner + 1))
        
        knot_vector += [1.0] * (degree + 1)
    else:
        # Unclamped knot vektor - uniformní rozložení
        knot_vector = [i / m for i in range(m + 1)]
    
    return knot_vector
