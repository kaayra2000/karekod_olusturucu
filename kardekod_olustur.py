import qrcode
import argparse
import os
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import cairosvg

def create_whatsapp_qr(data, output_file, title, resolution=1080, image_files=None):
    output_dir = os.path.splitext(output_file)[0]
    os.makedirs(output_dir, exist_ok=True)

    for version in range(1, 41):
        qr = qrcode.QRCode(version=version, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(back_color="white", 
                            image_factory=StyledPilImage, 
                            module_drawer=RoundedModuleDrawer())

        scale_factor = resolution / img.size[0]
        new_size = (resolution, int(img.size[1] * scale_factor))
        img = img.resize(new_size, Image.LANCZOS)

        img_w, img_h = img.size

        font_size = int(36 * scale_factor)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Yazı için kenar boşluğu ekleyin
        margin = int(50 * scale_factor)
        max_title_width = img_w - 2 * margin
        max_title_height = int(120 * scale_factor)

        wrapped_text = []
        while font_size > 8:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            wrapped_text = textwrap.wrap(title, width=int(max_title_width / (font_size / 2)))
            
            total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)
            if total_height <= max_title_height:
                break
            font_size -= 1

        title_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)

        spacing = int(5 * scale_factor)
        logo_max_size = int(50 * scale_factor)
        logo_spacing = int(10 * scale_factor)

        logos = []
        if image_files:
            for image_file in image_files:
                if image_file.lower().endswith('.svg'):
                    png_data = cairosvg.svg2png(url=image_file)
                    logo_img = Image.open(io.BytesIO(png_data))
                else:
                    logo_img = Image.open(image_file)
                
                ratio = min(logo_max_size / logo_img.width, logo_max_size / logo_img.height)
                new_size = (int(logo_img.width * ratio), int(logo_img.height * ratio))
                logo_img = logo_img.resize(new_size, Image.LANCZOS)
                
                logos.append(logo_img)

        total_logo_width = sum(logo.width for logo in logos) + (len(logos) - 1) * logo_spacing

        background = Image.new('RGB', (img_w, img_h + title_height + spacing + logo_max_size), color='white')
        bg_w, bg_h = background.size

        if logos:
            start_x = (bg_w - total_logo_width) // 2
            for logo in logos:
                logo_position = (start_x, (logo_max_size - logo.height) // 2)
                background.paste(logo, logo_position, logo if logo.mode == 'RGBA' else None)
                start_x += logo.width + logo_spacing

        offset = (0, title_height + spacing + logo_max_size)
        background.paste(img, offset)

        draw = ImageDraw.Draw(background)
        
        y_text = logo_max_size + spacing
        for line in wrapped_text:
            line_bbox = font.getbbox(line)
            line_width = line_bbox[2] - line_bbox[0]
            line_height = line_bbox[3] - line_bbox[1]
            draw.text(((bg_w - line_width) // 2, y_text), line, font=font, fill="black")
            y_text += line_height

        versioned_filename = f"{os.path.splitext(os.path.basename(output_file))[0]}_v{version}.png"
        versioned_output = os.path.join(output_dir, versioned_filename)

        background.save(versioned_output)
        print(f"QR kod versiyonu {version} başarıyla oluşturuldu ve {versioned_output} olarak kaydedildi.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp tarzı QR kod oluşturucu")
    parser.add_argument("data", help="QR kodunda yer alacak veri")
    parser.add_argument("-o", "--output", help="Çıktı dosyasının adı (örn: qrcode.png)", default="karekod.png")
    parser.add_argument("-t", "--title", help="QR kodun üstüne eklenecek başlık", default="WhatsApp QR Kodu")
    parser.add_argument("-i", "--images", nargs='+', help="Eklenecek resim dosyalarının yolları", default=None)
    parser.add_argument("-r", "--resolution", type=int, help="QR kodun çözünürlüğü (piksel cinsinden genişlik)", default=1080)
    args = parser.parse_args()

    create_whatsapp_qr(args.data, args.output, args.title, args.resolution ,args.images)
