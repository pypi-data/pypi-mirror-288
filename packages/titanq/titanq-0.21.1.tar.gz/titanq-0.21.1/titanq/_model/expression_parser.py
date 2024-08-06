# Copyright (c) 2024, InfinityQ Technology, Inc.

from typing import Optional, Tuple, Union

import numpy as np

from .variable_list import VariableVectorList
from .variable import Expression, SubVariable, Term


def process_expression(
    expr: Union[SubVariable, Term, Expression],
    variables: VariableVectorList,
) -> Tuple[Optional[np.ndarray], np.ndarray, float]:
    """
    Processes an expression to extract the bias vector, weights matrix and constant term.

    This function processes an expression and a list of variable vectors to extract
    the bias vector and weights matrix. The bias vector and weights matrix are initialized
    based on the number of variables and then populated based on the terms in the expression.

    Parameters
    ----------
    expr
        The expression from which to extract the bias vector, weights matrix and constant.
    variables
        A list of variable vectors used in the expression.
        Each variable vector's size contributes to the overall size of the bias vector and weights matrix.

    Returns
    -------
    weights matrix if any, bias vector, and constant

    Raises
    ------
    TypeError
        If the expression is of an unsupported type.
    """
    if not isinstance(expr, (SubVariable, Term, Expression)):
        raise TypeError("TitanQ supports expressions that input variable values and output a singular objective")

    total_size = variables.total_variable_size()
    bias = np.zeros(total_size, dtype=np.float32)
    weights = np.zeros((total_size, total_size), dtype=np.float32)

    if isinstance(expr, SubVariable):
        expr = Term(expr, None, 1)
    if isinstance(expr, Term):
        expr = Expression([expr])

    indexed_variables = variables.index_variables()
    constant = 0
    for term in expr.terms():
        if isinstance(term, Term):
            index_v1 = indexed_variables[term.v1().parent().name()] + term.v1().index()
            if term.v2() is None:# linear
                bias[index_v1] += term.coeff()
            else: # quadratic
                index_v2 = indexed_variables[term.v2().parent().name()] + term.v2().index()
                weights[index_v1, index_v2 ] += term.coeff()
                if index_v1 != index_v2:
                    weights[index_v2 , index_v1] += term.coeff()
        else:
            constant -= term

    return weights if np.any(weights) else None, bias, constant