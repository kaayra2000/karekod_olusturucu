import os
def save_qr_image(background, output_file, version, output_format):
    output_dir = os.path.splitext(output_file)[0]
    os.makedirs(output_dir, exist_ok=True)
    versioned_filename = f"{os.path.splitext(os.path.basename(output_file))[0]}_v{version}.{output_format}"
    versioned_output = os.path.join(output_dir, versioned_filename)
    try:
        background.save(versioned_output)
        print(f"QR kod versiyonu {version} başarıyla oluşturuldu ve {versioned_output} olarak kaydedildi.")
    except ValueError as e:
        print(f"Hata: {e}")
        print(f"QR kod versiyonu {version} kaydedilemedi. Lütfen geçerli bir format belirtin.")
