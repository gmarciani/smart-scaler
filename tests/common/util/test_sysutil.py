from services.common.util import sysutil
import unittest


class SysUtilTestCase(unittest.TestCase):

    def test_json(self):
        """
        Test the function import.
        :return: None
        """
        from services.common.util.mathutil import get_bounded

        DEFAULT_FUNCTION = get_bounded

        func_expressions = [DEFAULT_FUNCTION,
                            DEFAULT_FUNCTION.__module__ + "." + DEFAULT_FUNCTION.__name__,
                            get_bounded, lambda low, high, value: max(low, min(high, value))]

        class MyClass:
            def __init__(self, func=None):
                self.exec = sysutil.import_string(func) if isinstance(func, str) else func

            def bar(self, val):
                return self.exec(1, 10, val)

        for func_expression in func_expressions:
            obj = MyClass(DEFAULT_FUNCTION)
            actual = obj.bar(5)
            expected = 5
            self.assertEqual(expected, actual, "Error with function expression {}".format(func_expression))


if __name__ == "__main__":
    unittest.main()
