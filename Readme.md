# İşletme Arama Botu

Bu proje, Google üzerinde belirlenen şehir, ilçe ve kategoriye göre işletme araması yaparak bilgileri çekip Excel dosyası olarak kaydeden bir Python uygulamasıdır.

## Özellikler

- Şehir, ilçe ve kategori bazlı arama yapma
- Google arama sonuçlarından işletme bilgilerini çekme
- İşletme adı, adres, telefon numarası, yıldız puanı ve değerlendirme sayısını kaydetme
- Kullanıcı dostu arayüz (Tkinter ile)
- Çıktıları Excel (.xlsx) formatında kaydetme

## Gereksinimler

Bu projeyi çalıştırmadan önce aşağıdaki bağımlılıkları yüklediğinizden emin olun:

```bash
./install_requirements.bat
```

Ayrıca, Chrome tarayıcısının bilgisayarınızda yüklü olması gerekmektedir.

## Kurulum

1. Depoyu klonlayın veya dosyaları indirin.
2. Bağımlılıkları yükleyin.
3. `cities_districts.json` ve `categories.json` dosyalarını uygun şekilde doldurun.
4. Projeyi çalıştırın:

```bash
python main.py
```

## Kullanım

1. Uygulamayı başlatın.
2. Şehir, ilçe ve kategori seçin.
3. Arama için bir isim girin.
4. Hangi bilgilerin Excel dosyasına kaydedileceğini belirleyin.
5. "Ara ve Kaydet" butonuna basarak işlemi başlatın.

Sonuçlar, çalışma dizinine belirtilen isimle `.xlsx` formatında kaydedilecektir.

## Hata ve Sorunlar

- Eğer `cities_districts.json` veya `categories.json` dosyaları eksikse, program hata verecektir.
- Google sonuçları bazen değişebilir, bu yüzden XPath veya HTML etiketleri güncellenmesi gerekebilir.
- ChromeDriver güncel değilse, `webdriver-manager` kullanarak güncelleyin.

## Katkıda Bulunma

Herhangi bir geliştirme öneriniz veya hatayı düzeltme isteğiniz varsa, lütfen bir pull request oluşturun veya issue açın.

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.