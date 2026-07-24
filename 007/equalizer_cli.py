#!/usr/bin/env python3
"""
equalizer_cli.py — Equalizzatore grafico a N bande, controllabile da linea di comando.

LAB-TDM — Lezione 7 (Filtri audio: passa-basso, passa-alto ed equalizzatore)

Divide il segnale in N bande (filtri Butterworth passa-banda, log-spaziate tra --fmin e --fmax),
applica un guadagno indipendente (in dB) a ciascuna banda e ricompone il segnale in uscita.

Esempi d'uso
------------
Equalizzatore piatto a 6 bande (nessuna modifica), solo per ispezionare le bande generate:
    python equalizer_cli.py --input voce.wav --output voce_eq.wav --bands 6 --gains 0 0 0 0 0 0

Boost dei bassi e taglio degli alti su un brano musicale, con grafico dello spettro prima/dopo:
    python equalizer_cli.py --input musica.wav --output musica_eq.wav \\
        --bands 6 --gains 6 3 0 0 -3 -3 --plot

Attenuazione di una singola banda stretta (es. per ridurre un ronzio attorno ai 50 Hz),
usando più bande per restringere l'intervallo interessato:
    python equalizer_cli.py --input voce.wav --output voce_pulita.wav \\
        --bands 10 --fmin 30 --fmax 8000 \\
        --gains 0 -30 0 0 0 0 0 0 0 0
"""
import argparse
import sys

import numpy as np
import scipy.signal as sig
import soundfile as sf


def crea_bande(n_bande: int, fmin: float, fmax: float):
    """Restituisce n_bande intervalli (f_low, f_high) log-spaziati tra fmin e fmax (Hz)."""
    bordi = np.logspace(np.log10(fmin), np.log10(fmax), n_bande + 1)
    return list(zip(bordi[:-1], bordi[1:]))


def equalizzatore(x: np.ndarray, fs: int, bande, guadagni_db, ordine: int = 4) -> np.ndarray:
    """Applica un equalizzatore grafico a N bande.

    Parametri
    ---------
    x : segnale mono in ingresso
    fs : frequenza di campionamento (Hz)
    bande : lista di tuple (f_low, f_high) in Hz
    guadagni_db : guadagno in dB per banda (stessa lunghezza di `bande`)
    ordine : ordine dei filtri Butterworth passa-banda
    """
    nyq = fs / 2
    y = np.zeros_like(x, dtype=float)
    for (f_low, f_high), g_db in zip(bande, guadagni_db):
        wn = [max(f_low, 1e-6) / nyq, min(f_high / nyq, 0.999)]
        b, a = sig.butter(ordine, wn, btype="bandpass")
        filtrato = sig.filtfilt(b, a, x)
        y += filtrato * (10 ** (g_db / 20))
    picco = np.max(np.abs(y))
    return y / picco if picco > 0 else y


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Equalizzatore grafico a N bande per file audio (LAB-TDM, Lezione 7).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", "-i", required=True, help="File audio di ingresso (wav, mono o stereo).")
    p.add_argument("--output", "-o", required=True, help="File audio di uscita (wav).")
    p.add_argument("--bands", "-n", type=int, default=6, help="Numero di bande (default: 6).")
    p.add_argument(
        "--gains", "-g", type=float, nargs="+", required=True,
        help="Guadagno in dB per ciascuna banda, da bassa ad alta frequenza "
             "(deve avere lunghezza pari a --bands).",
    )
    p.add_argument("--fmin", type=float, default=60.0, help="Frequenza minima delle bande (Hz, default: 60).")
    p.add_argument("--fmax", type=float, default=8000.0, help="Frequenza massima delle bande (Hz, default: 8000).")
    p.add_argument("--order", type=int, default=4, help="Ordine dei filtri Butterworth (default: 4).")
    p.add_argument("--plot", action="store_true", help="Mostra il confronto spettrale prima/dopo (richiede display).")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if len(args.gains) != args.bands:
        print(
            f"Errore: --gains ha {len(args.gains)} valori ma --bands è {args.bands}. "
            "Devono coincidere.",
            file=sys.stderr,
        )
        return 1

    x, fs = sf.read(args.input)
    if x.ndim > 1:
        print("Nota: file stereo in ingresso, converto in mono facendo la media dei canali.")
        x = x.mean(axis=1)

    bande = crea_bande(args.bands, args.fmin, args.fmax)
    print(f"Bande generate (Hz): {[(round(l, 1), round(h, 1)) for l, h in bande]}")
    print(f"Guadagni (dB):       {args.gains}")

    y = equalizzatore(x, fs, bande, args.gains, ordine=args.order)
    sf.write(args.output, y, fs)
    print(f"File equalizzato scritto in: {args.output}")

    if args.plot:
        import matplotlib.pyplot as plt
        from scipy.fft import fft, fftfreq

        def spettro(sig_x, fs):
            n = len(sig_x)
            X = fft(sig_x)
            freqs = fftfreq(n, d=1 / fs)
            meta = n // 2
            return freqs[:meta], np.abs(X[:meta]) / n

        f1, a1 = spettro(x, fs)
        f2, a2 = spettro(y, fs)
        plt.figure(figsize=(8, 3))
        plt.plot(f1, a1, label="originale", alpha=0.7)
        plt.plot(f2, a2, label="equalizzato", alpha=0.7)
        plt.xlim(0, min(fs / 2, args.fmax * 1.5))
        plt.xlabel("Frequenza (Hz)")
        plt.ylabel("Ampiezza")
        plt.legend()
        plt.title("Effetto dell'equalizzatore")
        plt.tight_layout()
        plt.savefig(args.output.rsplit(".", 1)[0] + "_spettro.png")
        print(f"Grafico salvato in: {args.output.rsplit('.', 1)[0]}_spettro.png")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
