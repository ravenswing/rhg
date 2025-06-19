from glob import glob
from pathlib import Path
from tomllib import load as tomlload
from types import SimpleNamespace

from classes import Note


def find_tagged_notes(tag: str, exact: bool = True) -> list[Note]:
    tagged_notes = []
    for file in glob(f"{conf.vault}/**/*.md") + glob(f"{conf.vault}/*.md"):
        if f"{conf.vault}/templates/" in file:
            continue

        note = Note(file)

        if exact and note.tags:
            if tag in note.tags:
                tagged_notes.append(note)
        elif note.tags:
            if any([tag in x for x in note.tags]):
                tagged_notes.append(note)
        else:
            continue

    return tagged_notes


def main():
    home = str(Path.home())
    global conf
    with open(f"{home}/.config/rhg.toml", "rb") as f:
        conf = SimpleNamespace(**tomlload(f))

    # game_notes = find_tagged_notes("pandas", exact=False)

    # for note in game_notes:
    # print(note.name)
    #
    # print(len(find_tagged_notes("programming/python")))
    # print(len(find_tagged_notes("python", exact=False)))

    note = Note(f"{conf.vault}/python - structing a project.md")
    print(note)

    note.path = f"{conf.vault}/test test.md"

    print("\n\n")
    note.save()


if __name__ == "__main__":
    main()
