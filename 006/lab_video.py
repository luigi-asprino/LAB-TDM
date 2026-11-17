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

def _ffmpeg():
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise RuntimeError('FFmpeg non trovato: usare le codifiche fornite.')
    return ffmpeg

def codifica(frames, path, crf, gop=48):
    """Codifica H.264 (libx264). gop = intervallo massimo fra keyframe (-g)."""
    ffmpeg = _ffmpeg()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WIDTH}x{HEIGHT}',
           '-r', str(FPS), '-i', 'pipe:0', '-an', '-c:v', 'libx264',
           '-preset', 'fast', '-crf', str(crf), '-pix_fmt', 'yuv420p',
           '-g', str(gop), '-movflags', '+faststart', str(path)]
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
                mse_rgb=mse, psnr_rgb_db=psnr(mse))

def psnr(mse):
    """PSNR in dB per campioni a 8 bit, a partire da un MSE già calcolato."""
    return float(10*np.log10(255**2/mse)) if mse else float('inf')

# --- Separare la perdita del 4:2:0 da quella della codifica -----------------

def _ffmpeg_raw(args, dati):
    result = subprocess.run([_ffmpeg(), '-v', 'error'] + args, input=dati,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return result.stdout

def rgb_a_yuv420(frames):
    """Converte i frame RGB in YUV 4:2:0 con la stessa conversione usata da `codifica`.
    È il segnale che entra davvero nell'encoder. Restituisce (Y, U, V):
    Y ha forma (N, H, W), U e V hanno forma (N, H/2, W/2).
    """
    raw = _ffmpeg_raw(['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WIDTH}x{HEIGHT}',
                       '-i', 'pipe:0', '-pix_fmt', 'yuv420p', '-f', 'rawvideo', 'pipe:1'],
                      np.ascontiguousarray(frames).tobytes())
    return _piani(raw)

def yuv420_a_rgb(piani):
    """Riconverte (Y, U, V) 4:2:0 in RGB, come fa `decodifica`."""
    raw = np.concatenate([p.reshape(len(p), -1) for p in piani], axis=1).tobytes()
    out = _ffmpeg_raw(['-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', f'{WIDTH}x{HEIGHT}',
                       '-i', 'pipe:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'], raw)
    return np.frombuffer(out, dtype=np.uint8).reshape(-1, HEIGHT, WIDTH, 3)

def decodifica_yuv(path):
    """Decodifica il file restituendo i piani (Y, U, V), senza riconversione in RGB."""
    return _piani(_ffmpeg_raw(['-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'yuv420p', 'pipe:1'], None))

def _piani(raw):
    n_y, n_c = WIDTH*HEIGHT, (WIDTH//2)*(HEIGHT//2)
    a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, n_y + 2*n_c)
    return (a[:, :n_y].reshape(-1, HEIGHT, WIDTH),
            a[:, n_y:n_y+n_c].reshape(-1, HEIGHT//2, WIDTH//2),
            a[:, n_y+n_c:].reshape(-1, HEIGHT//2, WIDTH//2))

def mse_y(sorgente, ricostruito):
    """MSE sul piano Y fra ingresso dell'encoder e uscita del decoder, per frame."""
    a, b = sorgente[0].astype(np.float32), ricostruito[0].astype(np.float32)
    if a.shape != b.shape:
        raise ValueError('Numero o dimensioni dei frame differenti')
    return ((a-b)**2).mean(axis=(1, 2))

# --- Struttura del bitstream ---------------------------------------------------

def tipi_frame(path):
    """Tipo (I, P, B) e dimensione in byte di ogni frame, nell'ordine di visualizzazione.
    Richiede ffprobe (incluso nelle distribuzioni di FFmpeg).
    """
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        raise RuntimeError('ffprobe non trovato: usare materiali/frame.csv.')
    result = subprocess.run([ffprobe, '-v', 'error', '-select_streams', 'v:0',
                             '-show_entries', 'frame=pict_type,pkt_size', '-of', 'csv=p=0',
                             str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    righe = []
    for riga in result.stdout.split():
        campi = riga.strip(',').split(',')
        dim = next(int(c) for c in campi if c.isdigit())
        tipo = next(c for c in campi if c in ('I', 'P', 'B'))
        righe.append((tipo, dim))
    return righe
