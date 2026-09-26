from PIL import Image


def draw_tiles_block(
    tiles: list[str],
    canvas: Image.Image,
    margin: int,
    header_h: float,
    separator_gap: int,
    tile_h: int,
    tile_w: int,
    cols: int,
    gap: int,
) -> None:
    tiles_top = margin + header_h + separator_gap

    for i, tile_path in enumerate(tiles):
        tile = Image.open(tile_path).convert("RGBA")
        w, h = tile.size

        col, row = i % cols, i // cols
        x = margin + col * (tile_w + gap)
        y = tiles_top + row * (tile_h + gap)

        w, h = tile.size
        canvas.paste(tile, (x, y, x + w, y + h))
