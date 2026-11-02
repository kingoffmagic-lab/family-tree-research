"""Exercise real commands from relocated, standalone skill distributions."""
import json,shutil,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class Portability(unittest.TestCase):
    def smoke(self,skill,base):
        unrelated=base/'unrelated working directory';unrelated.mkdir(exist_ok=True)
        case=base/'private case'
        def run(script,*args):
            result=subprocess.run([sys.executable,str(skill/'scripts'/script),*map(str,args)],cwd=unrelated,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr+result.stdout)
            return result
        run('validate_catalogue.py')
        run('render_catalogue.py','--check')
        run('demo.py','--case-dir',case)
        run('audit_evidence.py','--case-dir',case,'--json')
        run('build_results.py','--case-dir',case)
        run('export_gedcom.py','--case-dir',case,'--out',case/'output/tree.ged')
        lookup=json.loads(run('search_catalogue.py','--country','estonia','--json').stdout)
        self.assertTrue(lookup['results'])
        self.assertIn('SKILL.md',(case/'AGENTS.md').read_text())
        self.assertIn('AGENTS.md',(case/'CLAUDE.md').read_text())
        self.assertIn(str(skill), (case/'toolkit.json').read_text())
        self.assertTrue((case/'output/report.html').is_file())
        self.assertTrue((case/'output/tree.ged').is_file())
    def test_claude_and_codex_directory_layouts(self):
        for host in ('.claude','.agents'):
            with self.subTest(host=host),tempfile.TemporaryDirectory() as tmp:
                base=Path(tmp)
                skill=base/host/'skills/family-tree-research'
                shutil.copytree(ROOT,skill,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
                self.smoke(skill,base)
    def test_zip_distribution(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);archive=base/'skill.zip'
            with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
                for p in ROOT.rglob('*'):
                    if p.is_file() and not any(x in p.parts for x in ('.git','__pycache__')):
                        z.write(p,'family-tree-research/'+str(p.relative_to(ROOT)))
            with zipfile.ZipFile(archive) as z:z.extractall(base/'extracted')
            self.smoke(base/'extracted/family-tree-research',base)
    def test_root_entry_is_standard_and_small(self):
        entry=(ROOT/'SKILL.md').read_text()
        self.assertTrue(entry.startswith('---\nname: family-tree-research\n'))
        self.assertLess(len(entry.split()),900)
        self.assertNotIn('${CLAUDE_SKILL_DIR}',entry)
        for p in (ROOT/'AGENTS.md',ROOT/'CLAUDE.md'):
            self.assertIn('SKILL.md',p.read_text())

if __name__=='__main__':unittest.main()
