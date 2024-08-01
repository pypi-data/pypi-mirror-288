from __future__ import (
    absolute_import,
)

import six
import operator

from collections import (
    Iterable,
)

from django.db.models import (
    Q,
)
from django.utils.functional import (
    LazyObject,
)

# Metadata
__docformat__ = 'restructuredtext'
__all__ = ['BooleanExpression', 'BE', 'expression_to_q', 'expression_to_bool', 'get_empty_filter_expression']


class BooleanExpression(object):
    """Логическое выражение (для построения фильтров)."""

    # Операторы сравнения
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    EQ = 'eq'
    NE = 'neq'
    LT = 'lt'
    LE = 'lte'
    GT = 'gt'
    GE = 'gte'
    IC = 'icontains'
    CT = 'contains'
    OL = 'overlap'
    IN = 'in'
    INL = 'isnull'
    EX = 'exact'
    RE = 'regex'
    CTB = 'contained_by'

    def __init__(self, left, operator=None, right=None):
        """Инициализация выражения.

        Args:
            left: Левый операнд.
            operator: Необязательный; Оператор на операндами.
            right: Необязательный; Правый операнд.

        """

        self.left = left
        self.right = right
        self.operator = operator

    def __unicode__(self):
        return f'{self.left} {self.operator} {self.right}'

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'

    # object & other
    def __and__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self, self.AND, other)
        elif other is None:
            return self
        else:
            raise TypeError((
                "unsupported operand type(s) for &: '{cls}' "
                "and '{other!r}'"
            ).format(
                cls=self.__class__.__name__,
                other=other
            ))

    # other & object
    __rand__ = __and__

    # object | other
    def __or__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self, self.OR, other)
        elif other is None:
            return self
        else:
            raise TypeError(
                "unsupported operand type(s) for |: 'BooleanExpression' "
                "and '%s'" % type(other))

    # other | object
    __ror__ = __or__

    def __invert__(self):
        return self.__class__(self, self.NOT)

    def find_value(self, value, in_left=True, in_right=False):
        """Поиск выражения.

        Поиск выражения, в котором встречается *value*. Параметры *in_left*
        и *in_right* указывают где искать, в каких частях выражения.

        Returns:
            Если выражение найдено, то оно возвращается (первое
            найденное), иначе возвращается :const:`None`.
        """

        expr = None
        if in_left and self.left == value:
            expr = self
        if not expr and in_right and self.right == value:
            expr = self
        if not expr and isinstance(self.left, self.__class__):
            expr = self.left.find_value(value, in_left, in_right)
        if not expr and isinstance(self.right, self.__class__):
            expr = self.right.find_value(value, in_left, in_right)
        return expr

    def iter_nodes(self, left=False, right=False):
        """
        Итератор по листовым значениям. Параметры left и right
        ограничивают, какие части выражения нужно выдавать.
        """

        if isinstance(self.left, self.__class__):
            yield from self.left.iter_nodes(left, right)
        elif left:
            yield self.left

        if isinstance(self.right, self.__class__):
            yield from self.right.iter_nodes(left, right)
        elif right:
            yield self.right

    def remove(self, expression):
        """
        Удаление вложенного выражения из текущего выражения.
        Оставшееся выражение заменяет родительское
        """

        parent_expr = self.__find_nested(expression)
        if parent_expr is not None:
            if parent_expr.left == expression:
                new_parent_expression = parent_expr.right
            else:
                new_parent_expression = parent_expr.left
            parent_expr.right = new_parent_expression.right
            parent_expr.operator = new_parent_expression.operator
            parent_expr.left = new_parent_expression.left

    def replace(self, expression, to_expression):
        """Замена вложенного выражения на новое."""

        parent_expr = self.__find_nested(expression)
        if parent_expr is not None:
            # если найденное выражение находится слева
            if parent_expr.left == expression:
                parent_expr.left = to_expression
            else:
                parent_expr.right = to_expression

    def to_bool(self, *a, **kw):
        return expression_to_bool(self, *a, **kw)

    def to_q(self, *a, **kw):
        return expression_to_q(self, *a, **kw)

    def __find_nested(self, expression):
        """Поиск вложенного выражения.

        Ищется вложенное выражение (первое вхождение) и возвращается
        родительское выражение, в которое оно входит.

        Returns:
            Если не нашлось, или текущее выражение совпадает с
            искомым, то возвращается :const:`None`.
        """

        result = None
        if expression == self:
            result = None
        elif isinstance(self.left, self.__class__) and expression == self.left:
            result = self
        elif isinstance(self.right, self.__class__) and expression == self.right:
            result = self
        if not result and isinstance(self.left, self.__class__):
            result = self.left.__find_nested(expression)
        if not result and isinstance(self.right, self.__class__):
            result = self.right.__find_nested(expression)

        return result


