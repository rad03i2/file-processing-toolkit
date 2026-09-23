import tempfile, unittest
from pathlib import Path
from file_processing_toolkit.core import scan, hash_file, find_duplicates, plan_rename, apply_rename

class ToolkitTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.root=Path(self.t.name)
    def tearDown(self): self.t.cleanup()
    def test_scan_filters_and_unicode(self):
        (self.root/"مرحبا.txt").write_text("hello",encoding="utf-8"); (self.root/"x.bin").write_bytes(b"12")
        rows=scan(self.root,extension="txt",min_size=5)
        self.assertEqual(len(rows),1); self.assertTrue(rows[0].path.endswith("مرحبا.txt"))
    def test_hash_known_value(self):
        p=self.root/"a"; p.write_bytes(b"abc")
        self.assertEqual(hash_file(p),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    def test_duplicates_verify_content(self):
        (self.root/"a").write_bytes(b"same"); (self.root/"b").write_bytes(b"same"); (self.root/"c").write_bytes(b"diff")
        self.assertEqual(len(find_duplicates(self.root)),1)
    def test_rename_preview_and_apply(self):
        (self.root/"z.txt").write_text("z"); (self.root/"a.txt").write_text("a")
        plan=plan_rename(self.root,prefix="doc-",width=2); self.assertEqual(len(plan),2)
        apply_rename(plan); self.assertTrue((self.root/"doc-01.txt").exists()); self.assertTrue((self.root/"doc-02.txt").exists())
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): scan(self.root,min_size=-1)
        with self.assertRaises(ValueError): hash_file(__file__,"not-a-hash")

if __name__=="__main__": unittest.main()
