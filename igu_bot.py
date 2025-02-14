import telebot
import os
from dotenv import load_dotenv
from akademik_takvim import akademik_takvim_getir, get_fakulte_listesi
from igu_uygulamalar import UygulamalarManager
from telebot import types  # Butonlar için types'ı import ediyoruz
from igu_duyurular import DuyuruManager
import logging
import sys
from typing import List

# .env dosyasından bot token'ı yükleme
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Bot ve uygulama yöneticisi oluştur
bot = telebot.TeleBot(TOKEN)
uygulama_manager = UygulamalarManager()
duyuru_manager = DuyuruManager()

# Loglama ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    """Bot başlatıldığında çalışacak komut"""
    bot.reply_to(message, 
        'Merhaba! IGU Bot\'una hoş geldiniz! 🎓\n\n'
        'Kullanabileceğiniz komutlar:\n'
        '/yemek - Günlük yemek menüsü\n'
        '/iban - Üniversite IBAN bilgileri\n'
        # '/bilgiler - Üniversite iletişim bilgileri\n'
        '/duyurular - Son duyurular\n'
        '/takvim - Akademik takvim bilgileri\n'
        '/uygulamalar - IGÜ Uygulamaları'
    )

@bot.message_handler(commands=['yemek'])
def yemek(message):
    """Günlük yemek menüsünü gösteren komut"""
    bot.reply_to(message, 'Günün menüsü yakında burada olacak! 🍽️')

@bot.message_handler(commands=['iban'])
def iban(message):
    """Üniversite IBAN bilgilerini gösteren komut"""
    bot.reply_to(message,
        'İGÜ Banka Hesap Bilgileri:\n\n'
        'Banka: XXX Bank\n'
        'IBAN: TRXX XXXX XXXX XXXX XXXX XXXX XX'
    )

@bot.message_handler(commands=['bilgiler'])
def bilgiler(message):
    """Üniversite iletişim bilgilerini gösteren komut"""
    bot.reply_to(message,
        'İstanbul Gelişim Üniversitesi İletişim Bilgileri:\n\n'
        'Adres: Cihangir Mahallesi Şehit Jandarma Komando Er Hakan Öner Sk. No: 1 Avcılar / İSTANBUL\n'
        'Tel: 0212 422 70 00\n'
        'E-posta: info@gelisim.edu.tr'
    )

@bot.message_handler(commands=['takvim'])
def takvim(message):
    """Akademik takvim bilgilerini gösteren komut"""
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        takvim_bilgisi = akademik_takvim_getir()
    else:
        fakulte = args[0] if len(args) > 0 else None
        yil = args[1] if len(args) > 1 else None
        olay = args[2] if len(args) > 2 else None
        takvim_bilgisi = akademik_takvim_getir(fakulte, yil, olay)
    
    bot.reply_to(message, takvim_bilgisi)

@bot.message_handler(commands=['takvim_yardim'])
def takvim_yardim(message):
    """Takvim komutu için yardım mesajı"""
    bot.reply_to(message,
        'Akademik Takvim Kullanımı:\n\n'
        '/takvim - Tüm akademik takvim bilgilerini gösterir\n'
        '/takvim <fakülte> - Belirli bir fakültenin takvimini gösterir\n'
        '/takvim <fakülte> <yıl> - Belirli bir yıl için takvimi gösterir\n'
        '/takvim <fakülte> <yıl> <olay> - Spesifik bir dönem için bilgileri gösterir\n\n'
        'Örnek: /takvim "Mühendislik" "2023-2024" "GÜZ DÖNEMİ"'
    )

@bot.message_handler(commands=['fakulteler'])
def fakulte_listesi(message):
    """Mevcut fakültelerin listesini gösterir"""
    fakulteler = get_fakulte_listesi()
    if fakulteler:
        mesaj = "📚 Mevcut Fakülteler:\n\n"
        for fakulte in fakulteler:
            mesaj += f"• {fakulte}\n"
    else:
        mesaj = "Fakülte listesi şu anda alınamıyor."
    
    bot.reply_to(message, mesaj)

