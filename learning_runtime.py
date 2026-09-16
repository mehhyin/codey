"""Shared local interpreter setup for attempts and interactive project previews."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent.parent / 'work'


def configure():
    packages = WORK / 'pyroom-packages'
    if packages.is_dir():
        sys.path.insert(0, str(packages))
    sys.path.insert(0, str(Path.cwd()))
    config = WORK / 'pyroom-matplotlib'
    config.mkdir(parents=True, exist_ok=True)
    os.environ['MPLBACKEND'] = 'Agg'
    os.environ['MPLCONFIGDIR'] = str(config)