BE = BooleanExpression


def expression_to_q(boolexp):
    """Преобразователь логического выражения в Q-объекты django."""

    operators = {
        BE.AND: operator.and_,
        BE.OR: operator.or_,
        BE.LE: '__lte',
        BE.LT: '__lt',
        BE.GE: '__gte',
        BE.GT: '__gt',
        BE.EQ: '',
        BE.NE: '',
        BE.IN: '__in',
        BE.INL: '__isnull',
        BE.EX: '__exact',
        BE.IC: '__icontains',
        BE.CT: '__contains',
        BE.CTB: '__contained_by',
        BE.OL: '__overlap',
        BE.RE: '__regex'
    }

    operator_const = boolexp.operator
    negation = operator_const == BE.NE

    # Инициализация левого и правого операндов.
    left = _init_operand_q(boolexp.left)
    right = _init_operand_q(boolexp.right)

    # Если правого оператора нет, то результатом будет левый
    # или отрицание левого.
    expr = _neg_left(operator_const, left, boolexp.right)

    # Если правый операнд содержит перечисление, то оператор
    # меняется на :attr:`BE.IN`.
    operator_const = _eq2in(right, operator_const)

    if operator_const in operators:
        operator_postfix = operators[operator_const]
        if callable(operator_postfix):
            expr = operator_postfix(left, right)
        elif isinstance(operator_postfix, six.string_types):
            expr = Q((left + operator_postfix, right))

    elif expr is None:
        raise ValueError(f"Handler for operator '{operator_const}' not exist.")

    return ~expr if negation else expr


def expression_to_bool(boolexp, left_callback=None, right_callback=None):
    """Преобразователь логического выражения в логическое значение."""

    operators = {
        BE.AND: operator.and_,
        BE.OR: operator.or_,
        BE.LE: operator.le,
        BE.LT: operator.lt,
        BE.GE: operator.ge,
        BE.GT: operator.gt,
        BE.EQ: operator.eq,
        BE.EX: operator.eq,
        BE.NE: operator.ne,
        BE.IN: lambda *a: operator.contains(*a[::-1]),
        BE.INL: lambda a, b: (a is None) == b,
        BE.OL: lambda a, b: bool(set(a) & set(b)),
    }

    operator_const = boolexp.operator

    # Инициализация левого и правого операндов.
    callbacks = (left_callback, right_callback)
    left = _init_operand(boolexp.left, left_callback, callbacks)
    right = _init_operand(boolexp.right, right_callback, callbacks)

    # Если правого оператора нет, то результатом будет левый
    # или отрицание левого.
    expr = _neg_left(operator_const, left, boolexp.right)

    # Если правый операнд содержит перечисление, то оператор
    # меняется на :attr:`BE.IN`.
    operator_const = _eq2in(right, operator_const)

    if operator_const == BE.IC:
        operator_callable = operators[BE.IN]
        expr = operator_callable(six.text_type(right).upper(),
                                 six.text_type(left).upper())

    elif operator_const in operators:
        operator_callable = operators[operator_const]
        expr = operator_callable(left, right)

    elif expr is None:
        raise ValueError(f"Handler for operator '{operator_const}' not exist.")

    return expr


def _init_operand_q(value):
    if isinstance(value, BE):
        operand = expression_to_q(value)
    else:
        operand = value

    return operand


def _init_operand(value, mutator, callbacks):
    if isinstance(value, BE):
        operand = expression_to_bool(value, *callbacks)
    else:
        operand = mutator(value) if mutator and mutator(value) else value

    return '' if operand is None else operand


def _eq2in(right_operand, operator_const):
    if (
        isinstance(right_operand, Iterable) and
        not isinstance(right_operand, LazyObject) and
        not isinstance(right_operand, six.string_types) and
        operator_const in (BE.EQ, BE.NE)
    ):
        operator_const = BE.IN

    return operator_const


def _neg_left(operator_const, left_operand, right_operand):
    expr = None
    if right_operand is None:
        expr = ~left_operand if operator_const == BE.NOT else left_operand

    return expr


def get_empty_filter_expression(attr):
    """Возвращает выражение для фильтрации.

    Возвращает выражение для фильтрации, если значение для фильтрации не пустое.

    Args:
        attr: Атрибут, по которому проходит фильтрация.

    Returns:
        Boolean expression или None.
    """

    def expression(value):
        return BE(attr, BE.IN, value) if list(filter(None, value)) else None

    return expression
