import unittest
from dataclasses import dataclass
from numbers import Number
from typing import Union

from calculator import Calculator


@dataclass
class TestCase:
    args: Union[tuple, Number]
    want: Union[Number, Exception]


class ApplicationTest(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        test_cases = [
            TestCase(args=(1, 1), want=2),
            TestCase(args=(-1, -1), want=-2),
            TestCase(args=(-1, 1), want=0),
            TestCase(args=(100, 200), want=300),
            TestCase(args=(500, -100), want=400),
        ]

        for test_case in test_cases:
            ret = self.calculator.add(*test_case.args)
            self.assertEqual(test_case.want, ret)

        error_test_case = TestCase(args=("1", 1), want=TypeError)
        with self.assertRaises(error_test_case.want):
            ret = self.calculator.add(*error_test_case.args)

    def test_divide(self):
        test_cases = [
            TestCase(args=(1, 1), want=1),
            TestCase(args=(-1, -1), want=1),
            TestCase(args=(-1, 1), want=-1),
            TestCase(args=(100, 200), want=0.5),
            TestCase(args=(500, -100), want=-5),
        ]

        for test_case in test_cases:
            ret = self.calculator.divide(*test_case.args)
            self.assertAlmostEqual(test_case.want, ret)

        error_test_case = TestCase(args=(1, 0), want=ZeroDivisionError)
        with self.assertRaises(error_test_case.want):
            ret = self.calculator.divide(*error_test_case.args)

    def test_sqrt(self):
        test_cases = [
            TestCase(args=1, want=1),
            TestCase(args=4, want=2),
            TestCase(args=25, want=5),
            TestCase(args=0.25, want=0.5),
            TestCase(args=100, want=10),
        ]

        for test_case in test_cases:
            ret = self.calculator.sqrt(test_case.args)
            self.assertAlmostEqual(test_case.want, ret, delta=1e-3)

        error_test_case = TestCase(args=-1, want=TypeError)
        with self.assertRaises(error_test_case.want):
            ret = self.calculator.sqrt(*error_test_case.args)

    def test_exp(self):
        test_cases = [
            TestCase(args=1, want=2.71828),
            TestCase(args=3, want=20.0855),
            TestCase(args=-1, want=0.36787),
            TestCase(args=0.5, want=1.64872),
            TestCase(args=-100, want=0),
        ]

        for test_case in test_cases:
            ret = self.calculator.exp(test_case.args)
            self.assertAlmostEqual(test_case.want, ret, delta=1e-3)

        error_test_case = TestCase(args=1e10, want=OverflowError)
        with self.assertRaises(error_test_case.want):
            ret = self.calculator.exp(error_test_case.args)


if __name__ == "__main__":
    unittest.main()
