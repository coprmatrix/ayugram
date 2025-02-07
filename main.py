from specfile import Specfile as SpecFile
import sys
import subprocess
import os
from os.path import join
import tarfile

cwd = os.getcwd()
cutedir = join(cwd, '64gramdir')
cutedir = join(cutedir, '64Gram')

with tarfile.open(sys.argv[1], 'r:gz') as tar:
  tar.extractall(path=cwd)

# Usage
specfile = SpecFile(join(cutedir, '64Gram.spec'))
patchdir = {}

with specfile.patches() as patches:
  b = len(patches)
  for i in range(b):
    i = patches[i]
    patchdir[i.number] = i.expanded_filename


for i in sorted(patchdir):
  file_path = join(cutedir, patchdir[i])
  if os.path.exists(file_path):
    subprocess.run(['patch', cwd, '-i', file_path])

