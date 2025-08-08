import unittest
import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.price_from_mandi import PriceFromMandi

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class TestPriceFromMandi(unittest.TestCase):
    def setUp(self):
        self.price_plugin = PriceFromMandi()

    def log_result(self, name, result):
        status = "✅ PASS" if result else "❌ FAIL"
        logging.info(f"{name}: {status}")

    def test_missing_commodity(self):
        name = "Test: Missing commodity"
        try:
            price = self.price_plugin.get_price("", "Maharashtra", "Pune", "Pune")
            self.assertEqual(price, 0)
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_missing_state(self):
        name = "Test: Missing state"
        try:
            price = self.price_plugin.get_price("Wheat", "", "Pune", "Pune")
            self.assertEqual(price, 0)
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_missing_district(self):
        name = "Test: Missing district"
        try:
            price = self.price_plugin.get_price("Wheat", "Maharashtra", "", "Pune")
            self.assertEqual(price, 0)
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_missing_market(self):
        name = "Test: Missing market"
        try:
            price = self.price_plugin.get_price("Wheat", "Maharashtra", "Pune", "")
            self.assertEqual(price, 0)
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_invalid_commodity(self):
        name = "Test: Invalid commodity"
        try:
            price = self.price_plugin.get_price("InvalidItemXYZ", "Maharashtra", "Pune", "Pune")
            self.assertEqual(price, 0)
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_case_insensitivity(self):
        name = "Test: Case insensitivity"
        try:
            price = self.price_plugin.get_price("wHeAt", "maharashtra", "pune", "pune")
            self.assertIsInstance(price, (int, float))
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_valid_query(self):
        name = "Test: Valid query (Onion - Rahata)"
        try:
            price = self.price_plugin.get_price("Onion", "Maharashtra", "Ahmednagar", "Rahata")
            self.assertIsInstance(price, (int, float))
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise

    def test_rare_query_no_data(self):
        name = "Test: Rare query (Dragon Fruit - Dimapur)"
        try:
            price = self.price_plugin.get_price("Dragon Fruit", "Nagaland", "Dimapur", "Dimapur")
            self.assertIn(price, [0, None])
            self.log_result(name, True)
        except Exception:
            self.log_result(name, False)
            raise
    def test_karjat_bengal_gram_price(self):
        """Should return correct modal price for Karjat market and Bengal Gram"""
        price = self.price_plugin.get_price("Bengal Gram(Gram)(Whole)", "Maharashtra", "Ahmednagar", "Karjat")
        self.assertEqual(price, 5100.0)
    

if __name__ == "__main__":
    unittest.main()
