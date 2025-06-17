from glob import glob
from pathlib import Path
from pprint import pprint
from tomllib import load as tomlload
from types import SimpleNamespace

from yaml import safe_load


def find_tagged_notes(tag) -> list[str]:
    tagged_notes = []
    for file in glob(f"{conf.vault}/**/*.md") + glob(f"{conf.vault}/*.md"):
        if f"{conf.vault}/templates/" in file:
            continue
        note = load_note(file)
        if note is None:
            continue
        else:
            properties, content = note

        tagged = False
        tagged_yaml = False
        has_yaml = False
        if properties is not None:
            has_yaml = True
            if "tags" in properties.keys():
                tagged_yaml = True if tag in properties["tags"] else tagged_yaml

        tagged = any([f"#{tag}" in x for x in content])

        if tagged and has_yaml:
            print(file, "  <-- need to convert tag to YAML")

        if any([tagged, tagged_yaml]):
            tagged_notes.append(file)
    return tagged_notes


def load_note(path, verbose=False):
    with open(path, "r") as f:
        lines = f.readlines()
    if not lines:
        if verbose:
            print(f"WARNING - {path} is an empty note")
        return None
    if lines[0].strip() == "---":
        indexes = [i for i, value in enumerate(lines) if value.strip() == "---"]
        properties = safe_load("".join(lines[indexes[0] + 1 : indexes[1]]))
        return properties, lines[indexes[1] :]
    else:
        return None, lines


def main():
    home = str(Path.home())
    global conf
    with open(f"{home}/.config/rhg.toml", "rb") as f:
        conf = SimpleNamespace(**tomlload(f))

    game_notes = find_tagged_notes("game")

    if game_notes:
        properties, content = load_note(game_notes[0])

        print(properties, content)


if __name__ == "__main__":
    main()
