__version__ = "0.3.0"

# V0.3 2024-06-01 Mejoras en la interfaz gráfica ttkbootstrap, barra de progreso y manejo de errores
# V0.2 2023-08-10 Poder descargar listas de reproducción
#                 Cuando se descarga una lista, coloca numeración en el nombre del archivo
# V0.1 2021-07-01 Interfaz Gráfica
# V0.0 2021-07-01

# Crear entorno virtual
#python3 -m venv .venv # En Ubuntu  
#python -m venv .venv # En Windows
#Activar
# source .venv/bin/activate # En Ubuntu 
# .venv\Scripts\Activate # En Windows
# Librerías
# pip freeze > requirements.txt
# pip install -r requirements.txt


import yt_dlp
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import subprocess
from pathlib import Path
import platform

def obtener_carpeta_descargas():
    # Determina la carpeta de descargas según el sistema operativo
    sistema = platform.system()
    
    if sistema == "Windows":
        return Path.home() / "Downloads"
    
    elif sistema == "Linux":
        try:
            resultado = subprocess.run(
                ["xdg-user-dir", "DOWNLOAD"],
                capture_output=True, text=True, timeout=2
            )
            ruta = resultado.stdout.strip()
            if ruta:
                return Path(ruta)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        # Fallback si xdg-user-dir no está disponible
        return Path.home() / "Descargas"
    
    else:  # macOS u otros
        return Path.home() / "Downloads"

def log(msg):
    log_box.insert("end", msg + "\n")
    log_box.see("end")

def progreso(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        try:
            progress['value'] = float(p)
        except:
            pass
    elif d['status'] == 'finished':
        progress['value'] = 100

def descargar():

    url = url_entry.get().strip()
    formato = formato_var.get()
    carpeta = carpeta_entry.get().strip()

    if not url:
        log("Ingrese una URL válida")
        return

    log(f"Iniciando descarga: {url}")

    if formato == "mp4 best":
        formato_ytdlp = "bv*[vcodec^=avc]+ba[acodec^=mp4a]/b[vcodec^=avc]/b"
    elif formato == "mp4 low":
        formato_ytdlp = "b[vcodec^=avc][height<=240]/b"
    else:
        formato_ytdlp = "ba/b"

    opciones = {
        "format": formato_ytdlp,
        "outtmpl": f"{carpeta}/%(playlist_index)03d - %(title)s.%(ext)s",
        "nooverwrites": True,
        "ignoreerrors": True,
        "noplaylist": False,
        "concurrent_fragment_downloads": 4,   # descarga más rápida
        "progress_hooks": [progreso],
    }

    if formato == "mp3":
        opciones["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "96"
        }]

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        log("Descarga finalizada\n")
    except Exception as e:
        log(f"Error: {e}")

def descargar_thread():
    t = threading.Thread(target=descargar)
    t.start()


# -------- UI --------

app = ttk.Window(themename="darkly")
app.title("EC4LAB - Video Downloader")
# si existe el archivo icono.png, se establece como icono de la aplicación
if Path("icono.png").exists():
    app.iconphoto(False, ttk.PhotoImage(file="icono.png"))
app.geometry("520x420")

main = ttk.Frame(app, padding=20)
main.pack(fill=BOTH, expand=True)

ANCHO = 40

# URL
ttk.Label(main, text="URL").grid(row=0, column=0, sticky="w", pady=5)

url_entry = ttk.Entry(main, width=ANCHO)
url_entry.grid(row=0, column=1, sticky="w", pady=5)

# Formato
ttk.Label(main, text="Formato").grid(row=1, column=0, sticky="w", pady=5)

formato_var = ttk.StringVar(value="mp4 low")

formato_menu = ttk.Combobox(
    main,
    textvariable=formato_var,
    values=["mp4 best","mp4 low","mp3"],
    state="readonly",
    width=ANCHO-2
)
formato_menu.grid(row=1, column=1, sticky="w", pady=5)

# Carpeta
ttk.Label(main, text="Carpeta").grid(row=2, column=0, sticky="w", pady=5)

carpeta_entry = ttk.Entry(main, width=ANCHO)
carpeta_entry.insert(0, str(obtener_carpeta_descargas()))
carpeta_entry.grid(row=2, column=1, sticky="w", pady=5)

# Botón descargar
ttk.Button(
    main,
    text="Descargar",
    bootstyle="success",
    command=descargar_thread,
    width=20
).grid(row=3, column=1, sticky="w", pady=10)

# Barra progreso
progress = ttk.Progressbar(
    main,
    orient="horizontal",
    length=380,
    mode="determinate",
    bootstyle="success-striped"
)
progress.grid(row=4, column=0, columnspan=2, pady=10)

# Log
log_box = ttk.Text(main, height=10)
log_box.grid(row=5, column=0, columnspan=2, sticky="nsew")

# Expandir log
main.columnconfigure(1, weight=1)
main.rowconfigure(5, weight=1)

app.mainloop()
