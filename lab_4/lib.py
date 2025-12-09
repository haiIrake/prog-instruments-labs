# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:29:11 2018

@author: Christian Bender
@license: MIT-license

This module contains some useful classes and functions for dealing
with linear algebra in python.

Overview:

- class Vector
- function zeroVector(dimension)
- function unitBasisVector(dimension,pos)
- function axpy(scalar,vector1,vector2)
- function randomVector(N,a,b)
- class Matrix
- function squareZeroMatrix(N)
- function randomMatrix(W,H,a,b)
"""


import math
import random
from typing import List, Union


class Vector(object):
    """
        This class represents a vector of arbitray size.
        You need to give the vector components. 
        
        Overview about the methods:
        
        constructor(components : list) : init the vector
        set(components : list) : changes the vector components.
        __str__() : toString method
        component(i : int): gets the i-th component (start by 0)
        __len__() : gets the size of the vector (number of components)
        euclidLength() : returns the eulidean length of the vector.
        operator + : vector addition
        operator - : vector subtraction
        operator * : scalar multiplication and dot product
        copy() : copies this vector and returns it.
        changeComponent(pos,value) : changes the specified component.
    """
    def __init__(self, components: List[float] = None):
        """
            input: components or nothing
            simple constructor for init the vector
        """
        self.__components = list(components) if components else []

    def set(self, components: List[float]) -> None:
        """
            input: new components
            changes the components of the vector.
            replace the components with newer one.
        """
        if not components:
            raise ValueError("Components list cannot be empty")

        self.__components = list(components)

    def __str__(self) -> str:
        """
            returns a string representation of the vector
        """
        return f"({", ".join(str(c) for c in self.__components)})"

    def component(self, index: int) -> float:
        """
            input: index (start at 0)
            output: the i-th component of the vector.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")

        if not -len(self) <= index < len(self):
            raise IndexError(f"Index {index} out of range for vector of length {len(self)}")

        return self.__components[index]

    def __len__(self) -> int:
        """
            returns the size of the vector
        """
        return len(self.__components)

    def eulidLength(self) -> float:
        """
            returns the eulidean length of the vector
        """
        return math.sqrt(sum(c ** 2 for c in self.__components))

    def __add__(self, other: "Vector") -> "Vector":
        """
            input: other vector
            assumes: other vector has the same size
            returns a new vector that represents the sum.
        """
        if len(self) != len(other):
            raise ValueError(f"Cannot add vectors of different dimensions: {len(self)} and {len(other)}")

        result = [self.__components[i] + other.component(i) for i in range(len(self))]
        return Vector(result)

    def __sub__(self, other: "Vector") -> "Vector":
        """
            input: other vector
            assumes: other vector has the same size
            returns a new vector that represents the differenz.
        """
        if len(self) != len(other):
            raise ValueError(f"Cannot subtract vectors of different dimensions: {len(self)} and {len(other)}")

        result = [self.__components[i] - other.component(i) for i in range(len(self))]
        return Vector(result)

    def __mul__(self, other: Union["Vector", int, float]) -> Union["Vector", float]:
        """
            mul implements the scalar multiplication 
            and the dot-product
        """
        if isinstance(other, float) or isinstance(other, int):
            return Vector([c * other for c in self.__components])

        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError(f"Cannot compute dot product of vectors with different dimensions: "
                                 f"{len(self)} and {len(other)}")

            return sum(self.__components[i] * other.component(i) for i in range(len(self)))

        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Vector' and '{type(other).__name__}'")

    def copy(self) -> "Vector":
        """
            copies this vector and returns it.
        """
        return Vector(self.__components)

    def changeComponent(self, position: int, value: float) -> None:
        """
            input: an index (pos) and a value
            changes the specified component (pos) with the
            'value'
        """
        if not -len(self.__components) <= position < len(self.__components):
            raise IndexError(f"Position {position} out of range")

        self.__components[position] = value


def zeroVector(dimension: int) -> Vector:
    """
        returns a zero-vector of size 'dimension'
    """
    if not isinstance(dimension, int):
        raise TypeError(f"Dimension must be an integer, got {type(dimension).__name__}")

    if dimension <= 0:
        raise ValueError(f"Dimension must be positive, got {dimension}")

    return Vector([0.0] * dimension)


def unitBasisVector(dimension: int, position: int) -> Vector:
    """
        returns a unit basis vector with a One 
        at index 'pos' (indexing at 0)
    """
    if not isinstance(dimension, int) or not isinstance(position, int):
        raise TypeError("Both dimension and position must be integers")

    if not 0 <= position < dimension:
        raise IndexError(f"Position {position} out of range for dimension {dimension}")

    components = [0.0] * dimension
    components[position] = 1.0
    return Vector(components)


def axpy(scalar: Union[int, float], x: Vector, y: Vector) -> Vector:
    """
        input: a 'scalar' and two vectors 'x' and 'y'
        output: a vector
        computes the axpy operation
    """
    if not isinstance(x, Vector) or not isinstance(y, Vector):
        raise TypeError("x and y must be Vector instances")

    if not isinstance(scalar, (int, float)):
        raise TypeError(f"Scalar must be int or float, got {type(scalar).__name__}")

    if len(x) != len(y):
        raise ValueError(f"Vectors must have same dimension: {len(x)} and {len(y)}")

    return x * scalar + y


