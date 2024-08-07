# Take Note

**Create, organise and open notes in your favourite editor.**

I like having a quick, reliable and repeatable way of taking notes. If I have to open an editor, nvigate to the correct file, or create one in the correct place when it doesn't exist, then I find that I end up taking notes in random places. With Take Note, I have a few simple aliases set up so that typing thisWeek in my shell gets me to the right place in my DropBox with a new file if needed, created from a template so that eveything is consistent. This really scratches my itch. If it works for you great! If not, create your own solution.

## Features

- Written in Python with minimal runtime dependencies. Initially there were none, but I recently added Confuse (in v2.0.0) to allow a config file to do some of the heavy lifting that made aliases cumbersome.
  - Works on Python 3.8 - 3.12.
- Open notes files for specified week using the `code` command line for VS Code.
  - --thisWeek, --lastWeek and --nextWeek are supported.
- Organises notes in a date based folder structure from your root notes folder, e.g. 2023/08
  - The default folder is $HOME/Notes. I prefer to keep them in Google Drive or DropBox so I can access from mobile, tablet or my spare laptop.
  - set the root notes folder using --notesFolder
- Choose which editor to use with --editor
- Specify a VS Code workspace to open along with the note file with --workspace
  - This will automatically override the --editor setting to `code`. I have my default workspace set up with:
    - Zen mode
    - Word wrap
- Specify a template file relative to the root notes folder to use when a new file is created using --template. This also performs a simple replacement of the text HEADER_DATE with the date formatted as "%A %d %B %Y" to use in the document title.
- Support for batch creation of files in advance. This is useful if you use a device where you can edit files, but can't easily create them. Use --batch 5 along with any of the --*Week options to create that week and the following 4 weeks too.
- Config file allows base options to be set and reduce command line arguments needed.

## Future features

- Support for daily notes options.

## Installation

### pipx

The recommended way to install the published package is through [pipx](https://pypa.github.io/pipx/).

```bash
# from PyPI
pipx install take-note-cli

# direct from github
pipx install git+https://github.com/wsinned/take-note
```

## Usage

### Config File

A basic config file will be created in ~/.config/TakeNote/config.yaml if it doesn't already exist. Specifying default values here simplifies use of the command line by reducing the number of options needed to be supplied or added to an alias.

#### Config File Default Options

- notesFolder: Notes
- editor: code
- workspace:
- template:
- batch:
- verbose: False

### Command Line

Command line arguments will override any specified in the config file.
Specify a folder using the --notesFolder option.
A week option must be supplied from --thisWeek, --lastWeek or --nextWeek

```bash
take-note --notesFolder=$HOME/MyNotes --thisWeek
```

A note will be created in the under the MyNotes/YYYY/mm folder named with the date of the Monday of this week, e.g. 2023-08-07-Weekly-log.md

### Aliases

Setting up aliases in you preferred shell is a great way to make accessing your notes quick and easy.

```bash
NOTES_FOLDER="$HOME/SomePath/MyNotes"

alias thisWeek="take-note --thisWeek --notesFolder $NOTES_FOLDER --workspace notes.code-workspace"
alias nextWeek="take-note --nextWeek --notesFolder $NOTES_FOLDER --workspace notes.code-workspace --batch 5"
alias lastWeek="take-note --lastWeek --editor hx"
```

All you have to do now is type one of the following to open the desired note file.

```bash
> thisWeek
> lastWeek
> nextWeek
```

## Other Installation Methods

### Virtual Environment

```bash
python -m venv venv 

source venv/bin/activate

venv/bin/pip install -r requirements.txt

# install with tests as editable src
venv/bin/pip install -e .

```

## Development

### Nix & NixOS

The supplied shell.nix definition provides support for entering a nix-shell directly in the repository with all dependencies.

```bash
nix-shell --run zsh # ensure using zsh over default bash session
```

Then follow the instructions for other OS.

### Other Linux or macOS

```bash
# only needed once, or to recreate the virtual environment
# install dependencies
poetry install

# enter an activated shell and run tests
poetry shell
pytest
ruff . --config pyproject.toml

# run the tests without activating a shell
poetry run pytest

# run the installed app
poetry run take-note-cli --thisWeek

# exit the shell
exit
```

## Linting

The project uses [ruff](https://github.com/charliermarsh/ruff) for linting and optionally for formatting.

```bash
poetry run ruff . --config pyproject.toml
```

## Build & Publish

From an installed and tested venv, do the following:

Bump the version in pyproject.toml

```bash
# build the package
poetry build

# publish the package
poetry publish
```

Credentials for twine should be either:
    - stored in .pypirc in the [pypi] section
    - entered at the prompt, username = **token** and password = your_api_key