@bot.message_handler(commands=['uygulamalar'])
def uygulamalar(message):
    """IGÜ uygulamalarını kategorilere göre listeler"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Kategori butonlarını oluştur
    buttons = []
    for kategori in uygulama_manager.kategoriler.keys():
        callback_data = f"kategori_{kategori}"  # 64 karakterden kısa olmalı
        buttons.append(types.InlineKeyboardButton(
            text=f"📱 {kategori}",
            callback_data=callback_data
        ))
    
    # Butonları markup'a ekle
    markup.add(*buttons)
    
    bot.reply_to(
        message,
        "📱 Lütfen görüntülemek istediğiniz kategoriyi seçin:",
        reply_markup=markup
    )

def truncate_message(message: str, max_length: int = 4096) -> List[str]:
    """Uzun mesajları Telegram limitlerine uygun parçalara böler"""
    if len(message) <= max_length:
        return [message]
    
    parts = []
    while message:
        if len(message) <= max_length:
            parts.append(message)
            break
        
        # En yakın satır sonunu bul
        split_index = message.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = max_length
        
        parts.append(message[:split_index])
        message = message[split_index:].lstrip()
    
    return parts

# Uzun mesajları bölmek için kullan
@bot.callback_query_handler(func=lambda call: call.data.startswith('kategori_'))
def kategori_handler(call):
    kategori = call.data.replace('kategori_', '')
    mesaj = uygulama_manager.get_kategori_detay(kategori)
    
    # Mesajı parçalara böl
    mesaj_parcalari = truncate_message(mesaj)
    
    # İlk parçayı gönder
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "◀️ Ana Menüye Dön",
            callback_data="ana_menu"
        )
    )
    
    for i, parca in enumerate(mesaj_parcalari):
        if i == 0:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=parca,
                reply_markup=markup if i == len(mesaj_parcalari)-1 else None
            )
        else:
            # Ek parçaları yeni mesaj olarak gönder
            bot.send_message(
                chat_id=call.message.chat.id,
                text=parca,
                reply_markup=markup if i == len(mesaj_parcalari)-1 else None
            )

@bot.callback_query_handler(func=lambda call: call.data == "ana_menu")
def ana_menu_handler(call):
    """Ana menüye dönüş butonu için handler"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Kategori butonlarını tekrar oluştur
    buttons = []
    for kategori in uygulama_manager.kategoriler.keys():
        callback_data = f"kategori_{kategori}"
        buttons.append(types.InlineKeyboardButton(
            text=f"📱 {kategori}",
            callback_data=callback_data
        ))
    
    markup.add(*buttons)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📱 Lütfen görüntülemek istediğiniz kategoriyi seçin:",
        reply_markup=markup
    )

@bot.message_handler(commands=['duyurular'])
def duyurular(message):
    """Son duyuruları gösteren komut"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Duyuru ve slider butonları
    buttons = [
        types.InlineKeyboardButton("📢 Duyurular", callback_data="show_duyurular"),
        types.InlineKeyboardButton("🎯 Güncel Görseller", callback_data="show_sliders")
    ]
    markup.add(*buttons)
    
    bot.reply_to(
        message,
        "Lütfen görüntülemek istediğiniz kategoriyi seçin:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["show_duyurular", "show_sliders"])
def duyuru_slider_handler(call):
    """Duyuru veya slider seçildiğinde çalışacak handler"""
    if call.data == "show_duyurular":
        duyurular = duyuru_manager.get_duyurular()
        mesaj = duyuru_manager.format_duyuru_message(duyurular)
    else:
        sliders = duyuru_manager.get_sliders()
        mesaj = duyuru_manager.format_slider_message(sliders)
    
    # Geri dönüş butonu
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "◀️ Geri Dön",
            callback_data="duyuru_menu"
        )
    )
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=mesaj,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "duyuru_menu")
def duyuru_menu_handler(call):
    """Duyuru menüsüne dönüş butonu için handler"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("📢 Duyurular", callback_data="show_duyurular"),
        types.InlineKeyboardButton("🎯 Güncel Görseller", callback_data="show_sliders")
    ]
    markup.add(*buttons)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Lütfen görüntülemek istediğiniz kategoriyi seçin:",
        reply_markup=markup
    )

def main():
    """Bot'u başlat"""
    try:
        print("Bot başlatılıyor...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"Bot çalışırken hata oluştu: {e}")
        sys.exit(1)

# Hata yakalama için decorator ekleyelim
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__} fonksiyonunda hata: {e}")
            # Kullanıcıya hata mesajı gönder
            if len(args) > 0 and hasattr(args[0], 'message'):
                bot.reply_to(args[0].message, "⚠️ Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
    return wrapper

# Tüm handler'lara hata yakalama ekleyelim
@handle_errors
@bot.message_handler(commands=['start'])
def start(message):
    """Bot başlatıldığında çalışacak komut"""
    bot.reply_to(message, 
        'Merhaba! IGU Bot\'una hoş geldiniz! 🎓\n\n'
        'Kullanabileceğiniz komutlar:\n'
        '/yemek - Günlük yemek menüsü\n'
        '/iban - Üniversite IBAN bilgileri\n'
        # '/bilgiler - Üniversite iletişim bilgileri\n'
        '/duyurular - Son duyurular\n'
        '/takvim - Akademik takvim bilgileri\n'
        '/uygulamalar - IGÜ Uygulamaları'
    )

@handle_errors
@bot.message_handler(commands=['duyurular'])
def duyurular(message):
    """Son duyuruları gösteren komut"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Duyuru ve slider butonları
    buttons = [
        types.InlineKeyboardButton("📢 Duyurular", callback_data="show_duyurular"),
        types.InlineKeyboardButton("🎯 Güncel Görseller", callback_data="show_sliders")
    ]
    markup.add(*buttons)
    
    bot.reply_to(
        message,
        "Lütfen görüntülemek istediğiniz kategoriyi seçin:",
        reply_markup=markup
    )

if __name__ == '__main__':
    main() 