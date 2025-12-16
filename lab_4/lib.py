# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:29:11 2018

@author: Christian Bender
@license: MIT-license

This module contains some useful classes and functions for dealing
with linear algebra in python.

Overview:

- class BaseVector(ABC)
- class Vector(BaseVector)
- class VectorFactory(ABC)
- class ZeroVectorFactory(VectorFactory)
- class UnitBasisVectorFactory(VectorFactory)
- class RandomVectorFactory(VectorFactory)
- function zero_vector(size)
- function unit_basis_vector(size, position)
- function random_vector(size, lower_bound, upper_bound)
- class BaseMatrix(ABC)
- class Matrix(BaseMatrix)
- class MatrixFactory(ABC)
- class SquareZeroMatrixFactory(MatrixFactory)
- class RandomMatrixFactory(MatrixFactory)
- function square_zero_matrix(size)
- function random_matrix(width, height, lower_bound, upper_bound)
- function axpy(scalar, x, y)
"""


import math
import random
from abc import ABC, abstractmethod
from typing import List, Union


class BaseVector(ABC):
    """Abstract base class for vectors."""

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def component(self, index: int) -> float:
        pass

    @abstractmethod
    def change_component(self, position: int, value: float) -> None:
        pass

    @abstractmethod
    def copy(self) -> "BaseVector":
        pass


class Vector(BaseVector):
    """Represents a vector of arbitrary size."""

    def __init__(self, components: List[float] = None):
        """
        Initialize vector with components.
        :param components: List of vector components. Defaults to empty list.
        """
        self._components = list(components) if components else []

    def set(self, components: List[float]) -> None:
        """
        Set new vector components.
        :param components: New vector components
        """
        if not components:
            raise ValueError("Components list cannot be empty")

        self._components = list(components)

    def __len__(self) -> int:
        """Return the number of components."""
        return len(self._components)

    def __str__(self) -> str:
        """Return string representation of the vector."""
        return f"({", ".join(str(c) for c in self._components)})"

    def component(self, index: int) -> float:
        """
        Get the i-th component of the vector.
        :param index: Component index (supports negative indexing)
        :return: The component value
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")

        if not -len(self) <= index < len(self):
            raise IndexError(f"Index {index} out of range for vector of length {len(self)}")

        return self._components[index]

    def change_component(self, position: int, value: float) -> None:
        """
        Change a specific component of the vector.
        :param position: Index of component to change
        :param value: New value
        """
        if not -len(self) <= position < len(self):
            raise IndexError(f"Position {position} out of range")

        self._components[position] = value

    def copy(self) -> "Vector":
        """Return a copy of this vector."""
        return Vector(self._components.copy())

    def euclidean_length(self) -> float:
        """Calculate the Euclidean length of the vector."""
        return math.sqrt(sum(c ** 2 for c in self._components))

    def __add__(self, other: "Vector") -> "Vector":
        """
        Vector addition.
        :param other: Another vector
        :return: New vector representing the sum
        """
        if len(self) != len(other):
            raise ValueError(f"Cannot add vectors of different dimensions: {len(self)} and {len(other)}")

        result = [self._components[i] + other.component(i) for i in range(len(self))]
        return Vector(result)

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Vector subtraction.
        :param other: Another vector
        :return: New vector representing the difference
        """
        if len(self) != len(other):
            raise ValueError(f"Cannot subtract vectors of different dimensions: {len(self)} and {len(other)}")

        result = [self._components[i] - other.component(i) for i in range(len(self))]
        return Vector(result)

    def scalar_multiply(self, scalar: Union[int, float]) -> "Vector":
        """
        Scalar multiplication.
        :param scalar: Scalar value
        :return: New vector scaled by scalar
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Scalar must be int or float, got {type(scalar).__name__}")

        return Vector([c * scalar for c in self._components])

    def dot_product(self, other: "Vector") -> float:
        """
        Dot product with another vector.
        :param other: Another vector
        :return: Dot product result
        """
        if len(self) != len(other):
            raise ValueError(f"Cannot compute dot product of vectors with different dimensions: "
                             f"{len(self)} and {len(other)}")

        return sum(self._components[i] * other.component(i) for i in range(len(self)))

    def __mul__(self, other: Union["Vector", int, float]) -> Union["Vector", float]:
        """
        Scalar multiplication or dot product.
        :param other: Either a scalar or another vector
        :return: Vector (if scalar multiplication) or float (if dot product)
        """
        if isinstance(other, (int, float)):
            return self.scalar_multiply(other)
        elif isinstance(other, Vector):
            return self.dot_product(other)

        raise TypeError(f"Unsupported operand type(s) for *: 'Vector' and '{type(other).__name__}'")


