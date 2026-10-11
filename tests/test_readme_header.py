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

    def test_canonical_links_are_html_anchors(self):
        self.assertEqual(len(br.LINKS), 5)
        for label, url in br.LINKS.items():
            with self.subTest(label=label, url=url):
                self.assertIn(f'<a href="{url}">{label}</a>', self.text)
        links_lines = [
            line for line in self.text.splitlines()
            if all(url in line for url in br.LINKS.values())
        ]
        self.assertEqual(len(links_lines), 1)
        line = links_lines[0]
        self.assertTrue(line.startswith("<p "))
        self.assertIn("</p>", line)
        self.assertEqual(line.count("<a href="), 5)
        self.assertNotIn("](", line)


if __name__ == "__main__":
    unittest.main()
