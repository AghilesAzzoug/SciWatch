import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", "-c", type=str, required=True, help="Path to toml configuration file")
