from PIL import ImageDraw, ImageFont


def draw_metadata(
    pairs: list[tuple[str, str]],
    draw: ImageDraw.ImageDraw,
    margin: int,
    line_h: float,
    font_meta: ImageFont.FreeTypeFont,
) -> None:
    labels = [f"{label} " for label, _ in pairs]
    label_w = max(draw.textlength(label, font=font_meta) for label in labels)
    value_x = margin + label_w + 8

    y = margin
    for (_, value), label in zip(pairs, labels):
        draw.text((margin, y), label, font=font_meta, fill=(255, 255, 255))
        draw.text((value_x, y), value, font=font_meta, fill=(255, 255, 255))
        y += line_h
