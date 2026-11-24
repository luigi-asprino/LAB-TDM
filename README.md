# Laboratorio di Trattamento dei Dati Multimediali

Il repository raccoglie i notebook e i materiali delle lezioni di laboratorio del corso di **Trattamento dei Dati Multimediali**. Le attività accompagnano le lezioni teoriche attraverso esperimenti su immagini, video e audio, svolti con Python.

## Presentazione del corso

Le slide introduttive del corso sono disponibili qui: [Slide introduttive](https://docs.google.com/presentation/d/1nqwwDtEDrNJQJZThwGhjYkMG8bW5IdWhWEnJCQ_Iyt0/edit?usp=sharing)

## Didattica sincrona

Il percorso comprende **nove lezioni di circa 90 minuti**, svolte attraverso spiegazioni del docente, esecuzione guidata dei notebook, modifica dei parametri e discussione collettiva dei risultati. Gli studenti applicano i concetti teorici, osservano gli effetti delle elaborazioni e confrontano misure quantitative e qualità percepita.

La numerazione organizza il percorso per argomenti; la collocazione delle attività nel calendario segue l'avanzamento della teoria. In particolare, la lezione sulla compressione video richiede l'introduzione alla predizione del movimento e a H.264/AVC.

### Lezione 1 — Manipolazione di immagini con Python (Pillow)

Introduzione alla rappresentazione e alla manipolazione delle immagini digitali. Si impara a caricare e ispezionare un'immagine, eseguire trasformazioni geometriche, convertire le modalità di colore e salvare in formati diversi. Il confronto tra dimensione dei file e artefatti JPEG permette di collegare le operazioni pratiche ai concetti di formato e compressione.

**Collegamento con la teoria:** rappresentazione digitale e formati delle immagini (modulo 1), con un'anticipazione della compressione JPEG.

[Apri il notebook](001/001-Pillow.ipynb)

### Lezione 2 — Analisi dell'istogramma e dei canali colore

Esplorazione dei canali RGB e della distribuzione dei livelli di intensità. Attraverso la visualizzazione degli istogrammi e l'equalizzazione si analizzano contrasto e distribuzione tonale, discutendo anche i limiti dell'applicazione di queste operazioni alle immagini a colori.

**Collegamento con la teoria:** rappresentazione delle immagini, scienza del colore e modelli di colore (modulo 1).

[Apri il notebook](002/002-IstorgrammaCanaliEqualizzazione.ipynb)

### Lezione 3 — RGB e HSV: rappresentazione e percezione del colore

Confronto tra i modelli RGB e HSV attraverso esperimenti di conversione e visualizzazione. In RGB si analizzano il contributo dei singoli canali alla luminanza percepita e il legame tra intensità della luce e valori dei canali. In HSV si modificano separatamente tonalità, saturazione e valore, misurando l'effetto sulla luminanza percepita e quanti pixel escono dall'intervallo valido (clipping). Infine si verifica che cosa si perde nella conversione RGB ↔ HSV: l'errore di quantizzazione a 8 bit e l'instabilità della tonalità nelle zone a bassa saturazione.

Il notebook evidenzia le API OpenCV e NumPy più importanti per lavorare sul colore (`cv2.imread`, `cv2.cvtColor`, `cv2.inRange`, `astype`, `np.clip`, `np.where`) e si chiude con un riepilogo su quando usare ciascuno spazio colore.

**Collegamento con la teoria:** scienza del colore e modelli di colore nelle immagini (modulo 1).

[Apri il notebook](003/notebook.ipynb)

### Lezione 4 — Elaborazione video frame-by-frame con OpenCV

Introduzione al video digitale come sequenza di fotogrammi. Si leggono i metadati, si estraggono frame e si applicano filtri quali conversione in scala di grigi, sfocatura, rilevamento dei bordi e sogliatura. Le operazioni vengono combinate in una pipeline di elaborazione e salvataggio, osservando anche i tempi di esecuzione.

**Collegamento con la teoria:** concetti fondamentali del video digitale (modulo 2).

[Apri il notebook](004/video_editing.ipynb) · [Note dopo la lezione](004/README.md)

### Lezione 5 — Video 360° e proiezioni equirettangolari

Esplorazione della rappresentazione dei video immersivi. Si parte dalla proiezione equirettangolare (ERP): come longitudine e latitudine vengono mappate sulle coordinate dei pixel, perché il frame ha aspect ratio 2:1 e perché la proiezione campiona la sfera in modo non uniforme. Il sovracampionamento verso i poli viene quantificato con il fattore 1/cos(latitudine). Si converte poi un frame ERP in cubemap e si estraggono viewport prospettiche, controllandone l'orientamento (yaw, pitch, roll) e il campo visivo.

Accanto al frame del video, il notebook usa una griglia ERP sintetica di meridiani e paralleli. Poiché la sua geometria sulla sfera è nota, permette di distinguere gli effetti delle diverse proiezioni: la distorsione di campionamento dell'ERP, la sua ridistribuzione sulle facce del cubemap e la distorsione prospettica della viewport, in cui i cerchi massimi tornano rette. Durante la lezione è previsto un breve esercizio sulla sequenza di viewport, che si completa con un esercizio facoltativo per casa.

Il notebook usa la libreria `py360convert` (`pip install py360convert`). Il video di esempio non è incluso nel repository: il link per scaricarlo si trova nel notebook.

**Collegamento con la teoria:** video 360° e rappresentazione del contenuto immersivo (modulo 2).

[Apri il notebook](005/video-360.ipynb)

### Lezione 6 — Compressione video: movimento, bitrate e qualità

Analisi della ridondanza temporale mediante due brevi sequenze sintetiche con velocità di movimento diverse. Si confrontano i residui prima e dopo la compensazione del movimento, anche con raggi di ricerca insufficienti, e si sperimentano tre impostazioni di qualità nella codifica H.264. Il confronto tra dimensioni dei file, bitrate e PSNR introduce il compromesso tra compressione e qualità.

Si analizza poi la struttura del bitstream con `ffprobe`: tipi di fotogramma I, P e B, dimensione di ciascun frame e peso dei keyframe. Un esercizio facoltativo per casa varia l'intervallo fra keyframe.

L'attività non prevede consegne. Sono disponibili video già codificati e misure di riferimento, anche per singolo frame, per svolgere l'analisi anche senza FFmpeg; la ricodifica richiede FFmpeg con l'encoder `libx264` e `ffprobe`.

**Collegamento con la teoria:** rateo e distorsione (modulo 5), predizione del movimento e compressione video (modulo 7), H.264/AVC (modulo 8).

[Apri il notebook](006/006-CompressioneVideo.ipynb) · [Slide introduttive](https://docs.google.com/presentation/d/1smDluSfw80nhMITgG4Pvi7T7g35Q0Vo2560sofdcdkc/edit?usp=sharing)

### Lezione 7 — Campionamento audio e teorema di Nyquist

Studio sperimentale del campionamento con toni puri, uno sweep e un segnale armonico, tutti generati in Python. Si prevede la frequenza di alias e la si verifica con spettro e ascolto. Si confrontano poi due ricostruzioni dei campioni: la ricostruzione a gradini (zero-order hold) lascia immagini udibili, il filtro di ricostruzione del convertitore digitale-analogico le rimuove. Il caso limite $f_s = 2f$ mostra che con due campioni per periodo ampiezza e fase non sono più separabili. Appena sopra la soglia la ricostruzione richiederebbe un filtro ideale: da qui la necessità di un margine.

Uno sweep campionato a 8 kHz rende udibile il ripiegamento delle frequenze. Infine, la decimazione di un dente di sega con e senza filtro anti-aliasing mostra che il filtro attenua l'aliasing senza eliminarlo, e che un filtro più ripido intacca anche la banda utile.

I suoni si ascoltano con un widget nel notebook, che funziona anche su Colab. Non servono file esterni.

**Collegamento con la teoria:** digitalizzazione del suono e campionamento (modulo 3).

[Apri il notebook](007/007.ipynb) · [Guida alla lezione](007/README.md) · [Slide introduttive](https://docs.google.com/presentation/d/1C39EN3gVrnE-6zQE8qHCUaaub1BvB6ppvZGZqDFSDlw/edit?usp=sharing)

### Lezione 8 — Dallo spettro al filtro: FFT, STFT e filtri audio

Analisi dei segnali audio nel dominio della frequenza e nel piano tempo-frequenza mediante FFT e STFT. Si sperimentano filtri passa-basso, passa-alto e un equalizzatore, confrontando forme d'onda, spettri e ascolti per comprendere come il filtraggio modifica il contenuto del segnale.

**Collegamento con la teoria:** filtraggio e qualità audio (modulo 3).

[Apri il notebook](008/008.ipynb)

### Lezione 9 — Compressione audio percettiva: dal PCM al MP3

Esplorazione della quantizzazione e di un modello semplificato del mascheramento psicoacustico, seguita da esperimenti di codifica MP3. Attraverso misure e ascolto si confrontano la rappresentazione PCM e l'audio compresso, collegando il risparmio di spazio agli effetti sulla qualità percepita.

**Collegamento con la teoria:** quantizzazione audio (modulo 3), psicoacustica e compressione audio MPEG (modulo 9).

[Apri il notebook](009/009.ipynb)
