# This file is placed in the Public Domain.


"create service file."


import getpass
import os


from ..disk  import skel
from ..utils import privileges


def skl(event):
    "create service file (pipx)."
    privileges(getpass.getuser())
    skel()
