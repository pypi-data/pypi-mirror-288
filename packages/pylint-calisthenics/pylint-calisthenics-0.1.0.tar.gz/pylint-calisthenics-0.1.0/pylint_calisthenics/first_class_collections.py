"""checks for Object Calisthenics rule 4: First class collections."""

import astroid
from pylint.checkers import BaseChecker


class FirstClassCollectionsChecker(BaseChecker):
    """checks for collection attributes to be the only field."""

    # configuration section name
    name = "first-class-collections"
    priority = -1
    msgs = {
        "R1241": (
            'Collection field in class "%s" must be first class',
            "collection-not-first-class",
            "Object Calisthenics Rule 4",
        ),
    }
    options = ()

    def visit_classdef(self, node):
        """check class attributes"""
        attribute_count = 0
        has_collection = False

        for attr, anodes in node.instance_attrs.items():
            if not any(node.instance_attr_ancestors(attr)):
                # print attr, '=', list(anodes[0].parent.get_children())[1]
                attribute_count += 1
                has_collection = has_collection or self._is_collection(anodes)

        if has_collection and attribute_count > 1:
            self.add_message("collection-not-first-class", node=node, args=(node.name,))

    def _is_collection(self, assign_nodes):  # pylint: disable=no-self-use
        assigned_values = [
            value
            for node in assign_nodes
            if not isinstance(
                value := list(node.parent.get_children())[1], astroid.node_classes.Const
            )
        ]

        collection_asts = [
            astroid.node_classes.List,  # []
            astroid.node_classes.Tuple,  # ()
            astroid.node_classes.Dict,
            astroid.scoped_nodes.ListComp,
            astroid.scoped_nodes.SetComp,
        ]

        for value in assigned_values:
            if isinstance(value, astroid.node_classes.Call):
                target = value.func
                if isinstance(target, astroid.node_classes.Name):
                    callee = target.name
                    if callee == "list" or callee == "set" or callee == "dict":
                        return True

            if any(
                isinstance(value, collection_ast) for collection_ast in collection_asts
            ):
                return True

        return False


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(FirstClassCollectionsChecker(linter))
