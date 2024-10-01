import io
from PIL import Image, ImageFont, ImageDraw, ImageChops, ImageOps
import cairosvg
from typing import List, Tuple
from .math_helper import calculate_dimensions
import numpy as np
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

def resize_qr_image(qr_image: Image.Image, resolution: int) -> Image.Image:
    """
    QR kod görüntüsünü istenen çözünürlüğe ölçeklendirir.

    Args:
        qr_image (Image.Image): Orijinal QR kod görüntüsü.
        resolution (int): Hedef çözünürlük.

    Returns:
        Image.Image: Ölçeklendirilmiş QR kod görüntüsü.
    """
    scale_factor = resolution / qr_image.size[0]
    new_size = (resolution, int(qr_image.size[1] * scale_factor))
    return qr_image.resize(new_size, Image.LANCZOS)


def add_logo_to_qr(qr_image: Image.Image, logo_path: str, logo_size: float, is_circle: bool = True,
                    border_size: float = 0.0, border_color: str = "white") -> Image.Image:
    """
    QR kod görüntüsünün merkezine logo ekler. Logo daire veya kare olarak eklenebilir.

    Args:
        qr_image (Image.Image): Orijinal QR kod görüntüsü.
        logo_path (str): Eklenecek logo dosyasının yolu.
        logo_size (float): Logo boyutu (0-1 arasında bir oran).
        is_circle (bool): Logo daire mi olsun, kare mi. Varsayılan True (daire).
        border_size (float): Logo etrafındaki kenarlık boyutu.
        border_color (str): Logo etrafındaki kenarlık rengi.

    Returns:
        Image.Image: Logo eklenmiş QR kod görüntüsü.
    """

    # Logo dosyasını aç ve işle
    logo = process_logo(logo_path)

    # Logo etrafındaki beyazlıkları hafifçe kırp
    logo = trim_logo(logo)

    # QR kodunun boyutunun %logo_size'ını hesapla
    qr_width, qr_height = qr_image.size
    max_logo_size = int(min(qr_width, qr_height) * logo_size)

    # Logo boyutunu oranları koruyarak yeniden boyutlandır
    logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

    # Beyaz arka planlı yeni bir resim oluştur
    border_size = int(logo.width * border_size)  # Kenar boşluğu (border_size oranında)
    new_size = (logo.width + 2 * border_size, logo.height + 2 * border_size)
    background = Image.new('RGBA', new_size, border_color)

    # Logoyu yeni arka planın ortasına yerleştir
    logo_position = (border_size, border_size)
    background.paste(logo, logo_position, mask=logo if logo.mode == 'RGBA' else None)

    if is_circle:
        # Dairesel maske oluştur
        mask = Image.new('L', new_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + new_size, fill=255)
        # Maskeyi arka plana uygula
        background.putalpha(mask)

    # Logoyu merkeze yerleştirmek için pozisyonu hesapla
    pos = ((qr_width - new_size[0]) // 2, (qr_height - new_size[1]) // 2)

    # Logoyu QR koda ekle
    qr_image.paste(background, pos, mask=background if background.mode == 'RGBA' else None)

    return qr_image



def trim_logo(logo: Image.Image) -> Image.Image:
    """
    Logo etrafındaki gereksiz boşlukları kırpar ve kare şeklinde yapar.

    Args:
        logo (Image.Image): Orijinal logo görüntüsü.

    Returns:
        Image.Image: Kırpılmış ve kare şekline getirilmiş logo görüntüsü.
    """
    # Alfa kanalını kullanarak kırpma yap
    if logo.mode in ('RGBA', 'LA'):
        alpha = logo.split()[-1]
        bbox = alpha.getbbox()
    else:
        bg = Image.new(logo.mode, logo.size, logo.getpixel((0, 0)))
        diff = ImageChops.difference(logo, bg)
        bbox = diff.getbbox()

    if bbox:
        logo = logo.crop(bbox)

    # Kare şeklinde kırpma yap
    width, height = logo.size
    size = max(width, height)
    
    # Orijinal logonun moduna göre yeni bir kare görüntü oluştur
    if logo.mode == 'RGBA':
        new_logo = Image.new('RGBA', (size, size), (255, 255, 255, 0))  # Şeffaf beyaz
    else:
        new_logo = Image.new(logo.mode, (size, size), (255, 255, 255))  # Opak beyaz
    
    # Logo'yu yeni kare görüntünün ortasına yerleştir
    x = (size - width) // 2
    y = (size - height) // 2
    new_logo.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)

    return new_logo



