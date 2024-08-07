from datetime import date
import sys
from take_note_cli.utils.paths import (
    generate_note_folder,
    generate_note_path,
    generate_template_path,
)
from take_note_cli.utils.dates import (
    get_monday,
    get_time_delta_from_options,
    format_header_date,
    get_weeks_delta,
)
from take_note_cli.utils.args import process_args
from take_note_cli.utils.config import process_config
from subprocess import call


def calculate_week_offset(options, parser):
    try:
        delta = get_time_delta_from_options(options)
    except ValueError:
        parser.print_help()
        sys.exit()
    return delta


def create_file(note_file, template_path, week: date):
    if not template_path:
        note_file.touch()
    else:
        text = ""
        with open(template_path, "r") as template_file:
            text = template_file.read().replace("HEADER_DATE", format_header_date(week))

        note_file.write_text(text)


def get_path_for_file(week: date, folder_path):
    folder = generate_note_folder(week, folder_path)

    if not folder.exists():
        print(f"Creating folder: {folder}")
        folder.mkdir(parents=True)

    note_path = folder.joinpath(generate_note_path(week))

    return note_path, note_path.exists()


def create_batch_of_files(options, week, template_path):
    verbose = options["verbose"]
    batch = options["batch"]
    notesFolder = options["notesFolder"]
    initial_note_path = None

    if batch is not None:
        for i in range(batch):
            batch_week = week + get_weeks_delta(i)
            note_path, file_exists = get_path_for_file(batch_week, notesFolder)
            if i == 0:
                initial_note_path = note_path

            if not file_exists:
                if verbose:
                    print(f"Creating file: {note_path}")
                create_file(note_path, template_path, batch_week)
    else:
        initial_note_path, file_exists = get_path_for_file(week, notesFolder)
        if not file_exists:
            if verbose:
                print(f"Creating file: {initial_note_path}")
            create_file(initial_note_path, template_path, week)

    return initial_note_path


def open_file(folder_path, editor, note_file, verbose, workspace=None):
    args = [editor, note_file]
    if workspace:
        args.append(folder_path.joinpath(workspace))

    if verbose:
        print(f"Opening file with args: {args}")

    call(args)


def main(argv):
    template_path = None
    options, parser = process_args(argv)
    config = process_config(options)

    if config["verbose"]:
        print("Welcome to take-note-cli")
        print(options)

    delta = calculate_week_offset(options, parser)
    week = get_monday(date.today()) + delta

    if config["template"] is not None:
        template_path = generate_template_path(
            config["notesFolder"], config["template"]
        )

    note_path = create_batch_of_files(config, week, template_path)

    open_file(
        config["notesFolder"],
        config["editor"],
        note_path,
        config["verbose"],
        config["workspace"],
    )
