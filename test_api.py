# Import unittest for writing test cases
import unittest

# Import the function to test
from wikipedia_api import fetch_revisions

# Define a test class that inherits from unittest.TestCase
class TestWikipediaAPI(unittest.TestCase):

    # Test that a valid article returns revision data
    def test_valid_article(self):
        result = fetch_revisions("Ball State University")
        self.assertIn("revisions", result)  # Check that revisions are present
        self.assertLessEqual(len(result["revisions"]), 30)  # Should be 30 or fewer

    # Test that a fake article name raises a ValueError
    def test_missing_article(self):
        with self.assertRaises(ValueError):
            fetch_revisions("ThisPageDoesNotExist123456")

# Run the tests if this file is executed directly
if __name__ == "__main__":
    unittest.main()