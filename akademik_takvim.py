import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging  # En üste ekleyin

# Logger'ı tanımla
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def akademik_takvim_getir(fakulte=None, yil=None, olay=None):
    """Akademik takvim bilgilerini web sitesinden çeker"""
    url = "https://oidb.gelisim.edu.tr/tr/idari-akademik-takvim"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Takvim tablosunu bul
        table = soup.find('table', {'class': 'table'})
        
        if not table:
            return "Akademik takvim tablosu bulunamadı."
        
        # Tablo başlıklarını al
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())
        
        # Tablo verilerini al
        rows = []
        for tr in table.find_all('tr')[1:]:  # İlk satırı (başlıkları) atla
            row = []
            for td in tr.find_all('td'):
                row.append(td.text.strip())
            if row:  # Boş satırları filtrele
                rows.append(row)
        
        # DataFrame oluştur
        df = pd.DataFrame(rows, columns=headers)
        
        # Filtreleme yap
        if fakulte:
            df = df[df['Fakülte/Program Adı'].str.contains(fakulte, case=False, na=False)]
        if yil:
            df = df[df['Akademik Yıl'].str.contains(yil, case=False, na=False)]
        if olay:
            df = df[df['İdari Olay'].str.contains(olay, case=False, na=False)]
        
        # Sonuçları formatla
        takvim_mesaji = "📅 İGÜ Akademik Takvim Bilgileri\n\n"
        
        if fakulte or yil or olay:
            takvim_mesaji += "Filtreleme Kriterleri:\n"
            if fakulte:
                takvim_mesaji += f"📚 Fakülte: {fakulte}\n"
            if yil:
                takvim_mesaji += f"📆 Akademik Yıl: {yil}\n"
            if olay:
                takvim_mesaji += f"📌 Olay Türü: {olay}\n"
            takvim_mesaji += "\n"
        
        if len(df) == 0:
            return takvim_mesaji + "❌ Belirtilen kriterlere uygun sonuç bulunamadı."
        
        # En fazla 10 sonuç göster
        for _, row in df.head(10).iterrows():
            takvim_mesaji += f"📍 {row['İdari Olay']}\n"
            takvim_mesaji += f"📚 {row['Fakülte/Program Adı']}\n"
            takvim_mesaji += f"📅 {row['Başlangıç Tarihi']} - {row['Bitiş Tarihi']}\n"
            if pd.notna(row.get('Açıklama', '')):
                takvim_mesaji += f"ℹ️ {row['Açıklama']}\n"
            takvim_mesaji += "\n"
        
        if len(df) > 10:
            takvim_mesaji += f"\n... ve {len(df) - 10} etkinlik daha.\n"
            takvim_mesaji += "Daha spesifik sonuçlar için filtreleme kullanabilirsiniz."
        
        return takvim_mesaji
        
    except Exception as e:
        logger.error(f"Akademik takvim çekilirken hata oluştu: {str(e)}")
        return "Akademik takvim bilgileri şu anda alınamıyor. Lütfen daha sonra tekrar deneyin."

def get_fakulte_listesi():
    """Mevcut fakültelerin listesini döndürür"""
    try:
        response = requests.get("https://oidb.gelisim.edu.tr/tr/idari-akademik-takvim")
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        
        fakulteler = set()
        for tr in table.find_all('tr')[1:]:
            fakulte = tr.find_all('td')[1].text.strip()
            if fakulte:
                fakulteler.add(fakulte)
        
        return sorted(list(fakulteler))
    except:
        return [] 