import unittest
from max_flow import MaxFlowCalculator


class TestMaxFlowCalculator(unittest.TestCase):
    def test_max_flow_from_csv(self):
        calculator = MaxFlowCalculator()
        calculator.read_csv("roads.csv")
        result = calculator.edmonds_karp()
        self.assertEqual(result, 17)


if __name__ == "__main__":
    unittest.main()
