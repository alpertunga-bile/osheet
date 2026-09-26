from PIL import ImageDraw, ImageFont


def draw_metadata(
    lines: list[str],
    draw: ImageDraw.ImageDraw,
    margin: int,
    line_h: float,
    font_meta: ImageFont.FreeTypeFont,
) -> None:
    y = margin

    for line in lines:
        draw.text((margin, y), line, font=font_meta, fill=(255, 255, 255))
        y += line_h
