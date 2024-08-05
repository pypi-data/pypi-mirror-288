import unittest

from src.postcode_parser_uk import UkPostcodeParser
from src.postcode_parser_uk.errors import PostCodeFormatError
from src.postcode_parser_uk.postcode import UKPostCode, SpecialUKPostCode


class TestRegexParsingHandler(unittest.TestCase):
    """Test the RegexParsingHandler class."""

    def setUp(self):
        """Set up the UkPostcodeParser instance for tests."""
        self.parser = UkPostcodeParser()

    def test_valid_postcodes(self):
        """Test valid postcodes."""
        postcodes = [
            ("SW1W 0NY", True),
            ("SW1W0NY", True),
            (" SW1W0NY  ", True),
            (" sw1w0ny  ", True),
            ("PO16 7GZ", True),
            ("PO167GZ", True),
            (" PO167GZ  ", True),
            (" po167gz  ", True),
            ("GU16 7HF", True),
            ("GU167HF", True),
            (" GU167HF  ", True),
            (" gu167hf  ", True),
            ("L1 8JQ", True),
            ("L18JQ", True),
            (" L18JQ ", True),
            (" l18jq ", True),
            (" SW1W0NY", True),
            ("SW1W0NY ", True),
            (" SW1W0NY ", True),
            ("sw1w 0ny", True),
            ("sw1W 0nY", True),
        ]
        for postcode, is_valid in postcodes:
            with self.subTest(postcode=postcode):
                result = self.parser.parse(postcode)
                self.assertEqual(result.is_valid, is_valid)
                self.assertIsInstance(result.value, UKPostCode)

    def test_invalid_postcodes(self):
        """Test invalid postcodes."""
        postcodes = [
            ("INVALID", False),
            ("123 ABC", False),
            ("ABCDE", False),
            ("", False),  # empty string
            (None, False),  # invalid type
            (12, False),  # invalid type
            ("@SW1W0NY", False),  # leading special character
            ("SW1W0NY@", False),  # trailing special character
            ("SW1W! 0NY", False),  # internal special character
            ("SW 1W 0NY", False),  # incorrect space
            ("S W1W0NY", False),  # incorrect space
            ("SW1W0N Y", False),  # incorrect space
            ("SW1W0 NY", False),  # incorrect space
            ("S@W1W0NY", False),  # special character
        ]
        for postcode, is_valid in postcodes:
            with self.subTest(postcode=postcode):
                result = self.parser.parse(postcode)
                self.assertEqual(result.is_valid, is_valid)
                self.assertIsInstance(result.error, PostCodeFormatError)

    def test_special_cases(self):
        """Test special cases."""
        special_cases = {
            "british_overseas_territories": [
                "ASCN 1ZZ",
                "ASCN1ZZ",
                " ASCN1ZZ",
                " aScN1zZ",
                "aScN1zZ ",
                "BBND 1ZZ",
                "BBND1ZZ",
                "BIQQ 1ZZ",
                "BIQQ1ZZ",
                "FIQQ 1ZZ",
                "FIQQ1ZZ",
                "GX11 1AA",
                "GX111AA",
                "PCRN 1ZZ",
                "PCRN1ZZ",
                "SIQQ 1ZZ",
                "SIQQ1ZZ",
                "STHL 1ZZ",
                "STHL1ZZ",
                "TDCU 1ZZ",
                "TDCU1ZZ",
                "TKCA 1ZZ",
                "TKCA1ZZ",
                "ascn 1zz",
                "ascn1zz",
                " ASCn1ZZ",
                " aScN1zZ",
                "ascn1zz ",
                "bbnd 1zz",
                "bbnd1zz",
                "biqq 1zz",
                "biqq1zz",
                "fiqq 1zz",
                "fiqq1zz",
                "gx11 1aa",
                "gx111aa",
                "pcrn 1zz",
                "pcrn1zz",
                "siqq 1zz",
                "siqq1zz",
                "sthl 1zz",
                "sthl1zz",
                "tdcu 1zz",
                "tdcu1zz",
                "tkca 1zz",
                "tkca1zz",
            ],
            "anguilla": ["AI-2640", "ai-2640", " Ai-2640 "],
            "cayman_islands": ["KY1-1102", "ky1-1102", " Ky1-1102 "],
            "montserrat": ["MSR-1234", "msr-1234", " Msr-1234 "],
            "british_virgin_islands": ["VG-1110", "vg-1110", " Vg-1110 "],
            "bermuda": ["HM12", "FL07", "hm12", "fl07", " Hm12 ", " Fl07 "],
            "bfpo": [
                "BFPO 801",
                "BFPO801",
                "bfpo 801",
                "bfpo801",
                " Bfpo 801 ",
                " Bfpo801 ",
            ],
            "non_geographic": [
                "GIR 0AA",
                "GIR0AA",
                "gir 0aa",
                "gir0aa",
                " Gir 0aa ",
                " Gir0aa ",
                "XM4 5HQ",
                "XM45HQ",
                "xm4 5hq",
                "xm45hq",
                " Xm4 5hq ",
                " Xm45hq ",
            ],
        }
        for case, postcodes in special_cases.items():
            for postcode in postcodes:
                with self.subTest(postcode=postcode):
                    result = self.parser.parse(postcode)
                    self.assertTrue(result.is_valid)
                    self.assertIsInstance(result.value, SpecialUKPostCode)
                    self.assertEqual(result.value.special_case, case)

    def test_formatting(self):
        """Test the extraction of area, district, sector, and unit."""
        postcodes = [
            ("SW1W 0NY", "SW", "1W", "0", "NY"),
            ("SW1W0NY", "SW", "1W", "0", "NY"),
            ("PO16 7GZ", "PO", "16", "7", "GZ"),
            ("PO167GZ", "PO", "16", "7", "GZ"),
            ("GU16 7HF", "GU", "16", "7", "HF"),
            ("GU167HF", "GU", "16", "7", "HF"),
            ("L1 8JQ", "L", "1", "8", "JQ"),
            ("L18JQ", "L", "1", "8", "JQ"),
        ]
        for postcode, area, district, sector, unit in postcodes:
            with self.subTest(postcode=postcode):
                result = self.parser.parse(postcode)
                self.assertTrue(result.is_valid)
                self.assertIsInstance(result.value, UKPostCode)
                self.assertEqual(result.value.area, area)
                self.assertEqual(result.value.district, district)
                self.assertEqual(result.value.sector, sector)
                self.assertEqual(result.value.unit, unit)


if __name__ == "__main__":
    unittest.main()
