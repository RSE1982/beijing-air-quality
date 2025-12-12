from pathlib import Path
import plotly.express as px
import PIL.Image as Image

ROOT = Path(__file__).parent.parent
IMG_PATH = ROOT / "figures"


def load_img(path: Path) -> bytes:
    """
    Load an image from the figures directory and return as a Plotly figure.
    Args:
        path (Path): Relative path to the image file within the
        figures directory.
    Returns:
        fig (px.Figure): Plotly figure containing the image.
    """
    img = Image.open(IMG_PATH / path)  # Load image from figures directory
    fig = px.imshow(img)  # Create Plotly figure
    fig.update_layout(height=500)  # Set figure height

    return fig
