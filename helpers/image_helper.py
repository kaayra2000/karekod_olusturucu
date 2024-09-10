import io
from PIL import Image, ImageFont
import cairosvg

def load_logos(image_files: list, logo_max_size: int) -> list:
    """
    Verilen dosya yollarından logo görüntülerini yükler ve boyutlandırır.

    Args:
        image_files (list): Logo dosyalarının yollarını içeren liste.
        logo_max_size (int): Logoların maksimum boyutu (piksel cinsinden).

    Returns:
        list: Yüklenmiş ve boyutlandırılmış logo görüntülerinin listesi.
    """
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

def load_font(font_size: int, scale_factor: float) -> ImageFont:
    """
    Belirtilen boyutta bir font yükler.

    Args:
        font_size (int): Yüklenecek fontun boyutu.
        scale_factor (float): Font boyutunu ölçeklendirmek için kullanılacak faktör.

    Returns:
        ImageFont: Yüklenen font nesnesi.
    """
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(font_size * scale_factor))
    except IOError:
        return ImageFont.load_default()

def svg_to_png(svg_file: str) -> Image:
    """
    SVG dosyasını PNG formatına dönüştürür.

    Args:
        svg_file (str): Dönüştürülecek SVG dosyasının yolu.

    Returns:
        Image: Dönüştürülmüş PNG görüntüsü.
    """
    png_data = cairosvg.svg2png(url=svg_file)
    return Image.open(io.BytesIO(png_data))
