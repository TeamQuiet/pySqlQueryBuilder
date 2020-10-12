#
# Author        Zirbs, Janus
# Date          2020-10-11
#

from enum import Enum

# Generic

class Node:

    def __init__(self):
        pass

    def acceptVisitor(self, visitor):
        raise Exception("Accept Visitor is not implemented")

# Expressions

class Expression(Node):

    def __init__(self):
        Node.__init__(self)

class Reference(Expression):

    def __init__(self, val: str = "", alias: str = None):
        Expression.__init__(self)
        self.__value = val
        self.__alias = alias

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, val: str):
        self.__value = val

    @property
    def alias(self) -> str:
        return self.__alias

    @alias.setter
    def alias(self, alias: str):
        self.__alias = alias

    def acceptVisitor(self, visitor):
        return visitor.visitReference(self)

class ReferenceList(Node):

    def __init__(self):
        Node.__init__(self)
        self.__iterator = -1
        self.__references = []

    def add(self, ref: Reference):
        if not any(_.value == ref.value for _ in self.__references):
            self.__references.append(ref)

    def remove(self, ref: Reference):
        for _ in self.__references:
            if _.value == ref.value:
                self.__references.remove(_)
                break

    def __iter__(self):
        self.__iterator = -1
        return self

    def __next__(self) -> Reference:
        if self.__iterator + 1 >= len(self.__references):
            raise StopIteration
        self.__iterator = self.__iterator + 1
        return self.__references[self.__iterator]

class StringValue(Expression):

    def __init__(self, val: str = ""):
        Expression.__init__(self)
        self.__value = val

    def get(self) -> str:
        return self.__value
    
    def set(self, val: str):
        self.__value = val

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, val: str):
        self.__value = val

    def acceptVisitor(self, visitor):
        return visitor.visitStringValue(self)

class NumericValue(Expression):

    def __init__(self, val: float = 0.0):
        Expression.__init__(self)
        self.__value = val

    def get(self) -> float:
        return self.__value
    
    def set(self, val: float):
        self.__value = val

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, val: float):
        self.__value = val

    def acceptVisitor(self, visitor):
        return visitor.visitNumericValue(self)

class Logic(Expression):

    def __init__(self):
        Expression.__init__(self)

class LogicNode(Logic):

    def __init__(self, left: Expression = None, right: Expression = None):
        Logic.__init__(self)
        self.__leftNode = left
        self.__rightNode = right

    @property
    def left(self) -> Expression:
        return self.__leftNode

    @left.setter
    def left(self, node: Expression):
        self.__leftNode = node

    @property
    def right(self) -> Expression:
        return self.__rightNode

    @right.setter
    def right(self, node: Expression):
        self.__rightNode = node

class And(LogicNode):

    def __init__(self, left: Expression = None, right: Expression = None):
        LogicNode.__init__(self, left, right)

    def acceptVisitor(self, visitor):
        return visitor.visitAnd(self)

class Or(LogicNode):

    def __init__(self, left: Expression = None, right: Expression = None):
        LogicNode.__init__(self, left, right)

    def acceptVisitor(self, visitor):
        return visitor.visitOr(self)

class Equal(LogicNode):

    def __init__(self, left: Expression = None, right: Expression = None):
        LogicNode.__init__(self, left, right)

    def acceptVisitor(self, visitor):
        return visitor.visitEqual(self)

class Unequal(LogicNode):

    def __init__(self, left: Expression = None, right: Expression = None):
        LogicNode.__init__(self, left, right)

    def acceptVisitor(self, visitor):
        return visitor.visitUnequal(self)

class Greater(LogicNode):

    def __init__(self, left: Expression = None, right: Expression = None):
        LogicNode.__init__(self, left, right)

    def acceptVisitor(self, visitor):
        return visitor.visitGreater(self)

class Less(LogicNode):

    def __init__(self, left: Expression = None, right: Expression = None):
        LogicNode.__init__(self, left, right)

    def acceptVisitor(self, visitor):
        return visitor.visitLess(self)

# Options

class Option(Node):

    def __init__(self):
        Node.__init__(self)

class JoinType(Enum):
    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"

class Join(Option):

    def __init__(self, reference: Reference = None, join_type: JoinType = JoinType.INNER, experssion: Expression = None):
        Option.__init__(self)
        self.__reference = reference
        self.__type = join_type
        self.__condition = experssion

    @property
    def reference(self):
        return self.__reference

    @reference.setter
    def reference(self, val: Reference):
        self.__reference = val

    def setJoin(self, join_type: JoinType):
        self.__type = join_type

    def isJoin(self, join_type: JoinType) -> bool:
        return self.__type == join_type

    @property
    def condition(self) -> Expression:
        return self.__condition

    @condition.setter
    def condition(self, condition: Expression):
        self.__condition = condition

    def acceptVisitor(self, visitor):
        return visitor.visitJoin(self)

