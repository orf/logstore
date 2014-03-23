from django.core import management
import sys


def run():
    if len(sys.argv) == 1:
        sys.argv.append("help")
    sys.argv.append("--settings=logstore.web.web_interface.settings")
    management.execute_from_command_line()

if __name__ == "__main__":
    run()