def process_logo(logo_path: str) -> Image.Image:
    """
    Logo dosyasını işler ve uygun formatta açar.

    Args:
        logo_path (str): Logo dosyasının yolu.

    Returns:
        Image.Image: İşlenmiş logo görüntüsü.
    """
    if logo_path.lower().endswith('.svg'):
        return svg_to_png(logo_path)
    else:
        return Image.open(logo_path)

def create_white_background(width: int, height: int, title_height: int, spacing: int, logo_max_size: int) -> Image.Image:
    """
    Beyaz bir arka plan oluşturur.

    Args:
        width (int): Arka plan genişliği.
        height (int): QR kod yüksekliği.
        title_height (int): Başlık yüksekliği.
        spacing (int): Boşluk miktarı.
        logo_max_size (int): Maksimum logo boyutu.

    Returns:
        Image.Image: Oluşturulan beyaz arka plan.
    """
    total_height = height + title_height + spacing + logo_max_size
    return Image.new('RGB', (width, total_height), color='white')


def create_background(qr_img: Image.Image, title: str, scale_factor: float, prepare_title_text: callable) -> Tuple[Image.Image, List[str], int, int, int, ImageFont.ImageFont]:
    """
    QR kodu ve başlık için arka plan oluşturur.

    Args:
        qr_img (Image.Image): QR kod görüntüsü.
        title (str): Eklenecek başlık metni.
        scale_factor (float): Ölçeklendirme faktörü.
        prepare_title_text (callable): Başlık metnini hazırlayan fonksiyon.

    Returns:
        Tuple[Image.Image, List[str], int, int, int, ImageFont.ImageFont]: 
        Arka plan görüntüsü, sarılmış metin, başlık yüksekliği, maksimum logo boyutu, boşluk ve font.
    """
    # QR kod görüntüsünün boyutlarını al
    img_w, img_h = qr_img.size
    
    # Boyutları hesapla
    margin, max_title_height, spacing, logo_max_size = calculate_dimensions(scale_factor, img_h)
    max_title_width = img_w - 2 * margin

    # Başlık metnini hazırla
    font, wrapped_text, title_height = prepare_title_text(title, max_title_width, max_title_height, scale_factor)

    # Beyaz arka planı oluştur
    background = create_white_background(img_w, img_h, title_height, spacing, logo_max_size)

    # Sonuçları döndür
    return background, wrapped_text, title_height, logo_max_size, spacing, font


def paste_logos(background: Image.Image, logos: List[Image.Image], logo_max_size: int, logo_spacing: int) -> None:
    """
    Arka plan görüntüsüne logoları yerleştirir.

    Args:
        background (Image.Image): Logoların yerleştirileceği arka plan görüntüsü.
        logos (List[Image.Image]): Yerleştirilecek logo görüntülerinin listesi.
        logo_max_size (int): Logoların maksimum boyutu.
        logo_spacing (int): Logolar arasındaki boşluk miktarı.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak arka plan görüntüsünü değiştirir.
    """
    bg_w, _ = background.size
    total_logo_width = calculate_total_logo_width(logos, logo_spacing)
    start_x = calculate_start_position(bg_w, total_logo_width)

    for logo in logos:
        logo_position = calculate_logo_position(start_x, logo_max_size, logo.height)
        paste_logo(background, logo, logo_position)
        start_x += logo.width + logo_spacing

def calculate_total_logo_width(logos: List[Image.Image], logo_spacing: int) -> int:
    """
    Tüm logoların toplam genişliğini hesaplar.

    Args:
        logos (List[Image.Image]): Logo görüntülerinin listesi.
        logo_spacing (int): Logolar arasındaki boşluk miktarı.

    Returns:
        int: Tüm logoların toplam genişliği.
    """
    return sum(logo.width for logo in logos) + (len(logos) - 1) * logo_spacing

def calculate_start_position(bg_width: int, total_logo_width: int) -> int:
    """
    Logoların yerleştirilmeye başlanacağı x koordinatını hesaplar.

    Args:
        bg_width (int): Arka plan genişliği.
        total_logo_width (int): Tüm logoların toplam genişliği.

    Returns:
        int: Başlangıç x koordinatı.
    """
    return (bg_width - total_logo_width) // 2

