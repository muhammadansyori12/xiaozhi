from fastapi import FastAPI, Request
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Server Pendukung Xiaozhi Menyala!"}

@app.post("/play")
async def play_music(request: Request):
    try:
        # Menangkap data yang dikirim dari Dashboard Xiaozhi
        data = await request.json()
        
        # Mengambil judul lagu dari data (Default: "lagu viral" jika kosong)
        judul_lagu = data.get("judul", "lagu viral") 
        
        # Proses pencarian YouTube rahasia menggunakan yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(judul_lagu, download=False)
            audio_url = info['entries'][0]['url'] # Ini URL MP3 streamingnya
            
        # Mengirimkan balasan ke ESP32/Xiaozhi
        return {
            "status": "success",
            "audio_url": audio_url,
            "pesan": f"Memutar {judul_lagu}"
        }
        
    except Exception as e:
        return {"status": "error", "pesan": "Gagal mencari lagu."}
