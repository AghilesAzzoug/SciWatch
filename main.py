from pathlib import Path

from sci_watch.sci_watcher import SciWatcher

if __name__ == "__main__":
    sc = SciWatcher.from_toml(Path(r"scrapping_config.toml").absolute())

    sc.exec()
