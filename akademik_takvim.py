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
        
        # Takvim tablosunu bul - farklı class'ları dene
        table = soup.find('table', {'class': ['table', 'table-bordered', 'akademik-takvim']})
        
        if not table:
            # Alternatif tablo arama yöntemi
            tables = soup.find_all('table')
            if tables:
                table = tables[0]  # İlk tabloyu al
            else:
                return "Akademik takvim tablosu bulunamadı."
        
        # Tablo başlıklarını al
        headers = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.text.strip())
        
        if not headers:
            headers = ['Akademik Yıl', 'Fakülte/Program Adı', 'İdari Olay', 'Başlangıç Tarihi', 'Bitiş Tarihi', 'Açıklama']
        
        # Tablo verilerini al
        rows = []
        for tr in table.find_all('tr')[1:]:  # İlk satırı (başlıkları) atla
            row = []
            for td in tr.find_all('td'):
                # HTML etiketlerini temizle
                text = ' '.join(td.stripped_strings)
                row.append(text)
            if row and len(row) >= len(headers):  # Geçerli satırları filtrele
                rows.append(row[:len(headers)])  # Başlık sayısı kadar veri al
        
        # DataFrame oluştur
        df = pd.DataFrame(rows, columns=headers)
        
        # Boş sütunları temizle
        df = df.dropna(how='all')
        
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
            try:
                takvim_mesaji += f"📍 {row.get('İdari Olay', 'Belirtilmemiş')}\n"
                takvim_mesaji += f"📚 {row.get('Fakülte/Program Adı', 'Tüm Fakülteler')}\n"
                takvim_mesaji += f"📅 {row.get('Başlangıç Tarihi', '')} - {row.get('Bitiş Tarihi', '')}\n"
                if pd.notna(row.get('Açıklama')):
                    takvim_mesaji += f"ℹ️ {row['Açıklama']}\n"
                takvim_mesaji += "\n"
            except Exception as e:
                logger.error(f"Satır formatlanırken hata: {str(e)}")
                continue
        
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
        
        # Farklı tablo class'larını dene
        table = soup.find('table', {'class': ['table', 'table-bordered', 'akademik-takvim']})
        
        if not table:
            tables = soup.find_all('table')
            if tables:
                table = tables[0]
            else:
                return []
        
        fakulteler = set()
        for tr in table.find_all('tr')[1:]:
            cells = tr.find_all('td')
            if len(cells) > 1:
                fakulte = cells[1].text.strip()
                if fakulte and fakulte != "Fakülte/Program Adı":
                    fakulteler.add(fakulte)
        
        return sorted(list(fakulteler))
    except Exception as e:
        logger.error(f"Fakülte listesi çekilirken hata oluştu: {str(e)}")
        return []

def debug_table_structure():
    """Tablo yapısını debug etmek için yardımcı fonksiyon"""
    try:
        response = requests.get("https://oidb.gelisim.edu.tr/tr/idari-akademik-takvim")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("Bulunan tablolar:")
        for i, table in enumerate(soup.find_all('table')):
            print(f"\nTablo {i+1}:")
            print(f"Class: {table.get('class', 'No class')}")
            print(f"ID: {table.get('id', 'No id')}")
            
            headers = []
            header_row = table.find('tr')
            if header_row:
                headers = [th.text.strip() for th in header_row.find_all(['th', 'td'])]
            print(f"Başlıklar: {headers}")
            
            row_count = len(table.find_all('tr'))
            print(f"Satır sayısı: {row_count}")
            
    except Exception as e:
        print(f"Hata: {str(e)}")

# Debug için çağır
if __name__ == "__main__":
    debug_table_structure() 