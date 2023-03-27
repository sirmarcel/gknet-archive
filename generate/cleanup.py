from pathlib import Path
import shutil

start = Path("../")

for p in start.rglob("*.py[co]"):
    p.unlink()

for p in start.rglob("*.DS_Store"):
    p.unlink()


for p in start.rglob("__pycache__"):
    shutil.rmtree(p)
