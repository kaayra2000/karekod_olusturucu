# QR Kod Oluşturucu

Bu Python scripti, özelleştirilmiş QR kodları oluşturmak için tasarlanmıştır. WhatsApp tarzında, başlık ve logolar eklenmiş QR kodları üretir.

## Özellikler

- Tüm QR kod versiyonlarını (1-40) oluşturur.
- Özelleştirilebilir başlık ekler.
- Birden fazla logo ekleyebilme özelliği.
- Yüksek çözünürlüklü çıktı (1080px genişlik).
- SVG dahil çeşitli resim formatlarını destekler.

## Gereksinimler

Bu script'i çalıştırmak için Python3 ve aşağıdaki Python kütüphanelerinin yüklü olması gerekmektedir:

- `qrcode`
- `Pillow (PIL)`
- `cairosvg`

Gereken kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
pip3 install qrcode[pil] Pillow cairosvg
```

## Linux'ta Kurulum

Linux sistemlerde kurulum yapmak için aşağıdaki adımları izleyin:
1. Terminal'i açın.
1. Aşağıdaki komutu çalıştırın
```bash
source create_venv.sh
```
1. Bu işlemden sonra *qr_code_env* adında bir klasör oluşacaktır.
1. Sonrasında **Kulanım** başlığına geçebilirsiniz.
1. Kullanımınız bittikten sonra isterseniz `deactivate` komutuyla sanal ortamı kapatabilirsiniz.


## Kullanım
Script'i komut satırından şu şekilde çalıştırabilirsiniz:
```bash
python karekod_olustur.py <data> -o <output_file> -t <title> -i <image1> <image2> ...
```
## Parametreler
Parametreler:
* **<data\>:** QR kodunda yer alacak veri (zorunlu).
* **-o, --output:** Çıktı dosyasının adı (varsayılan: "karekod.png").
* **-t, --title:** QR kodun üstüne eklenecek başlık (varsayılan: "WhatsApp QR Kodu").
* **-i, --images:** Eklenecek resim dosyalarının yolları (isteğe bağlı, birden fazla olabilir).
* **-r, --resolution:** Çıktının yatay piksel sayısı. (varsayılan: 1080)
* **-f, --format:** Çıktı dosyası formatı (varsayılan: "png").
## Örnek Kullanım:
```bash
python karekod_olustur.py "https://google.com" -t "Başlık" -i logo1.png logo2.svg logo3.jpg
```
Bu komut, verilen URL'yi içeren bir QR kodu oluşturacak, belirtilen başlığı ekleyecek ve üç logoyu QR kodunun üstüne yerleştirecektir.
## Çıktı
Script, belirtilen isimde bir klasör oluşturur ve tüm QR kod versiyonlarını bu klasöre kaydeder. Her bir dosya şu formatta adlandırılır:
```bash
<output_name>_v<version_number>.png
```
Örneğin, varsayılan çıktı adı kullanılırsa, karekod adlı bir klasör oluşturulur ve içinde **`karekod_v1.png`, `karekod_v2.png`, ..., `karekod_v40.png`** dosyaları yer alır.

## Özelleştirme
Kod içerisinde bazı parametreleri değiştirerek çıktıyı özelleştirebilirsiniz:

* **margin:** Başlık metninin kenar boşluklarını ayarlar.
* **logo_max_size:** Logoların maksimum boyutunu belirler.

## Notlar
* SVG dosyaları otomatik olarak PNG'ye dönüştürülür.
* Logolar, orijinal en-boy oranlarını koruyarak yeniden boyutlandırılır.
* Başlık metni, QR kodunun genişliğine göre otomatik olarak kaydırılır.
