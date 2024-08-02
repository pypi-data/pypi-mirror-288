"""
vector.py

This module defines a Vector class for representing 2D vectors and performing basic vector operations.

Classes:
    Vector: Represents a 2D vector and implements vector addition, subtraction, negation, scalar multiplication, and dot product.

Type Aliases:
    Number: Represents a numeric type, which can be either int or float.

Functions:
    __init__(self, x: Number = 0, y: Number = 0) -> None: Initializes a new Vector instance.
    add(self, other: "Vector") -> "Vector": Returns the result of adding the current vector with another vector.
    __add__(self, other: "Vector") -> "Vector": Implements the addition operator for vectors.
    __neg__(self) -> "Vector": Returns the negation of the current vector.
    sub(self, other: "Vector") -> "Vector": Returns the result of subtracting another vector from the current vector.
    __sub__(self, other: "Vector") -> "Vector": Implements the subtraction operator for vectors.
    norm(self) -> float: Returns the Euclidean norm (magnitude) of the vector.
    mul(self, factor: Number) -> "Vector": Returns the result of multiplying the vector by a scalar factor.
    __mul__(self, factor: Number) -> "Vector": Implements the multiplication operator for vectors.
    __rmul__(self, factor: Number) -> "Vector": Implements the right multiplication operator for vectors.
    dot(self, other: "Vector") -> float: Returns the dot product of the current vector with another vector.
    __str__(self) -> str: Returns a string representation of the vector.

Author: [Zhou Qiang]
Date: [2024-08-02]
Last Modified: [2024-08-02]
"""


from typing import Union

Number = Union[int, float]

class Vector:
    """
    This is a class representing a two-dimensional vector.
    """
    __slots__ = ('_x', '_y')

    def __init__(self, x:Number=0, y:Number=0) -> None:
        """
        Initialize a new Vector instance.
        Args:
            x (Number, optional): The x-coordinate of the vector. Defaults to 0.
            y (Number, optional): The y-coordinate of the vector. Defaults to 0.
        Returns:
            None.
        """
        self._x = x
        self._y = y

    @property
    def x(self) -> Number:
        return self._x
    
    @x.setter
    def x(self, value: Number) -> None:
        self._x = value

    @property
    def y(self) -> Number:
        return self._y
    
    @y.setter
    def y(self, value: Number) -> None:
        self._y = value

    def add(self, other: "Vector") -> "Vector":
        """
        Adds the current vector to another vector and returns the result.
        Args:
            other (Vector): The vector to add to the current vector.
        Returns:
            Vector: The result of the addition.
        """
        return Vector(self._x + other._x, self._y + other._y)
    
    def __add__(self, other: "Vector") -> "Vector":
        """
        Implement the addition operator for vectors by calling the add method.
        """
        return self.add(other)
    
    def __neg__(self) -> "Vector":
        """
        Returns:
            Vector: The negation of the current vector.
        """
        return Vector(-self._x, -self._y)
    
    def sub(self, other: "Vector") -> "Vector":
        """
        Subtracts another vector from the current vector and returns the result.
        Args:
            other (Vector): The vector to subtract from the current vector.
        Returns:
            Vector: The result of the subtraction.
        """
        return self.add(-other)
    
    def __sub__(self, other: "Vector") -> "Vector":
        """
        Implement the subtraction operator for vectors by calling the sub method.
        """
        return self.sub(other)
    
    @property
    def norm(self, ) -> float:
        """
        Returns:
            float: The Euclidean norm (magnitude) of the vector.
        """
        return (self._x ** 2 + self._y ** 2) ** 0.5
    
    def mul(self, factor: Number) -> "Vector":
        """
        Multiplies the current vector by a scalar factor and returns the result.
        Args:
            factor (Number): The scalar factor to multiply the vector by.
        Returns:
            Vector: The result of the multiplication.
        """
        assert isinstance(factor, (float, int)), "factor must be a number"
        return Vector(self._x * factor, self._y * factor)
    
    def __mul__(self, factor: Number) -> "Vector":
        """
        Implement the multiplication operator for vectors by calling the mul method.
        """
        return self.mul(factor)
    
    def __rmul__(self, factor: Number) -> "Vector":
        """
        Implement the right multiplication operator for vectors by calling the mul method.
        """
        return self.mul(factor)
    
    def dot(self, other: "Vector") -> float:
        """
        Computes the dot product of the current vector with another vector and returns the result.
        Args:
            other (Vector): The vector to compute the dot product with.
        Returns
            float: The dot product of the two vectors.
        """
        return self._x * other._x + self._y * other._y
    
    def __str__(self) -> str:
        """
        Returns:
            str: A string representation of the vector in the format "(x, y)".
        """
        return f"Vector({self._x}, {self._y})"
    
    def __eq__(self, other: "Vector") -> bool:
        assert isinstance(other, Vector), "other must be a Vector"
        """
        Returns:
            bool: True if the two vectors are equal, False otherwise.
        """
        return self._x == other._x and self._y == other._y
    
    def unit(self) -> "Vector":
        """
        Returns the unit vector (vector with magnitude 1) of the current vector.
        """
        norm = self.norm
        if norm < 1e-10:
            raise ValueError("Cannot compute the unit vector of a vector with near-zero magnitude")
        return Vector(self._x / norm, self._y / norm)