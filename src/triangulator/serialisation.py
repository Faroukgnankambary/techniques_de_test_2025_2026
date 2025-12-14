from __future__ import annotations
from typing import List, Tuple
import struct

Point = Tuple[float, float]
Triangle = Tuple[int, int, int]


def pointset_to_binary(points: List[Point]) -> bytes:
    """
    Sérialise un ensemble de points (PointSet) en binaire.

    Args:
        points: liste de tuples (x, y)

    Returns:
        Bytes représentant le PointSet au format défini dans le sujet.
    """
    nb_points = len(points)

    # 4 premiers octets : nombre de points
    blocs = [struct.pack("<I", nb_points)]

    # Ensuite, pour chaque point : X (float32) puis Y (float32)
    for x, y in points:
        blocs.append(struct.pack("<f", float(x)))
        blocs.append(struct.pack("<f", float(y)))

    return b"".join(blocs)


def binary_to_pointset(data: bytes) -> List[Point]:
    """
    Désérialise un PointSet binaire en liste de points (x, y).

    Args:
        data: données binaires au format PointSet

    Returns:
        Liste de points (x, y).

    Raises:
        ValueError: si les données sont trop courtes ou incohérentes.
    """
    if len(data) < 4:
        raise ValueError("Données trop courtes pour contenir un PointSet.")

    offset = 0

    # Nombre de points
    (nb_points,) = struct.unpack_from("<I", data, offset)
    offset += 4

    taille_attendue = 4 + nb_points * 8  # 4 octets (count) + 8 par point
    if len(data) < taille_attendue:
        raise ValueError("Données incomplètes pour le nombre de points annoncé.")

    points: List[Point] = []

    for _ in range(nb_points):
        x = struct.unpack_from("<f", data, offset)[0]
        offset += 4
        y = struct.unpack_from("<f", data, offset)[0]
        offset += 4
        points.append((x, y))

    return points


def triangles_to_binary(points: List[Point], triangles: List[Triangle]) -> bytes:
    """
    Sérialise un ensemble de triangles en format binaire Triangles.

    La première partie est le PointSet (les sommets),
    la deuxième partie est la liste des triangles sous forme d'indices.

    Args:
        points: liste de sommets (x, y)
        triangles: liste de triangles (a, b, c) où a, b, c sont des indices dans points.

    Returns:
        Bytes représentant la structure Triangles.
    """
    nb_triangles = len(triangles)

    # Première partie : les points (PointSet)
    blocs = [pointset_to_binary(points)]

    # Deuxième partie : nombre de triangles
    blocs.append(struct.pack("<I", nb_triangles))

    # Puis pour chaque triangle : 3 x unsigned int 32 bits
    for a, b, c in triangles:
        blocs.append(struct.pack("<I", int(a)))
        blocs.append(struct.pack("<I", int(b)))
        blocs.append(struct.pack("<I", int(c)))

    return b"".join(blocs)


def binary_to_triangles(data: bytes) -> Tuple[List[Point], List[Triangle]]:
    """
    Désérialise une structure Triangles en (points, triangles).

    Args:
        data: données binaires au format Triangles.

    Returns:
        Tuple (points, triangles) où :
            - points est une liste de (x, y)
            - triangles est une liste de (a, b, c) indices dans points

    Raises:
        ValueError: si les données sont trop courtes ou incohérentes.
    """
    if len(data) < 4:
        raise ValueError("Données trop courtes pour contenir un PointSet.")

    offset = 0

    # Lire le nombre de points
    (nb_points,) = struct.unpack_from("<I", data, offset)
    offset += 4

    # Taille de la partie PointSet
    taille_points = 4 + nb_points * 8
    if len(data) < taille_points + 4:
        raise ValueError("Données incomplètes pour points + triangles.")

    # On réutilise binary_to_pointset pour la première partie
    points = binary_to_pointset(data[:taille_points])

    offset = taille_points

    # Nombre de triangles
    (nb_triangles,) = struct.unpack_from("<I", data, offset)
    offset += 4

    triangles: List[Triangle] = []

    taille_attendue = taille_points + 4 + nb_triangles * 12
    if len(data) < taille_attendue:
        raise ValueError("Données incomplètes pour la liste de triangles.")

    for _ in range(nb_triangles):
        a = struct.unpack_from("<I", data, offset)[0]
        offset += 4
        b = struct.unpack_from("<I", data, offset)[0]
        offset += 4
        c = struct.unpack_from("<I", data, offset)[0]
        offset += 4
        triangles.append((a, b, c))

    return points, triangles



#Module de sérialisation / désérialisation pour les structures
#PointSet et Triangles utilisées par le service Triangulator.
#Format binaire (little-endian) :
#PointSet :
#   - 4 octets : nombre de points (unsigned long / unsigned int 32 bits)
#   - pour chaque point :
#        - 4 octets : coordonnée X (float32)
#       - 4 octets : coordonnée Y (float32)
#
#riangles :
#  - première partie : PointSet (voir ci-dessus)
#    - deuxième partie :
#       - 4 octets : nombre de triangles (unsigned long / unsigned int 32 bits)
#      - pour chaque triangle :
#           - 4 octets : indice du premier sommet (unsigned long)
#           - 4 octets : indice du deuxième sommet (unsigned long)
#           - 4 octets : indice du troisième sommet (unsigned long)