class VectorFactory(ABC):
    """Abstract factory for creating vectors."""

    @abstractmethod
    def create(self, *args, **kwargs) -> Vector:
        pass


class ZeroVectorFactory(VectorFactory):
    """Factory for creating zero vectors."""

    def create(self, size: int) -> Vector:
        """
        Create a zero vector of given size.
        :param size: Size of the vector
        :return: Zero vector of specified size
        """
        if not isinstance(size, int):
            raise TypeError(f"Vector size must be an integer, got {type(size).__name__}")

        if size <= 0:
            raise ValueError(f"Vector size must be positive, got {size}")

        return Vector([0] * size)


class UnitBasisVectorFactory(VectorFactory):
    """Factory for creating unit basis vectors."""

    def create(self, size: int, position: int) -> Vector:
        """
        Create a unit basis vector.
        :param size: Size of the vector
        :param position: Index where the 1 should be placed (0-based)
        :return: Unit basis vector
        """
        if not isinstance(size, int) or not isinstance(position, int):
            raise TypeError("Both size and position must be integers")

        if not 0 <= position < size:
            raise IndexError(f"Position {position} out of range for size {size}")

        components = [0] * size
        components[position] = 1
        return Vector(components)


class RandomVectorFactory(VectorFactory):
    """Factory for creating random vectors."""

    def create(self, size: int, lower_bound: int, upper_bound: int) -> Vector:
        """
        Generate a random vector.
        :param size: Number of components
        :param lower_bound: Minimum value for components
        :param upper_bound: Maximum value for components
        :return: Random vector with integer components
        """
        if not isinstance(size, int):
            raise TypeError(f"Vector size must be an integer, got {type(size).__name__}")

        if size <= 0:
            raise ValueError(f"Vector size must be positive, got {size}")

        if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
            raise TypeError("Both lower bound and upper bound must be integers")

        if lower_bound > upper_bound:
            raise ValueError(f"Lower bound ({lower_bound}) cannot be greater than upper bound ({upper_bound})")

        components = [random.randint(lower_bound, upper_bound) for _ in range(size)]
        return Vector(components)


def zero_vector(size: int) -> Vector:
    """Wrapper function for backward compatibility."""
    return ZeroVectorFactory().create(size)


def unit_basis_vector(size: int, position: int) -> Vector:
    """Wrapper function for backward compatibility."""
    return UnitBasisVectorFactory().create(size, position)


def random_vector(size: int, lower_bound: int, upper_bound: int) -> Vector:
    """Wrapper function for backward compatibility."""
    return RandomVectorFactory().create(size, lower_bound, upper_bound)


class BaseMatrix(ABC):
    """Abstract base class for matrices."""

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def component(self, row: int, col: int) -> float:
        pass

    @abstractmethod
    def change_component(self, row: int, col: int, value: float) -> None:
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass


