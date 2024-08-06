# Copyright (c) 2024, InfinityQ Technology, Inc.

from typing import Union
from titanq._model.variable import Expression, VariableVector, VectorExpression


def fastSum(exprVector: Union[VectorExpression, VariableVector]) -> Expression:
    """
    ℹ️ **This feature is experimental and may change.**

    Computes the sum of all elements in the provided `VectorExpression` or `VariableVector`.
    This function is an faster alternative to the traditional `sum()` operation for vector-based expressions.

    Parameters
    ----------
    exprVector
        The `VectorExpression` or `VariableVector` whose elements are to be summed.

    Returns
    -------
    Expression
        An `Expression` representing the sum of the elements in `exprVector`.

    Raises
    ------
    ValueError
        If the provided input is not of type `VectorExpression` or `VariableVector`.

    Examples
    --------
    >>> from titanq import Model, Vtype
    >>> x = model.add_variable_vector('x', 1000, Vtype.BINARY)
    >>> y = model.add_variable_vector('y', 1000, Vtype.BINARY))
    >>> exprA = fastSum((np.array([3, 4]) * x + (x * y) - 5 * y))
    >>> exprB = fastSum(x)
    """
    if not isinstance(exprVector, (VectorExpression, VariableVector)):
        raise ValueError(f"invalid input of type {type(expression).__name__}")
    
    return exprVector._fastSum()
