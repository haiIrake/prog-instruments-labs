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
from typing import List


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
    def __init__(self,components=[]):
        """
            input: components or nothing
            simple constructor for init the vector
        """
        self.__components = list(components)

    def set(self, components: List[float]) -> None:
        """
            input: new components
            changes the components of the vector.
            replace the components with newer one.
        """
        if not components:
            raise ValueError("Components list cannot be empty")

        self.__components = list(components)

    def __str__(self):
        """
            returns a string representation of the vector
        """
        return "(" + ",".join(map(str, self.__components)) + ")"

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

    def __len__(self):
        """
            returns the size of the vector
        """
        return len(self.__components)
    def eulidLength(self):
        """
            returns the eulidean length of the vector
        """
        summe = 0
        for c in self.__components:
            summe += c**2
        return math.sqrt(summe)

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

    def __mul__(self, other):
        """
            mul implements the scalar multiplication 
            and the dot-product
        """
        if isinstance(other, float) or isinstance(other, int):
            ans = [c*other for c in self.__components]
            return ans
        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError(f"Cannot compute dot product of vectors with different dimensions: "
                                 f"{len(self)} and {len(other)}")
            size = len(self)
            summe = 0
            for i in range(size):
                summe += self.__components[i] * other.component(i)
            return summe
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Vector' and '{type(other).__name__}'")

    def copy(self):
        """
            copies this vector and returns it.
        """
        return Vector(self.__components)
    def changeComponent(self,pos,value):
        """
            input: an index (pos) and a value
            changes the specified component (pos) with the
            'value'
        """
        #precondition
        assert (-len(self.__components) <= pos < len(self.__components))
        self.__components[pos] = value
    
def zeroVector(dimension):
    """
        returns a zero-vector of size 'dimension'
    """        
    #precondition
    assert(isinstance(dimension,int))
    return Vector([0]*dimension)


def unitBasisVector(dimension,pos):
    """
        returns a unit basis vector with a One 
        at index 'pos' (indexing at 0)
    """
    #precondition
    assert(isinstance(dimension,int) and (isinstance(pos,int)))
    ans = [0]*dimension
    ans[pos] = 1
    return Vector(ans)
        

def axpy(scalar,x,y):
    """
        input: a 'scalar' and two vectors 'x' and 'y'
        output: a vector
        computes the axpy operation
    """
    # precondition
    assert(isinstance(x,Vector) and (isinstance(y,Vector)) \
    and (isinstance(scalar,int) or isinstance(scalar,float)))
    return (x*scalar + y)
    

def randomVector(N,a,b):
    """
        input: size (N) of the vector.
               random range (a,b)
        output: returns a random vector of size N, with 
                random integer components between 'a' and 'b'.
    """
    random.seed(None)
    ans = [random.randint(a,b) for i in range(N)]
    return Vector(ans)


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
    def __init__(self,matrix,w,h):
        """
            simple constructor for initialzes 
            the matrix with components.
        """
        self.__matrix = matrix
        self.__width = w
        self.__height = h
    def __str__(self):
        """
            returns a string representation of this
            matrix.
        """
        ans = ""
        for i in range(self.__height):
            ans += "|"
            for j in range(self.__width):
                if j < self.__width -1:
                    ans += str(self.__matrix[i][j]) + ","
                else:
                    ans += str(self.__matrix[i][j]) + "|\n"
        return ans

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

    def width(self):
        """
            getter for the width
        """
        return self.__width
    def height(self):
        """
            getter for the height
        """
        return self.__height

    def __mul__(self, other):
        """
            implements the matrix-vector multiplication.
            implements the matrix-scalar multiplication
        """
        if isinstance(other, Vector):  # Matrix-vector multiplication
            if len(other) != self.__width:
                raise ValueError(f"Vector dimension ({len(other)}) must match matrix width ({self.__width})")

            ans = zeroVector(self.__height)
            for i in range(self.__height):
                summe = 0
                for j in range(self.__width):
                    summe += other.component(j) * self.__matrix[i][j]
                ans.changeComponent(i, summe)
                summe = 0
            return ans

        elif isinstance(other, int) or isinstance(other, float):  # Scalar multiplication
            matrix = [[self.__matrix[i][j] * other for j in range(self.__width)] for i in range(self.__height)]
            return Matrix(matrix, self.__width, self.__height)

    def __add__(self, other: "Matrix") -> "Matrix":
        """
            implements the matrix-addition.
        """
        if self.__width != other.width or self.__height != other.height:
            raise ValueError(
                f"Cannot add matrices of different dimensions: "
                f"{self.__height}x{self.__width} and {other.height}x{other.width}"
            )

        matrix = []
        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                row.append(self.__matrix[i][j] + other.component(i, j))
            matrix.append(row)
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

        matrix = []
        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                row.append(self.__matrix[i][j] - other.component(i, j))
            matrix.append(row)
        return Matrix(matrix, self.__width, self.__height)

def squareZeroMatrix(N):
    """
        returns a square zero-matrix of dimension NxN
    """
    ans = [[0]*N for i in range(N)]
    return Matrix(ans,N,N)
    
    
def randomMatrix(W,H,a,b):
    """
        returns a random matrix WxH with integer components
        between 'a' and 'b'
    """
    random.seed(None)
    matrix = [[random.randint(a,b) for j in range(W)] for i in range(H)]
    return Matrix(matrix,W,H)
            
        