class Matrix(BaseMatrix):
    """Represents a matrix of arbitrary dimensions."""

    def __init__(self, matrix: List[List[float]], width: int, height: int):
        """
        Initialize matrix with data.
        :param matrix: 2D list of elements
        :param width: Number of columns
        :param height: Number of rows
        """
        self._matrix = matrix
        self._width = width
        self._height = height

    def __str__(self) -> str:
        """Return a string representation of the matrix."""
        rows = []
        for i in range(self._height):
            row_str = "|" + ", ".join(str(self._matrix[i][j]) for j in range(self._width)) + "|"
            rows.append(row_str)

        return "\n".join(rows)

    def component(self, row: int, col: int) -> float:
        """
        Get a matrix component.
        :param row: Row index
        :param col: Column index
        :return: The component value
        """
        if not (0 <= row < self._height and 0 <= col < self._width):
            raise IndexError(f"Indices ({row}, {col}) out of bounds for {self._height}x{self._width} matrix")

        return self._matrix[row][col]

    def change_component(self, row: int, col: int, value: float) -> None:
        """
        Change a matrix component.
        :param row: Row index (0-based)
        :param col: Column index (0-based)
        :param value: New value
        """
        if not (0 <= row < self._height and 0 <= col < self._width):
            raise IndexError(f"Indices ({row}, {col}) out of bounds for {self._height}x{self._width} matrix")

        self._matrix[row][col] = value

    @property
    def width(self) -> int:
        """Get the number of columns."""
        return self._width

    @property
    def height(self) -> int:
        """Get the number of rows."""
        return self._height

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Matrix addition.
        :param other: Another matrix
        :return: Sum of matrices
        """
        if self._width != other.width or self._height != other.height:
            raise ValueError(
                f"Cannot add matrices of different dimensions: "
                f"{self._height}x{self._width} and {other.height}x{other.width}"
            )

        matrix = [
            [
                self._matrix[i][j] + other.component(i, j)
                for j in range(self._width)
            ]
            for i in range(self._height)
        ]

        return Matrix(matrix, self._width, self._height)

    def __sub__(self, other: "Matrix") -> "Matrix":
        """
        Matrix subtraction.
        :param other: Another matrix
        :return: Difference of matrices
        """
        if self._width != other.width or self._height != other.height:
            raise ValueError(
                f"Cannot subtract matrices of different dimensions: "
                f"{self._height}x{self._width} and {other.height}x{other.width}"
            )

        matrix = [
            [
                self._matrix[i][j] - other.component(i, j)
                for j in range(self._width)
            ]
            for i in range(self._height)
        ]

        return Matrix(matrix, self._width, self._height)

    def scalar_multiply(self, scalar: Union[int, float]) -> "Matrix":
        """
        Scalar multiplication.
        :param scalar: Scalar value
        :return: New matrix scaled by scalar
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Scalar must be int or float, got {type(scalar).__name__}")

        matrix = [
            [
                self._matrix[i][j] * scalar
                for j in range(self._width)
            ]
            for i in range(self._height)
        ]

        return Matrix(matrix, self._width, self._height)

    def vector_multiply(self, vector: Vector) -> Vector:
        """
        Matrix-vector multiplication.
        :param vector: Vector to multiply
        :return: Resulting vector
        """
        if len(vector) != self._width:
            raise ValueError(f"Vector dimension ({len(vector)}) must match matrix width ({self._width})")

        result = zero_vector(self._height)
        for i in range(self._height):
            row_sum = sum(self._matrix[i][j] * vector.component(j) for j in range(self._width))
            result.change_component(i, row_sum)

        return result

    def __mul__(self, other: Union[Vector, int, float]) -> Union['Matrix', Vector]:
        """
        Matrix multiplication or scalar multiplication.
        :param other: Vector (for matrix-vector multiplication) or scalar
        :return: Matrix (if scalar multiplication) or Vector (if matrix-vector multiplication)
        """
        if isinstance(other, Vector):
            return self.vector_multiply(other)
        elif isinstance(other, (int, float)):
            return self.scalar_multiply(other)

        raise TypeError(f"Unsupported operand type(s) for *: 'Matrix' and '{type(other).__name__}'")


class MatrixFactory(ABC):
    """Abstract factory for creating matrices."""

    @abstractmethod
    def create(self, *args, **kwargs) -> Matrix:
        pass


class SquareZeroMatrixFactory(MatrixFactory):
    """Factory for creating square zero matrices."""

    def create(self, size: int) -> Matrix:
        """
        Create a square zero matrix.
        :param size: Dimension of the matrix (size x size)
        :return: Zero matrix of specified size
        """
        if not isinstance(size, int):
            raise TypeError(f"Matrix size must be an integer, got {type(size).__name__}")

        if size <= 0:
            raise ValueError(f"Matrix size must be positive, got {size}")

        matrix = [[0] * size for _ in range(size)]
        return Matrix(matrix, size, size)


class RandomMatrixFactory(MatrixFactory):
    """Factory for creating random matrices."""

    def create(self, width: int, height: int, lower_bound: int, upper_bound: int) -> Matrix:
        """
        Generate a random matrix.
        :param width: Number of columns
        :param height: Number of rows
        :param lower_bound: Minimum value for elements
        :param upper_bound: Maximum value for elements
        :return: Random matrix with integer elements
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("Matrix dimensions must be integers")

        if width <= 0 or height <= 0:
            raise ValueError(f"Matrix dimensions must be positive: {height}x{width}")

        if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
            raise TypeError("Both lower bound and upper bound must be integers")

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


def square_zero_matrix(size: int) -> Matrix:
    """Wrapper function for backward compatibility."""
    return SquareZeroMatrixFactory().create(size)


def random_matrix(width: int, height: int, lower_bound: int, upper_bound: int) -> Matrix:
    """Wrapper function for backward compatibility."""
    return RandomMatrixFactory().create(width, height, lower_bound, upper_bound)


def axpy(scalar: Union[int, float], x: Vector, y: Vector) -> Vector:
    """
    Compute αx + y (AXPY operation).
    :param scalar: Scalar α
    :param x: First vector
    :param y: Second vector
    :return: Result of αx + y
    """
    if not isinstance(x, Vector) or not isinstance(y, Vector):
        raise TypeError("x and y must be Vector instances")

    if not isinstance(scalar, (int, float)):
        raise TypeError(f"Scalar must be int or float, got {type(scalar).__name__}")

    if len(x) != len(y):
        raise ValueError(f"Vectors must have same dimension: {len(x)} and {len(y)}")

    return x * scalar + y
