import sys


__version__ = "0.1.0"


def ring_length(radius: int) -> int:
    if radius == 0:
        return 1
    return 6 * (1 << (radius - 1))


def grid_size(radius: int) -> int:
    return 6 * (1 << radius) - 5


def get_tile_number(radius: int, angle: float) -> int:
    """Get the number representing a tile given its polar coordinates.

    Tiles are numbered from 0, in increasing order, starting at the
    origin (center of the grid), spiraling around the origin,
    with the first tile of each ring at 0°.

    :param radius: The distance to origin
    :param angle: The angle in degrees, 0° being at "noon"
    :return: The tile's identifying number
    :raises ValueError: When the angle is not between 0 and 360
    """
    if angle < 0 or angle >= 360:
        raise ValueError(
            f"Angle must be between 0 (included) and 360 (excluded). Got: ${angle}"
        )
    if radius == 0:
        return 0
    return round(6 * (1 << (radius - 1)) * (1 + angle/360) - 5)


def get_radius(number: int) -> int:
    """Get the radius of a tile given its associated number.

    :param number: The tile's identifying number
    :return: The distance to origin
    """
    if number == 0:
        return 0
    word_size = 64 if (sys.maxsize > 2**32) else 32
    for rank in range(1, word_size):
        if 1 << rank > (number + 5) / 6:
            return rank
    raise RuntimeError("Unexpected error")


def get_angle(number: int) -> float:
    """Get the angle of a tile given its associated number.

    :param number: The tile's identifying number
    :return: The angle in degrees relative to "noon"
    """
    numerator = number + 5
    denominator = 6 * (1 << (get_radius(number) - 1))
    return 360 * (numerator/denominator - 1)
