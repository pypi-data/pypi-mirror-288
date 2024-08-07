import sys
from take_note_cli.core import notes


def main():
    notes.main(sys.argv[1:])


if __name__ == "__main__":
    main()
