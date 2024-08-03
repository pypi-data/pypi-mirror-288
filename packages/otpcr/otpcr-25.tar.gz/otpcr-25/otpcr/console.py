# This file is placed in the Public Domain.
# pylint: disable=C0413,W0212,E0401


"main"


import os
import readline
import sys
import termios
import time


from .cfg    import Config
from .errors import errors
from .disk   import Persist, skel
from .main   import cmnd, enable, init, scan
from .parse  import parse
from .term   import Console
from .utils  import forever, modnames


from . import modules, user


if os.path.exists("mods"):
    import mods as MODS
else:
    MODS = None


Cfg         = Config()
Cfg.mod     = "cmd,mod,thr,err"
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


def wrap(func):
    "reset terminal."
    old3 = None
    try:
        old3 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old3:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old3)
    errors()


def main():
    "main"
    parse(Cfg, " ".join(sys.argv[1:]))
    Cfg.dis = Cfg.sets.dis
    Cfg.mod += "," + ",".join(modnames(modules, user, MODS))
    readline.redisplay()
    enable(print)
    skel()
    scan(Cfg.mod, modules, user, MODS)
    csl = Console(print, input)
    if "i" in Cfg.opts:
        init(Cfg.mod, modules, user, MODS)
    csl.start()
    cmnd(Cfg.otxt, print)
    forever()


def wrapped():
    wrap(main)


if __name__ == "__main__":
    wrapped()
