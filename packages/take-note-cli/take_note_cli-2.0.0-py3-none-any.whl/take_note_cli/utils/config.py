import pathlib
import confuse

template = {
    "notesFolder": confuse.Path(cwd=pathlib.Path.home()),
    "editor": "code",
    "workspace": None,
    "template": None,
    "batch": None,
    "verbose": False,
}


def check_for_config_file():
    config = confuse.Configuration("TakeNote")

    if not config.keys():
        config_filename = pathlib.Path.joinpath(
            pathlib.Path(config.config_dir()), confuse.CONFIG_FILENAME
        )

        template_filename = pathlib.Path("./src/take_note_cli/config/config.yaml")

        with open(template_filename, "r") as t:
            with open(config_filename, "w") as f:
                f.writelines(t.readlines())

        config = check_for_config_file()

    return config


def process_config(options):
    config = check_for_config_file()
    config.set_args(options)
    valid_config = config.get(template)

    workspace = config["workspace"].get(confuse.Optional(confuse.String()))
    if workspace is not None:
        options.editor = "code"

    return valid_config
