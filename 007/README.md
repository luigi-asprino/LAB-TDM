# Lezione 7 — Campionamento audio e teorema di Nyquist

Laboratorio di 90 minuti sul campionamento dei segnali audio. Si campionano toni puri, uno sweep e un segnale armonico a diverse frequenze di campionamento. Per ogni caso si prevede che cosa accadrà e lo si verifica sullo spettro e all'ascolto.

[Slide introduttive](https://docs.google.com/presentation/d/1C39EN3gVrnE-6zQE8qHCUaaub1BvB6ppvZGZqDFSDlw/edit?usp=sharing)

**Collegamento con la teoria:** digitalizzazione del suono e campionamento (modulo 3). Lo spettro è usato come strumento di misura: la trasformata di Fourier è l'argomento della lezione 8, la quantizzazione della lezione 9.

## Contenuto della cartella

| File | Contenuto |
|---|---|
| `007.ipynb` | Il notebook della lezione, già eseguito: grafici e misure sono visibili anche senza rieseguirlo. |
| `lab_audio.py` | Funzioni di supporto: generazione dei segnali, campionamento, ricostruzione, spettro, filtro anti-aliasing, ascolto. |
| `requirements.txt` | Dipendenze Python. |

Tutti i segnali sono generati dal codice: non servono file esterni né una connessione.

## Come eseguire il notebook

1. Installa le dipendenze, una sola volta: `pip install -r requirements.txt`.
2. Apri `007.ipynb` dalla cartella `007` o dalla radice del repository, con un kernel Python 3.
3. Esegui le celle in ordine.

I suoni si ascoltano con un riproduttore integrato nel notebook (`IPython.display.Audio`): premi play quando vuoi ascoltare. Funziona sia in locale sia su Google Colab, perché il suono è riprodotto dal browser.

**Tieni il volume basso**, soprattutto per lo sweep della sezione 4. Gli altoparlanti dei portatili riproducono male le frequenze sotto i 150–200 Hz.

## Percorso della lezione

| Minuti | Sezione | Attività |
|---|---|---|
| 0–10 | 1 | Toni puri e campioni |
| 10–35 | 2 | Aliasing: previsione, spettro, ascolto, due modi di ricostruire il segnale |
| 35–50 | 3 | Il caso limite fs = 2f e il margine |
| 50–60 | 4 | Uno sweep: ascoltare il ripiegamento delle frequenze |
| 60–80 | 5 | Filtro anti-aliasing su un segnale armonico |
| 80–90 | 6 | Previsione e verifica in coppia |

Ogni sezione si apre con una domanda: formula la tua previsione prima di eseguire le celle. La lezione non prevede consegne. In fondo al notebook ci sono tre esercizi facoltativi per casa.

## Concetti e termini

**Campionamento.** Misurare un segnale continuo x(t) a intervalli regolari, negli istanti n/fs. La frequenza di campionamento fs è il numero di misure al secondo.

**Frequenza di Nyquist.** Metà della frequenza di campionamento, fs/2: la frequenza più alta che si può rappresentare correttamente. Il teorema di Nyquist–Shannon garantisce la ricostruzione esatta di un segnale se fs > 2·fmax, dove fmax è la sua componente più alta. La disuguaglianza è stretta: con fs = 2f esatto i campioni dipendono dalla fase del tono e possono essere tutti nulli (sezione 3).

**Aliasing.** Quando una componente supera fs/2, dopo il campionamento ricompare a una frequenza più bassa, detta frequenza di alias:

  f_alias = |f − k·fs|, con k = round(f / fs)

Per esempio, un tono a 3000 Hz campionato a 4000 Hz produce gli stessi campioni di un tono a 1000 Hz. Dopo il campionamento non c'è modo di distinguere i due casi: l'aliasing non si corregge, si previene.

**Ricostruzione.** Per ascoltare i campioni bisogna trasformarli di nuovo in un segnale continuo. Nel notebook si confrontano due modi:
- **ricostruzione a gradini** (in inglese *zero-order hold*, mantenimento di ordine zero): ogni campione resta costante fino al successivo. I gradini aggiungono copie spurie del segnale a frequenze più alte (a k·fs ± f), che si sentono;
- **ricostruzione filtrata:** un filtro passa-basso elimina tutto ciò che sta sopra fs/2 e restituisce un segnale liscio.

**Convertitore digitale-analogico.** Il componente della scheda audio che trasforma i campioni (numeri) in una tensione che muove altoparlanti o cuffie. Nello schema più semplice produce prima una tensione a gradini, poi la fa passare in un filtro passa-basso, detto filtro di ricostruzione, che elimina le copie spurie. I convertitori moderni aumentano prima la frequenza di campionamento con un filtro digitale (sovracampionamento), così da richiedere un filtro analogico più semplice. Nel notebook il filtro è simulato con `scipy.signal.resample_poly`.

**Sweep** (o *chirp*). Un tono puro la cui frequenza cambia in modo continuo nel tempo, come una sirena. Nella sezione 4 la frequenza sale da 50 a 12 000 Hz in 6 secondi. Campionato a 8000 Hz, lo si sente salire fino a 4000 Hz, scendere fino a zero e poi risalire: è il ripiegamento delle frequenze reso udibile.

**Filtro anti-aliasing.** Un filtro passa-basso applicato prima del campionamento, per eliminare le componenti sopra fs/2. Un filtro reale passa gradualmente da "lascia passare" a "blocca": attenua l'aliasing ma non lo elimina, e se è molto ripido intacca anche la parte utile del segnale (sezione 5). Per questo i sistemi reali lasciano un margine tra la banda utile e fs/2: il Compact Disc campiona a 44 100 Hz una banda utile fino a circa 20 kHz.

## Risultati da tenere d'occhio

I valori seguenti sono stati misurati eseguendo il notebook. Servono da riferimento per controllare la propria esecuzione.

| Esperimento | Risultato |
|---|---|
| Tono a 3000 Hz, fs = 4000 Hz, ricostruzione filtrata | Un solo picco, a 1000 Hz; le altre componenti sotto i −65 dB |
| Stesso tono, ricostruzione a gradini | Oltre all'alias a 1000 Hz, una copia a 3000 Hz a circa −10 dB |
| Tono a 1000 Hz, fs = 2000 Hz, fase 0 | Campioni tutti nulli (a meno di errori di arrotondamento) |
| Tono a 1000 Hz, fs = 2004,5 Hz | Due componenti, a 1000 e 1004,5 Hz, entrambe a circa −6 dB: si sente un battimento |
| Dente di sega a 440 Hz, da 44 100 a 11 025 Hz | Energia di alias: −14,3 dB senza filtro, −42,8 dB con un filtro Butterworth di ordine 8 |
