import json
import unittest

from src.ZJountries import get_place

class TestBy(unittest.TestCase):
	def test_module(self):
		self.assertEqual(
			get_place(by='name', value='poland', fields='name'), 
			[{"name": {"common": "Poland", "official": "Republic of Poland", "native": {"polish": "Rzeczpospolita Polska"}}}]
      	)

if __name__ == '__main__':
    unittest.main()