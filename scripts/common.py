"""Shared paths and CSV helpers; Python 3.9+, standard library only."""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'vendor' / 'ex-ussr-kinship-research'

def read_json(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'archive_defaults' in data:
        data['archives'] = [{**data['archive_defaults'], **row} for row in data['archives']]
    if isinstance(data, dict) and 'verification_sources' in data:
        for row in data['archives']:
            row['verification'] = data['verification_sources'][row['verification_id']]
    for key in ('region_defaults', 'coverage_defaults'):
        if isinstance(data, dict) and key in data:
            data['regions'] = [{**data[key], **row} for row in data['regions']]
    return data

def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def table(case, name):
    with (Path(case) / (name + '-register.csv')).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def ids(text):
    return [s.strip() for s in re.split(r'[;|,]', text or '') if s.strip()]

def outside_toolkit(path):
    path = Path(path).expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError('Private cases and generated results must be outside the toolkit checkout.')
    return path

def audit(case):
    result = subprocess.run([sys.executable, str(UPSTREAM / 'scripts/audit_evidence.py'),
                             '--case-dir', str(case), '--json'], capture_output=True, text=True)
    if not result.stdout.strip():
        raise ValueError(result.stderr.strip() or 'Upstream evidence audit failed.')
    data = json.loads(result.stdout)
    if data.get('errors'):
        raise ValueError('Fix evidence audit errors first:\n' + '\n'.join(data['errors']))
    return data

def fail(message):
    print('Error: ' + str(message), file=sys.stderr)
    return 2
