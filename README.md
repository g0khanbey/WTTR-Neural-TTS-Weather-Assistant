# 🌤️ WTTR Neural TTS Weather Assistant

WTTR Neural TTS Weather Assistant, Python ile geliştirilmiş, WTTR.in üzerinden hava durumu verisi alan ve bu verileri Türkçe olarak seslendiren modern bir masaüstü hava asistanıdır.  
Uygulama, günlük hava tahminini sabah, öğle, akşam ve gece olarak görsel ve sesli şekilde sunar.

---

## 🚀 Özellikler

- 🌍 Otomatik konumdan hava durumu
- 🔎 Şehir adına göre manuel arama
- ☀️ Bugün / Yarın / Öbür Gün tahmin kartları
- 🧠 Akıllı hava durumu sınıflandırması
- 🌡️ Sıcaklık ve hissedilen sıcaklık gösterimi
- 🎤 Neural Türkçe seslendirme (Microsoft Edge TTS)
- 🖥️ Modern koyu temalı Tkinter arayüz
- ⚡ Anlık WTTR.in API verileri

---

## 🖼️ Arayüz

Uygulama 4 zaman dilimi gösterir:

| Zaman |
|------|
| Sabah |
| Öğle |
| Akşam |
| Gece |

Her bölümde:
- Hava durumu ikonu
- Sıcaklık
- Türkçe açıklama

bulunur.

---

## 🔊 Sesli Hava Durumu

“Bugünü Seslendir” butonuna basıldığında sistem şunu üretir:

> Bugünkü hava durumu tahmini şu şekilde.  
> Sabahleyin açık bekleniyor, sıcaklık 18 derece…  

Seslendirme Microsoft **Neural Türkçe ses motoru** kullanır.

---

## 📦 Gereksinimler

Python 3.9+

```bash
pip install requests edge-tts pygame
