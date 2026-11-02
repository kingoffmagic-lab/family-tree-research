#!/usr/bin/env python3
"""Forward arguments to the unmodified, pinned evidence auditor."""
import subprocess
import sys
from common import UPSTREAM

if __name__ == '__main__':
    raise SystemExit(subprocess.call([sys.executable, str(UPSTREAM / 'scripts/audit_evidence.py'), *sys.argv[1:]]))
