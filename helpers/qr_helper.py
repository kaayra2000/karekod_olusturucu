import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont
import textwrap
from .image_helper import load_logos, load_font, svg_to_png
from .filesystem_helper import save_qr_image
from typing import Tuple, List


def create_qr_code(data: str, version: int, resolution: int, center_logo: str = None) -> Image.Image:
    """
    Özelleştirilmiş bir QR kodu oluşturur.

    Args:
        data (str): QR kodunda kodlanacak veri.
        version (int): QR kodunun sürümü (1-40 arası).
        resolution (int): Oluşturulacak QR kodunun çözünürlüğü.
        center_logo (str, optional): Merkeze eklenecek logo dosyasının yolu.

    Returns:
        Image.Image: Oluşturulan QR kod görüntüsü.
    """
    # QR kod nesnesini oluştur
    qr = qrcode.QRCode(version=version, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Yuvarlak köşeli modül çizici ile QR kod görüntüsünü oluştur
    img = qr.make_image(back_color="white", 
                        image_factory=StyledPilImage, 
                        module_drawer=RoundedModuleDrawer())

    if center_logo:
        # Logo dosyasını aç ve işle
        logo = svg_to_png(center_logo) if center_logo.lower().endswith('.svg') else Image.open(center_logo)
        # Logo boyutunu QR kodunun yaklaşık 1/4'ü olacak şekilde yeniden boyutlandır
        logo_size = img.size[0] // 4
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        
        # Logoyu merkeze yerleştirmek için pozisyonu hesapla
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        
        # Logo için beyaz bir arka plan oluştur
        white_box = Image.new('RGBA', logo.size, 'white')
        img.paste(white_box, pos)
        img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

    # QR kodu istenen çözünürlüğe ölçeklendir
    scale_factor = resolution / img.size[0]
    new_size = (resolution, int(img.size[1] * scale_factor))
    return img.resize(new_size, Image.LANCZOS)





def wrap_text(title: str, font: ImageFont.ImageFont, max_width: int, max_height: int, scale_factor: float) -> Tuple[List[str], ImageFont.ImageFont]:
    """
    Metni belirli bir genişliğe ve yüksekliğe sığacak şekilde sarar ve gerekirse font boyutunu küçültür.

    Args:
        title (str): Sarılacak metin.
        font (ImageFont.ImageFont): Kullanılacak başlangıç fontu.
        max_width (int): Metnin sığması gereken maksimum genişlik.
        max_height (int): Metnin sığması gereken maksimum yükseklik.
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        Tuple[List[str], ImageFont.ImageFont]: Sarılmış metin satırları ve kullanılan font.
    """
    font_size = int(font.size)
    while font_size > int(8 * scale_factor):  # Minimum font boyutunu ölçeklendir
        wrapped_text = textwrap.wrap(title, width=int(max_width / (font_size / 2)))
        total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)
        if total_height <= max_height:
            return wrapped_text, font
        font_size -= 1
        font = load_font(font_size, scale_factor)
    return [], font

def create_background(qr_img: Image.Image, title: str, scale_factor: float) -> Tuple[Image.Image, List[str], int, int, int, ImageFont.ImageFont]:
    """
    QR kodu ve başlık için arka plan oluşturur.

    Args:
        qr_img (Image.Image): QR kod görüntüsü.
        title (str): Eklenecek başlık metni.
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        Tuple[Image.Image, List[str], int, int, int, ImageFont.ImageFont]: 
        Arka plan görüntüsü, sarılmış metin, başlık yüksekliği, maksimum logo boyutu, boşluk ve font.
    """
    img_w, img_h = qr_img.size
    margin = int(50 * scale_factor)
    max_title_width = img_w - 2 * margin
    max_title_height = int(120 * scale_factor)
    
    font = load_font(36, scale_factor)
    wrapped_text, font = wrap_text(title, font, max_title_width, max_title_height, scale_factor)
    title_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)

    spacing = int(5 * scale_factor)
    logo_max_size = int(50 * scale_factor)
    
    background = Image.new('RGB', (img_w, img_h + title_height + spacing + logo_max_size), color='white')
    return background, wrapped_text, title_height, logo_max_size, spacing, font


