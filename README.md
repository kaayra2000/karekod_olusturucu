# QR Kod Oluşturucu

Bu Python scripti, özelleştirilmiş QR kodları oluşturmak için tasarlanmıştır. WhatsApp tarzında, başlık ve logolar eklenmiş QR kodları üretir.

## Özellikler

- Tüm QR kod versiyonlarını (1-40) oluşturur.
- Özelleştirilebilir başlık ekler.
- Birden fazla logo ekleyebilme özelliği.
- Ayarlanabilir çözünürlüklü çıktı (varsayılan 1080px genişlik).
- SVG dahil çeşitli resim formatlarını destekler.

## Gereksinimler

Bu script'i çalıştırmak için Python3.12.3 ve aşağıdaki Python kütüphanelerinin yüklü olması gerekmektedir:

- `qrcode`
- `Pillow (PIL)`
- `cairosvg`
- `numpy`
- `emoji`

Gereken kütüphaneleri yüklemek için aşağıdaki komutlardan birini kullanabilirsiniz:

```bash
pip3 install qrcode[pil] Pillow cairosvg numpy emoji
```

```bash
pip3 install -r requirements.txt
```

## Linux'ta Kurulum

Linux sistemlerde kurulum yapmak için aşağıdaki adımları izleyin:

1. Terminal'i açın.
1. Aşağıdaki komutu çalıştırın

```bash
source create_venv.sh
```

1. Bu işlemden sonra _qr_code_env_ adında bir klasör oluşacaktır.
1. Sonrasında **Kulanım** başlığına geçebilirsiniz.
1. Kullanımınız bittikten sonra isterseniz `deactivate` komutuyla sanal ortamı kapatabilirsiniz.

## Kullanım

Script'i komut satırından şu şekilde çalıştırabilirsiniz:

```bash
python3 main.py <data> -o <output_file> -t <title> -i <image1> <image2> ...
```

## Parametreler

Parametreler:

- **<data\>:** QR kodunda yer alacak veri (zorunlu).
- **-o, --output:** Çıktı dosyasının adı _(varsayılan: "karekod.png")_.
- **-cl, --center_logo:** QR kodunun merkezinde gözükecek logo. _(varsayılan: None, svg de olabilir)_
- **-cls, --center_logo_size:** QR kodunun merkezinde gözükecek logonun kardekoda oranı. Çok büyük seçilirse karakod okunmaz hale gelir. _(varsayılan: 0.2)_
- **-t, --title:** QR kodun üstüne eklenecek başlık _(varsayılan: "WhatsApp QR Kodu")_.
- **-tc, --title_color:** QR kodun üstündeki başlığın rengi _[varsayılan: black (siyah)]_
- **-i, --images:** Üst kısma eklenecek resim dosyalarının yolları (isteğe bağlı, birden fazla olabilir, svg de olabilir).
- **-r, --resolution:** Çıktının yatay piksel sayısı. _(varsayılan: 1080)_
- **-f, --format:** Çıktı dosyası formatı _(varsayılan: "png")_.
- **-ts, --text_scale_factor:** Başlık boyutu. _(varsayılan: 1)_
- **-ls, --logo_scale_factor:** Logoların boyutu. _(varsayılan: 1)_
- **-mv, --min_version:** Oluşturulacak versiyon numaralarının en küçüğü. _(varsayılan 1, maksimumdan büyük olamaz)_
- **-xv, --max_version:** Oluşturulacak versiyon numaralarının en büyüğü. _(varsayılan 1, minimumdan küçük olamaz)_
- **-ilc, --is_logo_circle** Merkezdeki logonun dairesel mi yoksa kare mi olacağını belirler.
- **-bs, --border_size** Merkezdeki logonun etrafındaki boş alanın (quiet zone) genişliğini ayarlar. _(en fazla 0.15 önerilir)_
- **-bc, --border_color** Merkezdeki logonun kenarlık rengini belirler. _(varsayılan beyaz)_
- **-fgc, --foreground_color:** QR kodun ön plan rengi _(varsayılan: "black")_
- **-bgc, --background_color:** QR kodun arka plan rengi _(varsayılan: "white")_

## Örnek Kullanım:

```bash
python3 main.py "https://example.com" -o output -t "Örnek QR Kodu" -tc "blue" -i logo1.png logo2.svg -cl center_logo.png -r 2000 -f jpg -ls 1.2 -ts 1.3 -mv 4 -xv 12 -ilc -bs 0.03 -bc white -cls 0.2
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

- **margin:** Başlık metninin kenar boşluklarını ayarlar.
- **logo_max_size:** Logoların maksimum boyutunu belirler.

## Notlar

- SVG dosyaları otomatik olarak PNG'ye dönüştürülür.
- Logolar, orijinal en-boy oranlarını koruyarak yeniden boyutlandırılır.
- Başlık metni, QR kodunun genişliğine göre otomatik olarak kaydırılır.
