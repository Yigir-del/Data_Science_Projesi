# 📊 WhatsApp Chat Analizi Projesi

Bu proje, bir WhatsApp konuşma dosyasını (".txt" formatında dışa aktarılmış) okuyarak, kullanıcı bazlı analizler üretir ve görselleştirmeler sunar. Python, pandas ve regex temelli geliştirilmiştir.

## 🚀 Özellikler

- Katılımcıların:
  - En çok kullandığı kelimeler
  - En çok ettiği küfürler 😅
  - En çok sevgi sözcüğü kullandığı kelimeler 💕
  - En aktif oldukları ay, saat ve dakika bilgisi
  - Toplam kelime sayısı
- Zaman bazlı (aylık, saatlik, dakikalık) detaylı analiz
- Geliştirici moduyla tüm kullanıcıların zaman içindeki etkileşimleri
- Hazır görselleştirme fonksiyonları (`viz_engine.py` üzerinden)

## 🧠 Kullanım

### 1. Gerekli Dosyalar

Aşağıdaki dosyaların aynı klasörde bulunması gerekir:

- `chat.txt` → WhatsApp dışa aktarılmış konuşma dosyası (UTF-8 formatında)
- `hakaretler.py` → Hakaret kelimelerini içeren liste: `kelimeler = ["..."]`
- `sevgi_sozcukleri.py` → Sevgi içerikli kelimeler: `kelimeler = ["..."]`
- `stop_words.py` → Gereksiz kelimeleri tutan liste: `liste = ["..."]`
- `viz_engine.py` → Görselleştirme fonksiyonlarını içeren sınıf

### 2. Ana Script

```python
from whatsapp_analiz import WhatsappAnalizi
import viz_engine

obj = WhatsappAnalizi("chat.txt")
veriler = obj.df_by_choice("dev")  # "user" da seçebilirsin

gobj = viz_engine.WhatsappAnaliziGrafiks()
gobj.grafik_aylik_dagilim(veriler["month"])
