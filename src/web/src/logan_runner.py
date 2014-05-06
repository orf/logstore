from logan.runner import run_app
import os


def generate_settings():
    from .web_interface import default_logain_settings

    with open(default_logain_settings.__file__, "rb") as fd:
        return fd.read()



def main():
    run_app(
        project="logstore.web",
        default_config_path=os.path.join('~', '.logstore', 'web_settings.py'),
        default_settings='logstore.web.web_interface.settings',
        settings_initializer=generate_settings,
        settings_envvar='LOGSTORE_WEB_CONF',
        config_module_name="logstore.web.web_interface.logan_settings",
    )


if __name__ == "__main__":
    main()