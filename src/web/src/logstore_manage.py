from django.core import management
from logstore import web
import sys
import os


def run():
    sys.path.append(os.path.dirname(web.__file__))
    if len(sys.argv) == 1:
        sys.argv.append("help")
    sys.argv.append("--settings=logstore.web.web_interface.settings")
    management.execute_from_command_line()

if __name__ == "__main__":
    run()