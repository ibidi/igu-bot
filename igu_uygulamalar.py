from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Uygulama:
    isim: str
    aciklama: str
    url: str
    emoji: str

class UygulamalarManager:
    def __init__(self):
        self.kategoriler: Dict[str, List[Uygulama]] = {
            "Sık Kullanılan": [
                Uygulama("Açık Erişim", "İGÜ Kurumsal Açık Erişim Arşivi", "https://acikerisim.gelisim.edu.tr", "📚"),
                Uygulama("GBS", "Gelişim Bilgi Sistemi", "https://gbs.gelisim.edu.tr", "💻"),
                Uygulama("İGUMER", "İGÜ Paydaş Görüş Ve Öneri Sistemi", "https://igumer.gelisim.edu.tr", "📝"),
                Uygulama("AVESİS", "Akademik Veri Yönetim Sistemi", "https://avesis.gelisim.edu.tr", "📊"),
                Uygulama("EBYS", "Elektronik Belge Yönetim Sistemi", "https://ebys.gelisim.edu.tr", "📄"),
                Uygulama("LMS", "Gelişim Üniversitesi E-Öğrenme Platformu", "https://lms.gelisim.edu.tr", "🎓"),
                Uygulama("OBİS", "Öğrenci Bilgi Sistemi", "https://obis.gelisim.edu.tr", "👨‍🎓"),
                Uygulama("ÖMS", "Öğrenci Mail Sistemi", "https://oms.gelisim.edu.tr", "📧"),
                Uygulama("PERSİS", "Personel Bilgi Sistemi", "https://persis.gelisim.edu.tr", "👥"),
                Uygulama("PMS", "Personel Mail Sistemi", "https://pms.gelisim.edu.tr", "📧"),
            ],
            "İdari": [
                Uygulama("KUTSİS", "Kütüphane Bilgi Sistemi", "https://kutsis.gelisim.edu.tr", "📚"),
                Uygulama("PERSİS", "Personel Bilgi Sistemi", "https://persis.gelisim.edu.tr", "👥"),
                Uygulama("KYS", "Kalite Yönetim Sistemi (QDMS)", "https://kys.gelisim.edu.tr", "✅"),
                Uygulama("MUHSİS", "Ön Muhasebe Bilgi Sistemi", "https://muhsis.gelisim.edu.tr", "💰"),
                Uygulama("SEMSİS", "Sürekli Eğitim Merkezi Bilgi Sistemi", "https://semsis.gelisim.edu.tr", "📚"),
                Uygulama("EBYS", "Elektronik Belge Yönetim Sistemi", "https://ebys.gelisim.edu.tr", "📄"),
                Uygulama("HALSİS", "Halkla İlişkiler Bilgi Sistemi", "https://halsis.gelisim.edu.tr", "👥"),
                Uygulama("PMS", "Personel Mail Sistemi", "https://pms.gelisim.edu.tr", "📧"),
                Uygulama("GUVSİS", "Güvenlik Bilgi Sistemi", "https://guvsis.gelisim.edu.tr", "🔒"),
                Uygulama("KARSİS", "Kariyer Birimi", "https://karsis.gelisim.edu.tr", "💼"),
                Uygulama("YAPSİS", "Yapı İşleri Bilgi Sistemi", "https://yapsis.gelisim.edu.tr", "🏗️"),
                Uygulama("REVSİS", "Revir Bilgi Sistemi", "https://revsis.gelisim.edu.tr", "🏥"),
            ],
            "Öğrenci": [
                Uygulama("METSİS", "Mezunlar ve Mensuplar Koordinatörlüğü", "https://metsis.gelisim.edu.tr", "🎓"),
                Uygulama("OBİS", "Öğrenci Bilgi Sistemi", "https://obis.gelisim.edu.tr", "👨‍🎓"),
                Uygulama("GBS", "Gelişim Bilgi Sistemi", "https://gbs.gelisim.edu.tr", "💻"),
                Uygulama("ÖMS", "Öğrenci Mail Sistemi", "https://oms.gelisim.edu.tr", "📧"),
                Uygulama("LMS", "E-Öğrenme Platformu", "https://lms.gelisim.edu.tr", "🎓"),
                Uygulama("Ön Kayıt", "Ön Kayıt Sistemi", "https://onkayit.gelisim.edu.tr", "📝"),
            ],
            "Aday Öğrenci": [
                Uygulama("Aday Sayfası", "Aday Web Sayfası", "https://aday.gelisim.edu.tr", "🎯"),
                Uygulama("Tercih Robotu", "Tercih Robotu", "https://tercihrobotu.gelisim.edu.tr", "🤖"),
                Uygulama("GELSİS", "Öğrenci İşleri Bilgi Sistemi", "https://gelsis.gelisim.edu.tr", "📊"),
            ],
            "Web Sayfaları": [
                Uygulama("Ana Sayfa", "Üniversite Web Sayfası", "https://www.gelisim.edu.tr", "🏛️"),
            ],
            "Diğer": [
                Uygulama("Form", "Başvuru Formları", "https://form.gelisim.edu.tr", "📝"),
                Uygulama("AVESİS", "Akademik Veri Yönetim Sistemi", "https://avesis.gelisim.edu.tr", "📊"),
                Uygulama("Açık Erişim", "İGÜ Kurumsal Açık Erişim Arşivi", "https://acikerisim.gelisim.edu.tr", "📚"),
                Uygulama("İGÜMER", "İGÜ Paydaş Görüş Ve Öneri Sistemi", "https://igumer.gelisim.edu.tr", "📝"),
            ],
        }

    def get_kategori_listesi(self) -> str:
        """Tüm kategorilerin listesini döndürür"""
        mesaj = "📱 IGÜ Uygulama Kategorileri:\n\n"
        for i, kategori in enumerate(self.kategoriler.keys(), 1):
            mesaj += f"{i}. {kategori}\n"
        mesaj += "\nKategori detayları için: /uygulamalar <kategori_adı>"
        return mesaj

    def get_kategori_detay(self, kategori: str) -> str:
        """Belirli bir kategorideki uygulamaların detaylarını döndürür"""
        kategori = kategori.title()  # İlk harfleri büyük yap
        if kategori not in self.kategoriler:
            return "❌ Böyle bir kategori bulunamadı. Kategorileri görmek için /uygulamalar yazın."
        
        mesaj = f"📱 {kategori} Uygulamaları\n"
        mesaj += "─" * 30 + "\n\n"
        
        for app in self.kategoriler[kategori]:
            mesaj += f"{app.emoji} {app.isim}\n"
            mesaj += f"├ {app.aciklama}\n"
            mesaj += f"└ {app.url}\n\n"
        
        return mesaj 