from pathlib import Path
import plotly.express as px
import PIL.Image as Image

ROOT = Path(__file__).parent.parent
IMG_PATH = ROOT / "figures"


def load_img(path: Path) -> bytes:
    img = Image.open(IMG_PATH / path)
    fig = px.imshow(img)
    fig.update_layout(height=500)
    return fig
