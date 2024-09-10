import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageFont
from .text_helper import wrap_text
from .image_helper import load_logos, load_font, add_logo_to_qr, resize_qr_image, create_background, paste_logos, draw_title
from .filesystem_helper import save_qr_image
from typing import Tuple, List
from .math_helper import calculate_text_height

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
    qr_image = generate_qr_image(data, version)
    
    if center_logo:
        qr_image = add_logo_to_qr(qr_image, center_logo)
    
    return resize_qr_image(qr_image, resolution)

def generate_qr_image(data: str, version: int) -> Image.Image:
    """
    Verilen data ve sürüm bilgisine göre QR kod görüntüsü oluşturur.

    Args:
        data (str): QR kodunda kodlanacak veri.
        version (int): QR kodunun sürümü.

    Returns:
        Image.Image: Oluşturulan temel QR kod görüntüsü.
    """
    # QR kod nesnesini oluştur
    qr = qrcode.QRCode(version=version, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Yuvarlak köşeli modül çizici ile QR kod görüntüsünü oluştur
    return qr.make_image(back_color="white", 
                         image_factory=StyledPilImage, 
                         module_drawer=RoundedModuleDrawer())

def prepare_title_text(title: str, max_width: int, max_height: int, scale_factor: float) -> Tuple[ImageFont.ImageFont, List[str], int]:
    """
    Başlık metnini hazırlar ve sarar.

    Args:
        title (str): Başlık metni.
        max_width (int): Maksimum metin genişliği.
        max_height (int): Maksimum metin yüksekliği.
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        Tuple[ImageFont.ImageFont, List[str], int]: Kullanılan font, sarılmış metin ve başlık yüksekliği.
    """
    font = load_font(36, scale_factor)
    wrapped_text, font = wrap_text(title, font, max_width, max_height, scale_factor)
    title_height = calculate_text_height(wrapped_text, font)
    return font, wrapped_text, title_height

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
            background, wrapped_text, title_height, logo_max_size, spacing, font = create_background(qr_img, title, text_scale_factor, prepare_title_text)
            
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
