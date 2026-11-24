"""Funzioni di supporto per il laboratorio 7. Nessun download richiesto.

Il "segnale analogico" è una funzione matematica del tempo: campionarlo significa
valutarla negli istanti n/fs, per qualsiasi fs (anche non divisore di 44100 Hz).
"""
from fractions import Fraction
import numpy as np
from scipy import signal

FS_AUDIO = 44100  # Hz, frequenza usata per ascoltare e per disegnare il segnale "continuo"


def tono(f, t, ampiezza=0.5, fase=0.0):
    """Valore di A·sin(2πft + φ) negli istanti t (in secondi)."""
    return ampiezza * np.sin(2 * np.pi * f * np.asarray(t) + fase)


def istanti(fs, durata):
    """Istanti di campionamento n/fs nell'intervallo [0, durata)."""
    return np.arange(int(round(fs * durata))) / fs


def campiona(f, fs, durata=1.0, ampiezza=0.5, fase=0.0):
    """Campiona esattamente un tono puro a frequenza fs. Restituisce (campioni, t)."""
    t = istanti(fs, durata)
    return tono(f, t, ampiezza, fase), t


def frequenza_alias(f, fs):
    """Frequenza apparente dopo il campionamento: f ripiegata in [0, fs/2]."""
    return abs(f - fs * round(f / fs))


def ricostruisci_gradini(campioni, fs, fs_out=FS_AUDIO):
    """Ricostruzione a gradini (zero-order hold, mantenimento di ordine zero):
    ogni campione resta costante fino al successivo."""
    n_out = int(round(len(campioni) * fs_out / fs))
    idx = np.floor(np.arange(n_out) * fs / fs_out).astype(int)
    return campioni[np.minimum(idx, len(campioni) - 1)]


def ricostruisci_filtrata(campioni, fs, fs_out=FS_AUDIO):
    """Ricostruzione con filtro passa-basso (come un convertitore digitale-analogico): ricampionamento
    polifase fs -> fs_out con taglio a fs/2. Richiede fs razionale."""
    r = Fraction(fs_out / fs).limit_denominator(1000)
    return signal.resample_poly(campioni, r.numerator, r.denominator)


def spettro(x, fs):
    """Spettro di ampiezza (finestra di Hann). Un tono di ampiezza A produce un picco ≈ A."""
    w = np.hanning(len(x))
    S = np.abs(np.fft.rfft(x * w)) * 2 / w.sum()
    return np.fft.rfftfreq(len(x), 1 / fs), S


def picchi(x, fs, n=3, fmin=20):
    """Le n componenti più forti dello spettro (frequenza, ampiezza), ordinate per ampiezza."""
    f, S = spettro(x, fs)
    S = np.where(f < fmin, 0, S)
    idx, _ = signal.find_peaks(S)
    idx = idx[np.argsort(S[idx])[::-1][:n]]
    return [(float(f[i]), float(S[i])) for i in idx]


def db(a, rif=0.5):
    """Ampiezza in dB rispetto a rif (default: ampiezza dei toni del notebook)."""
    return 20 * np.log10(np.maximum(a, 1e-12) / rif)


def dente_di_sega(f0, t, fmax=20000, ampiezza=0.5):
    """Dente di sega a banda limitata: armoniche n·f0 fino a fmax, ampiezza ∝ 1/n."""
    n = np.arange(1, int(fmax // f0) + 1)
    x = (np.sin(2 * np.pi * f0 * np.outer(t, n)) / n).sum(axis=1)
    return ampiezza * x / np.abs(x).max()


def chirp(t, f0, f1, durata, ampiezza=0.5):
    """Sweep lineare da f0 a f1 Hz in 'durata' secondi, valutato negli istanti t."""
    return ampiezza * np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t**2 / (2 * durata)))


def ascolta(x, fs=FS_AUDIO, dissolvenza=0.01):
    """Widget audio nel notebook (funziona in locale e su Colab).
    Brevi dissolvenze evitano i 'click' all'inizio e alla fine; normalize=False
    conserva le differenze di volume tra i segnali."""
    from IPython.display import Audio
    x = np.array(x, dtype=float)
    n = min(int(dissolvenza * fs), len(x) // 2)
    if n:
        rampa = np.linspace(0, 1, n)
        x[:n] *= rampa
        x[-n:] *= rampa[::-1]
    return Audio(np.clip(x, -1, 1), rate=int(round(fs)), normalize=False)


def filtro_passabasso(x, fs, fc, ordine=8):
    """Butterworth passa-basso causale (come un filtro analogico prima del convertitore analogico-digitale)."""
    sos = signal.butter(ordine, fc, fs=fs, output='sos')
    return signal.sosfilt(sos, x)


def energia_alias_db(y, fs, f0, tolleranza=3.0):
    """Energia fuori dalle armoniche n·f0 rispetto a quella sulle armoniche, in dB.
    Per un dente di sega non contaminato vale circa -100 dB o meno (solo rumore numerico)."""
    f, S = spettro(y, fs)
    armonica = np.zeros_like(f, dtype=bool)
    for n in range(1, int(fs / 2 // f0) + 1):
        armonica |= np.abs(f - n * f0) < tolleranza
    P = S**2
    return 10 * np.log10(P[~armonica & (f > 20)].sum() / P[armonica].sum())


def componente(y, fs, f, tolleranza=3.0):
    """Ampiezza dello spettro vicino alla frequenza f."""
    ff, S = spettro(y, fs)
    return float(S[np.abs(ff - f) < tolleranza].max())
