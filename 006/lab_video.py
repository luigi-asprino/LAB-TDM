"""Funzioni di supporto per il laboratorio 6. Nessun download richiesto."""
from pathlib import Path
import shutil
import subprocess
import numpy as np

WIDTH, HEIGHT, FPS, N_FRAMES = 320, 180, 24, 120
CRFS = (18, 28, 38)
NAMES = ('lento', 'veloce')

def genera_clip(velocita):
    """Stessa scena e stessa traiettoria periodica, percorse a velocità diverse."""
    y, x = np.indices((HEIGHT, WIDTH))
    bg = np.stack((35 + x % 70, 45 + y % 65, 55 + (x+y) % 55), axis=-1).astype(np.uint8)
    ty, tx = np.indices((48, 48))
    tile = np.stack((60 + 150*((tx//4+ty//4)%2), 70+tx*3, 210-ty*3), axis=-1).astype(np.uint8)
    frames = np.repeat(bg[None], N_FRAMES, axis=0)
    for t in range(N_FRAMES):
        pos = 16 + (velocita*t) % 240
        frames[t, 66:114, pos:pos+48] = tile
    return frames

def grigio(frame):
    """Luma approssimata per la demo, da RGB non lineare; non luminanza fisica."""
    return np.asarray(frame, dtype=np.float32) @ np.array([.299, .587, .114], dtype=np.float32)

def cerca_blocco(precedente, corrente, x, y, lato=16, raggio=12):
    """Trova nel precedente il predittore del blocco corrente mediante SAD.
    Vettore restituito: posizione nel riferimento meno posizione nel corrente.
    """
    a, b = grigio(precedente), grigio(corrente)
    target = b[y:y+lato, x:x+lato]
    if target.shape != (lato, lato):
        raise ValueError('Blocco fuori immagine')
    best = None
    for dy in range(-raggio, raggio+1):
        for dx in range(-raggio, raggio+1):
            xx, yy = x+dx, y+dy
            if xx < 0 or yy < 0 or xx+lato > a.shape[1] or yy+lato > a.shape[0]:
                continue
            pred = a[yy:yy+lato, xx:xx+lato]
            sad = float(np.abs(target-pred).sum())
            key = (sad, dx*dx+dy*dy)
            if best is None or key < best[0]:
                best = (key, dx, dy, pred.copy())
    return (best[1], best[2]), target-a[y:y+lato, x:x+lato], target-best[3]

def codifica(frames, path, crf):
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise RuntimeError('FFmpeg non trovato: usare le codifiche fornite.')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WIDTH}x{HEIGHT}',
           '-r', str(FPS), '-i', 'pipe:0', '-an', '-c:v', 'libx264',
           '-preset', 'fast', '-crf', str(crf), '-pix_fmt', 'yuv420p',
           '-g', '48', '-movflags', '+faststart', str(path)]
    result = subprocess.run(cmd, input=frames.tobytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace'))

def decodifica(path):
    result = subprocess.run([shutil.which('ffmpeg') or 'ffmpeg', '-v', 'error',
        '-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return np.frombuffer(result.stdout, dtype=np.uint8).reshape(-1, HEIGHT, WIDTH, 3)

def misura(originale, ricostruito, path):
    if originale.shape != ricostruito.shape:
        raise ValueError('Numero o dimensioni dei frame differenti')
    # MSE globale sui campioni RGB, poi PSNR; non media dei PSNR per frame.
    mse = float(np.mean((originale.astype(np.float32)-ricostruito.astype(np.float32))**2))
    durata = len(originale)/FPS
    byte = Path(path).stat().st_size
    return dict(byte=byte, bitrate_kbps=byte*8/durata/1000,
                mse_rgb=mse, psnr_rgb_db=float(10*np.log10(255**2/mse)) if mse else float('inf'))
