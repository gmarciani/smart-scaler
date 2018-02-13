from services.common.util import sysutil
import unittest


class SysUtilTestCase(unittest.TestCase):

    def test_json_function(self):
        """
        Test the function import from JSON.
        :return: None
        """
        from services.common.util.mathutil import get_bounded

        DEFAULT_FUNCTION = get_bounded

        func_expressions = [DEFAULT_FUNCTION,
                            DEFAULT_FUNCTION.__module__ + "." + DEFAULT_FUNCTION.__name__,
                            get_bounded, lambda low, high, value: max(low, min(high, value))
                            ]

        class MyClass:
            def __init__(self, func=DEFAULT_FUNCTION):
                self.exec = sysutil.import_string(func) if isinstance(func, str) else func

            def bar(self, val):
                return self.exec(1, 10, val)

        for func_expression in func_expressions:
            obj = MyClass(DEFAULT_FUNCTION)
            actual = obj.bar(5)
            expected = 5
            self.assertEqual(expected, actual, "Error with function expression {}".format(func_expression))

    def test_json_enumeration(self):
        """
        Test the enumeration import from JSON.
        :return: None
        """
        from services.common.model.ai.ai_techniques import AITechnique

        DEFAULT_ENUM_VALUE = AITechnique.QLEARNING

        enum_value_expressions = [DEFAULT_ENUM_VALUE,
                                  DEFAULT_ENUM_VALUE.__module__ + "." + DEFAULT_ENUM_VALUE.__class__.__name__ + "." + DEFAULT_ENUM_VALUE.name,
                                  ]

        class MyClass:
            def __init__(self, enum_value=DEFAULT_ENUM_VALUE):
                self.enum_value = sysutil.import_string(enum_value) if isinstance(enum_value, str) else enum_value

        for enum_value_expression in enum_value_expressions:
            obj = MyClass(enum_value_expression)
            actual = obj.enum_value
            expected = AITechnique.QLEARNING
            self.assertEqual(expected, actual, "Error with enum value expression {}".format(enum_value_expression))


if __name__ == "__main__":
    unittest.main()
