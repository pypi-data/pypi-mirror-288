# This file is placed in the Public Domain.
# pylint: disable=C0413,W0212,W0613,E0401


"main"


import getpass
import os
import sys


from .cfg    import Config
from .cmds   import Commands
from .errors import errors
from .disk   import Persist, skel
from .main   import cmnd, enable, scan, wrap
from .parse  import parse
from .utils  import modnames, privileges


from . import modules, user


Cfg         = Config()
Cfg.mod     = "cmd,skl,req,srv"
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.user    = getpass.getuser()
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


def srv(event):
    "create service file (pipx)."
    if event.args:
        username = event.args[0]
    else:
        username  = getpass.getuser()
    txt = f"""[Unit]
Description={Cfg.name.upper()}
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
User={username}
Group={username}
ExecStartPre=/home/{username}/.local/bin/{Cfg.name} skl
ExecStart=/home/{username}/.local/bin/{Cfg.name}d
ExitType=cgroup
KillSignal=SIGKILL
KillMode=control-group
RemainAfterExit=yes
Restart=no

[Install]
WantedBy=default.target"""
    event.reply(txt)


def main():
    "main"
    Commands.add(srv)
    parse(Cfg, " ".join(sys.argv[1:]))
    enable(print)
    Cfg.dis = Cfg.sets.dis
    if "a" in Cfg.opts:
        Cfg.mod = ",".join(modnames(modules, user))
    scan(Cfg.mod, modules, user)
    cmnd(Cfg.otxt, print)


def wrapped():
    wrap(main)


if __name__ == "__main__":
    wrapped()
