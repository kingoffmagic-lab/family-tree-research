import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import ROOT,audit
from demo import create
from init_case import initialize
from build_results import build
from export_gedcom import export
from result_view import build_view
from validate_catalogue import validate,check_url
from search_catalogue import search

class Workflow(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.case=create(Path(self.tmp.name)/'case')
    def tearDown(self):self.tmp.cleanup()
    def test_demo_audits(self):self.assertEqual(audit(self.case)['errors'],[])
    def test_no_reinitialization(self):
        before=(self.case/'person-register.csv').read_bytes()
        with self.assertRaises(ValueError):initialize(self.case,'overwrite')
        self.assertEqual(before,(self.case/'person-register.csv').read_bytes())
    def test_internal_destination_rejected(self):
        with self.assertRaises(ValueError):initialize(ROOT/'cases'/'test','test')
    def test_symlink_destination_rejected(self):
        path=Path(self.tmp.name)/'link';path.symlink_to(ROOT,target_is_directory=True)
        with self.assertRaises(ValueError):initialize(path/'new-case','test')
    def test_public_and_private_views(self):
        self.assertEqual(len(build_view(self.case)['people']),3)
        self.assertEqual(len(build_view(self.case,True)['people']),4)
    def test_html_filters_embedded_data_and_is_offline(self):
        paths=build(self.case)
        text=paths[0].read_text()
        self.assertNotIn('Private Teaching Person',text)
        self.assertNotIn('P-0004',text)
        self.assertIn('connect-src',text)
        self.assertIn('application/json',text)
    def test_output_overwrite_requires_flag(self):
        build(self.case)
        with self.assertRaises(ValueError):build(self.case)
    def test_hidden_root_rejected(self):
        with self.assertRaises(ValueError):build_view(self.case,root_person='P-0004')
    def test_gedcom_preserves_uncertainty(self):
        text=export(self.case,self.case/'output/tree.ged').read_text()
        self.assertIn('1 GEDC',text);self.assertIn('1 HUSB @I2@',text)
        self.assertIn('Unasserted parent-of',text);self.assertNotIn('Private Teaching Person',text)
        self.assertEqual(text.count('0 @F'),1)
    def test_originals_are_protected(self):
        with self.assertRaises(ValueError):build(self.case,self.case/'originals',overwrite=True)
        with self.assertRaises(ValueError):export(self.case,self.case/'sources/file.ged',overwrite=True)
    def test_script_injection_is_inert(self):
        from build_results import document
        view=build_view(self.case)
        view['people'][0]['name']='</script><script>alert(1)</script>'
        text=document(view)
        self.assertNotIn('</script><script>alert(1)',text)
        self.assertIn('\\u003c/script',text)
    def test_catalogue_integrity(self):self.assertEqual(validate(),[])
    def test_unsafe_url_rejected(self):
        for url in ['https://example.org/?token=secret','https://user:password@example.org/','file:///private/case']:
            self.assertFalse(check_url(url))
    def test_historical_lookup_does_not_invent_custody(self):
        result=search('Тверь',year=1890)
        self.assertTrue(result['results']);self.assertFalse(result['year_used_as_filter'])
        self.assertTrue(result['historical_routes'])

if __name__=='__main__':unittest.main()
