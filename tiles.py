import shutil

from PIL import Image


def draw_tiles_block(
    tiles: list[str],
    canvas: Image.Image,
    tile_start_h: float,
    margin: int,
    tile_w: int,
    tile_h: int,
    cols: int,
    gap: int,
) -> None:
    for i, tile_path in enumerate(tiles):
        tile = Image.open(tile_path).convert("RGBA")
        w, h = tile.size

        col, row = i % cols, i // cols
        x = margin + col * (tile_w + gap)
        y = tile_start_h + row * (tile_h + gap)

        canvas.paste(tile, (x, y, x + w, y + h))

        tile.close()

    shutil.rmtree("temp")
