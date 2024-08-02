import unittest
from sys_info_api import common


class TestCommon(unittest.TestCase):
	def test_formatted_string_to_bytes(self):
		self.assertEqual(common.formatted_string_to_bytes('1 PB'), 1125899906842624)
		self.assertEqual(common.formatted_string_to_bytes('1 TB'), 1099511627776)
		self.assertEqual(common.formatted_string_to_bytes('1 GB'), 1073741824)
		self.assertEqual(common.formatted_string_to_bytes('1 MB'), 1048576)
		self.assertEqual(common.formatted_string_to_bytes('1 kB'), 1024)

		self.assertEqual(common.formatted_string_to_bytes('1P'), 1125899906842624)
		self.assertEqual(common.formatted_string_to_bytes('1T'), 1099511627776)
		self.assertEqual(common.formatted_string_to_bytes('1G'), 1073741824)
		self.assertEqual(common.formatted_string_to_bytes('1M'), 1048576)
		self.assertEqual(common.formatted_string_to_bytes('1k'), 1024)

		self.assertEqual(common.formatted_string_to_bytes('1 PB/s'), 1e15)
		self.assertEqual(common.formatted_string_to_bytes('1 TB/s'), 1e12)
		self.assertEqual(common.formatted_string_to_bytes('1 GB/s'), 1e9)
		self.assertEqual(common.formatted_string_to_bytes('1 MB/s'), 1e6)
		self.assertEqual(common.formatted_string_to_bytes('1 kB/s'), 1000)

		self.assertEqual(common.formatted_string_to_bytes('1 Pb/s'), 1.25e14)
		self.assertEqual(common.formatted_string_to_bytes('1 Tb/s'), 1.25e11)
		self.assertEqual(common.formatted_string_to_bytes('1 Gb/s'), 1.25e8)
		self.assertEqual(common.formatted_string_to_bytes('1 Mb/s'), 1.25e5)
		self.assertEqual(common.formatted_string_to_bytes('1 kb/s'), 125)

	def test_formatted_string_to_bits(self):
		# 10kB == 80k bits
		self.assertEqual(common.formatted_string_to_bits('10 KB/s'), 80000)
