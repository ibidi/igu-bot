import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
from datetime import datetime
import logging

@dataclass
class Slider:
    baslik: str
    aciklama: str
    resim_url: str
    link: str

@dataclass
class Duyuru:
    baslik: str
    tarih: str
    link: str

class DuyuruManager:
    def __init__(self):
        self.base_url = "https://www.gelisim.edu.tr"
        
    def get_sliders(self) -> List[Slider]:
        """Ana sayfadaki slider görsellerini çeker"""
        try:
            response = requests.get(f"{self.base_url}/tr/gelisim-anasayfa")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            sliders = []
            slider_container = soup.find('div', {'class': 'carousel-inner'})
            
            if slider_container:
                for item in slider_container.find_all('div', {'class': 'carousel-item'}):
                    baslik = item.find('h2').text.strip() if item.find('h2') else ""
                    aciklama = item.find('p').text.strip() if item.find('p') else ""
                    resim = item.find('img')
                    resim_url = f"{self.base_url}{resim['src']}" if resim and resim.get('src') else ""
                    link = item.find('a')['href'] if item.find('a') else ""
                    
                    if link and not link.startswith('http'):
                        link = f"{self.base_url}{link}"
                    
                    sliders.append(Slider(
                        baslik=baslik,
                        aciklama=aciklama,
                        resim_url=resim_url,
                        link=link
                    ))
            
            return sliders
            
        except Exception as e:
            logging.error(f"Slider verileri çekilirken hata oluştu: {str(e)}")
            return []

    def get_duyurular(self) -> List[Duyuru]:
        """Ana sayfadaki duyuruları çeker"""
        try:
            response = requests.get(f"{self.base_url}/tr/gelisim-anasayfa")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            duyurular = []
            duyuru_container = soup.find('div', {'class': 'duyurular'})
            
            if duyuru_container:
                for item in duyuru_container.find_all('div', {'class': 'duyuru-item'}):
                    baslik = item.find('h3').text.strip() if item.find('h3') else ""
                    tarih = item.find('span', {'class': 'tarih'}).text.strip() if item.find('span', {'class': 'tarih'}) else ""
                    link = item.find('a')['href'] if item.find('a') else ""
                    
                    if link and not link.startswith('http'):
                        link = f"{self.base_url}{link}"
                    
                    duyurular.append(Duyuru(
                        baslik=baslik,
                        tarih=tarih,
                        link=link
                    ))
            
            return duyurular
            
        except Exception as e:
            logging.error(f"Duyurular çekilirken hata oluştu: {str(e)}")
            return []

    def format_slider_message(self, sliders: List[Slider]) -> str:
        """Slider bilgilerini mesaj formatına çevirir"""
        if not sliders:
            return "❌ Slider bilgileri alınamadı."
        
        mesaj = "🎯 Güncel Slider Görselleri\n"
        mesaj += "─" * 30 + "\n\n"
        
        for i, slider in enumerate(sliders, 1):
            mesaj += f"📌 {slider.baslik}\n"
            if slider.aciklama:
                mesaj += f"└ {slider.aciklama}\n"
            if slider.link:
                mesaj += f"└ 🔗 {slider.link}\n"
            mesaj += "\n"
            
        return mesaj

    def format_duyuru_message(self, duyurular: List[Duyuru]) -> str:
        """Duyuruları mesaj formatına çevirir"""
        if not duyurular:
            return "❌ Duyuru bulunamadı."
        
        mesaj = "📢 Son Duyurular\n"
        mesaj += "─" * 30 + "\n\n"
        
        for duyuru in duyurular:
            mesaj += f"📌 {duyuru.baslik}\n"
            mesaj += f"└ 📅 {duyuru.tarih}\n"
            if duyuru.link:
                mesaj += f"└ 🔗 {duyuru.link}\n"
            mesaj += "\n"
            
        return mesaj 