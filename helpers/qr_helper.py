import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw
import textwrap
from .image_helper import load_logos, load_font, svg_to_png
from .filesystem_helper import save_qr_image



def create_qr_code(data, version, resolution, center_logo=None):
    qr = qrcode.QRCode(version=version, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(back_color="white", 
                        image_factory=StyledPilImage, 
                        module_drawer=RoundedModuleDrawer())

    if center_logo:
        logo = svg_to_png(center_logo) if center_logo.lower().endswith('.svg') else Image.open(center_logo)
        # Resize logo to be about 1/4 the size of the QR code
        logo_size = img.size[0] // 4
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        
        # Calculate position to place logo in center
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        
        # Create a white background for the logo
        white_box = Image.new('RGBA', logo.size, 'white')
        img.paste(white_box, pos)
        img.paste(logo, pos, logo if logo.mode == 'RGBA' else None)

    scale_factor = resolution / img.size[0]
    new_size = (resolution, int(img.size[1] * scale_factor))
    return img.resize(new_size, Image.LANCZOS)




def wrap_text(title, font, max_width, max_height, scale_factor):
    font_size = int(font.size)
    while font_size > int(8 * scale_factor):  # Scale the minimum font size
        wrapped_text = textwrap.wrap(title, width=int(max_width / (font_size / 2)))
        total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)
        if total_height <= max_height:
            return wrapped_text, font
        font_size -= 1
        font = load_font(font_size, scale_factor)
    return [], font




def create_background(qr_img, title, scale_factor):
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



def paste_logos(background, logos, logo_max_size, logo_spacing):
    bg_w, _ = background.size
    total_logo_width = sum(logo.width for logo in logos) + (len(logos) - 1) * logo_spacing
    start_x = (bg_w - total_logo_width) // 2
    for logo in logos:
        logo_position = (start_x, (logo_max_size - logo.height) // 2)
        background.paste(logo, logo_position, logo if logo.mode == 'RGBA' else None)
        start_x += logo.width + logo_spacing

def draw_title(background, wrapped_text, font, logo_max_size, spacing):
    draw = ImageDraw.Draw(background)
    bg_w, _ = background.size
    y_text = logo_max_size + spacing
    for line in wrapped_text:
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        draw.text(((bg_w - line_width) // 2, y_text), line, font=font, fill="black")
        y_text += line_height


def create_whatsapp_qr(data, output_file, title, resolution=1080, image_files=None, output_format="png",
                    text_scale_factor=1.0, logo_scale_factor=1.0, min_version=1, max_version=20, center_logo=None):

    try:
        for version in range(min_version, max_version + 1):
            qr_img = create_qr_code(data, version, resolution, center_logo)
            logos = load_logos(image_files, int(50 * logo_scale_factor))
            
            background, wrapped_text, title_height, logo_max_size, spacing, font = create_background(qr_img, title, text_scale_factor)
            
            if not wrapped_text:
                raise ValueError("Başlık metni çok küçük, okunamaz durumda.")
            
            if logos:
                paste_logos(background, logos, int(50 * logo_scale_factor), int(10 * logo_scale_factor))
            
            background.paste(qr_img, (0, title_height + spacing + logo_max_size))
            
            draw_title(background, wrapped_text, font, logo_max_size, spacing)
            
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

