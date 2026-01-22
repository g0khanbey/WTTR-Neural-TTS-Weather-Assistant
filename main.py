import tkinter as tk
import requests
import threading
import asyncio
import edge_tts
import pygame

# ---------- Weather ----------
def get_weather(city=None):
    url = f"https://wttr.in/{city}?format=j1" if city else "https://wttr.in/?format=j1"
    return requests.get(url, timeout=8).json()

# ---------- Translate ----------
def turkce(desc):
    d = desc.lower()
    if "drizzle" in d: return "Hafif çisenti"
    if "sun" in d or "clear" in d: return "Açık"
    if "cloud" in d: return "Bulutlu"
    if "rain" in d: return "Yağmurlu"
    if "snow" in d: return "Karlı"
    if "storm" in d: return "Fırtınalı"
    if "fog" in d or "mist" in d: return "Sisli"
    return desc

def icon(desc):
    d = desc.lower()
    if "drizzle" in d: return "🌦️"
    if "sun" in d or "clear" in d: return "☀️"
    if "cloud" in d: return "☁️"
    if "rain" in d: return "🌧️"
    if "snow" in d: return "❄️"
    if "storm" in d: return "⛈️"
    if "fog" in d or "mist" in d: return "🌫️"
    return "🌤️"

# ---------- Day Data ----------
def gun_karti(weather_day):
    h = weather_day["hourly"]
    slots = {"Sabah": h[2], "Öğle": h[4], "Akşam": h[6], "Gece": h[7]}
    out = {}
    for k,v in slots.items():
        desc = v["weatherDesc"][0]["value"]
        out[k] = {"temp": v["tempC"], "desc": turkce(desc), "icon": icon(desc)}
    return out

# ---------- TTS Text ----------
def bugun_ses_metin(weather_day):
    h = weather_day["hourly"]
    slots = {
        "sabahleyin": h[2],
        "öğlenleyin": h[4],
        "akşam": h[6],
        "gece": h[7],
    }
    text = "Bugünkü hava durumu tahmini şu şekilde. "
    for k,v in slots.items():
        desc = turkce(v["weatherDesc"][0]["value"])
        temp = v["tempC"]
        text += f"{k} {desc} bekleniyor, sıcaklık {temp} derece. "
    return text

# ---------- Neural TTS ----------
async def tts_play(text):
    communicate = edge_tts.Communicate(text, "tr-TR-EmelNeural")
    await communicate.save("tts.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("tts.mp3")
    pygame.mixer.music.play()

def speak_async():
    if today_weather:
        text = bugun_ses_metin(today_weather)
        threading.Thread(target=lambda: asyncio.run(tts_play(text))).start()

# ---------- GUI Drawing ----------
def draw_day(frame, title, data):
    for w in frame.winfo_children(): w.destroy()
    tk.Label(frame, text=title, font=("Segoe UI",14,"bold"),
             fg="cyan", bg="#1e1e2f").grid(row=0,column=0,columnspan=4)

    col = 0
    for part in ["Sabah","Öğle","Akşam","Gece"]:
        d = data[part]
        tk.Label(frame, text=part, fg="white", bg="#1e1e2f",
                 font=("Segoe UI",10,"bold")).grid(row=1,column=col,padx=10)

        txt = f"{d['icon']}\n{d['temp']}°C\n{d['desc']}"
        tk.Label(frame, text=txt, fg="white", bg="#1e1e2f",
                 font=("Segoe UI",11), justify="center").grid(row=2,column=col,padx=10,pady=5)
        col += 1

# ---------- Load ----------
today_weather = None

def load(city=None):
    global today_weather
    try:
        data = get_weather(city)
        area = data["nearest_area"][0]["areaName"][0]["value"]

        now = data["current_condition"][0]
        now_desc = now["weatherDesc"][0]["value"]

        header.config(
            text=f"Şu an: {icon(now_desc)} {turkce(now_desc)} — {now['temp_C']}°C (Hissedilen {now['FeelsLikeC']}°C)"
        )

        today_weather = data["weather"][0]

        draw_day(today_frame, "Bugün", gun_karti(data["weather"][0]))
        draw_day(tomorrow_frame, "Yarın", gun_karti(data["weather"][1]))
        draw_day(next_frame, "Öbür Gün", gun_karti(data["weather"][2]))

        status.config(text="")
    except:
        status.config(text="Veri alınamadı")

def auto_load():
    status.config(text="Otomatik Konum Verisi İleYükleniyor...")
    threading.Thread(target=lambda: load(None)).start()

def manual():
    city = entry.get().strip()
    if city:
        status.config(text="Yükleniyor...")
        threading.Thread(target=lambda: load(city)).start()

# ---------- UI ----------
root = tk.Tk()
root.title("WTTR Hava Asistanı")
root.geometry("720x750")
root.configure(bg="#1e1e2f")

tk.Label(root, text="WTTR Hava Asistanı", font=("Segoe UI",20),
         fg="white", bg="#1e1e2f").pack(pady=5)

entry = tk.Entry(root, font=("Segoe UI",14), justify="center")
entry.pack(pady=5)

tk.Button(root, text="Şehir Ara", font=("Segoe UI",12), command=manual).pack()

tk.Button(root, text="🔊 Bugünü Seslendir", font=("Segoe UI",12),
          command=speak_async).pack(pady=4)

status = tk.Label(root, text="", fg="yellow", bg="#1e1e2f")
status.pack()

header = tk.Label(root, text="", font=("Segoe UI",14),
                  fg="white", bg="#1e1e2f")
header.pack(pady=8)

today_frame = tk.Frame(root, bg="#1e1e2f")
today_frame.pack(pady=10)

tomorrow_frame = tk.Frame(root, bg="#1e1e2f")
tomorrow_frame.pack(pady=10)

next_frame = tk.Frame(root, bg="#1e1e2f")
next_frame.pack(pady=10)

root.after(300, auto_load)
root.mainloop()
