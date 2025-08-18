import unittest
import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.price_from_mandi import PriceFromMandi

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class TestPriceFromMandi(unittest.TestCase):
    def test_get_price_minimal(self):
        """Test get_price with only required parameters."""
        price = self.price_plugin.get_price("Wheat", "Maharashtra", "Pune", "Pune")
        print(f"Minimal get_price response: {price}")
        self.assertIsInstance(price, (int, float))

    def test_get_price_with_variety(self):
        """Test get_price with variety parameter."""
        price = self.price_plugin.get_price("Onion", "Maharashtra", "Ahmednagar", "Rahata", variety="Red")
        print(f"get_price with variety response: {price}")
        self.assertIsInstance(price, (int, float))

    def test_get_price_with_grade(self):
        """Test get_price with grade parameter."""
        price = self.price_plugin.get_price("Potato", "Maharashtra", "Pune", "Pune", grade="A")
        print(f"get_price with grade response: {price}")
        self.assertIsInstance(price, (int, float))

    def test_get_price_with_limit_offset(self):
        """Test get_price with limit and offset parameters."""
        price = self.price_plugin.get_price("Onion", "Maharashtra", "Ahmednagar", "Rahata", limit=2, offset=1)
        print(f"get_price with limit/offset response: {price}")
        self.assertIsInstance(price, (int, float))

    def test_get_price_with_format_xml(self):
        """Test get_price with format xml (should fallback to 0 if not supported parsing)."""
        price = self.price_plugin.get_price("Wheat", "Maharashtra", "Pune", "Pune", format_='xml')
        print(f"get_price with format xml response: {price}")
        self.assertIsInstance(price, (int, float))

    def test_get_price_with_all_params(self):
        """Test get_price with all possible parameters."""
        price = self.price_plugin.get_price(
            "Onion", "Maharashtra", "Ahmednagar", "Rahata",
            variety="Red", grade="A", limit=2, offset=1, format_='json'
        )
        print(f"get_price with all params response: {price}")
        self.assertIsInstance(price, (int, float))

    def test_get_price_invalid_variety(self):
        """Test get_price with invalid variety (should return 0)."""
        price = self.price_plugin.get_price("Onion", "Maharashtra", "Ahmednagar", "Rahata", variety="InvalidVariety")
        print(f"get_price with invalid variety response: {price}")
        self.assertIn(price, [0, None])

    def test_get_price_invalid_grade(self):
        """Test get_price with invalid grade (should return 0)."""
        price = self.price_plugin.get_price("Potato", "Maharashtra", "Pune", "Pune", grade="InvalidGrade")
        print(f"get_price with invalid grade response: {price}")
        self.assertIn(price, [0, None])

    def test_get_price_invalid_format(self):
        """Test get_price with invalid format (should return 0)."""
        price = self.price_plugin.get_price("Wheat", "Maharashtra", "Pune", "Pune", format_='invalidformat')
        print(f"get_price with invalid format response: {price}")
        self.assertIn(price, [0, None])
    def test_raw_api_response_wheat(self):
        """Print and check raw API response for Wheat in Pune market"""
        api_client = self.price_plugin.api_client
        records = api_client(
            state="Maharashtra",
            district="Pune",
            commodity="Wheat",
            limit=1
        )
        print(f"Raw API response for Wheat in Pune market: {records}")
        self.assertIsInstance(records, list)

    def test_raw_api_response_onion(self):
        """Print and check raw API response for Onion in Rahata market"""
        api_client = self.price_plugin.api_client
        records = api_client(
            state="Maharashtra",
            district="Ahmednagar",
            commodity="Onion",
            limit=1
        )
        print(f"Raw API response for Onion in Rahata market: {records}")
        self.assertIsInstance(records, list)

    def test_raw_api_response_potato(self):
        """Print and check raw API response for Potato in Pune market"""
        api_client = self.price_plugin.api_client
        records = api_client(
            state="Maharashtra",
            district="Pune",
            commodity="Potato",
            limit=1
        )
        print(f"Raw API response for Potato in Pune market: {records}")
        self.assertIsInstance(records, list)
    def test_raw_api_response(self):
        """Print and check raw API response for Bengal Gram(Gram)(Whole) in Karjat market"""
        # Directly call the API client for raw response
        api_client = self.price_plugin.api_client
        records = api_client(
            state="Maharashtra",
            district="Ahmednagar",
            commodity="Bengal Gram(Gram)(Whole)",
            limit=1
        )
        print(f"Raw API response for Bengal Gram(Gram)(Whole) in Karjat market: {records}")
        self.assertIsInstance(records, list)
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
        """Should return a valid float price for Karjat market and Bengal Gram (price is dynamic)"""
        price = self.price_plugin.get_price("Onion", "Maharashtra", "Ahmednagar", "Karjat")
        print(f"Actual price response for Onion in Karjat market: {price}")
        self.assertIsInstance(price, (int, float))
        if price == 0:
            logging.warning("No price data found for Onion in Karjat market.")
        else:
            self.assertGreater(price, 0, "Price should be a positive number if data is available.")
    

if __name__ == "__main__":
    unittest.main()
