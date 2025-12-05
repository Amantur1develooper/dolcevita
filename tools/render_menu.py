from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image

pdf_path = Path("DOLCEMENU2025.pdf")
out_dir = Path("static/menu")
out_dir.mkdir(parents=True, exist_ok=True)

zoom = 2.0  # ~ 144 dpi (увеличь до 2.5-3.0 для более чётких картинок)
mat = fitz.Matrix(zoom, zoom)

with fitz.open(pdf_path) as doc:
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(out_dir / f"page-{i}.webp", format="WEBP", quality=80)

print("Готово:", out_dir)