def randomVector(size: int, lower_bound: int, upper_bound: int) -> Vector:
    """
        input: size (N) of the vector.
               random range (a,b)
        output: returns a random vector of size N, with 
                random integer components between 'a' and 'b'.
    """
    if lower_bound > upper_bound:
        raise ValueError(f"Lower bound ({lower_bound}) cannot be greater than upper bound ({upper_bound})")

    components = [random.randint(lower_bound, upper_bound) for _ in range(size)]
    return Vector(components)


class Matrix(object):
    """
    class: Matrix
    This class represents a arbitrary matrix.
    
    Overview about the methods:
    
           __str__() : returns a string representation 
           operator * : implements the matrix vector multiplication
                        implements the matrix-scalar multiplication.
           changeComponent(x,y,value) : changes the specified component.
           component(x,y) : returns the specified component.
           width() : returns the width of the matrix
           height() : returns the height of the matrix
           operator + : implements the matrix-addition.
           operator - _ implements the matrix-subtraction
    """
    def __init__(self, matrix: List[List[float]], width: int, height: int):
        """
            simple constructor for initialzes 
            the matrix with components.
        """
        self.__matrix = matrix
        self.__width = width
        self.__height = height

    def __str__(self) -> str:
        """
            returns a string representation of this
            matrix.
        """
        rows = []
        for i in range(self.__height):
            row_str = f"|{", ".join(str(self.__matrix)[i][j] for j in range(self.__width))}|"
            rows.append(row_str)

        return "\n".join(rows)

    def changeComponent(self, row: int, col: int, value: float) -> None:
        """
            changes the x-y component of this matrix
        """
        if not (0 <= row < self.__height and 0 <= col < self.__width):
            raise IndexError(f"Indices ({row}, {col}) out of bounds for {self.__height}x{self.__width} matrix")

        self.__matrix[row][col] = value

    def component(self, row: int, col: int) -> float:
        """
            returns the specified (x,y) component
        """
        if not (0 <= row < self.__height and 0 <= col < self.__width):
            raise IndexError(f"Indices ({row}, {col}) out of bounds for {self.__height}x{self.__width} matrix")

        return self.__matrix[row][col]

    def width(self) -> int:
        """
            getter for the width
        """
        return self.__width

    def height(self) -> int:
        """
            getter for the height
        """
        return self.__height

    def __mul__(self, other: Union[Vector, int, float]) -> Union['Matrix', Vector]:
        """
            implements the matrix-vector multiplication.
            implements the matrix-scalar multiplication
        """
        if isinstance(other, Vector):  # Matrix-vector multiplication
            if len(other) != self.__width:
                raise ValueError(f"Vector dimension ({len(other)}) must match matrix width ({self.__width})")

            result = zeroVector(self.__height)
            for i in range(self.__height):
                row_sum = sum(self.__matrix[i][j] * other.component(j) for j in range(self.__width))
                result.changeComponent(i, row_sum)

            return result

        elif isinstance(other, (int, float)):  # Scalar multiplication
            matrix = [
                [
                    self.__matrix[i][j] * other
                    for j in range(self.__width)
                ]
                for i in range(self.__height)
            ]

            return Matrix(matrix, self.__width, self.__height)

        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Matrix' and '{type(other).__name__}'")

    def __add__(self, other: "Matrix") -> "Matrix":
        """
            implements the matrix-addition.
        """
        if self.__width != other.width or self.__height != other.height:
            raise ValueError(
                f"Cannot add matrices of different dimensions: "
                f"{self.__height}x{self.__width} and {other.height}x{other.width}"
            )

        matrix = [
            [
                self.__matrix[i][j] + other.component(i, j)
                for j in range(self.__width)
            ]
            for i in range(self.__height)
        ]

        return Matrix(matrix, self.__width, self.__height)

    def __sub__(self, other: "Matrix") -> "Matrix":
        """
            implements the matrix-subtraction.
        """
        if self.__width != other.width or self.__height != other.height:
            raise ValueError(
                f"Cannot subtract matrices of different dimensions: "
                f"{self.__height}x{self.__width} and {other.height}x{other.width}"
            )

        matrix = [
            [
                self.__matrix[i][j] - other.component(i, j)
                for j in range(self.__width)
            ]
            for i in range(self.__height)
        ]

        return Matrix(matrix, self.__width, self.__height)


def squareZeroMatrix(size: int) -> Matrix:
    """
        returns a square zero-matrix of dimension NxN
    """
    if size <= 0:
        raise ValueError(f"Matrix size must be positive, got {size}")

    matrix = [[0.0] * size for _ in range(size)]
    return Matrix(matrix, size, size)


def randomMatrix(width: int, height: int, lower_bound: int, upper_bound: int) -> Matrix:
    """
        returns a random matrix WxH with integer components
        between 'a' and 'b'
    """
    if width <= 0 or height <= 0:
        raise ValueError(f"Matrix dimensions must be positive: {height}x{width}")

    if lower_bound > upper_bound:
        raise ValueError(f"Lower bound ({lower_bound}) cannot be greater than upper bound ({upper_bound})")

    matrix = [
        [
            random.randint(lower_bound, upper_bound)
            for _ in range(width)
        ]
        for _ in range(height)
    ]

    return Matrix(matrix, width, height)
