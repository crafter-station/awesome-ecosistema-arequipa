"""Tiny check: generated README has the keyword H1 and all canonical links."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_readme as br  # noqa: E402


class TestReadmeHeader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_h1_with_keywords(self):
        self.assertIn(f"# {br.H1}", self.text)

    def test_canonical_links(self):
        self.assertEqual(len(br.LINKS), 5)
        for url in br.LINKS.values():
            with self.subTest(url=url):
                self.assertIn(url, self.text)


if __name__ == "__main__":
    unittest.main()
