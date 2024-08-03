import sys
from os import execl
from pathlib import Path


def restart():
    print(sys.executable, *sys.argv)
    p = Path(sys.argv[0])
    if p.name == "__main__.py":
        init = p.parent / "__init__.py"
        for m, obj in sys.modules.items():
            if getattr(obj, "__file__", None) == str(init):
                print(m)
                break
        execl(sys.executable, sys.executable, "-m", m, *sys.argv[1:])
    else:
        execl(sys.executable, sys.executable, *sys.argv)
