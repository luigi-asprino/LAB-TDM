# Laboratorio di Trattamento dei Dati Multimediali

Il repository raccoglie i notebook e i materiali delle lezioni di laboratorio del corso di **Trattamento dei Dati Multimediali**. Le attività accompagnano le lezioni teoriche attraverso esperimenti su immagini, video e audio, svolti con Python.

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

Confronto tra i modelli RGB e HSV attraverso esperimenti di conversione, visualizzazione e modifica selettiva del colore. Si osservano il ruolo dei singoli canali, gli effetti delle variazioni di tonalità, saturazione e valore e le differenze tra distanze numeriche e percezione del colore.

**Collegamento con la teoria:** scienza del colore e modelli di colore nelle immagini (modulo 1).

[Apri il notebook](003/notebook.ipynb)

### Lezione 4 — Elaborazione video frame-by-frame con OpenCV

Introduzione al video digitale come sequenza di fotogrammi. Si leggono i metadati, si estraggono frame e si applicano filtri quali conversione in scala di grigi, sfocatura, rilevamento dei bordi e sogliatura. Le operazioni vengono combinate in una pipeline di elaborazione e salvataggio, osservando anche i tempi di esecuzione.

**Collegamento con la teoria:** concetti fondamentali del video digitale (modulo 2).

[Apri il notebook](004/video_editing.ipynb)

### Lezione 5 — Video 360° e proiezioni equirettangolari

Esplorazione della rappresentazione dei video immersivi. A partire da fotogrammi equirettangolari si osservano le distorsioni della proiezione, si costruisce una rappresentazione cubemap e si estraggono viste prospettiche con orientamento e campo visivo modificabili.

**Collegamento con la teoria:** video 360° e rappresentazione del contenuto immersivo (modulo 2).

[Apri il notebook](005/video-360.ipynb)

### Lezione 6 — Compressione video: movimento, bitrate e qualità

Analisi della ridondanza temporale mediante due brevi sequenze sintetiche con velocità di movimento diverse. Si confrontano i residui prima e dopo la compensazione del movimento e si sperimentano tre impostazioni di qualità nella codifica H.264. Il confronto tra dimensioni dei file, bitrate, PSNR e artefatti visivi introduce il compromesso tra compressione e qualità.

L'attività termina con una discussione collettiva, senza consegne. Sono disponibili video già codificati e misure di riferimento per svolgere l'analisi anche senza FFmpeg; la ricodifica richiede FFmpeg con l'encoder `libx264`.

**Collegamento con la teoria:** rateo e distorsione (modulo 5), predizione del movimento e compressione video (modulo 7), H.264/AVC (modulo 8).

[Apri il notebook](006/006-CompressioneVideo.ipynb) · [Guida docente](006/Guida_docente.txt)

### Lezione 7 — Campionamento audio e teorema di Nyquist

Studio sperimentale del campionamento attraverso segnali sinusoidali generati in Python. Si confrontano rappresentazioni e ascolti a frequenze di campionamento diverse, osservando l'aliasing e discutendo il caso limite della soglia di Nyquist. Gli esperimenti collegano la frequenza del segnale alla scelta della frequenza di campionamento.

**Collegamento con la teoria:** digitalizzazione del suono e campionamento (modulo 3).

[Apri il notebook](007/006.ipynb)

### Lezione 8 — Dallo spettro al filtro: FFT, STFT e filtri audio

Analisi dei segnali audio nel dominio della frequenza e nel piano tempo-frequenza mediante FFT e STFT. Si sperimentano filtri passa-basso, passa-alto e un equalizzatore, confrontando forme d'onda, spettri e ascolti per comprendere come il filtraggio modifica il contenuto del segnale.

**Collegamento con la teoria:** filtraggio e qualità audio (modulo 3).

[Apri il notebook](008/007.ipynb)

### Lezione 9 — Compressione audio percettiva: dal PCM al MP3

Esplorazione della quantizzazione e di un modello semplificato del mascheramento psicoacustico, seguita da esperimenti di codifica MP3. Attraverso misure e ascolto si confrontano la rappresentazione PCM e l'audio compresso, collegando il risparmio di spazio agli effetti sulla qualità percepita.

**Collegamento con la teoria:** quantizzazione audio (modulo 3), psicoacustica e compressione audio MPEG (modulo 9).

[Apri il notebook](009/008.ipynb)
