from glob import glob
from pathlib import Path
from pprint import pprint
from tomllib import load as tomlload
from types import SimpleNamespace


def main():
    # home = os.path.expanduser("~")
    home = str(Path.home())
    with open(f"{home}/.config/rhg.toml", "rb") as f:
        conf = SimpleNamespace(**tomlload(f))

    print(conf.vault)
    print(conf.steam_id)


if __name__ == "__main__":
    main()
