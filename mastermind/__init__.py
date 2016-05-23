from __future__ import (absolute_import, print_function, division)

from itertools import repeat
import os

from . import cli
from . import proxyswitch
from . import say
from . import version
from mitmproxy.main import mitmdump

def main():
    parser = cli.args()
    args, extra_args = parser.parse_known_args()

    config = cli.config(args)
    mitm_args = cli.mitm_args(config)
    is_sudo = os.getuid() == 0

    if type(mitm_args) == Exception:
        parser.error(mitm_args.message)

    say.level(config["core"]["verbose"])

    try:
        if config["os"]["proxy-settings"]:
            if not is_sudo:
                parser.error("proxy-settings is enabled, please provide sudo in order to change the OSX proxy configuration.")

            proxyswitch.enable(config["core"]["host"],
                               str(config["core"]["port"]))

        mitmdump(mitm_args + extra_args)
    finally:
        if config["os"]["proxy-settings"] and is_sudo:
            proxyswitch.disable()
