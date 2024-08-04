"""checks for Object Calisthenics rule 8: Only two instance variables."""

# see https://pylint.readthedocs.io/en/latest/how_tos/custom_checkers.html
from pylint.checkers import BaseChecker


class TwoInstanceVariablesChecker(BaseChecker):
    """checks for number of instance variables."""

    # configuration section name
    name = "two-instance-variables"
    priority = -1
    msgs = {
        "R1281": (
            'More than two instance variables in class "%s"',
            "more-than-two-instance-variables",
            "Object Calisthenics Rule 8",
        ),
    }
    options = ()

    def evaluate_attributes(self, attributes):
        if any(attributes):
            return 0
        return 1

    def visit_classdef(self, node):
        """check number of class attributes"""
        attribute_count = 0

        for attr in node.instance_attrs:
            attribute_count += self.evaluate_attributes(
                node.instance_attr_ancestors(attr)
            )

        if attribute_count > 2:
            self.add_message(
                "more-than-two-instance-variables", node=node, args=(node.name,)
            )


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(TwoInstanceVariablesChecker(linter))
