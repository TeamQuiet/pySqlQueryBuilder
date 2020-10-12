from . import query

class Builder(query.Builder):

    def __init__(self):
        query.Builder.__init__(self)

    # Expressions

    def visitReference(self, node: query.Reference):
        if node.alias is not None and len(node.alias) > 0:
            qstr = "{} as {}".format(node.value, node.alias)
        else:
            qstr = node.value   
        return qstr

    def visitStringValue(self, node: query.StringValue):
        return str(node.get())

    def visitNumericValue(self, node: query.NumericValue):
        return str(node.get())

    def visitAnd(self, node: query.And):
        return node.left.acceptVisitor(self) + " and " + node.right.acceptVisitor(self)

    def visitOr(self, node: query.Or):
        return node.left.acceptVisitor(self) + " or " + node.right.acceptVisitor(self)

    def visitEqual(self, node: query.Equal):
        return node.left.acceptVisitor(self) + " = " + node.right.acceptVisitor(self)

    # Query Options

    def visitJoin(self, node: query.Join):
        join_key = "inner"
        if node.isJoin(query.JoinType.INNER): join_key = "inner"
        elif node.isJoin(query.JoinType.LEFT): join_key = "left"
        else: join_key = "right"
        return "{} join {} on ({})".format(join_key, node.reference.acceptVisitor(self), node.condition.acceptVisitor(self))

    def visitPage(self, node: query.Page):
        return "limit {limit} offset {offset}".format(
            offset=node.size * node.index,
            limit=node.size
        )

    def visitOrder(self, node: query.Order):
        order_key = ""
        if node.isOrder(query.OrderType.ASC): order_key = "asc"
        else: order_key = "desc"
        return "order by {} {}".format(node.reference.get(), order_key)

    def visitCondition(self, node: query.Condition):
        return "where " + node.expression.acceptVisitor(self)

    # Statements

    def visitSelect(self, node: query.Select):
        return "select {fields} from {tables} {joins} {condition} {order} {page}".format(
            fields=     ", ".join([ _.acceptVisitor(self) for _ in node.fields]),
            tables=     ", ".join([ _.acceptVisitor(self) for _ in node.tables]),
            joins=      " ".join([_.acceptVisitor(self) for _ in node.joins]),
            condition=  node.condition.acceptVisitor(self) if node.condition is not None else "",
            order=      node.order.acceptVisitor(self) if node.order is not None else "",
            page=       node.page.acceptVisitor(self) if node.page is not None else ""
        )

