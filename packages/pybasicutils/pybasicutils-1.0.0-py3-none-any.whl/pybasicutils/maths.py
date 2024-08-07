from typing import Union
from math import pi, sqrt

def add(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """
    # func > add

    Returns the sum of x and y

    :param x: Union[int, float]
    :param y: Union[int, float]
    :return: Union[int, float]
    """

    return x + y


def sub(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """
    # func > sub

    Returns the difference of x and y

    :param x: Union[int, float]
    :param y: Union[int, float]
    :return: Union[int, float]
    """

    return x - y


def mul(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """
    # func > mul

    Returns the product of x and y.

    :param x: Union[int, float]
    :param y: Union[int, float]
    :return: Union[int, float]
    """

    return x * y

def div(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """
    # func > mul

    Returns the quotient of x and y.

    :param x: Union[int, float]
    :param y: Union[int, float]
    :return: Union[int, float]
    """

    return x / y

def square(x: Union[int, float]) -> Union[int, float]:
    """
    # func > square

    Returns the square root of x.

    :param x: Union[int, float]
    :return: Union[int, float]
    """

    return sqrt(x)


class area:
    """
    # class > area

    Holder namespace for area.
    Look at subfunctions (static).
    """

    @staticmethod
    def square(side: Union[int, float]) -> Union[int, float]:
        """
        # func > square

        Returns the area of a square.

        :param side: Union[int, float]
        :return: Union[int, float]
        """

        return side * side

    @staticmethod
    def rect(l: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        # func > rect

        Returns the area of a rectangle.

        :param l: Union[int, float]
        :param b: Union[int, float]
        :return: Union[int, float]
        """

        return l * b

    @staticmethod
    def circ(r: Union[int, float]) -> Union[int, float]:
        """
        # func > cric

        Returns the area of a circle.

        :param r: Union[int, float]
        :return: Union[int, float]
        """

        return pi * r * 2