def calculate_logo_position(start_x: int, logo_max_size: int, logo_height: int) -> tuple:
    """
    Bir logonun yerleştirileceği pozisyonu hesaplar.

    Args:
        start_x (int): Başlangıç x koordinatı.
        logo_max_size (int): Logoların maksimum boyutu.
        logo_height (int): Logonun yüksekliği.

    Returns:
        tuple: Logonun yerleştirileceği (x, y) koordinatları.
    """
    return (start_x, (logo_max_size - logo_height) // 2)

def paste_logo(background: Image.Image, logo: Image.Image, position: tuple) -> None:
    """
    Bir logoyu arka plan görüntüsüne yapıştırır.

    Args:
        background (Image.Image): Arka plan görüntüsü.
        logo (Image.Image): Yapıştırılacak logo görüntüsü.
        position (tuple): Logonun yerleştirileceği (x, y) koordinatları.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak arka plan görüntüsünü değiştirir.
    """
    background.paste(logo, position, logo if logo.mode == 'RGBA' else None)

def draw_title(background: Image.Image, wrapped_text: List[str], font: ImageFont.ImageFont, logo_max_size: int, spacing: int) -> None:
    """
    Arka plan görüntüsüne başlık metnini çizer.

    Args:
        background (Image.Image): Metnin çizileceği arka plan görüntüsü.
        wrapped_text (List[str]): Çizilecek metin satırlarının listesi.
        font (ImageFont.ImageFont): Kullanılacak font.
        logo_max_size (int): Logoların maksimum boyutu (metin konumlandırması için kullanılır).
        spacing (int): Metin ile logolar arasındaki boşluk miktarı.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak arka plan görüntüsünü değiştirir.
    """
    draw = create_draw_object(background)
    bg_width = background.size[0]
    start_y = calculate_start_y(logo_max_size, spacing)
    
    for line in wrapped_text:
        line_width, line_height = calculate_line_dimensions(font, line)
        x_position = calculate_x_position(bg_width, line_width)
        draw_text_line(draw, line, font, x_position, start_y)
        start_y += line_height

def create_draw_object(image: Image.Image) -> ImageDraw.ImageDraw:
    """
    Verilen görüntü üzerinde çizim yapmak için bir ImageDraw nesnesi oluşturur.

    Args:
        image (Image.Image): Üzerinde çizim yapılacak görüntü.

    Returns:
        ImageDraw.ImageDraw: Oluşturulan çizim nesnesi.
    """
    return ImageDraw.Draw(image)

def calculate_start_y(logo_max_size: int, spacing: int) -> int:
    """
    Metnin başlangıç y koordinatını hesaplar.

    Args:
        logo_max_size (int): Logoların maksimum boyutu.
        spacing (int): Metin ile logolar arasındaki boşluk miktarı.

    Returns:
        int: Metnin başlangıç y koordinatı.
    """
    return logo_max_size + spacing

def calculate_line_dimensions(font: ImageFont.ImageFont, line: str) -> tuple:
    """
    Bir metin satırının genişliğini ve yüksekliğini hesaplar.

    Args:
        font (ImageFont.ImageFont): Kullanılan font.
        line (str): Metin satırı.

    Returns:
        tuple: Satırın genişliği ve yüksekliği.
    """
    line_bbox = font.getbbox(line)
    return line_bbox[2] - line_bbox[0], line_bbox[3] - line_bbox[1]

def calculate_x_position(bg_width: int, line_width: int) -> int:
    """
    Metin satırının x koordinatını hesaplar (ortalamak için).

    Args:
        bg_width (int): Arka plan genişliği.
        line_width (int): Metin satırının genişliği.

    Returns:
        int: Metin satırının x koordinatı.
    """
    return (bg_width - line_width) // 2

def draw_text_line(draw: ImageDraw.ImageDraw, line: str, font: ImageFont.ImageFont, x: int, y: int) -> None:
    """
    Belirtilen konuma bir metin satırı çizer.

    Args:
        draw (ImageDraw.ImageDraw): Çizim nesnesi.
        line (str): Çizilecek metin satırı.
        font (ImageFont.ImageFont): Kullanılacak font.
        x (int): Metnin x koordinatı.
        y (int): Metnin y koordinatı.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak çizim nesnesini günceller.
    """
    draw.text((x, y), line, font=font, fill="black")