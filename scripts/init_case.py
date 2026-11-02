#!/usr/bin/env python3
"""Initialize an external private case using the pinned upstream templates."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from common import ROOT, UPSTREAM, outside_toolkit, fail

def initialize(destination, question, label=''):
    case = outside_toolkit(destination)
    if case.exists():
        raise ValueError('Destination exists. Resume it, or choose a new empty destination; no files were changed.')
    case.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.kinship-init-', dir=str(case.parent)) as tmp:
        staged = Path(tmp) / 'case'
        result = subprocess.run([sys.executable, str(UPSTREAM / 'scripts/init_case.py'),
                                 '--case-dir', str(staged), '--research-question', question,
                                 '--subject-label', label], capture_output=True, text=True)
        if result.returncode:
            raise ValueError(result.stderr or result.stdout)
        intake = staged / 'case-intake.yaml'
        content = intake.read_text(encoding='utf-8')
        content = content.replace('case_id: "case"', 'case_id: ' + json.dumps(case.name, ensure_ascii=False), 1)
        intake.write_text(content, encoding='utf-8')
        for name in ('originals', 'sources', 'work', 'output', 'plan'):
            (staged / name).mkdir(exist_ok=True)
        for source, dest in [('BOARD.md', 'plan/BOARD.md'), ('task.md', 'plan/task-template.md'),
                             ('handoff.md', 'plan/handoff-template.md'), ('blocked.md', 'plan/blocked.md')]:
            shutil.copyfile(ROOT / 'templates' / source, staged / dest)
        pointer = json.dumps(str(ROOT), ensure_ascii=False)
        (staged / 'AGENTS.md').write_text(
            '# Private family-history case\n\nToolkit location: ' + pointer + '\n\n'
            'Read the toolkit SKILL.md entry point before research. '
            'If the toolkit moved, use the currently loaded skill root instead of this location hint. '
            'The project policy overrides the upstream CAPTCHA, sending, and upload defaults.\n\n'
            'Canonical CSV registers are in this case root. Read research-state.md and plan/BOARD.md '
            'before continuing. Save originals unchanged. Write task proposals in work/<task-id>/; '
            'one integrator updates registers after reviewing the handoff.\n', encoding='utf-8')
        (staged / 'CLAUDE.md').write_text('Read AGENTS.md in this case for the research entry point and resume instructions.\n', encoding='utf-8')
        (staged / 'toolkit.json').write_text(json.dumps({'toolkit_path': str(ROOT), 'schema_version': 1}, indent=2)+'\n', encoding='utf-8')
        # rename is atomic and refuses a populated destination on supported local filesystems.
        if case.exists():
            raise ValueError('Destination appeared during initialization; no existing files were changed.')
        staged.chmod(0o700)
        staged.rename(case)
    return case

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case-dir', required=True)
    parser.add_argument('--research-question', required=True)
    parser.add_argument('--subject-label', default='')
    args = parser.parse_args()
    try:
        print(initialize(args.case_dir, args.research_question, args.subject_label))
        return 0
    except (ValueError, OSError) as error:
        return fail(error)

if __name__ == '__main__':
    raise SystemExit(main())
