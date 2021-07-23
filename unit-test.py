import unittest
from stock_prices import fetchStockData
import io
import sys


class TestFileName(unittest.TestCase):
    def test_function1(self):
        symbol = 'AAPL'
        self.assertTrue(fetchStockData(symbol), None)


if __name__ == '__main__':
    unittest.main()
