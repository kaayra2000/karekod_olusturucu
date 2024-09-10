import os

def save_qr_image(background: object, output_file: str, version: int, output_format: str) -> None:
    """
    QR kod görüntüsünü belirtilen formatta ve sürüm numarasıyla kaydeder.

    Args:
        background (object): Kaydedilecek QR kod görüntüsü (muhtemelen bir PIL Image nesnesi).
        output_file (str): Kaydedilecek dosyanın yolu ve adı.
        version (int): QR kod sürüm numarası.
        output_format (str): Çıktı dosyasının formatı (örn. 'png', 'jpg').

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak dosya sisteminde bir görüntü oluşturur.
    """
    # Çıktı dizinini oluştur
    output_dir = os.path.splitext(output_file)[0]
    os.makedirs(output_dir, exist_ok=True)

    # Sürüm numarasını içeren dosya adını oluştur
    versioned_filename = f"{os.path.splitext(os.path.basename(output_file))[0]}_v{version}.{output_format}"
    versioned_output = os.path.join(output_dir, versioned_filename)

    try:
        # QR kod görüntüsünü kaydet
        background.save(versioned_output)
        print(f"QR kod versiyonu {version} başarıyla oluşturuldu ve {versioned_output} olarak kaydedildi.")
    except ValueError as e:
        # Hata durumunda kullanıcıyı bilgilendir
        print(f"Hata: {e}")
        print(f"QR kod versiyonu {version} kaydedilemedi. Lütfen geçerli bir format belirtin.")
