from pathlib import Path


ROOT = Path(__file__).parent.parent.parent
IMG_PATH = ROOT / "figures"


def load_img(path: Path) -> bytes:
    """Load an image from the given path."""
    with open(IMG_PATH / path, "rb") as f:
        return f.read()
