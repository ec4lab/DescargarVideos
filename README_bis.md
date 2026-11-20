# Descargar Videos

Programa en python para descargar videos de la web, en formato mp4 o solo el audio en mp3. Con interfaz gráfica realizada en  ttkbootstrap


Funciona Con you tube
you tube music
instagram # si el video se ve sin estar logeado.
tiktok

## exe

Con el programa descargado, el entorno virtual creado e instalado requirements.txt, se debe instalar `pyinstaller`para generar el binario

```bash
pip install pyinstaller  
``` 

pyinstaller --onefile descargar_youtube_V1.3.py
(ver que pasa con el icono)

```bash
pyinstaller --onefile --noconsole --icon=icono.png --hidden-import=PIL._tkinter_finder --collect-all ttkbootstrap --collect-all PIL DownVideo.py
```




## Generar app en Ubuntu

Con el programa descargado, el entorno virtual creado e instalado requirements.txt, se debe instalar `pyinstaller`para generar el binario

```bash
pip install pyinstaller  
```

y luego ejecutar:

```bash
pyinstaller --onefile --noconsole --icon=icono.png \
  --hidden-import=PIL._tkinter_finder \
  --collect-all ttkbootstrap \
  --collect-all PIL \
  DownVideo.py
```

Esto genera varios archivos y carpetas, lo que interesa es:

```text
/DescargarVideos
└── dist/
    └── DownVideo
```

Se debe copiar el binario `dist/DownVideo` e `icono.png` a una carpeta definitiva, por ejemplo 'home/USUARIO/soft/', entonces en el mismo terminal de VSCode

```bash
mkdir ~/soft/
mkdir ~/soft/DownVideo/
cp dist/DownVideo ~/soft/DownVideo/DownVideo
cp icono.png ~/soft/DownVideo/icono.png
```

entonces

```text
/home/USUARIO/soft
              └── DownVideo/
                      ├── DownVideo
                      └── icono.png
```

En este punto es posible ejecutar directamente el binario, haciendo doble click o con click derecho `Ejecutar`, pero Nautilus no siempre funciona bien, además es probable que abra un terminal, asi que para evitar inconvenientes es posible agregar la app al menú de aplicaciones.

Se debe crear un archivo `.desktop`

```bash
sudo nano ~/.local/share/applications/downvideo.desktop
```

y dentro pegar

```text
[Desktop Entry]
Type=Application
Name=DownVideo
Comment=Descargar videos de YouTube
Exec=/home/martin/Soft/DownVideo/DownVideo
Icon=/home/martin/Soft/DownVideo/icono.png
Terminal=false
Categories=Utility;AudioVideo;
```

Hacer ejecutable el archivo

```bash
sudo chmod +x ~/.local/share/applications/downvideo.desktop
```

Luego hay que marcarlo como confiable

```bash
gio set ~/.local/share/applications/downvideo.desktop metadata::trusted true
```

y refrescar la base de datos de aplicaciones

```bash
update-desktop-database ~/.local/share/applications/
```

>[!TIP]  
>Si todavía no aparece en las app, cerrar sesión y volver a ingresar

### Ahora un script para automatizar la creación de la app