class JoinList(Node):

    def __init__(self):
        Node.__init__(self)
        self.__iterator = -1
        self.__joins = []

    def add(self, join: Join):
        if not any(_.value == join.value for _ in self.__joins):
            self.__joins.append(join)

    def remove(self, join: Join):
        for _ in self.__joins:
            if _.value == join.value:
                self.__joins.remove(_)
                break

    def __iter__(self):
        self.__iterator = -1
        return self

    def __next__(self) -> Join:
        if self.__iterator + 1 >= len(self.__joins):
            raise StopIteration
        self.__iterator = self.__iterator + 1
        return self.__joins[self.__iterator]

class Page(Option):

    def __init__(self, index: int = 0, size: int = 0):
        Option.__init__(self)
        self.__page = index
        self.__size = size

    @property
    def index(self) -> int:
        return self.__page

    @index.setter
    def index(self, val: int) -> int:
        self.__page = val

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, val: int) -> int:
        self.__size = val

    def acceptVisitor(self, visitor):
        return visitor.visitPage(self)

class OrderType(Enum):
    ASC = "asc"
    DESC = "desc"

class Order(Option):

    def __init__(self, ref: Reference = None, order: JoinType = OrderType.ASC):
        Option.__init__(self)
        self.__order = order
        self.__reference = ref

    def setOrder(self, order_type: OrderType):
        self.__order = order_type

    def isOrder(self, order_type: OrderType) -> bool:
        return self.__order == order_type

    @property
    def reference(self):
        return self.__reference

    @reference.setter
    def reference(self, reference: Reference):
        self.__reference = reference

    def acceptVisitor(self, visitor):
        return visitor.visitOrder(self)

class Condition(Option):

    def __init__(self, expression: Expression = None):
        Option.__init__(self)
        self.__expression = expression

    @property
    def expression(self) -> Expression:
        return self.__expression

    @expression.setter
    def expression(self, expression: Expression):
        self.__expression = expression

    def acceptVisitor(self, visitor):
        return visitor.visitCondition(self)

# Statements

class Statement:

    def __init__(self):
        pass

class Select(Statement):

    def __init__(self):
        Statement.__init__(self)
        self.__order = None
        self.__condition = Condition(NumericValue(1))
        self.__fields = ReferenceList()
        self.__tables = ReferenceList()
        self.__joins = JoinList()
        self.__page = None

    @property
    def condition(self) -> Condition:
        return self.__condition

    @condition.setter
    def condition(self, condition: Condition):
        self.__condition = condition

    @property
    def fields(self) -> ReferenceList:
        return self.__fields

    @property
    def tables(self) -> ReferenceList:
        return self.__tables

    @property
    def joins(self) -> JoinList:
        return self.__joins

    @property
    def order(self) -> Order:
        return self.__order

    @order.setter
    def order(self, order: Order):
        self.__order = order

    @property
    def page(self) -> Page:
        return self.__page

    @page.setter
    def page(self, page: Page):
        self.__page = page

    def acceptVisitor(self, visitor):
        return visitor.visitSelect(self)

# Builder

class Builder:

    # Expressions

    def visitReference(self, node: Reference):
        raise Exception("QueryBuilder: Missing visitReference implementation")

    def visitStringValue(self, node: StringValue):
        raise Exception("QueryBuilder: Missing visitStringValue implementation")

    def visitNumericValue(self, node: NumericValue):
        raise Exception("QueryBuilder: Missing visitNumericValue implementation")

    def visitAnd(self, node: And):
        raise Exception("QueryBuilder: Missing visitAnd implementation")

    def visitOr(self, node: Or):
        raise Exception("QueryBuilder: Missing visitOr implementation")

    def visitEqual(self, node: Equal):
        raise Exception("QueryBuilder: Missing visitEqual implementation")
    
    def visitUnequal(self, node: Equal):
        raise Exception("QueryBuilder: Missing visitEqual implementation")
    
    def visitGreater(self, node: Equal):
        raise Exception("QueryBuilder: Missing visitGreater implementation")
    
    def visitLess(self, node: Equal):
        raise Exception("QueryBuilder: Missing visitLess implementation")

    # Query Options

    def visitJoin(self, node: Join):
        raise Exception("QueryBuilder: Missing visitJoin implementation")

    def visitPage(self, node: Page):
        raise Exception("QueryBuilder: Missing visitPage implementation")

    def visitOrder(self, node: Order):
        raise Exception("QueryBuilder: Missing visitOrder implementation")

    def visitCondition(self, node: Condition):
        raise Exception("QueryBuilder: Missing visitCondition implementation")

    # Statements

    def visitSelect(self, node: Select):
        raise Exception("QueryBuilder: Missing visitSelect implementation")

    # Generic

    def build(self, node):
        return node.acceptVisitor(self)