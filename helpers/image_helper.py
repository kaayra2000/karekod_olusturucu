import cairosvg, io
from PIL import Image, ImageFont
def load_logos(image_files, logo_max_size):
    logos = []
    for image_file in image_files or []:
        if image_file.lower().endswith('.svg'):
            png_data = cairosvg.svg2png(url=image_file)
            logo_img = Image.open(io.BytesIO(png_data))
        else:
            logo_img = Image.open(image_file)
        
        ratio = min(logo_max_size / logo_img.width, logo_max_size / logo_img.height)
        new_size = (int(logo_img.width * ratio), int(logo_img.height * ratio))
        logos.append(logo_img.resize(new_size, Image.LANCZOS))
    return logos

def load_font(font_size, scale_factor):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(font_size * scale_factor))
    except IOError:
        return ImageFont.load_default()
def svg_to_png(svg_file):
    png_data = cairosvg.svg2png(url=svg_file)
    return Image.open(io.BytesIO(png_data))