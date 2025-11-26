"""
Minimální NURBS křivka - extrahováno z geomdl
Jednoduchý samostatný projekt pro práci s NURBS křivkami
"""

from .curve import NURBSCurve
from . import export

__version__ = "1.0.0"
__all__ = ["NURBSCurve", "export"]
