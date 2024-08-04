"""Unit tests for Object Calisthenics rule 2: Don't use the ELSE keyword."""

import astroid
from pylint.testutils import CheckerTestCase
from pylint_calisthenics.no_else import NoElseChecker
from pylint.testutils.output_line import MessageTest


class TestNoElseChecker(CheckerTestCase):
    """Unit tests for the no-else checker."""

    CHECKER_CLASS = NoElseChecker

    def test_allow_if(self):
        """Test that if is left alone."""

        node = astroid.parse(
            """
        class IfSample(object):
            def __init__(self):
                self._a = 0

            def uses_else(self):
                self._a = 1
                if self._a > 1:
                    self._a = 1
        """
        )

        with self.assertNoMessages():
            self.walk(node.root())

    def test_find_else(self):
        """Test that else keyword is flagged."""

        node = astroid.parse(
            """
        class ElseSample(object):
            def __init__(self):
                self._a = 0

            def uses_else(self):
                self._a = 1
                if self._a > 1:
                    self._a = 1
                else:
                    self._a = 2
        """
        )

        class_def = list(node.get_children())[0]
        fun_def = class_def.body[1]
        if_def = fun_def.body[1]
        expected_message = MessageTest(
            "if-has-else",
            node=if_def,
            line=if_def.lineno,
            col_offset=if_def.col_offset,
            end_line=if_def.end_lineno,
            end_col_offset=if_def.end_col_offset,
        )
        with self.assertAddsMessages(expected_message):
            self.walk(node.root())
