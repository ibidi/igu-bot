# 🎓 IGU Telegram Bot

İstanbul Gelişim Üniversitesi öğrencileri için geliştirilmiş kapsamlı bir Telegram botu. Bu bot, öğrencilerin üniversite ile ilgili güncel bilgilere hızlı ve kolay erişimini sağlar.

## 🌟 Özellikler

### 📱 Üniversite Uygulamaları
- Tüm IGÜ web uygulamalarına kategorize edilmiş erişim
- Sık kullanılan sistemler (OBİS, LMS, vb.)
- İdari sistemler
- Öğrenci sistemleri
- Aday öğrenci portalları

### 📢 Güncel Bilgiler
- Üniversite duyuruları
- Güncel slider görselleri
- Etkinlik ve haberler

### 📅 Akademik Bilgiler
- Akademik takvim sorgulama
- Fakülte bazlı filtreleme
- Tarih ve dönem bazlı arama

### 💡 Diğer Özellikler
- Yemek menüsü (Yakında)
- IBAN bilgileri
- İletişim bilgileri

## 🛠️ Teknolojiler

- Python 3.x
- pyTelegramBotAPI
- Requests

## 🚀 Kurulum

1. Repository'yi klonlayın ve gerekli paketleri yükleyin:
   ```bash
   git clone https://github.com/ibidi/igu-bot.git
   cd igu-bot
   pip install pyTelegramBotAPI python-dotenv requests beautifulsoup4 pandas
   ```

2. `.env` dosyasını oluşturun ve Telegram Bot Token'ınızı ekleyin:
   ```bash
   BOT_TOKEN=your_telegram_bot_token_here
   ```

3. Botu çalıştırın:
   ```bash
   python3 igu_bot.py
   ```

## 📱 Kullanım

Telegram'da botu başlatmak için:
1. @IGU_Bot'u arayın
2. /start komutunu gönderin
3. Menüden istediğiniz özelliği seçin

Mevcut komutlar:
- `/start` - Bot'u başlatır ve mevcut komutları listeler
- `/yemek` - Günlük yemek menüsünü gösterir
- `/iban` - Üniversite IBAN bilgilerini gösterir
- `/duyurular` - Son duyurular ve güncel görselleri gösterir
- `/takvim` - Akademik takvim bilgilerini gösterir
- `/fakulteler` - Fakülte listesini gösterir
- `/uygulamalar` - IGÜ uygulamalarını kategorilere göre listeler

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak için:
1. Bu repository'yi fork'layın
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit'leyin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push'layın (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
