import tempfile, unittest
from pathlib import Path
from file_processing_toolkit.cli import main

class CliTests(unittest.TestCase):
    def test_scan_and_rename_preview(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,"a.txt").write_text("x")
            self.assertEqual(main(["scan",d,"--json"]),0)
            self.assertEqual(main(["rename",d,"--prefix","safe-"]),0)
            self.assertTrue(Path(d,"a.txt").exists())
    def test_missing_path(self): self.assertEqual(main(["scan","/path/that/does/not/exist"]),2)

if __name__=="__main__": unittest.main()