def paste_logos(background: Image.Image, logos: list, logo_max_size: int, logo_spacing: int) -> None:
    """
    Arka plan görüntüsüne logoları yerleştirir.

    Args:
        background (Image.Image): Logoların yerleştirileceği arka plan görüntüsü.
        logos (list): Yerleştirilecek logo görüntülerinin listesi.
        logo_max_size (int): Logoların maksimum boyutu.
        logo_spacing (int): Logolar arasındaki boşluk miktarı.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak arka plan görüntüsünü değiştirir.
    """
    bg_w, _ = background.size
    total_logo_width = sum(logo.width for logo in logos) + (len(logos) - 1) * logo_spacing
    start_x = (bg_w - total_logo_width) // 2
    for logo in logos:
        logo_position = (start_x, (logo_max_size - logo.height) // 2)
        background.paste(logo, logo_position, logo if logo.mode == 'RGBA' else None)
        start_x += logo.width + logo_spacing

def draw_title(background: Image.Image, wrapped_text: list, font: ImageFont.ImageFont, logo_max_size: int, spacing: int) -> None:
    """
    Arka plan görüntüsüne başlık metnini çizer.

    Args:
        background (Image.Image): Metnin çizileceği arka plan görüntüsü.
        wrapped_text (list): Çizilecek metin satırlarının listesi.
        font (ImageFont.ImageFont): Kullanılacak font.
        logo_max_size (int): Logoların maksimum boyutu (metin konumlandırması için kullanılır).
        spacing (int): Metin ile logolar arasındaki boşluk miktarı.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak arka plan görüntüsünü değiştirir.
    """
    draw = ImageDraw.Draw(background)
    bg_w, _ = background.size
    y_text = logo_max_size + spacing
    for line in wrapped_text:
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        draw.text(((bg_w - line_width) // 2, y_text), line, font=font, fill="black")
        y_text += line_height

def create_whatsapp_qr(data: str, output_file: str, title: str, resolution: int = 1080, 
                       image_files: list = None, output_format: str = "png",
                       text_scale_factor: float = 1.0, logo_scale_factor: float = 1.0, 
                       min_version: int = 1, max_version: int = 20, center_logo: str = None) -> None:
    """
    WhatsApp QR kodu oluşturur ve kaydeder.

    Args:
        data (str): QR kodunda kodlanacak veri.
        output_file (str): Çıktı dosyasının yolu.
        title (str): QR kodunun başlığı.
        resolution (int): QR kodunun çözünürlüğü (piksel cinsinden).
        image_files (list): Eklenecek logo dosyalarının yollarını içeren liste.
        output_format (str): Çıktı dosyasının formatı.
        text_scale_factor (float): Metin boyutu için ölçek faktörü.
        logo_scale_factor (float): Logo boyutu için ölçek faktörü.
        min_version (int): Minimum QR kod versiyonu.
        max_version (int): Maksimum QR kod versiyonu.
        center_logo (str): Merkeze yerleştirilecek logo dosyasının yolu.

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak bir QR kodu dosyası oluşturur.
    """
    try:
        for version in range(min_version, max_version + 1):
            # QR kodunu oluştur
            qr_img = create_qr_code(data, version, resolution, center_logo)
            
            # Logoları yükle
            logos = load_logos(image_files, int(50 * logo_scale_factor))
            
            # Arka planı oluştur
            background, wrapped_text, title_height, logo_max_size, spacing, font = create_background(qr_img, title, text_scale_factor)
            
            if not wrapped_text:
                raise ValueError("Başlık metni çok küçük, okunamaz durumda.")
            
            # Logoları yapıştır
            if logos:
                paste_logos(background, logos, int(50 * logo_scale_factor), int(10 * logo_scale_factor))
            
            # QR kodunu arka plana yapıştır
            background.paste(qr_img, (0, title_height + spacing + logo_max_size))
            
            # Başlığı çiz
            draw_title(background, wrapped_text, font, logo_max_size, spacing)
            
            # QR kodunu kaydet
            save_qr_image(background, output_file, version, output_format)
    except ValueError as e:
        if "invalid width" in str(e):
            print(f"Hata: Ölçek faktörü çok büyük, geçersiz bir genişliğe neden oluyor.")
            print("Lütfen daha küçük bir ölçek faktörü deneyin veya çözünürlüğü artırın.")
        elif "Başlık metni çok küçük" in str(e):
            print(f"Hata: Metin ölçek faktörü ile başlık metni çok küçük ve okunamaz durumda.")
            print("Lütfen daha büyük bir metin ölçek faktörü deneyin veya çözünürlüğü artırın.")
        else:
            print(f"Beklenmeyen bir hata oluştu: {e}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
