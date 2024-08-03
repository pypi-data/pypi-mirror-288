import sys
import time
from os import execl


def restart():
    execl(sys.executable, sys.executable, *sys.argv)


if __name__ == "__main__":
    print("bonjour!")
    time.sleep(1)
    restart()


# import os
# import re
# import signal
# import subprocess
# from contextlib import contextmanager


# @contextmanager
# def serve(*args):
#     args = ["starbear", "serve", "-p", "0", *args]
#     proc = subprocess.Popen(
#         args, stderr=subprocess.PIPE, env={**os.environ, "PYTHONUNBUFFERED": "1"}
#     )
#     try:
#         while True:
#             line = proc.stderr.readline().decode("utf8")
#             print(line, end="")
#             if m := re.match(string=line, pattern=r".*Serving at:.*(https?://[a-zA-Z0-9_.:]+)"):
#                 yield m.groups()[0]
#                 break
#     finally:
#         # proc.kill()
#         proc.send_signal(signal.SIGINT)


# with serve("-m", "tests.server.app_hello") as addr:
#     print(addr)
