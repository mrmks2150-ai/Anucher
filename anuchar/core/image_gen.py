import requests
import io
from PIL import Image
from urllib.parse import quote


def generate_image(prompt, style="Realistic", width=1024, height=1024, seed=0):
    full = f"{prompt}, {style} style, highly detailed, 8k, best quality"
    url = (
        f"https://image.pollinations.ai/prompt/{quote(full)}"
        f"?width={width}&height={height}&seed={seed}&nologo=true"
    )
    r = requests.get(url, timeout=90)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content))
    return img, full, url
